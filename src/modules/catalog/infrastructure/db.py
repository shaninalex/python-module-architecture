from typing import List

from modules.catalog.domain.product import ProductModel


class DBCatalog:
    def __init__(self, db_client):
        self.db_client = db_client

    async def list_products(self, *, query: str | None, page: int, limit: int) -> List[ProductModel]:
        return self.db_client.list_products(query, page, limit)
