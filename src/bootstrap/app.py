from bootstrap.container import Container
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

    # modules
    catalog_module = CatalogModule()
    _container.register(CatalogModule, instance=catalog_module)

    application = Application(
        commands=commands,
        events=events,
    )

    _container.register(Application, instance=application)

    # configure modules after declaring all base dependencies
    catalog_module.configure(_container)

    return _container
