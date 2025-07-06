

from pydantic import EmailStr
from sqlalchemy import select
from models.users import UsersOrm
from repositories.base import BaseRepository
from sсhemas.users import User, UserWithHashedPassword


class UsersRepositoriy(BaseRepository):
    model = UsersOrm
    schema = User

    async def get_user_hashed_password(self, email: EmailStr):
        query = select(self.model).filter_by(email=email)
        result = await self.session.execute(query)
        model =result.scalars().one_or_none()
        if model is None:
            return False
        
        return UserWithHashedPassword.model_validate(model)
