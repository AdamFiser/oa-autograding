from datetime import datetime, timezone

import pytest

from oa_autograding.checks import base
from oa_autograding.checks.base import CheckResult
from oa_autograding.grade import grade
from oa_autograding.render import (
    MARKER, GradeEnv, HistoryEntry, format_cz, of_word, render_comment,
    render_error_body, render_history, render_release_body,
)
from oa_autograding.spec import parse_spec

T0 = datetime(2026, 9, 5, 12, 32, tzinfo=timezone.utc)  # 14:32 v Praze (letní čas)


@pytest.fixture(autouse=True)
def fake_types(monkeypatch):
    monkeypatch.setattr(base, "_REGISTRY", {})
    base.register("t.ok")(lambda c, p: CheckResult(True))
    base.register("t.ko")(lambda c, p: CheckResult(False, "Důvod | s trubkou."))


def report(repo, extra_b=None):
    repo.write("a.md", "x")
    repo.write("b.md", "x")
    spec = parse_spec({"schema": "oa-autograding/checks/v1", "title": "Cvičení", "docs": "https://d.cz/p/", "tasks": [
        {"id": "a", "name": "Úkol A", "prefix": "A", "file": "a.md", "checks": [
            {"id": "1", "description": "Nadpisy", "type": "t.ok", "points": 2},
            {"id": "2", "description": "Kotva", "type": "t.ko", "hint": "Použij `[x](#y)`.", "docs": "#odkazy"},
        ]},
        {"id": "b", "name": "Úkol B", "prefix": "B", "file": extra_b or "b.md", "checks": [
            {"id": "1", "description": "Vše", "type": "t.ok"},
        ]},
    ]})
    return grade(spec, repo.root)


def test_format_cz():
    assert format_cz(T0) == "5. 9. 2026 14:32"
    assert format_cz(T0, with_year=False) == "5. 9. 14:32"


def test_of_word():
    assert of_word(1) == "bodu" and of_word(4) == "bodů" and of_word(27) == "bodů"


def test_release_body(repo):
    body = render_release_body(report(repo), GradeEnv("a1b2c3d4e5", "https://c", "https://r", T0))
    assert body.startswith("**Automatická kontrola: 3 z 4 bodů**")
    assert "`a1b2c3d`" in body and "5. 9. 2026 14:32" in body
    assert "### Úkol A · `a.md` · 2/3" in body
    assert "| A1 | ✅ | Nadpisy |  |" in body  # prázdná nápověda = dvě mezery mezi svislítky
    assert "| A2 | ❌ | Kotva | Důvod \\| s trubkou. Použij `[x](#y)`. Viz [prezentace](https://d.cz/p/#odkazy). |" in body
    assert "### Úkol B · `b.md` · 1/1" in body and "Všechny požadavky splněny. 🎉" in body
    assert "[Release](https://r)" in body and "Dotazy k hodnocení pište sem do PR." in body
    assert MARKER not in body


def test_release_body_missing_file(repo):
    body = render_release_body(report(repo, extra_b="chybi.md"), GradeEnv("a1b2c3d", None, None, T0))
    assert "### Úkol B · `chybi.md` · 0/1" in body
    assert "Soubor `chybi.md` v repozitáři není" in body and "B1" in body
    assert "| B1 |" not in body
    assert "[Release]" not in body


def test_history_and_comment():
    entries = [
        HistoryEntry(T0, "a1b2c3d", 3, 4, ["A2"], "https://r/1"),
        HistoryEntry(datetime(2026, 9, 5, 12, 10, tzinfo=timezone.utc), "9f8e7d6", 1, 4, ["A1", "A2", "B1"], None),
    ]
    h = render_history(entries)
    assert "<summary>Historie odevzdání (2)</summary>" in h
    assert "| 5. 9. 14:32 | [a1b2c3d](https://r/1) | 3/4 | A2 |" in h
    assert "| 5. 9. 14:10 | 9f8e7d6 | 1/4 | A1, A2, B1 |" in h
    assert render_history([]) == ""
    c = render_comment("TĚLO", entries)
    assert c.startswith(MARKER + "\n") and "TĚLO" in c and "<details>" in c
    assert render_comment("TĚLO", []).rstrip().endswith("TĚLO")


def test_error_body():
    b = render_error_body("https://run")
    assert "technické chybě" in b and "https://run" in b
