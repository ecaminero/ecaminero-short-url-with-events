from redis import asyncio, Redis
from src.configs.Environment import get_environment_variables

env = get_environment_variables()

async def async_get_redis_connection() -> Redis:
    session =  await asyncio.from_url(
        f"redis://{env.REDIS_HOST}:{env.REDIS_PORT}", 
        password=env.REDIS_PASSWORD, 
        encoding="utf-8", 
        decode_responses=True
    )
    return session
