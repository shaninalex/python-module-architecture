from dataclasses import dataclass


@dataclass(frozen=True)
class ListProductsCommand:
    query: str | None = None
    offset: int = 1
    limit: int = 20
