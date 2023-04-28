from __future__ import annotations
import logging
import json
from functools import wraps
from typing import Any, Awaitable, Callable, TypeVar
from src.configs import async_get_redis_connection
from fastapi.responses import RedirectResponse
from typing_extensions import ParamSpec
from src.tasks import nats

P = ParamSpec("P")
R = TypeVar("R")

def cache(function: Callable[P, Awaitable[R]]) -> Callable[P, Awaitable[R]]:
    @wraps(function)
    async def wrapper(*args, **kwargs):
        copy_kwargs = kwargs.copy()
        background_tasks = copy_kwargs.pop("background_tasks")
        request = copy_kwargs.pop("request")
        short_url = copy_kwargs["short_url"]
        try:
            redis = await async_get_redis_connection()
            cache_data = await redis.get(short_url)
            if cache_data:
                cache_data = json.loads(cache_data)
                logging.info("--GET FROM CACHE--")
                metrics = {"short": short_url, "original": cache_data["original"]}
                background_tasks.add_task(nats.send_metrics, metrics, request)
                return RedirectResponse(cache_data["original"])
        except Exception as e:
            logging.error("redis.cache", e)
        
        return await function(*args, **kwargs)
    
    return wrapper


