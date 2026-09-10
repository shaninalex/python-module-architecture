from sqlalchemy.ext.asyncio import AsyncEngine

from core.command_bus import CommandBus
from modules.customer.application.commands import CustomerCreateCommand, CustomerGetCommand
from modules.customer.application.handlers import CustomerCreateHandler, CustomerGetHandler
from modules.customer.infrastructure.db import CustomerDB

class CustomerModule:
    def configure(self, container):
        db = container.resolve(AsyncEngine)
        customer_db = CustomerDB(db)
        cmd = container.resolve(CommandBus)

        cmd.register(CustomerCreateCommand, CustomerCreateHandler(customer_db))
        cmd.register(CustomerGetCommand, CustomerGetHandler(customer_db))
