from decimal import Decimal

import pytest

from sentinel.utils.condition import Condition, Threshold, is_condition, parse_condition


def series(text, values):
    """The results of a Threshold over a series of values."""
    threshold = Threshold(text)
    return [threshold.check(v) for v in values]


# ------------------------------------------------------------------ parsing


@pytest.mark.parametrize(
    "text, operator, number, percent, delta, mode, absolute",
    [
        ("= 100", "eq", "100", False, None, "always", False),
        ("== 100", "eq", "100", False, None, "always", False),
        ("!= 100", "neq", "100", False, None, "always", False),
        ("> 50", "gt", "50", False, None, "always", True),
        ("< 25", "lt", "25", False, None, "always", True),
        (">= 35", "gte", "35", False, None, "always", True),
        ("<= 50", "lte", "50", False, None, "always", True),
        ("> +10", "gt", "10", False, None, "always", False),
        ("> -15", "gt", "-15", False, None, "always", False),
        ("< +30", "lt", "30", False, None, "always", False),
        ("< -20", "lt", "-20", False, None, "always", False),
        ("> 25%", "gt", "25", True, None, "always", True),
        ("< 10%", "lt", "10", True, None, "always", True),
        (">= 50%", "gte", "50", True, None, "always", True),
        ("= 100%", "eq", "100", True, None, "always", False),
        ("> ++100", "gt", "100", False, "increase", "always", False),
        ("< --50", "lt", "50", False, "decrease", "always", False),
        (">= ++30", "gte", "30", False, "increase", "always", False),
        ("= ++20", "eq", "20", False, "increase", "always", False),
        ("> ++25%", "gt", "25", True, "increase", "always", False),
        (">> 10", "gt", "10", False, None, "once", True),
        ("<< 25", "lt", "25", False, None, "once", True),
        (">>= 10", "gte", "10", False, None, "once", True),
        ("<<= 25", "lte", "25", False, None, "once", True),
        (">> ++100", "gt", "100", False, "increase", "once", False),
        (">> 25%", "gt", "25", True, None, "once", True),
        (">>> 100", "gt", "100", False, None, "extreme", True),
        ("<<< 50", "lt", "50", False, None, "extreme", True),
        (">>>= 100", "gte", "100", False, None, "extreme", True),
        ("<<<= 50", "lte", "50", False, None, "extreme", True),
        (">= 4.05", "gte", "4.05", False, None, "always", True),
        (">=.5", "gte", "0.5", False, None, "always", True),
    ],
)
def test_every_form_of_the_documentation_parses(text, operator, number, percent, delta, mode, absolute):
    condition = parse_condition(text)
    assert condition.operator == operator
    assert condition.number == Decimal(number)
    assert condition.percent is percent
    assert condition.delta == delta
    assert condition.mode == mode
    assert condition.absolute is absolute
    assert condition.text == text


@pytest.mark.parametrize("text", ["> ++ 100", ">++100", " >  ++100 ", "> ++\t100", "> ++100\n"])
def test_spaces_are_ignored(text):
    assert parse_condition(text) == parse_condition("> ++100").__class__(
        text=text.strip(), operator="gt", number=Decimal(100), delta="increase", absolute=False
    )


@pytest.mark.parametrize(
    "text",
    [
        "",
        "   ",
        "100",
        "> ",
        ">",
        "> abc",
        "> 1e3",
        "> 1,000",
        "> inf",
        "> nan",
        "=> 5",
        "~ 5",
        "> ++",
        "> ++-5",
        "> 5%%",
        None,
        5,
    ],
)
def test_invalid_conditions_are_refused_with_a_reason(text):
    with pytest.raises(ValueError):
        parse_condition(text)
    assert not is_condition(text) if isinstance(text, str) else True


def test_the_condition_shows_as_written():
    assert str(parse_condition(">= 1000")) == ">= 1000"


# ------------------------------------------------------------------ basic comparisons


@pytest.mark.parametrize(
    "text, value, expected",
    [
        ("= 100", 100, True),
        ("= 100", -100, False),
        ("!= 100", 99, True),
        ("!= 100", 100, False),
        ("> 50", 51, True),
        ("> 50", -51, True),  # absolute value
        ("> 50", 50, False),
        ("< 25", -24, True),
        ("< 25", -26, False),
        (">= 35", 35, True),
        ("<= 50", -50, True),
        ("> +10", 11, True),
        ("> +10", -11, False),  # signed: no absolute value
        ("> -15", -14, True),
        ("> -15", -16, False),
        ("< -20", -21, True),
        ("< -20", 21, False),
        ("< +30", -100, True),
    ],
)
def test_basic_comparisons(text, value, expected):
    assert parse_condition(text).matches(value) is expected


def test_numbers_are_compared_exactly():
    assert parse_condition("= 4.0000000001").matches(Decimal("4")) is False
    assert parse_condition("= 4.0000000001").matches(Decimal("4.0000000001")) is True
    assert parse_condition("> 4.05").matches(Decimal("4.0500000001")) is True
    assert parse_condition("> 4.05").matches(4.05) is False
    assert parse_condition("= 0.1").matches(0.1) is True  # a float goes through its shortest text
    assert parse_condition(">= 99999999999999999999999999999999999.9999999999").matches(
        Decimal("99999999999999999999999999999999999.9999999999")
    )


def test_a_plain_comparison_stays_exact_past_the_default_precision():
    amount = Decimal("1234567890123456789012345678.1234567891")  # 38 digits, 10 decimals
    assert parse_condition("> 1234567890123456789012345678.1").matches(amount) is True
    assert parse_condition("<= 1234567890123456789012345678.1234567891").matches(amount) is True
    assert parse_condition("> -12345678901234567890123456789012").number == Decimal("-12345678901234567890123456789012")


