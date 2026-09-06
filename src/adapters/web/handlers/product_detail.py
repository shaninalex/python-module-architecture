from starlette.requests import Request

from adapters.web.core.template import Templates
from core.application import Application
from modules.catalog.application.query import ProductDetailCommand


class ProductPage:
    def __init__(self, app: Application, templates: Templates):
        self.templates = templates
        self.app = app

    async def get(self, request: Request):
        product = await self.app.execute(
            ProductDetailCommand(
                product_id=int(request.path_params.get("product_id")),
            )
        )

        return self.templates.TemplateResponse(request, "views/product_detail.html", {
            "product": product,
        })
