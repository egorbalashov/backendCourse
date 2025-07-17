from datetime import date
from fastapi import APIRouter, Body, Path, Query
from api.dependency import DBDep
from sсhemas.rooms import RoomsADD, RoomsAddRequests, RoomsPatchRequests


router = APIRouter(prefix="/hotels", tags=["Номера"])


@router.get("/{hotel_id}/rooms")
async def get_rooms(hotel_id: int,
                    db: DBDep,
                    date_from: date = Query(example="2025-07-30"),
                    date_to: date = Query(example="2025-07-16"),
                    ):
    return await db.rooms.get_filtered_by_time(hotel_id=hotel_id,
                                               date_to=date_to,
                                               date_from=date_from)


@router.get("/{hotel_id}/rooms/{room_id}")
async def get_room(hotel_id: int, room_id: int,
                   db: DBDep):
    return await db.rooms.get_one_or_none(id=room_id, hotel_id=hotel_id)


@router.post("/{hotel_id}/room")
async def add_rooms(db: DBDep,
                    hotel_id: int = Path(description="ID отеля"),
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

    room = await db.rooms.add(data=_room_data)
    await db.commit()

    return {"status": "OK", "data": room}


@router.put("/{hotel_id}/room/{room_id}")
async def put_room(hotel_id: int,
                   room_id: int,
                   room_data: RoomsAddRequests,
                   db: DBDep,):
    _room_data = RoomsADD(hotel_id=hotel_id, **room_data.model_dump())

    room = await db.rooms.edit(data=_room_data, id=room_id)
    await db.commit()
    return {"status": "ОК"}


@router.patch("/{hotel_id}/room/{room_id}")
async def patch_room(hotel_id: int,
                     room_id: int,
                     room_data: RoomsPatchRequests,
                     db: DBDep,):

    result = await db.rooms.edit(id=room_id, hotel_id=hotel_id, data=room_data, exclude_unset=True)
    await db.commit()
    return {"status": "ОК"}


@router.delete("/{hotel_id}/room/{room_id}")
async def delete_room(hotel_id: int,
                      room_id: int,
                      db: DBDep,):

    result = await db.rooms.delete(id=room_id, hotel_id=hotel_id)
    await db.commit()
    return {"status": "ОК"}
