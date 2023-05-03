from typing import List, Optional
from nanoid import generate
from fastapi import Depends
from sqlalchemy.dialects.postgresql import UUID

from src.models.UrlModel import Url
from src.repositories.UrlRepository import UrlRepository
from src.schemas.pydantic import UrlSchema
from src.configs.Environment import get_environment_variables
from src.schemas.filters.UrlFilter import UrlFilter
from src.utils import remove_empty_keys

env = get_environment_variables()


class UrlService:
    urlRepository: UrlRepository

    def __init__(self, urlRepository: UrlRepository = Depends()) -> None:
        self.urlRepository = urlRepository

    def create(self, data: UrlSchema) -> Url:
        key = generate(size=env.URL_SIZE)
        return self.urlRepository.create(
            Url(
                original=data.original,
                short=f"{env.BASE_URL}/{key}",
                key=key,
                expire_at=data.expire_at)
        )

    def delete(self, url: Url) -> None:
        return self.urlRepository.delete(url)

    def filter(self, filter: Optional[UrlFilter], first:bool = False) -> List[Url]:
        return self.urlRepository.filter(filter, first)

    def get_by_id(self, id: UUID) -> Url:
        return self.urlRepository.get_by_id(Url(id=id))

    def get(self, data: Url) -> Url:
        return self.urlRepository.get_by_query(data)

    def update(self, data: dict) -> dict:
        update = remove_empty_keys(data)
        update = Url(**update)
        return self.urlRepository.update(update)

    def is_duplicated(self, url: UrlSchema) -> bool:
        data = self.urlRepository.get_by_query(Url.original == url.original, Url.id)
        return bool(data.first())
