# Для упрощения импортов в других частях приложения они вынесены в __init__.py
from src.models.hotels import HotelsOrm
from src.models.rooms import RoomsOrm
from src.models.users import UsersOrm
from src.models.bookings import BookingsOrm
from src.models.facilities import FacilitiesOrm