"""Kontroly GitHub Markdownu. Pracují nad textem bez fenced bloků kódu (ctx.no_code),
pokud kontrola nepotřebuje bloky samotné (md.code)."""
from __future__ import annotations

import re
from typing import Any

from oa_autograding.checks.base import CheckContext, CheckResult, register

UL = r"^[-*+]\s+\S"
OL = r"^\d+\.\s+\S"
NESTED_UL = r"^[ \t]{2,}[-*+]\s+\S"
NESTED_OL = r"^[ \t]{2,}\d+\.\s+\S"


def find_headings(text: str) -> list[tuple[int, str]]:
    return [(len(m.group(1)), m.group(2).strip()) for m in re.finditer(r"^(#{1,6})\s+(.+)$", text, re.M)]


def _levels(levels: list[int]) -> str:
    return ", ".join(f"H{l}" for l in levels)


@register("md.headings")
def headings(ctx: CheckContext, p: dict[str, Any]) -> CheckResult:
    present = {lvl for lvl, _ in find_headings(ctx.no_code)}
    required = sorted(set(p.get("levels_required", [1])))
    any_of = sorted(set(p.get("levels_any_of", [])))
    missing = [l for l in required if l not in present]
    if missing:
        return CheckResult(False, f"Chybí nadpis úrovně {_levels(missing)} (`{'#' * missing[0]} Text`).")
    if any_of and not any(l in present for l in any_of):
        return CheckResult(False, "Chybí alespoň jeden nadpis úrovně " + " nebo ".join(f"H{l}" for l in any_of) + ".")
    return CheckResult(True)


_BOLD = r"\*\*[^\n*]+\*\*|__[^\n_]+__"
_ITALIC = r"(?<!\*)\*(?!\*)[^\n*]+(?<!\*)\*(?!\*)|(?<!_)_(?!_)[^\n_]+(?<!_)_(?!_)"
_STRIKE = r"~~[^\n~]+~~"


@register("md.formatting")
def formatting(ctx: CheckContext, p: dict[str, Any]) -> CheckResult:
    t = re.sub(r"`[^`\n]+`", "", ctx.no_code)
    missing: list[str] = []
    if p.get("bold", True) and not re.search(_BOLD, t):
        missing.append("tučný text (`**text**`)")
    if p.get("italic", True) and not re.search(_ITALIC, t):
        missing.append("kurzíva (`*text*`)")
    if p.get("strikethrough", True) and not re.search(_STRIKE, t):
        missing.append("přeškrtnutý text (`~~text~~`)")
    if missing:
        return CheckResult(False, "Chybí: " + ", ".join(missing) + ".")
    return CheckResult(True)


@register("md.anchor-link")
def anchor_link(ctx: CheckContext, p: dict[str, Any]) -> CheckResult:
    if re.search(r"\[[^\]]+\]\(#[^)]+\)", ctx.no_code):
        return CheckResult(True)
    return CheckResult(False, "Nenašel se odkaz na sekci ve tvaru `[Text](#kotva)`; kotva je název nadpisu malými písmeny s pomlčkami.")


def _ordered_inside_unordered(lines: list[str]) -> bool:
    for idx, line in enumerate(lines):
        if not re.match(UL, line):
            continue
        for nxt in lines[idx + 1:]:
            if re.match(NESTED_OL, nxt):
                return True
            if re.match(UL, nxt) or re.match(OL, nxt):
                break
            if nxt.strip() == "":
                continue
            if not nxt.startswith((" ", "\t")):
                break
    return False


@register("md.list")
def md_list(ctx: CheckContext, p: dict[str, Any]) -> CheckResult:
    kind = p.get("kind", "unordered")
    min_items = int(p.get("min_items", 1))
    nested = p.get("nested", "none")
    lines = ctx.no_code.splitlines()
    pattern, name, priklad = (UL, "nečíslovaného", "- položka") if kind == "unordered" else (OL, "číslovaného", "1. položka")
    items = [l for l in lines if re.match(pattern, l)]
    if len(items) < min_items:
        return CheckResult(False, f"Nalezeno {len(items)} položek {name} seznamu (`{priklad}`), požadováno alespoň {min_items}.")
    if nested == "any" and not any(re.match(NESTED_UL, l) or re.match(NESTED_OL, l) for l in lines):
        return CheckResult(False, "Chybí vnořený podseznam — položku odsaďte alespoň dvěma mezerami pod nadřazenou položku.")
    if nested == "ordered-in-unordered" and not _ordered_inside_unordered(lines):
        return CheckResult(False, "Žádná položka nečíslovaného seznamu neobsahuje vnořený číslovaný podseznam (`  1. text` odsazený pod `- položka`).")
    return CheckResult(True)


