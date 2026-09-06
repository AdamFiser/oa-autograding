import json
from datetime import datetime, timezone
from pathlib import Path

import pytest

from oa_autograding.checks import base
from oa_autograding.checks.base import CheckResult
from oa_autograding.grade import grade
from oa_autograding.result import build_result
from oa_autograding.runner import main
from oa_autograding.spec import parse_spec

T0 = datetime(2026, 9, 5, 12, 32, 5, tzinfo=timezone.utc)
ENV = {
    "CLASSROOM": "1sk-ctvrtek", "ASSIGNMENT": "10-markdown", "SUBMISSION_TAG": "submit/2026-09-05T12-32-05Z-a1b2c3d",
    "COMMIT_URL": "https://c", "RELEASE_URL": "https://r", "REVIEW_URL": "https://v", "GITHUB_SHA": "a1b2c3d4e5f6",
}


@pytest.fixture(autouse=True)
def fake_types(monkeypatch):
    monkeypatch.setattr(base, "_REGISTRY", {})
    base.register("t.ok")(lambda c, p: CheckResult(True))
    base.register("t.ko")(lambda c, p: CheckResult(False, "ne"))


SPEC = {"schema": "oa-autograding/checks/v1", "title": "T", "tasks": [
    {"id": "a", "name": "A", "prefix": "A", "file": "a.md", "checks": [
        {"id": "1", "description": "x" * 120, "type": "t.ok", "points": 2},
        {"id": "2", "description": "Kotva", "type": "t.ko"},
    ]},
]}


def test_build_result(repo):
    repo.write("a.md", "x")
    r = build_result(grade(parse_spec(SPEC), repo.root), ENV, T0)
    assert r["schema"] == "classroom50/result/v1"
    assert (r["classroom"], r["assignment"], r["submission"]) == ("1sk-ctvrtek", "10-markdown", ENV["SUBMISSION_TAG"])
    assert (r["commit"], r["release"], r["review"]) == ("https://c", "https://r", "https://v")
    assert r["datetime"] == "2026-09-05T12:32:05Z"
    assert (r["score"], r["max-score"]) == (2, 3)
    assert r["tests"][1] == {"test-name": "A2 Kotva", "passed": False, "score": 0, "max-score": 1}
    assert r["tests"][0]["test-name"].startswith("A1 ") and len(r["tests"][0]["test-name"].encode()) <= 100


def test_runner_writes_files(repo, tmp_path):
    bundle = tmp_path / "bundle"
    bundle.mkdir()
    (bundle / "checks.json").write_text(json.dumps(SPEC), encoding="utf-8")
    repo.write("a.md", "x")
    assert main(bundle, repo.root, ENV) == 0
    result = json.loads((repo.root / "result.json").read_text(encoding="utf-8"))
    assert result["score"] == 2
    body = (repo.root / "release-body.md").read_text(encoding="utf-8")
    assert body.startswith("**Automatická kontrola: 2 z 3 bodů**") and "`a1b2c3d`" in body


def test_runner_invalid_spec(repo, tmp_path, capsys):
    bundle = tmp_path / "bundle"
    bundle.mkdir()
    (bundle / "checks.json").write_text("{}", encoding="utf-8")
    assert main(bundle, repo.root, ENV) == 2
    assert "schema" in capsys.readouterr().err
    assert not (repo.root / "result.json").exists()
