from pydantic import BaseModel
from datetime import datetime

from app.database.schemas.users import UserResponse

class CartBase(BaseModel):
    user_id: int


class CartCreate(CartBase):
    pass


class CartResponse(BaseModel):
    id: int
    user: UserResponse
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}