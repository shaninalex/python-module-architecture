from typing import List

from databases import Database

from modules.catalog.domain.product import ProductModel


class DBCatalog:
    def __init__(self, db: Database):
        self.db = db

    async def list_products(self, *, query: str | None, page: int, limit: int) -> List[ProductModel]:
        # return self.db_client.list_products(query, page, limit)
        return []