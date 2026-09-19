import yaml
from pathlib import Path
from dataclasses import dataclass
from typing import Literal

from blog.runtime.secret import Secret


@dataclass(frozen=True, slots=True)
class DatabaseConfig:
    url: Secret
    echo: bool = False
    pool_size: int = 10
    ssl: bool = True


@dataclass(frozen=True, slots=True)
class WebConfig:
    secret_key: Secret
    https_only: bool = True
    session_max_age: int = 14 * 24 * 3600
    same_site: Literal["lax", "strict", "none"] = "lax"


@dataclass(frozen=True, slots=True)
class ApiConfig:
    cors_origins: tuple[str, ...] = ()


@dataclass(frozen=True, slots=True)
class Config:
    env: Literal["development", "staging", "production"]
    debug: bool
    database: DatabaseConfig
    web: WebConfig
    api: ApiConfig


def load(path: Path) -> Config:
    with open(path) as f:
        config = yaml.safe_load(f)
        return config
