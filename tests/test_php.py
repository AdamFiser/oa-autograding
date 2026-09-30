import shutil

import pytest

from oa_autograding.checks import base
from oa_autograding.checks.base import CheckContext
import oa_autograding.checks  # noqa: F401

pytestmark = pytest.mark.skipif(shutil.which("php") is None, reason="PHP není nainstalované")


def page(repo, text, **params):
    repo.write("index.php", text)
    return base.get("php.page").fn(CheckContext.for_file(repo.root, "index.php"), params)


def test_included_and_regex(repo):
    src = "<h1><?php echo 'Hello, world!'; ?></h1>"
    assert page(repo, src, expected="<h1>Hello, world!</h1>").passed
    assert page(repo, src, expected=r"<h1>\s*Hello, world!\s*</h1>", comparison="regex").passed


def test_html_comments_do_not_count(repo):
    res = page(repo, "<!-- Očekávaný výstup: Hello, world! -->\n<h1>Statický text</h1>", expected="Hello, world!")
    assert not res.passed and "komentáře" in res.reason


def test_query_fills_get(repo):
    src = "<strong><?php echo htmlspecialchars(trim($_GET['hledat'] ?? '')); ?></strong>"
    assert page(repo, src, query={"hledat": "  <i>a</i>  "}, expected="<strong>&lt;i&gt;a&lt;/i&gt;</strong>").passed
    assert page(repo, src, expected="<strong></strong>").passed
    res = page(repo, src, query={"hledat": "web"}, expected="auto")
    assert not res.passed and "?hledat=web" in res.reason


def test_no_warnings(repo):
    src = "<p><?php echo $undefined; ?></p>"
    assert page(repo, src, expected="<p></p>").passed  # varování samo o sobě výstup nekazí
    res = page(repo, src, no_warnings=True)
    assert not res.passed and "Warning" in res.reason and "$undefined" in res.reason
    assert page(repo, "<p><?php echo 1; ?></p>", no_warnings=True).passed


def test_fatal_and_parse_error(repo):
    res = page(repo, "<?php undefined_function(); ?>", expected="x")
    assert not res.passed and "Fatal error" in res.reason
    res = page(repo, "<?php echo 'x' ?> <?php ... ?>", expected="x")
    assert not res.passed and "Parse error" in res.reason


def test_bad_comparison(repo):
    res = page(repo, "x", expected="x", comparison="exact")
    assert not res.passed and "checks.json" in res.reason
