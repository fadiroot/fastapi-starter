"""Application-level exceptions."""


class ApplicationException(Exception):
    """Base exception for application layer."""

    def __init__(self, message: str, code: str | None = None) -> None:
        self.message = message
        self.code = code or "APPLICATION_ERROR"
        super().__init__(self.message)


class ServiceException(ApplicationException):
    """Raised when an external service fails."""

    def __init__(self, message: str) -> None:
        super().__init__(message, code="SERVICE_ERROR")


class ValidationException(ApplicationException):
    """Raised when input validation fails."""

    def __init__(self, message: str, errors: list | None = None) -> None:
        self.errors = errors or []
        super().__init__(message, code="VALIDATION_ERROR")
