

from fastapi import APIRouter, Body, Path

from repositories.rooms import RoomsRepository
from sсhemas.rooms import RoomsADD, RoomsAddRequests, RoomsPatchRequests
from src.database import async_session_maker

router = APIRouter(prefix="/hotels", tags=["Номера"])


@router.get("/{hotel_id}/rooms")
async def get_rooms(hotel_id: int):
    async with async_session_maker() as session:
        return await RoomsRepository(session).get_filtered(hotel_id=hotel_id)


@router.get("/{hotel_id}/rooms/{room_id}")
async def get_room(hotel_id: int, room_id: int):
    async with async_session_maker() as session:
        return await RoomsRepository(session).get_one_or_none(id=room_id, hotel_id=hotel_id)


@router.post("/{hotel_id}/room")
async def add_rooms(hotel_id: int = Path(description="ID отеля"),
                    room_data: RoomsAddRequests = Body(
    openapi_examples={
        "1": {
        "summary": "Одноместный номер",
        "value": {
            "title": "Одноместный номер",
            "description": "Одноместный номер с кондиционером",
            "price": 3000,
            "quantity": 10
        }
        },
        "2": {
        "summary": "Двухместный номер",
        "value": {
            "title": "Двухместный номер",
            "description": "Двухместный номер с кондиционером",
            "price": 8000,
            "quantity": 15
        }
        },
    })
):
    # Добавление в схему hotel_id который передается в path
    _room_data = RoomsADD(hotel_id=hotel_id, **room_data.model_dump())
    async with async_session_maker() as session:
        room = await RoomsRepository(session).add(data=_room_data)
        await session.commit()

    return {"status": "OK", "data": room}


@router.put("/{hotel_id}/room/{room_id}")
async def put_room(hotel_id: int,
                   room_id: int,
                   room_data: RoomsAddRequests):
    _room_data = RoomsADD(hotel_id=hotel_id, **room_data.model_dump())
    async with async_session_maker() as session:
        room = await RoomsRepository(session).edit(data=_room_data, id=room_id)
        await session.commit()
        return {"status": "ОК", "data": room}


@router.patch("/{hotel_id}/room/{room_id}")
async def patch_room(hotel_id: int,
                     room_id: int,
                     room_data: RoomsPatchRequests):
    async with async_session_maker() as session:
        result = await RoomsRepository(session).edit(id=room_id, hotel_id=hotel_id, data=room_data, exclude_unset=True)
        await session.commit()
        return {"status": "ОК"}


@router.delete("/{hotel_id}/room/{room_id}")
async def delete_room(hotel_id: int,
                      room_id: int):
    async with async_session_maker() as session:
        result = await RoomsRepository(session).delete(id=room_id, hotel_id=hotel_id)
        await session.commit()
        return {"status": "ОК"}
