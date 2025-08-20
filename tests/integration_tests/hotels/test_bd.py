from src.sсhemas.hotel import HotelADD
from src.utils.db_manager import DBManager


#  Для подсвечивания синтаксиса для .hotels.add(hotel_data) .commit() нужно указать тип для db
async def test_add_hotel(db: DBManager):
    hotel_data = HotelADD(title="Hotel 5 stars", location="Сочи")
    await db.hotels.add(hotel_data)
    await db.commit()
