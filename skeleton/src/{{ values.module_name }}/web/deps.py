from collections.abc import Generator
from typing import Annotated

from fastapi import Depends
{% if values.enable_redis %}
from redis import Redis
{% endif %}
{% if values.enable_postgres %}
from sqlalchemy import Engine
from sqlmodel import Session
{% endif %}

from {{ values.module_name }}.auth.services import JwtService
from {{ values.module_name }}.config.app import AppConfig, cfg
{% if values.enable_postgres %}
from {{ values.module_name }}.database.engine import create_db_engine, get_session_sync
from {{ values.module_name }}.foo.repositories import FooRepo
from {{ values.module_name }}.foo.services import FooService
{% endif %}
{% if values.enable_redis %}
from {{ values.module_name }}.redis.cache import CacheService
from {{ values.module_name }}.redis.client import create_redis_client
{% endif %}

ConfigDep = Annotated[AppConfig, Depends(dependency=cfg)]

{% if values.enable_postgres %}

def __get_engine(config: ConfigDep) -> Engine:
    return create_db_engine(settings=config.db)


EngineDep = Annotated[Engine, Depends(dependency=__get_engine)]


def __get_session_sync(engine: EngineDep) -> Generator[Session, None, None]:
    with get_session_sync(engine=engine) as session:
        with session.begin():
            try:
                yield session
            except Exception:
                session.rollback()
                raise


SyncSessionDep = Annotated[Session, Depends(dependency=__get_session_sync)]


def __get_foo_repo(s: SyncSessionDep) -> FooRepo:
    return FooRepo(session=s)


__FooRepoDep = Annotated[FooRepo, Depends(dependency=__get_foo_repo)]


def __get_foo_service(repo: __FooRepoDep) -> FooService:
    return FooService(repo=repo)


FooServiceDep = Annotated[FooService, Depends(dependency=__get_foo_service)]

{% endif %}


def __get_jwt_service(conf: ConfigDep) -> JwtService:
    return JwtService(conf.jwt)


JwtServiceDep = Annotated[JwtService, Depends(dependency=__get_jwt_service)]

{% if values.enable_redis %}


def __get_redis_client(config: ConfigDep) -> Redis:
    return create_redis_client(settings=config.redis)


RedisClientDep = Annotated[Redis, Depends(dependency=__get_redis_client)]


def __get_cache_service(redis: RedisClientDep) -> CacheService:
    return CacheService(redis=redis)


CacheServiceDep = Annotated[CacheService, Depends(dependency=__get_cache_service)]

{% endif %}
