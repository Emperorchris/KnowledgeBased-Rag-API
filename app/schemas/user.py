from pydantic import BaseModel, EmailStr, ConfigDict
from uuid import UUID
from datetime import datetime


# Request: creating a new user
class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str


# Request: updating an existing user
class UserUpdate(BaseModel):
    name: str | None = None
    email: EmailStr | None = None


# Response: what the API returns (no password)
class UserResponse(BaseModel):
    id: UUID
    name: str
    email: str
    is_active: bool
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)



class AuthResponse(BaseModel):
    user: UserResponse
    access_token: str
    refresh_token: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class RefreshTokenRequest(BaseModel):
    refresh_token: str
