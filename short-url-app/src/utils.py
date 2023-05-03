import re
import json
import requests
from datetime import datetime, timedelta, date
from fastapi import status
import logging


def validate_url(url) -> bool:
    """Validate URL"""
    URL_PATTERN = "^https?:\\/\\/(?:www\\.)?[-a-zA-Z0-9@:%._\\+~#=]{1,256}\\.[a-zA-Z0-9()]{1,6}\\b(?:[-a-zA-Z0-9()@:%_\\+.~#?&\\/=]*)$"
    return bool(re.match(URL_PATTERN, url)) 

def available_url(url: str, timeout:int=1) -> bool:
    """Validate Available URL"""
    resp = False 
    try:
        resp = requests.get(url, timeout=timeout)
        resp = resp.status_code in (status.HTTP_200_OK, status.HTTP_201_CREATED)
    except Exception as e:
        logging.error(e)
        resp = False
    
    return resp 

def get_seconds(end_date: datetime = date.today()) -> int:
    """Get seconds between two dates"""
    return int((end_date - date.today()).total_seconds())

def get_default_datetime(date: datetime) -> datetime:
    """Get default datetime"""
    default = datetime.now() + timedelta(days=30)
    return date or default

def encode_json(data: dict) -> str:
    """Encode JSON"""
    return json.dumps(data).encode("utf-8")

def remove_empty_keys(data: dict):
    return {k: v for k,v in data.items()}