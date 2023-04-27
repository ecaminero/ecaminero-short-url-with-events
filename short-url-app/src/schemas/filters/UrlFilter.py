from typing import Optional
from fastapi_filter.contrib.sqlalchemy import Filter
from src.models.UrlModel import Url
from pydantic import validator


class UrlFilter(Filter):
    key: Optional[str]
    id: Optional[str]
    original__like: Optional[str]
    short__like: Optional[str]
    order_by: Optional[list[str]]
    
    class Constants(Filter.Constants):
        model = Url
        search_field_name = "search_url"
        search_model_fields = ["original", "short"]  # It will search in both `name` and `email` columns.
    
    @validator("order_by")
    def restrict_sortable_fields(cls, value):
        if value is None:
            return None

        allowed_field_names = ["expire_at"]

        for field_name in value:
            field_name = field_name.replace("+", "").replace("-", "")  # (1)
            if field_name not in allowed_field_names:
                raise ValueError(f"You may only sort by: {', '.join(allowed_field_names)}")



