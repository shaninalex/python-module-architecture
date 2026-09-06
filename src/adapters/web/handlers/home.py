from dataclasses import asdict

from starlette.requests import Request

from adapters.web.core.template import Templates
from core.application import Application
from modules.catalog.application.query import ListProductsCommand


class HomePage:
    def __init__(self, app: Application, templates: Templates):
        self.templates = templates
        self.app = app

    async def get(self, request: Request):
        query = request.query_params.get("q")
        offset = 0
        limit = 20

        _offset = request.query_params.get("offset")
        if _offset is not None:
            offset = int(_offset)

        _limit = request.query_params.get("limit")
        if _limit is not None:
            limit = int(_limit)

        products = await self.app.execute(
            ListProductsCommand(
                query=query,
                offset=offset,
                limit=limit,
            )
        )

        return self.templates.TemplateResponse(request, "views/home.html", {
            "products": [asdict(p) for p in products],
        })
