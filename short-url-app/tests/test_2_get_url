from fastapi.testclient import TestClient
from fastapi import status
from faker import Faker
from src.main import app
from src.utils import validate_url
from datetime import datetime
import logging

logger = logging.getLogger("LoggingTest")

fake = Faker()
client = TestClient(app)
headers={"Authorization": "Bearer hailhydra"}

def test_get_url():
    """Test create new URL"""
    response = client.get(f"/hst04l", headers=headers)
    response.text
    response.status_code
    # assert response.status_code == status.HTTP_307
