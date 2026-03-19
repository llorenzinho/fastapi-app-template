from collections.abc import Generator
from typing import Annotated

from fastapi import Depends
from redis import Redis
from sqlalchemy import Engine
from sqlmodel import Session

from fastapi_template.auth.services import JwtService
from fastapi_template.config.app import AppConfig, cfg
from fastapi_template.database.engine import create_db_engine, get_session_sync
from fastapi_template.foo.repositories import FooRepo
from fastapi_template.foo.services import FooService
from fastapi_template.redis.cache import CacheService
from fastapi_template.redis.client import create_redis_client

ConfigDep = Annotated[AppConfig, Depends(dependency=cfg)]


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


def __get_jwt_service(conf: ConfigDep) -> JwtService:
    return JwtService(conf.jwt)


JwtServiceDep = Annotated[JwtService, Depends(dependency=__get_jwt_service)]


def __get_redis_client(config: ConfigDep) -> Redis:
    return create_redis_client(settings=config.redis)


RedisClientDep = Annotated[Redis, Depends(dependency=__get_redis_client)]


def __get_cache_service(redis: RedisClientDep) -> CacheService:
    return CacheService(redis=redis)


CacheServiceDep = Annotated[CacheService, Depends(dependency=__get_cache_service)]
