

from fastapi import APIRouter, Body, Query
from sqlalchemy import insert, select

from models.hotels import HotelsOrm
from src.api.dependency import PaginationDep
from src.sсhemas.hotel import Hotel, HotelPATCH
from src.database import async_session_maker
router = APIRouter(prefix='/hotels', tags=["Отели"])


hotels = [
    {"id": 1, "title": "Sochi", "name": "sochi"},
    {"id": 2, "title": "Дубай", "name": "dubai"},
    {"id": 3, "title": "Мальдивы", "name": "maldivi"},
    {"id": 4, "title": "Геленджик", "name": "gelendzhik"},
    {"id": 5, "title": "Москва", "name": "moscow"},
    {"id": 6, "title": "Казань", "name": "kazan"},
    {"id": 7, "title": "Санкт-Петербург", "name": "spb"},

]


@router.get("")
async def get_hotels(pagination: PaginationDep,):

    async with async_session_maker() as session:
        query = select(HotelsOrm)
        result = await session.execute(query)
        hotels = result.scalars().all()
        return hotels

    # start = (pagination.page*pagination.per_page)-pagination.per_page
    # end = pagination.page*pagination.per_page
    # return hotels[start:end]


@router.post("")
async def add_hotel(hotel_data: Hotel = Body(
    # Пример для отображения в документации
    openapi_examples={
        "1": {
        "summary": "Дубай",
        "value": {
            "title": 'Отель Дубай',
            "location": 'ул. Мира д.1',
        }

        },
        "2": {
        "summary": "Сочи",
        "value": {
            "title": 'Отель Сочи',
            "location": 'ул. Сочи д.15',
        }

        },
    })
):
    async with async_session_maker() as session:
        add_hotel_stmt = insert(HotelsOrm).values(**hotel_data.model_dump())
        await session.execute(add_hotel_stmt)
        await session.commit()
    return {"status": "ОК"}


@router.put("{hotel_id}")
def put_hotel(
    hotel_id: int,
    hotel_data: Hotel,
):
    global hotels
    for hotel in hotels:
        if hotel_id == hotel["id"]:
            hotel["title"] = hotel_data.title
            hotel["name"] = hotel_data.name
    return {"status": "success", "result": [hotel for hotel in hotels]}


@router.patch("{hotel_id}")
def path_hotel(
    hotel_id: int,
    hotel_data: HotelPATCH,
):
    global hotels
    for hotel in hotels:
        if hotel_id == hotel["id"]:
            if hotel_data.title:
                hotel["title"] = hotel_data.title
            if hotel_data.name:
                hotel["name"] = hotel_data.name
    return {"status": "success", "result": [hotel for hotel in hotels]}
