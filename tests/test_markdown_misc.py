from oa_autograding.checks import base
from oa_autograding.checks.base import CheckContext
import oa_autograding.checks  # noqa: F401


def run(repo, text, type_, **params):
    repo.write("a.md", text)
    return base.get(type_).fn(CheckContext.for_file(repo.root, "a.md"), params)


def test_blockquote_any(repo):
    assert run(repo, "> a\n", "md.blockquote").passed
    res = run(repo, "text\n", "md.blockquote")
    assert not res.passed and ">" in res.reason


def test_blockquote_single_and_multi(repo):
    assert run(repo, "> a\n\n> b\n> c\n", "md.blockquote", single=True, multi=True).passed
    res = run(repo, "> a\n", "md.blockquote", single=True, multi=True)
    assert not res.passed and "víceřádková" in res.reason
    res = run(repo, "> a\n> b\n", "md.blockquote", single=True, multi=True)
    assert not res.passed and "jednořádková" in res.reason


def test_details(repo):
    assert run(repo, "<details>\n<summary>S</summary>\nx\n</details>\n", "md.details").passed
    res = run(repo, "<details>x</details>", "md.details")
    assert not res.passed and "summary" in res.reason


def test_details_ignores_html_comment(repo):
    res = run(repo, "<!-- <details><summary>x</summary>y</details> -->\n", "md.details")
    assert not res.passed


def test_checkboxes_pass(repo):
    assert run(repo, "- [x] a\n- [ ] b\n- [ ] c\n", "md.checkboxes", min_items=3).passed


def test_checkboxes_too_few(repo):
    res = run(repo, "- [x] a\n- [ ] b\n", "md.checkboxes", min_items=3)
    assert not res.passed and "2" in res.reason and "3" in res.reason


def test_checkboxes_not_mixed(repo):
    res = run(repo, "- [ ] a\n- [ ] b\n- [ ] c\n", "md.checkboxes", min_items=3)
    assert not res.passed and "nezaškrtnuté" in res.reason
    assert run(repo, "- [ ] a\n- [ ] b\n", "md.checkboxes", min_items=2, mixed=False).passed


def test_hr(repo):
    assert run(repo, "a\n\n---\n\nb\n", "md.hr").passed
    assert run(repo, "***\n", "md.hr").passed
    res = run(repo, "| a |\n|---|\n", "md.hr")
    assert not res.passed and "---" in res.reason


def test_hr_rejects_setext_underline(repo):
    # `Nadpis\n---` GitHub vykreslí jako nadpis H2, ne jako čáru.
    res = run(repo, "Nadpis\n---\n", "md.hr")
    assert not res.passed and "---" in res.reason


def test_hr_rejects_yaml_front_matter(repo):
    res = run(repo, "---\ntitle: x\n---\n", "md.hr")
    assert not res.passed


def test_footnote(repo):
    assert run(repo, "Text[^1].\n\n[^1]: Poznámka.\n", "md.footnote").passed
    res = run(repo, "Text.\n\n[^1]: Poznámka.\n", "md.footnote")
    assert not res.passed and "odkaz" in res.reason
    res = run(repo, "Text[^1].\n", "md.footnote")
    assert not res.passed and "definice" in res.reason


def test_footnote_id_mismatch(repo):
    res = run(repo, "Text[^1].\n\n[^2]: Poznámka.\n", "md.footnote")
    assert not res.passed and ("definice" in res.reason or "odkaz" in res.reason)


def test_footnote_id_case_insensitive(repo):
    assert run(repo, "Text[^a].\n\n[^A]: P.\n", "md.footnote").passed
