from httpx import AsyncClient
import pytest
from src.services.auth import AuthService


@pytest.mark.parametrize("email, password, status_code", [
    ("test_api_register_user@example.com", "123456", 200),
    ("2test_api_register_user@YA.com", "123456", 200),
])
async def test_register_user(email,
                             password,
                             status_code,
                             ac: AsyncClient,
                             ):
    response = await ac.post(
        url="/auth/register",
        json={
            "email": email,
            "password": password
        }
    )
    result = response.json()
    assert response.status_code == status_code
    assert result["status"] == "OK"


@pytest.mark.parametrize("email, password, status_code", [
    ("test_api_register_user@example.com", "123456", 200),
    ("2test_api_register_user@YA.com", "123456", 200),
])
async def test_login_user(email,
                          password,
                          status_code,
                          ac: AsyncClient,
                          ):
    response = await ac.post(
        url="/auth/login",
        json={
            "email": email,
            "password": password
        }
    )
    result = response.json()
    assert response.status_code == status_code
    assert result["access_token"]



async def test_me_user(ac: AsyncClient,  ):
    response = await ac.get(
        url="/auth/me",

    )
    result = response.json()
    assert response.status_code == 200
    assert result["id"]


async def test_logout_user(ac: AsyncClient,  ):
    response = await ac.post(
        url="/auth/logout",

    )
    result = response.json()
    assert response.status_code == 200









def test_decode_and_encode_access_token():
    data = {"user_id": 1}
    jwt_token = AuthService().create_access_token(data)

    assert jwt_token
    assert isinstance(jwt_token, str)

    payload = AuthService().decode_token(jwt_token)
    assert payload
    assert payload["user_id"] == data["user_id"]
