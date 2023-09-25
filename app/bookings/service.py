from datetime import date

from sqlalchemy import and_, insert, or_, select
from sqlalchemy.sql.functions import count
from sqlalchemy.exc import SQLAlchemyError
from app.bookings.models import Bookings
from app.database import async_session_maker
from app.hotels.models import Hotels
from app.hotels.rooms.models import Rooms
from app.logger import logger
from app.service.base import BaseService


class BookingService(BaseService):
    model = Bookings

    @classmethod
    async def add(cls, user_id: int, room_id: int, date_from: date, date_to: date):
        """
        with booked_rooms as(
        select * from bookings
        where room_id = 1 and
        (date_from >= '2023-05-15' and date_from <= '2023-06-20') or
        (date_from <= '2023-05-15' and date_to > '2023-05-15')
        )

        select rooms.quantity - count(booked_rooms.room_id) from rooms
        left join booked_rooms on booked_rooms.room_id = rooms.id
        where rooms.id = 1
        group by rooms.quantity, booked_rooms.room_id
        """
        try:
            async with async_session_maker() as session:
                booked_rooms = (
                    select(Bookings)
                    .where(
                        and_(
                            Bookings.room_id == room_id,
                            or_(
                                and_(
                                    Bookings.date_from >= date_from,
                                    Bookings.date_from <= date_to,
                                ),
                                and_(
                                    Bookings.date_from <= date_from,
                                    Bookings.date_to >= date_from,
                                ),
                            ),
                        )
                    )
                    .cte("booked_rooms")
                )

                get_rooms_left = (
                    select(
                        (Rooms.quantity - count(booked_rooms.c.room_id)).label(
                            "get_rooms_left"
                        )
                    )
                    .select_from(Rooms)
                    .join(booked_rooms, booked_rooms.c.room_id == Rooms.id, isouter=True)
                    .where(Rooms.id == room_id)
                    .group_by(Rooms.quantity, booked_rooms.c.room_id)
                )
                rooms_left = await session.execute(get_rooms_left)
                rooms_left: int = rooms_left.scalar()

                if rooms_left > 0:
                    get_price = select(Rooms.price).filter_by(id=room_id)
                    price = await session.execute(get_price)
                    price: int = price.scalar()  # цена отеля за 1 день
                    add_booking = (
                        insert(Bookings)
                        .values(
                            room_id=room_id,
                            user_id=user_id,
                            date_from=date_from,
                            date_to=date_to,
                            price=price,
                        )
                        .returning(Bookings)
                    )  # вернуть строку если надо (на фронте к примеру)

                    new_booking = await session.execute(add_booking)
                    await session.commit()

                    return (
                        new_booking.scalar()
                    )  # scalar возвращает число, если БД вернуло число, но также scalar
                    # вернет строку из модели, если в returning укажем ЦЕЛИКОМ модель
                else:
                    return None

        except (SQLAlchemyError, Exception) as e:
            if isinstance(e, SQLAlchemyError):
                msg = "Database Exc"
            else:
                msg = "Unknown Exc"

            msg += ": Cannot add booking"
            extra = {
                'user_id': user_id,
                'room_id': room_id,
                'date_from': date_from,
                'date_to': date_to,
            }
            logger.error(
                msg, extra=extra, exc_info=True
            )
