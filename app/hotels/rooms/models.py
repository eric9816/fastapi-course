from typing import Optional

from sqlalchemy import JSON, ForeignKey
from sqlalchemy.orm import mapped_column, Mapped, relationship

from app.database import Base

class Rooms(Base):
    __tablename__ = "rooms"

    id: Mapped[int] = mapped_column(primary_key=True)
    hotel_id: Mapped[int] = mapped_column(ForeignKey("hotels.id"))
    name: Mapped[str]
    description: Mapped[Optional[str]]
    price: Mapped[int]
    services: Mapped[list[str]] = mapped_column(JSON)
    quantity: Mapped[int]
    image_id: Mapped[int]

    hotel: Mapped["Hotels"] = relationship(back_populates="rooms")
    bookings = relationship("Bookings", back_populates="room")

    def __str__(self):
        return f"Комната {self.description}"