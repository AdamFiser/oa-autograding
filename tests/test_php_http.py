import shutil

import pytest

from oa_autograding.checks import base
from oa_autograding.checks.base import CheckContext
import oa_autograding.checks  # noqa: F401

pytestmark = pytest.mark.skipif(shutil.which("php") is None, reason="PHP není nainstalované")

FORM = """<?php
declare(strict_types=1);
session_start();
$_SESSION['t'] ??= 'tajny-token';
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    if (($_POST['t'] ?? '') !== $_SESSION['t']) {
        http_response_code(403);
        exit('Neplatný token.');
    }
    $jmeno = trim($_POST['jmeno'] ?? '');
    if ($jmeno !== '') {
        header('Location: form.php?ok=1', true, 303);
        exit;
    }
    echo '<p>Vyplňte jméno.</p>';
}
if (isset($_GET['ok'])) { echo '<p>Děkujeme.</p>'; }
?>
<!-- Vyplňte jméno. (zadání v komentáři se nepočítá) -->
<form method="post"><input type="hidden" value="<?= $_SESSION['t'] ?>" name="t"><input name="jmeno"></form>
"""


def http(repo, **params):
    return base.get("php.http").fn(CheckContext(repo_root=repo.root, file=None), params)


def test_get_with_query_and_contains(repo):
    repo.write("index.php", "<p><?= htmlspecialchars($_GET['q'] ?? '') ?></p><p><?= count($_GET['z'] ?? []) ?></p>")
    ok = http(repo, steps=[{"path": "index.php", "query": {"q": "<b>škol</b>", "z[]": ["1", "2"]},
                            "expect": {"status": 200, "contains": ["<p>&lt;b&gt;škol&lt;/b&gt;</p>", "<p>2</p>"],
                                       "not_contains": ["<b>"]}}])
    assert ok.passed, ok.reason
    res = http(repo, steps=[{"path": "index.php", "label": "hledání", "expect": {"contains": ["Nalezeno"]}}])
    assert not res.passed and "hledání" in res.reason and "Nalezeno" in res.reason
    res = http(repo, steps=[{"path": "index.php", "query": {"q": "x"}, "expect": {"contains": ["Nalezeno"]}}])
    assert not res.passed and res.reason.startswith("`GET index.php?q=x`")


def test_not_contains_and_regex(repo):
    repo.write("index.php", "<b>ahoj</b>")
    res = http(repo, steps=[{"path": "index.php", "expect": {"not_contains": ["<b>ahoj</b>"]}}])
    assert not res.passed and "<b>ahoj</b>" in res.reason
    assert http(repo, steps=[{"path": "index.php", "expect": {"regex": r"<b>\w+</b>"}}]).passed
    assert not http(repo, steps=[{"path": "index.php", "expect": {"regex": r"<i>"}}]).passed
    res = http(repo, steps=[{"path": "index.php", "expect": {"regex": [r"<b>", r"<i>"]}}])
    assert not res.passed and "<i>" in res.reason


def test_html_comments_do_not_count(repo):
    repo.write("form.php", FORM)
    res = http(repo, steps=[{"path": "form.php", "expect": {"contains": ["Vyplňte jméno."]}}])
    assert not res.passed


def test_session_csrf_post_and_redirect(repo):
    repo.write("form.php", FORM)
    ok = http(repo, steps=[
        {"path": "form.php"},
        {"method": "POST", "path": "form.php", "form": {"jmeno": "Jan"}, "csrf": "t",
         "expect": {"status": 303, "location": "form.php?ok=1"}},
        {"path": "form.php?ok=1", "expect": {"contains": ["Děkujeme."]}},
    ])
    assert ok.passed, ok.reason
    invalid = http(repo, steps=[
        {"path": "form.php"},
        {"method": "POST", "path": "form.php", "form": {"jmeno": ""}, "csrf": "t", "expect": {"contains": ["Vyplňte jméno."]}},
    ])
    assert invalid.passed, invalid.reason
    # Bez tokenu (a bez session) odpoví stránka 403.
    no_token = http(repo, steps=[{"method": "POST", "path": "form.php", "form": {"jmeno": "Jan"},
                                  "expect": {"status": 403, "contains": ["Neplatný token."]}}])
    assert no_token.passed, no_token.reason
    wrong = http(repo, steps=[{"method": "POST", "path": "form.php", "form": {"jmeno": "Jan"}, "label": "odeslání",
                               "expect": {"status": 303}}])
    assert not wrong.passed and "403" in wrong.reason and "odeslání" in wrong.reason


