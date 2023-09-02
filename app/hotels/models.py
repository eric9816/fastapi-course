from sqlalchemy import JSON, ForeignKey
from sqlalchemy.orm import mapped_column, Mapped

from app.database import Base

class Hotels(Base):
    __tablename__ = "hotels"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    location: Mapped[str] = mapped_column(nullable=False)
    services: Mapped[list[str]] = mapped_column(JSON)
    rooms_quantity: Mapped[int] = mapped_column(nullable=False)
    image_id: Mapped[int]


class Rooms(Base):
    __tablename__ = "rooms"

    id: Mapped[int] = mapped_column(primary_key=True, nullable=False)
    hotel_id: Mapped[int] = mapped_column(ForeignKey("hotels.id"), nullable=False)
    name: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column(nullable=True)
    price: Mapped[int] = mapped_column( nullable=False)
    services: Mapped[list[str]] = mapped_column(JSON, nullable=True)
    quantity: Mapped[int] = mapped_column(nullable=False)
    image_id: Mapped[int]

# old_alchemy

# class Hotels(Base):
#     __tablename__ = "hotels"
#
#     id = Column(Integer, primary_key=True)
#     name = Column(String, nullable=False)
#     location = Column(String, nullable=False)
#     services = Column(JSON)
#     rooms_quantity = Column(Integer, nullable=False)
#     image_id = Column(Integer)
#
#
# class Rooms(Base):
#     __tablename__ = "rooms"
#
#     id = Column(Integer, primary_key=True, nullable=False)
#     hotel_id = Column(ForeignKey("hotels.id"), nullable=False)
#     name = Column(String, nullable=False)
#     description = Column(String, nullable=True)
#     price = Column(Integer, nullable=False)
#     services = Column(JSON, nullable=True)
#     quantity = Column(Integer, nullable=False)
#     image_id = Column(Integer)
