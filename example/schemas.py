"""Pydantic schemas for the User model."""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr


class UserInput(BaseModel):
    """Schema for creating a new user."""

    username: str
    email: EmailStr
    full_name: Optional[str] = None
    bio: Optional[str] = None
    is_active: bool = True


class UserUpdateInput(BaseModel):
    """Schema for updating a user."""

    username: Optional[str] = None
    email: Optional[EmailStr] = None
    full_name: Optional[str] = None
    bio: Optional[str] = None
    is_active: Optional[bool] = None


class UserFilter(BaseModel):
    """Schema for filtering users."""

    username: Optional[str] = None
    email: Optional[EmailStr] = None
    is_active: Optional[bool] = None


class UserOutput(BaseModel):
    """Schema for reading a user."""

    id: int
    username: str
    email: str
    full_name: Optional[str] = None
    bio: Optional[str] = None
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True
