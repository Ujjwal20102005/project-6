#!/usr/bin/env python3
"""Enterprise E-Commerce Platform - Main Application (v1.0.0, MIT)."""
import logging
import os
from datetime import datetime, timezone

import uvicorn
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from pathlib import Path

from fastapi.responses import FileResponse, JSONResponse, Response
from prometheus_client import CONTENT_TYPE_LATEST, generate_latest

from src.api.routes import router
from src.config.settings import settings
from src.core.database import Base, engine
from src.middleware.middleware import LoggingMiddleware, RateLimitMiddleware
from src.models import models  # noqa: F401  (register tables)
from src.services.services import ServiceError

os.makedirs("logs", exist_ok=True)
logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
                    handlers=[logging.FileHandler("logs/app.log"), logging.StreamHandler()])

app = FastAPI(
    title="Enterprise E-Commerce Platform",
    description="Production-ready e-commerce API built with FastAPI",
    version="1.0.0",
    docs_url="/docs" if settings.DEBUG else None,
    redoc_url="/redoc" if settings.DEBUG else None,
    openapi_url="/openapi.json" if settings.DEBUG else None,
)
app.add_middleware(CORSMiddleware, allow_origins=settings.ALLOWED_ORIGINS, allow_credentials=True,
                   allow_methods=["*"], allow_headers=["*"])
app.add_middleware(TrustedHostMiddleware, allowed_hosts=settings.ALLOWED_HOSTS)
app.add_middleware(LoggingMiddleware)
app.add_middleware(RateLimitMiddleware)
app.include_router(router)
Base.metadata.create_all(engine)


@app.exception_handler(ServiceError)
async def service_error_handler(_: Request, exc: ServiceError):
    return JSONResponse({"detail": exc.message}, status_code=exc.status)


STATIC = Path(__file__).parent / "static"


@app.get("/", include_in_schema=False)
async def storefront():
    return FileResponse(STATIC / "index.html")


@app.get("/health", tags=["Health"])
async def health():
    return {"status": "healthy", "timestamp": datetime.now(timezone.utc).isoformat(),
            "service": "e-commerce-platform", "version": "1.0.0"}


@app.get("/metrics", include_in_schema=False)
async def metrics():
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)


if __name__ == "__main__":
    uvicorn.run("src.main:app", host=settings.HOST, port=settings.PORT, reload=settings.DEBUG)
