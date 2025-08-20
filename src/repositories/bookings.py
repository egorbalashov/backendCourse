

from datetime import date
from src.repositories.mappers.mappers import BookingDataMapper
from src.database import engine
from sqlalchemy import func, select
from src.models.bookings import BookingsOrm
from src.models.rooms import RoomsOrm
from src.repositories.base import BaseRepository
from src.sсhemas.bookings import Booking, BookingsAddRequests


class BookingsRepositories(BaseRepository):
    model=BookingsOrm
    mapper = BookingDataMapper

    async def add_booking(self,
                          data_booking:BookingsAddRequests,
                          count_room:int
                          ):
        booking_rooms = await self.get_filtered(self.model.room_id==data_booking.room_id )
        count_booked = len(booking_rooms)
        print(f"Уже забронировано: {count_booked}")
        
        if count_booked >= count_room:
            print(booking_rooms)
            raise Exception("Нет свободных комнат",count_room-count_booked )
        else:
            print(f"Еще свободно: {count_room-count_booked}")
                    



