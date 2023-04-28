import logging
from src.configs.Nats import get_nats_connector
from src.configs.Nats import EVENT_METRICS_VISIT_CREATE
from src.utils import encode_json
from datetime import datetime

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
        await nats_connection.publish(
            EVENT_METRICS_VISIT_CREATE, encode_json(data))
        logging.debug("pushed message from client ->", data["host"], "url -->", data["short"])
    except Exception as e:
        logging.error("task.send_metrics", e)
        import pdb; pdb.set_trace()

