"""
Error alerts: "Track Errors" and "Track Errors (always)"

A detector that fails on its own (an endpoint is down, a contract call or a query fails) can say so
with an alert instead of only a log line. Two form fields decide it, with the names and meaning the
Scala detectors use, so a client sees the same two checkboxes on every detector:

- `track_err` (Track Errors): raise an alert when the detector hits an internal error.
- `err_always` (Track Errors (always)): raise a new alert every time the error repeats. Without
  it, an error alerts once and its repeats are skipped until it clears, so a service that stays
  down for a day is one alert, not one per check.

An error "clears" when the detector reports that the operation works again (`ErrorTracker.clear`),
or when a different error takes its place. The Scala SDK keeps only the last error text per
condition and never clears it on success; clearing on recovery lets the same error alert again
the next time it happens, after things were fine in between.

    class Schema(ErrorTrackingSchema, BaseSchema): ...

    tracker = ErrorTracker()
    if tracker.should_alert("ledger-api", str(err), track_err=p["track_err"], err_always=p["err_always"]):
        await emit_error_alert(...)
    ...
    tracker.clear("ledger-api")   # the query works again
"""

from typing import Dict, Hashable, Optional

from pydantic import BaseModel, Field


class ErrorTrackingSchema(BaseModel):
    """The two error fields, to mix into a detector's schema."""

    track_err: bool = Field(
        default=True,
        title="Track Errors",
        description=(
            "Raise an alert when the detector itself fails, for example when an endpoint it reads "
            "is down or a call fails"
        ),
    )
    err_always: bool = Field(
        default=False,
        title="Track Errors (always)",
        description=(
            "Raise a new alert every time the same error repeats. Off: the error alerts once and "
            "its repeats are skipped until it clears"
        ),
    )


class ErrorTracker:
    """
    Which internal errors become alerts. Keeps the last error per source (`key`: an endpoint, a
    query, a condition id), so the same error alerts once until it clears or changes.
    """

    def __init__(self) -> None:
        self._last: Dict[Hashable, str] = {}

    def should_alert(
        self,
        key: Hashable,
        error: str,
        track_err: bool = True,
        err_always: bool = False,
    ) -> bool:
        """
        Whether this occurrence of `error` from `key` should raise an alert, and remember it.
        - `track_err` off: never (the error is still remembered, so turning it on later does not
          replay an old error as new).
        - `err_always` on: every time.
        - otherwise: only when it differs from the last error of `key` (or there was none).
        """
        error = str(error)
        repeated = self._last.get(key) == error
        self._last[key] = error
        if not track_err:
            return False
        return err_always or not repeated

    def clear(self, key: Optional[Hashable] = None) -> bool:
        """The source works again: its next error alerts as new. No key clears every source.
        Returns whether an error was pending."""
        if key is None:
            pending = bool(self._last)
            self._last.clear()
            return pending
        return self._last.pop(key, None) is not None

    def last(self, key: Hashable) -> Optional[str]:
        return self._last.get(key)

    def __contains__(self, key: Hashable) -> bool:
        return key in self._last
