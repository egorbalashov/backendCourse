

from fastapi import APIRouter, Body, Query
from sqlalchemy import insert

from models.hotels import HotelsOrm
from repositories.hotels import HotelsRepository
from src.api.dependency import PaginationDep
from src.sсhemas.hotel import Hotel, HotelPATCH
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


@router.post("")
async def add_hotel(hotel_data: Hotel = Body(
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
