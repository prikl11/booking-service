from pydantic import BaseModel

from app.database.schemas.rooms import RoomResponse
from app.database.schemas.services import ServiceResponse

class RoomServiceBase(BaseModel):
    room_id: int
    service_id: int


class RoomServiceCreate(RoomServiceBase):
    pass


class RoomServiceResponse(BaseModel):
    room: RoomResponse
    service: ServiceResponse

    model_config = {"from_attributes": True}


class RoomServiceUpdate(BaseModel):
    service_id: int | None = None