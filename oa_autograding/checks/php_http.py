"""`php.http`: projde stránky žáka jako prohlížeč přes vestavěný server PHP (`php -S`).

Parametry kontroly: `steps` (povinné), `files` (seznam `{"glob", "min"|"max"}` nad kopií repa
po posledním kroku), `timeout` (celkový limit, výchozí `20` s).

Krok: `method` (`GET` | `POST`, výchozí `GET`), `path` (cesta k souboru, smí obsahovat `?…`),
`query` (slovník přidaný do adresy; seznam = opakovaný klíč, pole PHP pište jako `"znamka[]"`),
`form` (pole odesílaného formuláře, seznam = opakovaný klíč), `files` (`{pole: {"fixture",
"filename", "content_type"}}` — formulář se pak pošle jako `multipart/form-data`), `csrf` (název
skrytého pole: jeho hodnota se převezme z předchozí odpovědi; když tam pole není, nepošle se),
`label` (popis kroku pro žáka) a `expect` (`status`, `location` — část hlavičky `Location`,
`contains`, `not_contains`, `regex` — vzor nebo seznam vzorů, `no_warnings`).

Server běží nad kopií repa (nahrané soubory žákovi nezůstanou), cookies (session) se mezi kroky
drží, přesměrování se nenásleduje. Z odpovědi se před porovnáním odstraní HTML komentáře
(v cvičeních je v nich text zadání). Chyba PHP (`Fatal error`, nezachycená výjimka) shodí krok
vždy, varování jen s `no_warnings`."""
from __future__ import annotations

import base64
import html
import http.client
import os
import re
import shutil
import socket
import subprocess
import tempfile
import time
import uuid
from http.cookies import SimpleCookie
from pathlib import Path
from typing import Any
from urllib.parse import quote, urlencode

from oa_autograding.checks.base import CheckContext, CheckResult, register, strip_html_comments

_CLIP = 2000
_ERROR = re.compile(r"^(?:PHP )?(Fatal error|Parse error|Warning|Notice|Deprecated):\s*(.*)$", re.M)
_FATAL = ("Fatal error", "Parse error")
_PNG = base64.b64decode(
    "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNkYPhfDwAChwGA60e6kgAAAABJRU5ErkJggg=="
)
# fixture → (obsah, výchozí název, výchozí Content-Type)
_FIXTURES: dict[str, tuple[bytes, str, str]] = {
    "png": (_PNG, "foto.png", "image/png"),
    "png-3mb": (_PNG + b"\0" * 3_000_000, "velka.png", "image/png"),
    "php": (b"<?php echo 'hacked';\n", "virus.php", "application/x-php"),
    "text": (b"Ahoj\n", "poznamka.txt", "text/plain"),
}


class _StepFailed(Exception):
    pass


def _free_port() -> int:
    with socket.socket() as s:
        s.bind(("127.0.0.1", 0))
        return int(s.getsockname()[1])


def _pairs(data: dict[str, Any]) -> list[tuple[str, str]]:
    out: list[tuple[str, str]] = []
    for key, value in data.items():
        for v in value if isinstance(value, list) else [value]:
            out.append((key, str(v)))
    return out


def _multipart(fields: list[tuple[str, str]], files: dict[str, Any]) -> tuple[bytes, str]:
    boundary = "oa-" + uuid.uuid4().hex
    parts: list[bytes] = []
    for key, value in fields:
        parts.append(f'--{boundary}\r\nContent-Disposition: form-data; name="{key}"\r\n\r\n'.encode() + value.encode() + b"\r\n")
    for key, spec in files.items():
        if spec.get("fixture") not in _FIXTURES:
            raise ValueError(f"neznámá fixture {spec.get('fixture')!r}, povoleno {', '.join(_FIXTURES)}")
        content, name, ctype = _FIXTURES[spec["fixture"]]
        name, ctype = spec.get("filename", name), spec.get("content_type", ctype)
        head = f'--{boundary}\r\nContent-Disposition: form-data; name="{key}"; filename="{name}"\r\nContent-Type: {ctype}\r\n\r\n'
        parts.append(head.encode() + content + b"\r\n")
    return b"".join(parts) + f"--{boundary}--\r\n".encode(), f"multipart/form-data; boundary={boundary}"


