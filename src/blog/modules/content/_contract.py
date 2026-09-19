import enum
from collections.abc import Sequence
from dataclasses import dataclass
from datetime import datetime
from typing import Protocol

from blog.core.messages import Command, Query


class ArticleStatus(enum.Enum):
    DRAFT = "draft"
    PUBLISHED = "published"
    HIDDEN = "hidden"


@dataclass(frozen=True, slots=True)
class ArticleView:
    id: int
    slug: str
    title: str
    body: str
    status: ArticleStatus
    author_id: int
    author_name: str
    published_at: datetime | None


@dataclass(frozen=True, slots=True)
class ArticleTeaser:
    id: int
    slug: str
    title: str
    excerpt: str
    author_name: str
    published_at: datetime | None


@dataclass(frozen=True, slots=True)
class ArticlePage:
    items: tuple[ArticleTeaser, ...]
    total: int


@dataclass(frozen=True, slots=True)
class DraftArticle(Command[ArticleView]):
    title: str
    body: str

    def permission(self) -> str | None:
        return "article.draft"


@dataclass(frozen=True, slots=True)
class EditArticle(Command[ArticleView]):
    article_id: int
    title: str
    body: str

    def permission(self) -> str | None:
        return "article.draft"


@dataclass(frozen=True, slots=True)
class PublishArticle(Command[ArticleView]):
    article_id: int

    def permission(self) -> str | None:
        return "article.publish"


@dataclass(frozen=True, slots=True)
class HideArticle(Command[ArticleView]):
    article_id: int

    def permission(self) -> str | None:
        return "article.publish"


@dataclass(frozen=True, slots=True)
class GetArticle(Query[ArticleView]):
    slug: str

    def permission(self) -> str | None:
        return None


@dataclass(frozen=True, slots=True)
class ListArticles(Query[ArticlePage]):
    tag: str | None
    author_id: int | None
    offset: int
    limit: int

    def permission(self) -> str | None:
        return None


@dataclass(frozen=True, slots=True)
class ArticlePublished:
    article_id: int
    slug: str
    author_id: int
    published_at: datetime

    @property
    def event_name(self) -> str:
        return "content.article_published"


# implemented at _internal/infra/readers.py.
class ArticleVisibility(Protocol):
    async def is_visible(self, article_id: int) -> bool: ...


class AuthorNames(Protocol):
    async def display_names(self, ids: Sequence[int]) -> dict[int, str]: ...
