from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_shim_placeholders():
    shim = (ROOT / "templates" / "shim.yaml").read_text(encoding="utf-8")
    assert shim.count("{{ORG}}") == 1
    assert "cancel-in-progress: true" in shim
    assert "adamfiser/oa-autograding/.github/actions/feedback-comment@" in shim
    assert 'branches: [main, master]' in shim


def test_autograder_stub_pins_version():
    stub = (ROOT / "templates" / "autograder.py").read_text(encoding="utf-8")
    assert 'VERSION = "v1-rc"' in stub
    assert "oa_autograding.runner" in stub
    compile(stub, "autograder.py", "exec")
