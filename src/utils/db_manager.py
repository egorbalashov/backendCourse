

from repositories.bookings import BookingsRepositories
from repositories.hotels import HotelsRepository
from repositories.rooms import RoomsRepository
from repositories.users import UsersRepositoriy


class DBManager:

    def __init__(self, session_factory):
        self.session_factory = session_factory

    async def __aenter__(self):

        self.session = self.session_factory()
        
        self.hotels = HotelsRepository(self.session)
        self.rooms = RoomsRepository(self.session)
        self.users = UsersRepositoriy(self.session)
        self.bookings = BookingsRepositories(self.session)

        return self

    async def __aexit__(self, *args):
        await self.session.rollback()
        await self.session.close()

    async def commit(self):
        await self.session.commit()
