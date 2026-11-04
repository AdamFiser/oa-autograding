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


def test_source_contains_ignores_comments(repo):
    src = "<?php\n// getGreeting( jen v komentáři\n$g = 'Ahoj'; ?>\n<!-- getGreeting( -->\n<p><?= $g ?></p>\n"
    res = page(repo, src, expected="<p>Ahoj</p>", source_contains=["getGreeting("])
    assert not res.passed and "chybí `getGreeting(`" in res.reason
    src = "<?php\nfunction getGreeting(): string { return 'Ahoj'; }\n$g = getGreeting ( ); ?>\n<p><?= $g ?></p>\n"
    assert page(repo, src, expected="<p>Ahoj</p>", source_contains=["getGreeting(", "$g=getGreeting()"]).passed


def test_bad_comparison(repo):
    res = page(repo, "x", expected="x", comparison="exact")
    assert not res.passed and "checks.json" in res.reason


def fn(repo, text, **params):
    repo.write("functions.php", text)
    return base.get("php.function").fn(CheckContext.for_file(repo.root, "functions.php"), params)


GOOD = """<?php
declare(strict_types=1);

function getDaysWord(int $days): string {
    $count = abs($days);
    if ($count === 1) {
        return 'den';
    }
    return $count >= 2 && $count <= 4 ? 'dny' : 'dní';
}

function average(array $grades): float {
    return $grades === [] ? 0.0 : round(array_sum($grades) / count($grades), 2);
}

function findFirst(array $items): ?string {
    return $items[0] ?? null;
}

function countAll(array $chapters): int {
    $count = 0;
    foreach ($chapters as $chapter) {
        $count += 1 + countAll($chapter['chapters']);
    }
    return $count;
}
"""
DAYS = [{"args": [1], "expected": "den"}, {"args": [3], "expected": "dny"}, {"args": [-2], "expected": "dny"},
        {"args": [5], "expected": "dní"}]


def test_function_cases_pass(repo):
    assert fn(repo, GOOD, name="getDaysWord", cases=DAYS, typed=True).passed
    assert fn(repo, GOOD, name="average", cases=[{"args": [[1, 2]], "expected": 1.5}, {"args": [[]], "expected": 0}]).passed
    assert fn(repo, GOOD, name="findFirst", cases=[{"args": [["a"]], "expected": "a"}, {"args": [[]], "expected": None}]).passed
    outline = [{"chapters": [{"chapters": []}]}, {"chapters": []}]
    assert fn(repo, GOOD, name="countAll", cases=[{"args": [outline], "expected": 3}], calls_itself=True).passed


def test_function_wrong_result_names_call(repo):
    res = fn(repo, GOOD, name="getDaysWord", cases=[{"args": [5], "expected": "dny"}])
    assert not res.passed and '`getDaysWord(5)` vrátila "dní", očekáváno "dny"' in res.reason
    res = fn(repo, GOOD, name="average", cases=[{"args": [[1, 2]], "label": "dvě známky", "expected": 2}])
    assert not res.passed and "`average(dvě známky)`" in res.reason


def test_function_type_matters(repo):
    res = fn(repo, GOOD, name="findFirst", cases=[{"args": [["1"]], "expected": 1}])
    assert not res.passed and 'vrátila "1"' in res.reason


def test_function_missing_and_syntax_error(repo):
    res = fn(repo, GOOD, name="getGreeting", cases=[])
    assert not res.passed and "není funkce `getGreeting`" in res.reason
    res = fn(repo, "<?php\nfunction a(): int { return 1 }\n", name="a")
    assert not res.passed and "ParseError" in res.reason
    res = fn(repo, "<?php\nfunction a(): int { return 1; }\nfunction a(): int { return 2; }\n", name="a")
    assert not res.passed and "nejde načíst" in res.reason and "Cannot redeclare" in res.reason


def test_function_echo_instead_of_return(repo):
    src = "<?php\nfunction printDeadline(int $d): void {\n    echo 'Zbývá ' . $d;\n}\n"
    res = fn(repo, src, name="printDeadline", cases=[{"args": [3], "expected": "Zbývá 3"}])
    assert not res.passed and "vypisuje text" in res.reason and "return" in res.reason


def test_function_strict_types_and_errors(repo):
    src = "<?php\nfunction twice(string $n): int {\n    return (int) $n * 2;\n}\n"
    res = fn(repo, src, name="twice", cases=[{"args": [5], "expected": 10}])
    assert not res.passed and "TypeError" in res.reason


def test_function_typed(repo):
    src = "<?php\nfunction a($x) {\n    return $x;\n}\nfunction b(int $x) {\n    return $x;\n}\n"
    res = fn(repo, src, name="a", cases=[{"args": [1], "expected": 1}], typed=True)
    assert not res.passed and "$x" in res.reason and "datový typ" in res.reason
    res = fn(repo, src, name="b", cases=[{"args": [1], "expected": 1}], typed=True)
    assert not res.passed and "návratové hodnoty" in res.reason
    assert fn(repo, src, name="a", cases=[{"args": [1], "expected": 1}]).passed


def test_function_calls_itself(repo):
    src = "<?php\nfunction countAll(array $c): int {\n    return count($c);\n}\n"
    res = fn(repo, src, name="countAll", cases=[{"args": [[1, 2]], "expected": 2}], calls_itself=True)
    assert not res.passed and "rekurzí" in res.reason


def test_function_needs_name(repo):
    res = fn(repo, GOOD, cases=[])
    assert not res.passed and "checks.json" in res.reason
