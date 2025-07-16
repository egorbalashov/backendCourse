



from datetime import date
from pydantic import BaseModel


# class Bookings(BaseModel):

class BookingsAddRequests(BaseModel):
    room_id: int
    date_to: date
    date_from: date


class BookingsAdd(BookingsAddRequests):
    price: int

class Booking(BookingsAdd):
    user_id:int