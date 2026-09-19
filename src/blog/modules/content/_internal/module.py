from dataclasses import dataclass

from blog.core.app import App
from blog.modules import content as contract
from blog.modules.content._internal import infra, handlers
from blog.runtime.clock import Clock
from blog.runtime.db.session import SessionProvider


@dataclass(frozen=True, slots=True)
class Deps:
    session: SessionProvider
    clock: Clock
    authors: contract.AuthorNames


class ContentModule:
    def __init__(self, deps: Deps) -> None:
        articles = infra.ArticleRepository(deps.session)
        # self._visibility = infra.VisibilityReader(deps.session)
        self._draft = handlers.DraftArticle(articles, deps.authors, deps.clock)
        # self._edit = handlers.EditArticle(articles, deps.authors, deps.clock)
        self._publish = handlers.PublishArticle(articles, deps.authors, deps.clock)
        # self._hide = handlers.HideArticle(articles, deps.authors, deps.clock)
        # self._get = handlers.GetArticle(articles, deps.authors)
        # self._list = handlers.ListArticles(articles, deps.authors)

    @property
    def name(self) -> str:
        return "content"

    def visibility(self) -> contract.ArticleVisibility:
        return self._visibility

    def register(self, app: App) -> None:
        app.commands.register(contract.DraftArticle, self._draft)
        app.commands.register(contract.EditArticle, self._edit)
        app.commands.register(contract.PublishArticle, self._publish)
        app.commands.register(contract.HideArticle, self._hide)
        app.queries.register(contract.GetArticle, self._get)
        app.queries.register(contract.ListArticles, self._list)


def build(deps: Deps) -> ContentModule:
    return ContentModule(deps)