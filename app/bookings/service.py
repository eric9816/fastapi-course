from app.bookings.models import Bookings
from app.service.base import BaseService


class BookingService(BaseService):
    model = Bookings