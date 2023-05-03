from fastapi.responses import RedirectResponse
from src.services.UrlService import UrlService
from src.decorators.redis import cache
from src.tasks import redis, nats
from src.schemas.filters.UrlFilter import UrlFilter
from fastapi import (
    APIRouter, Depends,
    status, HTTPException,
    BackgroundTasks, Request
)

MainRouter = APIRouter(prefix="")


@MainRouter.get("/")
async def pong() -> str:
    return "pong"


@MainRouter.get("/{short_url}",
                response_class=RedirectResponse,
                status_code=status.HTTP_302_FOUND)
@cache
async def get_ĺong_url(short_url: str, request: Request, background_tasks: BackgroundTasks, urlService: UrlService = Depends()):
    result = urlService.filter(UrlFilter(key=short_url), first=True)
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    metrics = {"short": short_url, "original": result.original}
    background_tasks.add_task(nats.send_metrics, metrics, request)
    background_tasks.add_task(redis.set_key, result)
    return result.original
