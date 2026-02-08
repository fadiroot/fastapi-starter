"""User API routes."""

from fastapi import APIRouter, Depends, HTTPException, status

from src.api.dependencies import get_user_use_case_dep
from src.application.dto.user_dto import UserCreateInput, UserResponse, UserUpdateInput
from src.application.use_cases.user_use_case import UserUseCase
from src.domain.exceptions.domain_exceptions import (
    EntityAlreadyExistsError,
    EntityNotFoundError,
)

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/{user_id}", response_model=UserResponse)
async def get_user(
    user_id: str,
    use_case: UserUseCase = Depends(get_user_use_case_dep),
) -> UserResponse:
    """Get user by ID."""
    try:
        return await use_case.get_user(user_id)
    except EntityNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.message)


@router.post("", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(
    input_data: UserCreateInput,
    use_case: UserUseCase = Depends(get_user_use_case_dep),
) -> UserResponse:
    """Create a new user."""
    try:
        return await use_case.create_user(input_data)
    except EntityAlreadyExistsError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=e.message)


@router.patch("/{user_id}", response_model=UserResponse)
async def update_user(
    user_id: str,
    input_data: UserUpdateInput,
    use_case: UserUseCase = Depends(get_user_use_case_dep),
) -> UserResponse:
    """Update an existing user."""
    try:
        return await use_case.update_user(user_id, input_data)
    except EntityNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.message)
    except EntityAlreadyExistsError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=e.message)


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    user_id: str,
    use_case: UserUseCase = Depends(get_user_use_case_dep),
) -> None:
    """Delete a user."""
    try:
        await use_case.delete_user(user_id)
    except EntityNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.message)
