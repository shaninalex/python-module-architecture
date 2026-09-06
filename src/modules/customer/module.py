from sqlalchemy.ext.asyncio import AsyncEngine

from bootstrap.abstract import Module
from bootstrap.container import Container
from core.command_bus import CommandBus
from modules.customer.application.commands import CustomerCreateCommand, CustomerGetCommand, CustomerGetByEmailCommand
from modules.customer.application.handlers import CustomerCreateHandler, CustomerGetHandler, CustomerGetByEmailHandler
from modules.customer.infrastructure.db import CustomerDB


class CustomerModule(Module):
    def configure(self, container: Container):
        db = container.resolve(AsyncEngine)
        customer_db = CustomerDB(db)
        cmd = container.resolve(CommandBus)

        cmd.register(CustomerCreateCommand, CustomerCreateHandler(customer_db))
        cmd.register(CustomerGetCommand, CustomerGetHandler(customer_db))
        cmd.register(CustomerGetByEmailCommand, CustomerGetByEmailHandler(customer_db))
