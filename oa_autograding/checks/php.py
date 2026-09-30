"""Kontrola vykreslené PHP stránky nad souborem z `file`.

- `php.page`: `expected` (volitelné), `comparison` (`"included"` | `"regex"`, výchozí
  `"included"`), `query` (slovník pro `$_GET`, výchozí `{}`), `no_warnings` (`false`),
  `timeout` (`10` s) — vykreslí stránku přes `php` (CLI) v kořeni repa, z výstupu
  odstraní HTML komentáře (v cvičeních v nich je text zadání včetně očekávaného
  výstupu) a porovná. S `no_warnings` neprojde stránka, ve které PHP ohlásí chybu,
  varování, upozornění nebo deprecated. Bez `expected` stačí, že se stránka vykreslí."""
from __future__ import annotations

import json
import os
import re
import subprocess
from typing import Any

from oa_autograding.checks.base import CheckContext, CheckResult, register, strip_html_comments

_CLIP = 4000
# `$_GET` z proměnné prostředí, pak stránka žáka; chyby PHP jdou na stderr, stdout je čistá stránka.
_BOOTSTRAP = '$_GET = json_decode((string) getenv("OA_QUERY"), true) ?: []; $_REQUEST = $_GET; include $argv[1];'
_ERROR = re.compile(r"^(?:PHP )?(Fatal error|Parse error|Warning|Notice|Deprecated):\s*(.*)$", re.M)
_FATAL = ("Fatal error", "Parse error")


def _query_note(query: dict[str, Any]) -> str:
    if not query:
        return ""
    return " (stránka otevřená s `?" + "&".join(f"{k}={v}" for k, v in query.items()) + "`)"


@register("php.page")
def php_page(ctx: CheckContext, p: dict[str, Any]) -> CheckResult:
    assert ctx.file is not None
    query = p.get("query") or {}
    timeout = float(p.get("timeout", 10))
    cmd = [
        "php", "-d", "display_errors=stderr", "-d", "log_errors=0", "-d", "html_errors=0",
        "-d", "error_reporting=-1", "-d", "xdebug.mode=off", "-r", _BOOTSTRAP, "--", ctx.file.name,
    ]
    try:
        proc = subprocess.run(
            cmd, cwd=ctx.file.parent, capture_output=True, text=True, encoding="utf-8", errors="replace",
            timeout=timeout, env={**os.environ, "OA_QUERY": json.dumps(query)},
        )
    except FileNotFoundError:
        return CheckResult(False, "Na stroji s kontrolou chybí PHP — chyba prostředí, ne vaše; dejte vědět učiteli.")
    except subprocess.TimeoutExpired:
        return CheckResult(False, f"Stránka se nevykreslila do {timeout:g} s — nezacyklil se někde kód?")

    stderr = proc.stderr.replace(str(ctx.file.parent) + os.sep, "")
    details = f"$ php {ctx.file.name}{_query_note(query)}\nexit {proc.returncode}\n--- stdout ---\n{proc.stdout[:_CLIP]}\n--- stderr ---\n{stderr[:_CLIP]}"
    errors = _ERROR.findall(stderr)
    fatal = next((f"{kind}: {msg}" for kind, msg in errors if kind in _FATAL), None)
    if fatal or proc.returncode != 0:
        first = fatal or (stderr.strip().splitlines() or [f"návratový kód {proc.returncode}"])[0]
        return CheckResult(False, f"Stránka se nevykreslila, PHP skončilo chybou: `{first}`.", details)
    if p.get("no_warnings") and errors:
        kind, msg = errors[0]
        return CheckResult(
            False,
            f"PHP při vykreslení stránky hlásí {len(errors)}× chybu nebo varování, první: `{kind}: {msg}`.",
            details,
        )
    if "expected" in p:
        page = strip_html_comments(proc.stdout)
        expected = str(p["expected"])
        comparison = str(p.get("comparison", "included"))
        if comparison == "included":
            ok = expected in page
        elif comparison == "regex":
            ok = re.search(expected, page, re.M) is not None
        else:
            return CheckResult(False, f"Neznámé `comparison` {comparison!r}, povoleno included|regex (chyba v checks.json).")
        if not ok:
            return CheckResult(
                False, f"Ve vykreslené stránce{_query_note(query)} chybí očekávaný výstup (HTML komentáře se nepočítají).", details,
            )
    return CheckResult(True, details=details)
