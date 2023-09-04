from datetime import date

from sqlalchemy import select, and_, or_, insert
from sqlalchemy.sql.functions import count

from app.hotels.rooms.models import Rooms
from app.database import async_session_maker
from app.hotels.rooms.models import Rooms
from app.service.base import BaseService


class RoomService(BaseService):
    model = Rooms