from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession, AsyncEngine
from sqlalchemy.orm import selectinload

from modules.catalog.infrastructure.schema import Product


class DBCatalog:
    def __init__(self, db: AsyncEngine):
        self.db = db

    async def list_products(self, *, query: str | None, offset: int, limit: int):
        async with AsyncSession(self.db) as session:
            stmt = (
                select(Product)
                .options(selectinload(Product.variants))
                .limit(limit)
                .offset(offset)
            )
            result = await session.scalars(stmt)
            products = result.all()
            return products
