from pydantic import BaseModel
from datetime import datetime

class HotelBase(BaseModel):
    name: str
    description: str | None = None
    country: str
    city: str
    address: str
    zip_code: str | None = None


class HotelCreate(HotelBase):
    pass


class HotelResponse(HotelBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class HotelUpdate(BaseModel):
    name: str | None = None
    description: str | None = None
    country: str | None = None
    city: str | None = None
    address: str | None = None
    zip_code: str | None = None