from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession, AsyncEngine

from modules.catalog.infrastructure.schema import Product


class DBCatalog:
    def __init__(self, db: AsyncEngine):
        self.db = db

    async def list_products(self, *, query: str | None, offset: int, limit: int):
        async with AsyncSession(self.db) as session:
            stmt = select(Product).limit(limit).offset(offset)
            products = await session.scalars(stmt)
            return products
