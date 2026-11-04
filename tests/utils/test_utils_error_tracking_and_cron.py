from datetime import datetime, timedelta, timezone

import pytest

from sentinel.manifest import BaseSchema
from sentinel.utils.cron import CronSchema, _quartz_weekdays, cron_interval_ms
from sentinel.utils.error_tracking import ErrorTracker, ErrorTrackingSchema

# ------------------------------------------------------------------ error tracking


def test_the_same_error_alerts_once_until_it_clears():
    tracker = ErrorTracker()
    assert tracker.should_alert("api", "connection refused") is True
    assert tracker.should_alert("api", "connection refused") is False
    assert tracker.should_alert("api", "connection refused") is False
    assert tracker.clear("api") is True
    assert tracker.should_alert("api", "connection refused") is True


def test_a_different_error_alerts():
    tracker = ErrorTracker()
    assert tracker.should_alert("api", "connection refused") is True
    assert tracker.should_alert("api", "timeout") is True
    assert tracker.should_alert("api", "connection refused") is True


def test_always_alerts_on_every_repeat():
    tracker = ErrorTracker()
    assert all(tracker.should_alert("api", "down", err_always=True) for _ in range(3))


def test_track_err_off_never_alerts_and_does_not_replay_later():
    tracker = ErrorTracker()
    assert tracker.should_alert("api", "down", track_err=False) is False
    assert tracker.should_alert("api", "down", track_err=False, err_always=True) is False
    # turned on while the same error is still there: it was already known, no alert
    assert tracker.should_alert("api", "down", track_err=True) is False


def test_sources_are_tracked_apart():
    tracker = ErrorTracker()
    assert tracker.should_alert("api", "down") is True
    assert tracker.should_alert("db", "down") is True
    assert tracker.should_alert("api", "down", scope=7) is True
    assert "api" in tracker and tracker.last("api") == "down"
    assert tracker.clear("nothing") is False
    assert tracker.clear() is True
    assert tracker.should_alert("api", "down") is True


def test_an_error_reported_for_one_condition_does_not_silence_another():
    tracker = ErrorTracker()
    assert tracker.should_alert("ledger-api", "HTTP 401", scope=28079) is True
    assert tracker.should_alert("ledger-api", "HTTP 401", scope=28079) is False
    # a new condition with the same failure is a new alert
    assert tracker.should_alert("ledger-api", "HTTP 401", scope=28081) is True
    assert tracker.should_alert("ledger-api", "HTTP 401", scope=28081) is False
    assert tracker.last("ledger-api", scope=28079) == "HTTP 401"
    assert tracker.last("ledger-api") is None  # the detector without conditions has its own state


def test_clear_by_key_reaches_every_condition_and_by_scope_only_one():
    tracker = ErrorTracker()
    tracker.should_alert("api", "down", scope=1)
    tracker.should_alert("api", "down", scope=2)
    tracker.should_alert("db", "down", scope=2)
    assert tracker.clear("api", scope=1) is True
    assert tracker.should_alert("api", "down", scope=1) is True
    assert tracker.should_alert("api", "down", scope=2) is False
    assert tracker.clear("api") is True  # the source works again, for every condition
    assert tracker.should_alert("api", "down", scope=1) is True
    assert tracker.should_alert("api", "down", scope=2) is True
    assert "db" in tracker


def test_a_disabled_or_removed_condition_loses_its_errors():
    tracker = ErrorTracker()
    tracker.should_alert("api", "down", scope=1)
    tracker.should_alert("api", "down", scope=2)
    tracker.should_alert("api", "down")  # no condition
    assert tracker.forget(1) is True
    assert tracker.forget(1) is False
    assert tracker.forget(None) is False
    assert tracker.should_alert("api", "down", scope=1) is True  # back later: alerts as new
    # only condition 2 is still in force
    assert tracker.retain([2]) is True
    assert tracker.last("api", scope=1) is None
    assert tracker.last("api", scope=2) == "down"
    assert tracker.last("api") == "down"
    assert tracker.retain([2]) is False


def test_the_schema_fields_carry_the_scala_names():
    class Schema(ErrorTrackingSchema, BaseSchema):
        pass

    schema = Schema().model_json_schema()["properties"]
    assert schema["track_err"]["default"] is True
    assert schema["err_always"]["default"] is False
    assert schema["track_err"]["title"] == "Track Errors"
    assert schema["err_always"]["title"] == "Track Errors (always)"
    assert "severity" in schema


@pytest.mark.parametrize("scopes", ["cfg-1", b"cfg-1"])
def test_retain_refuses_a_single_string(scopes):
    tracker = ErrorTracker()
    tracker.should_alert("api", "down", scope="cfg-1")
    with pytest.raises(TypeError):
        tracker.retain(scopes)
    assert not tracker.should_alert("api", "down", scope="cfg-1")


# ------------------------------------------------------------------ cron


