

from fastapi import APIRouter

from api.dependency import DBDep
from sсhemas.fasilities import FasilitiesAddRequests


router = APIRouter(prefix="/fasilities", tags=["Удобства"])


@router.get("")
async def all_fasilities(db: DBDep):
    fasilities = await db.fasilities.get_all()
    return {"status": "ОК", "data": fasilities}


@router.post("")
async def add_fasilities(db: DBDep,
                         title: FasilitiesAddRequests
                         ):
    room = await db.fasilities.add(data=title)
    await db.commit()

    return {"status": "OK", "data": room}
