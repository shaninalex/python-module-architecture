from modules.customer.application.commands import CustomerCreateCommand, CustomerGetCommand, CustomerGetByEmailCommand
from modules.customer.domain.customer import CustomerModel
from modules.customer.domain.ports import CustomerPort


class CustomerCreateHandler:

    def __init__(self, catalog: CustomerPort):
        self.catalog = catalog

    async def __call__(self, cmd: CustomerCreateCommand) -> CustomerModel:
        customer = await self.catalog.create(payload=cmd.payload)
        return customer


class CustomerGetHandler:

    def __init__(self, catalog: CustomerPort):
        self.catalog = catalog

    async def __call__(self, cmd: CustomerGetCommand) -> CustomerModel:
        customer = await self.catalog.get(customer_id=cmd.user_id)
        return customer


class CustomerGetByEmailHandler:

    def __init__(self, catalog: CustomerPort):
        self.catalog = catalog

    async def __call__(self, cmd: CustomerGetByEmailCommand) -> CustomerModel:
        customer = await self.catalog.get_by_email(email=cmd.email)
        return customer
