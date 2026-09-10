from sqlalchemy.ext.asyncio import AsyncEngine

from core.command_bus import CommandBus
from modules.catalog.application.handlers import ListProductsHandler, ProductDetailHandler
from modules.catalog.application.commands import ListProductsCommand, ProductDetailCommand
from modules.catalog.infrastructure.repository import CatalogRepository


class CatalogModule:
    def configure(self, container):
        db = container.resolve(AsyncEngine)
        catalog = CatalogRepository(db)
        cmd = container.resolve(CommandBus)

        cmd.register(ListProductsCommand, ListProductsHandler(catalog))
        cmd.register(ProductDetailCommand, ProductDetailHandler(catalog))
