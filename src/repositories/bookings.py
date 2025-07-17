

from datetime import date
from src.database import engine
from sqlalchemy import func, select
from models.bookings import BookingsOrm
from models.rooms import RoomsOrm
from repositories.base import BaseRepository
from sсhemas.bookings import Booking


class BookingsRepositories(BaseRepository):
    model=BookingsOrm
    schema = Booking



