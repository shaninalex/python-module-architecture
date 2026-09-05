from typing import Protocol


class Module(Protocol):
    def configure(self, container):
        ...