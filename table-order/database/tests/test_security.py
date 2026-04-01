"""Tests for password hashing utilities."""

from database.utils.security import hash_password, verify_password


def test_hash_password_returns_hash():
    """Test that hash_password returns a bcrypt hash."""
    hashed = hash_password("password123")
    assert hashed != "password123"
    assert hashed.startswith("$2b$")


def test_verify_password_correct():
    """Test that verify_password returns True for correct password."""
    hashed = hash_password("password123")
    assert verify_password("password123", hashed) is True


def test_verify_password_incorrect():
    """Test that verify_password returns False for incorrect password."""
    hashed = hash_password("password123")
    assert verify_password("wrongpassword", hashed) is False


def test_hash_password_unique():
    """Test that same password produces different hashes (salt)."""
    hash1 = hash_password("password123")
    hash2 = hash_password("password123")
    assert hash1 != hash2


def test_verify_pin():
    """Test hashing and verifying a 4-digit PIN."""
    pin = "1234"
    hashed = hash_password(pin)
    assert verify_password(pin, hashed) is True
    assert verify_password("5678", hashed) is False
