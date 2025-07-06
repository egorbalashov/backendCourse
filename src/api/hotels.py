

from fastapi import APIRouter, Body, Query
from sqlalchemy import insert

from models.hotels import HotelsOrm
from repositories.hotels import HotelsRepository
from src.api.dependency import PaginationDep
from src.sсhemas.hotel import Hotel, HotelADD, HotelPATCH
from src.database import async_session_maker


router = APIRouter(prefix='/hotels', tags=["Отели"])


@router.get("")
async def get_hotels(pagination: PaginationDep,
                     title: str | None = Query(None, description="Название"),
                     location: str | None = Query(None, description="Адрес")
                     ):

    per_page = pagination.per_page or 5
    async with async_session_maker() as session:
        return await HotelsRepository(session).get_all(
            title=title,
            location=location,
            limit=per_page,
            offset=per_page*(pagination.page-1))

@router.get("/hotels/{hotels_id}")
async def get_hotel(hotel_id: int = Query(description='Id отеля')):
    async with async_session_maker() as session:
        return await HotelsRepository(session).get_one_or_none(id=hotel_id)
    




@router.post("")
async def add_hotel(hotel_data: HotelADD = Body(
    # Пример для отображения в документации
    openapi_examples={
        "1": {
        "summary": "Дубай",
        "value": {
            "title": 'Отель ПОД СОЛНЦЕМ',
            "location": 'Дубай, ул. Мира д.1',
        }

        },
        "2": {
        "summary": "Сочи",
        "value": {
            "title": 'Отель У МОРЯ',
            "location": 'Сочи, ул. Земли д.15',
        }

        },
    })
):
    async with async_session_maker() as session:
        result = await HotelsRepository(session).add(hotel_data)
        await session.commit()
    return {"status": "ОК", "data": result}


@router.put("{hotel_id}")
async def put_hotel(
    hotel_id: int,
    hotel_data: HotelADD,
):
    async with async_session_maker() as session:
        result = await HotelsRepository(session).edit(id=hotel_id,
                                                      data=hotel_data)
        await session.commit()
        return {"status": "ОК"}


@router.delete("{hotel_id}")
async def delete_hotel(hotel_id: int,
                       ):
    async with async_session_maker() as session:
        result = await HotelsRepository(session).delete(id=hotel_id)
        await session.commit()
        return {"status": "ОК"}


@router.patch("{hotel_id}")
async def path_hotel(
    hotel_id: int,
    hotel_data: HotelPATCH,
):
    async with async_session_maker() as session:
        result = await HotelsRepository(session).edit(id=hotel_id, exclude_unset=True,
                                                      data=hotel_data)
        await session.commit()
        return {"status": "ОК"}
