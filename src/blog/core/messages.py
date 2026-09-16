from typing import Protocol


class Command[R]: ...


class Query[R]: ...


class Event(Protocol):
    @property
    def event_name(self) -> str: ...


class Permissioned(Protocol):
    def permission(self) -> str | None: ...
