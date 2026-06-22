from pydantic import BaseModel
from datetime import datetime
from decimal import Decimal

from app.database.schemas.hotels import HotelResponse

class RoomBase(BaseModel):
    hotel_id: int
    name: str
    description: str | None = None
    price: Decimal
    discount: Decimal | None = None
    personas: int
    is_active: bool


class RoomCreate(RoomBase):
    pass


class RoomResponse(BaseModel):
    id: int
    hotel: HotelResponse
    name: str
    description: str | None = None
    price: Decimal
    discount: Decimal | None = None
    personas: int
    is_active: bool
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class RoomUpdate(BaseModel):
    hotel_id: int | None = None
    name: str | None = None
    description: str | None = None
    price: Decimal | None = None
    discount: Decimal | None = None
    personas: int | None = None
    is_active: bool | None = None