"""
The detector's `cron` field, read as a time window

Detectors that measure something over time (a change within a period, a count of transfers) take
the period from their `cron` field, as the Scala detectors do: a cron of one hour means a one hour
window. The field accepts what the Scala detectors accept:

    "1h", "1 hour", "10 min", "90s", "2 days"   a duration
    "60000"                                     milliseconds
    "0 * * * *"                                 a cron expression (5 fields)
    "0 0 * * * ?"                               a Quartz expression (6 or 7 fields, seconds first)

A cron expression's window is the time between two consecutive runs; for an irregular one (only on
weekdays, twice a day at uneven hours) the gap between the next two runs from now.
"""

import re
from datetime import datetime, timezone
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


class CronSchema(BaseModel):
    """The `cron` field, to mix into a detector's schema. Detectors override the default."""

    cron: str = Field(
        default="1h",
        title="Cron",
        description="How often the detector checks, which is also its time window: 1h, 10 min, 1d or a cron expression",
    )


def cron_interval_ms(value: str, now: Optional[datetime] = None) -> int:
    """`"1h"` -> 3600000. Raises ValueError with the reason when the text is none of the forms above."""
    if not isinstance(value, str) or not value.strip():
        raise ValueError("empty cron: write a duration (1h, 10 min) or a cron expression")
    text = value.strip()
    match = _DURATION.fullmatch(text)
    if match:
        number, unit = int(match.group(1)), (match.group(2) or "ms").lower()
        if unit not in UNITS_MS:
            raise ValueError(f"{text!r}: unknown unit {unit!r}, use s, min, h or d")
        ms = number * UNITS_MS[unit]
        if ms <= 0:
            raise ValueError(f"{text!r}: the interval must be longer than zero")
        return ms
    return _expression_interval_ms(text, now)


def _expression_interval_ms(text: str, now: Optional[datetime]) -> int:
    fields = text.split()
    if len(fields) in (6, 7):
        # Quartz: seconds first, optional year last, "?" for "no specific value"
        fields = fields[1:6]
    if len(fields) != 5:
        raise ValueError(f"{text!r}: not a duration (1h, 10 min) nor a cron expression")
    expression = " ".join(f.replace("?", "*") for f in fields)
    try:
        cron = croniter(expression, now or datetime.now(tz=timezone.utc))
        first = cron.get_next(datetime)
        second = cron.get_next(datetime)
    except (ValueError, KeyError) as err:
        raise ValueError(f"{text!r}: not a valid cron expression ({err})") from None
    return int((second - first).total_seconds() * 1000)
