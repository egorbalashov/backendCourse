


from pydantic import BaseModel


class FasilitiesAddRequests(BaseModel):
    title:str


class Fasilities(FasilitiesAddRequests):
    id:int
     

class RoomFasilitiesAdd(BaseModel):
    room_id: int
    facility_id :int


class RoomFasilities(RoomFasilitiesAdd):
    id:int