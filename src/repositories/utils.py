

from datetime import date
from src.database import engine
from sqlalchemy import func, select

from src.models.bookings import BookingsOrm
from src.models.rooms import RoomsOrm


def rooms_ids_for_booking(
        date_to: date,
        date_from: date,
        hotel_id: int | None = None,
):
    room_count = (
        select(BookingsOrm.room_id, func.count("*").label("rooms_booked"))
        .select_from(BookingsOrm)
        .filter(BookingsOrm.date_to >= date_to, BookingsOrm.date_from <= date_from)
        .group_by(BookingsOrm.room_id)
        .cte(name="room_count")
    )

    rooms_left_table = (
        select(
            RoomsOrm.id.label("room_id"),
            (RoomsOrm.quantity - func.coalesce(room_count.c.rooms_booked, 0)
             ).label("rooms_left"),
        )
        .select_from(RoomsOrm)
        .outerjoin(room_count, RoomsOrm.id == room_count.c.room_id)
        .cte(name="rooms_left_table")
    )
    rooms_ids_for_hotel = (
        select(RoomsOrm.id)
        .select_from(RoomsOrm))
    
    if hotel_id is not None:
          rooms_ids_for_hotel= rooms_ids_for_hotel.filter_by(hotel_id=hotel_id)
    
    rooms_ids_for_hotel = ( 
         rooms_ids_for_hotel.subquery(name="rooms_ids_for_hotel")
                           )


    rooms_ids_to_get = (
        select(rooms_left_table.c.room_id)
        .select_from(rooms_left_table)
        .filter(rooms_left_table.c.rooms_left > 0,
                # Подзапрос
                rooms_left_table.c.room_id.in_(rooms_ids_for_hotel))
    )
    print(rooms_ids_to_get.compile(bind=engine,
          compile_kwargs={"literal_binds": True}))
    return rooms_ids_to_get
