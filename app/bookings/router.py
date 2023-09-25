from datetime import date
from typing import List

from fastapi import APIRouter, Depends
from pydantic import TypeAdapter

from app.bookings.schemas import SBooking
from app.bookings.service import BookingService
from app.exceptions import BookingRoomCannotBeBooked
from app.tasks.tasks import send_booking_confirmation_email
from app.users.dependencies import get_current_user
from app.users.models import Users
from fastapi_versioning import version

router = APIRouter(
    prefix="/bookings",
    tags=["Бронирования"]
)


@router.get("")
@version(1)
async def get_booking(user: Users = Depends(get_current_user)) -> List[SBooking]:
    return await BookingService.find_all(user_id=user.id)


@router.post("")
@version(1)
async def add_booking(room_id: int,
                      date_from: date,
                      date_to: date,
                      user: Users = Depends(get_current_user)):
    booking = await BookingService.add(user.id, room_id, date_from, date_to)
    booking_dict = SBooking.model_validate(booking).model_dump()
    send_booking_confirmation_email.delay(booking_dict, user.email)
    return booking_dict
    # if not booking:
    #     raise BookingRoomCannotBeBooked
