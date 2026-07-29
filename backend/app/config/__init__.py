"""Application configuration (typed settings). See settings.py.

Config lives in its own package (not scattered across shared/) because it grows
faster than expected.
"""

from app.config.settings import Settings, get_settings

__all__ = ["Settings", "get_settings"]
