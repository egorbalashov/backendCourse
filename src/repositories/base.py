

from pydantic import BaseModel
from sqlalchemy import delete, insert, select, update
from src.repositories.mappers.base import DataMapper

class BaseRepository:
    model = None
    mapper: DataMapper = None

    def __init__(self, session):
        self.session = session

    async def get_one_or_none(self, **filter_by):
        query = select(self.model).filter_by(**filter_by)
        result = await self.session.execute(query)
        model = result.scalars().one_or_none()
        if model is None:
            return None
        return self.mapper.map_to_domain_entity(model)
    
    async def get_all(self, *args, **kwargs):
        return await self.get_filtered()

    async def get_filtered(self, *filter,**filter_by):
        query = (
            select(self.model)
            .filter(*filter)
            .filter_by(**filter_by)
        )
        result = await self.session.execute(query)
        return [self.mapper.map_to_domain_entity(model) for model in result.scalars().all()]

    

    async def add(self, data: BaseModel):
        add_data_stmt = insert(self.model).values(
            **data.model_dump()).returning(self.model)
        result = await self.session.execute(add_data_stmt)
        model = result.scalars().one()
        return self.mapper.map_to_domain_entity(model)
    
    async def add_bulk(self, data: list[BaseModel]):
        add_data_stmt = insert(self.model).values([item.model_dump() for item in data])
        await self.session.execute(add_data_stmt)


    async def edit(self, data: BaseModel, exclude_unset: bool = False, **filter_by) -> None:
        update_stmt = update(self.model).filter_by(
            # exclude_unset=True В результирующий словарь попадут только те поля, которые были ЯВНО установлены Пропускаются поля со значениями по умолчанию
            **filter_by).values(**data.model_dump(exclude_unset=exclude_unset))
        result = await self.session.execute(update_stmt)
        return

    async def delete(self, **filter_by) -> None:
        delete_stmt = delete(self.model).filter_by(**filter_by)
        result = await self.session.execute(delete_stmt)
        return

    async def delete_list(self, *filter,**filter_by):
        delete_stmt=delete(self.model).filter(*filter).filter_by(**filter_by)
 
        result = await self.session.execute(delete_stmt)