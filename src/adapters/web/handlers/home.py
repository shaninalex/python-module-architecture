from dataclasses import asdict

from starlette.requests import Request
from starlette.responses import JSONResponse

from core.application import Application
from modules.catalog.application.query import ListProductsCommand


class HomePage:
    def __init__(self, app: Application):
        self.app = app

    async def get(self, request: Request):
        query = request.query_params.get("q")

        products = await self.app.execute(
            ListProductsCommand(query=query)
        )

        return JSONResponse([asdict(p) for p in products])
