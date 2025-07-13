

from pydantic import BaseModel, ConfigDict


class RoomsADD(BaseModel):
    hotel_id: int
    title: str
    description: str| None = None
    price: int
    quantity: int

class Rooms(RoomsADD):
    id: int

    model_config=ConfigDict(from_attributes=True)