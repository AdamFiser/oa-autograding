import shutil
from pathlib import Path

import pytest

from oa_autograding.grade import grade
from oa_autograding.spec import load_spec

EX = Path(__file__).resolve().parents[1] / "examples" / "scm_10_markdown"


def test_spec_loads_with_expected_shape():
    spec = load_spec(EX / "checks.json")
    a, b = spec.tasks
    assert [c.label for c in a.checks] == [f"A{i}" for i in range(1, 16)]
    assert [c.label for c in b.checks] == [f"B{i}" for i in range(1, 13)]
    assert spec.max_points == 27
    assert spec.docs is None  # bez odkazů na slajdy
    assert all(c.hint for t in spec.tasks for c in t.checks)


def test_kostra_fails_expected_checks():
    rep = grade(load_spec(EX / "checks.json"), EX / "kostra")
    a, b = rep.tasks
    assert b.missing_file == "it_markdown_practice.md" and b.score == 0
    # Kostra má H1 („# TODO“) i H2 sekce a už obsahuje `---`, takže A1 a A13 projdou;
    # všechno ostatní chybí, včetně A15 (zbývají TODO značky).
    assert "A1" not in a.failed_labels
    assert "A13" not in a.failed_labels
    assert set(a.failed_labels) == {"A2", "A3", "A4", "A5", "A6", "A7", "A8", "A9", "A10", "A11", "A12", "A14", "A15"}
    assert rep.score < rep.max_score


def test_reseni_passes_everything():
    rep = grade(load_spec(EX / "checks.json"), EX / "reseni")
    assert rep.passed, rep.failed_labels
    assert rep.score == rep.max_score == 27


PY_EX = Path(__file__).resolve().parents[1] / "examples" / "py_co_umim_z_pva1"


def test_py_kostra_fails_all_but_run():
    rep = grade(load_spec(PY_EX / "checks.json"), PY_EX / "kostra")
    # Kostra jsou jen data bez výpočtu, takže doběhne bez chyby (A1); vše ostatní chybí.
    assert rep.score == 1 and "A1" not in rep.failed_labels


def test_py_reseni_passes_everything():
    rep = grade(load_spec(PY_EX / "checks.json"), PY_EX / "reseni")
    assert rep.passed, rep.failed_labels
    assert rep.score == rep.max_score == 23


PHP_EX = Path(__file__).resolve().parents[1] / "examples" / "php_02_vystup_html"
needs_php = pytest.mark.skipif(shutil.which("php") is None, reason="PHP není nainstalované")


@needs_php
def test_php_kostra_fails_all_but_no_warnings():
    rep = grade(load_spec(PHP_EX / "checks.json"), PHP_EX / "kostra")
    a, b = rep.tasks
    # Kostra se vykreslí bez varování (A23); text zadání v HTML komentářích se nepočítá.
    assert a.score == 1 and "A23" not in a.failed_labels
    assert b.missing_file == "aboutme.php" and b.score == 0


@needs_php
def test_php_reseni_passes_everything():
    rep = grade(load_spec(PHP_EX / "checks.json"), PHP_EX / "reseni")
    assert rep.passed, rep.failed_labels
    assert rep.score == rep.max_score == 37


PHP06_EX = Path(__file__).resolve().parents[1] / "examples" / "php_06_include_require"


@needs_php
def test_php06_kostra_passes_only_regression_guards():
    rep = grade(load_spec(PHP06_EX / "checks.json"), PHP06_EX / "kostra")
    # Kostra se vykreslí bez varování a s kartami (C5, C6, D4); vše, co vyžaduje rozdělení do souborů, chybí.
    labels = {c.label for t in rep.tasks for c in t.task.checks}
    assert labels - set(rep.failed_labels) == {"C5", "C6", "D4"}
    assert rep.score == 3


@needs_php
def test_php06_reseni_passes_everything():
    rep = grade(load_spec(PHP06_EX / "checks.json"), PHP06_EX / "reseni")
    assert rep.passed, rep.failed_labels
    assert rep.score == rep.max_score == 35
