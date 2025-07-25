

from typing import Annotated
from fastapi import Depends, HTTPException, Query, Request
from pydantic import BaseModel

from src.services.auth import AuthService
from src.utils.db_manager import DBManager
from src.database import async_session_maker


class PaginationParams(BaseModel):

    page: Annotated[int, Query(1, ge=1, description="Номер страницы")]
    per_page: Annotated[int, Query(
        15, gt=1, lt=30, description="Количество элементов на странице")]


PaginationDep = Annotated[PaginationParams, Depends()]


def get_token(requests: Request) -> str:
    token = requests.cookies.get("access_token", None)
    if not token:
        raise HTTPException(status_code=401, detail="Не найден токен")
    return token


def get_current_user_id(token: str = Depends(get_token)) -> int:
    data = AuthService.decode_token(token)
    return data["user_id"]


UserIDDep = Annotated[int, Depends(get_current_user_id)]


def get_db_manager():
    return DBManager(session_factory=async_session_maker)


async def get_db():
    async with get_db_manager() as db:
        yield db

DBDep = Annotated[DBManager, Depends(get_db)]
