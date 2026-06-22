from pydantic import BaseModel

from app.database.schemas.hotels import HotelResponse

class HotelImageBase(BaseModel):
    hotel_id: int
    image_url: str


class HotelImageCreate(HotelImageBase):
    pass


class HotelImageResponse(BaseModel):
    id: int
    hotel: HotelResponse
    image_url: str

    model_config = {"from_attributes": True}


class HotelImageUpdate(BaseModel):
    image_url: str | None = None