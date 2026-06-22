from pydantic import BaseModel
from datetime import datetime

class ServiceBase(BaseModel):
    name: str
    image_url: str | None = None


class ServiceCreate(ServiceBase):
    pass


class ServiceResponse(ServiceBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class ServiceUpdate(BaseModel):
    name: str | None = None
    image_url: str | None = None