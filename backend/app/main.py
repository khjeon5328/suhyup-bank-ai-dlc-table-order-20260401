"""FastAPI application entry point."""

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded

from app.config import settings
from app.core.database import engine
from app.core.event_bus import event_bus
from app.core.exceptions import AppException, app_exception_handler, global_exception_handler
from app.core.logging_config import setup_logging
from app.core.sse_manager import sse_manager
from app.middleware.request_id import RequestIDMiddleware
from app.middleware.security_headers import SecurityHeadersMiddleware
from app.routers import auth, events, images, menus, orders, stores, tables, users


@asynccontextmanager
async def lifespan(app: FastAPI):
    setup_logging()
    yield
    await engine.dispose()


app = FastAPI(
    title="테이블오더 API",
    version="1.0.0",
    lifespan=lifespan,
)

# Middleware (outer → inner)
app.add_middleware(SecurityHeadersMiddleware)
app.add_middleware(RequestIDMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Exception handlers
app.add_exception_handler(AppException, app_exception_handler)
app.add_exception_handler(Exception, global_exception_handler)
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# Routers
app.include_router(auth.router, prefix="/api/v1/auth", tags=["auth"])
app.include_router(stores.router, prefix="/api/v1/stores", tags=["stores"])
app.include_router(tables.router, prefix="/api/v1/stores/{store_id}/tables", tags=["tables"])
app.include_router(menus.router, prefix="/api/v1/stores/{store_id}/menus", tags=["menus"])
app.include_router(orders.router, prefix="/api/v1/stores/{store_id}/orders", tags=["orders"])
app.include_router(users.router, prefix="/api/v1/stores/{store_id}/users", tags=["users"])
app.include_router(images.router, prefix="/api/v1/stores/{store_id}/images", tags=["images"])
app.include_router(events.router, prefix="/api/v1/stores/{store_id}/events", tags=["events"])


@app.get("/health")
async def health_check():
    return {"status": "ok"}
