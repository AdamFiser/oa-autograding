from pathlib import Path

from oa_autograding.checks import base
from oa_autograding.checks.base import CheckContext
import oa_autograding.checks  # noqa: F401


def test_exists_pass(repo):
    repo.write("a.md", "x")
    reg = base.get("file.exists")
    assert reg.needs_file is False
    assert reg.fn(CheckContext(repo.root, repo.root / "a.md"), {}).passed


def test_exists_fail(repo):
    res = base.get("file.exists").fn(CheckContext(repo.root, repo.root / "chybi.md"), {})
    assert not res.passed
    assert "`chybi.md`" in res.reason


def test_exists_without_file(repo):
    res = base.get("file.exists").fn(CheckContext(repo.root, None), {})
    assert not res.passed and "checks.json" in res.reason


def test_no_marker_pass(repo):
    repo.write("a.md", "# Hotovo\n")
    ctx = CheckContext.for_file(repo.root, "a.md")
    assert base.get("file.no-marker").fn(ctx, {}).passed


def test_no_marker_fail_counts_and_lines(repo):
    repo.write("a.md", "<!-- TODO 1: x -->\nok\n<!--TODO 2 -->\n")
    ctx = CheckContext.for_file(repo.root, "a.md")
    res = base.get("file.no-marker").fn(ctx, {})
    assert not res.passed
    assert "2" in res.reason and "řádky 1, 3" in res.reason


def test_no_marker_custom(repo):
    repo.write("a.py", "pass  # FIXME\n")
    ctx = CheckContext.for_file(repo.root, "a.py")
    assert not base.get("file.no-marker").fn(ctx, {"marker": "FIXME"}).passed
