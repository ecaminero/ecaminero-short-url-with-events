from fastapi.testclient import TestClient
from fastapi import status
from faker import Faker
from src.main import app
from datetime import datetime

from src.configs.Environment import get_environment_variables

# Application Environment Configuration
env = get_environment_variables()
app.dependency_overrides = {}

fake = Faker()
client = TestClient(app)
headers={"Authorization": "Bearer hailhydra"}


def test_create_url():
    """Test create new URL"""
    now = datetime.now().strftime("%m/%d/%Y %H:%M:%S")

    response = client.post("/admin/url",
        headers=headers,
        json={"url": fake.image_url(), "end_date": now},
    )
    assert response.status_code == status.HTTP_201_CREATED
    assert len(response.json()["short_url"].split("/")[-1]) == env.URL_SIZE
    assert response.json()["end_date"] == now


def test_create_url_with_invalid_params():
    """Test create with invalid params"""
    now = datetime.now().strftime("%m/%d/%Y %H:%M:%S")
    
    # Validate url 
    response = client.post("/admin/url",
        headers=headers,
        json={"url": "fake.image_url()", "end_date": now},
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "The url has an invalid format" in response.text

    response = client.post("/admin/url",
        headers=headers,
        json={"url": "", "end_date": ""},
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "The url has an invalid format" in response.text 