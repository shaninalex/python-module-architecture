from typing import Protocol, List

from modules.catalog.domain.product import ProductModel


class Catalog(Protocol):

    async def list_products(self, *, query: str | None, offset: int, limit: int) -> List[ProductModel]:
        ...

    async def product_detail(self, *, product_id: int) -> ProductModel:
        ...
