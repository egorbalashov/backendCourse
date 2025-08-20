from fastapi import APIRouter

from src.api.dependency import DBDep, UserIDDep
from src.sсhemas.bookings import BookingsAdd, BookingsAddRequests


router = APIRouter(prefix="/bookings", tags=["Бронирование"])


@router.get("/bookings")
async def all_bookings(db: DBDep):
    bookings = await db.bookings.get_all()
    return {"status": "ОК", "data": bookings}


@router.get("/bookings/me")
async def all_bookings_me(db: DBDep, user_id: UserIDDep):
    bookings_me = await db.bookings.get_filtered(user_id=user_id)
    return {"status": "ОК", "data": bookings_me}


@router.post("")
async def add_booking(data_booking: BookingsAddRequests, user_id: UserIDDep, db: DBDep):
    room = await db.rooms.get_one_or_none(id=data_booking.room_id)
    hotel = await db.hotels.get_one_or_none(id=room.hotel_id)
    _bookings_data = BookingsAdd(price=room.price, user_id=user_id, **data_booking.model_dump())
    booking = await db.bookings.add_booking(_bookings_data, hotel_id=hotel.id)
    await db.commit()
    return {"status": "OK", "data": booking}
