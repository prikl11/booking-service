from pydantic import BaseModel
from datetime import datetime

class ServiceBase(BaseModel):
    name: str


class ServiceCreate(ServiceBase):
    pass


class ServiceResponse(ServiceBase):
    id: int
    image_url: str | None = None
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class ServiceUpdate(BaseModel):
    name: str | None = None