from sqlalchemy import select, or_
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
            if query is not None:
                stmt = stmt.filter(
                    or_(
                        Product.title.contains(query),
                        Product.description.contains(query),
                        Product.short_description.contains(query),
                    )
                )

            result = await session.scalars(stmt)
            products = result.all()
            return products

    async def product_detail(self, *, product_id: int):
        async with AsyncSession(self.db) as session:
            stmt = (
                select(Product)
                .options(selectinload(Product.variants))
                .where(Product.id==product_id)
            )
            result = await session.scalar(stmt)
            return result
