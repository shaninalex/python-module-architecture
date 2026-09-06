from typing import Protocol


class AuthPort(Protocol):

    async def set_last_login(self, *, customer_id: int):
        ...
