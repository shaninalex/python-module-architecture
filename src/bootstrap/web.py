from starlette.applications import Starlette
from starlette.types import ASGIApp


def create_app() -> ASGIApp:
    return Starlette(
        debug=True,
        routes=[],
    )
