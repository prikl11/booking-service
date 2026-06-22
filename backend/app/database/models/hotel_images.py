from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, String

from app.database.base import Base


class HotelImage(Base):
    __tablename__ = "hotel_images"

    id: Mapped[int] = mapped_column(primary_key=True)
    hotel_id: Mapped[int] = mapped_column(ForeignKey("hotels.id"))
    image_url: Mapped[str] = mapped_column(String(255))

    hotel: Mapped["Hotel"] = relationship(back_populates="hotel_images")