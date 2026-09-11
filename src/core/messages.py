from typing import Protocol


class Command[R]:
    """Command marker (record). R — result type."""


class Query[R]:
    """Request marker (read). Dedicated bus: no write transaction."""


class Event(Protocol):
    @property
    def event_name(self) -> str: ...


class Permissioned(Protocol):
    def permission(self) -> tuple[str, int] | None:
        """(action, scope) or None for an explicitly public operation."""