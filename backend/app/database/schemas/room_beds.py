from pydantic import BaseModel

from app.database.schemas.rooms import RoomResponse
from app.database.models.room_beds import BedType

class RoomBedBase(BaseModel):
    room_id: int
    bed_type: BedType
    quantity: int


class RoomBedCreate(RoomBedBase):
    pass


class RoomBedResponse(BaseModel):
    id: int
    room: RoomResponse
    bed_type: BedType
    quantity: int

    model_config = {"from_attributes": True}


class RoomBedUpdate(BaseModel):
    bed_type: BedType | None = None
    quantity: int | None = None