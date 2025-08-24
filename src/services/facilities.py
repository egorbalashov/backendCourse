from src.sсhemas.fasilities import FasilitiesAddRequests
from src.services.base import BaseService
from src.tasks.tasks import test_task
from sсhemas.fasilities import FasilitiesAddRequests


class FacilityService(BaseService):
    async def add_fasilities(self, data: FasilitiesAddRequests):
        facility = await self.db.fasilities.add(data)
        await self.db.commit()

        # test_task.delay()  # type: ignore
        return facility