def _hidden_value(page: str, field: str) -> str | None:
    for tag in re.findall(r"<input\b[^>]*>", page, re.I):
        attrs = {k.lower(): html.unescape(v1 or v2) for k, v1, v2 in re.findall(r"([\w-]+)\s*=\s*(?:\"([^\"]*)\"|'([^']*)')", tag)}
        if attrs.get("name") == field:
            return attrs.get("value", "")
    return None


def _check_step(where: str, status: int, location: str, body: str, expect: dict[str, Any]) -> None:
    errors = _ERROR.findall(body)
    fatal = next((f"{kind}: {msg}" for kind, msg in errors if kind in _FATAL), None)
    if fatal:
        raise _StepFailed(f"{where}: PHP skončilo chybou `{fatal}`.")
    if "status" in expect and status != int(expect["status"]):
        moved = f" (přesměrování na `{location}`)" if location else ""
        raise _StepFailed(f"{where}: stránka odpověděla kódem {status}{moved}, očekáváno {expect['status']}.")
    if "location" in expect and str(expect["location"]) not in location:
        target = f"míří na `{location}`" if location else "chybí (stránka nepřesměrovala)"
        raise _StepFailed(f"{where}: přesměrování {target}, očekáváno `{expect['location']}`.")
    for text in expect.get("contains", []):
        if text not in body:
            raise _StepFailed(f"{where}: v odpovědi chybí `{text}` (HTML komentáře se nepočítají).")
    for text in expect.get("not_contains", []):
        if text in body:
            raise _StepFailed(f"{where}: odpověď obsahuje `{text}`, ale neměla by.")
    patterns = expect.get("regex", [])
    for pattern in [patterns] if isinstance(patterns, str) else patterns:
        if re.search(str(pattern), body, re.M) is None:
            raise _StepFailed(f"{where}: odpověď neodpovídá očekávanému tvaru (`{pattern}`).")
    if expect.get("no_warnings") and errors:
        kind, msg = errors[0]
        raise _StepFailed(f"{where}: PHP hlásí {len(errors)}× chybu nebo varování, první: `{kind}: {msg}`.")


@register("php.http", needs_file=False)
def php_http(ctx: CheckContext, p: dict[str, Any]) -> CheckResult:
    steps = p.get("steps") or []
    if not steps:
        return CheckResult(False, "Kontrola nemá žádné `steps` (chyba v checks.json).")
    php = shutil.which("php")
    if php is None:
        return CheckResult(False, "Na stroji s kontrolou chybí PHP — chyba prostředí, ne vaše; dejte vědět učiteli.")
    deadline = time.monotonic() + float(p.get("timeout", 20))
    log: list[str] = []

    with tempfile.TemporaryDirectory(prefix="oa-http-") as tmp:
        tmp = str(Path(tmp).resolve())  # Windows: krátká cesta s `~` by rozbila hodnotu `-d` v PHP
        root = Path(tmp) / "repo"
        shutil.copytree(ctx.repo_root, root, ignore=shutil.ignore_patterns(".git"))
        (Path(tmp) / "sess").mkdir()
        port = _free_port()
        server_log = open(Path(tmp) / "server.log", "w+b")
        flags = {
            "display_errors": "1", "html_errors": "0", "error_reporting": "-1", "log_errors": "0",
            "xdebug.mode": "off", "output_buffering": "4096", "session.save_path": str(Path(tmp) / "sess"),
            "upload_max_filesize": "8M", "post_max_size": "16M",
        }
        cmd = [php, "-S", f"127.0.0.1:{port}", "-t", str(root)] + [a for k, v in flags.items() for a in ("-d", f"{k}={v}")]
        server = subprocess.Popen(cmd, cwd=root, stdout=server_log, stderr=subprocess.STDOUT)
        try:
            while True:
                try:
                    socket.create_connection(("127.0.0.1", port), timeout=0.2).close()
                    break
                except OSError:
                    if time.monotonic() > deadline or server.poll() is not None:
                        return CheckResult(False, "Vestavěný server PHP se nespustil — chyba prostředí, dejte vědět učiteli.")
                    time.sleep(0.05)
            result = _run_steps(steps, port, deadline, log, root)
            if result is None:
                result = _check_files(p.get("files") or [], root)
        except _StepFailed as e:
            result = CheckResult(False, str(e))
        except ValueError as e:
            result = CheckResult(False, f"Neplatný krok kontroly: {e} (chyba v checks.json).")
        except (OSError, http.client.HTTPException) as e:
            result = CheckResult(False, f"Stránka neodpověděla včas nebo spojení spadlo ({type(e).__name__}) — nezacyklil se kód?")
        finally:
            server.terminate()
            try:
                server.wait(timeout=5)
            except subprocess.TimeoutExpired:
                server.kill()
            server_log.seek(0)
            log.append("--- server ---\n" + server_log.read().decode("utf-8", "replace")[-_CLIP:])
            server_log.close()

    details = "\n".join(log).replace(str(root) + os.sep, "").replace(str(root), "")
    return CheckResult(result.passed, result.reason, details)


