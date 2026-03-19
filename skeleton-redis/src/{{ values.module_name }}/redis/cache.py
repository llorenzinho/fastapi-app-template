from collections.abc import Callable
from typing import Any, TypeVar

from pydantic import TypeAdapter
from redis import Redis

from {{ values.module_name }}.core.log import get_logger

T = TypeVar("T")


class CacheService:
    def __init__(self, redis: Redis) -> None:
        self.redis = redis
        self.__log = get_logger(CacheService.__name__)

    def get_or_set(
        self,
        key: str,
        factory: Callable[[], T],
        schema: Any,
        ttl: int = 300,
    ) -> T:
        self.__log.debug(f"try to get cached {key}")
        adapter: TypeAdapter[T] = TypeAdapter(schema)
        cached = self.redis.get(key)
        if cached:
            self.__log.debug("cache hit")
            return adapter.validate_json(cached)  # type: ignore

        result = factory()
        self.redis.setex(key, ttl, adapter.dump_json(result).decode())
        return result

    def invalidate(self, key: str) -> None:
        self.__log.debug(f"invalidating {key}")
        self.redis.delete(key)

    def ping(self) -> bool:
        try:
            return bool(self.redis.ping())  # type: ignore
        except Exception:
            return False
