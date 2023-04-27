from fastapi.responses import RedirectResponse
from src.services.UrlService import UrlService
from src.decorators.redis import cache
from src.tasks import redis
from src.schemas.filters.UrlFilter import UrlFilter
from fastapi import (
    APIRouter, Depends,
    status, HTTPException,
    BackgroundTasks
)

MainRouter = APIRouter(prefix="")

@MainRouter.get("/")
async def pong() -> str:
    return "pong"

@MainRouter.get("/{short_url}", response_class=RedirectResponse)
@cache
async def get_ĺong_url(short_url: str,  background_tasks: BackgroundTasks, urlService: UrlService = Depends()):
    url = urlService.get(UrlFilter(key=short_url))
    if not url:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    background_tasks.add_task(redis.set_key, url)
    return RedirectResponse(url.original)
