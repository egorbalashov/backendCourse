

from pydantic import BaseModel, ConfigDict


class HotelADD(BaseModel):
    title: str
    location: str

class Hotel(HotelADD):
    id: int

    model_config=ConfigDict(from_attributes=True)


class HotelPATCH(BaseModel):
    title: str | None = None
    location: str | None = None