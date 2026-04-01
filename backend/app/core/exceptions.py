"""Custom exception hierarchy and global exception handlers."""

from typing import Any, Dict, Optional

import structlog
from fastapi import Request
from fastapi.responses import JSONResponse

logger = structlog.get_logger()


class AppException(Exception):
    """Base application exception."""

    status_code: int = 500
    error_code: str = "GENERAL_INTERNAL_ERROR"
    message: str = "서버 내부 오류가 발생했습니다."

    def __init__(
        self,
        message: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None,
    ):
        if message:
            self.message = message
        self.details = details
        super().__init__(self.message)


# Auth exceptions
class InvalidCredentialsException(AppException):
    status_code = 401
    error_code = "AUTH_INVALID_CREDENTIALS"
    message = "잘못된 인증 정보입니다."


class TokenExpiredException(AppException):
    status_code = 401
    error_code = "AUTH_TOKEN_EXPIRED"
    message = "토큰이 만료되었습니다."


class InsufficientPermissionException(AppException):
    status_code = 403
    error_code = "AUTH_INSUFFICIENT_PERMISSION"
    message = "권한이 부족합니다."


class ForbiddenException(AppException):
    status_code = 403
    error_code = "AUTH_FORBIDDEN"
    message = "접근이 거부되었습니다."


class AccountLockedException(AppException):
    status_code = 423
    error_code = "AUTH_ACCOUNT_LOCKED"
    message = "계정이 잠겼습니다. 잠시 후 다시 시도해 주세요."


# Resource exceptions
class NotFoundException(AppException):
    status_code = 404
    error_code = "RESOURCE_NOT_FOUND"
    message = "리소스를 찾을 수 없습니다."


class OrderNotFoundException(NotFoundException):
    error_code = "ORDER_NOT_FOUND"
    message = "주문을 찾을 수 없습니다."


class MenuNotFoundException(NotFoundException):
    error_code = "MENU_NOT_FOUND"
    message = "메뉴를 찾을 수 없습니다."


class TableNotFoundException(NotFoundException):
    error_code = "TABLE_NOT_FOUND"
    message = "테이블을 찾을 수 없습니다."


class UserNotFoundException(NotFoundException):
    error_code = "USER_NOT_FOUND"
    message = "사용자를 찾을 수 없습니다."


class SessionNotFoundException(NotFoundException):
    error_code = "SESSION_NOT_FOUND"
    message = "활성 세션을 찾을 수 없습니다."


class CategoryNotFoundException(NotFoundException):
    error_code = "CATEGORY_NOT_FOUND"
    message = "카테고리를 찾을 수 없습니다."


class StoreNotFoundException(NotFoundException):
    error_code = "STORE_NOT_FOUND"
    message = "매장을 찾을 수 없습니다."


# Conflict exceptions
class ConflictException(AppException):
    status_code = 409
    error_code = "RESOURCE_CONFLICT"
    message = "리소스 충돌이 발생했습니다."


class DuplicateTableException(ConflictException):
    error_code = "TABLE_DUPLICATE"
    message = "이미 존재하는 테이블 번호입니다."


class DuplicateUserException(ConflictException):
    error_code = "USER_DUPLICATE"
    message = "이미 존재하는 사용자명입니다."


class DuplicateCategoryException(ConflictException):
    error_code = "CATEGORY_DUPLICATE"
    message = "이미 존재하는 카테고리명입니다."


# Validation exceptions
class ValidationException(AppException):
    status_code = 400
    error_code = "GENERAL_VALIDATION_ERROR"
    message = "입력값이 유효하지 않습니다."


class InvalidStatusTransitionException(ValidationException):
    error_code = "ORDER_INVALID_STATUS_TRANSITION"
    message = "허용되지 않는 상태 전이입니다."


class InvalidMenuDataException(ValidationException):
    error_code = "MENU_INVALID_DATA"
    message = "메뉴 데이터가 유효하지 않습니다."


# Business rule exceptions
class BusinessRuleException(AppException):
    status_code = 422
    error_code = "BUSINESS_RULE_VIOLATION"
    message = "비즈니스 규칙 위반입니다."


class PendingOrdersException(BusinessRuleException):
    error_code = "SESSION_PENDING_ORDERS"
    message = "미완료 주문이 존재합니다."


class LastOwnerException(BusinessRuleException):
    error_code = "USER_LAST_OWNER"
    message = "매장의 마지막 점주 계정은 삭제할 수 없습니다."


class CannotDeleteSelfException(BusinessRuleException):
    error_code = "USER_CANNOT_DELETE_SELF"
    message = "자기 자신은 삭제할 수 없습니다."


class CannotChangeOwnRoleException(BusinessRuleException):
    error_code = "USER_CANNOT_CHANGE_OWN_ROLE"
    message = "자기 자신의 역할은 변경할 수 없습니다."


class CategoryHasMenusException(BusinessRuleException):
    error_code = "CATEGORY_HAS_MENUS"
    message = "메뉴가 존재하는 카테고리는 삭제할 수 없습니다."


# Rate limit
class RateLimitException(AppException):
    status_code = 429
    error_code = "RATE_LIMIT_EXCEEDED"
    message = "요청 횟수를 초과했습니다."


# Exception handlers
async def app_exception_handler(request: Request, exc: AppException) -> JSONResponse:
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error_code": exc.error_code,
            "message": exc.message,
            "details": exc.details,
        },
    )


async def global_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    logger.error("unhandled_exception", exc_info=exc)
    return JSONResponse(
        status_code=500,
        content={
            "error_code": "GENERAL_INTERNAL_ERROR",
            "message": "서버 내부 오류가 발생했습니다.",
            "details": None,
        },
    )
