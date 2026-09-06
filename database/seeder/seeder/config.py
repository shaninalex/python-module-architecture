from dataclasses import dataclass
from pathlib import Path

import yaml


@dataclass(frozen=True)
class DatabaseConfig:
    database: str
    user: str
    password: str
    host: str
    port: int
    schema: str = "public"


@dataclass(frozen=True)
class Config:
    database: DatabaseConfig


def read_config(path: Path) -> Config:
    with open(path, "r") as f:
        fconf = yaml.safe_load(f)
        return Config(
            database=DatabaseConfig(**fconf["database"]),
        )
