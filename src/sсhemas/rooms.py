

from pydantic import BaseModel, ConfigDict


class RoomsAddRequests(BaseModel):
    title: str
    description: str | None = None
    price: int
    quantity: int
    fasilities_ids: list[int] | None = None


class RoomsADD(BaseModel):
    hotel_id: int
    title: str
    description: str | None = None
    price: int
    quantity: int
    fasilities_ids: list[int] | None = None


class Rooms(RoomsADD):
    id: int

    model_config = ConfigDict(from_attributes=True)


class RoomsPatchRequests(BaseModel):
    title: str | None = None
    description: str | None = None
    price: int | None = None
    quantity: int | None = None
