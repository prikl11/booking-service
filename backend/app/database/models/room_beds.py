from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, Enum
import enum

from app.database.base import Base


class BedType(enum.Enum):
    single = "single"
    double = "double"
    bunk = "bunk"


class RoomBed(Base):
    __tablename__ = "room_beds"

    id: Mapped[int] = mapped_column(primary_key=True)
    room_id: Mapped[int] = mapped_column(ForeignKey("rooms.id"))
    bed_type: Mapped[BedType] = mapped_column(Enum(BedType))
    quantity: Mapped[int] = mapped_column(server_default="1")

    room: Mapped["Room"] = relationship(back_populates="room_beds")