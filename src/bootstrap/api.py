from starlette.types import ASGIApp

from adapters.api.server import ApiAdapter
from bootstrap.container import Container
from core.application import Application


def create_api(container: Container) -> ASGIApp:
    application = container.resolve(Application)
    adapter = ApiAdapter(application)
    return adapter()
