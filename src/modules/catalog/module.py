from bootstrap.container import Container
from core.command_bus import CommandBus
from modules.catalog.application.handlers import ListProductsHandler
from modules.catalog.application.query import ListProducts
from modules.catalog.infrastructure.db import DBCatalog
from modules.catalog.infrastructure.mock_db_client import MockDBCatalogClient
from src.bootstrap.abstract import Module

class CatalogModule(Module):
    def configure(self, container: Container):
        db = MockDBCatalogClient()
        catalog = DBCatalog(db)

        handler = ListProductsHandler(catalog)
        cmd = container.resolve(CommandBus)

        cmd.register(
            ListProducts,
            handler,
        )
