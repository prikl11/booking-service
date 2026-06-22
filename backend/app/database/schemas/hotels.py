from pydantic import BaseModel
from datetime import datetime

class HotelBase(BaseModel):
    name: str
    description: str | None = None


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