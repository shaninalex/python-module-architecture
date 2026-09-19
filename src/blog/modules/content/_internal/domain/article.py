from dataclasses import dataclass, replace
from datetime import datetime

from blog.lib import slugs
from blog.modules.content._contract import ArticleStatus
from blog.modules.content._internal.domain import errors


@dataclass(frozen=True, slots=True)
class Article:
    id: int | None
    slug: str
    title: str
    body: str
    author_id: int
    status: ArticleStatus
    created_at: datetime
    published_at: datetime | None = None
    updated_at: datetime | None = None

    @classmethod
    def draft(cls, title: str, body: str, author_id: int, now: datetime) -> "Article":
        title = title.strip()
        if not title:
            raise errors.EMPTY_TITLE
        return Article(
            id=None,
            slug=slugs.slugify(title),
            title=title,
            body=body,
            author_id=author_id,
            status=ArticleStatus.DRAFT,
            created_at=now,
        )

    def publish(self, now: datetime) -> "Article":
        if self.status == ArticleStatus.PUBLISHED:
            raise errors.ALREADY_PUBLISHED
        if not self.body.strip():
            raise errors.EMPTY_BODY
        return replace(
            self,
            status=ArticleStatus.PUBLISHED,
            published_at=self.published_at or now,
            updated_at=now,
        )

    def hide(self, now: datetime) -> "Article":
        if self.status is not ArticleStatus.PUBLISHED:
            raise errors.NOT_PUBLISHED
        return replace(self, status=ArticleStatus.HIDDEN, updated_at=now)

    def visible_to(self, *, user_id: int | None, is_editor: bool) -> bool:
        if self.status is ArticleStatus.PUBLISHED:
            return True
        return is_editor or (user_id is not None and user_id == self.author_id)