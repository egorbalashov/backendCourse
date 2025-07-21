

from models.facilities import FacilitiesOrm, RoomsFacilitiesOrm
from repositories.base import BaseRepository
from sсhemas.fasilities import Fasilities, RoomFasilities


class FasilitiesRepositories(BaseRepository):
    model=FacilitiesOrm
    schema = Fasilities


class RoomFasilitiesRepositories(BaseRepository):
    model=RoomsFacilitiesOrm
    schema = RoomFasilities

