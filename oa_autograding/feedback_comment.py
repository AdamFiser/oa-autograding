"""Sticky komentář s výsledkem do Feedback PR. Veškerá práce s GitHubem přes `gh`
(injektovatelná funkce, aby šla testovat bez sítě)."""
from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
from datetime import datetime, timezone
from typing import Callable, Mapping

from oa_autograding.render import MARKER, HistoryEntry, render_comment, render_error_body

GhRunner = Callable[[list[str]], str]


class GhError(RuntimeError):
    """gh skončilo nenulově."""


def default_gh(args: list[str]) -> str:
    proc = subprocess.run(["gh", *args], capture_output=True, text=True, encoding="utf-8", errors="replace")
    if proc.returncode != 0:
        raise GhError(f"gh {' '.join(args[:3])}: {proc.stderr.strip()}")
    return proc.stdout


def find_feedback_pr(gh: GhRunner, repo: str) -> int | None:
    out = gh(["pr", "list", "-R", repo, "--base", "feedback", "--state", "open", "--json", "number", "--limit", "10"])
    numbers = [int(p["number"]) for p in json.loads(out or "[]")]
    return min(numbers) if numbers else None


def list_submit_releases(gh: GhRunner, repo: str) -> list[dict]:
    out = gh(["release", "list", "-R", repo, "--json", "tagName,publishedAt,url", "--limit", "100"])
    rels = [r for r in json.loads(out or "[]") if str(r.get("tagName", "")).startswith("submit/")]
    rels.sort(key=lambda r: r.get("publishedAt", ""), reverse=True)
    return rels


def find_release_for_sha(releases: list[dict], sha: str) -> dict | None:
    suffix = f"-{sha[:7]}"
    return next((r for r in releases if r["tagName"].endswith(suffix)), None)


def release_body(gh: GhRunner, repo: str, tag: str) -> str:
    return gh(["release", "view", tag, "-R", repo, "--json", "body", "--jq", ".body"])


def fetch_result(gh: GhRunner, repo: str, tag: str) -> dict | None:
    try:
        out = gh(["release", "download", tag, "-R", repo, "--pattern", "result.json", "--output", "-"])
        data = json.loads(out)
    except (GhError, json.JSONDecodeError):
        return None
    return data if isinstance(data, dict) else None


def _parse_dt(value: str | None, fallback: str | None) -> datetime:
    for v in (value, fallback):
        if v:
            try:
                return datetime.fromisoformat(v.replace("Z", "+00:00")).astimezone(timezone.utc)
            except ValueError:
                continue
    return datetime.now(timezone.utc)


def build_history(gh: GhRunner, repo: str, releases: list[dict], limit: int) -> list[HistoryEntry]:
    entries: list[HistoryEntry] = []
    for rel in releases[:limit]:
        tag = rel["tagName"]
        result = fetch_result(gh, repo, tag)
        if result is None:
            continue
        failed = [str(t.get("test-name", "")).split(" ", 1)[0] for t in result.get("tests", []) if not t.get("passed")]
        entries.append(HistoryEntry(
            when=_parse_dt(result.get("datetime"), rel.get("publishedAt")),
            sha7=tag.rsplit("-", 1)[-1],
            score=int(result.get("score", 0)),
            max_score=int(result.get("max-score", 0)),
            failed_labels=failed,
            release_url=rel.get("url"),
        ))
    return entries


def find_existing_comment(gh: GhRunner, repo: str, pr: int, marker: str) -> int | None:
    out = gh(["api", f"repos/{repo}/issues/{pr}/comments", "--paginate", "--jq",
              f'.[] | select(.body | contains("{marker}")) | .id'])
    ids = [int(line) for line in out.split() if line.strip().isdigit()]
    return ids[0] if ids else None


def upsert_comment(gh: GhRunner, repo: str, pr: int, body: str, marker: str) -> str:
    with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False, encoding="utf-8") as f:
        json.dump({"body": body}, f, ensure_ascii=False)
        payload = f.name
    existing = find_existing_comment(gh, repo, pr, marker)
    if existing is None:
        gh(["api", "-X", "POST", f"repos/{repo}/issues/{pr}/comments", "--input", payload])
        return "created"
    gh(["api", "-X", "PATCH", f"repos/{repo}/issues/comments/{existing}", "--input", payload])
    return "updated"


def main(gh: GhRunner = default_gh, env: Mapping[str, str] | None = None) -> int:
    env = os.environ if env is None else env
    repo = env["GITHUB_REPOSITORY"]
    sha = env["GITHUB_SHA"]
    marker = env.get("OA_MARKER") or MARKER
    limit = int(env.get("OA_HISTORY_LIMIT") or 20)
    run_url = f"{env.get('GITHUB_SERVER_URL', 'https://github.com')}/{repo}/actions/runs/{env.get('GITHUB_RUN_ID', '')}"
    try:
        pr = find_feedback_pr(gh, repo)
        if pr is None:
            print("::notice::Feedback PR neexistuje (vypnutý, nebo ještě nevznikl) — komentář se nepíše.")
            return 0
        releases = list_submit_releases(gh, repo)
        release = find_release_for_sha(releases, sha)
        if release is None:
            body, history = render_error_body(run_url), []
        else:
            body = release_body(gh, repo, release["tagName"])
            history = build_history(gh, repo, releases, limit)
        action = upsert_comment(gh, repo, pr, render_comment(body, history, marker), marker)
        print(f"oa-autograding: komentář ve Feedback PR #{pr} {action}.")
        return 0
    except GhError as e:
        print(f"::error::oa-autograding: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
