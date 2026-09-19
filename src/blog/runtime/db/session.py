from collections.abc import Callable
from contextlib import asynccontextmanager
from contextvars import ContextVar

from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker

type SessionProvider = Callable[[], AsyncSession]

_session: ContextVar[AsyncSession | None] = ContextVar("session", default=None)


class Database:
    def __init__(self, engine: AsyncEngine) -> None:
        self._engine = engine
        self._factory = async_sessionmaker(engine, expire_on_commit=False)

    def session(self) -> AsyncSession:
        current = _session.get()
        if current is None:
            raise RuntimeError("db: no active session — виклик поза транзакцією застосунку")
        return current

    @asynccontextmanager
    async def transaction(self):
        if _session.get() is not None:
            raise RuntimeError("db: nested transaction")
        async with self._factory() as session, session.begin():
            token = _session.set(session)
            try:
                yield session
            finally:
                _session.reset(token)

    @asynccontextmanager
    async def read_only(self):
        existing = _session.get()
        if existing is not None:
            yield existing
            return
        async with self._factory() as session:
            token = _session.set(session)
            try:
                yield session
            finally:
                _session.reset(token)

    async def dispose(self) -> None:
        await self._engine.dispose()