

from pydantic import BaseModel


class HotelADD(BaseModel):
    title: str
    location: str

class Hotel(HotelADD):
    id: int


class HotelPATCH(BaseModel):
    title: str | None = None
    location: str | None = None