import pytest
from sqlalchemy import insert, select
from conftest import client
from src.auth_service.models import User
from src.auth_service.services import hash_password, create_user






def test_reg():
    response = client.post(
        "/v1/user/",
        json={"username": "general", "login": "sheppard", "password": "normandy777_X"},
    )
    print(response.text)
    assert response.status_code == 201