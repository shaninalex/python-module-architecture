from typing import List

from sqlalchemy import select, or_
from sqlalchemy.ext.asyncio import AsyncSession, AsyncEngine
from sqlalchemy.orm import selectinload

from modules.catalog.domain.product import Product
from modules.catalog.infrastructure.schema import ProductORM


class CatalogRepository:
    def __init__(self, db: AsyncEngine):
        self.db = db

    async def list_products(self, *, query: str | None, offset: int, limit: int) -> List[Product]:
        async with AsyncSession(self.db) as session:
            stmt = (
                select(ProductORM)
                .options(selectinload(ProductORM.variants))
                .limit(limit)
                .offset(offset)
            )
            if query is not None:
                stmt = stmt.filter(
                    or_(
                        ProductORM.title.contains(query),
                        ProductORM.description.contains(query),
                        ProductORM.short_description.contains(query),
                    )
                )

            result = await session.scalars(stmt)
            products = result.all()
            return [p.to_model() for p in products]

    async def product_detail(self, *, product_id: int) -> Product | None:
        async with AsyncSession(self.db) as session:
            stmt = (
                select(ProductORM)
                .options(selectinload(ProductORM.variants))
                .where(ProductORM.id==product_id)
            )
            result = await session.scalar(stmt)
            if result is None:
                return None

            return result.to_model()
