from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import func, String
from datetime import datetime

from app.database.base import Base


class Service(Base):
    __tablename__ = "services"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(100))
    image_url: Mapped[str | None] = mapped_column(String(255))
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(server_default=func.now(), onupdate=func.now())

    hotel_services: Mapped[list["HotelService"]] = relationship(back_populates="service")