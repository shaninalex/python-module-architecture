from dataclasses import dataclass
from datetime import datetime
from typing import Protocol

from starlette.datastructures import Secret

from blog.core.messages import Command


class Account(Protocol):
    @property
    def user_id(self) -> int: ...

    @property
    def email(self) -> str: ...


@dataclass(frozen=True, slots=True)
class SessionView:
    session_id: str
    user_id: int
    issued_at: datetime
    expires_at: datetime


@dataclass(frozen=True, slots=True)
class RegisterWithPassword(Command[SessionView]):
    email: str
    display_name: str
    password: Secret

    def permission(self) -> str | None:
        return None
