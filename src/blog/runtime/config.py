import os
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


def config_path(p: str | Path | None = None) -> Path:
    if p:
        return Path(p).expanduser().resolve()

    env_path = os.getenv("BLOG_CONFIG_PATH") or os.getenv("BLOG_CONFIG")
    if env_path:
        return Path(env_path).expanduser().resolve()

    candidates = [
        Path.cwd() / "config" / "config.yaml",
        Path.cwd() / "config" / "config.yml",
        Path.cwd() / "config.yaml",
        Path("/etc/blog/config.yaml"),
    ]
    for candidate in candidates:
        if candidate.is_file():
            return candidate.resolve()

    return (Path.cwd() / "config" / "config.yaml").resolve()


def load(path: Path) -> Config:
    with open(path) as f:
        config = yaml.safe_load(f)
        return Config(
            env=config.get("env", "development"),
            debug=config.get("debug", False),
            database=DatabaseConfig(
                url=Secret(config["database"]["url"]),
                echo=config["database"]["echo"],
                pool_size=config["database"].get("pool_size", 10),
                ssl=config["database"]["ssl"],
            ),
            web=WebConfig(
                secret_key=Secret(config["web"]["secret_key"]),
                https_only=config["web"]["https_only"],
                session_max_age=config["web"].get("session_max_age"),
                same_site=config["web"].get("same_site"),
            ),
            api=ApiConfig(
                cors_origins=config["api"]["cors_origins"],
            ),
        )
