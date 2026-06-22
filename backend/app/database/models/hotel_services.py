from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey

from app.database.base import Base


class HotelService(Base):
    __tablename__ = "hotel_services"

    hotel_id: Mapped[int] = mapped_column(ForeignKey("hotels.id"), primary_key=True, autoincrement=False)
    service_id: Mapped[int] = mapped_column(ForeignKey("services.id"), primary_key=True, autoincrement=False)

    hotel: Mapped["Hotel"] = relationship(back_populates="hotel_services")
    service: Mapped["Service"] = relationship(back_populates="hotel_services")