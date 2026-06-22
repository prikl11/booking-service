from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Enum, ForeignKey
import enum

from app.database.base import Base


class Role(enum.Enum):
    owner = "owner"
    manager = "manager"
    administrator = "administrator"


class HotelStaff(Base):
    __tablename__ = "hotel_staff"

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), primary_key=True, autoincrement=False)
    hotel_id: Mapped[int] = mapped_column(ForeignKey("hotels.id"), primary_key=True, autoincrement=False)
    role: Mapped[Role] = mapped_column(Enum(Role))

    user: Mapped["User"] = relationship(back_populates="staff")
    hotel: Mapped["Hotel"] = relationship(back_populates="staff")