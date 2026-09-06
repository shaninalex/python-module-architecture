from dataclasses import dataclass
from typing import Protocol


@dataclass
class AuthCredentials:
    customer_id: int
    password_hash: str
    active: bool


class AuthCredentialsReaderPort(Protocol):
    async def get_login_credentials(self, *, email: str, credentials_type: str = "email") -> AuthCredentials | None:
        ...
