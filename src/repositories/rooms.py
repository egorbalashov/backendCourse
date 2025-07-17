

from sqlalchemy import func, select
from models.rooms import RoomsOrm
from repositories.base import BaseRepository
from sсhemas.rooms import Rooms

from datetime import date
from src.database import engine
from sqlalchemy import func, select
from models.bookings import BookingsOrm


class RoomsRepository(BaseRepository):
    model = RoomsOrm
    schema = Rooms


    async def get_filtered_by_time(
            self,
            hotel_id,
            date_to: date,
            date_from: date,
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
                (RoomsOrm.quantity - func.coalesce(room_count.c.rooms_booked, 0)).label("rooms_left"),
            )
            .select_from(RoomsOrm)
            .outerjoin(room_count, RoomsOrm.id == room_count.c.room_id)
            .cte(name="rooms_left_table")
        )
        rooms_ids_for_hotel=(
            select(RoomsOrm.id)
            .select_from(RoomsOrm)
            .filter_by(hotel_id=hotel_id)
            .subquery(name="rooms_ids_for_hotel")
        )

        rooms_ids_to_get  = (
            select(rooms_left_table.c.room_id)
            .select_from(rooms_left_table)
            .filter(rooms_left_table.c.rooms_left > 0,
                    # Подзапрос
                    rooms_left_table.c.room_id.in_(rooms_ids_for_hotel))
        )
        print(rooms_ids_to_get.compile(bind=engine, compile_kwargs={"literal_binds": True}))
        return await self.get_filtered(RoomsOrm.id.in_(rooms_ids_to_get))
''' 
select
	*
from
	rooms_left_table
where
	rooms_left>0
'''


'''
	
with room_count as (
select
	fk_booking_room_id ,
	count(*)as rooms_booked
from
	bookings
where
	date_to >= '2025-07-16'
	and date_from <= '2025-07-30'
group by
	fk_booking_room_id 
),
rooms_left_table as(
select rooms.id as room_id, quantity - coalesce(rooms_booked, 0) as rooms_left from room_count
left join rooms on room_count.fk_booking_room_id = rooms.id
)
select
	*
from
	rooms_left_table
where
	rooms_left>0
'''
