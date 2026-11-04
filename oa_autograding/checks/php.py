"""Kontroly PHP nad souborem z `file`.

- `php.page`: `expected` (volitelné), `comparison` (`"included"` | `"regex"`, výchozí
  `"included"`), `query` (slovník pro `$_GET`, výchozí `{}`), `no_warnings` (`false`),
  `timeout` (`10` s) — vykreslí stránku přes `php` (CLI) v kořeni repa, z výstupu
  odstraní HTML komentáře (v cvičeních v nich je text zadání včetně očekávaného
  výstupu) a porovná. S `no_warnings` neprojde stránka, ve které PHP ohlásí chybu,
  varování, upozornění nebo deprecated. Bez `expected` stačí, že se stránka vykreslí.
  `source_contains` (seznam textů) navíc vyžaduje, aby je kód stránky obsahoval mimo
  komentáře (bez ohledu na mezery) — stejný výstup tak nestačí, když ho nepočítá funkce.
- `php.function`: `name` (povinné), `cases` (`[{"args": [...], "expected": …, "label": …}]`),
  `typed` (`false`), `calls_itself` (`false`), `timeout` (`10` s) — načte soubor, zavolá
  funkci se `strict_types` a porovná výsledek včetně typu (int a float se smí zaměnit).
  Neprojde funkce, která něco vypisuje (výsledek má vracet). `typed` vyžaduje typ u všech
  parametrů i návratové hodnoty, `calls_itself` rekurzi. `label` nahradí ve zprávě
  dlouhé argumenty popisem."""
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
    if p.get("source_contains"):
        # `php -w` zahodí PHP komentáře, HTML komentáře odstraníme sami; mezery se neporovnávají.
        src = subprocess.run(["php", "-w", ctx.file.name], cwd=ctx.file.parent, capture_output=True, text=True,
                             encoding="utf-8", errors="replace", timeout=timeout).stdout
        code = re.sub(r"\s+", "", strip_html_comments(src))
        missing = [t for t in p["source_contains"] if re.sub(r"\s+", "", t) not in code]
        if missing:
            return CheckResult(
                False, f"Stránka ukazuje správný výsledek, ale v jejím kódu chybí `{missing[0]}` (komentáře se nepočítají).", details,
            )
    return CheckResult(True, details=details)


# `php.function`: harness načte soubor žáka (výstup zahodí), funkci zavolá ze souboru se
# strict_types (špatný typ argumentu = TypeError jako u žáka) a vrátí JSON na poslední řádek.
_FN_HARNESS = r'''declare(strict_types=1);
$req = json_decode((string) stream_get_contents(STDIN), true);
$res = [];
ob_start();
try { require $argv[1]; } catch (Throwable $e) { $res["load_error"] = get_class($e) . ": " . $e->getMessage() . " (řádek " . $e->getLine() . ")"; }
ob_end_clean();
$name = $req["name"];
if (!function_exists($name)) { $res["missing"] = true; echo "\n", json_encode($res, JSON_UNESCAPED_UNICODE), "\n"; exit; }
$rf = new ReflectionFunction($name);
$res["name"] = $rf->getName();
$res["untyped"] = [];
foreach ($rf->getParameters() as $p) { if (!$p->hasType()) { $res["untyped"][] = "$" . $p->getName(); } }
$res["return_type"] = $rf->hasReturnType() ? (string) $rf->getReturnType() : null;
$lines = file($rf->getFileName());
$body = implode("", array_slice($lines, $rf->getStartLine() - 1, $rf->getEndLine() - $rf->getStartLine() + 1));
$res["self_calls"] = preg_match_all("/\b" . preg_quote($name, "/") . "\s*\(/i", $body) - 1;
$res["cases"] = [];
foreach ($req["cases"] as $args) {
    ob_start();
    try { $r = ["got" => $name(...$args)]; } catch (Throwable $e) { $r = ["error" => get_class($e) . ": " . $e->getMessage()]; }
    $r["output"] = ob_get_clean();
    $res["cases"][] = $r;
}
echo "\n", json_encode($res, JSON_UNESCAPED_UNICODE | JSON_PRESERVE_ZERO_FRACTION | JSON_PARTIAL_OUTPUT_ON_ERROR), "\n";
'''