_REF_DEF = re.compile(r"^\s*\[([^\]]+)\]:\s*\S+", re.M)


def _links_like(ctx: CheckContext, p: dict[str, Any], image: bool) -> CheckResult:
    t = ctx.no_code
    bang = "!" if image else "(?<!!)"
    inline_re = rf"{bang}\[[^\]]*\]\([^)]+\)" if image else rf"{bang}\[[^\]]+\]\([^)]+\)"
    ref_re = rf"{bang}\[[^\]]*\]\[([^\]]+)\]" if image else rf"{bang}\[[^\]]+\]\[([^\]]+)\]"
    co, inl, ref = ("obrázek", "![popis](url)", "![popis][id]") if image else ("odkaz", "[text](url)", "[text][id]")
    missing: list[str] = []
    if p.get("inline", True) and not re.search(inline_re, t):
        missing.append(f"inline {co} `{inl}`")
    if p.get("reference", True):
        referenced = {m.group(1).strip().lower() for m in re.finditer(ref_re, t)}
        defined = {m.group(1).strip().lower() for m in _REF_DEF.finditer(t)}
        if not (referenced & defined):
            missing.append(f"reference {co} `{ref}` s definicí `[id]: url` na samostatném řádku (odkazované id nemá definici)")
    if missing:
        return CheckResult(False, "Chybí: " + ", ".join(missing) + ".")
    return CheckResult(True)


@register("md.links")
def links(ctx: CheckContext, p: dict[str, Any]) -> CheckResult:
    return _links_like(ctx, p, image=False)


@register("md.images")
def images(ctx: CheckContext, p: dict[str, Any]) -> CheckResult:
    return _links_like(ctx, p, image=True)


def find_code_blocks(text: str) -> list[tuple[str, str]]:
    return re.findall(r"```([^\n`]*)\n(.*?)```", text, re.DOTALL)


@register("md.code")
def code(ctx: CheckContext, p: dict[str, Any]) -> CheckResult:
    missing: list[str] = []
    if p.get("block", True):
        blocks = find_code_blocks(ctx.raw)
        langs = [str(l).strip().lower() for l in p.get("block_lang", [])]
        if not blocks:
            missing.append("blok kódu ohraničený trojicí zpětných apostrofů (```) na samostatných řádcích")
        elif langs and not any(lang.strip().lower() in langs for lang, _ in blocks):
            missing.append(f"blok kódu s označením jazyka `{langs[0]}` hned za úvodními apostrofy (```{langs[0]})")
    if p.get("inline", True) and not re.search(r"(?<!`)`[^`\n]+`(?!`)", ctx.no_code):
        missing.append("inline kód mezi jednoduchými zpětnými apostrofy (`text`)")
    if missing:
        return CheckResult(False, "Chybí: " + ", ".join(missing) + ".")
    return CheckResult(True)


_TABLE_SEP = re.compile(r"^\s*\|?\s*:?-{3,}:?\s*(\|\s*:?-{3,}:?\s*)+\|?\s*$")


def find_tables(text: str) -> list[tuple[int, int]]:
    """Vrací (sloupce, datové řádky) pro každou tabulku s oddělovačem hlavičky."""
    lines = text.splitlines()
    tables: list[tuple[int, int]] = []
    i = 0
    while i < len(lines) - 1:
        header, sep = lines[i], lines[i + 1]
        if "|" in header and _TABLE_SEP.match(sep):
            cols = len(header.strip().strip("|").split("|"))
            rows = 0
            j = i + 2
            while j < len(lines) and "|" in lines[j] and lines[j].strip():
                rows += 1
                j += 1
            tables.append((cols, rows))
            i = j
        else:
            i += 1
    return tables


