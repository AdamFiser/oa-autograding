"""Základ kontrol: kontext souboru, výsledek a registr typů."""
from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable


@dataclass(frozen=True)
class CheckResult:
    passed: bool
    reason: str | None = None  # česky, pro žáka (proč neprošlo)
    details: str | None = None  # technický detail, jen do Release


@dataclass
class CheckContext:
    repo_root: Path
    file: Path | None  # None = kontrola nepracuje se souborem
    raw: str = ""
    no_code: str = ""

    @classmethod
    def for_file(cls, repo_root: Path, rel: str) -> "CheckContext":
        path = repo_root / rel
        raw = path.read_text(encoding="utf-8-sig", errors="replace")
        return cls(repo_root=repo_root, file=path, raw=raw, no_code=strip_code_blocks(raw))


Checker = Callable[[CheckContext, dict[str, Any]], CheckResult]


@dataclass(frozen=True)
class Registered:
    fn: Checker
    needs_file: bool


class UnknownCheckType(KeyError):
    """Typ kontroly není registrován."""


_REGISTRY: dict[str, Registered] = {}


def register(type_name: str, *, needs_file: bool = True) -> Callable[[Checker], Checker]:
    def decorator(fn: Checker) -> Checker:
        if type_name in _REGISTRY:
            raise RuntimeError(f"typ kontroly {type_name!r} je registrován dvakrát")
        _REGISTRY[type_name] = Registered(fn, needs_file)
        return fn

    return decorator


def get(type_name: str) -> Registered:
    try:
        return _REGISTRY[type_name]
    except KeyError:
        raise UnknownCheckType(type_name) from None


def is_registered(type_name: str) -> bool:
    return type_name in _REGISTRY


def registered_types() -> list[str]:
    return sorted(_REGISTRY)


def strip_code_blocks(text: str) -> str:
    """Nahradí fenced bloky kódu a HTML komentáře prázdnými řádky (regexy pak nevidí falešné nadpisy
    ani příkladovou syntaxi schovanou v komentáři)."""
    text = re.sub(r"```.*?```", lambda m: "\n" * m.group(0).count("\n"), text, flags=re.DOTALL)
    text = re.sub(r"<!--.*?-->", lambda m: "\n" * m.group(0).count("\n"), text, flags=re.DOTALL)
    return text
