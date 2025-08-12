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

        