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

The state is kept per condition, as in Scala: pass the condition id as `scope`, so an error already
reported for one condition never silences the same error on another. A condition that is disabled,
removed or replaced has nothing left to report: `forget(scope)` drops its state, and
`retain(scopes)` drops the state of every condition not in force.

    class Schema(ErrorTrackingSchema, BaseSchema): ...

    tracker = ErrorTracker()
    if tracker.should_alert("ledger-api", str(err), track_err=p["track_err"], err_always=p["err_always"], scope=config_id):
        await emit_error_alert(...)
    ...
    tracker.clear("ledger-api")      # the query works again (for every condition)
    tracker.retain(active_ids)       # conditions disabled or removed: their errors are forgotten
"""

from typing import Dict, Hashable, Iterable, Optional, Tuple

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
    Which internal errors become alerts. Keeps the last error per condition (`scope`, the condition
    id; None for a detector without conditions) and source (`key`: an endpoint, a query), so the
    same error alerts once per condition until it clears or changes.
    """

    def __init__(self) -> None:
        self._last: Dict[Tuple[Optional[Hashable], Hashable], str] = {}

    def should_alert(
        self,
        key: Hashable,
        error: str,
        track_err: bool = True,
        err_always: bool = False,
        scope: Optional[Hashable] = None,
    ) -> bool:
        """
        Whether this occurrence of `error` from `key`, for the condition `scope`, should raise an
        alert, and remember it.
        - `track_err` off: never (the error is still remembered, so turning it on later does not
          replay an old error as new).
        - `err_always` on: every time.
        - otherwise: only when it differs from the last error of `key` in this `scope` (or there
          was none). Another scope's errors never count.
        """
        error = str(error)
        repeated = self._last.get((scope, key)) == error
        self._last[(scope, key)] = error
        if not track_err:
            return False
        return err_always or not repeated

    def clear(self, key: Optional[Hashable] = None, scope: Optional[Hashable] = None) -> bool:
        """
        The source works again: its next error alerts as new. `key` alone clears that source in
        every scope; `scope` limits it to one condition; neither clears everything.
        Returns whether an error was pending.
        """
        if key is None and scope is None:
            pending = bool(self._last)
            self._last.clear()
            return pending
        drop = [k for k in self._last if (key is None or k[1] == key) and (scope is None or k[0] == scope)]
        for k in drop:
            del self._last[k]
        return bool(drop)

    def forget(self, scope: Hashable) -> bool:
        """The condition `scope` was disabled, removed or replaced: drop all its errors."""
        return self.clear(scope=scope) if scope is not None else False

    def retain(self, scopes: Iterable[Hashable]) -> bool:
        """
        Keep only the errors of the conditions in `scopes` (the ones in force) and of the detector
        without conditions (scope None). Returns whether anything was dropped.
        """
        keep = set(scopes)
        drop = [k for k in self._last if k[0] is not None and k[0] not in keep]
        for k in drop:
            del self._last[k]
        return bool(drop)

    def last(self, key: Hashable, scope: Optional[Hashable] = None) -> Optional[str]:
        return self._last.get((scope, key))

    def __contains__(self, key: Hashable) -> bool:
        """Whether `key` has a pending error in any scope."""
        return any(k[1] == key for k in self._last)
