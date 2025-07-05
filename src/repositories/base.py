

from pydantic import BaseModel
from sqlalchemy import delete, insert, select, update


class BaseRepository:
    model = None

    def __init__(self, session):
        self.session = session

    async def get_all(self, *args, **kwargs):
        query = select(self.model)
        result = await self.session.execute(query)
        return result.scalars().all()

    async def add(self, data: BaseModel):
        print(data, '-'*40)
        add_data_stmt = insert(self.model).values(
            **data.model_dump()).returning(self.model)
        result = await self.session.execute(add_data_stmt)
        return result.scalars().one()

    async def edit(self, data: BaseModel, **filter_by) -> None:
        update_stmt = update(self.model).filter_by(
            **filter_by).values(**data.model_dump())
        result = await self.session.execute(update_stmt)
        return

    async def delete(self, **filter_by) -> None:
        # print( **filter_by)
        delete_stmt = delete(self.model).filter_by(**filter_by)
        result = await self.session.execute(delete_stmt)
        return
