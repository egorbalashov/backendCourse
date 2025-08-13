import json
from typing import List
from httpx import ASGITransport, AsyncClient
import pytest

from src.config import settings
from src.database import Base, engine_null_pool, async_session_maker_null_pool
from src.models import *
from src.main import app
from src.sсhemas.hotel import HotelADD
from src.sсhemas.rooms import RoomsADD
from src.utils.db_manager import DBManager


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
    hotels = [HotelADD.model_validate(hotel) for hotel in hotels_data]
    async with DBManager(session_factory=async_session_maker_null_pool) as db:
        await db.hotels.add_bulk(hotels)
        await db.commit()

@pytest.fixture(scope="session", autouse=True)
async def add_rooms(add_hotels):
    with open('tests/mock_rooms.json', 'r', encoding='utf-8') as file:
        hotels_rooms: List[dict] = json.load(file)
        # 3. Используем один клиент для всех запросов
    rooms = [RoomsADD.model_validate(room) for room in hotels_rooms]
    async with DBManager(session_factory=async_session_maker_null_pool) as db:
        await db.rooms.add_bulk(rooms)
        await db.commit()

