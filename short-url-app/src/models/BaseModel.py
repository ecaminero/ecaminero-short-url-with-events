from sqlalchemy.orm import declarative_base
from src.configs.Database import Engine

# Base Entity Model Schema
Base = declarative_base()

def init():
    Base.metadata.create_all(bind=Engine)