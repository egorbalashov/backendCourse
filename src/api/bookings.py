



from fastapi import APIRouter, Response

from api.dependency import DBDep, UserIDDep
from sсhemas.bookings import BookingsAdd, BookingsAddRequests


router = APIRouter(prefix="/bookings", tags=["Бронирование"])

@router.post("")
async def add_booking(data_booking: BookingsAddRequests,
                      user_id: UserIDDep,
                      db:DBDep):
    room= await db.rooms.get_one_or_none(id=data_booking.room_id)
    _bookings_data = BookingsAdd(price=room.price,user_id=user_id, **data_booking.model_dump())
    booking =await db.bookings.add(data=_bookings_data)
    await db.commit()
    return {"status": "ОК", "data": booking}

