from blog.modules.content import ArticleStatus
from blog.modules.content._internal.domain import article
from blog.modules.content._internal.infra import records


def to_domain(a: records.ArticleRecord) -> article.Article:
    return article.Article(
        id=a.id,
        slug=a.slug,
        title=a.title,
        body=a.body,
        author_id=a.author_id,
        status=ArticleStatus(a.status),
        created_at=a.created_at,
        published_at=a.published_at,
        updated_at=a.updated_at,
    )