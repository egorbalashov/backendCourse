from datetime import date
from fastapi import APIRouter, Body, Path, Query
from fastapi_cache.decorator import cache
from src.api.dependency import DBDep, PaginationDep
from src.sсhemas.hotel import HotelADD, HotelPATCH
from src.exceptions import ObjectNotFoundException, HotelNotFoundHTTPException
from src.services.hotels import HotelService

router = APIRouter(prefix="/hotels", tags=["Отели"])


@cache(expire=10)
@router.get("")
async def get_hotels(
    pagination: PaginationDep,
    db: DBDep,
    date_from: date = Query(examples="2025-07-30"),
    date_to: date = Query(examples="2025-07-16"),
    title: str | None = Query(None, description="Название"),
    location: str | None = Query(None, description="Адрес"),
):
    return await HotelService(db).get_filtered_by_time(
        pagination=pagination, date_from=date_from, date_to=date_to, title=title, location=location
    )


@router.get("/{hotel_id}")
async def get_hotel(db: DBDep, hotel_id: int = Path(..., description="ID отеля")):
    try:
        return await HotelService(db).get_hotel(hotel_id)
    except ObjectNotFoundException:
        raise HotelNotFoundHTTPException


@router.post("")
async def add_hotel(
    db: DBDep,
    hotel_data: HotelADD = Body(
        # Пример для отображения в документации
        openapi_examples={
            "1": {
                "summary": "Дубай",
                "value": {
                    "title": "Отель ПОД СОЛНЦЕМ",
                    "location": "Дубай, ул. Мира д.1",
                },
            },
            "2": {
                "summary": "Сочи",
                "value": {
                    "title": "Отель У МОРЯ",
                    "location": "Сочи, ул. Земли д.15",
                },
            },
        }
    ),
):
    hotel = await HotelService(db).add_hotel(hotel_data)
    await db.commit()
    return {"status": "ОК", "data": hotel}


@router.put("{hotel_id}")
async def put_hotel(hotel_id: int, hotel_data: HotelADD, db: DBDep):
    await HotelService(db).edit_hotel(hotel_id, hotel_data)
    await db.commit()
    return {"status": "ОК"}


@router.delete("{hotel_id}")
async def delete_hotel(hotel_id: int, db: DBDep):
    await HotelService(db).delete_hotel(hotel_id=hotel_id)
    return {"status": "ОК"}


@router.patch("{hotel_id}")
async def path_hotel(hotel_id: int, hotel_data: HotelPATCH, db: DBDep):
    await HotelService(db).edit_hotel_partially(hotel_id, hotel_data, exclude_unset=True)
    await db.commit()
    return {"status": "ОК"}
