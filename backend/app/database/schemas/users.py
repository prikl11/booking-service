from pydantic import BaseModel, EmailStr
from datetime import datetime

class UserBase(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    phone: str
    image_url: str | None = None


class UserCreate(UserBase):
    password: str


class UserResponse(UserBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class UserUpdate(BaseModel):
    first_name: str | None = None
    last_name: str | None = None
    email: EmailStr | None = None
    phone: str | None = None
    password: str | None = None
    image_url: str | None = None
    is_admin: bool | None = None