import oa_autograding


def test_version_is_string():
    assert isinstance(oa_autograding.__version__, str)


from pathlib import Path

import pytest

from oa_autograding.checks import base
from oa_autograding.checks.base import CheckContext, CheckResult, strip_code_blocks


def test_strip_code_blocks_keeps_line_count():
    text = "a\n```md\n# ne nadpis\n```\nb"
    out = strip_code_blocks(text)
    assert "# ne nadpis" not in out
    assert out.count("\n") == text.count("\n")


def test_strip_html_comments_keeps_line_count():
    text = "a\n<!-- x\n# ne nadpis\n[k](#k) -->\nb"
    out = strip_code_blocks(text)
    assert "# ne nadpis" not in out
    assert "(#k)" not in out
    assert out.count("\n") == text.count("\n")


def test_register_and_get(monkeypatch):
    monkeypatch.setattr(base, "_REGISTRY", {})

    @base.register("test.echo", needs_file=False)
    def echo(ctx, params):
        return CheckResult(True, params.get("msg"))

    reg = base.get("test.echo")
    assert reg.needs_file is False
    assert reg.fn(CheckContext(Path("."), None), {"msg": "ok"}) == CheckResult(True, "ok")
    assert base.is_registered("test.echo")
    assert base.registered_types() == ["test.echo"]


def test_register_twice_fails(monkeypatch):
    monkeypatch.setattr(base, "_REGISTRY", {})
    base.register("x")(lambda c, p: CheckResult(True))
    with pytest.raises(RuntimeError):
        base.register("x")(lambda c, p: CheckResult(True))


def test_get_unknown():
    with pytest.raises(base.UnknownCheckType):
        base.get("neexistuje")


def test_for_file_reads_bom_and_strips_code(repo):
    repo.write("a.md", "﻿# H\n```\n# x\n```\n")
    ctx = CheckContext.for_file(repo.root, "a.md")
    assert ctx.raw.startswith("# H")
    assert "# x" not in ctx.no_code
    assert ctx.file == repo.root / "a.md"
