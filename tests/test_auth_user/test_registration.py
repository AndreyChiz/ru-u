from httpx import AsyncClient




async def test_registration_ok(ac: AsyncClient):
    response = await ac.post(
        "/v1/user/",
        json={"username": "General", "login": "Sheppard", "password": "normandy777_X"},
    )
    assert response.status_code == 201, "Успешная регистрация пользователя"
    assert response.text == '{"username":"General","login":"Sheppard"}'

    response = response = await ac.post(
        "/v1/user/",
        json={
            "username": "Gordon",
            "login": "Freeman",
            "password": "B1ack_mesa",
        },
    )
    assert response.status_code == 201, "Успешная регистрация пользователя"
    assert response.text == '{"username":"Gordon","login":"Freeman"}'


async def test_registration_broken(ac: AsyncClient):
    response = await ac.post(
        "/v1/user/",
        json={"username": "General", "login": "Sheppard", "password": "normandy777_X"},
    )
    assert response.status_code == 400, "Пользователь с name или login существует"
    assert response.text == '{"detail":"User with this name or login already exist"}'

    response = await ac.post(
        "/v1/user/",
        json={"username": "Gordon", "login": "Sheppard", "password": "normandy777_X"},
    )
    assert response.status_code == 400, "Пользователь с name или login существует"
    assert response.text == '{"detail":"User with this name or login already exist"}'

    response = await ac.post(
        "/v1/user/",
        json={"username": "General", "login": "Freeman", "password": "normandy777_X"},
    )
    assert response.status_code == 400, "Пользователь с name или login существует"
    assert response.text == '{"detail":"User with this name or login already exist"}'

    response = await ac.post(
        "/v1/user/",
        json={"username": "", "login": "Sheppard", "password": "normandy777_X"},
    )

    assert response.status_code == 422, "Пустое поле name"
    assert (
        response.text
        == '{"detail":[{"type":"string_too_short","loc":["body","username"],"msg":"String should have at least 3 characters","input":"","ctx":{"min_length":3},"url":"https://errors.pydantic.dev/2.6/v/string_too_short"}]}'
    )

    username = "x" * 2
    response = await ac.post(
        "/v1/user/",
        json={"username": "xx", "login": "Sheppard", "password": "normandy777_X"},
    )

    assert response.status_code == 422, "Name меньше разрешённого"
    assert (
        response.text
        == '{"detail":[{"type":"string_too_short","loc":["body","username"],"msg":"String should have at least 3 characters","input":"'
        + username
        + '","ctx":{"min_length":3},"url":"https://errors.pydantic.dev/2.6/v/string_too_short"}]}'
    )

    username = "x" * 40
    response = await ac.post(
        "/v1/user/",
        json={"username": username, "login": "Sheppard", "password": "normandy777_X"},
    )
    assert response.status_code == 422, "Name больше разрешённого"
    assert (
        response.text
        == '{"detail":[{"type":"string_too_long","loc":["body","username"],"msg":"String should have at most 32 characters","input":"'
        + username
        + '","ctx":{"max_length":32},"url":"https://errors.pydantic.dev/2.6/v/string_too_long"}]}'
    )

    username = "General1"
    response = await ac.post(
        "/v1/user/",
        json={"username": username, "login": "Sheppard", "password": "normandy777_X"},
    )

    assert response.status_code == 400, "Name содержит цыфры"
    assert response.text == '{"detail":"Username must contain at least only letters"}'





















# async def test_login_ok(ac: AsyncClient):
#     response = await ac.post(
#         "/v1/user/login",
#         json={"username": "General1", "login": "Sheppard", "password": "normandy777_X"},
#     )
#     assert response.status_code == 200
#     assert response.headers == {
#         "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6IkdlbmVyYWwxIiwibG9naW4iOiJTaGVwcGFyZCIsImlkIjoxfQ.4CDGeFqp70n7sShoaZIy0MK9U7cZ8r90aht1ZwLQ0Uo",
#         "token_type": "Bearer",
#         "content-length": "22",
#         "content-type": "application/json",
#     }
#     assert response.text == '{"message":"login ok"}'

#     response = await ac.post(
#         "/v1/user/login", json={"login": "Freeman", "password": "B1ack_mesa"}
#     )

#     assert response.status_code == 200
#     assert response.headers == {
#         "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6IkdvcmRvbiIsImxvZ2luIjoiRnJlZW1hbiIsImlkIjoyfQ.NwYifsUbIzG5yVh64Ro9tSM7K2ZWB51i1Nn3n1zR_NI",
#         "token_type": "Bearer",
#         "content-length": "22",
#         "content-type": "application/json",
#     }


# async def test_login_broken(ac: AsyncClient):
#     response = await ac.post(
#         "/v1/user/login",
#         json={"login": "", "password": ""},
#     )
#     assert response.status_code == 400

#     response = await ac.post(
#         "/v1/user/login",
#         json={"username": "General1", "login": "Sheppard", "password": "B1ack_mesa"},
#     )
#     assert response.status_code == 400
