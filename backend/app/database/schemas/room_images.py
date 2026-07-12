from pydantic import BaseModel

from app.database.schemas.rooms import RoomResponse

class RoomImageBase(BaseModel):
    room_id: int


class RoomImageCreate(RoomImageBase):
    pass


class RoomImageResponse(BaseModel):
    id: int
    room: RoomResponse
    image_url: str

    model_config = {"from_attributes": True}
