


from pydantic import BaseModel


class FasilitiesAddRequests(BaseModel):
    title:str


class Fasilities(FasilitiesAddRequests):
    id:int
     