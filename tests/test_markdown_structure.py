import pytest

from oa_autograding.checks import base
from oa_autograding.checks.base import CheckContext
import oa_autograding.checks  # noqa: F401


def run(repo, text, type_, **params):
    repo.write("a.md", text)
    return base.get(type_).fn(CheckContext.for_file(repo.root, "a.md"), params)


def test_headings_default_pass(repo):
    assert run(repo, "# A\n\n## B\n", "md.headings", levels_any_of=[2, 3]).passed


def test_headings_missing_h1(repo):
    res = run(repo, "## B\n", "md.headings")
    assert not res.passed and "H1" in res.reason


def test_headings_missing_any_of(repo):
    res = run(repo, "# A\n", "md.headings", levels_any_of=[2, 3])
    assert not res.passed and "H2 nebo H3" in res.reason


def test_headings_all_required(repo):
    assert run(repo, "# A\n## B\n### C\n", "md.headings", levels_required=[1, 2, 3]).passed
    assert not run(repo, "# A\n## B\n", "md.headings", levels_required=[1, 2, 3]).passed


def test_headings_ignore_code_blocks(repo):
    assert not run(repo, "```\n# A\n```\n", "md.headings").passed


def test_formatting_pass(repo):
    assert run(repo, "**t** *k* ~~p~~", "md.formatting").passed
    assert run(repo, "__t__ _k_ ~~p~~", "md.formatting").passed


def test_formatting_reports_missing(repo):
    res = run(repo, "**t** jen tučně", "md.formatting")
    assert not res.passed
    assert "kurzíva" in res.reason and "přeškrtnutý" in res.reason and "tučný" not in res.reason


def test_formatting_subset(repo):
    assert run(repo, "**t**", "md.formatting", italic=False, strikethrough=False).passed


def test_formatting_ignores_inline_code(repo):
    res = run(repo, "Metoda `__init__` a `moje_promenna_x` ~~p~~ *k*", "md.formatting")
    assert not res.passed and "tučný" in res.reason


def test_formatting_pass_with_inline_code_present(repo):
    assert run(repo, "**t** *k* ~~p~~ plus `__init__`", "md.formatting").passed


def test_formatting_ignores_snake_case_in_plain_text(repo):
    # GFM podtržítka uvnitř slova nevykreslí, kontrola je nesmí brát jako formátování.
    res = run(repo, "Soubor it_markdown_practice.md a metoda v tride. ~~p~~", "md.formatting")
    assert not res.passed and "kurzíva" in res.reason and "tučný" in res.reason


def test_formatting_counts_dunder_as_bold_like_github(repo):
    # `__init__` obklopené mezerami GitHub podle CommonMark opravdu vykreslí tučně,
    # takže se uznává; falešně pozitivní byla jen kurzíva ze snake_case uvnitř slova.
    res = run(repo, "Soubor it_markdown_practice.md a metoda __init__ v tride.", "md.formatting")
    assert not res.passed and "kurzíva" in res.reason and "tučný" not in res.reason


def test_formatting_accepts_underscore_variants_on_word_boundary(repo):
    assert run(repo, "Text _kurzíva_ a __tučně__ a ~~p~~ tady.", "md.formatting").passed


def test_anchor_link(repo):
    assert run(repo, "[Sekce](#sekce)", "md.anchor-link").passed
    res = run(repo, "[Web](https://x.cz)", "md.anchor-link")
    assert not res.passed and "#kotva" in res.reason


def test_anchor_link_rejects_image_with_anchor(repo):
    # `![alt](#k)` je obrázek, ne odkaz na sekci.
    res = run(repo, "![alt](#kotva)\n", "md.anchor-link")
    assert not res.passed and "#kotva" in res.reason


def test_anchor_link_accepts_normal_link_next_to_image(repo):
    assert run(repo, "![alt](#kotva) a [Sekce](#sekce)\n", "md.anchor-link").passed


def test_anchor_link_ignores_html_comment(repo):
    res = run(repo, "<!-- např. [Funkce](#funkce) -->\n", "md.anchor-link")
    assert not res.passed


def test_list_unordered_min(repo):
    assert run(repo, "- a\n- b\n- c\n- d\n", "md.list", min_items=4).passed
    res = run(repo, "- a\n- b\n", "md.list", min_items=4)
    assert not res.passed and "2" in res.reason and "4" in res.reason


def test_list_ordered_min(repo):
    assert run(repo, "1. a\n2. b\n3. c\n", "md.list", kind="ordered", min_items=3).passed
    assert not run(repo, "- a\n- b\n- c\n", "md.list", kind="ordered", min_items=3).passed


def test_list_nested_any(repo):
    assert run(repo, "- a\n  - a1\n- b\n", "md.list", nested="any").passed
    res = run(repo, "- a\n- b\n", "md.list", nested="any")
    assert not res.passed and "vnořený" in res.reason


def test_list_nested_any_accepts_tab_indent(repo):
    # GitHub vykreslí jeden tabulátor jako vnoření, kontrola ho nesmí odmítnout.
    assert run(repo, "- a\n\t- b\n", "md.list", nested="any").passed


def test_list_nested_ordered_in_unordered_accepts_tab_indent(repo):
    assert run(repo, "- a\n\t1. x\n", "md.list", nested="ordered-in-unordered").passed


def test_list_nested_ordered_in_unordered(repo):
    ok = "- a\n  1. x\n  2. y\n- b\n"
    assert run(repo, ok, "md.list", nested="ordered-in-unordered").passed
    assert not run(repo, "- a\n  - x\n", "md.list", nested="ordered-in-unordered").passed
    assert not run(repo, "1. a\n   - x\n", "md.list", nested="ordered-in-unordered").passed
