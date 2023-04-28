import logging
from src.configs.Nats import get_nats_connector
from src.configs.Nats import EVENT_METRICS_VISIT_CREATE
from src.utils import encode_json
from datetime import datetime
import asyncio

async def send_metrics(metrics: dict, request: any):
    try:
        nats_connection = await get_nats_connector()
        data = {
            "browser": request.headers.get("user-agent"),
            "acceptLanguage": request.headers.get("accept-language"),
            "time": datetime.now().isoformat(),
            **request.client._asdict(),
            **metrics,
        }
        future = asyncio.Future()
        async def cb(msg):
            nonlocal future
            future.set_result(msg)
        
        await nats_connection.subscribe(EVENT_METRICS_VISIT_CREATE, queue="metrics", cb=cb)
        await nats_connection.publish(EVENT_METRICS_VISIT_CREATE, encode_json(data))
        logging.info("pushed message from client ->", data["host"], "url -->", data["short"])
        # Terminate connection to NATS.
        msg = await asyncio.wait_for(future, 1)

        await nats_connection.drain()
    except Exception as e:
        logging.error("task.send_metrics")

    