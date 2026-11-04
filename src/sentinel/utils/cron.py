"""
The detector's `cron` field, read as a time window

Detectors that measure something over time (a change within a period, a count of transfers) take
the period from their `cron` field, as the Scala detectors do: a cron of one hour means a one hour
window. The field accepts what the Scala detectors accept:

    "1h", "1 hour", "10 min", "90s", "2 days"   a duration
    "60000"                                     milliseconds
    "0 * * * *"                                 a cron expression (5 fields)
    "0 0 * * * ?"                               a Quartz expression (6 or 7 fields, seconds first)

A cron expression's window is the shortest gap between two consecutive runs over a week. It never
depends on when the detector starts: only on weekdays is one day, also from a Thursday. The week is
a fixed one (from Monday 2021-01-04); a schedule that runs less often than that takes the first gap
after it, so a monthly cron is always 28 days.

Quartz and Unix number the days differently, and each form keeps its own: in a Quartz expression
SUN is 1 and SAT is 7, in a 5-field one SUN is 0. The seconds of a Quartz expression count (0/30 is
30 seconds); its year is checked, and does not change the gap.
"""

import re
from datetime import datetime, timedelta, timezone
from functools import lru_cache
from typing import Optional

from croniter import croniter
from pydantic import BaseModel, Field

UNITS_MS = {
    "ms": 1,
    "s": 1_000,
    "sec": 1_000,
    "secs": 1_000,
    "second": 1_000,
    "seconds": 1_000,
    "m": 60_000,
    "min": 60_000,
    "mins": 60_000,
    "minute": 60_000,
    "minutes": 60_000,
    "h": 3_600_000,
    "hr": 3_600_000,
    "hour": 3_600_000,
    "hours": 3_600_000,
    "d": 86_400_000,
    "day": 86_400_000,
    "days": 86_400_000,
}

_DURATION = re.compile(r"([0-9]+)\s*([a-zA-Z]+)?")

_YEAR_ITEM = r"[0-9]{4}(-[0-9]{4})?(/[0-9]+)?"
_QUARTZ_YEAR = re.compile(rf"\*(/[0-9]+)?|{_YEAR_ITEM}(,{_YEAR_ITEM})*")
# A day number: not a step (1/2) nor the position in the month (6#3).
_QUARTZ_DAY = re.compile(r"(?<![/#0-9])[0-9]+")

# One second before Monday 00:00, so a run on that Monday counts. Not a leap year, nor the one after.
_WEEK_START = datetime(2021, 1, 3, 23, 59, 59, tzinfo=timezone.utc)
# Enough for the shortest gap of any schedule: a dense one repeats it from the start, and walking a
# whole week of seconds would take 10 seconds.
_MAX_RUNS = 10_000


class CronSchema(BaseModel):
    """The `cron` field, to mix into a detector's schema. Detectors override the default."""

    cron: str = Field(
        default="1h",
        title="Cron",
        description="How often the detector checks, which is also its time window: 1h, 10 min, 1d or a cron expression",
    )


def cron_interval_ms(value: str, now: Optional[datetime] = None) -> int:
    """
    `"1h"` -> 3600000. Raises ValueError with the reason when the text is none of the forms above.
    `now` has no effect: the window does not depend on when it is read.
    """
    if not isinstance(value, str) or not value.strip():
        raise ValueError("empty cron: write a duration (1h, 10 min) or a cron expression")
    text = value.strip()
    match = _DURATION.fullmatch(text)
    if match:
        number, unit = int(match.group(1)), match.group(2) or "ms"
        # Other units ignore case, but M is a month to whoever writes it, never a minute.
        if unit == "M" or unit.lower() not in UNITS_MS:
            raise ValueError(f"{text!r}: unknown unit {unit!r}, use s, min, h or d")
        ms = number * UNITS_MS[unit.lower()]
        if ms <= 0:
            raise ValueError(f"{text!r}: the interval must be longer than zero")
        return ms
    return _expression_interval_ms(text)


def _quartz_weekdays(field: str) -> str:
    """The day-of-week field from Quartz numbers (SUN=1) to croniter's (SUN=0). Names stay as they are."""

    def shift(match: re.Match) -> str:
        day = int(match.group())
        if not 1 <= day <= 7:
            raise ValueError(f"day {day}: Quartz days go from 1 (SUN) to 7 (SAT)")
        return str(day - 1)

    return _QUARTZ_DAY.sub(shift, field)


@lru_cache(maxsize=256)
def _expression_interval_ms(text: str) -> int:
    fields = text.split()
    quartz = len(fields) in (6, 7)
    if quartz and len(fields) == 7:
        # The year only says which years run: it can remove runs, never bring two closer.
        if not _QUARTZ_YEAR.fullmatch(fields[6]):
            raise ValueError(f"{text!r}: not a valid cron expression (year {fields[6]!r})")
        fields = fields[:6]
    if not quartz and len(fields) != 5:
        raise ValueError(f"{text!r}: not a duration (1h, 10 min) nor a cron expression")
    # "?" is "no specific value", and only the two day fields can say it.
    for position in (-3, -1):
        fields[position] = fields[position].replace("?", "*")
    try:
        if quartz:
            fields[-1] = _quartz_weekdays(fields[-1])
        cron = croniter(" ".join(fields), _WEEK_START, second_at_beginning=quartz)
        previous = cron.get_next(datetime)
        week_end = previous + timedelta(days=7)
        shortest = None
        for _ in range(_MAX_RUNS):
            current = cron.get_next(datetime)
            gap = current - previous
            shortest = gap if shortest is None else min(shortest, gap)
            if current >= week_end:
                break
            previous = current
    except (ValueError, KeyError) as err:
        raise ValueError(f"{text!r}: not a valid cron expression ({err})") from None
    return int(shortest.total_seconds() * 1000)
