"""Kontrola `run`: spustí příkaz v kořeni repa a porovná výstup nebo návratový kód."""
from __future__ import annotations

import re
import subprocess
from typing import Any

from oa_autograding.checks.base import CheckContext, CheckResult, register

_CLIP = 4000


def _compare(stdout: str, expected: str, comparison: str) -> bool:
    if comparison == "included":
        return expected in stdout
    if comparison == "exact":
        return stdout.strip() == expected.strip()
    if comparison == "regex":
        return re.search(expected, stdout, re.M) is not None
    raise ValueError(f"neznámé comparison {comparison!r} (included|exact|regex)")


@register("run", needs_file=False)
def run_cmd(ctx: CheckContext, p: dict[str, Any]) -> CheckResult:
    cmd = p.get("cmd")
    if not cmd:
        return CheckResult(False, "Kontrola nemá zadaný příkaz `cmd` (chyba v checks.json).")
    timeout = float(p.get("timeout", 10))
    try:
        proc = subprocess.run(
            cmd, shell=True, cwd=ctx.repo_root, input=p.get("stdin"),
            capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=timeout,
        )
    except subprocess.TimeoutExpired:
        return CheckResult(False, f"Program neskončil do {timeout:g} s — nečeká někde na vstup nebo se nezacyklil?", f"$ {cmd}\n(timeout {timeout:g} s)")
    details = (
        f"$ {cmd}\nexit {proc.returncode}\n--- stdout ---\n{proc.stdout[:_CLIP]}\n--- stderr ---\n{proc.stderr[:_CLIP]}"
    )
    exit_code = p.get("exit_code")
    if exit_code is not None and proc.returncode != int(exit_code):
        return CheckResult(False, f"Program skončil s návratovým kódem {proc.returncode}, očekáván {exit_code}.", details)
    if "expected" in p:
        if not _compare(proc.stdout, str(p["expected"]), str(p.get("comparison", "included"))):
            return CheckResult(False, "Výstup programu neodpovídá očekávanému.", details)
    elif exit_code is None and proc.returncode != 0:
        return CheckResult(False, f"Program skončil s chybou (návratový kód {proc.returncode}).", details)
    return CheckResult(True, details=details)
