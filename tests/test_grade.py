import pytest

from oa_autograding.checks import base
from oa_autograding.checks.base import CheckResult
from oa_autograding.grade import grade
from oa_autograding.spec import parse_spec


@pytest.fixture(autouse=True)
def fake_types(monkeypatch):
    monkeypatch.setattr(base, "_REGISTRY", {})
    base.register("t.contains")(lambda c, p: CheckResult(p["s"] in c.raw, None if p["s"] in c.raw else f"chybí {p['s']}"))
    base.register("t.nofile", needs_file=False)(lambda c, p: CheckResult(True, details="d"))

    def boom(c, p):
        raise RuntimeError("bum")

    base.register("t.boom")(boom)


def make(tasks):
    return parse_spec({"schema": "oa-autograding/checks/v1", "title": "T", "tasks": tasks})


def test_scores_and_labels(repo):
    repo.write("a.md", "ahoj")
    spec = make([{"id": "a", "name": "A", "prefix": "A", "file": "a.md", "checks": [
        {"id": "1", "description": "má ahoj", "type": "t.contains", "s": "ahoj", "points": 2},
        {"id": "2", "description": "má nazdar", "type": "t.contains", "s": "nazdar", "points": 3},
        {"id": "3", "description": "bez souboru", "type": "t.nofile"},
    ]}])
    rep = grade(spec, repo.root)
    t = rep.tasks[0]
    assert (t.score, t.max_score, t.passed) == (3, 6, False)
    assert t.failed_labels == ["A2"]
    assert t.outcomes[1].reason == "chybí nazdar"
    assert t.outcomes[2].details == "d" and t.outcomes[2].file == "a.md"
    assert (rep.score, rep.max_score, rep.passed) == (3, 6, False)
    assert rep.failed_labels == ["A2"]


def test_missing_task_file(repo):
    spec = make([{"id": "b", "name": "B", "prefix": "B", "file": "chybi.md", "checks": [
        {"id": "1", "description": "x", "type": "t.contains", "s": "x"},
        {"id": "2", "description": "y", "type": "t.contains", "s": "y"},
    ]}])
    t = grade(spec, repo.root).tasks[0]
    assert t.missing_file == "chybi.md" and t.score == 0
    assert all("`chybi.md`" in o.reason for o in t.outcomes)


def test_check_file_override(repo):
    repo.write("b.md", "y")
    spec = make([{"id": "b", "name": "B", "file": "a.md", "checks": [
        {"id": "1", "description": "y", "type": "t.contains", "s": "y", "file": "b.md"},
    ]}])
    t = grade(spec, repo.root).tasks[0]
    assert t.passed and t.missing_file == "a.md" and t.outcomes[0].file == "b.md"


def test_check_without_file_needing_file(repo):
    spec = make([{"id": "b", "name": "B", "checks": [{"id": "1", "description": "x", "type": "t.contains", "s": "x"}]}])
    o = grade(spec, repo.root).tasks[0].outcomes[0]
    assert not o.passed and "checks.json" in o.reason


def test_exception_becomes_failed_with_details(repo):
    repo.write("a.md", "x")
    spec = make([{"id": "b", "name": "B", "file": "a.md", "checks": [{"id": "1", "description": "x", "type": "t.boom"}]}])
    o = grade(spec, repo.root).tasks[0].outcomes[0]
    assert not o.passed and o.reason is None and "RuntimeError: bum" in o.details
