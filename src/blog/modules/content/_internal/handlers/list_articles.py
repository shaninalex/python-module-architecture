from blog.lib import excerpt
from blog.modules.content import _contract as contract
from blog.modules.content._internal.domain.ports import ArticleRepo


class ListArticles:

    def __init__(self, authors: contract.AuthorNames, articles: ArticleRepo):
        self._authors = authors
        self._articles = articles

    async def __call__(self, q: contract.ListArticles) -> contract.ArticlePage:
        articles, total = await self._articles.page(
            tag=q.tag, author_id=q.author_id, offset=q.offset, limit=q.limit
        )

        names = await self._authors.display_names([a.author_id for a in articles])
        return contract.ArticlePage(
            items=tuple(
                contract.ArticleTeaser(
                    id=a.id,
                    slug=a.slug,
                    title=a.title,
                    excerpt=excerpt.first_paragraph(a.body, limit=200),
                    author_name=names.get(a.author_id, ""),
                    published_at=a.published_at,
                )
                for a in articles
            ),
            total=total,
        )