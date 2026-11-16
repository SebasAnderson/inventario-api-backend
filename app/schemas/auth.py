from pydantic import BaseModel, EmailStr, Field
from app.schemas.user import UserResponse


class LoginRequest(BaseModel):
    email: EmailStr = Field(..., examples=["admin@comicstore.com"])
    password: str = Field(..., examples=["password123"])


class TokenResponse(BaseModel):
    access_token: str = Field(..., examples=["eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."])
    token_type: str = Field("bearer", examples=["bearer"])
    user: UserResponse
