from datetime import date
from pydantic import BaseModel, ConfigDict


# class Bookings(BaseModel):


class BookingsAddRequests(BaseModel):
    room_id: int
    date_to: date
    date_from: date


class BookingsAdd(BaseModel):
    room_id: int
    date_to: date
    date_from: date
    price: int
    user_id: int


class Booking(BookingsAdd):
    id: int

    model_config = ConfigDict(from_attributes=True)
