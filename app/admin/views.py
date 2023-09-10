from sqladmin import ModelView

from app.bookings.models import Bookings
from app.hotels.models import Hotels
from app.hotels.rooms.models import Rooms
from app.users.models import Users


class UsersAdmin(ModelView, model=Users):
    can_delete = False  # Нельзя в админке удалять пользователей
    column_list = [Users.id, Users.email]  # какие колонки будут на главной странице админки
    name = "Пользователь"  # Название строчки
    name_plural = "Пользователи"
    icon = "fa-solid fa-user"
    column_details_exclude_list = [Users.hashed_password]  # при нажатии на глазик в админке, появляется вкладка details
    # можно исключить из нее hashed password пользователя

class BookingsAdmin(ModelView, model=Bookings):
    column_list = [c.name for c in Bookings.__table__.c] + [Bookings.user, Bookings.room]  # какие колонки будут на главной странице админки
    name = "Бронь"  # Название строчки
    name_plural = "Брони"
    icon = "fa-solid fa-book"


class RoomsAdmin(ModelView, model=Rooms):
    column_list = [c.name for c in Rooms.__table__.c] + [Rooms.hotel, Rooms.bookings]  # какие колонки будут на главной странице админки
    name = "Номер"  # Название строчки
    name_plural = "Номера"
    icon = "fa-solid fa-bed"


class HotelsAdmin(ModelView, model=Hotels):
    column_list = [c.name for c in Hotels.__table__.c] + [Hotels.rooms]  # какие колонки будут на главной странице админки
    name = "Отель"  # Название строчки
    name_plural = "Отели"
    icon = "fa-solid fa-hotel"
