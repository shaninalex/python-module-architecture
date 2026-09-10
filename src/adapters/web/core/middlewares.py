import os

from starlette.middleware import Middleware
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware

from core.application import Application
from modules.customer.application.commands import CustomerGetCommand


def middlewares(application: Application):
    secret_key = os.getenv("APP_MARKET_SECRET")
    if secret_key is None:
        raise Exception("Unable to init SessionMiddleware - secret key is not defined")

    https_only = os.getenv("APP_MARKET_ENV") != "development"

    return [
        Middleware(SessionMiddleware, secret_key=secret_key, https_only=https_only),
        Middleware(CORSMiddleware, allow_origins=['*']),
        Middleware(CustomerHeaderMiddleware, application=application)
    ]


class CustomerHeaderMiddleware(BaseHTTPMiddleware):
    def __init__(
            self,
            app,
            application: Application,
    ):
        super().__init__(app)
        self.application = application

    async def dispatch(self, request, call_next):
        user_id = request.session.get("user_id")
        if user_id is not None:
            customer = await self.application.execute(
                CustomerGetCommand(user_id=int(user_id))
            )
            request.state.customer = customer

        response = await call_next(request)
        return response
