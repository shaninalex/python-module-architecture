from blog.core.actor import current_actor
from blog.core.errors import forbidden
from blog.modules import content as contract
from blog.modules.content._internal.domain import errors, ports
from blog.runtime import outbox
from blog.runtime.clock import Clock


class PublishArticle:
    def __init__(
            self,
            articles: ports.ArticleRepo,
            authors: contract.AuthorNames,
            clock: Clock,
    ) -> None:
        self._articles = articles
        self._authors = authors
        self._clock = clock

    async def __call__(self, cmd: contract.PublishArticle) -> contract.ArticleView:
        article = await self._articles.by_id(cmd.article_id)
        if article is None:
            raise errors.NO_SUCH_ARTICLE

        actor = current_actor()
        if article.author_id != actor.user_id and "editor" not in actor.roles:
            raise forbidden("content.not_your_article", "You can only publish your own articles.")

        published = await self._articles.save(article.publish(now=self._clock.now()))

        await outbox.record(contract.ArticlePublished(
            article_id=published.id,
            slug=published.slug,
            author_id=published.author_id,
            published_at=published.published_at,
        ))

        names = await self._authors.display_names([published.author_id])
        return contract.ArticleView(
            id=published.id,
            slug=published.slug,
            title=published.title,
            body=published.body,
            status=published.status,
            author_id=published.author_id,
            author_name=names.get(published.author_id, ""),
            published_at=published.published_at,
        )
