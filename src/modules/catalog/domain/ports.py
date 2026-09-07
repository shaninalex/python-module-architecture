from typing import Protocol, List

from modules.catalog.domain.product import Product


class CatalogAdapter(Protocol):

    async def list_products(self, *, query: str | None, offset: int, limit: int) -> List[Product]:
        ...

    async def product_detail(self, *, product_id: int) -> Product | None:
        ...