@register("md.table")
def table(ctx: CheckContext, p: dict[str, Any]) -> CheckResult:
    min_cols = int(p.get("min_cols", 2))
    min_rows = int(p.get("min_rows", 1))
    tables = find_tables(ctx.no_code)
    if not tables:
        return CheckResult(False, "Nenašla se tabulka — pod řádkem hlaviček chybí oddělovač `|---|---|`.")
    if any(c >= min_cols and r >= min_rows for c, r in tables):
        return CheckResult(True)
    best = max(tables, key=lambda t: (t[0] >= min_cols, t[1]))
    return CheckResult(False, f"Největší tabulka má {best[0]} sloupce a {best[1]} datových řádků; požadováno alespoň {min_cols} sloupce a {min_rows} řádky (hlavička se nepočítá).")


def _blockquote_groups(text: str) -> list[int]:
    groups: list[int] = []
    current = 0
    for line in text.splitlines():
        if re.match(r"^\s*>", line):
            current += 1
        else:
            if current:
                groups.append(current)
            current = 0
    if current:
        groups.append(current)
    return groups


@register("md.blockquote")
def blockquote(ctx: CheckContext, p: dict[str, Any]) -> CheckResult:
    groups = _blockquote_groups(ctx.no_code)
    if not groups:
        return CheckResult(False, "Nenašla se citace — řádek začínající znakem `>`.")
    missing: list[str] = []
    if p.get("single", False) and not any(g == 1 for g in groups):
        missing.append("jednořádková citace (jeden řádek `> text`)")
    if p.get("multi", False) and not any(g >= 2 for g in groups):
        missing.append("víceřádková citace (alespoň dva řádky za sebou začínající `>`)")
    if missing:
        return CheckResult(False, "Chybí: " + ", ".join(missing) + ".")
    return CheckResult(True)


@register("md.details")
def details(ctx: CheckContext, p: dict[str, Any]) -> CheckResult:
    t = ctx.raw.lower()
    if "<details>" in t and "</details>" in t and "<summary>" in t:
        return CheckResult(True)
    return CheckResult(False, "Chybí sbalitelný blok `<details><summary>Nadpis</summary> obsah </details>` (včetně `<summary>`).")


@register("md.checkboxes")
def checkboxes(ctx: CheckContext, p: dict[str, Any]) -> CheckResult:
    min_items = int(p.get("min_items", 1))
    mixed = bool(p.get("mixed", True))
    t = ctx.no_code
    unchecked = re.findall(r"^\s*[-*+]\s+\[\s?\]\s+\S", t, re.M)
    checked = re.findall(r"^\s*[-*+]\s+\[[xX]\]\s+\S", t, re.M)
    total = len(unchecked) + len(checked)
    if total < min_items:
        return CheckResult(False, f"Nalezeno {total} položek se zaškrtávacím políčkem (`- [ ] text`), požadováno alespoň {min_items}.")
    if mixed and not (unchecked and checked):
        stav = "zaškrtnuté" if checked else "nezaškrtnuté"
        return CheckResult(False, f"Všechny položky jsou {stav}; seznam má obsahovat oba stavy (`- [x]` i `- [ ]`).")
    return CheckResult(True)


@register("md.hr")
def hr(ctx: CheckContext, p: dict[str, Any]) -> CheckResult:
    for line in ctx.no_code.splitlines():
        s = line.strip()
        if re.fullmatch(r"-{3,}|\*{3,}|_{3,}", s):
            return CheckResult(True)
    return CheckResult(False, "Nenašla se horizontální čára — `---` na samostatném řádku s prázdným řádkem nad sebou.")


_FOOTNOTE_DEF = re.compile(r"^\s*\[\^([^\]]+)\]:", re.M)


@register("md.footnote")
def footnote(ctx: CheckContext, p: dict[str, Any]) -> CheckResult:
    t = ctx.no_code
    defined = {m.group(1).strip().lower() for m in _FOOTNOTE_DEF.finditer(t)}
    if not defined:
        return CheckResult(False, "Chybí definice poznámky pod čarou ve tvaru `[^1]: text` na samostatném řádku.")
    referenced: set[str] = set()
    for line in t.splitlines():
        if _FOOTNOTE_DEF.match(line):
            continue
        referenced.update(m.group(1).strip().lower() for m in re.finditer(r"\[\^([^\]]+)\]", line))
    if not (referenced & defined):
        return CheckResult(False, "Chybí odkaz na poznámku v textu — za slovo napište `[^1]` se stejným id jako u definice.")
    return CheckResult(True)
