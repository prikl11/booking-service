from pydantic import BaseModel, EmailStr

from app.database.schemas import UserResponse


class TokenResponse(BaseModel):
    user: UserResponse
    access_token: str
    refresh_token: str
    token_type: str