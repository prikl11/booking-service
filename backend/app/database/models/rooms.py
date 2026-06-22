from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, ForeignKey, Text, func, Numeric
from datetime import datetime
import decimal

from app.database.base import Base


class Room(Base):
    __tablename__ = "rooms"

    id: Mapped[int] = mapped_column(primary_key=True)
    hotel_id: Mapped[int] = mapped_column(ForeignKey("hotels.id"))
    name: Mapped[str] = mapped_column(String(150))
    description: Mapped[str | None] = mapped_column(Text)
    price: Mapped[decimal.Decimal] = mapped_column(Numeric(10, 2), server_default="0")
    discount: Mapped[decimal.Decimal | None] = mapped_column(Numeric(10, 2))
    personas: Mapped[int] = mapped_column(server_default="1")
    is_active: Mapped[bool] = mapped_column(server_default="true")
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(server_default=func.now(), onupdate=func.now())

    hotel: Mapped["Hotel"] = relationship(back_populates="rooms")
    room_services: Mapped[list["RoomService"]] = relationship(back_populates="room")
    room_images: Mapped[list["RoomImage"]] = relationship(back_populates="room")
    room_beds: Mapped[list["RoomBed"]] = relationship(back_populates="room")
    bookings: Mapped[list["Booking"]] = relationship(back_populates="room")