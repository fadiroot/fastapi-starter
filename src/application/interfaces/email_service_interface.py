"""Email service port - abstract interface for external email service."""

from abc import ABC, abstractmethod


class IEmailService(ABC):
    """Abstract interface for sending emails."""

    @abstractmethod
    async def send_email(self, to: str, subject: str, body: str) -> bool:
        """Send an email. Returns True if successful."""
        ...
