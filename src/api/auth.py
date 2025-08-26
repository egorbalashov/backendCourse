from fastapi import APIRouter, HTTPException, Response


from src.exceptions import ObjectAlreadyExistsException
from src.api.dependency import DBDep, UserIDDep
from src.services.auth import AuthService
from src.sсhemas.users import UserADD, UserRequestsADD


router = APIRouter(prefix="/auth", tags=["Авторизация и Аутентификация"])


@router.post("/register")
async def register_user(data: UserRequestsADD, db: DBDep):
    try:
        hashd_password = AuthService().hash_password(data.password)
        new_user_data = UserADD(email=data.email, hash_password=hashd_password)

        await db.users.add(new_user_data)
        await db.commit()
    except ObjectAlreadyExistsException:
        raise HTTPException(status_code=409, detail="Пользователь с такой почтой уже существует")

    return {"status": "OK"}


@router.post("/login")
async def login_user(data: UserRequestsADD, response: Response, db: DBDep):
    user = await db.users.get_user_hashed_password(email=data.email)
    if not user:
        raise HTTPException(status_code=401, detail="Неверный логин или пароль")
    if not AuthService().verify_password(data.password, user.hash_password):
        raise HTTPException(status_code=401, detail="Неверный логин или пароль")

    access_token = AuthService().create_access_token({"user_id": user.id})
    response.set_cookie("access_token", access_token)
    return {"access_token": access_token}


@router.get("/me")
async def get_me(user_id: UserIDDep, db: DBDep):
    user = await db.users.get_one_or_none(id=user_id)
    return user


@router.post("/logout")
async def logout(responce: Response):
    responce.delete_cookie("access_token")
    return {"status": "ОК"}
