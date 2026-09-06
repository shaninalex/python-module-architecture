from typing import Dict, List, Protocol

from seeder.config import Config
from seeder.context import Context
from seeder.db import Tables
from seeder.entities import BrandsSeeder, CategorySeeder, ProductsSeeder
from seeder.utils import create_connection


class Seeder(Protocol):
    def name(self) -> str: ...

    def seed(self, ctx: Context): ...

    def clear(self, ctx: Context): ...


class SeederRegistry:
    def __init__(self):
        self._registry: Dict[str, Seeder] = {}

    def register(self, s: Seeder):
        self._registry[s.name()] = s

    def list(self) -> List[Seeder]:
        return list(self._registry.values())


def log(s: Seeder, msg: str):
    print(f"[{s.name()}]: {msg}")


class Executor:
    def __init__(self, ctx: Context, registry: SeederRegistry):
        self._ctx = ctx
        self._registry = registry

    def clear(self):
        # reverse of the seed order, so children go before the rows they reference
        for s in reversed(self._registry.list()):
            log(s, "clearing")
            s.clear(self._ctx)

    def run(self):
        for s in self._registry.list():
            log(s, "seeding...")
            s.seed(self._ctx)
            log(s, "complete.")


def context(config: Config) -> Context:
    connection = create_connection(config)
    return Context(
        config=config,
        connection=connection,
        tables=Tables(connection, config.database.schema),
    )


def start(config: Config):
    ctx = context(config)

    registry = SeederRegistry()
    registry.register(CategorySeeder())
    registry.register(BrandsSeeder())
    registry.register(ProductsSeeder())

    executor = Executor(ctx, registry)
    executor.clear()
    executor.run()
