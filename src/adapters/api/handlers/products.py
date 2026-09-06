from typing import List

from starlette.requests import Request
from starlette.responses import JSONResponse

from core.application import Application
from modules.catalog.application.query import ListProductsCommand, ProductDetailCommand
from modules.catalog.domain.product import ProductModel


class ProductEndpoint:
    def __init__(self, app: Application):
        self.app = app

    async def list(self, request: Request):
        query = request.query_params.get("q")
        offset = 0
        limit = 20

        _offset = request.query_params.get("offset")
        if _offset is not None:
            offset = int(_offset)

        _limit = request.query_params.get("limit")
        if _limit is not None:
            limit = int(_limit)

        products: List[ProductModel] = await self.app.execute(
            ListProductsCommand(
                query=query,
                offset=offset,
                limit=limit,
            )
        )

        return JSONResponse({
            "products": [p.to_dict() for p in products],
        })

    async def details(self, request: Request):
        product = await self.app.execute(
            ProductDetailCommand(
                product_id=int(request.path_params.get("product_id")),
            )
        )

        return JSONResponse(product.to_dict())