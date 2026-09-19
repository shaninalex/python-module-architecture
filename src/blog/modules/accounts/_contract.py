from dataclasses import dataclass
from datetime import datetime
from typing import Protocol, Sequence


@dataclass(frozen=True, slots=True)
class AccountRef:
    user_id: int
    email: str
    display_name: str
    created_at: datetime


class Directory(Protocol):

    async def by_email(self, email: str) -> AccountRef | None: ...

    async def create(self, *, email: str, display_name: str) -> AccountRef: ...


class DisplayNames(Protocol):
    async def display_names(self, ids: Sequence[int]) -> dict[int, str]: ...
