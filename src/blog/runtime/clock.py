from datetime import datetime, timedelta, timezone
from typing import Any, Protocol, runtime_checkable


@runtime_checkable
class Clock(Protocol):

    def now(self) -> datetime:
        ...


class SystemClock:

    def now(self) -> datetime:
        return datetime.now(timezone.utc)


class MockClock:

    def __init__(self, initial_time: datetime | None = None) -> None:
        self._now = initial_time or datetime.now(timezone.utc)

    def now(self) -> datetime:
        return self._now

    def set_time(self, new_time: datetime) -> None:
        self._now = new_time

    def advance(self, delta: timedelta | None = None, **delta_kwargs: Any) -> None:
        if delta is not None:
            self._now += delta
        if delta_kwargs:
            self._now += timedelta(**delta_kwargs)
