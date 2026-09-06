"""Lokální CLI: ověření checks.json proti adresáři (pro učitele, skill i žáka)."""
from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

from oa_autograding.checks.base import registered_types
from oa_autograding.grade import grade
from oa_autograding.render import GradeEnv, render_release_body
from oa_autograding.result import build_result
from oa_autograding.spec import SpecError, load_spec


def main(argv: list[str] | None = None) -> int:
    try:  # Windows konzole (cp1250) neumí ✅/❌ — bez přepnutí by výpis spadl
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, OSError):
        pass
    parser = argparse.ArgumentParser(prog="oa-check", description="Kontroly cvičení oa-autograding.")
    sub = parser.add_subparsers(dest="cmd", required=True)
    chk = sub.add_parser("check", help="Ohodnotí adresář podle checks.json a vypíše výsledek.")
    chk.add_argument("--spec", required=True, type=Path, help="cesta ke checks.json")
    chk.add_argument("--repo", default=Path("."), type=Path, help="kořen hodnoceného repozitáře (výchozí .)")
    chk.add_argument("--json", action="store_true", help="vypsat result.json místo textu")
    sub.add_parser("types", help="Vypíše registrované typy kontrol.")
    args = parser.parse_args(argv)

    if args.cmd == "types":
        print("\n".join(registered_types()))
        return 0

    try:
        spec = load_spec(args.spec)
    except SpecError as e:
        print(f"oa-check: neplatný checks.json — {e}", file=sys.stderr)
        return 2
    report = grade(spec, args.repo)
    now = datetime.now(timezone.utc)
    if args.json:
        print(json.dumps(build_result(report, {}, now), ensure_ascii=False, indent=2))
    else:
        print(render_release_body(report, GradeEnv("lokální", None, None, now)))
    return 0 if report.passed else 1
