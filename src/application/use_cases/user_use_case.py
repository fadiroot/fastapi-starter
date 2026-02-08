"""User use case - orchestrates domain logic."""

from src.application.dto.user_dto import UserCreateInput, UserResponse, UserUpdateInput
from src.application.interfaces.email_service_interface import IEmailService
from src.domain.constants.error_messages import (
    USER_ALREADY_EXISTS,
    USER_NOT_FOUND,
)
from src.domain.entities.user import User
from src.domain.exceptions.domain_exceptions import (
    EntityAlreadyExistsError,
    EntityNotFoundError,
)
from src.domain.repositories.user_repository import IUserRepository


class UserUseCase:
    """Use case for user operations."""

    def __init__(
        self,
        user_repository: IUserRepository,
        email_service: IEmailService | None = None,
    ) -> None:
        self._user_repository = user_repository
        self._email_service = email_service

    async def get_user(self, user_id: str) -> UserResponse:
        """Get user by ID."""
        user = await self._user_repository.get_by_id(user_id)
        if not user:
            raise EntityNotFoundError(USER_NOT_FOUND, entity="User")
        return UserResponse(**user.to_dict())

    async def create_user(self, input_data: UserCreateInput) -> UserResponse:
        """Create a new user."""
        existing = await self._user_repository.get_by_email(input_data.email)
        if existing:
            raise EntityAlreadyExistsError(USER_ALREADY_EXISTS)

        user = await self._user_repository.create(
            email=input_data.email,
            name=input_data.name,
        )
        return UserResponse(**user.to_dict())

    async def update_user(self, user_id: str, input_data: UserUpdateInput) -> UserResponse:
        """Update an existing user."""
        user = await self._user_repository.get_by_id(user_id)
        if not user:
            raise EntityNotFoundError(USER_NOT_FOUND, entity="User")

        update_data = input_data.model_dump(exclude_unset=True)
        if not update_data:
            return UserResponse(**user.to_dict())

        if "email" in update_data:
            existing = await self._user_repository.get_by_email(update_data["email"])
            if existing and existing.id != user_id:
                raise EntityAlreadyExistsError(USER_ALREADY_EXISTS)

        updated_user = User(
            id=user.id,
            email=update_data.get("email", user.email),
            name=update_data.get("name", user.name),
            created_at=user.created_at,
            updated_at=user.updated_at,
        )
        result = await self._user_repository.update(updated_user)
        return UserResponse(**result.to_dict())

    async def delete_user(self, user_id: str) -> bool:
        """Delete a user."""
        user = await self._user_repository.get_by_id(user_id)
        if not user:
            raise EntityNotFoundError(USER_NOT_FOUND, entity="User")
        return await self._user_repository.delete(user_id)
