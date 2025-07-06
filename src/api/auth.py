
from datetime import datetime, timezone, timedelta
from fastapi import APIRouter, HTTPException
from passlib.context import CryptContext
import sqlalchemy
import jwt
from repositories.users import UsersRepositoriy
from sсhemas.users import UserADD, UserRequestsADD
from src.database import async_session_maker

router = APIRouter(prefix="/auth", tags=["Авторизация и Аутентификация"])


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + \
        timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode |= {"exp": expire}
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


@router.post("/register")
async def register_user(data: UserRequestsADD):
    hashd_password = pwd_context.hash(data.password)
    new_user_data = UserADD(email=data.email, hash_password=hashd_password)
    try:
        async with async_session_maker() as session:
            await UsersRepositoriy(session).add(new_user_data)
            await session.commit()
    except sqlalchemy.exc.IntegrityError as e:
        return {"status": "false",
                "detail": "Key email already exists"}
    return {"status": "ОК"}


@router.post("/login")
async def login_user(data: UserRequestsADD):
    async with async_session_maker() as session:
        user = await UsersRepositoriy(session).get_one_or_none(email=data.email)
        if not user:
            raise HTTPException(
                status_code=401, detail="Пользователь с таким email не зарегистрирован")
        access_token = create_access_token({"user_id": user.id})
        return {"access_token":access_token}
