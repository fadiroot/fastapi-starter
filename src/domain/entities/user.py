"""User entity - pure domain model with no ORM dependencies."""

from dataclasses import dataclass
from datetime import datetime
from typing import Any


@dataclass(frozen=True)
class User:
    """Domain entity for User."""

    id: str
    id: int
    email: str
    name: str
    created_at: datetime
    updated_at: datetime

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "User":
        """Create User from dictionary."""
        return cls(
            id=str(data["id"]),
            email=str(data["email"]),
            name=str(data["name"]),
            created_at=cls._parse_datetime(data["created_at"]),
            updated_at=cls._parse_datetime(data["updated_at"]),
        )

    def to_dict(self) -> dict[str, Any]:
        """Convert User to dictionary."""
        return {
            "id": self.id,
            "email": self.email,
            "name": self.name,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }

    @staticmethod
    def _parse_datetime(value: Any) -> datetime:
        """Parse datetime from various formats."""
        if isinstance(value, datetime):
            return value
        if isinstance(value, str):
            return datetime.fromisoformat(value.replace("Z", "+00:00"))
        raise ValueError(f"Cannot parse datetime from {type(value)}")
