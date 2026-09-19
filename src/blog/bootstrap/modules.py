from logging import Logger

from blog.core.app import Module
from blog.modules.content import module as content
from blog.modules.accounts import module as accounts
from blog.runtime.clock import Clock
from blog.runtime.config import Config
from blog.runtime.db.session import Database


def build_modules(
        cfg: Config, db: Database, clock: Clock, logger: Logger
) -> tuple[Module, ...]:
    accounts_mod = accounts.build(accounts.Deps(
        session=db.session,
        clock=clock,
    ))

    content_mod = content.build(content.Deps(
        session=db.session,
        clock=clock,
        authors=accounts_mod.display_names(),
    ))

    return accounts_mod, content_mod
