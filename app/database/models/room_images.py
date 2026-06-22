from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, String

from app.database.base import Base


class RoomImage(Base):
    __tablename__ = "room_images"

    id: Mapped[int] = mapped_column(primary_key=True)
    room_id: Mapped[int] = mapped_column(ForeignKey("rooms.id"))
    image_url: Mapped[str] = mapped_column(String(255))

    room: Mapped["Room"] = relationship(back_populates="room_images")