def _show(value: Any, limit: int = 60) -> str:
    text = json.dumps(value, ensure_ascii=False)
    return text if len(text) <= limit else text[: limit - 1] + "…"


def _same(got: Any, expected: Any) -> bool:
    num = (int, float)
    if type(got) in num and type(expected) in num:
        return abs(got - expected) < 1e-9
    return type(got) is type(expected) and got == expected


@register("php.function")
def php_function(ctx: CheckContext, p: dict[str, Any]) -> CheckResult:
    assert ctx.file is not None
    name = p.get("name")
    cases = p.get("cases") or []
    if not name:
        return CheckResult(False, "Kontrola nemá zadané `name` (chyba v checks.json).")
    timeout = float(p.get("timeout", 10))
    cmd = ["php", "-d", "display_errors=stderr", "-d", "log_errors=0", "-d", "html_errors=0",
           "-d", "xdebug.mode=off", "-r", _FN_HARNESS, "--", ctx.file.name]
    req = {"name": name, "cases": [c.get("args", []) for c in cases]}
    try:
        proc = subprocess.run(cmd, cwd=ctx.file.parent, input=json.dumps(req), capture_output=True, text=True,
                              encoding="utf-8", errors="replace", timeout=timeout)
    except FileNotFoundError:
        return CheckResult(False, "Na stroji s kontrolou chybí PHP — chyba prostředí, ne vaše; dejte vědět učiteli.")
    except subprocess.TimeoutExpired:
        return CheckResult(False, f"Funkce `{name}` neskončila do {timeout:g} s — nezacyklila se?")
    stderr = proc.stderr.replace(str(ctx.file.parent) + os.sep, "")
    details = f"$ php {ctx.file.name} → {name}()\nexit {proc.returncode}\n--- stdout ---\n{proc.stdout[-_CLIP:]}\n--- stderr ---\n{stderr[:_CLIP]}"
    try:
        res = json.loads(proc.stdout.strip().splitlines()[-1])
    except (IndexError, json.JSONDecodeError):
        errors = _ERROR.findall(stderr)
        first = f"{errors[0][0]}: {errors[0][1]}" if errors else (stderr.strip().splitlines() or [f"návratový kód {proc.returncode}"])[0]
        return CheckResult(False, f"Soubor `{ctx.file.name}` nejde načíst, PHP skončilo chybou: `{first}`.", details)

    crash = f" Pozor: načtení souboru skončilo chybou `{res['load_error']}`." if res.get("load_error") else ""
    if res.get("missing"):
        return CheckResult(False, f"V souboru `{ctx.file.name}` není funkce `{name}`.{crash}", details)
    fn = res["name"]
    for case, got in zip(cases, res["cases"]):
        call = f"`{fn}({case['label'] if 'label' in case else ', '.join(_show(a) for a in case.get('args', []))})`"
        if "error" in got:
            return CheckResult(False, f"{call} skončila chybou `{got['error']}`.", details)
        if got["output"].strip():
            return CheckResult(False, f"{call} vypisuje text ({_show(got['output'].strip())}) — výsledek má funkce vracet přes `return`, ne vypisovat.", details)
        if "expected" in case and not _same(got.get("got"), case["expected"]):
            return CheckResult(False, f"{call} vrátila {_show(got.get('got'))}, očekáváno {_show(case['expected'])}.", details)
    if p.get("typed"):
        if res["untyped"]:
            return CheckResult(False, f"Parametr {', '.join(res['untyped'])} funkce `{fn}` nemá datový typ.", details)
        if not res["return_type"]:
            return CheckResult(False, f"Funkce `{fn}` nemá datový typ návratové hodnoty (`): typ` za závorkou parametrů).", details)
    if p.get("calls_itself") and res["self_calls"] < 1:
        return CheckResult(False, f"Funkce `{fn}` nevolá sama sebe — úloha chce řešení rekurzí.", details)
    return CheckResult(True, details=details)
