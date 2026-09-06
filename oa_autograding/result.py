"""result.json podle smlouvy classroom50/result/v1."""
from __future__ import annotations

from datetime import datetime
from typing import Any, Mapping

from oa_autograding.grade import GradeReport

_NAME_BYTES = 100


def _clip_utf8(text: str, limit: int) -> str:
    data = text.encode("utf-8")
    if len(data) <= limit:
        return text
    ellipsis = "…"
    budget = limit - len(ellipsis.encode("utf-8"))
    return data[:budget].decode("utf-8", errors="ignore") + ellipsis


def build_result(report: GradeReport, env: Mapping[str, str], graded_at: datetime) -> dict[str, Any]:
    tests = [
        {
            "test-name": _clip_utf8(f"{o.check.label} {o.check.description}", _NAME_BYTES),
            "passed": o.passed,
            "score": o.score,
            "max-score": o.check.points,
        }
        for t in report.tasks
        for o in t.outcomes
    ]
    return {
        "schema": "classroom50/result/v1",
        "classroom": env.get("CLASSROOM", ""),
        "assignment": env.get("ASSIGNMENT", ""),
        "submission": env.get("SUBMISSION_TAG", ""),
        "commit": env.get("COMMIT_URL", ""),
        "release": env.get("RELEASE_URL", ""),
        "review": env.get("REVIEW_URL", ""),
        "datetime": graded_at.strftime("%Y-%m-%dT%H:%M:%SZ"),
        "score": report.score,
        "max-score": report.max_score,
        "tests": tests,
    }
