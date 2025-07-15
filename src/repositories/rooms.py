

from sqlalchemy import func, select
from models.rooms import RoomsOrm
from repositories.base import BaseRepository
from sсhemas.rooms import Rooms


class RoomsRepository(BaseRepository):
    model = RoomsOrm
    schema = Rooms

    # async def get_all(self,
    #                   hotel_id,
    #                   title,
    #                   description,
    #                   price,
    #                   quantity):
    #     query = select(self.model)
    #     if hotel_id:
    #         query = query.filter_by(hotel_id=hotel_id)
    #     if title:
    #         query = query.filter(func.lower(self.model.title).contains(title.strip().lower()))
    #     if description:
    #         query = query.filter(func.lower(self.model.description).contains(description.strip().lower()))
    #     if price:
    #         query = query.filter_by(price=price) 
    #     if quantity:
    #         query = query.filter_by(quantity=quantity) 
    #     result= await self.session.execute(query)
    #     return [self.schema.model_validate(model, from_attributes=True) for model in result.scalars().all()]

        

