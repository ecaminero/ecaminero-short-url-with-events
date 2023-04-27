from uuid import UUID
from src.schemas.pydantic.UrlSchema import Url
from src.schemas.filters.UrlFilter import UrlFilter
from src.services.UrlService import UrlService
from src.tasks import redis
from fastapi_filter import FilterDepends
from src.decorators.messages import publish_message
from src.configs.Nats import EVENT_URL_CREATE
from fastapi import (
    APIRouter,
    Depends,
    status,
    HTTPException,
    BackgroundTasks
)

AdminRouter = APIRouter(
    prefix="/admin/url",
    tags=["administration"]
)

@AdminRouter.get("")
async def filter(
        url_filter: UrlFilter = FilterDepends(UrlFilter),
        urlService: UrlService = Depends()) -> list:
    return urlService.filter(url_filter)


@AdminRouter.post("", status_code=status.HTTP_201_CREATED)
@publish_message(EVENT_URL_CREATE)
async def create(data: Url, background_tasks: BackgroundTasks, urlService: UrlService = Depends()) -> dict:
    is_duplicate = urlService.is_duplicated(data)
    if is_duplicate:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Url already exists")

    result = await urlService.create(data)
    background_tasks.add_task(redis.set_key, result)
    return result.normalize()


@AdminRouter.get("/{id}")
async def get(id: UUID, urlService: UrlService = Depends()) -> dict:
    result = urlService.getById(id)
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return result.normalize()


@AdminRouter.delete("/{id}", status_code=status.HTTP_200_OK)
async def delete(id: UUID, urlService: UrlService = Depends()) -> dict:
    result = urlService.getById(id)
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    await urlService.delete(result)
    return result.normalize()


@AdminRouter.put("/{id}", status_code=status.HTTP_200_OK)
@publish_message("url.update")
async def update(id: UUID, data: Url, background_tasks: BackgroundTasks, urlService: UrlService = Depends()) -> dict:
    url = urlService.get(id)
    if not url:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    print("url.id----->", url.id)
    print("url.data----->", data)

    result = await urlService.update(url, data)
    background_tasks.add_task(redis.set_key, result)

    return result.normalize()
