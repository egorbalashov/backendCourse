

from sqlalchemy import func, select
from models.hotels import HotelsOrm
from repositories.base import BaseRepository
from sсhemas.hotel import Hotel


class HotelsRepository(BaseRepository):
    model=HotelsOrm
    schema = Hotel

    async def get_all(self,
                      title,
                      location,
                      limit,
                      offset):
        query = select(HotelsOrm)
        if location :
            query = query.filter(func.lower(HotelsOrm.location).contains(location.strip().lower()))
        if title:
            query = query.filter(func.lower(HotelsOrm.title).contains(title.strip().lower()))

        query = (query
                 .limit(limit)
                 .offset(offset)
                 )
        # print(query.compile(compile_kwargs={"literal_binds": True}))
        result = await self.session.execute(query)
        return [self.schema.model_validate(model, from_attributes=True) for model in result.scalars().all()]

    




