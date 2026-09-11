from datetime import datetime

from typing import Protocol


class Hasher(Protocol):
    def hash(self, plain: str) -> str: ...

    def verify(self, hashed: str, plain: str) -> bool: ...

    def needs_rehash(self, hashed: str) -> bool: ...


class LoginLog(Protocol):
    async def record(self, *, customer_id: int, at: datetime) -> None: ...
