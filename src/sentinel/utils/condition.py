"""
Conditions (thresholds): the Extractor's universal syntax for "when does a number alert"

One text field replaces the many separate fields a detector would otherwise need (minimum, maximum,
drop, increase, percentage...). The syntax is the one the Extractor documentation describes under
Common Configurations > Condition (Threshold), and the one the Scala detectors read:

Basic comparison (>, <, >=, <= compare the absolute value unless the number carries a sign):
    = 100      value equals 100
    != 100     value does not equal 100
    > 50       |value| > 50
    >= 35      |value| >= 35
    < 25       |value| < 25
    <= 50      |value| <= 50

Explicit sign (the signed value, no absolute value):
    > +10      value > 10
    > -15      value > -15
    < -20      value < -20

Percentage change from the previous value, (v - v0) / v0 * 100 (absolute unless signed):
    > 25%      the change is more than 25%, up or down
    < -10%     the value fell by more than 10%
    = 100%     the value doubled

Delta (change from the previous value), ++ increase and -- decrease:
    > ++100    increase greater than 100
    >= ++30    increase of at least 30
    < --50     decrease greater than 50 (a decrease is compared by its size)
    <= --25    decrease of at least 25
    > ++25%    increase greater than 25%
    < --10%    decrease greater than 10%

Once (edge detection): alerts only when the condition turns true, not while it stays true:
    >> 10      once, when the value crosses above 10
    << 25      once, when the value crosses below 25
    >>= 10     once, when it reaches 10 or more
    <<= 25     once, when it reaches 25 or less
    >> ++100   once, when the increase crosses 100
    >> 25%     once, when the change crosses 25%

Max / min: alerts only on a new maximum (minimum) past the threshold:
    >>> 100    a new maximum above 100
    <<< 50     a new minimum below 50
    >>>= 100   a new maximum at or above 100
    <<<= 50    a new minimum at or below 50

Spaces are ignored: `> ++ 100` and `>++100` are the same condition.

Numbers are compared exactly (Decimal), never as floats: `= 4.0000000001` does not match 4. A value
given as a float is read through its shortest text form (0.1 is 0.1, not 0.1000000000000000055...).

Usage
-----
Stateless, the caller chooses the previous value:

    condition = parse_condition("< --10%")       # a drop of more than 10%
    condition.matches(900, previous=1000)        # False: a 10% drop is not more than 10%
    condition.matches(850, previous=1000)        # True: a 15% drop

Stateful, the previous value is the last one checked (what a Scala Threshold does):

    threshold = Threshold("> ++100")
    threshold.check(1000)   # False: no previous value yet
    threshold.check(1200)   # True: +200
"""

import re
from dataclasses import dataclass, field
from decimal import Decimal, InvalidOperation, localcontext
from typing import Dict, Optional, Union

Number = Union[int, float, Decimal, str]

# Exact arithmetic for percentages and deltas: well above the 38 digits of the largest ledger amounts.
PRECISION = 80

OPERATORS = ("gt", "gte", "lt", "lte", "eq", "neq")
SYMBOLS = {"gt": ">", "gte": ">=", "lt": "<", "lte": "<=", "eq": "=", "neq": "!="}

# Longest first, so `>>>=` is not read as `>>` followed by `>=`.
_PREFIXES = (
    (">>>=", "gte", "extreme"),
    ("<<<=", "lte", "extreme"),
    (">>>", "gt", "extreme"),
    ("<<<", "lt", "extreme"),
    (">>=", "gte", "once"),
    ("<<=", "lte", "once"),
    (">>", "gt", "once"),
    ("<<", "lt", "once"),
    (">=", "gte", "always"),
    ("<=", "lte", "always"),
    ("!=", "neq", "always"),
    ("==", "eq", "always"),
    (">", "gt", "always"),
    ("<", "lt", "always"),
    ("=", "eq", "always"),
)

# Plain digits with an optional fraction: no exponent, no separators, no inf/nan.
_NUMBER = re.compile(r"[0-9]+(\.[0-9]+)?|\.[0-9]+")
_SPACES = re.compile(r"\s+")


def to_decimal(value: Number) -> Decimal:
    """A number as an exact Decimal. Floats go through their shortest text form; bools and
    non-finite values are refused."""
    if isinstance(value, bool):
        raise ValueError("not a number")
    if isinstance(value, Decimal):
        number = value
    elif isinstance(value, (int, float, str)):
        try:
            number = Decimal(str(value).strip())
        except InvalidOperation:
            raise ValueError(f"not a number: {value!r}") from None
    else:
        raise ValueError(f"not a number: {value!r}")
    if not number.is_finite():
        raise ValueError(f"not a finite number: {value!r}")
    return number


