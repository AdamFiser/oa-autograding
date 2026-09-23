"""Samostatný skript pro kontroly `py.eval` a `py.function`: spouští se v podprocesu
(`python _pyharness.py <soubor žáka>`), požadavek čte jako JSON ze stdin a výsledek
vypíše jako JSON na poslední řádek stdout. Neimportuje nic z oa_autograding.

Program žáka se vykoná po příkazech nejvyšší úrovně: když jeden spadne (např. výpis
nad ještě neopravenými daty), ostatní — data, definice funkcí — se vykonají dál.
Výstup programu i funkcí se zahazuje, `input()` dostane prázdný vstup."""
from __future__ import annotations

import ast
import builtins
import contextlib
import copy
import inspect
import io
import json
import os
import sys
from typing import Any

_REPR = 200


def same(got: Any, exp: Any) -> bool:
    """Porovnání s typem: "5" ≠ 5, True ≠ 1; int a float se smí zaměnit (5.0 == 5)."""
    if isinstance(exp, bool) or isinstance(got, bool):
        return type(got) is type(exp) and got == exp
    if isinstance(exp, (int, float)):
        return isinstance(got, (int, float)) and abs(got - exp) <= 1e-9
    if isinstance(exp, list):
        return isinstance(got, (list, tuple)) and len(got) == len(exp) and all(map(same, got, exp))
    if isinstance(exp, dict):
        return isinstance(got, dict) and got.keys() == exp.keys() and all(same(got[k], exp[k]) for k in exp)
    return type(got) is type(exp) and got == exp


def show(value: Any) -> str:
    text = repr(value)
    text = text if len(text) <= _REPR else text[:_REPR] + "…"
    return f"{text} ({type(value).__name__})"


def load(path: str) -> tuple[dict[str, Any], str | None]:
    with open(path, encoding="utf-8-sig") as f:
        tree = ast.parse(f.read(), path)
    ns: dict[str, Any] = {"__name__": "__main__", "__file__": path, "__builtins__": builtins}
    first_error = None
    for stmt in tree.body:
        try:
            exec(compile(ast.Module([stmt], []), path, "exec"), ns)
        except BaseException as e:  # noqa: BLE001 — i SystemExit/KeyboardInterrupt z programu žáka
            if first_error is None:
                first_error = f"řádek {stmt.lineno}: {type(e).__name__}: {e}"
    return ns, first_error


def op_eval(ns: dict[str, Any], req: dict[str, Any]) -> dict[str, Any]:
    try:
        # Výraz píše učitel do checks.json; kód žáka tu běží tak jako tak (izolace = podproces).
        got = eval(req["expr"], ns)
    except Exception as e:  # noqa: BLE001
        return {"ok": False, "error": f"{type(e).__name__}: {e}"}
    return {"ok": same(got, req["expected"]), "got": show(got)}


def _call_forms(fn: Any, args: list[Any]) -> list[tuple[tuple, dict]]:
    """Jak funkci zavolat: f(*args), a je-li jediný argument slovník, i f(**slovník)
    omezený na parametry funkce (žák mohl napsat f(odvetvi, obrat, …, konference=False))."""
    sig = inspect.signature(fn)
    forms: list[tuple[tuple, dict]] = []
    try:
        sig.bind(*args)
        forms.append((tuple(args), {}))
    except TypeError:
        pass
    if len(args) == 1 and isinstance(args[0], dict):
        params = sig.parameters
        takes_all = any(p.kind is p.VAR_KEYWORD for p in params.values())
        kw = {k: v for k, v in args[0].items() if takes_all or k in params}
        try:
            sig.bind(**kw)
            forms.append(((), kw))
        except TypeError:
            pass
    return forms


def _try_function(name: str, fn: Any, cases: list[dict[str, Any]]) -> dict[str, Any]:
    passed = 0
    for i, case in enumerate(cases):
        args = case.get("args", [])
        forms = _call_forms(fn, args)
        if not forms:
            return {"name": name, "passed": passed, "case": i, "error": "nejde zavolat s tímto počtem argumentů"}
        got: Any = None
        for form_args, form_kw in forms:
            try:
                with contextlib.redirect_stdout(io.StringIO()):
                    got = fn(*copy.deepcopy(form_args), **copy.deepcopy(form_kw))
            except Exception as e:  # noqa: BLE001
                got = e
                continue
            if same(got, case["expected"]):
                break
        else:
            res = {"name": name, "passed": passed, "case": i, "args": show(args)[:_REPR]}
            if isinstance(got, Exception):
                res["error"] = f"{type(got).__name__}: {got}"
            else:
                res["got"] = show(got)
            return res
        passed += 1
    return {"name": name, "passed": passed, "ok": True}


def op_function(ns: dict[str, Any], req: dict[str, Any], path: str) -> dict[str, Any]:
    want = req.get("name")
    funcs = {
        k: v for k, v in ns.items()
        if inspect.isfunction(v) and v.__code__.co_filename == path and (want is None or k == want)
    }
    if not funcs:
        return {"ok": False, "no_functions": True}
    tries = [_try_function(k, v, req["cases"]) for k, v in funcs.items()]
    for t in tries:
        if t.get("ok"):
            return {"ok": True, "name": t["name"]}
    return {"ok": False, "best": max(tries, key=lambda t: t["passed"])}


def main() -> None:
    path = sys.argv[1]
    req = json.load(sys.stdin)
    sys.stdin = io.StringIO("")
    sys.path.insert(0, os.path.dirname(path))
    sys.stdout.reconfigure(encoding="utf-8")  # rodič čte UTF-8, Windows by psal cp1250
    real_stdout = sys.stdout
    try:
        with contextlib.redirect_stdout(io.StringIO()):
            ns, load_error = load(path)
    except SyntaxError as e:
        res: dict[str, Any] = {"ok": False, "syntax_error": f"řádek {e.lineno}: {e.msg}"}
    else:
        res = op_eval(ns, req) if req["op"] == "eval" else op_function(ns, req, path)
        res["load_error"] = load_error
    # ponytail: žák by mohl vypsat podvržený JSON přes sys.__stdout__; u cvičení bez známky to neřešíme
    real_stdout.write("\n" + json.dumps(res, ensure_ascii=False) + "\n")


if __name__ == "__main__":
    main()
