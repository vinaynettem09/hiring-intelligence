"""Password hashing tests (Story 1.1)."""

from app.shared.security import hash_password, verify_password


def test_hash_is_not_plaintext_and_verifies() -> None:
    hashed = hash_password("password123")
    assert hashed != "password123"
    assert verify_password(hashed, "password123") is True


def test_verify_rejects_wrong_password() -> None:
    hashed = hash_password("password123")
    assert verify_password(hashed, "wrong-password") is False
