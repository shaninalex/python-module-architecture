from contextlib import asynccontextmanager

from starlette.applications import Starlette

from blog.bootstrap.app import Application, build_app
from blog.runtime.config import Config


def build_web(cfg: Config) -> Starlette:
    holder: dict[str, Application] = {}

    @asynccontextmanager
    async def lifespan(_: Starlette):
        holder["app"] = await build_app(cfg)
        try:
            yield {"app": holder["app"]}
        finally:
            await holder["app"].aclose()

    return Starlette(
        debug=cfg.debug,
        lifespan=lifespan,
        # routes=routes(lambda: holder["app"]),
        # middleware=middleware(cfg),
        # exception_handlers={AppError: web_error_handler},
    )