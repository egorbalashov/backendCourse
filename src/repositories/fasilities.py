

from models.facilities import FacilitiesOrm
from repositories.base import BaseRepository
from sсhemas.fasilities import Fasilities


class FasilitiesRepositories(BaseRepository):
    model=FacilitiesOrm
    schema = Fasilities

