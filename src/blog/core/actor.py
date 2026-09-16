from contextlib import contextmanager
from contextvars import ContextVar
from dataclasses import dataclass, field


@dataclass(frozen=True, slots=True)
class Actor:
    user_id: int | None = None
    roles: frozenset[str] = field(default_factory=frozenset)
    is_system: bool = False

    @classmethod
    def system(cls) -> "Actor":
        return cls(is_system=True)

    @classmethod
    def anonymous(cls) -> "Actor":
        return cls()


_current: ContextVar[Actor] = ContextVar("actor", default=Actor.anonymous())


def current_actor() -> Actor:
    return _current.get()


@contextmanager
def acting_as(actor: Actor):
    token = _current.set(actor)
    try:
        yield
    finally:
        _current.reset(token)
