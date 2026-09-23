import pytest

from oa_autograding.checks import base
from oa_autograding.checks.base import CheckContext
import oa_autograding.checks  # noqa: F401


def check(repo, type_name, src, **params):
    repo.write("r.py", src)
    return base.get(type_name).fn(CheckContext.for_file(repo.root, "r.py"), params)


def test_eval_type_strict(repo):
    src = 'data = [{"obrat": "5"}]\n'
    res = check(repo, "py.eval", src, expr='data[0]["obrat"]', expected=5)
    assert not res.passed and "'5' (str)" in res.reason and "5 (int)" in res.reason
    assert check(repo, "py.eval", 'x = 5.0\n', expr="x", expected=5).passed
    assert not check(repo, "py.eval", 'x = 1\n', expr="x", expected=True).passed


def test_eval_survives_crash_later_in_program(repo):
    src = 'data = [1, "2"]\nprint(sum(data))\n'
    res = check(repo, "py.eval", src, expr="data[1]", expected=2)
    assert not res.passed and "TypeError" in res.reason and "řádek 2" in res.reason
    assert check(repo, "py.eval", src, expr="data[0]", expected=1).passed


def test_eval_input_and_syntax_error(repo):
    assert check(repo, "py.eval", 'x = 3\ny = input()\n', expr="x", expected=3).passed
    res = check(repo, "py.eval", "x = (\n", expr="x", expected=3)
    assert not res.passed and "syntaktickou" in res.reason


def test_eval_timeout(repo):
    res = check(repo, "py.eval", "while True: pass\n", expr="1", expected=1, timeout=1)
    assert not res.passed and "neskončil" in res.reason


CASES = [{"args": [{"a": 1, "b": 2}], "expected": 3}, {"args": [{"a": 1}], "expected": 1}]


def test_function_found_by_behaviour(repo):
    src = "def jina(x):\n    return 0\n\ndef soucet(d):\n    return d['a'] + d.get('b', 0)\n"
    res = check(repo, "py.function", src, cases=CASES)
    assert res.passed and "soucet" in res.details


def test_function_kwargs_from_dict(repo):
    src = "def soucet(a, b=0):\n    print('ladim')\n    return a + b\n"
    assert check(repo, "py.function", src, cases=CASES).passed


def test_function_reports_nearest(repo):
    src = "def soucet(d):\n    return str(d['a'] + d['b'])\n"
    res = check(repo, "py.function", src, cases=CASES)
    assert not res.passed and "'3' (str)" in res.reason and "3 (int)" in res.reason


def test_function_none_or_error(repo):
    assert "není žádná funkce" in check(repo, "py.function", "x = 1\n", cases=CASES).reason
    res = check(repo, "py.function", "def soucet(d):\n    return d['a'] + d['b']\n", cases=CASES)
    assert not res.passed and "KeyError" in res.reason


def test_function_does_not_mutate_between_cases(repo):
    src = "def f(d):\n    d['a'] += 1\n    return d['a']\n"
    cases = [{"args": [{"a": 1}], "expected": 2}, {"args": [{"a": 1}], "expected": 2}]
    assert check(repo, "py.function", src, cases=cases).passed


@pytest.mark.parametrize("construct, yes, no", [
    ("for", "for x in y: pass", "while 0: pass"),
    ("fstring", 'print(f"{x}")', 'print("x")'),
    ("dict-lookup", 'b = {"a": 3, "b": 2}', 'z = {"nazev": "A", "obrat": 5}'),
    ("in-collection", 'x in ("CZ", "SK")', "x in y"),
    ("dict-get-default", 'd.get("k", False)', 'd.get("k")'),
    ("default-param", "def f(x=False): pass", "def f(x): pass"),
    ("sort-key", "sorted(s, key=len, reverse=True)", "sorted(s)"),
])
def test_uses(repo, construct, yes, no):
    assert check(repo, "py.uses", yes + "\n", any_of=[construct]).passed
    res = check(repo, "py.uses", no + "\n", any_of=[construct])
    assert not res.passed and "V kódu není" in res.reason


def test_uses_invalid_param(repo):
    assert "checks.json" in check(repo, "py.uses", "x = 1\n", any_of=["zzz"]).reason


def test_file_contains(repo):
    src = "x = 1  # OPRAVA: typ\ny = 2  #oprava: překlep\n"
    assert check(repo, "file.contains", src, text="# OPRAVA:", min_count=2).passed
    res = check(repo, "file.contains", src, text="# OPRAVA:", min_count=5)
    assert not res.passed and "2 řádcích" in res.reason


def test_relative_repo_root(repo, monkeypatch):
    repo.write("r.py", "x = 5\n")
    monkeypatch.chdir(repo.root.parent)
    rel = repo.root.relative_to(repo.root.parent)
    res = base.get("py.eval").fn(CheckContext.for_file(rel, "r.py"), {"expr": "x", "expected": 5})
    assert res.passed, res.reason
