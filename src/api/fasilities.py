from fastapi import APIRouter

from src.api.dependency import DBDep
from src.sсhemas.fasilities import FasilitiesAddRequests
from src.services.facilities import FacilityService
from fastapi_cache.decorator import cache


router = APIRouter(prefix="/fasilities", tags=["Удобства"])


@router.get("")
@cache(expire=10)
async def get_facilities(db: DBDep):
    result = await FacilityService(db).get_all()
    return result


@router.post("")
async def add_fasilities(db: DBDep, title: FasilitiesAddRequests):
    facility = await FacilityService(db).add_fasilities(title)
    await db.commit()

    return {"status": "OK", "data": facility}
