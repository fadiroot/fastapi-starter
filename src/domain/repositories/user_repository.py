"""User repository port - abstract interface for persistence."""

from abc import ABC, abstractmethod

from src.domain.entities.user import User


class IUserRepository(ABC):
    """Abstract repository for User persistence operations."""

    @abstractmethod
    async def get_by_id(self, user_id: str) -> User | None:
        """Get user by ID."""
        ...

    @abstractmethod
    async def get_by_email(self, email: str) -> User | None:
        """Get user by email."""
        ...

    @abstractmethod
    async def create(self, email: str, name: str) -> User:
        """Create a new user."""
        ...

    @abstractmethod
    async def update(self, user: User) -> User:
        """Update an existing user."""
        ...

    @abstractmethod
    async def delete(self, user_id: str) -> bool:
        """Delete a user by ID."""
        ...
