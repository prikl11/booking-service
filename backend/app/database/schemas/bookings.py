from pydantic import BaseModel
from datetime import datetime
import decimal

from app.database.schemas.cart import CartResponse
from app.database.schemas.rooms import RoomResponse
from app.database.models.bookings import Status

class BookingBase(BaseModel):
    room_id: int
    people_quantity: int
    comments: str | None = None
    arrival_date: datetime
    departure_date: datetime


class BookingCreate(BookingBase):
    pass


class BookingResponse(BaseModel):
    id: int
    cart: CartResponse
    room: RoomResponse
    total_price: decimal.Decimal
    people_quantity: int
    status: Status
    comments: str | None = None
    arrival_date: datetime
    departure_date: datetime
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class BookingUpdate(BaseModel):
    room_id: int | None = None
    status: Status | None = None
    comments: str | None = None
    arrival_date: datetime | None = None
    departure_date: datetime | None = None