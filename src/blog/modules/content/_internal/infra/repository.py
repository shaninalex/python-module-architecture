from collections.abc import Sequence
from sqlalchemy import func, select

from blog.modules.content._internal.domain import article as domain
from blog.modules.content._internal.infra import mappers, records
from blog.runtime.db.session import SessionProvider


class ArticleRepository:
    """
    Implements article repository.:
    blog.modules.content._internal.domain.ports.ArticleRepo
    """

    def __init__(self, session: SessionProvider) -> None:
        self._session = session

    async def by_slug(self, slug: str) -> domain.Article | None:
        stmt = select(records.ArticleRecord).where(records.ArticleRecord.slug == slug)
        row = await self._session().scalar(stmt)
        return mappers.to_domain(row) if row is not None else None

    async def page(
            self, *, tag: str | None, author_id: int | None, offset: int, limit: int
    ) -> tuple[Sequence[domain.Article], int]:
        stmt = select(records.ArticleRecord)
        if author_id is not None:
            stmt = stmt.where(records.ArticleRecord.author_id == author_id)
        # if tag is not None:
        #     stmt = stmt.join(records.ArticleTagRecord).where(...)
        total = await self._session().scalar(
            select(func.count()).select_from(stmt.subquery())
        )
        rows = await self._session().scalars(
            stmt.order_by(records.ArticleRecord.published_at.desc())
            .offset(offset).limit(limit)
        )
        return [mappers.to_domain(r) for r in rows], total or 0
