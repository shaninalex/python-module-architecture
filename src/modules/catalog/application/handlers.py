from typing import List

from modules.catalog.application.query import ListProductsCommand, ProductDetailCommand
from modules.catalog.domain.ports import Catalog
from modules.catalog.domain.product import ProductModel


class ListProductsHandler:

    def __init__(self, catalog: Catalog):
        self.catalog = catalog

    async def __call__(self, query: ListProductsCommand) -> List[ProductModel]:
        db_products = await self.catalog.list_products(
            query=query.query,
            offset=query.offset,
            limit=query.limit,
        )
        return [d.to_model() for d in db_products]


class ProductDetailHandler:

    def __init__(self, catalog: Catalog):
        self.catalog = catalog

    async def __call__(self, query: ProductDetailCommand) -> ProductModel:
        product = await self.catalog.product_detail(
            product_id=query.product_id
        )
        return product.to_model()
