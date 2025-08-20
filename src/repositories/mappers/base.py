from typing import TypeVar

from pydantic import BaseModel

from src.database import Base


# TODO: Добавить подсветку синтаксиса для TypeVar в IDE
DBModelType = TypeVar("DBModelType", bound=Base)
SchemaType = TypeVar("SchemaType", bound=BaseModel)


class DataMapper:
    db_model: type[DBModelType] = None
    schema: type[SchemaType] = None

    # Превращает SQL модель в Pydantic схему
    @classmethod
    def map_to_domain_entity(cls, data):
        return cls.schema.model_validate(data, from_attributes=True)

    # Превращает Pydantic схему в SQL модель
    @classmethod
    def map_to_persistence_entity(cls, data):
        return cls.db_model(**data.model_dump())
