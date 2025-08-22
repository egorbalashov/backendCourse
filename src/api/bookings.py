from fastapi import APIRouter, HTTPException
from src.exceptions import ObjectNotFoundException, AllRoomsAreBookedException
from src.api.dependency import DBDep, UserIDDep
from src.sсhemas.bookings import BookingsAdd, BookingsAddRequests
from src.sсhemas.rooms import Rooms
from src.exceptions import ObjectNotFoundException, AllRoomsAreBookedException, RoomNotFoundHTTPException


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
    try:
        room: Rooms = await db.rooms.get_one(id=data_booking.room_id)
    except ObjectNotFoundException:
        raise RoomNotFoundHTTPException
    hotel = await db.hotels.get_one_or_none(id=room.hotel_id)
    _bookings_data = BookingsAdd(price=room.price, user_id=user_id, **data_booking.model_dump())
    try:
        booking = await db.bookings.add_booking(_bookings_data, hotel_id=hotel.id)
    except AllRoomsAreBookedException as ex:
        raise HTTPException(status_code=409, detail=ex.detail)
    await db.commit()
    return {"status": "OK", "data": booking}
