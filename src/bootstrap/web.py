from starlette.types import ASGIApp

from adapters.web.server import WebAdapter
from bootstrap.container import Container
from core.application import Application


def create_web(container: Container) -> ASGIApp:
    application = container.resolve(Application)
    adapter = WebAdapter(application)
    return adapter()
