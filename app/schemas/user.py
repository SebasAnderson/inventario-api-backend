from datetime import datetime, timezone
from typing import Optional
from pydantic import BaseModel, EmailStr, Field, ConfigDict
from app.schemas.common import UserRole


class UserBase(BaseModel):
    email: EmailStr = Field(..., examples=["usuario@ejemplo.com"])
    rol: UserRole = Field(UserRole.CLIENTE, examples=[UserRole.CLIENTE])
    activo: bool = Field(True, examples=[True])


class UserCreate(UserBase):
    password: str = Field(..., min_length=6, max_length=100, examples=["contraseñaSegura123"])


class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    rol: Optional[UserRole] = None
    activo: Optional[bool] = None
    password: Optional[str] = Field(None, min_length=6, max_length=100)


class UserResponse(UserBase):
    id: int = Field(..., examples=[1])
    fecha_creacion: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    model_config = ConfigDict(from_attributes=True)

