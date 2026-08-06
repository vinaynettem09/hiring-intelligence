"""Email platform seam.

The domain never talks to SMTP directly — it depends on the `EmailProvider` Protocol.
Local dev uses `SmtpEmailProvider` pointed at Mailhog; tests inject a fake. Swapping to
a real transactional provider later is a new implementation behind the same seam.
"""

import asyncio
import json
import smtplib
import urllib.error
import urllib.request
from dataclasses import dataclass
from email.message import EmailMessage as MimeMessage
from email.utils import parseaddr
from typing import Protocol

from app.config import get_settings

_BREVO_API_URL = "https://api.brevo.com/v3/smtp/email"


class EmailSendError(Exception):
    """A transactional email failed to send (transport error or provider rejection)."""


@dataclass(frozen=True)
class EmailMessage:
    to: str
    subject: str
    html_body: str
    text_body: str


class EmailProvider(Protocol):
    async def send(self, message: EmailMessage) -> None: ...


class SmtpEmailProvider:
    """Sends via SMTP. Local dev = Mailhog (no auth, no TLS). A real transactional provider
    (Story 9.1) sets `use_tls=True` (STARTTLS) and username/password (SMTP AUTH). smtplib is
    blocking, so it runs in a worker thread to keep the event loop free. The password is only
    ever read from settings/env and passed to `smtp.login` — never logged or stored."""

    def __init__(
        self,
        *,
        host: str,
        port: int,
        sender: str,
        username: str = "",
        password: str = "",
        use_tls: bool = False,
    ) -> None:
        self._host = host
        self._port = port
        self._sender = sender
        self._username = username
        self._password = password
        self._use_tls = use_tls

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
            if self._use_tls:
                smtp.starttls()
            if self._username:
                smtp.login(self._username, self._password)
            smtp.send_message(mime)


class BrevoApiEmailProvider:
    """Sends via Brevo's HTTPS transactional API (port 443) instead of SMTP.

    Required on hosts that block outbound SMTP (e.g. Render), where SmtpEmailProvider would
    hang on connect. The HTTP call is blocking (urllib), so it runs in a worker thread with
    an explicit timeout — it can never hang the event loop or a request. The api key is read
    from settings/env and sent only in the `api-key` header — never logged."""

    def __init__(self, *, api_key: str, sender: str, timeout: float = 15.0) -> None:
        self._api_key = api_key
        self._sender = sender  # "Display Name <addr@example.com>" or a bare address
        self._timeout = timeout

    async def send(self, message: EmailMessage) -> None:
        await asyncio.to_thread(self._send_sync, message)

    def _send_sync(self, message: EmailMessage) -> None:
        name, address = parseaddr(self._sender)
        sender: dict[str, str] = {"email": address}
        if name:
            sender["name"] = name
        payload = json.dumps(
            {
                "sender": sender,
                "to": [{"email": message.to}],
                "subject": message.subject,
                "htmlContent": message.html_body,
                "textContent": message.text_body,
            }
        ).encode("utf-8")
        request = urllib.request.Request(
            _BREVO_API_URL,
            data=payload,
            headers={
                "api-key": self._api_key,
                "content-type": "application/json",
                "accept": "application/json",
            },
            method="POST",
        )
        try:
            with urllib.request.urlopen(request, timeout=self._timeout) as response:  # noqa: S310
                if response.status not in (200, 201):
                    raise EmailSendError(f"Brevo API returned HTTP {response.status}")
        except urllib.error.HTTPError as exc:
            # Surface Brevo's reason (e.g. sender not verified) WITHOUT leaking the api key.
            detail = exc.read().decode("utf-8", "replace")[:500]
            raise EmailSendError(
                f"Brevo API rejected the send (HTTP {exc.code}): {detail}"
            ) from exc
        except urllib.error.URLError as exc:
            raise EmailSendError(f"Could not reach the Brevo API: {exc.reason}") from exc


def get_email_provider() -> EmailProvider:
    """FastAPI dependency. Constructed per request (cheap); overridable in tests. Selects the
    transport from governed config: `brevo_api` (HTTPS, for SMTP-blocked hosts) or `smtp`."""
    settings = get_settings()
    if settings.email_provider == "brevo_api":
        return BrevoApiEmailProvider(api_key=settings.brevo_api_key, sender=settings.email_from)
    return SmtpEmailProvider(
        host=settings.smtp_host,
        port=settings.smtp_port,
        sender=settings.email_from,
        username=settings.smtp_username,
        password=settings.smtp_password,
        use_tls=settings.smtp_use_tls,
    )
