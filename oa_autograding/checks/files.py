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


@register("file.contains")
def file_contains(ctx: CheckContext, params: dict[str, Any]) -> CheckResult:
    """Alespoň `min_count` (1) řádků obsahuje `text`; bez ohledu na mezery a velikost písmen."""
    text = str(params.get("text", ""))
    if not text:
        return CheckResult(False, "Kontrola nemá zadaný `text` (chyba v checks.json).")
    need = int(params.get("min_count", 1))
    needle = text.replace(" ", "").casefold()
    count = sum(needle in line.replace(" ", "").casefold() for line in ctx.raw.splitlines())
    if count >= need:
        return CheckResult(True)
    return CheckResult(False, f"`{text}` je v souboru na {count} řádcích, požadováno alespoň {need}.")
