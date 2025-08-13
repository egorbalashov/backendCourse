from datetime import date
from typing import AsyncGenerator

from src.sсhemas.bookings import BookingsAdd
from utils.db_manager import DBManager


async def test_booking_crud(db: DBManager):
    user_id = (await db.users.get_all())[0].id
    room_id = (await db.rooms.get_all())[0].id
    booking_data = BookingsAdd(
        user_id=user_id,
        room_id=room_id,
        date_from=date(year=2024, month=8, day=10),
        date_to=date(year=2024, month=8, day=20),
        price=100,
    )
    await db.bookings.add(booking_data)
    await db.commit()

    created_booking = await db.bookings.get_one_or_none(user_id=user_id)
    assert created_booking is not None
    assert created_booking.price == 100


    updated_data = BookingsAdd(
        user_id=user_id,
        room_id=room_id,
        date_from=date(2024, 8, 10),
        date_to=date(2024, 8, 20),
        price=200,
    )
    update_result = await db.bookings.edit(
        data=updated_data,
        exclude_unset=True,
        id=created_booking.id  # Добавляем фильтр по ID
    )

    result_booking = await db.bookings.get_one_or_none(user_id=user_id)
    assert result_booking is not None
    assert result_booking.price == updated_data.price
    
    delete_booking = await db.bookings.delete(id=result_booking.id)
    result_booking = await db.bookings.get_one_or_none(id=result_booking.id)
    assert  result_booking is None
    await db.commit()

