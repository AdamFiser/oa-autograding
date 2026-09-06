import json

import pytest

from oa_autograding import spec as specmod
from oa_autograding.checks import base
from oa_autograding.checks.base import CheckResult
from oa_autograding.spec import SpecError, load_spec, parse_spec, resolve_docs


@pytest.fixture(autouse=True)
def fake_types(monkeypatch):
    monkeypatch.setattr(base, "_REGISTRY", {})
    base.register("t.a")(lambda c, p: CheckResult(True))
    base.register("t.b", needs_file=False)(lambda c, p: CheckResult(True))


def minimal(**over):
    data = {
        "schema": "oa-autograding/checks/v1",
        "title": "Cvičení",
        "docs": "https://example.com/prezentace/",
        "tasks": [
            {
                "id": "ukol-a",
                "name": "Úkol A",
                "prefix": "A",
                "file": "a.md",
                "checks": [
                    {"id": "one", "description": "Jedna", "type": "t.a", "hint": "Nápověda", "docs": "#kap"},
                    {"id": "two", "description": "Dvě", "type": "t.b", "points": 3, "min_items": 4},
                ],
            },
            {"id": "ukol-b", "name": "Úkol B", "checks": [{"id": "x", "description": "X", "type": "t.a", "file": "b.md"}]},
        ],
    }
    data.update(over)
    return data


def test_parse_minimal():
    s = parse_spec(minimal())
    assert s.title == "Cvičení"
    a, b = s.tasks
    assert [c.label for c in a.checks] == ["A1", "A2"]
    assert [c.label for c in b.checks] == ["1"]
    assert a.checks[1].points == 3 and a.checks[1].params == {"min_items": 4}
    assert a.checks[0].points == 1 and a.checks[0].params == {}
    assert a.max_points == 4 and s.max_points == 5
    assert b.checks[0].file == "b.md" and a.checks[0].file is None


def test_resolve_docs():
    s = parse_spec(minimal())
    assert resolve_docs(s, s.tasks[0].checks[0]) == "https://example.com/prezentace/#kap"
    assert resolve_docs(s, s.tasks[0].checks[1]) == "https://example.com/prezentace/"
    s2 = parse_spec(minimal(docs=None))
    assert resolve_docs(s2, s2.tasks[0].checks[0]) is None
    s3 = parse_spec(minimal(tasks=[{"id": "t", "name": "T", "checks": [
        {"id": "c", "description": "C", "type": "t.a", "docs": "https://jinde.cz/x"}]}]))
    assert resolve_docs(s3, s3.tasks[0].checks[0]) == "https://jinde.cz/x"


@pytest.mark.parametrize("mutate, msg", [
    (lambda d: d.update(schema="jiné"), "schema"),
    (lambda d: d.pop("title"), "title"),
    (lambda d: d.update(tasks=[]), "tasks"),
    (lambda d: d["tasks"][0]["checks"][0].update(type="t.zzz"), "neznámý typ"),
    (lambda d: d["tasks"][0]["checks"][0].update(points=0), "points"),
    (lambda d: d["tasks"][0]["checks"][0].update(points=True), "points"),
    (lambda d: d["tasks"][0]["checks"][1].update(id="one"), "duplicit"),
    (lambda d: d["tasks"][1].update(id="ukol-a"), "duplicit"),
    (lambda d: d["tasks"][0]["checks"][0].pop("description"), "description"),
])
def test_invalid(mutate, msg):
    d = minimal()
    mutate(d)
    with pytest.raises(SpecError, match=msg):
        parse_spec(d)


def test_load_spec_errors(tmp_path):
    with pytest.raises(SpecError, match="neexistuje"):
        load_spec(tmp_path / "chybi.json")
    bad = tmp_path / "bad.json"
    bad.write_text("{", encoding="utf-8")
    with pytest.raises(SpecError, match="neplatný JSON"):
        load_spec(bad)
    ok = tmp_path / "ok.json"
    ok.write_text("﻿" + json.dumps(minimal(), ensure_ascii=False), encoding="utf-8")
    assert load_spec(ok).title == "Cvičení"
