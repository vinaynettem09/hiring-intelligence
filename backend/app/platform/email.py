"""Email platform seam.

The domain never talks to SMTP directly — it depends on the `EmailProvider` Protocol.
Local dev uses `SmtpEmailProvider` pointed at Mailhog; tests inject a fake. Swapping to
a real transactional provider later is a new implementation behind the same seam.
"""

import asyncio
import smtplib
from dataclasses import dataclass
from email.message import EmailMessage as MimeMessage
from typing import Protocol

from app.config import get_settings


@dataclass(frozen=True)
class EmailMessage:
    to: str
    subject: str
    html_body: str
    text_body: str


class EmailProvider(Protocol):
    async def send(self, message: EmailMessage) -> None: ...


class SmtpEmailProvider:
    """Sends via SMTP (Mailhog in local dev). smtplib is blocking, so it runs in a
    worker thread to keep the event loop free."""

    def __init__(self, *, host: str, port: int, sender: str) -> None:
        self._host = host
        self._port = port
        self._sender = sender

    async def send(self, message: EmailMessage) -> None:
        await asyncio.to_thread(self._send_sync, message)

    def _send_sync(self, message: EmailMessage) -> None:
        mime = MimeMessage()
        mime["From"] = self._sender
        mime["To"] = message.to
        mime["Subject"] = message.subject
        mime.set_content(message.text_body)
        mime.add_alternative(message.html_body, subtype="html")
        with smtplib.SMTP(self._host, self._port) as smtp:
            smtp.send_message(mime)


def get_email_provider() -> EmailProvider:
    """FastAPI dependency. Constructed per request (cheap); overridable in tests."""
    settings = get_settings()
    return SmtpEmailProvider(
        host=settings.smtp_host, port=settings.smtp_port, sender=settings.email_from
    )
