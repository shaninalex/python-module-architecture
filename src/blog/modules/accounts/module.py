from dataclasses import dataclass

from blog.core.app import App
from blog.modules import accounts as contract
from blog.runtime.clock import Clock
from blog.runtime.db.session import SessionProvider


@dataclass(frozen=True, slots=True)
class Deps:
    session: SessionProvider
    clock: Clock


class AccountModule:
    def __init__(self, deps: Deps) -> None:
        self._display_names: contract.DisplayNames

    @property
    def name(self) -> str:
        return "accounts"

    def display_names(self) -> contract.DisplayNames:
        return self._display_names

    def register(self, app: App) -> None:
        return None


def build(deps: Deps) -> AccountModule:
    return AccountModule(deps)
