from oa_autograding.checks import base
from oa_autograding.checks.base import CheckContext
import oa_autograding.checks  # noqa: F401


def run(repo, text, type_, **params):
    repo.write("a.md", text)
    return base.get(type_).fn(CheckContext.for_file(repo.root, "a.md"), params)


def test_links_pass(repo):
    assert run(repo, "[a](https://a.cz) a [b][1]\n\n[1]: https://b.cz\n", "md.links").passed


def test_links_missing_reference_definition(repo):
    res = run(repo, "[a](https://a.cz) a [b][1]\n", "md.links")
    assert not res.passed and "reference" in res.reason


def test_links_ignore_images(repo):
    res = run(repo, "![a](x.png) ![b][1]\n\n[1]: y.png\n", "md.links")
    assert not res.passed and "inline" in res.reason


def test_images_pass(repo):
    assert run(repo, "![a](x.png) ![b][1]\n\n[1]: y.png\n", "md.images").passed


def test_images_only_inline(repo):
    res = run(repo, "![a](x.png)", "md.images")
    assert not res.passed and "reference" in res.reason
    assert run(repo, "![a](x.png)", "md.images", reference=False).passed


def test_links_reference_id_mismatch(repo):
    res = run(repo, "[a](https://a.cz) [b][1]\n\n[2]: https://b.cz\n", "md.links")
    assert not res.passed and "reference" in res.reason


def test_links_reference_case_insensitive(repo):
    assert run(repo, "[a](https://a.cz) [b][Wiki]\n\n[wiki]: https://b.cz\n", "md.links").passed


def test_images_reference_id_mismatch(repo):
    res = run(repo, "![a](x.png) ![b][1]\n\n[2]: y.png\n", "md.images")
    assert not res.passed and "reference" in res.reason


def test_images_reference_case_insensitive(repo):
    assert run(repo, "![a](x.png) ![b][Logo]\n\n[logo]: y.png\n", "md.images").passed


def test_code_pass(repo):
    assert run(repo, "```bash\nls\n```\ntext `x`\n", "md.code", block_lang=["bash", "sh"]).passed


def test_code_missing_lang(repo):
    res = run(repo, "```\nls\n```\n`x`\n", "md.code", block_lang=["bash"])
    assert not res.passed and "bash" in res.reason


def test_code_missing_inline(repo):
    res = run(repo, "```\nls\n```\n", "md.code")
    assert not res.passed and "inline" in res.reason


def test_code_no_block(repo):
    res = run(repo, "`x`", "md.code")
    assert not res.passed and "blok" in res.reason


def test_table_pass(repo):
    t = "| a | b |\n|---|---|\n| 1 | 2 |\n| 3 | 4 |\n| 5 | 6 |\n"
    assert run(repo, t, "md.table", min_cols=2, min_rows=3).passed


def test_table_too_small(repo):
    t = "| a | b |\n|---|---|\n| 1 | 2 |\n"
    res = run(repo, t, "md.table", min_cols=2, min_rows=3)
    assert not res.passed and "1" in res.reason and "3" in res.reason


def test_table_none(repo):
    res = run(repo, "| a | b |\n| 1 | 2 |\n", "md.table")
    assert not res.passed and "oddělovač" in res.reason
