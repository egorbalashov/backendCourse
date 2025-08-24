from fastapi import APIRouter, HTTPException
from src.services.bookings import BookingService
from src.exceptions import ObjectNotFoundException, AllRoomsAreBookedException
from src.api.dependency import DBDep, UserIDDep
from src.sсhemas.bookings import BookingsAdd, BookingsAddRequests
from src.sсhemas.rooms import Rooms
from src.exceptions import ObjectNotFoundException, AllRoomsAreBookedException, RoomNotFoundHTTPException


router = APIRouter(prefix="/bookings", tags=["Бронирование"])


@router.get("/bookings")
async def all_bookings(db: DBDep):
    bookings = await BookingService(db).get_all()
    return {"status": "ОК", "data": bookings}


@router.get("/bookings/me")
async def all_bookings_me(db: DBDep, user_id: UserIDDep):
    
    
    bookings_me = await BookingService(db).get_filtered(user_id=user_id)
    return {"status": "ОК", "data": bookings_me}

@router.post("")
async def add_booking(data_booking: BookingsAddRequests, user_id: UserIDDep, db: DBDep):
    booking = await BookingService(db).add_booking(data_booking=data_booking,
                                                   user_id=user_id,
                                                   )
    return {"status": "OK", "data": booking}
