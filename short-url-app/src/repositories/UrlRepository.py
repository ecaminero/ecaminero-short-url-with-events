from fastapi import Depends
from typing import List, Optional
from sqlalchemy.orm import Session
from datetime import datetime
from src.configs import get_db_connection
from src.models.UrlModel import Url
from src.schemas import UrlFilter
import logging


class UrlRepository:
    original: str
    short: float
    expire_at: datetime
    db: Session

    def __init__(self, db: Session = Depends(get_db_connection)) -> None:
        self.db = db

    async def create(self, data: Url) -> Url:
        try:
            self.db.add(data)
            self.db.commit()
            self.db.refresh(data)
        except Exception as e:
            logging.error(e.message)
            raise(e)

        return data

    def getById(self, data: Url) -> Url:
        return self.db.get(Url, data.id)
    
    def getByQuery(self, data: Url, attr: Optional[Url] = Url) -> List[Url]:
        try:
            return self.db.query(attr).filter(data)
        except Exception as e:
            return None
    
    async def update(self, data: Url) -> Url:
        try:
            self.db.merge(data)
            self.db.commit()
            self.db.refresh(data)
        except Exception as e:
            logging.error(e.message)
            raise (e)

        return data

    async def delete(self, url: Url) -> None:
        try:
            self.db.delete(url)
            self.db.commit()
            self.db.flush()
        except Exception as e:
            logging.error(e.message)

            raise (e)

    def filter(self, filter: Optional[UrlFilter], first:bool = False) -> List[Url]:
        query = self.db.query(Url)
        query = filter.filter(query)
        query = filter.sort(query)
        scalars = self.db.execute(query).scalars()
        return scalars.first() if first else scalars.all()
