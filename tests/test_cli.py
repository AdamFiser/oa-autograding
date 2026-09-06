import json

import pytest

from oa_autograding.checks import base
from oa_autograding.checks.base import CheckResult
from oa_autograding.cli import main


@pytest.fixture(autouse=True)
def fake_types(monkeypatch):
    monkeypatch.setattr(base, "_REGISTRY", {})
    base.register("t.ok")(lambda c, p: CheckResult(True))
    base.register("t.ko")(lambda c, p: CheckResult(False, "ne"))


def write_spec(tmp_path, ko=True):
    checks = [{"id": "1", "description": "OK", "type": "t.ok"}]
    if ko:
        checks.append({"id": "2", "description": "KO", "type": "t.ko"})
    p = tmp_path / "checks.json"
    p.write_text(json.dumps({"schema": "oa-autograding/checks/v1", "title": "T", "tasks": [
        {"id": "a", "name": "A", "file": "a.md", "checks": checks}]}), encoding="utf-8")
    return p


def test_check_fail_exit_1(repo, tmp_path, capsys):
    repo.write("a.md", "x")
    code = main(["check", "--spec", str(write_spec(tmp_path)), "--repo", str(repo.root)])
    out = capsys.readouterr().out
    assert code == 1 and "1 z 2 bodů" in out and "| 2 | ❌ | KO |" in out


def test_check_pass_exit_0(repo, tmp_path, capsys):
    repo.write("a.md", "x")
    assert main(["check", "--spec", str(write_spec(tmp_path, ko=False)), "--repo", str(repo.root)]) == 0
    assert "Všechny požadavky splněny" in capsys.readouterr().out


def test_check_json(repo, tmp_path, capsys):
    repo.write("a.md", "x")
    main(["check", "--spec", str(write_spec(tmp_path)), "--repo", str(repo.root), "--json"])
    data = json.loads(capsys.readouterr().out)
    assert data["schema"] == "classroom50/result/v1" and data["score"] == 1


def test_check_invalid_spec(tmp_path, capsys):
    bad = tmp_path / "bad.json"
    bad.write_text("{}", encoding="utf-8")
    assert main(["check", "--spec", str(bad), "--repo", str(tmp_path)]) == 2
    assert "schema" in capsys.readouterr().err


def test_types(capsys):
    assert main(["types"]) == 0
    assert "t.ko\nt.ok" in capsys.readouterr().out
