from typing import Protocol

from bootstrap.container import Container


class Module(Protocol):
    def configure(self, container: Container):
        ...