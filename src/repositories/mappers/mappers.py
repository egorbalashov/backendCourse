from src.models.bookings import BookingsOrm
from src.models.facilities import FacilitiesOrm, RoomsFacilitiesOrm
from src.models.rooms import RoomsOrm
from src.models.users import UsersOrm
from src.models.hotels import HotelsOrm
from src.repositories.mappers.base import DataMapper
from src.sсhemas.hotel import Hotel
from src.sсhemas.bookings import Booking
from src.sсhemas.fasilities import Fasilities, RoomFasilities
from src.sсhemas.rooms import RoomWithRels, Rooms
from src.sсhemas.users import User


class HotelDataMapper(DataMapper):
    db_model = HotelsOrm
    schema = Hotel


class RoomDataMapper(DataMapper):
    db_model = RoomsOrm
    schema = Rooms


class RoomDataWithRelsMapper(DataMapper):
    db_model = RoomsOrm
    schema = RoomWithRels


class UserDataMapper(DataMapper):
    db_model = UsersOrm
    schema = User


class BookingDataMapper(DataMapper):
    db_model = BookingsOrm
    schema = Booking


class FacilityDataMapper(DataMapper):
    db_model = FacilitiesOrm
    schema = Fasilities


class RoomFacilityDataMapper(DataMapper):
    db_model = RoomsFacilitiesOrm
    schema = RoomFasilities