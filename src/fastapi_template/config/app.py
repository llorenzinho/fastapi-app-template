from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict

from fastapi_template.config.database import DatabaseCfg
from fastapi_template.config.jwt import JwtConfig
from fastapi_template.config.log import LogCfg
from fastapi_template.config.redis import RedisCfg
from fastapi_template.config.server import ServerCfg


class AppConfig(BaseSettings):
    db: DatabaseCfg
    log: LogCfg
    server: ServerCfg
    jwt: JwtConfig
    redis: RedisCfg

    model_config = SettingsConfigDict(
        env_prefix="APP_",
        env_file=".env",
        extra="ignore",
        env_nested_delimiter="__",
    )


@lru_cache
def cfg() -> AppConfig:
    return AppConfig()  # type: ignore
