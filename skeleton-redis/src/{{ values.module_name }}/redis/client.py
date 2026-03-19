from redis import Redis

from {{ values.module_name }}.config.redis import RedisCfg


def create_redis_client(settings: RedisCfg) -> Redis:
    return Redis(
        host=settings.host,
        port=settings.port,
        db=settings.db,
        password=settings.password,
        decode_responses=True,
    )
