"""Dependency injection container - wires use cases with implementations."""

from sqlalchemy.ext.asyncio import AsyncSession

from src.application.interfaces.email_service_interface import IEmailService
from src.application.use_cases.user_use_case import UserUseCase
from src.infrastructure.adapters.outbound.email_adapter import EmailAdapter
from src.infrastructure.config.settings import get_settings
from src.infrastructure.database.postgresql.repositories.user_repository_impl import (
    UserRepositoryImpl,
)
from src.domain.repositories.user_repository import IUserRepository


def get_user_repository(session: AsyncSession) -> IUserRepository:
    """Factory for user repository."""
    return UserRepositoryImpl(session)


def get_email_service() -> IEmailService:
    """Factory for email service adapter."""
    return EmailAdapter(get_settings())


def get_user_use_case(session: AsyncSession) -> UserUseCase:
    """Factory for user use case with injected dependencies."""
    user_repo = get_user_repository(session)
    email_service = get_email_service()
    return UserUseCase(user_repository=user_repo, email_service=email_service)
