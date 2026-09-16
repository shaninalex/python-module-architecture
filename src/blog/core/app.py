from dataclasses import dataclass
from typing import Protocol

from blog.core.bus import CommandBus, QueryBus, EventBus


@dataclass(frozen=True, slots=True)
class App:
    commands: CommandBus
    queries: QueryBus
    events: EventBus


class Module(Protocol):

    @property
    def name(self) -> str: ...

    def register(self, app: App) -> None: ...
