import os
from contextlib import asynccontextmanager

from starlette.applications import Starlette
from starlette.middleware import Middleware
from starlette.middleware.sessions import SessionMiddleware
from starlette.routing import Route, Mount
from starlette.staticfiles import StaticFiles
from starlette.types import ASGIApp

from adapters.web.core.middlewares import middlewares
from adapters.web.core.template import Templates
from adapters.web.handlers.customer import CustomerPages
from adapters.web.handlers.home import HomePage
from adapters.web.handlers.product_detail import ProductPage
from adapters.web.handlers.static_pages import StaticPages
from bootstrap.database import db_engine
from core.application import Application


@asynccontextmanager
async def lifespan(app):
    yield
    await db_engine.dispose()


class WebAdapter:
    def __init__(self, application: Application):
        self.templates = Templates()
        self.app = application

    def __call__(self, *args, **kwargs) -> ASGIApp:
        return Starlette(
            debug=True,
            routes=self.routes(),
            lifespan=lifespan,
            middleware=self.make_middlewares(),
        )

    def make_middlewares(self):
        return middlewares(self.app)

    def routes(self):
        home_page = HomePage(self.app, self.templates)
        product_page = ProductPage(self.app, self.templates)
        static_pages = StaticPages(self.templates)
        customer_pages = CustomerPages(self.app, self.templates)
        return [
            Mount("/static", app=StaticFiles(directory=os.environ.get("APP_MARKET_WEB_STATIC_PATH")), name="static"),
            Route("/", home_page.get, name='home'),
            Route("/contact", static_pages.contact, name='contact'),
            Route("/about", static_pages.about, name='about'),
            Route("/terms", static_pages.terms_conditions, name='terms_conditions'),
            Route("/product/{product_id:int}", product_page.get, name='product'),
            Route("/registration", customer_pages.register_get, name='register', methods=['GET']),
            Route("/registration", customer_pages.register_submit, name='register_submit', methods=['POST']),
            Route("/login", customer_pages.login_get, name='login', methods=['GET']),
            Route("/login", customer_pages.login_post, name='login_submit', methods=['POST']),
            Route("/logout", customer_pages.logout, name='logout', methods=['GET']),
        ]
