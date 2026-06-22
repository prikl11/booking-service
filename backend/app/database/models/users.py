from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, func
from datetime import datetime

from app.database.base import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    first_name: Mapped[str] = mapped_column(String(50))
    last_name: Mapped[str] = mapped_column(String(100))
    email: Mapped[str] = mapped_column(String(150), unique=True)
    phone: Mapped[str] = mapped_column(String(40), unique=True)
    password: Mapped[str] = mapped_column()
    image_url: Mapped[str | None] = mapped_column(String(255))
    is_admin: Mapped[bool] = mapped_column(server_default="false")
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(server_default=func.now(), onupdate=func.now())

    staff: Mapped[list["HotelStaff"]] = relationship(back_populates="user")
    carts: Mapped[list["Cart"]] = relationship(back_populates="user")