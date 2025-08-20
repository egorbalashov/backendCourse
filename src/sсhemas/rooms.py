from pydantic import BaseModel, ConfigDict

from sсhemas.fasilities import Fasilities


class RoomsAddRequests(BaseModel):
    title: str
    description: str | None = None
    price: int
    quantity: int
    facilities_ids: list[int] = []


class RoomsADD(BaseModel):
    hotel_id: int
    title: str
    description: str | None = None
    price: int
    quantity: int


class Rooms(RoomsADD):
    id: int

    model_config = ConfigDict(from_attributes=True)


class RoomWithRels(Rooms):
    facilities: list[Fasilities]


class RoomsPatchRequests(BaseModel):
    title: str | None = None
    description: str | None = None
    price: int | None = None
    facilities_ids: list[int] = []


class RoomPatch(BaseModel):
    hotel_id: int | None = None
    title: str | None = None
    description: str | None = None
    price: int | None = None
    quantity: int | None = None