@dataclass(frozen=True)
class Condition:
    """
    One parsed condition. Immutable: the state that once and max/min operators need lives in a
    `Threshold` (or in the `state` dict the caller passes to `matches`).
    """

    text: str  # as written, spaces included
    operator: str  # gt, gte, lt, lte, eq, neq
    number: Decimal  # signed: `> -15` is -15
    percent: bool = False  # `%`: compare the percentage change from the previous value
    delta: Optional[str] = None  # "increase" (++), "decrease" (--) or None
    mode: str = "always"  # always, once (>> <<), extreme (>>> <<<)
    absolute: bool = True  # compare |value| (>, >=, <, <= without an explicit sign)

    @property
    def needs_previous(self) -> bool:
        """Whether the condition compares with a previous value (percentage or delta)."""
        return self.percent or self.delta is not None

    @property
    def is_once(self) -> bool:
        return self.mode == "once"

    @property
    def is_extreme(self) -> bool:
        return self.mode == "extreme"

    @property
    def is_increase(self) -> bool:
        """`++`: only an increase can match."""
        return self.delta == "increase"

    @property
    def is_decrease(self) -> bool:
        """`--`: only a decrease can match."""
        return self.delta == "decrease"

    def __str__(self) -> str:
        return self.text

    # ------------------------------------------------------------------ evaluation

    def measure(self, value: Number, previous: Optional[Number] = None) -> Optional[Decimal]:
        """
        The quantity the operator compares with the number: the value itself, its change from
        `previous` (delta), or the percentage change. None when the condition cannot match at all:
        no previous value for a percentage or delta, an increase that did not happen for `++`, a
        decrease that did not happen for `--`.
        """
        current = to_decimal(value)
        if not self.needs_previous:
            return abs(current) if self.absolute else current
        if previous is None:
            return None
        before = to_decimal(previous)
        with localcontext() as ctx:
            ctx.prec = PRECISION
            change = current - before
            if self.percent:
                if before == 0:
                    if change == 0:
                        change = Decimal(0)
                    else:
                        change = Decimal("Infinity") if change > 0 else Decimal("-Infinity")
                else:
                    change = change * 100 / abs(before)
            if self.delta == "increase":
                return change if change > 0 else None
            if self.delta == "decrease":
                return -change if change < 0 else None
            return abs(change) if self.absolute else change

    def compare(self, measured: Decimal) -> bool:
        """The operator applied to a measured quantity (see `measure`)."""
        operator = self.operator
        if self.delta == "decrease":
            # A decrease is compared by its size: `< --50` reads "a decrease of more than 50".
            operator = {"lt": "gt", "lte": "gte"}.get(operator, operator)
        number = self.number
        if operator == "gt":
            return measured > number
        if operator == "gte":
            return measured >= number
        if operator == "lt":
            return measured < number
        if operator == "lte":
            return measured <= number
        if operator == "eq":
            return measured == number
        return measured != number

    def matches(self, value: Number, previous: Optional[Number] = None, state: Optional[Dict] = None) -> bool:
        """
        Whether `value` (with `previous` for a percentage or a delta) meets the condition.

        Once and max/min operators need memory between calls: pass the same `state` dict every
        time (one per series of values, e.g. per token); it is updated in place. Without a state
        they behave like their plain operator.
        """
        measured = self.measure(value, previous)
        result = measured is not None and self.compare(measured)
        if state is None or self.mode == "always":
            return result
        if self.mode == "once":
            fired = result and not state.get("was_true", False)
            state["was_true"] = result
            return fired
        # extreme: a new maximum (>>>) or minimum (<<<) of the measured quantity, past the number
        if measured is None:
            return False
        upward = self.operator in ("gt", "gte")
        best = state.get("extreme")
        is_new = best is None or (measured > best if upward else measured < best)
        if is_new:
            state["extreme"] = measured
        return result and is_new


def parse_condition(text: str) -> Condition:
    """
    `"> ++100"` -> Condition. Raises ValueError with a reason a person can act on. An empty text is
    refused here: whether empty means "no condition" or "every value" is the caller's choice.
    """
    if not isinstance(text, str):
        raise ValueError("a condition is text, for example > 1000")
    body = _SPACES.sub("", text)
    if not body:
        raise ValueError("empty condition: write an operator and a number, for example > 1000")
    for prefix, operator, mode in _PREFIXES:
        if body.startswith(prefix):
            rest = body[len(prefix) :]
            break
    else:
        raise ValueError(f"{text.strip()!r}: start with an operator (>, >=, <, <=, =, !=, >>, <<, >>>, <<<)")

    delta = None
    if rest.startswith("++"):
        delta, rest = "increase", rest[2:]
    elif rest.startswith("--"):
        delta, rest = "decrease", rest[2:]

    percent = rest.endswith("%")
    if percent:
        rest = rest[:-1]

    signed = rest[:1] in ("+", "-")
    if signed and delta is not None:
        raise ValueError(f"{text.strip()!r}: ++ and -- already give the direction, write the number without a sign")
    negative = rest.startswith("-")
    if signed:
        rest = rest[1:]

    if not _NUMBER.fullmatch(rest):
        raise ValueError(
            f"{text.strip()!r}: the number must be plain digits, for example 1000 or 4.05 (no exponent or separators)"
        )
    number = Decimal(rest)
    if negative:
        number = -number

    absolute = not signed and operator not in ("eq", "neq") and delta is None
    return Condition(
        text=text.strip(),
        operator=operator,
        number=number,
        percent=percent,
        delta=delta,
        mode=mode,
        absolute=absolute,
    )


def is_condition(text: str) -> bool:
    """Whether `text` parses as a condition."""
    try:
        parse_condition(text)
    except ValueError:
        return False
    return True


@dataclass
class Threshold:
    """
    A condition with its memory: the previous value for percentages and deltas, and the state of
    once and max/min operators. One Threshold per series of values (a token, an asset, an address).

        threshold = Threshold("> 25%")
        threshold.check(100)   # False: nothing to compare with yet
        threshold.check(130)   # True: +30%
    """

    condition: Condition
    previous: Optional[Decimal] = None
    state: Dict = field(default_factory=dict)

    def __init__(self, condition: Union[str, Condition]):
        self.condition = condition if isinstance(condition, Condition) else parse_condition(condition)
        self.previous = None
        self.state = {}

    def check(self, value: Number) -> bool:
        """Whether `value` meets the condition; it then becomes the previous value."""
        current = to_decimal(value)
        result = self.condition.matches(current, self.previous, self.state)
        self.previous = current
        return result

    def reset(self) -> None:
        self.previous = None
        self.state = {}
