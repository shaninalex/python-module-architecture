from sqlalchemy.ext.asyncio import AsyncEngine

from bootstrap.container import Container
from bootstrap.database import db_engine
from core.application import Application
from core.command_bus import CommandBus
from core.event_bus import EventBus
from modules.catalog.module import CatalogModule


def create_application():
    _container = Container()

    # core
    commands = CommandBus()
    _container.register(CommandBus, instance=commands)

    events = EventBus()
    _container.register(EventBus, instance=events)
    _container.register(AsyncEngine, instance=db_engine)

    # modules
    application = Application(
        commands=commands,
        events=events,
    )

    _container.register(Application, instance=application)

    # configure modules after declaring all base dependencies
    CatalogModule().configure(_container)

    return _container
