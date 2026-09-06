"""Spustí kontroly ze Spec nad žákovským checkoutem a sečte body."""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from oa_autograding.checks import base
from oa_autograding.checks.base import CheckContext, CheckResult
from oa_autograding.spec import Check, Spec, Task


@dataclass
class CheckOutcome:
    check: Check
    file: str | None
    passed: bool
    score: int
    reason: str | None
    details: str | None


@dataclass
class TaskReport:
    task: Task
    outcomes: list[CheckOutcome]
    missing_file: str | None

    @property
    def score(self) -> int:
        return sum(o.score for o in self.outcomes)

    @property
    def max_score(self) -> int:
        return self.task.max_points

    @property
    def passed(self) -> bool:
        return all(o.passed for o in self.outcomes)

    @property
    def failed_labels(self) -> list[str]:
        return [o.check.label for o in self.outcomes if not o.passed]


@dataclass
class GradeReport:
    spec: Spec
    tasks: list[TaskReport]

    @property
    def score(self) -> int:
        return sum(t.score for t in self.tasks)

    @property
    def max_score(self) -> int:
        return self.spec.max_points

    @property
    def passed(self) -> bool:
        return all(t.passed for t in self.tasks)

    @property
    def failed_labels(self) -> list[str]:
        return [l for t in self.tasks for l in t.failed_labels]


def grade(spec: Spec, repo_root: Path) -> GradeReport:
    reports: list[TaskReport] = []
    for task in spec.tasks:
        outcomes = [_run_check(task, check, repo_root) for check in task.checks]
        missing = task.file if task.file is not None and not (repo_root / task.file).is_file() else None
        reports.append(TaskReport(task, outcomes, missing))
    return GradeReport(spec, reports)


def _run_check(task: Task, check: Check, repo_root: Path) -> CheckOutcome:
    rel = check.file or task.file
    reg = base.get(check.type)
    if reg.needs_file:
        if rel is None:
            return _fail(check, None, "Kontrola nemá zadaný soubor (chyba v checks.json).")
        if not (repo_root / rel).is_file():
            return _fail(check, rel, f"Soubor `{rel}` v repozitáři není.")
        ctx = CheckContext.for_file(repo_root, rel)
    else:
        ctx = CheckContext(repo_root, (repo_root / rel) if rel else None)
    try:
        res = reg.fn(ctx, check.params)
    except Exception as e:  # kontrola nesmí shodit hodnocení
        res = CheckResult(False, None, f"Kontrola selhala výjimkou: {type(e).__name__}: {e}")
    return CheckOutcome(check, rel, res.passed, check.points if res.passed else 0, res.reason, res.details)


def _fail(check: Check, rel: str | None, reason: str) -> CheckOutcome:
    return CheckOutcome(check, rel, False, 0, reason, None)
