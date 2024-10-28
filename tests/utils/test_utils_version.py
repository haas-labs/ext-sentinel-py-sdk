import pytest

from sentinel.utils.version import IncorrectVersionFormat, is_bugfix


def test_utils_version_is_bugfix():
    assert is_bugfix("0.1", "0.1"), "Incorrect detection of bug-fix version"
    assert is_bugfix("0.1", "0.1.0"), "Incorrect detection of bug-fix version"
    assert is_bugfix("0.1", "0.1.1"), "Incorrect detection of bug-fix version"
    assert is_bugfix("0.1", "0.1.10"), "Incorrect detection of bug-fix version"

    assert is_bugfix("0.1", "00.01.10"), "Incorrect detection of bug-fix version"

    assert not is_bugfix("0.2", "0.1.1"), "Incorrect detection of bug-fix version"
    assert not is_bugfix("0.1", "0.2.1"), "Incorrect detection of bug-fix version"


def test_utils_version_is_exact_version():
    assert is_bugfix("0.1.1", "0.1.1"), "Incorrect detection of exact version"
    assert not is_bugfix("0.1.1", "0.1.2"), "Incorrect detection of version mappings"
    assert not is_bugfix("0.2.1", "0.2.2"), "Incorrect detection of version mappings"


def test_utils_version_corrupted_version():
    # Main version
    with pytest.raises(IncorrectVersionFormat):
        assert is_bugfix("0,1,1", "0.1.1"), "Incorrectly handle wrong version format"

    with pytest.raises(IncorrectVersionFormat):
        assert is_bugfix("0.1.a", "0.1.1"), "Incorrectly handle wrong version format"

    with pytest.raises(IncorrectVersionFormat):
        assert is_bugfix("0.1.1.1", "0.1.1"), "Incorrectly handle wrong version format"

    # Version
    with pytest.raises(IncorrectVersionFormat):
        assert is_bugfix("0.1.1", "0,1,1"), "Incorrectly handle wrong version format"

    with pytest.raises(IncorrectVersionFormat):
        assert is_bugfix("0.1.1", "0.1.a"), "Incorrectly handle wrong version format"

    with pytest.raises(IncorrectVersionFormat):
        assert is_bugfix("0.1.1", "0.1.1.1"), "Incorrectly handle wrong version format"
