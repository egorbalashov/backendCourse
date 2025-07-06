

from models.users import UsersOrm
from repositories.base import BaseRepository
from sсhemas.users import User


class UsersRepositoriy(BaseRepository):
    model = UsersOrm
    schema = User