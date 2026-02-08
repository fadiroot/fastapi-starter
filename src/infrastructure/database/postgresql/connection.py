"""PostgreSQL async connection and session management."""

from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

from src.infrastructure.config.settings import Settings


class Base(DeclarativeBase):
    """SQLAlchemy declarative base."""

    pass


class PostgreSQLConnection:
    """PostgreSQL connection manager with async session factory."""

    def __init__(self, settings: Settings) -> None:
        self._settings = settings
        self._engine = None
        self._session_factory: async_sessionmaker[AsyncSession] | None = None

    async def connect(self) -> None:
        """Initialize engine and session factory."""
        self._engine = create_async_engine(
            self._settings.postgresql_url,
            echo=False,
            pool_pre_ping=True,
            pool_size=5,
            max_overflow=10,
        )
        self._session_factory = async_sessionmaker(
            self._engine,
            class_=AsyncSession,
            expire_on_commit=False,
            autocommit=False,
            autoflush=False,
        )

    async def disconnect(self) -> None:
        """Close engine and connection pool."""
        if self._engine:
            await self._engine.dispose()
            self._engine = None
            self._session_factory = None

    def session_factory(self) -> async_sessionmaker[AsyncSession]:
        """Return session factory. Must call connect() first."""
        if self._session_factory is None:
            raise RuntimeError("Database not connected. Call connect() first.")
        return self._session_factory

    async def get_session(self) -> AsyncGenerator[AsyncSession, None]:
        """Async generator yielding database sessions."""
        factory = self.session_factory()
        async with factory() as session:
            try:
                yield session
                await session.commit()
            except Exception:
                await session.rollback()
                raise
