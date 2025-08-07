
from fastapi import APIRouter

from src.api.dependency import DBDep
from src.sсhemas.fasilities import FasilitiesAddRequests
from fastapi_cache.decorator import cache

router = APIRouter(prefix="/fasilities", tags=["Удобства"])


@router.get("")
@cache(expire=10)
async def get_facilities(db: DBDep):
    return await db.fasilities.get_all()


@router.post("")
async def add_fasilities(db: DBDep,
                         title: FasilitiesAddRequests
                         ):
    room = await db.fasilities.add(data=title)
    await db.commit()

    return {"status": "OK", "data": room}
