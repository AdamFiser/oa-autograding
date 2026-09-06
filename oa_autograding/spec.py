"""Načtení a validace checks.json (schema oa-autograding/checks/v1)."""
from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from oa_autograding import checks as _checks  # noqa: F401  (import registruje typy kontrol)
from oa_autograding.checks.base import is_registered

SCHEMA = "oa-autograding/checks/v1"
_CHECK_KEYS = {"id", "description", "type", "points", "hint", "docs", "file"}


class SpecError(ValueError):
    """Neplatný checks.json — zpráva říká, kde je problém."""


@dataclass(frozen=True)
class Check:
    id: str
    label: str
    description: str
    type: str
    points: int
    hint: str | None
    docs: str | None
    file: str | None
    params: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class Task:
    id: str
    name: str
    prefix: str | None
    file: str | None
    checks: tuple[Check, ...]

    @property
    def max_points(self) -> int:
        return sum(c.points for c in self.checks)


@dataclass(frozen=True)
class Spec:
    title: str
    docs: str | None
    tasks: tuple[Task, ...]

    @property
    def max_points(self) -> int:
        return sum(t.max_points for t in self.tasks)


def load_spec(path: Path) -> Spec:
    try:
        text = path.read_text(encoding="utf-8-sig")
    except FileNotFoundError:
        raise SpecError(f"{path}: soubor neexistuje") from None
    try:
        data = json.loads(text)
    except json.JSONDecodeError as e:
        raise SpecError(f"{path}: neplatný JSON ({e})") from None
    return parse_spec(data)


def parse_spec(data: Any) -> Spec:
    if not isinstance(data, dict):
        raise SpecError("kořen musí být objekt")
    if data.get("schema") != SCHEMA:
        raise SpecError(f"schema musí být {SCHEMA!r}")
    title = _req_str(data, "title", "kořen")
    docs = _opt_str(data, "docs", "kořen")
    tasks_raw = data.get("tasks")
    if not isinstance(tasks_raw, list) or not tasks_raw:
        raise SpecError("tasks musí být neprázdný seznam")
    tasks = tuple(_parse_task(t, i) for i, t in enumerate(tasks_raw))
    _no_duplicates([t.id for t in tasks], "tasks[].id")
    return Spec(title=title, docs=docs, tasks=tasks)


def resolve_docs(spec: Spec, check: Check) -> str | None:
    if check.docs is None:
        return spec.docs
    if check.docs.startswith(("http://", "https://")):
        return check.docs
    if spec.docs is None:
        return None
    if check.docs.startswith("#"):
        return spec.docs + check.docs
    return spec.docs.rstrip("/") + "/" + check.docs.lstrip("/")


def _parse_task(raw: Any, idx: int) -> Task:
    where = f"tasks[{idx}]"
    if not isinstance(raw, dict):
        raise SpecError(f"{where}: musí být objekt")
    prefix = _opt_str(raw, "prefix", where)
    checks_raw = raw.get("checks")
    if not isinstance(checks_raw, list) or not checks_raw:
        raise SpecError(f"{where}.checks musí být neprázdný seznam")
    checks = tuple(
        _parse_check(c, f"{where}.checks[{i}]", prefix, i + 1) for i, c in enumerate(checks_raw)
    )
    _no_duplicates([c.id for c in checks], f"{where}.checks[].id")
    return Task(
        id=_req_str(raw, "id", where),
        name=_req_str(raw, "name", where),
        prefix=prefix,
        file=_opt_str(raw, "file", where),
        checks=checks,
    )


def _parse_check(raw: Any, where: str, prefix: str | None, number: int) -> Check:
    if not isinstance(raw, dict):
        raise SpecError(f"{where}: musí být objekt")
    ctype = _req_str(raw, "type", where)
    if not is_registered(ctype):
        raise SpecError(f"{where}.type: neznámý typ kontroly {ctype!r}")
    points = raw.get("points", 1)
    if isinstance(points, bool) or not isinstance(points, int) or points < 1:
        raise SpecError(f"{where}.points: musí být celé číslo >= 1")
    return Check(
        id=_req_str(raw, "id", where),
        label=f"{prefix}{number}" if prefix else str(number),
        description=_req_str(raw, "description", where),
        type=ctype,
        points=points,
        hint=_opt_str(raw, "hint", where),
        docs=_opt_str(raw, "docs", where),
        file=_opt_str(raw, "file", where),
        params={k: v for k, v in raw.items() if k not in _CHECK_KEYS},
    )


def _req_str(d: dict[str, Any], key: str, where: str) -> str:
    v = d.get(key)
    if not isinstance(v, str) or not v.strip():
        raise SpecError(f"{where}.{key}: povinný neprázdný řetězec")
    return v


def _opt_str(d: dict[str, Any], key: str, where: str) -> str | None:
    v = d.get(key)
    if v is None:
        return None
    if not isinstance(v, str):
        raise SpecError(f"{where}.{key}: musí být řetězec")
    return v


def _no_duplicates(ids: list[str], where: str) -> None:
    seen: set[str] = set()
    for i in ids:
        if i in seen:
            raise SpecError(f"{where}: duplicitní id {i!r}")
        seen.add(i)
