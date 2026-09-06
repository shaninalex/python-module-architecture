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

        products = await self.app.execute(
            ListProductsCommand(query=query)
        )

        return self.templates.TemplateResponse(request, "views/home.html", {
            "products": [asdict(p) for p in products],
        })