from argon2 import PasswordHasher

from modules.customer.application.commands import CustomerCreateCommand, CustomerGetCommand
from modules.customer.domain.customer import Customer
from modules.customer.domain.ports import CustomerInternalReader, CustomerInternalWriter


class CustomerCreateHandler:

    def __init__(self, catalog: CustomerInternalWriter):
        self.catalog = catalog

    async def __call__(self, cmd: CustomerCreateCommand) -> Customer:
        ph = PasswordHasher()
        _hash = ph.hash(cmd.payload.password)
        cmd.payload.password = _hash
        customer = await self.catalog.create(payload=cmd.payload)
        return customer


class CustomerGetHandler:

    def __init__(self, catalog: CustomerInternalReader):
        self.catalog = catalog

    async def __call__(self, cmd: CustomerGetCommand) -> Customer:
        customer = await self.catalog.get(customer_id=cmd.user_id)
        return customer
