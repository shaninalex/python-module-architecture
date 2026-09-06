from typing import Protocol

from modules.customer.domain.customer import CustomerCreate, CustomerUpdate


class CustomerInternalReader(Protocol):
    async def get(self, *, customer_id: int):
        ...

    async def get_by_email(self, *, email: str):
        ...


class CustomerInternalWriter(Protocol):

    async def create(self, *, payload: CustomerCreate):
        ...

    async def update(self, *, payload: CustomerUpdate):
        ...
