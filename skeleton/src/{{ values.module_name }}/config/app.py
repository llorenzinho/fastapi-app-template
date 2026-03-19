from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict

{% if values.enable_postgres %}
from {{ values.module_name }}.config.database import DatabaseCfg
{% endif %}
from {{ values.module_name }}.config.jwt import JwtConfig
from {{ values.module_name }}.config.log import LogCfg
{% if values.enable_redis %}
from {{ values.module_name }}.config.redis import RedisCfg
{% endif %}
from {{ values.module_name }}.config.server import ServerCfg


class AppConfig(BaseSettings):
    {% if values.enable_postgres %}
    db: DatabaseCfg
    {% endif %}
    log: LogCfg
    server: ServerCfg
    jwt: JwtConfig
    {% if values.enable_redis %}
    redis: RedisCfg
    {% endif %}

    model_config = SettingsConfigDict(
        env_prefix="APP_",
        env_file=".env",
        extra="ignore",
        env_nested_delimiter="__",
    )


@lru_cache
def cfg() -> AppConfig:
    return AppConfig()  # type: ignore