def _run_steps(steps: list[dict[str, Any]], port: int, deadline: float, log: list[str], root: Path) -> CheckResult | None:
    cookies: dict[str, str] = {}
    previous = ""
    for step in steps:
        method = str(step.get("method", "GET")).upper()
        path = str(step.get("path", "index.php"))
        url = "/" + quote(path.lstrip("/"), safe="/?&=[]%+")
        if step.get("query"):
            url += ("&" if "?" in url else "?") + urlencode(_pairs(step["query"]))
        shown = path + (("&" if "?" in path else "?") + "&".join(f"{k}={v}" for k, v in _pairs(step["query"])) if step.get("query") else "")
        where = step.get("label") or f"`{method} {shown}`"
        headers = {"Cookie": "; ".join(f"{k}={v}" for k, v in cookies.items())} if cookies else {}
        body: bytes | None = None
        if method == "POST":
            fields = _pairs(step.get("form") or {})
            if step.get("csrf"):
                token = _hidden_value(previous, str(step["csrf"]))
                if token is not None:
                    fields.append((str(step["csrf"]), token))
            if step.get("files"):
                body, headers["Content-Type"] = _multipart(fields, step["files"])
            else:
                body, headers["Content-Type"] = urlencode(fields).encode(), "application/x-www-form-urlencoded"
        conn = http.client.HTTPConnection("127.0.0.1", port, timeout=max(0.5, deadline - time.monotonic()))
        try:
            conn.request(method, url, body=body, headers=headers)
            resp = conn.getresponse()
            raw = resp.read().decode("utf-8", "replace")
            for header in resp.headers.get_all("Set-Cookie") or []:
                for name, morsel in SimpleCookie(header).items():
                    cookies[name] = morsel.value
            status, location = resp.status, resp.headers.get("Location", "")
        finally:
            conn.close()
        page = strip_html_comments(raw)
        clean = page.replace(str(root) + os.sep, "").replace(str(root), "")
        log.append(f"$ {method} {url} → {status}" + (f" Location: {location}" if location else "") + f"\n{clean[:_CLIP]}")
        _check_step(where, status, location, clean, step.get("expect") or {})
        previous = page
    return None


def _check_files(rules: list[dict[str, Any]], root: Path) -> CheckResult:
    for rule in rules:
        pattern = str(rule["glob"])
        found = len(list(root.glob(pattern)))
        if "min" in rule and found < int(rule["min"]):
            return CheckResult(False, f"Ve `{pattern}` je {found} souborů, očekáváno aspoň {rule['min']} — uložil se soubor?")
        if "max" in rule and found > int(rule["max"]):
            return CheckResult(False, f"Ve `{pattern}` je {found} souborů, smí jich být nejvýš {rule['max']}.")
    return CheckResult(True)
