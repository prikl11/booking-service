from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey

from app.database.base import Base


class RoomService(Base):
    __tablename__ = "room_services"

    room_id: Mapped[int] = mapped_column(ForeignKey("rooms.id"), primary_key=True, autoincrement=False)
    service_id: Mapped[int] = mapped_column(ForeignKey("services.id"), primary_key=True, autoincrement=False)

    room: Mapped["Room"] = relationship(back_populates="room_services")
    service: Mapped["Service"] = relationship(back_populates="room_services")