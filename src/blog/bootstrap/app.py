import logging
from dataclasses import dataclass
from logging import Logger

from sqlalchemy.ext.asyncio import create_async_engine

from blog.bootstrap.modules import build_modules
from blog.core.app import App, Module
from blog.core.bus import EventBus, QueryBus, CommandBus
from blog.runtime.clock import Clock, SystemClock
from blog.runtime.config import Config
from blog.runtime.db.session import Database
from blog.runtime.permissions import Guard


@dataclass(frozen=True, slots=True)
class Application:
    core: App
    db: Database
    config: Config
    clock: Clock
    logger: Logger
    modules: tuple[Module, ...]

    async def aclose(self) -> None:
        await self.db.dispose()


async def build_app(cfg: Config) -> Application:
    logger = logging.getLogger(__name__)  # make our own logger
    clock = SystemClock()
    db_url = cfg.database.url.reveal()
    # Ensure async driver (asyncpg) is used for PostgreSQL connections
    if db_url.startswith("postgresql://"):
        db_url = db_url.replace("postgresql://", "postgresql+asyncpg://", 1)

    _engine = create_async_engine(url=db_url, echo=cfg.database.echo)
    db = Database(_engine)

    guard = Guard()
    write = ()
    read = ()

    core = App(
        commands=CommandBus(*write),
        queries=QueryBus(*read),
        events=EventBus(logger),
    )

    modules = build_modules(cfg, db, clock, logger)
    failures: list[Exception] = []
    for module in modules:
        try:
            module.register(core)
        except Exception as exc:
            failures.append(RuntimeError(f"register module {module.name}: {exc}"))
    if failures:
        raise ExceptionGroup("module registration failed", failures)

    core.commands.seal()
    core.queries.seal()

    return Application(
        core=core,
        db=db,
        config=cfg,
        clock=clock,
        logger=logger,
        modules=modules
    )
