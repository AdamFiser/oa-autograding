"""Kontroly nad soubory: existence a nepřítomnost značek (TODO)."""
from __future__ import annotations

from typing import Any

from oa_autograding.checks.base import CheckContext, CheckResult, register


def _rel(ctx: CheckContext) -> str:
    assert ctx.file is not None
    try:
        return ctx.file.relative_to(ctx.repo_root).as_posix()
    except ValueError:
        return ctx.file.name


@register("file.exists", needs_file=False)
def file_exists(ctx: CheckContext, params: dict[str, Any]) -> CheckResult:
    if ctx.file is None:
        return CheckResult(False, "Kontrola nemá zadaný soubor (chyba v checks.json).")
    if ctx.file.is_file():
        return CheckResult(True)
    return CheckResult(False, f"Soubor `{_rel(ctx)}` v repozitáři není.")


@register("file.no-marker")
def file_no_marker(ctx: CheckContext, params: dict[str, Any]) -> CheckResult:
    marker = str(params.get("marker", "<!-- TODO"))
    needle = marker.replace(" ", "")
    lines = [i for i, line in enumerate(ctx.raw.splitlines(), 1) if needle in line.replace(" ", "")]
    if not lines:
        return CheckResult(True)
    kde = ", ".join(str(n) for n in lines[:10]) + (" …" if len(lines) > 10 else "")
    return CheckResult(
        False,
        f"V souboru zůstává {len(lines)}× značka `{marker}` (řádky {kde}). Každou nahraďte obsahem podle jejího textu.",
    )
