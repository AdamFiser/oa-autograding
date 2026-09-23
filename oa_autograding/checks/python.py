"""Kontroly programu v Pythonu nad souborem z `file`.

- `py.eval`: `expr` (povinné), `expected` (JSON hodnota), `timeout` (`10` s) — vykoná
  program žáka a porovná hodnotu výrazu včetně typu ("5" ≠ 5, True ≠ 1; int a float
  se smí zaměnit). Vhodné na data: `poptavka[2]["obrat"]`.
- `py.function`: `cases` (povinné, `[{"args": [...], "expected": …}]`), `name`
  (volitelné; bez něj se zkusí každá funkce ze souboru), `timeout` (`10` s) — projde,
  když jedna funkce vrátí pro všechny vstupy očekávanou hodnotu. Jediný slovníkový
  argument se zkusí předat i jako pojmenované parametry (`f(**zakazka)`).
- `py.uses`: `any_of` (povinné, seznam konstrukcí z `CONSTRUCTS`) — statická analýza
  (AST), kód se nespouští; projde, když je v kódu alespoň jedna z konstrukcí.

`py.eval` a `py.function` spouští program v podprocesu (`_pyharness.py`) po příkazech
nejvyšší úrovně: spadne-li výpis, data a funkce jsou k dispozici dál."""
from __future__ import annotations

import ast
import json
import subprocess
import sys
from pathlib import Path
from typing import Any, Callable

from oa_autograding.checks.base import CheckContext, CheckResult, register

_HARNESS = Path(__file__).with_name("_pyharness.py")


def _harness(ctx: CheckContext, req: dict[str, Any], timeout: float) -> tuple[dict[str, Any] | None, str]:
    assert ctx.file is not None
    try:
        proc = subprocess.run(
            [sys.executable, str(_HARNESS), str(ctx.file.resolve())], cwd=ctx.repo_root,
            input=json.dumps(req), capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=timeout,
        )
    except subprocess.TimeoutExpired:
        return None, f"Program neskončil do {timeout:g} s — nečeká někde na vstup nebo se nezacyklil?"
    lines = proc.stdout.strip().splitlines()
    try:
        return json.loads(lines[-1]), ""
    except (IndexError, json.JSONDecodeError):
        return None, f"Kontrolu se nepodařilo vyhodnotit.\n{proc.stderr[-2000:]}"


def _common_fail(res: dict[str, Any] | None, err: str) -> CheckResult | None:
    if res is None:
        return CheckResult(False, err.splitlines()[0], err)
    if "syntax_error" in res:
        return CheckResult(False, f"Soubor obsahuje syntaktickou chybu ({res['syntax_error']}), Python ho nespustí.")
    return None


def _crash_note(res: dict[str, Any]) -> str:
    return f" Pozor: program při spuštění spadl ({res['load_error']})." if res.get("load_error") else ""


@register("py.eval")
def py_eval(ctx: CheckContext, p: dict[str, Any]) -> CheckResult:
    if "expr" not in p or "expected" not in p:
        return CheckResult(False, "Kontrola nemá zadané `expr` a `expected` (chyba v checks.json).")
    res, err = _harness(ctx, {"op": "eval", "expr": p["expr"], "expected": p["expected"]}, float(p.get("timeout", 10)))
    if (fail := _common_fail(res, err)) is not None:
        return fail
    assert res is not None
    if res["ok"]:
        return CheckResult(True)
    exp = f"{p['expected']!r} ({type(p['expected']).__name__})"
    if "error" in res:
        return CheckResult(False, f"Výraz `{p['expr']}` nejde vyhodnotit ({res['error']}).{_crash_note(res)}")
    return CheckResult(False, f"`{p['expr']}` je {res['got']}, očekáváno {exp}.{_crash_note(res)}")


