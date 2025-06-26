

from fastapi import Body, FastAPI, Query
import uvicorn


app = FastAPI()


hotels = [
    {"id": 1, "title": "Sochi", "name": "Сочи"},
    {"id": 2, "title": "Дубай", "name": "Дубай"},
]


@app.get("/hotels")
def get_hotels():
    return [hotel for hotel in hotels]


@app.put("/hotels/{hotel_id}")
def put_hotel(
    hotel_id: int,
    title: str = Body(description="Название отеля"), 
    name: str= Body(description="Имя Отеля"),
):
    global hotels
    for hotel in hotels:
        if hotel_id == hotel["id"]:
            hotel["title"]=title
            hotel["name"]=name
        else: return {"status": "false", "result":f"hotel_id:{hotel_id} not found"}
    return {"status": "success", "result":[hotel for hotel in hotels]}

@app.patch("/hotels/{hotel_id}")
def path_hotel(
    hotel_id: int,
    title: str | None = Body(None, description="Название отеля"),
    name: str | None= Body(None,description="Имя Отеля")

):
    global hotels
    for hotel in hotels:
        if hotel_id == hotel["id"]:
            if title:
                hotel["title"]=title
            if name:
                hotel["name"]=name
        else: return {"status": "false", "result":f"hotel_id:{hotel_id} not found"}
    return {"status": "success", "result":[hotel for hotel in hotels]}



if __name__ == "__main__":
    uvicorn.run("main:app",
                reload=True)
