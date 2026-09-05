from starlette.applications import Starlette
from starlette.routing import Route
from starlette.types import ASGIApp

from adapters.web.handlers.home import HomePage
from adapters.web.handlers.static_pages import StaticPages
from core.application import Application


class WebAdapter:
    def __init__(self, app: Application):
        self.app = app

    def __call__(self, *args, **kwargs) -> ASGIApp:
        return Starlette(
            debug=True,
            routes=self.routes(),
        )

    def routes(self):
        home_page = HomePage(self.app)
        static_pages = StaticPages()
        return [
            Route("/", home_page.get, name='home'),
            Route("/contact", static_pages.contact, name='contact'),
            Route("/about", static_pages.about, name='about'),
            Route("/terms", static_pages.terms_conditions, name='terms_conditions'),
        ]
