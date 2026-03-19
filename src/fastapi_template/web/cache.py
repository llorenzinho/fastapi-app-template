import functools
import inspect
from collections.abc import Callable
from typing import Any, ParamSpec, TypeVar

from fastapi_template.redis.cache import CacheService
from fastapi_template.web.deps import CacheServiceDep

P = ParamSpec("P")
T = TypeVar("T")


def cached(
    schema: Any, key: str, ttl: int = 300
) -> Callable[[Callable[P, T]], Callable[P, T]]:
    """
    Decorator for FastAPI route handlers that caches the response in Redis.

    The `key` supports format-string placeholders resolved from the route's
    kwargs at call time, e.g. key="foo:{id}" resolves {id} from the request.

    Usage::

        @router.get("/{id}")
        @cached(key="foo:{id}", schema=FooSchema, ttl=60)
        def get_foo(svc: FooServiceDep, id: UUIDParam) -> FooSchema:
            return svc.get_foo_detail(id)
    """

    def decorator(func: Callable[P, T]) -> Callable[P, T]:
        sig = inspect.signature(func)
        cache_param = inspect.Parameter(
            "__cache__",
            kind=inspect.Parameter.KEYWORD_ONLY,
            annotation=CacheServiceDep,
        )
        new_sig = sig.replace(parameters=[*sig.parameters.values(), cache_param])

        @functools.wraps(func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> T:
            cache: CacheService = kwargs.pop("__cache__")  # type: ignore[misc]
            resolved_key = key.format_map(kwargs)
            return cache.get_or_set(
                key=resolved_key,
                factory=lambda: func(*args, **kwargs),
                schema=schema,
                ttl=ttl,
            )

        wrapper.__signature__ = new_sig  # type: ignore[attr-defined]
        return wrapper  # type: ignore[return-value]

    return decorator


def invalidate_cache(*keys: str) -> Callable[[Callable[P, T]], Callable[P, T]]:
    """
    Decorator for FastAPI route handlers that invalidates one or more Redis keys
    after the handler executes successfully.

    Each key supports format-string placeholders resolved from the route's
    kwargs at call time, e.g. "foo:{id}" resolves {id} from the request.

    Usage::

        @router.delete("/{id}")
        @invalidate_cache("foo:{id}", "foo:list")
        def delete_foo(svc: FooServiceDep, id: UUIDParam) -> FooSchema:
            return svc.delete_foo(id)
    """

    def decorator(func: Callable[P, T]) -> Callable[P, T]:
        sig = inspect.signature(func)
        cache_param = inspect.Parameter(
            "__cache__",
            kind=inspect.Parameter.KEYWORD_ONLY,
            annotation=CacheServiceDep,
        )
        new_sig = sig.replace(parameters=[*sig.parameters.values(), cache_param])

        @functools.wraps(func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> T:
            cache: CacheService = kwargs.pop("__cache__")  # type: ignore[misc]
            result = func(*args, **kwargs)
            for key in keys:
                cache.invalidate(key.format_map(kwargs))
            return result

        wrapper.__signature__ = new_sig  # type: ignore[attr-defined]
        return wrapper  # type: ignore[return-value]

    return decorator
