"""Token helpers (centralized, like security.py).

Access tokens are short-lived JWTs carrying ONLY: sub, organization_id, role, jti,
iat, exp. Refresh tokens are opaque random strings — NOT JWTs — so they can be
persisted and revoked (only their SHA-256 hash is stored).
"""

import hashlib
import secrets
import time
import uuid
from typing import Any

import jwt


def create_access_token(
    *,
    user_id: str,
    organization_id: str,
    role: str,
    secret: str,
    algorithm: str,
    ttl_seconds: int,
) -> tuple[str, int]:
    """Return (token, expires_in_seconds)."""
    now = int(time.time())
    claims: dict[str, Any] = {
        "sub": user_id,
        "organization_id": organization_id,
        "role": role,
        "jti": uuid.uuid4().hex,
        "iat": now,
        "exp": now + ttl_seconds,
    }
    return jwt.encode(claims, secret, algorithm=algorithm), ttl_seconds


def decode_access_token(token: str, *, secret: str, algorithm: str) -> dict[str, Any]:
    """Decode + verify a JWT. Raises jwt.PyJWTError on invalid/expired tokens."""
    decoded: dict[str, Any] = jwt.decode(token, secret, algorithms=[algorithm])
    return decoded


def generate_opaque_token() -> str:
    """A high-entropy, URL-safe opaque token. The raw value is shown/sent once; only
    its hash is ever stored. Used for refresh tokens and candidate invitation links."""
    return secrets.token_urlsafe(32)


def hash_opaque_token(token: str) -> str:
    """SHA-256 of an opaque token — what we persist, so a raw token is never at rest."""
    return hashlib.sha256(token.encode("utf-8")).hexdigest()


# Backwards-compatible names used by the identity (refresh-token) module.
generate_refresh_token = generate_opaque_token
hash_refresh_token = hash_opaque_token
