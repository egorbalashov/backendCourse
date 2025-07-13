

from fastapi import APIRouter, Body, Path, Query

from repositories.rooms import RoomsRepository
from sсhemas.rooms import RoomsADD
from src.database import async_session_maker

router = APIRouter(prefix="/hotels", tags=["Номера"])


@router.get("/rooms/")
async def get_rooms(hotel_id: int | None = Query(
                        None, description="ID отеля"),
                    title: str | None = Query(
                        None, description="Название номера"),
                    description: str | None = Query(
                        None,  description="Описание номера"),
                    price: int | None = Query(
                        None,  description="Цена номера"),
                    quantity: int | None = Query(
                        None,  description="Количество номеров")
                    ):
    async with async_session_maker() as session:
        result = await RoomsRepository(session).get_all(
            hotel_id=hotel_id,
            title=title,
            description=description,
            price=price,
            quantity=quantity)
    return result


@router.post("/{hotel_id}")
async def add_rooms(hotel_id: int = Path(description="ID отеля"), rooms_data: RoomsADD = Body(
    openapi_examples={
        "1": {
        "summary": "Одноместный номер",
        "description": "Пример добавления номера. **hotel_id берется из пути URL!**",
        "value": {
            "hotel_id": 1,  # "Берется из пути /hotels/{hotel_id}"
            "title": "Одноместный номер",
            "description": "Одноместный номер с кондиционером",
            "price": 3000,
            "quantity": 10
        }
        },
        "2": {
        "summary": "Двухместный номер",
        "description": "Пример добавления номера. **hotel_id берется из пути URL!**",
        "value": {
            "hotel_id": 1,  # "Берется из пути /hotels/{hotel_id}"
            "title": "Двухместный номер",
            "description": "Двухместный номер с кондиционером",
            "price": 8000,
            "quantity": 15
        }
        },
    })
):
    rooms_data.hotel_id = hotel_id
    async with async_session_maker() as session:
        result = await RoomsRepository(session).add(rooms_data)
        await session.commit()
    return {"status": "ОК", "data": result}
