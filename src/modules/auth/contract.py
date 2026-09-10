from typing import Protocol


class Credentials(Protocol):
    @property
    def customer_id(self) -> int: ...

    @property
    def password_hash(self) -> str: ...

    @property
    def active(self) -> bool: ...



class CredentialsReader(Protocol):
    async def by_email(self, *, email: str, provider: str) -> Credentials | None: ...