

from fastapi import APIRouter, HTTPException, Request, Response

import sqlalchemy

from api.dependency import UserIDDep
from repositories.users import UsersRepositoriy
from services.auth import AuthService
from sсhemas.users import UserADD, UserRequestsADD

from src.database import async_session_maker

router = APIRouter(prefix="/auth", tags=["Авторизация и Аутентификация"])


@router.post("/register")
async def register_user(data: UserRequestsADD):
    hashd_password = AuthService().hash_password(data.password)
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
async def login_user(data: UserRequestsADD,
                     response: Response):
    async with async_session_maker() as session:
        user = await UsersRepositoriy(session).get_user_hashed_password(email=data.email)
        if not user:
            raise HTTPException(
                status_code=401, detail="Неверный логин или пароль")
        if not AuthService().verify_password(data.password, user.hash_password):
            raise HTTPException(
                status_code=401, detail="Неверный логин или пароль")

        access_token = AuthService().create_access_token({"user_id": user.id})
        response.set_cookie("access_token", access_token)
        return {"access_token": access_token}
    

@router.get("/me")
async def get_me(
        user_id: UserIDDep,
):
    async with async_session_maker() as session:
        user=await UsersRepositoriy(session).get_one_or_none(id=user_id)
        return user


