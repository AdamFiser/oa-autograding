import sys

import pytest

from oa_autograding.checks import base
from oa_autograding.checks.base import CheckContext
import oa_autograding.checks  # noqa: F401

PY = f'"{sys.executable}"'


def run(repo, **params):
    return base.get("run").fn(CheckContext(repo.root, None), params)


def test_registered_without_file():
    assert base.get("run").needs_file is False


def test_expected_included(repo):
    res = run(repo, cmd=f"{PY} -c \"print('Ahoj svete')\"", expected="Ahoj")
    assert res.passed and "stdout" in res.details


def test_expected_exact_fail(repo):
    res = run(repo, cmd=f"{PY} -c \"print('Ahoj')\"", expected="Ahoj svete", comparison="exact")
    assert not res.passed and "neodpovídá" in res.reason


def test_expected_regex(repo):
    assert run(repo, cmd=f"{PY} -c \"print(42)\"", expected=r"^\d+$", comparison="regex").passed


def test_exit_code(repo):
    assert run(repo, cmd=f"{PY} -c \"raise SystemExit(3)\"", exit_code=3).passed
    res = run(repo, cmd=f"{PY} -c \"raise SystemExit(3)\"")
    assert not res.passed and "3" in res.reason


def test_stdin_and_cwd(repo):
    repo.write("vstup.txt", "x")
    res = run(repo, cmd=f"{PY} -c \"import sys,os; print(sys.stdin.read().upper(), os.path.exists('vstup.txt'))\"", stdin="ahoj", expected="AHOJ True")
    assert res.passed


def test_timeout(repo):
    res = run(repo, cmd=f"{PY} -c \"import time; time.sleep(5)\"", timeout=0.5)
    assert not res.passed and "neskončil" in res.reason


def test_missing_cmd(repo):
    res = run(repo)
    assert not res.passed and "checks.json" in res.reason


def test_bad_comparison(repo):
    with pytest.raises(ValueError):
        run(repo, cmd=f"{PY} -c \"print(1)\"", expected="1", comparison="zzz")
