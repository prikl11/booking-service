from pydantic import BaseModel

from app.database.schemas.hotels import HotelResponse

class HotelImageBase(BaseModel):
    hotel_id: int


class HotelImageCreate(HotelImageBase):
    pass


class HotelImageResponse(BaseModel):
    id: int
    hotel: HotelResponse
    image_url: str

    model_config = {"from_attributes": True}
