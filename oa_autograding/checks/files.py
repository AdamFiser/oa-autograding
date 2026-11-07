"""Kontroly nad soubory: existence, nepřítomnost značek (TODO), otisk obsahu a zakázané soubory."""
from __future__ import annotations

import hashlib
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


@register("file.sha256")
def file_sha256(ctx: CheckContext, params: dict[str, Any]) -> CheckResult:
    """Soubor je bajtově shodný s originálem (SHA-256 v `sha256`)."""
    expected = str(params.get("sha256", "")).strip().lower()
    if not expected:
        return CheckResult(False, "Kontrola nemá zadaný `sha256` (chyba v checks.json).")
    assert ctx.file is not None
    actual = hashlib.sha256(ctx.file.read_bytes()).hexdigest()
    if actual == expected:
        return CheckResult(True)
    return CheckResult(
        False,
        f"Soubor `{_rel(ctx)}` se liší od zadání. Vraťte jeho původní obsah ze šablony.",
        f"sha256 {actual}, očekáváno {expected}",
    )


@register("file.absent", needs_file=False)
def file_absent(ctx: CheckContext, params: dict[str, Any]) -> CheckResult:
    """Žádná z cest v `paths` (soubor ani adresář) v repozitáři není."""
    paths = params.get("paths")
    if not isinstance(paths, list) or not paths or not all(isinstance(p, str) and p for p in paths):
        return CheckResult(False, "Kontrola nemá zadaný seznam `paths` (chyba v checks.json).")
    found = [p for p in paths if (ctx.repo_root / p).exists() or (ctx.repo_root / p).is_symlink()]
    if not found:
        return CheckResult(True)
    return CheckResult(False, "V repozitáři nesmí být: " + ", ".join(f"`{p}`" for p in found) + ". Odstraňte je.")
