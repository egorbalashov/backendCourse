from httpx import AsyncClient


async def test_get_hotels(ac: AsyncClient):
    response = await ac.get(
        url="/hotels",
        params={
            "date_from": "2025-01-05",
            "date_to": "2026-01-04",
        },
    )
    print(f"{response.json()=}")
    assert response.status_code == 200
