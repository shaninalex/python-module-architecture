from typing import Protocol

from modules.customer.domain.customer import CustomerModel, CustomerCreate, CustomerUpdate


class CustomerPort(Protocol):
    async def get(self, *, customer_id: int):
        ...

    async def create(self, *, payload: CustomerCreate):
        ...

    async def update(self, *, payload: CustomerUpdate):
        ...

    async def get_by_email(self, *, email: str):
        ...