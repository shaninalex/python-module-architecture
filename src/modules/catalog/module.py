from databases import Database

from bootstrap.container import Container
from core.command_bus import CommandBus
from modules.catalog.application.handlers import ListProductsHandler
from modules.catalog.application.query import ListProductsCommand
from modules.catalog.infrastructure.db import DBCatalog
from src.bootstrap.abstract import Module

class CatalogModule(Module):
    def configure(self, container: Container):
        db = container.resolve(Database)

        catalog = DBCatalog(db)

        handler = ListProductsHandler(catalog)
        cmd = container.resolve(CommandBus)

        cmd.register(
            ListProductsCommand,
            handler,
        )
