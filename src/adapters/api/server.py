from contextlib import asynccontextmanager

from starlette.applications import Starlette
from starlette.routing import Route
from starlette.types import ASGIApp

from adapters.api.handlers.products import ProductEndpoint
from bootstrap.database import db_engine
from core.application import Application


@asynccontextmanager
async def lifespan(app):
    yield
    await db_engine.dispose()


class ApiAdapter:
    def __init__(self, application: Application):
        self.app = application

    def __call__(self, *args, **kwargs) -> ASGIApp:
        return Starlette(
            debug=True,
            routes=self.routes(),
            lifespan=lifespan
        )

    def routes(self):
        product_endpoint = ProductEndpoint(self.app)
        return [
            Route("/api/v1/products", product_endpoint.list, name='products'),
            Route("/api/v1/products/{product_id:int}", product_endpoint.details, name='products'),
        ]
