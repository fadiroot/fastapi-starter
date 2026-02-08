"""Domain-level exceptions."""


class DomainException(Exception):
    """Base exception for domain layer."""

    def __init__(self, message: str, code: str | None = None) -> None:
        self.message = message
        self.code = code or "DOMAIN_ERROR"
        super().__init__(self.message)


class EntityNotFoundError(DomainException):
    """Raised when an entity is not found."""

    def __init__(self, message: str, entity: str | None = None) -> None:
        self.entity = entity
        super().__init__(message, code="ENTITY_NOT_FOUND")


class EntityAlreadyExistsError(DomainException):
    """Raised when an entity already exists (e.g. duplicate email)."""

    def __init__(self, message: str) -> None:
        super().__init__(message, code="ENTITY_ALREADY_EXISTS")


class InvalidEntityError(DomainException):
    """Raised when entity validation fails."""

    def __init__(self, message: str) -> None:
        super().__init__(message, code="INVALID_ENTITY")