def test_a_value_that_is_not_a_number_is_refused():
    for value in ("abc", True, None, float("nan"), float("inf")):
        with pytest.raises(ValueError):
            parse_condition("> 1").matches(value)


# ------------------------------------------------------------------ percentage and delta


@pytest.mark.parametrize(
    "text, value, previous, expected",
    [
        ("> 25%", 1300, 1000, True),
        ("> 25%", 700, 1000, True),  # -30%, absolute
        ("> 25%", 1200, 1000, False),
        ("< 10%", 1050, 1000, True),
        (">= 50%", 1500, 1000, True),
        ("= 100%", 2000, 1000, True),
        ("< -10%", 850, 1000, True),  # signed: a fall of more than 10%
        ("< -10%", 1200, 1000, False),
        ("> 10%", 5, 0, True),  # from zero: an infinite change
        ("> 10%", 0, 0, False),
        ("> ++100", 1200, 1000, True),
        ("> ++100", 1100, 1000, False),
        ("> ++100", 500, 1000, False),  # a decrease never matches ++
        ("< --50", 900, 1000, True),  # a decrease of 100 > 50
        ("< --50", 960, 1000, False),
        ("< --50", 1100, 1000, False),  # an increase never matches --
        ("<= --25", 975, 1000, True),
        (">= ++30", 1030, 1000, True),
        ("= ++20", 1020, 1000, True),
        ("> ++25%", 1300, 1000, True),
        ("> ++25%", 700, 1000, False),
        ("< --10%", 850, 1000, True),
        ("< --10%", 900, 1000, False),  # exactly 10% is not more than 10%
        ("<= --10%", 900, 1000, True),
    ],
)
def test_changes_from_the_previous_value(text, value, previous, expected):
    assert parse_condition(text).matches(value, previous=previous) is expected


def test_a_change_without_a_previous_value_never_matches():
    for text in ("> 25%", "> ++100", "< --50", "> ++25%"):
        condition = parse_condition(text)
        assert condition.needs_previous
        assert condition.matches(10**9) is False
    assert not parse_condition("> 5").needs_previous


def test_a_percentage_from_a_negative_value_keeps_its_direction():
    # -100 -> -50 is a rise of 50%: the base is taken by its size
    assert parse_condition("> ++40%").matches(-50, previous=-100) is True


# ------------------------------------------------------------------ once and max/min


def test_once_fires_on_the_crossing_only():
    assert series(">> 10", [5, 11, 12, 15, 8, 20]) == [False, True, False, False, False, True]
    assert series("<< 25", [30, 20, 10, 30, 24]) == [False, True, False, False, True]
    assert series(">>= 10", [9, 10, 10]) == [False, True, False]
    assert series("<<= 25", [26, 25, 24]) == [False, True, False]


def test_once_with_a_change():
    assert series(">> ++100", [1000, 1200, 1400, 1450, 1600]) == [False, True, False, False, True]
    assert series(">> 25%", [100, 130, 170, 180, 300]) == [False, True, False, False, True]


def test_new_maximum_as_in_the_documentation():
    assert series(">>> 100", [90, 200, 150, 300, 200]) == [False, True, False, True, False]


def test_new_minimum():
    assert series("<<< 50", [60, 40, 45, 30, 30, 10]) == [False, True, False, True, False, True]
    assert series(">>>= 100", [100, 100, 101]) == [True, False, True]
    assert series("<<<= 50", [50, 50, 49]) == [True, False, True]


def test_without_a_state_once_and_extreme_behave_like_the_plain_operator():
    assert parse_condition(">> 10").matches(11) is True
    assert parse_condition(">>> 100").matches(200) is True


def test_a_threshold_keeps_the_previous_value_and_resets():
    threshold = Threshold("> ++100")
    assert threshold.check(1000) is False
    assert threshold.check(1200) is True
    assert threshold.previous == Decimal(1200)
    threshold.reset()
    assert threshold.check(1400) is False


def test_a_threshold_takes_a_parsed_condition():
    condition = parse_condition("> 5")
    assert isinstance(condition, Condition)
    assert Threshold(condition).check(6) is True


def test_a_negative_base_divides_by_its_size():
    assert series("> 10%", [-100, -50]) == [False, True]  # +50%
    assert series("< -10%", [-100, -50]) == [False, False]
    assert series("< -10%", [-100, -150]) == [False, True]  # -50%
    assert parse_condition("= 50%").matches(-50, previous=-100) is True


def test_a_new_maximum_after_a_move_from_zero():
    # the move from zero alerts; 5 -> 10 (+100%) and 10 -> 100 (+900%) are new maxima, 100 -> 1000 (+900%) is not
    assert series(">>> 10%", [0, 5, 10, 100, 1000]) == [False, True, True, True, False]


def test_a_second_move_from_zero_does_not_wipe_the_maximum():
    # +900%, then from zero (alerts, not kept), +900% is no record, +1100% is
    assert series(">>> 10%", [100, 1000, 0, 5, 50, 600]) == [False, True, False, True, False, True]


def test_the_record_of_a_decrease_follows_the_operator_as_written():
    # <<< keeps a minimum, >>> a maximum, of the size of the drop; `--` does not swap them
    drops = [1000, 850, 700, 400]  # -15%, -17.6%, -42.9%
    assert series(">>>= --10%", drops) == [False, True, True, True]
    assert series("<<<= --10%", drops) == [False, True, False, False]
