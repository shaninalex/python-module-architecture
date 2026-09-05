from starlette.requests import Request
from starlette.responses import PlainTextResponse


class StaticPages:
    async def contact(self, request: Request):
        return PlainTextResponse("contact page")

    async def about(self, request: Request):
        return PlainTextResponse("about")

    async def terms_conditions(self, request: Request):
        return PlainTextResponse("terms_conditions")
