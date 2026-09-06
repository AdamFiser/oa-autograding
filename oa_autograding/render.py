"""Český Markdown pro Release, Job Summary a komentář ve Feedback PR."""
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

from oa_autograding.grade import GradeReport, TaskReport
from oa_autograding.spec import resolve_docs

MARKER = "<!-- oa-autograding -->"


@dataclass(frozen=True)
class GradeEnv:
    commit_sha: str
    commit_url: str | None
    release_url: str | None
    graded_at: datetime


@dataclass(frozen=True)
class HistoryEntry:
    when: datetime
    sha7: str
    score: int
    max_score: int
    failed_labels: list[str]
    release_url: str | None


def _prague(dt: datetime) -> datetime:
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    try:
        return dt.astimezone(ZoneInfo("Europe/Prague"))
    except ZoneInfoNotFoundError:  # chybí tzdata (Windows bez balíčku)
        return dt.astimezone(timezone.utc)


def format_cz(dt: datetime, with_year: bool = True) -> str:
    d = _prague(dt)
    rok = f" {d.year}" if with_year else ""
    return f"{d.day}. {d.month}.{rok} {d:%H:%M}"


def of_word(n: int) -> str:
    return "bodu" if n == 1 else "bodů"


def _cell(text: str) -> str:
    return text.replace("|", "\\|").replace("\n", " ").strip()


def _hint(report: GradeReport, t: TaskReport, idx: int) -> str:
    o = t.outcomes[idx]
    parts: list[str] = []
    if o.reason:
        parts.append(o.reason)
    if o.check.hint:
        parts.append(o.check.hint)
    url = resolve_docs(report.spec, o.check)
    if url:
        parts.append(f"Viz [prezentace]({url}).")
    return _cell(" ".join(parts))


def _details_block(report: GradeReport) -> list[str]:
    """Technické detaily nesplněných kontrol (výjimky, výstup `run`) — sbalené na konci."""
    items = [(o.check.label, o.details) for t in report.tasks for o in t.outcomes if not o.passed and o.details]
    if not items:
        return []
    lines = ["<details>", "<summary>Technické detaily</summary>", ""]
    for label, text in items:
        lines += [f"- **{label}:**", "", "  ```", *[f"  {l}" for l in str(text).splitlines() or [""]], "  ```", ""]
    lines += ["</details>", ""]
    return lines


def render_release_body(report: GradeReport, env: GradeEnv) -> str:
    lines = [f"**Automatická kontrola: {report.score} z {report.max_score} {of_word(report.max_score)}**", ""]
    sha7 = env.commit_sha[:7] or "?"
    commit = f"[`{sha7}`]({env.commit_url})" if env.commit_url else f"`{sha7}`"
    lines.append(f"Hodnocený commit {commit}, {format_cz(env.graded_at)}. Komentář se při každém dalším pushi přepíše aktuálním stavem.")
    lines.append("")
    for t in report.tasks:
        soubor = f" · `{t.task.file}`" if t.task.file else ""
        lines.append(f"### {t.task.name}{soubor} · {t.score}/{t.max_score}")
        lines.append("")
        if t.missing_file:
            labels = ", ".join(o.check.label for o in t.outcomes)
            lines.append(f"Soubor `{t.missing_file}` v repozitáři není, požadavky {labels} jsou proto za 0 bodů. Vytvořte ho přesně s tímto názvem v kořeni repozitáře.")
        elif t.passed:
            lines.append("Všechny požadavky splněny. 🎉")
        else:
            lines.append("| # | Stav | Požadavek | Nápověda |")
            lines.append("|---|---|---|---|")
            for i, o in enumerate(t.outcomes):
                stav = "✅" if o.passed else "❌"
                napoveda = "" if o.passed else _hint(report, t, i)
                lines.append(f"| {o.check.label} | {stav} | {_cell(o.check.description)} | {napoveda} |")
        lines.append("")
    lines += _details_block(report)
    pata = "Dotazy k hodnocení pište sem do PR."
    if env.release_url:
        pata = f"Podrobnosti v [Release]({env.release_url}). " + pata
    lines.append(f"<sub>{pata}</sub>")
    return "\n".join(lines)


def render_history(entries: list[HistoryEntry]) -> str:
    if not entries:
        return ""
    lines = [
        "<details>",
        f"<summary>Historie odevzdání ({len(entries)})</summary>",
        "",
        "| Datum | Commit | Body | Nesplněno |",
        "|---|---|---|---|",
    ]
    for e in entries:
        commit = f"[{e.sha7}]({e.release_url})" if e.release_url else e.sha7
        nesplneno = ", ".join(e.failed_labels) if e.failed_labels else "—"
        lines.append(f"| {format_cz(e.when, with_year=False)} | {commit} | {e.score}/{e.max_score} | {nesplneno} |")
    lines += ["", "</details>"]
    return "\n".join(lines)


def render_comment(release_body: str, entries: list[HistoryEntry], marker: str = MARKER) -> str:
    parts = [marker, release_body.rstrip()]
    history = render_history(entries)
    if history:
        parts += ["", history]
    return "\n".join(parts) + "\n"


def render_error_body(run_url: str) -> str:
    return (
        "**Automatická kontrola neproběhla kvůli technické chybě.**\n\n"
        f"Nejde o chybu ve vašem řešení. Napište učiteli; podrobnosti jsou v [záznamu běhu]({run_url})."
    )
