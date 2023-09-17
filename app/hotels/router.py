import time
from datetime import date, datetime, timedelta
from typing import List, Optional

from fastapi import APIRouter, Query
from fastapi_cache.decorator import cache

#from app.exceptions import CannotBookHotelForLongPeriod, DateFromCannotBeAfterDateTo

from app.hotels.service import HotelService
from app.hotels.schemas import SHotel, SHotelInfo

router = APIRouter(prefix="/hotels", tags=["Отели"])


@router.get("/{location}")
@cache(expire=30)
async def get_hotels_by_location_and_time(
    location: str,
    date_from: date = Query(..., description=f"Например, {datetime.now().date()}"),
    date_to: date = Query(..., description=f"Например, {(datetime.now() + timedelta(days=14)).date()}"),
) -> List[SHotelInfo]:
    # if date_from > date_to:
    #     raise DateFromCannotBeAfterDateTo
    # if (date_to - date_from).days > 31:
    #     raise CannotBookHotelForLongPeriod
    time.sleep(3)
    hotels = await HotelService.find_all(location, date_from, date_to)
    return hotels


@router.get("/id/{hotel_id}", include_in_schema=True)
# Этот эндпоинт используется для фронтенда, когда мы хотим отобразить все
# номера в отеле и информацию о самом отеле. Этот эндпоинт как раз отвечает за информацию
# об отеле.
# В нем нарушается правило именования эндпоинтов: конечно же, /id/ здесь избыточен.
# Тем не менее, он используется, так как эндпоинтом ранее мы уже задали получение
# отелей по их локации вместо id.
async def get_hotel_by_id(
    hotel_id: int,
) -> Optional[SHotel]:
    return await HotelService.find_one_or_none(id=hotel_id)


from sqlalchemy import select
from sqlalchemy.orm import selectinload, joinedload
from app.hotels.models import Hotels
from app.hotels.rooms.models import Rooms
from app.bookings.models import Bookings
from app.database import async_session_maker
from fastapi.encoders import jsonable_encoder

@router.get("/example/no_orm")
async def get_noorm():
    async with async_session_maker() as session:
        query = (
            select(
                Rooms.__table__.columns,
                Hotels.__table__.columns,
                Bookings.__table__.columns
            )
            .join(Hotels, Rooms.hotel_id == Hotels.id)
            .join(Bookings, Bookings.room_id == Rooms.id)
        )
        res = await session.execute(query)
        res = res.mappings().all()
        return res


# ИСПОЛЬЗУЯ RELATIONSHIPS
@router.get("/example/orm")
async def get_noorm():
    async with async_session_maker() as session:
        query = (
            select(Rooms)
            .options(joinedload(Rooms.hotel))
            .options(selectinload(Rooms.bookings))
        )
        res = await session.execute(query)
        res = res.scalars().all()
        res = jsonable_encoder(res)
        return res

