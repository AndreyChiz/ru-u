from httpx import AsyncClient



async def test_login_ok(ac: AsyncClient):
    response = await ac.post(
        "/v1/user/login", json={"login": "Sheppard", "password": "normandy777_X"}
    )

    assert response.status_code == 200, "Успешная авторизация"
    assert response.text == '{"message":"login ok"}'
    assert response.headers == {
        "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6IkdlbmVyYWwiLCJsb2dpbiI6IlNoZXBwYXJkIiwiaWQiOjF9.uoirpMPVvhXv2mRio4kepfUap6xJV3zaHaabcLInQBc",
        "token_type": "Bearer",
        "content-length": "22",
        "content-type": "application/json",
    }

    response = await ac.post(
        "/v1/user/login",
        json={
            "login": "Freeman",
            "password": "B1ack_mesa",
        },
    )
    assert response.status_code == 200, "Успешная авторизация"
    assert response.text == '{"message":"login ok"}'
    assert response.headers == {
        "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6IkdvcmRvbiIsImxvZ2luIjoiRnJlZW1hbiIsImlkIjoyfQ.NwYifsUbIzG5yVh64Ro9tSM7K2ZWB51i1Nn3n1zR_NI",
        "token_type": "Bearer",
        "content-length": "22",
        "content-type": "application/json",
    }
