from pydantic import EmailStr
from sqlalchemy import select
from src.repositories.mappers.mappers import UserDataMapper
from src.models.users import UsersOrm
from src.repositories.base import BaseRepository
from src.sсhemas.users import UserWithHashedPassword


class UsersRepositoriy(BaseRepository):
    model = UsersOrm
    mapper = UserDataMapper

    async def get_user_hashed_password(self, email: EmailStr):
        query = select(self.model).filter_by(email=email)
        result = await self.session.execute(query)
        model = result.scalars().one_or_none()
        if model is None:
            return False

        return UserWithHashedPassword.model_validate(model)
