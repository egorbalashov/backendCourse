from httpx import AsyncClient


async def test_add_facilities(ac: AsyncClient):
    response = await ac.post(url="/fasilities", json={"title": "string22"})
    print(f"{response.json()=}")
    assert response.status_code == 200


async def test_get_facilities(ac: AsyncClient):
    response = await ac.get(
        url="/fasilities",
    )
    print(f"{response.json()=}")
    assert response.status_code == 200
    assert response.json() != []
