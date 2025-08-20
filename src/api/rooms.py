from datetime import date
from fastapi import APIRouter, Body, Path, Query
from src.api.dependency import DBDep
from src.sсhemas.fasilities import RoomFasilitiesAdd
from src.sсhemas.rooms import RoomPatch, RoomsADD, RoomsAddRequests, RoomsPatchRequests


router = APIRouter(prefix="/hotels", tags=["Номера"])


@router.get("/{hotel_id}/rooms")
async def get_rooms(
    hotel_id: int,
    db: DBDep,
    date_from: date = Query(examples="2025-07-30"),
    date_to: date = Query(examples="2025-07-16"),
):
    return await db.rooms.get_filtered_by_time(hotel_id=hotel_id, date_to=date_to, date_from=date_from)


@router.get("/{hotel_id}/rooms/{room_id}")
async def get_room(hotel_id: int, room_id: int, db: DBDep):
    return await db.rooms.get_rooms_fasilitiy(id=room_id, hotel_id=hotel_id)


@router.post("/{hotel_id}/room")
async def add_rooms(
    db: DBDep,
    hotel_id: int = Path(description="ID отеля"),
    room_data: RoomsAddRequests = Body(
        openapi_examples={
            "1": {
                "summary": "Одноместный номер",
                "value": {
                    "title": "Одноместный номер",
                    "description": "Одноместный номер с кондиционером",
                    "price": 3000,
                    "quantity": 10,
                    "facilities_ids": [1, 2],
                },
            },
            "2": {
                "summary": "Двухместный номер",
                "value": {
                    "title": "Двухместный номер",
                    "description": "Двухместный номер с кондиционером",
                    "price": 8000,
                    "quantity": 15,
                    "facilities_ids": [3],
                },
            },
        }
    ),
):
    # Добавление в схему hotel_id который передается в path
    _room_data = RoomsADD(hotel_id=hotel_id, **room_data.model_dump())
    room = await db.rooms.add(data=_room_data)

    if room_data.facilities_ids:
        rooms_fasilities_date = [
            RoomFasilitiesAdd(room_id=room.id, facility_id=f_id) for f_id in room_data.facilities_ids
        ]
        await db.facilities_ids.add_bulk(rooms_fasilities_date)

    await db.commit()

    return {"status": "OK", "data": room}


@router.put("/{hotel_id}/rooms/{room_id}")
async def edit_room(
    hotel_id: int,
    room_id: int,
    room_data: RoomsAddRequests,
    db: DBDep,
):
    _room_data = RoomsADD(hotel_id=hotel_id, **room_data.model_dump())
    await db.rooms.edit(_room_data, id=room_id)
    await db.room_fasilities.set_room_facilities(room_id, facilities_ids=room_data.facilities_ids)
    await db.commit()
    return {"status": "OK"}


@router.patch("/{hotel_id}/rooms/{room_id}")
async def partially_edit_room(
    hotel_id: int,
    room_id: int,
    room_data: RoomsPatchRequests,
    db: DBDep,
):
    _room_data_dict = room_data.model_dump(exclude_unset=True)
    _room_data = RoomPatch(hotel_id=hotel_id, **_room_data_dict)
    await db.rooms.edit(_room_data, exclude_unset=True, id=room_id, hotel_id=hotel_id)
    if "facilities_ids" in _room_data_dict:
        await db.room_fasilities.set_room_facilities(room_id, facilities_ids=_room_data_dict["facilities_ids"])
    await db.commit()
    return {"status": "OK"}


@router.delete("/{hotel_id}/room/{room_id}")
async def delete_room(
    hotel_id: int,
    room_id: int,
    db: DBDep,
):
    await db.rooms.delete(id=room_id, hotel_id=hotel_id)
    await db.commit()
    return {"status": "ОК"}
