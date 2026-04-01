"""Tests for custom exception hierarchy."""

import pytest
from app.core.exceptions import (
    AppException,
    InvalidCredentialsException,
    OrderNotFoundException,
    PendingOrdersException,
)


class TestExceptions:
    def test_base_exception(self):
        exc = AppException()
        assert exc.status_code == 500
        assert exc.error_code == "GENERAL_INTERNAL_ERROR"

    def test_auth_exception(self):
        exc = InvalidCredentialsException()
        assert exc.status_code == 401
        assert exc.error_code == "AUTH_INVALID_CREDENTIALS"

    def test_not_found_exception(self):
        exc = OrderNotFoundException()
        assert exc.status_code == 404
        assert exc.error_code == "ORDER_NOT_FOUND"

    def test_business_rule_exception_with_details(self):
        exc = PendingOrdersException(
            message="미완료 주문 3건",
            details={"pending_count": 3},
        )
        assert exc.status_code == 422
        assert exc.details["pending_count"] == 3

    def test_custom_message(self):
        exc = AppException(message="커스텀 메시지")
        assert exc.message == "커스텀 메시지"
