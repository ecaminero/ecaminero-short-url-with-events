import logging
import json
from src.configs import async_get_redis_connection
from src.utils import get_seconds

async def set_key(data: dict):
    try:
        redis = await async_get_redis_connection()
        await redis.set(data.key, json.dumps(data.normalize()))

        print(get_seconds(data.expire_at))
        await redis.expire(data.key, get_seconds(data.expire_at))
    except Exception as e:
        logging.warn("Redis Server is not available")


async def delete_key(data: dict):
    try:
        redis = await async_get_redis_connection()
        await redis.delete(data.key)
    except Exception as e:
        logging.warn("Redis Server is not available")
