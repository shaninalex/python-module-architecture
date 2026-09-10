from datetime import datetime
from dataclasses import dataclass
from typing import Protocol


@dataclass(frozen=True, slots=True)
class LoginCredentials:
    customer_id: int
    password_hash: str
    active: bool
    last_login_at: datetime | None = None


class CredentialsReader(Protocol):
    async def by_email(self, *, email: str, provider: str) -> LoginCredentials | None: ...