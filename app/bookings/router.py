from typing import List

from fastapi import APIRouter

from app.bookings.schemas import SBooking
from app.bookings.service import BookingService

router = APIRouter(
    prefix="/bookings",
    tags=["Бронирования"]
)

@router.get("")
async def get_bookings() -> List[SBooking]:
    return await BookingService.find_all()