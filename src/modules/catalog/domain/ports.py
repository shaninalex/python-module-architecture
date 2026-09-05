from typing import Protocol, List

from modules.catalog.domain.product import ProductModel


class Catalog(Protocol):

    async def list_products(self, *, query: str | None, page: int, limit: int) -> List[ProductModel]:
        ...
