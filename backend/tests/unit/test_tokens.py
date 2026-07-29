"""Access-token claim tests (Story 1.2)."""

from app.shared.tokens import create_access_token, decode_access_token

_SECRET = "test-secret"
_ALG = "HS256"


def test_access_token_carries_only_expected_claims() -> None:
    token, expires_in = create_access_token(
        user_id="u1",
        organization_id="org1",
        role="admin",
        secret=_SECRET,
        algorithm=_ALG,
        ttl_seconds=900,
    )
    assert expires_in == 900

    claims = decode_access_token(token, secret=_SECRET, algorithm=_ALG)
    assert claims["sub"] == "u1"
    assert claims["organization_id"] == "org1"
    assert claims["role"] == "admin"
    # Exactly the intended claim set — nothing leaks (e.g. no email/name).
    assert set(claims.keys()) == {"sub", "organization_id", "role", "jti", "iat", "exp"}
