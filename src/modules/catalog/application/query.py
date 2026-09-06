from dataclasses import dataclass


@dataclass(frozen=True)
class ListProductsCommand:
    query: str | None = None
    offset: int = 1
    limit: int = 20


@dataclass(frozen=True)
class ProductDetailCommand:
    product_id: int
