from fastapi import HTTPException
from src.exceptions import AllRoomsAreBookedException, ObjectNotFoundException, RoomNotFoundHTTPException
from src.api.dependency import DBDep, UserIDDep
from src.services.base import BaseService
from src.sсhemas.bookings import BookingsAdd, BookingsAddRequests
from src.sсhemas.rooms import Rooms


class BookingService(BaseService):

    
    async def get_all(self):
        return await self.db.bookings.get_all()
    

    async def get_filtered(self,
                           user_id:int):
    
        return await self.db.bookings.get_filtered(user_id=user_id)
    
    async def add_booking(self,
                          data_booking: BookingsAddRequests, 
                          user_id: UserIDDep, 
                          
):
        try:
            room: Rooms = await self.db.rooms.get_one(id=data_booking.room_id)
        except ObjectNotFoundException:
            raise RoomNotFoundHTTPException
        hotel = await self.db.hotels.get_one_or_none(id=room.hotel_id)
        _bookings_data = BookingsAdd(price=room.price, user_id=user_id, **data_booking.model_dump())
        try:
            booking = await self.db.bookings.add_booking(_bookings_data, hotel_id=hotel.id)
        except AllRoomsAreBookedException as ex:
            raise HTTPException(status_code=409, detail=ex.detail)
        await self.db.commit()
        return booking