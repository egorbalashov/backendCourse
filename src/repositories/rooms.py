

from sqlalchemy import func, select
from sqlalchemy.orm import joinedload
from src.repositories.mappers.mappers import RoomDataMapper, RoomDataWithRelsMapper
from src.models.rooms import RoomsOrm
from src.repositories.base import BaseRepository
from src.repositories.utils import rooms_ids_for_booking


from datetime import date
from src.database import engine
from sqlalchemy import func, select



class RoomsRepository(BaseRepository):
    model = RoomsOrm
    mapper = RoomDataMapper

    async def get_filtered_by_time(
            self,
            hotel_id,
            date_to: date,
            date_from: date,
    ):

        rooms_ids_to_get = rooms_ids_for_booking(
            hotel_id=hotel_id, date_to=date_to, date_from=date_from)
        # print(rooms_ids_to_get.compile(bind=engine, compile_kwargs={"literal_binds": True}))

        query = (
            select(self.model)
            .options(joinedload(self.model.facilities))
            .filter(RoomsOrm.id.in_(rooms_ids_to_get))

        )
        result = await self.session.execute(query)
        return [RoomDataWithRelsMapper.map_to_domain_entity(model) for model in result.unique().scalars().all()]

    async def get_rooms_fasilitiy(self, **filter_by):
        query = (select(self.model)
                 .options(joinedload(self.model.facilities))
                 .filter_by(**filter_by)
                 )
        result = await self.session.execute(query)
        model = result.unique().scalars().one_or_none()
        if model is None:
            return None
        return RoomDataWithRelsMapper.map_to_domain_entity(model)
