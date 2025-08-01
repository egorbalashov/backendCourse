

from pathlib import Path
import sys
import uvicorn
from fastapi import FastAPI

sys.path.append(str(Path(__file__).parent.parent))

from src.config import settings
from src.api.hotels import router as router_hotels
from src.api.auth import router as router_auth
from src.api.rooms import router as router_rooms
from src.api.bookings import router as router_bookings
from src.api.fasilities import router as router_fasilities


app = FastAPI()
app.include_router(router_auth)
app.include_router(router_hotels)
app.include_router(router_rooms)
app.include_router(router_bookings)
app.include_router(router_fasilities)



if __name__ == "__main__":
    uvicorn.run("main:app",
                reload=True)
