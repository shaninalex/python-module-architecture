from modules.catalog.application.query import ListProducts
from modules.catalog.domain.ports import Catalog


class ListProductsHandler:

    def __init__(self, catalog: Catalog):
        self.catalog = catalog

    async def __call__(self, query: ListProducts):
        return await self.catalog.list_products(
            query=query.query,
            page=query.page,
            limit=query.limit,
        )