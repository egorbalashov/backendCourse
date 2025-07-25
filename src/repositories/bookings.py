

from datetime import date
from src.repositories.mappers.mappers import BookingDataMapper
from src.database import engine
from sqlalchemy import func, select
from src.models.bookings import BookingsOrm
from src.models.rooms import RoomsOrm
from src.repositories.base import BaseRepository
from src.sсhemas.bookings import Booking


class BookingsRepositories(BaseRepository):
    model=BookingsOrm
    mapper = BookingDataMapper



