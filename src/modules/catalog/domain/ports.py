from typing import Protocol, List

from modules.catalog.infrastructure.schema import Product


class CatalogPort(Protocol):

    async def list_products(self, *, query: str | None, offset: int, limit: int) -> List[Product]:
        ...

    async def product_detail(self, *, product_id: int) -> Product:
        ...
