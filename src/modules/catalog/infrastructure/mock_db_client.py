from typing import List

from modules.catalog.domain.product import ProductModel


class MockDBCatalogClient:
    def list_products(self, query: str | None, page: int, limit: int) -> List[ProductModel]:
        return [
            ProductModel(id=1, title="A"),
            ProductModel(id=2, title="b"),
            ProductModel(id=3, title="c"),
            ProductModel(id=4, title="d"),
            ProductModel(id=5, title="e")
        ]