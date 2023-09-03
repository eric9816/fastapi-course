from datetime import date
from typing import List

from fastapi import APIRouter, Depends

from app.bookings.schemas import SBooking
from app.bookings.service import BookingService
from app.users.dependencies import get_current_user
from app.users.models import Users
from app.exceptions import BookingRoomCannotBeBooked

router = APIRouter(
    prefix="/bookings",
    tags=["Бронирования"]
)


@router.get("")
async def get_booking(user: Users = Depends(get_current_user)) -> List[SBooking]:
    return await BookingService.find_all(user_id=user.id)


@router.post("")
async def add_booking(room_id: int,
                      date_from: date,
                      date_to: date,
                      user: Users = Depends(get_current_user)):
    booking = await BookingService.add(user.id, room_id, date_from, date_to)
    if not booking:
        raise BookingRoomCannotBeBooked
