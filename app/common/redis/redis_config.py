
from redis.asyncio import Redis

from app.common.redis.redis_settings import redis_settings

redis_client: Redis | None = None

async def init_redis() -> Redis:
    global redis_client

    redis_client = Redis.from_url(
        redis_settings.redis_url,
        encoding="utf-8",
        decode_responses=True,
    )

    await redis_client.ping() # 퐁안오면 앱 시작 실패
    return redis_client

async def close_redis() -> None:
    global redis_client
    if redis_client:
        await redis_client.aclose()
        redis_client = None

def get_redis() -> Redis:
    if redis_client is None:
        raise RuntimeError("Redis is not initialized")
    return redis_client