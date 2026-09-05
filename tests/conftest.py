from __future__ import annotations

from pathlib import Path

import pytest


class Repo:
    """Dočasný „žákovský checkout“ — zapisuje soubory relativně ke kořeni."""

    def __init__(self, root: Path) -> None:
        self.root = root

    def write(self, rel: str, text: str) -> Path:
        p = self.root / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(text, encoding="utf-8")
        return p


@pytest.fixture
def repo(tmp_path: Path) -> Repo:
    return Repo(tmp_path)
