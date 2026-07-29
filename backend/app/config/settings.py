"""Typed application settings.

No module-level singleton: settings are obtained via `get_settings()` (cached),
so they are injectable (`Depends(get_settings)`) and overridable in tests.
Do NOT write `settings = Settings()` at import time anywhere.
"""

from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Environment-driven configuration.

    Values come from environment variables (and an optional `.env` in the process
    working directory). Field names map case-insensitively to env vars, so
    `APP_ENV` populates `app_env`. New settings are added as their story lands.
    """

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        frozen=True,  # config never mutates after startup
    )

    app_env: str = "local"
    # Local default points at the docker-compose Postgres; overridden by env in prod/docker.
    database_url: str = "postgresql+asyncpg://app:app@localhost:5432/hiring"  # Story 0.4

    # Auth (Story 1.2). jwt_secret MUST be overridden in prod (see TD-005).
    jwt_secret: str = "dev-insecure-secret-change-in-production"  # noqa: S105  dev default; TD-005
    jwt_algorithm: str = "HS256"
    access_token_ttl_seconds: int = 900  # 15 minutes
    refresh_token_ttl_seconds: int = 1_209_600  # 14 days

    # Candidate invitations (Story 4.1).
    frontend_base_url: str = "http://localhost:3000"  # candidate links point here
    invitation_ttl_seconds: int = 1_209_600  # 14 days

    # Email (Story 4.1). Local dev delivers to Mailhog (see infra/docker-compose):
    # no auth, no TLS. A real transactional provider (Story 9.1) sets username/password
    # and smtp_use_tls=True. Credentials come only from the environment — never committed.
    smtp_host: str = "localhost"
    smtp_port: int = 1025
    smtp_username: str = ""  # set for a real provider (e.g. Brevo); empty = no SMTP AUTH
    smtp_password: str = ""  # empty default; real value only via env (secret)
    smtp_use_tls: bool = False  # True = STARTTLS (real providers); False = Mailhog
    email_from: str = "Hiring Intelligence <no-reply@hiring.local>"

    # AI evaluation (Story 5.1/5.3). Default `mock` = deterministic in-process provider
    # (no network, no cost); `anthropic` = the real adapter, which requires explicit config
    # (an API key) and never silently falls back to mock.
    ai_provider: str = "mock"
    # Honesty floor: if platform-computed confidence is below this, the exposed proposal
    # is forced to ESCALATE regardless of what the provider proposed. One governed knob —
    # never hard-coded across the pipeline.
    evaluation_confidence_floor: float = 0.5

    # Anthropic provider (Story 5.3). Used ONLY when ai_provider == "anthropic".
    # The API key comes only from the environment — never committed/logged/persisted.
    anthropic_api_key: str = ""
    # Deliberate MVP default: a mid-tier model (good reasoning + structured output at
    # reasonable latency/cost); not the largest/most expensive. Recorded exactly in
    # provenance. Compare models later via the synthetic fixture harness.
    anthropic_model: str = "claude-sonnet-5"
    anthropic_max_tokens: int = 2048
    anthropic_timeout_seconds: float = 60.0
    anthropic_max_retries: int = 2  # SDK-managed → up to 3 attempts total per request

    # Gemini provider (Story 5.3 provider-portability). Used ONLY when ai_provider=="gemini".
    # ⚠️ The Gemini FREE TIER may use submitted data to improve Google's products — so this
    # provider is for our SYNTHETIC A-G fixtures only, never real candidate Evidence (TD-017).
    # Key comes only from the environment — never committed/logged/persisted.
    gemini_api_key: str = ""
    # A current free-tier Flash-family model (verified 2026-07-28); exact id in provenance.
    # Configurable — Gemini is a provider under test, NOT a permanent default.
    gemini_model: str = "gemini-3.6-flash"
    gemini_timeout_seconds: float = 60.0


@lru_cache
def get_settings() -> Settings:
    """Return the (cached) application settings.

    Cached so the whole app shares one instance without a global variable.
    Tests can override the FastAPI dependency or call `get_settings.cache_clear()`.
    """
    return Settings()
