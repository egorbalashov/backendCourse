

from datetime import date
from sqlalchemy import func, select
from src.models.hotels import HotelsOrm
from src.models.rooms import RoomsOrm
from src.repositories.base import BaseRepository
from src.repositories.utils import rooms_ids_for_booking
from src.repositories.mappers.mappers import HotelDataMapper


class HotelsRepository(BaseRepository):
    model=HotelsOrm
    mapper = HotelDataMapper

    # async def get_all(self,
    #                   title,
    #                   location,
    #                   limit,
    #                   offset):
    #     query = select(HotelsOrm)
    #     if location :
    #         query = query.filter(func.lower(HotelsOrm.location).contains(location.strip().lower()))
       

    #     query = (query
    #              .limit(limit)
    #              .offset(offset)
    #              )
    #     # print(query.compile(compile_kwargs={"literal_binds": True}))
    #     result = await self.session.execute(query)
    #     return [self.schema.model_validate(model, from_attributes=True) for model in result.scalars().all()]
    
    async def get_filtered_by_time(
            self,
            date_to: date,
            date_from: date,
            title,
            location,
            limit,
            offset

    ):
        rooms_ids_to_get = rooms_ids_for_booking(date_from=date_from, date_to=date_to)
        hotel_ids_to_get = (
            select(RoomsOrm.hotel_id)
            .select_from(RoomsOrm)
            .filter(RoomsOrm.id.in_(rooms_ids_to_get))
            )
        if location :
            hotel_ids_to_get= (
                hotel_ids_to_get.filter(func.lower(HotelsOrm.location).contains(location.strip().lower()))
            )
        if title:
            hotel_ids_to_get = hotel_ids_to_get.filter(func.lower(HotelsOrm.title).contains(title.strip().lower()))
        hotel_ids_to_get = (
            hotel_ids_to_get
                .limit(limit)
                .offset(offset)
        )
        return await self.get_filtered(HotelsOrm.id.in_(hotel_ids_to_get))
    



    




