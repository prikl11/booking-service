from pydantic import BaseModel

from app.database.schemas.hotels import HotelResponse
from app.database.schemas.services import ServiceResponse

class HotelServiceBase(BaseModel):
    hotel_id: int
    service_id: int


class HotelServiceCreate(HotelServiceBase):
    pass


class HotelServiceResponse(BaseModel):
    hotel: HotelResponse
    service: ServiceResponse

    model_config = {"from_attributes": True}


class HotelServiceUpdate(BaseModel):
    service_id: int | None = None