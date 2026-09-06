"""Vstupní bod pro autograder.py v classroom50: checks.json vedle autograderu → result.json + release-body.md."""
from __future__ import annotations

import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Mapping

from oa_autograding.grade import grade
from oa_autograding.render import GradeEnv, render_release_body
from oa_autograding.result import build_result
from oa_autograding.spec import SpecError, load_spec


def main(bundle_dir: Path, repo_root: Path | None = None, env: Mapping[str, str] | None = None) -> int:
    env = os.environ if env is None else env
    repo_root = repo_root or Path.cwd()
    try:
        spec = load_spec(Path(bundle_dir) / "checks.json")
    except SpecError as e:
        print(f"oa-autograding: neplatný checks.json — {e}", file=sys.stderr)
        return 2
    report = grade(spec, repo_root)
    now = datetime.now(timezone.utc)
    genv = GradeEnv(
        commit_sha=env.get("GITHUB_SHA", ""),
        commit_url=env.get("COMMIT_URL") or None,
        release_url=env.get("RELEASE_URL") or None,
        graded_at=now,
    )
    (repo_root / "result.json").write_text(
        json.dumps(build_result(report, env, now), ensure_ascii=False, indent=2), encoding="utf-8"
    )
    (repo_root / "release-body.md").write_text(render_release_body(report, genv), encoding="utf-8")
    print(f"oa-autograding: {report.score}/{report.max_score} bodů, nesplněno: {', '.join(report.failed_labels) or 'nic'}")
    return 0
