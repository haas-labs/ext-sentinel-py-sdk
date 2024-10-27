from sentinel.utils.version import is_bugfix


def test_utils_version_is_bugfix():
    assert is_bugfix("0.1", "0.1"), "Incorrect detection of bug-fix version"
    assert is_bugfix("0.1", "0.1.0"), "Incorrect detection of bug-fix version"
    assert is_bugfix("0.1", "0.1.1"), "Incorrect detection of bug-fix version"
    assert is_bugfix("0.1", "0.1.10"), "Incorrect detection of bug-fix version"

    assert is_bugfix("0.1", "00.01.10"), "Incorrect detection of bug-fix version"

    assert is_bugfix("0.1.1", "0.1.1"), "Incorrect detection of bug-fix version"

    assert not is_bugfix("0.2", "0.1.1"), "Incorrect detection of bug-fix version"
    assert not is_bugfix("0.1", "0.2.1"), "Incorrect detection of bug-fix version"
