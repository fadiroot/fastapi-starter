"""User DTOs for request/response validation."""

from datetime import datetime

from pydantic import BaseModel, EmailStr, Field


class UserCreateInput(BaseModel):
    """Input DTO for creating a user."""

    email: EmailStr
    name: str = Field(..., min_length=1, max_length=255)


class UserUpdateInput(BaseModel):
    """Input DTO for updating a user."""

    email: EmailStr | None = None
    name: str | None = Field(None, min_length=1, max_length=255)


class UserResponse(BaseModel):
    """Response DTO for user."""

    id: str
    email: str
    name: str
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
