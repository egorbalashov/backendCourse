

from src.repositories.bookings import BookingsRepositories
from src.repositories.fasilities import FasilitiesRepositories, RoomFasilitiesRepositories
from src.repositories.hotels import HotelsRepository
from src.repositories.rooms import RoomsRepository
from src.repositories.users import UsersRepositoriy


class DBManager:

    def __init__(self, session_factory):
        self.session_factory = session_factory

    async def __aenter__(self):

        self.session = self.session_factory()
        
        self.hotels = HotelsRepository(self.session)
        self.rooms = RoomsRepository(self.session)
        self.users = UsersRepositoriy(self.session)
        self.bookings = BookingsRepositories(self.session)
        self.fasilities = FasilitiesRepositories(self.session)
        self.facilities_ids = RoomFasilitiesRepositories(self.session)

        return self

    async def __aexit__(self, *args):
        await self.session.rollback()
        await self.session.close()

    async def commit(self):
        await self.session.commit()
