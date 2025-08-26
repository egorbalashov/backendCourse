from datetime import date
from fastapi import APIRouter, Body, Path, Query
from src.api.dependency import DBDep
from src.sсhemas.fasilities import RoomFasilitiesAdd
from src.sсhemas.rooms import RoomPatch, RoomsADD, RoomsAddRequests, RoomsPatchRequests
from src.exceptions import (
    check_date_to_after_date_from,
    ObjectNotFoundException,
    HotelNotFoundHTTPException,
    RoomNotFoundHTTPException,
)
from src.exceptions import (
    HotelNotFoundHTTPException,
    RoomNotFoundHTTPException,
    RoomNotFoundException,
    HotelNotFoundException,
)
from src.sсhemas.rooms import RoomsAddRequests, RoomsAddRequests
from src.services.rooms import RoomService


router = APIRouter(prefix="/hotels", tags=["Номера"])


@router.get("/{hotel_id}/rooms")
async def get_rooms(
    hotel_id: int,
    db: DBDep,
    date_from: date = Query(examples="2025-07-30"),
    date_to: date = Query(examples="2025-07-16"),
):
    return await RoomService(db).get_filtered_by_time(hotel_id, date_from, date_to)


@router.get("/{hotel_id}/rooms/{room_id}")
async def get_room(hotel_id: int, room_id: int, db: DBDep):
    try:
        return await RoomService(db).get_room(room_id, hotel_id=hotel_id)
    except RoomNotFoundException:
        raise RoomNotFoundHTTPException


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
    try:
        room = await RoomService(db).create_room(hotel_id, room_data)
    except HotelNotFoundException:
        raise HotelNotFoundHTTPException

    return {"status": "OK", "data": room}


@router.put("/{hotel_id}/rooms/{room_id}")
async def edit_room(
    hotel_id: int,
    room_id: int,
    room_data: RoomsAddRequests,
    db: DBDep,
):
    await RoomService(db).edit_room(hotel_id, room_id, room_data)
    return {"status": "OK"}


@router.patch("/{hotel_id}/rooms/{room_id}")
async def partially_edit_room(
    hotel_id: int,
    room_id: int,
    room_data: RoomsPatchRequests,
    db: DBDep,
):
    await RoomService(db).partially_edit_room(hotel_id, room_id, room_data)
    return {"status": "OK"}


@router.delete("/{hotel_id}/room/{room_id}")
async def delete_room(
    hotel_id: int,
    room_id: int,
    db: DBDep,
):
    await RoomService(db).delete_room(hotel_id, room_id)
    return {"status": "ОК"}
