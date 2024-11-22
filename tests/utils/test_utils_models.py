import pytest

from sentinel.utils.models import scientific_notation_to_int


@pytest.mark.parametrize(
    "input_value, expected_output",
    [
        ("1e6", 1000000),
        (1e6, 1000000),
        ("2.5e3", 2500),
        (2.5e3, 2500),
        (123, 123),
        ("123", 123),
        (0, 0),
        ("0", 0),
    ],
)
def test_scientific_notation_to_int_valid(input_value, expected_output):
    assert scientific_notation_to_int(input_value) == expected_output


@pytest.mark.parametrize(
    "input_value",
    [
        "abc",
        "1.2.3",
        None,
        [],
        {},
        set(),
    ],
)
def test_scientific_notation_to_int_invalid(input_value):
    with pytest.raises(ValueError):
        scientific_notation_to_int(input_value)
