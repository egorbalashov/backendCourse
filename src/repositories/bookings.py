

from models.bookings import BookingsOrm
from repositories.base import BaseRepository
from sсhemas.bookings import Booking


class BookingsRepositories(BaseRepository):
    model=BookingsOrm
    schema = Booking