"""Settings tests."""

from app.config import Settings, get_settings


def test_get_settings_returns_settings() -> None:
    settings = get_settings()
    assert isinstance(settings, Settings)
    assert settings.app_env  # default "local"


def test_get_settings_is_cached() -> None:
    # Same instance each call — one shared config, no global variable.
    assert get_settings() is get_settings()
