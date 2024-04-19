from httpx import AsyncClient


async def test_registration_ok(ac: AsyncClient):
    response = await ac.post(
        "/v1/user/",
        json={"username": "General1", "login": "Sheppard", "password": "normandy777_X"},
    )
    assert response.status_code == 201, "Успешная регистрация пользователя"

    response = response = await ac.post(
        "/v1/user/",
        json={
            "username": "Gordon",
            "login": "Freeman",
            "password": "B1ack_mesa",
        },
    )
    assert response.status_code == 201, "Успешная регистрация пользователя"


async def test_registration_broken(ac: AsyncClient):
    response = await ac.post(
        "/v1/user/",
        json={"username": "General1", "login": "Sheppard", "password": "normandy777_X"},
    )
    response = await ac.post(
        "/v1/user/",
        json={"username": "Gordon", "login": "Sheppard", "password": "normandy777_X"},
    )
    assert (
        response.status_code == 400
    ), "Повторное создание пользователя с cсуществующим именем или логином"

    response = await ac.post(
        "/v1/user/",
        json={"username": "General1", "login": "Freeman", "password": "normandy777_X"},
    )
    assert (
        response.status_code == 400
    ), "Повторное создание пользователя с cсуществующим именем или логином"


async def test_login_ok(ac: AsyncClient):
    response = await ac.post(
        "/v1/user/login",
        json={"username": "General1", "login": "Sheppard", "password": "normandy777_X"},
    )
    assert response.status_code == 200
    assert (
        response.headers
        == {'access_token': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6IkdlbmVyYWwxIiwibG9naW4iOiJTaGVwcGFyZCIsImlkIjoxfQ.4CDGeFqp70n7sShoaZIy0MK9U7cZ8r90aht1ZwLQ0Uo', 'token_type': 'Bearer', 'content-length': '22', 'content-type': 'application/json'}
    )
    assert response.text == '{"message":"login ok"}'

    response = await ac.post("/v1/user/login", json={"login": "Freeman", "password": "B1ack_mesa"})

    assert response.status_code == 200
    assert response.headers == {
        "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6IkdvcmRvbiIsImxvZ2luIjoiRnJlZW1hbiIsImlkIjoyfQ.NwYifsUbIzG5yVh64Ro9tSM7K2ZWB51i1Nn3n1zR_NI",
        "token_type": "Bearer",
        "content-length": "22",
        "content-type": "application/json",
    }

async def test_login_broken(ac: AsyncClient):
    response = await ac.post(
        "/v1/user/login",
        json={"login": "", "password": ""},
    )
    assert response.status_code == 400

    response = await ac.post(
        "/v1/user/login",
        json={"username": "General1", "login": "Sheppard", "password": "B1ack_mesa"},
    )
    assert response.status_code == 400
