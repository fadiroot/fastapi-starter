"""PostgreSQL implementation of User repository."""

from datetime import datetime, timezone
from uuid import uuid4

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.entities.user import User
from src.domain.repositories.user_repository import IUserRepository


class UserRepositoryImpl(IUserRepository):
    """PostgreSQL implementation of IUserRepository."""

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    def _row_to_user(self, row: dict) -> User:
        """Map database row to User entity."""
        return User.from_dict(row)

    async def get_by_id(self, user_id: str) -> User | None:
        """Get user by ID."""
        result = await self._session.execute(
            text("SELECT id, email, name, created_at, updated_at FROM users WHERE id = :id"),
            {"id": user_id},
        )
        row = result.mappings().first()
        if not row:
            return None
        return self._row_to_user(dict(row))

    async def get_by_email(self, email: str) -> User | None:
        """Get user by email."""
        result = await self._session.execute(
            text("SELECT id, email, name, created_at, updated_at FROM users WHERE email = :email"),
            {"email": email},
        )
        row = result.mappings().first()
        if not row:
            return None
        return self._row_to_user(dict(row))

    async def create(self, email: str, name: str) -> User:
        """Create a new user."""
        now = datetime.now(timezone.utc)
        user_id = str(uuid4())
        await self._session.execute(
            text("""
                INSERT INTO users (id, email, name, created_at, updated_at)
                VALUES (:id, :email, :name, :created_at, :updated_at)
            """),
            {
                "id": user_id,
                "email": email,
                "name": name,
                "created_at": now,
                "updated_at": now,
            },
        )
        return User(
            id=user_id,
            email=email,
            name=name,
            created_at=now,
            updated_at=now,
        )

    async def update(self, user: User) -> User:
        """Update an existing user."""
        now = datetime.now(timezone.utc)
        await self._session.execute(
            text("""
                UPDATE users
                SET email = :email, name = :name, updated_at = :updated_at
                WHERE id = :id
            """),
            {
                "id": user.id,
                "email": user.email,
                "name": user.name,
                "updated_at": now,
            },
        )
        return User(
            id=user.id,
            email=user.email,
            name=user.name,
            created_at=user.created_at,
            updated_at=now,
        )

    async def delete(self, user_id: str) -> bool:
        """Delete a user by ID."""
        result = await self._session.execute(
            text("DELETE FROM users WHERE id = :id"),
            {"id": user_id},
        )
        return result.rowcount > 0
