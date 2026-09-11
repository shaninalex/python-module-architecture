from dataclasses import dataclass
from datetime import datetime
from typing import Protocol, Literal

from core.messages import Command
from core.secret import Secret


@dataclass(frozen=True, slots=True)
class SessionView:
    customer_id: int
    issued_at: datetime


@dataclass(frozen=True, slots=True)
class AuthenticateByEmail(Command[SessionView]):
    email: str
    password: Secret

    def permission(self) -> tuple[str, int] | None:
        return None


class Credentials(Protocol):
    @property
    def customer_id(self) -> int: ...

    @property
    def password_hash(self) -> str: ...

    @property
    def active(self) -> bool: ...


Provider = Literal["email", "google", "github"]


class CredentialsReader(Protocol):
    async def by_email(self, *, email: str, provider: Provider) -> Credentials | None: ...
