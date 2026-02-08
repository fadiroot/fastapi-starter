"""Email service adapter - implements IEmailService."""

import logging

from src.application.exceptions.application_exceptions import ServiceException
from src.application.interfaces.email_service_interface import IEmailService
from src.infrastructure.config.settings import Settings

logger = logging.getLogger(__name__)


class EmailAdapter(IEmailService):
    """Outbound adapter for sending emails."""

    def __init__(self, settings: Settings) -> None:
        self._settings = settings

    async def send_email(self, to: str, subject: str, body: str) -> bool:
        """Send an email. Logs in dev; integrates with real SMTP in prod."""
        try:
            logger.info("Email would be sent: to=%s, subject=%s", to, subject)
            # TODO: Integrate with SMTP/sendgrid/etc using settings
            return True
        except Exception as e:
            logger.exception("Failed to send email: %s", e)
            raise ServiceException(f"Email delivery failed: {e}") from e
