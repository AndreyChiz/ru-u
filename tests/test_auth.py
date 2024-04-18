import pytest
from sqlalchemy import insert, select
from conftest import client
from src.auth_service.models import User
from src.auth_service.services import hash_password, create_user


def test_reg():
    response = client.post(
        "/v1/user/",
        json={"username": "general1", "login": "sheppard", "password": "normandy777_X"},
    )
    print(response.text)
    assert response.status_code == 201


def test_log():
    response = client.post(
        "/v1/user/login",
        json={"login": "sheppard", "password": "normandy777_X"},
    )
    assert response.status_code == 200
    assert response.headers == {
        "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6ImdlbmVyYWwxIiwibG9naW4iOiJzaGVwcGFyZCIsImlkIjoxfQ.o2OtwN60xzqY9Qbp_y0njjW2L8FMG5SU-70asUi2fXA",
        "token_type": "Bearer",
        "content-length": "22",
        "content-type": "application/json",
    }
    assert response.text == '{"message":"login ok"}'
