from modules.customer.application.commands import CustomerCreateCommand
from modules.customer.domain.customer import CustomerModel
from modules.customer.domain.ports import CustomerPort


class CustomerCreateHandler:

    def __init__(self, catalog: CustomerPort):
        self.catalog = catalog

    async def __call__(self, cmd: CustomerCreateCommand) -> CustomerModel:
        customer = await self.catalog.create(payload=cmd.payload)
        return customer