@pytest.mark.parametrize(
    "text, ms",
    [
        ("1h", 3_600_000),
        ("1 hour", 3_600_000),
        ("2 hours", 7_200_000),
        ("10 min", 600_000),
        ("10min", 600_000),
        ("90s", 90_000),
        ("1d", 86_400_000),
        ("2 days", 172_800_000),
        ("60000", 60_000),
        ("1000 ms", 1_000),
        ("0 * * * *", 3_600_000),
        ("*/5 * * * *", 300_000),
        ("0 0 * * * ?", 3_600_000),  # Quartz, seconds first
        ("0 0/10 * * * ? *", 600_000),  # Quartz with a year
        ("0 0 * * *", 86_400_000),
    ],
)
def test_cron_interval(text, ms):
    assert cron_interval_ms(text, now=datetime(2026, 10, 30, 12, 0, tzinfo=timezone.utc)) == ms


@pytest.mark.parametrize("text", ["", "  ", "1 week", "0h", "every hour", "* * *", "61 * * * *", None])
def test_invalid_cron_is_refused(text):
    with pytest.raises(ValueError):
        cron_interval_ms(text)


DAY = 86_400_000
MONDAY = datetime(2026, 11, 2, 12, 0, tzinfo=timezone.utc)


def test_quartz_seconds_count():
    assert cron_interval_ms("0/30 * * * * ?") == 30_000
    assert cron_interval_ms("*/10 * * * * ? *") == 10_000
    assert cron_interval_ms("0 0/5 * * * ?") == 300_000


@pytest.mark.parametrize(
    "text",
    [
        "abc 0 * * * ?",  # seconds
        "60 0 * * * ?",
        "0 0 0 * * ? abc",  # year
        "0 0 0 * * ? ?",
        "? 0 0 * * ?",  # "?" is only for the day fields
        "0 ? * * *",
        "0 0 0 30 2 ?",  # a date that never comes
    ],
)
def test_invalid_quartz_fields_are_refused(text):
    with pytest.raises(ValueError):
        cron_interval_ms(text)


@pytest.mark.parametrize(
    "text", ["0 0 0 * * ? 2030", "0 0 0 * * ? 2026-2030", "0 0 0 * * ? 2026,2028", "0 0 0 * * ? */2"]
)
def test_a_quartz_year_does_not_change_the_window(text):
    assert cron_interval_ms(text) == DAY


@pytest.mark.parametrize("text", ["1M", "1 M", "10M"])
def test_a_capital_m_is_refused(text):
    with pytest.raises(ValueError, match="unknown unit 'M'"):
        cron_interval_ms(text)


@pytest.mark.parametrize("text, ms", [("1 Min", 60_000), ("1m", 60_000), ("1H", 3_600_000), ("1 Hour", 3_600_000)])
def test_other_units_still_ignore_case(text, ms):
    assert cron_interval_ms(text) == ms


@pytest.mark.parametrize(
    "text, ms",
    [
        ("0 0 0 ? * MON-FRI", DAY),  # Friday to Monday is three days, the shortest gap is one
        ("0 0 * * 1-5", DAY),
        ("0 0 0 ? * MON,THU", 3 * DAY),  # Thursday to Monday is four
        ("0 0 8,12 * * ?", 4 * 3_600_000),  # uneven hours
        ("0 0 * * 0", 7 * DAY),  # once a week
        ("0 0 1 * *", 28 * DAY),  # less often than a week: the first gap from the fixed week
        ("0 0 1 1 *", 365 * DAY),
    ],
)
def test_the_window_of_an_irregular_cron_is_the_shortest_gap(text, ms):
    assert cron_interval_ms(text) == ms


@pytest.mark.parametrize("text", ["0 0 0 ? * MON-FRI", "0 0 0 ? * 2-6", "0 0 1 * *", "0 0 8,12 * * ?"])
def test_the_window_does_not_depend_on_the_start(text):
    windows = {cron_interval_ms(text, MONDAY + timedelta(days=i, hours=i)) for i in range(40)}
    assert len(windows) == 1


def test_the_shortest_gap_of_a_schedule_with_seconds_comes_fast():
    assert cron_interval_ms("* * * * * ?") == 1_000


@pytest.mark.parametrize(
    "field, expected",
    [
        ("1", "0"),  # SUN
        ("7", "6"),  # SAT
        ("2-6", "1-5"),
        ("1,4,7", "0,3,6"),
        ("7-1", "6-0"),
        ("1/2", "0/2"),  # the step is not a day
        ("2-6/2", "1-5/2"),
        ("6#3", "5#3"),  # nor the position in the month
        ("MON-FRI", "MON-FRI"),
        ("*", "*"),
    ],
)
def test_quartz_day_numbers_become_croniter_numbers(field, expected):
    assert _quartz_weekdays(field) == expected


def test_quartz_counts_days_from_one_and_unix_from_zero():
    assert cron_interval_ms("0 0 0 ? * 2-6") == cron_interval_ms("0 0 0 ? * MON-FRI")
    assert cron_interval_ms("0 0 0 ? * 7") == 7 * DAY  # SAT, a day number croniter's own form refuses
    assert cron_interval_ms("0 0 * * 0") == 7 * DAY  # SUN in the 5-field form
    for bad in ("0 0 0 ? * 0", "0 0 0 ? * 8"):
        with pytest.raises(ValueError, match="Quartz days"):
            cron_interval_ms(bad)


def test_cron_schema_default():
    assert CronSchema().cron == "1h"
