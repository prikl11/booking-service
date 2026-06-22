from pydantic import BaseModel

from app.database.schemas.users import UserResponse
from app.database.schemas.hotels import HotelResponse
from app.database.models.hotel_staff import Role

class HotelStaffBase(BaseModel):
    user_id: int
    hotel_id: int
    role: Role


class HotelStaffCreate(HotelStaffBase):
    pass


class HotelStaffResponse(BaseModel):
    user: UserResponse
    hotel: HotelResponse
    role: Role

    model_config = {"from_attributes": True}


class HotelStaffUpdate(BaseModel):
    role: Role | None = None