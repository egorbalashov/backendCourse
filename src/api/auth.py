

from fastapi import APIRouter
from passlib.context import CryptContext

from repositories.users import UsersRepositoriy
from sсhemas.users import UserADD, UserRequestsADD
from src.database import async_session_maker

router = APIRouter(prefix="/auth", tags=["Авторизация и Аутентификация"])


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

@router.post("/register")
async def register_user(data: UserRequestsADD):
    hashd_password = pwd_context.hash(data.password)
    new_user_data= UserADD(email=data.email, hash_password=hashd_password)
    async with async_session_maker() as session:
        await UsersRepositoriy(session).add(new_user_data)
        await session.commit()
    return {"status": "ОК"}
    
