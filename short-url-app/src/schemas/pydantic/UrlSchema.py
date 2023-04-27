from __future__ import annotations

from datetime import datetime, timedelta, date
from pydantic import BaseModel, validator
from fastapi import Body
from typing import Optional
from src.utils import validate_url, available_url

class Url(BaseModel):
    url: str
    expire_at: Optional[date] = Body(
        default_factory=lambda: date.today() + timedelta(days=1))

    @validator("expire_at")
    def expire_at_is_valid(cls, expire_at: date) -> date:
        if expire_at <= date.today():
            raise ValueError("expire_at must be greater than today")

        return expire_at
    
    @validator("url")
    def url_is_valid(cls, url: str) -> datetime:
        if not validate_url(url):
            raise ValueError("Url is not valid, must be https://example.com")
        
        if not available_url(url, 4):
            raise ValueError("The url must be available")
        
        return url

