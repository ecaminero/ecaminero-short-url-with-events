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

@MainRouter.get("/{short_url}", 
                response_class=RedirectResponse, 
                status_code=status.HTTP_307_TEMPORARY_REDIRECT)
@cache
async def get_ĺong_url(short_url: str, background_tasks: BackgroundTasks, urlService: UrlService = Depends()):
    url = urlService.filter(UrlFilter(key=short_url))
    if not url:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    url = url[0] # first element
    background_tasks.add_task(redis.set_key, url)
    return  url.original
