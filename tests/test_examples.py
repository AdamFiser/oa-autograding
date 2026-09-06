from pathlib import Path

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
