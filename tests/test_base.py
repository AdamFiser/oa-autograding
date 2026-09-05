import oa_autograding


def test_version_is_string():
    assert isinstance(oa_autograding.__version__, str)
