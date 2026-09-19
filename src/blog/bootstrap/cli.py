import asyncio
from collections.abc import AsyncIterator, Callable, Coroutine
from contextlib import asynccontextmanager
from functools import wraps
from pathlib import Path
from typing import Any, ParamSpec, TypeVar

from blog.bootstrap.app import Application, build_app
from blog.core.actor import Actor, acting_as
from blog.core.errors import AppError
from blog.runtime.config import config_path, load

P: ParamSpec = ParamSpec("P")
R: TypeVar = TypeVar("R")


@asynccontextmanager
async def cli_session(cfg_path: str | Path | None = None) -> AsyncIterator[Application]:
    cfg = load(config_path(cfg_path))
    app = await build_app(cfg)
    try:
        with acting_as(Actor.system()):
            yield app
    finally:
        await app.aclose()


def async_cli_command(fn: Callable[..., Coroutine[Any, Any, int | None]]) -> Callable[..., int]:
    @wraps(fn)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> int:
        import click

        ctx = click.get_current_context()
        cfg_file = ctx.obj.get("config_path") if ctx.obj else None

        async def _runner() -> int:
            try:
                async with cli_session(cfg_file) as app:
                    res = await fn(app, *args, **kwargs)
                    return res if res is not None else 0
            except AppError as exc:
                click.secho(f"Error [{exc.code}]: {exc.message}", fg="red", err=True)
                return 1

        return asyncio.run(_runner())

    return wrapper
