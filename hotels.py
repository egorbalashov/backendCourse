

from fastapi import APIRouter

from sсhemas.hotel import Hotel, HotelPATCH

router = APIRouter(prefix='/hotels',tags=["Отели"])


hotels = [
    {"id": 1, "title": "Sochi", "name": "sochi"},
    {"id": 2, "title": "Дубай", "name": "dubai"},
    {"id": 3, "title": "Мальдивы", "name": "maldivi"},
    {"id": 4, "title": "Геленджик", "name": "gelendzhik"},
    {"id": 5, "title": "Москва", "name": "moscow"},
    {"id": 6, "title": "Казань", "name": "kazan"},
    {"id": 7, "title": "Санкт-Петербург", "name": "spb"},

]


@router.get("")
def get_hotels(page: int = 1,
               per_page: int = 3
               ):
    start = (page*per_page)-per_page
    end = page*per_page
    return hotels[start:end]


@router.post("")
def add_hotel(hotel_data: Hotel,

              ):
    hotel_id = hotels[-1]["id"]
    hotels.append(
        {"id": hotel_id+1,
         "title": hotel_data.title,
         "name": hotel_data.name, }
    )
    return {"status": "success", "result": [hotel for hotel in hotels]}


@router.put("{hotel_id}")
def put_hotel(
    hotel_id: int,
    hotel_data: Hotel,
):
    global hotels
    for hotel in hotels:
        if hotel_id == hotel["id"]:
            hotel["title"] = hotel_data.title
            hotel["name"] = hotel_data.name
    return {"status": "success", "result": [hotel for hotel in hotels]}


@router.patch("{hotel_id}")
def path_hotel(
    hotel_id: int,
    hotel_data: HotelPATCH,
):
    global hotels
    for hotel in hotels:
        if hotel_id == hotel["id"]:
            if hotel_data.title:
                hotel["title"] = hotel_data.title
            if hotel_data.name:
                hotel["name"] = hotel_data.name
    return {"status": "success", "result": [hotel for hotel in hotels]}
