import os
from functools import lru_cache
from pydantic import BaseSettings

@lru_cache
def get_env_filename():
    runtime_env = os.getenv("ENV")
    return f".env.{runtime_env}" if runtime_env else ".env"

class EnvironmentSettings(BaseSettings):
    API_VERSION: str = "v1"
    APP_NAME: str = "Short URL API"
    APP_PORT: int =  os.getenv("APP_PORT", 8000)
    URL_SIZE: int = os.getenv("URL_SIZE", 6)
    DEBUG_MODE: bool = os.getenv("DEBUG_MODE", True)
    BASE_URL: str = os.getenv("BASE_URL", "http://localhost:8000") 
    # Database 
    DATABASE_DIALECT: str = os.getenv("DATABASE_DIALECT", "postgresql+psycopg2")
    DATABASE_HOST: str  = os.getenv("DATABASE_HOST", "localhost")
    DATABASE_NAME: str = os.getenv("DATABASE_NAME", "meli")
    DATABASE_PASSWORD: str = os.getenv("DATABASE_PASSWORD", "meli")
    DATABASE_PORT: int = os.getenv("DATABASE_PORT", "5432")
    DATABASE_USERNAME: str = os.getenv("DATABASE_DIALECT", "meli")
    # Redis
    REDIS_HOST: str = os.getenv("REDIS_HOST", "localhost")
    REDIS_PORT: int = os.getenv("REDIS_PORT", 6379)
    REDIS_PASSWORD: str = os.getenv("REDIS_PASSWORD", "meli")
    NATS_SERVER: str

    class Config:
        env_file = get_env_filename()
        env_file_encoding = "utf-8"

@lru_cache
def get_environment_variables():
    return EnvironmentSettings()