def test_csrf_field_missing_is_skipped(repo):
    # Stránka bez tokenu (úkol s tokenem ještě není hotový): csrf pole se prostě nepošle.
    repo.write("index.php", "<?= $_SERVER['REQUEST_METHOD'] ?>:<?= implode(',', array_keys($_POST)) ?>")
    res = http(repo, steps=[{"path": "index.php"},
                            {"method": "POST", "path": "index.php", "form": {"a": "1"}, "csrf": "t",
                             "expect": {"contains": ["POST:a"]}}])
    assert res.passed, res.reason


def test_location_mismatch(repo):
    repo.write("index.php", "<?php header('Location: jinam.php', true, 302);")
    res = http(repo, steps=[{"path": "index.php", "expect": {"status": 303, "location": "index.php?ok=1"}}])
    assert not res.passed and "302" in res.reason
    res = http(repo, steps=[{"path": "index.php", "expect": {"location": "index.php?ok=1"}}])
    assert not res.passed and "jinam.php" in res.reason


def test_warnings_and_fatal(repo):
    repo.write("index.php", "<p><?= $nic ?></p>")
    assert http(repo, steps=[{"path": "index.php", "expect": {"contains": ["<p>"]}}]).passed
    res = http(repo, steps=[{"path": "index.php", "expect": {"no_warnings": True}}])
    assert not res.passed and "Warning" in res.reason and "$nic" in res.reason
    repo.write("index.php", "<?php trim(['x']);")
    res = http(repo, steps=[{"path": "index.php", "expect": {"contains": ["x"]}}])
    assert not res.passed and "TypeError" in res.reason


def test_upload_fixtures_and_files(repo):
    repo.write("up.php", """<?php
$f = $_FILES['foto'] ?? null;
if ($f && $f['error'] === UPLOAD_ERR_OK) {
    $typ = mime_content_type($f['tmp_name']);
    if ($typ === 'image/png') {
        move_uploaded_file($f['tmp_name'], __DIR__ . '/uploads/' . bin2hex(random_bytes(4)) . '.png');
    }
    echo $typ, ' ', $f['size'], ' ', $f['name'];
}
""")
    repo.write("uploads/.gitkeep", "")
    ok = http(repo, steps=[{"method": "POST", "path": "up.php", "files": {"foto": {"fixture": "png", "filename": "a.png"}},
                            "expect": {"contains": ["image/png"]}}],
              files=[{"glob": "uploads/*.png", "min": 1}, {"glob": "uploads/*.php", "max": 0}])
    assert ok.passed, ok.reason
    # Kontrola pracuje na kopii repa, žákovský checkout zůstane beze změny.
    assert list((repo.root / "uploads").glob("*.png")) == []
    php = http(repo, steps=[{"method": "POST", "path": "up.php",
                             "files": {"foto": {"fixture": "php", "filename": "foto.jpg", "content_type": "image/jpeg"}},
                             "expect": {"contains": ["text/x-php", "foto.jpg"]}}],
               files=[{"glob": "uploads/*.png", "min": 1}])
    assert not php.passed and "uploads/*.png" in php.reason
    big = http(repo, steps=[{"method": "POST", "path": "up.php", "files": {"foto": {"fixture": "png-3mb"}},
                             "expect": {"regex": r"image/png 3\d{6} "}}])
    assert big.passed, big.reason


def test_bad_spec(repo):
    repo.write("index.php", "x")
    assert "steps" in http(repo, steps=[]).reason
    assert "fixture" in http(repo, steps=[{"method": "POST", "path": "index.php",
                                           "files": {"f": {"fixture": "nic"}}}]).reason
