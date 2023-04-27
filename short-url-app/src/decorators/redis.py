from __future__ import annotations
import logging
import json
from functools import wraps
from typing import Any, Awaitable, Callable, TypeVar
from src.configs import async_get_redis_connection
from fastapi.responses import RedirectResponse
from typing_extensions import ParamSpec

P = ParamSpec("P")
R = TypeVar("R")

def cache(function: Callable[P, Awaitable[R]]) -> Callable[P, Awaitable[R]]:
    @wraps(function)
    async def wrapper(*args, **kwargs):
        copy_kwargs = kwargs.copy()
        try:
            redis = await async_get_redis_connection()
            cache_value = await redis.get(copy_kwargs["short_url"])
            if cache_value:
                cache_value = json.loads(cache_value)
                logging.info("--Get From cache--")
                return RedirectResponse(cache_value["original"])
        except Exception as e:
            logging.warn("NATS Server is not available")
        return await function(*args, **kwargs)
    
    return wrapper


