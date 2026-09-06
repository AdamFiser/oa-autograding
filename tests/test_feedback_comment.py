import json

import pytest

from oa_autograding import feedback_comment as fc
from oa_autograding.render import MARKER

REPO = "org/1sk-ctvrtek-10-markdown-zak"
SHA = "a1b2c3d4e5f6a7b8"
RELEASES = [
    {"tagName": "submit/2026-09-05T12-32-05Z-a1b2c3d", "publishedAt": "2026-09-05T12:32:20Z", "url": "https://r/2"},
    {"tagName": "submit/2026-09-05T12-10-00Z-9f8e7d6", "publishedAt": "2026-09-05T12:10:20Z", "url": "https://r/1"},
    {"tagName": "latest", "publishedAt": "2026-09-05T12:32:21Z", "url": "https://r/latest"},
]
RESULTS = {
    "submit/2026-09-05T12-32-05Z-a1b2c3d": {"datetime": "2026-09-05T12:32:05Z", "score": 3, "max-score": 4,
        "tests": [{"test-name": "A1 X", "passed": True}, {"test-name": "A2 Kotva", "passed": False}]},
    "submit/2026-09-05T12-10-00Z-9f8e7d6": {"datetime": "2026-09-05T12:10:00Z", "score": 1, "max-score": 4,
        "tests": [{"test-name": "A1 X", "passed": False}, {"test-name": "A2 Kotva", "passed": False}]},
}


class FakeGh:
    def __init__(self, prs=(7,), comments=(), releases=RELEASES, results=RESULTS, body="TĚLO"):
        self.prs, self.comments, self.releases, self.results, self.body = list(prs), list(comments), releases, results, body
        self.calls: list[list[str]] = []

    def __call__(self, args):
        self.calls.append(args)
        a = " ".join(args)
        if args[:2] == ["pr", "list"]:
            return json.dumps([{"number": n} for n in self.prs])
        if args[:2] == ["release", "list"]:
            return json.dumps(self.releases)
        if args[:2] == ["release", "view"]:
            return self.body
        if args[:2] == ["release", "download"]:
            tag = args[2]
            if tag not in self.results:
                raise fc.GhError("asset not found")
            return json.dumps(self.results[tag])
        if args[0] == "api" and "/comments" in a and "-X" not in args:
            return "\n".join(str(c) for c in self.comments)
        if args[0] == "api" and "-X" in args:
            return "{}"
        raise AssertionError(f"neočekávané volání gh {args}")


def test_find_feedback_pr():
    assert fc.find_feedback_pr(FakeGh(prs=[9, 7]), REPO) == 7
    assert fc.find_feedback_pr(FakeGh(prs=[]), REPO) is None


def test_releases_filter_and_match():
    rels = fc.list_submit_releases(FakeGh(), REPO)
    assert [r["tagName"] for r in rels] == [RELEASES[0]["tagName"], RELEASES[1]["tagName"]]
    assert fc.find_release_for_sha(rels, SHA)["url"] == "https://r/2"
    assert fc.find_release_for_sha(rels, "0000000") is None


def test_build_history_limit_and_labels():
    rels = fc.list_submit_releases(FakeGh(), REPO)
    hist = fc.build_history(FakeGh(), REPO, rels, limit=1)
    assert len(hist) == 1 and hist[0].sha7 == "a1b2c3d" and hist[0].failed_labels == ["A2"]
    assert hist[0].score == 3 and hist[0].release_url == "https://r/2"
    assert hist[0].when.isoformat() == "2026-09-05T12:32:05+00:00"


def test_build_history_skips_release_without_result():
    gh = FakeGh(results={k: v for k, v in RESULTS.items() if "a1b2c3d" in k})
    hist = fc.build_history(gh, REPO, fc.list_submit_releases(gh, REPO), limit=20)
    assert [h.sha7 for h in hist] == ["a1b2c3d"]


def test_upsert_creates_then_updates(tmp_path, monkeypatch):
    gh = FakeGh(comments=[])
    assert fc.upsert_comment(gh, REPO, 7, "text", MARKER) == "created"
    post = [c for c in gh.calls if "-X" in c][-1]
    assert "POST" in post and f"repos/{REPO}/issues/7/comments" in post
    gh2 = FakeGh(comments=[555])
    assert fc.upsert_comment(gh2, REPO, 7, "text", MARKER) == "updated"
    patch = [c for c in gh2.calls if "-X" in c][-1]
    assert "PATCH" in patch and f"repos/{REPO}/issues/comments/555" in patch


def test_main_happy_path(capsys):
    gh = FakeGh(comments=[555])
    env = {"GITHUB_REPOSITORY": REPO, "GITHUB_SHA": SHA, "GITHUB_RUN_ID": "1"}
    assert fc.main(gh, env) == 0
    patch = [c for c in gh.calls if "-X" in c][-1]
    payload = json.loads(open(patch[patch.index("--input") + 1], encoding="utf-8").read())
    assert payload["body"].startswith(MARKER) and "TĚLO" in payload["body"]
    assert "Historie odevzdání (2)" in payload["body"]


def test_main_no_pr(capsys):
    gh = FakeGh(prs=[])
    assert fc.main(gh, {"GITHUB_REPOSITORY": REPO, "GITHUB_SHA": SHA}) == 0
    assert "::notice::" in capsys.readouterr().out
    assert not any("-X" in c for c in gh.calls)


def test_main_no_release_posts_error_body():
    gh = FakeGh(releases=[RELEASES[1]], results={})
    env = {"GITHUB_REPOSITORY": REPO, "GITHUB_SHA": SHA, "GITHUB_RUN_ID": "42"}
    assert fc.main(gh, env) == 0
    post = [c for c in gh.calls if "-X" in c][-1]
    payload = json.loads(open(post[post.index("--input") + 1], encoding="utf-8").read())
    assert "technické chybě" in payload["body"] and f"{REPO}/actions/runs/42" in payload["body"]


def test_main_gh_error_returns_1(capsys):
    def broken(args):
        raise fc.GhError("HTTP 500")

    assert fc.main(broken, {"GITHUB_REPOSITORY": REPO, "GITHUB_SHA": SHA}) == 1
    assert "::error::" in capsys.readouterr().out
