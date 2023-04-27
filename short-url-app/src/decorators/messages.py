from __future__ import annotations
import logging
from functools import wraps
from typing import Optional, TypeVar
from src.utils import encode_json
from src.configs.Nats import get_nats_connector
from typing import Any, Awaitable, Callable, TypeVar

from typing_extensions import ParamSpec

P = ParamSpec("P")
R = TypeVar("R")

def publish_message(channel: Optional[str] = ""):
    def inner_decorator(function: Callable[P, Awaitable[R]]) -> Callable[P, Awaitable[R]]:
        
        @wraps(function)
        async def wrapper(*args, **kwargs):
            nonlocal channel
            result = await function(*args, **kwargs)
            try:
                nats_connection = await get_nats_connector()
                await nats_connection.publish(channel, encode_json(result))
                logging.debug("pushed message", result)
            except Exception as e:
                logging.warn("NATS Server is not available")
            # Process a message
            return result
        return wrapper
    return inner_decorator
