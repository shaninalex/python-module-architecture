from typing import Protocol


class Account(Protocol):
    @property
    def user_id(self) -> int: ...

    @property
    def email(self) -> str: ...
