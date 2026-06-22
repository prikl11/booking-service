from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import func, String, Text
from datetime import datetime

from app.database.base import Base


class Hotel(Base):
    __tablename__ = "hotels"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(150))
    description: Mapped[str | None] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(server_default=func.now(), onupdate=func.now())

    staff: Mapped[list["HotelStaff"]] = relationship(back_populates="hotel")
    hotel_services: Mapped[list["HotelService"]] = relationship(back_populates="hotel")
    hotel_images: Mapped[list["HotelImage"]] = relationship(back_populates="hotel")
    rooms: Mapped[list["Room"]] = relationship(back_populates="hotel")