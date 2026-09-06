from dataclasses import dataclass
from typing import Any

from seeder.config import Config
from seeder.db import Tables


@dataclass(frozen=True)
class Context:
    """What every seeder gets: the connection plus a schema bound table factory."""

    config: Config
    connection: Any
    tables: Tables

    def cursor(self):
        return self.connection.cursor()

    def commit(self):
        self.connection.commit()
