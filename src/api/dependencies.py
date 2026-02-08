"""FastAPI dependencies for DB session and use cases."""

from collections.abc import AsyncGenerator

from fastapi import Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession

from src.application.use_cases.user_use_case import UserUseCase
from src.infrastructure.di.container import get_user_use_case


async def get_db(request: Request) -> AsyncGenerator[AsyncSession, None]:
    """Async generator yielding AsyncSession from session_factory."""
    db = request.app.state.db
    factory = db.session_factory()
    async with factory() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise


def get_user_use_case_dep(
    session: AsyncSession = Depends(get_db),
) -> UserUseCase:
    """Instantiate user use case with session and adapters from DI container."""
    return get_user_use_case(session)
