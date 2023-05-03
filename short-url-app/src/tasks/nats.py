import logging
from src.configs.Nats import get_nats_connector
from src.configs.Nats import EVENT_URL_METRICS
from src.utils import encode_json
from datetime import datetime
import uuid

async def send_metrics(metrics: dict, request: any):
    try:
        nats_connection = await get_nats_connector()
        data = {
            "eventId": str(uuid.uuid4()),
            "browser": request.headers.get("user-agent"),
            "acceptLanguage": request.headers.get("accept-language"),
            "time": datetime.now().isoformat(),
            **request.client._asdict(),
            **metrics,
        }
        js = nats_connection.jetstream()
        logging.info("pushed message from client ->", data["host"], "url -->", data["short"])
        await js.publish("metrics.url.visit", encode_json(data))
        await nats_connection.close()        
        # Disconnect from the server
    except Exception as e:
        print(e)
        logging.error("task.send_metrics")

    