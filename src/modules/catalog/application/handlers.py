from typing import List

from modules.catalog.application.commands import ListProductsCommand, ProductDetailCommand
from modules.catalog.domain.ports import CatalogAdapter
from modules.catalog.domain.product import Product


class ListProductsHandler:

    def __init__(self, catalog: CatalogAdapter):
        self.catalog = catalog

    async def __call__(self, query: ListProductsCommand) -> List[Product]:
        products = await self.catalog.list_products(
            query=query.query,
            offset=query.offset,
            limit=query.limit,
        )
        return products


class ProductDetailHandler:

    def __init__(self, catalog: CatalogAdapter):
        self.catalog = catalog

    async def __call__(self, query: ProductDetailCommand) -> Product | None:
        product = await self.catalog.product_detail(
            product_id=query.product_id
        )

        if product is None:
            return None

        return product
