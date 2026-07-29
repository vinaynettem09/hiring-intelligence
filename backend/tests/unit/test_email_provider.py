"""SmtpEmailProvider auth/TLS wiring (Story 9.1).

Mailhog (local) needs neither STARTTLS nor SMTP AUTH; a real transactional provider (Brevo,
Gmail, ...) needs both. Verified against a fake SMTP so no real network/credentials are used.
"""

import smtplib
from email.message import EmailMessage as MimeMessage
from typing import ClassVar

import pytest

from app.platform.email import EmailMessage, SmtpEmailProvider


class _FakeSMTP:
    """Records what the provider does to an SMTP connection, without touching the network."""

    instances: ClassVar[list["_FakeSMTP"]] = []

    def __init__(self, host: str, port: int) -> None:
        self.host = host
        self.port = port
        self.started_tls = False
        self.login_args: tuple[str, str] | None = None
        self.sent: list[MimeMessage] = []
        _FakeSMTP.instances.append(self)

    def __enter__(self) -> "_FakeSMTP":
        return self

    def __exit__(self, *exc: object) -> None:
        return None

    def starttls(self) -> None:
        self.started_tls = True

    def login(self, username: str, password: str) -> None:
        self.login_args = (username, password)

    def send_message(self, mime: MimeMessage) -> None:
        self.sent.append(mime)


_MSG = EmailMessage(to="candidate@example.com", subject="s", html_body="<p>h</p>", text_body="t")


@pytest.fixture(autouse=True)
def _fake_smtp(monkeypatch: pytest.MonkeyPatch) -> None:
    _FakeSMTP.instances = []
    monkeypatch.setattr(smtplib, "SMTP", _FakeSMTP)


async def test_mailhog_style_uses_no_tls_and_no_auth() -> None:
    await SmtpEmailProvider(host="localhost", port=1025, sender="x@y.z").send(_MSG)
    smtp = _FakeSMTP.instances[-1]
    assert smtp.started_tls is False
    assert smtp.login_args is None
    assert len(smtp.sent) == 1


async def test_real_provider_uses_starttls_then_login() -> None:
    await SmtpEmailProvider(
        host="smtp-relay.example.com",
        port=587,
        sender="x@y.z",
        username="apikey-user",
        password="super-secret",
        use_tls=True,
    ).send(_MSG)
    smtp = _FakeSMTP.instances[-1]
    assert smtp.started_tls is True
    assert smtp.login_args == ("apikey-user", "super-secret")
    assert len(smtp.sent) == 1
