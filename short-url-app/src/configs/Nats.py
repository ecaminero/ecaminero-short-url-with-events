import nats
import logging
from src.configs.Environment import get_environment_variables

env = get_environment_variables()
EVENT_URL_CREATE = "url.create"
EVENT_URL_UPDATE = "url.update"
EVENT_URL_METRICS = "metrics.url.visit"

async def get_nats_connector():
    async def disconnected_cb():
        logging.warn('Got disconnected!')

    async def reconnected_cb():
        logging.info(f'Got reconnected to {nc.connected_url.netloc}')

    async def error_cb(e):
        logging.error(f'There was an error: {e}')

    async def closed_cb():
        logging.info('Connection is closed')

    nc = await nats.connect(
        env.NATS_SERVER,
        error_cb=error_cb,
        reconnected_cb=reconnected_cb,
        disconnected_cb=disconnected_cb,
        closed_cb=closed_cb,
    )
    return nc
