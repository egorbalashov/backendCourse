import json
from typing import List
from httpx import ASGITransport, AsyncClient
import pytest

from src.config import settings
from src.database import Base, engine_null_pool
from src.models import *
from src.main import app


@pytest.fixture(scope="session", autouse=True)
def check_test_mode():
    """
    - Проверяет тестовый режим (MODE=TEST)
    - Иначе фиксура  async_main НЕ ЗАПУСКАЕТСЯ
    """
    assert settings.MODE == "TEST"


@pytest.fixture(scope="session",    # scope: определяет время жизни фикстуры:
                                    # "function" - для каждой тест-функции (по умолчанию)
                                    # "class" - для каждого тест-класса
                                    # "module" - для каждого модуля с тестами
                                    # "session" - один раз на все тесты (как в этом случае)

                autouse=True)
async def setup_database(check_test_mode):
    async with engine_null_pool.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)




@pytest.fixture(scope="session", autouse=True)
async def register_user(setup_database):
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        await ac.post(
            "/auth/register",
            json={
                "email": "kot@pes.com",
                "password": "1234"
            }
        )

@pytest.fixture(scope="session", autouse=True)
async def add_hotels(setup_database):
    with open('tests/mock_hotels.json', 'r', encoding='utf-8') as file:
        hotels_data: List[dict] = json.load(file)
        # 3. Используем один клиент для всех запросов
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        for hotel_data in hotels_data:
            response = await ac.post(
                "/hotels",
                json={
                    "title": hotel_data['title'],
                    "location": hotel_data['location']
                }
            )
            assert response.status_code == 200  # Проверяем успешность

@pytest.fixture(scope="session", autouse=True)
async def add_rooms(add_hotels):
    with open('tests/mock_rooms.json', 'r', encoding='utf-8') as file:
        hotels_rooms: List[dict] = json.load(file)
        # 3. Используем один клиент для всех запросов
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        for rooms in hotels_rooms:
            response = await ac.post(
                f"/hotels/{rooms['hotel_id']}/room",
                json={
                    "hotel_id": rooms['hotel_id'],
                    "title": rooms['title'],
                    "description": rooms['description'],
                    "price": rooms['price'],
                    "quantity": rooms['quantity'],
                    "facilities_ids":[]

                }
            )
            assert response.status_code == 200  # Проверяем успешность
    