@register("py.function")
def py_function(ctx: CheckContext, p: dict[str, Any]) -> CheckResult:
    cases = p.get("cases")
    if not cases:
        return CheckResult(False, "Kontrola nemá zadané `cases` (chyba v checks.json).")
    req = {"op": "function", "cases": cases, "name": p.get("name")}
    res, err = _harness(ctx, req, float(p.get("timeout", 10)))
    if (fail := _common_fail(res, err)) is not None:
        return fail
    assert res is not None
    if res["ok"]:
        return CheckResult(True, details=f"funkce `{res['name']}`")
    if res.get("no_functions"):
        what = f"funkce `{p['name']}`" if p.get("name") else "žádná funkce (`def`)"
        return CheckResult(False, f"V souboru není {what}.{_crash_note(res)}")
    best = res["best"]
    case = cases[best["case"]]
    if "args" not in best:
        why = f"funkce `{best['name']}` {best['error']}"
    else:
        got = f"skončila chybou {best['error']}" if "error" in best else f"vrátila {best['got']}"
        exp = f"{case['expected']!r} ({type(case['expected']).__name__})"
        why = f"`{best['name']}` pro vstup {best['args']} {got}, očekáváno {exp}"
    return CheckResult(False, f"Žádná funkce nevrátila pro všechny vstupy správný výsledek. Nejblíž: {why}.{_crash_note(res)}")


def _is_const(node: ast.AST, *types: type) -> bool:
    return isinstance(node, ast.Constant) and type(node.value) in types


def _call_name(node: ast.AST) -> str | None:
    if not isinstance(node, ast.Call):
        return None
    f = node.func
    return f.id if isinstance(f, ast.Name) else f.attr if isinstance(f, ast.Attribute) else None


# Konstrukce: název → (popis pro žáka, test nad uzlem AST).
CONSTRUCTS: dict[str, tuple[str, Callable[[ast.AST], bool]]] = {
    "for": ("cyklus `for`", lambda n: isinstance(n, ast.For)),
    "while": ("cyklus `while`", lambda n: isinstance(n, ast.While)),
    "def": ("vlastní funkce `def`", lambda n: isinstance(n, ast.FunctionDef)),
    "fstring": ("f-string `f\"…{x}…\"`", lambda n: isinstance(n, ast.JoinedStr)),
    "comprehension": ("generátorová notace `[… for … in …]`",
                      lambda n: isinstance(n, (ast.ListComp, ast.SetComp, ast.DictComp, ast.GeneratorExp))),
    "dict-lookup": ("slovník jako tabulka hodnot `{\"klíč\": 3, …}`",
                    lambda n: isinstance(n, ast.Dict) and len(n.keys) >= 2
                    and all(k is not None and _is_const(k, str) for k in n.keys)
                    and all(_is_const(v, int, float) for v in n.values)),
    "in-collection": ("test `x in (…)` / `[…]` / `{…}`",
                      lambda n: isinstance(n, ast.Compare) and any(isinstance(o, (ast.In, ast.NotIn)) for o in n.ops)
                      and any(isinstance(c, (ast.List, ast.Tuple, ast.Set)) for c in n.comparators)),
    "dict-get-default": ("`slovnik.get(klic, vychozi)`",
                         lambda n: _call_name(n) == "get" and isinstance(n.func, ast.Attribute) and len(n.args) == 2),
    "default-param": ("parametr s výchozí hodnotou `def f(x=…)`",
                      lambda n: isinstance(n, ast.FunctionDef) and bool(n.args.defaults or any(n.args.kw_defaults))),
    "sort-key": ("`sorted(…, key=…)` nebo `.sort(key=…)`",
                 lambda n: _call_name(n) in ("sorted", "sort") and any(k.arg == "key" for k in n.keywords)),
}


@register("py.uses")
def py_uses(ctx: CheckContext, p: dict[str, Any]) -> CheckResult:
    names = p.get("any_of") or []
    unknown = [n for n in names if n not in CONSTRUCTS]
    if not names or unknown:
        return CheckResult(False, f"Kontrola má neplatné `any_of` {unknown or names!r} (chyba v checks.json).")
    try:
        tree = ast.parse(ctx.raw)
    except SyntaxError as e:
        return CheckResult(False, f"Soubor obsahuje syntaktickou chybu (řádek {e.lineno}: {e.msg}), Python ho nespustí.")
    found = [n for n in names if any(CONSTRUCTS[n][1](node) for node in ast.walk(tree))]
    if found:
        return CheckResult(True, details="nalezeno: " + ", ".join(found))
    return CheckResult(False, "V kódu není " + " ani ".join(CONSTRUCTS[n][0] for n in names) + ".")
