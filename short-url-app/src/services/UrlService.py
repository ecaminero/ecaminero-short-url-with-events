from typing import List, Optional
from nanoid import generate
from fastapi import Depends
from sqlalchemy.dialects.postgresql import UUID

from src.models.UrlModel import Url
from src.repositories.UrlRepository import UrlRepository
from src.schemas.pydantic import UrlSchema
from src.configs.Environment import get_environment_variables
from src.schemas.filters.UrlFilter import UrlFilter

env = get_environment_variables()


class UrlService:
    urlRepository: UrlRepository

    def __init__(self, urlRepository: UrlRepository = Depends()) -> None:
        self.urlRepository = urlRepository

    def create(self, data: UrlSchema) -> Url:
        key = generate(size=env.URL_SIZE)
        return self.urlRepository.create(
            Url(
                original=data.url,
                short=f"{env.BASE_URL}/{key}",
                key=key,
                expire_at=data.expire_at)
        )

    def delete(self, url: Url) -> None:
        return self.urlRepository.delete(url)

    def filter(self, filter: Optional[UrlFilter]) -> List[Url]:
        return self.urlRepository.filter(filter)

    def getById(self, id: UUID) -> Url:
        return self.urlRepository.getById(Url(id=id))

    def get(self, data: Url) -> Url:
        return self.urlRepository.getByQuery(data)

    def update(self, url: Url, data: UrlSchema) -> dict:
        url.expire_at = data.expire_at
        url.original = data.url
        return self.urlRepository.update(url)

    def is_duplicated(self, url: UrlSchema) -> bool:
        data = self.urlRepository.getByQuery(Url.original == url.url, Url.id)
        return bool(data.first())
