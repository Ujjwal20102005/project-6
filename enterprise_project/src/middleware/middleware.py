import logging
import time
from collections import defaultdict, deque

from prometheus_client import Counter, Histogram
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse

from src.config.settings import settings

logger = logging.getLogger("app.access")
REQUESTS = Counter("http_requests_total", "HTTP requests", ["method", "path", "status"])
LATENCY = Histogram("http_request_seconds", "Request latency", ["path"])


class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        start = time.perf_counter()
        response = await call_next(request)
        elapsed = time.perf_counter() - start
        REQUESTS.labels(request.method, request.url.path, response.status_code).inc()
        LATENCY.labels(request.url.path).observe(elapsed)
        response.headers["X-Process-Time"] = f"{elapsed:.4f}"
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["Strict-Transport-Security"] = "max-age=63072000; includeSubDomains"
        logger.info("%s %s -> %s (%.1fms)", request.method, request.url.path,
                    response.status_code, elapsed * 1000)
        return response


class RateLimitMiddleware(BaseHTTPMiddleware):
    """Sliding-window per-IP limiter (in-memory; use Redis for multi-replica)."""

    def __init__(self, app):
        super().__init__(app)
        self.hits = defaultdict(deque)

    async def dispatch(self, request, call_next):
        ip = request.client.host if request.client else "unknown"
        now, q = time.time(), self.hits[ip]
        while q and now - q[0] > 60:
            q.popleft()
        if len(q) >= settings.RATE_LIMIT_PER_MIN:
            return JSONResponse({"detail": "Rate limit exceeded"}, status_code=429)
        q.append(now)
        return await call_next(request)
