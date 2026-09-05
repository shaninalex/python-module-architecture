from dataclasses import dataclass


@dataclass(frozen=True)
class ListProducts:
    query: str | None = None
    page: int = 1
    limit: int = 20
