from datetime import date
from typing import List

from fastapi import APIRouter
from app.hotels.service import HotelService
from app.hotels.schemas import SHotel

router = APIRouter(prefix="/hotels", tags=["Отели"])

@router.get("/{location}")
async def get_hotels(location: str, date_from: date, date_to: date) -> List[SHotel]:
    await HotelService.find_all(location, date_from, date_to)