from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, Numeric, Enum, Text, TIMESTAMP, func
from datetime import datetime
from decimal import Decimal
import enum

from app.database.base import Base


class Status(enum.Enum):
    pending = "pending"
    booked = "booked"
    canceled = "canceled"
    done = "done"


class Booking(Base):
    __tablename__ = "bookings"

    id: Mapped[int] = mapped_column(primary_key=True)
    cart_id: Mapped[int] = mapped_column(ForeignKey("carts.id"))
    room_id: Mapped[int] = mapped_column(ForeignKey("rooms.id"))
    total_price: Mapped[Decimal] = mapped_column(Numeric(10, 2))
    people_quantity: Mapped[int] = mapped_column(server_default="1")
    status: Mapped[Status] = mapped_column(Enum(Status), server_default="pending")
    comments: Mapped[str | None] = mapped_column(Text)
    arrival_date: Mapped[datetime] = mapped_column(TIMESTAMP)
    departure_date: Mapped[datetime] = mapped_column(TIMESTAMP)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(server_default=func.now(), onupdate=func.now())

    cart: Mapped["Cart"] = relationship(back_populates="bookings")
    room: Mapped["Room"] = relationship(back_populates="bookings")