

from datetime import date
from fastapi import APIRouter, Body, Path, Query

from src.api.dependency import DBDep, PaginationDep
from src.sсhemas.hotel import HotelADD, HotelPATCH
from src.database import async_session_maker


router = APIRouter(prefix='/hotels', tags=["Отели"])


@router.get("")
async def get_hotels(
    pagination: PaginationDep,
    db: DBDep,
    date_from: date = Query(example="2025-07-30"),
    date_to: date = Query(example="2025-07-16"),
    title: str | None = Query(None, description="Название"),
    location: str | None = Query(None, description="Адрес"),

):

    per_page = pagination.per_page or 5
    # return await db.hotels.get_all(
    #     title=title,
    #     location=location,
    #     limit=per_page,
    #     offset=per_page*(pagination.page-1))
    return await db.hotels.get_filtered_by_time(
                                date_from=date_from, 
                                date_to=date_to,
                                title=title,location=location,
                                limit=per_page, 
                                offset=per_page*(pagination.page-1) 
                                )


@router.get("/{hotel_id}")
async def get_hotel(db: DBDep, hotel_id: int = Path(..., description="ID отеля")):
    async with async_session_maker() as session:
        return await db.hotels.get_one_or_none(id=hotel_id)


@router.post("")
async def add_hotel(db: DBDep, hotel_data: HotelADD = Body(
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
    }),

):

    hotel = await db.hotels.add(hotel_data)
    await db.commit()
    return {"status": "ОК", "data": hotel}


@router.put("{hotel_id}")
async def put_hotel(
    hotel_id: int,
    hotel_data: HotelADD,
    db: DBDep
):

    hotel = await db.hotels.edit(id=hotel_id,
                                 data=hotel_data)
    await db.commit()
    return {"status": "ОК"}


@router.delete("{hotel_id}")
async def delete_hotel(hotel_id: int,
                       db: DBDep
                       ):

    result = await db.hotels.delete(id=hotel_id)
    await db.commit()
    return {"status": "ОК"}


@router.patch("{hotel_id}")
async def path_hotel(
    hotel_id: int,
    hotel_data: HotelPATCH,
    db: DBDep
):
    result = await db.hotels.edit(id=hotel_id, exclude_unset=True,
                                  data=hotel_data)
    await db.commit()
    return {"status": "ОК"}
