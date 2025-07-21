

from sqlalchemy import func, select
from sqlalchemy.orm import joinedload
from models.rooms import RoomsOrm
from repositories.base import BaseRepository
from repositories.utils import rooms_ids_for_booking
from sсhemas.rooms import RoomWithRels, Rooms

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

        rooms_ids_to_get = rooms_ids_for_booking(hotel_id=hotel_id, date_to=date_to, date_from=date_from)
        # print(rooms_ids_to_get.compile(bind=engine, compile_kwargs={"literal_binds": True}))

        query = (
            select(self.model)
            .options(joinedload(self.model.facilities))
            .filter(RoomsOrm.id.in_(rooms_ids_to_get))
            
        )
        result = await self.session.execute(query)
        return [RoomWithRels.model_validate(model, from_attributes=True) for model in result.unique().scalars().all()]