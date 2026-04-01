"""Tests for JWT and password utilities."""

import pytest
from app.core.security import create_access_token, decode_access_token, hash_password, verify_password


class TestPasswordHashing:
    def test_hash_and_verify(self):
        password = "test_password_123"
        hashed = hash_password(password)
        assert hashed != password
        assert verify_password(password, hashed) is True

    def test_wrong_password(self):
        hashed = hash_password("correct_password")
        assert verify_password("wrong_password", hashed) is False


class TestJWT:
    def test_create_and_decode(self):
        data = {"user_id": 1, "store_id": 1, "role": "owner"}
        token = create_access_token(data=data)
        payload = decode_access_token(token)
        assert payload["user_id"] == 1
        assert payload["store_id"] == 1
        assert payload["role"] == "owner"

    def test_token_with_expiry(self):
        from datetime import timedelta
        data = {"user_id": 1, "store_id": 1, "role": "owner"}
        token = create_access_token(data=data, expires_delta=timedelta(hours=16))
        payload = decode_access_token(token)
        assert "exp" in payload
