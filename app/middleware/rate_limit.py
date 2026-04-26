# ============================================================
# CyberShield — Rate Limiting Middleware
# ============================================================

from collections import defaultdict
from time import time

from fastapi import Request
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware


class RateLimitMiddleware(BaseHTTPMiddleware):
    """
    Limits requests per IP address.
    Default: 60 requests per 60 seconds.
    Auth endpoints: 10 requests per 60 seconds.
    """

    def __init__(self, app, max_requests: int = 60, window_seconds: int = 60):
        super().__init__(app)
        self.max_requests = max_requests
        self.window = window_seconds
        self.requests: dict = defaultdict(list)

        # Stricter limits for sensitive endpoints
        self.strict_paths = ["/auth/login", "/auth/register"]
        self.strict_max = 10

    def _get_limit(self, path: str) -> int:
        for p in self.strict_paths:
            if path.startswith(p):
                return self.strict_max
        return self.max_requests

    def _clean_old(self, ip: str, now: float):
        self.requests[ip] = [
            t for t in self.requests[ip] if now - t < self.window
        ]

    async def dispatch(self, request: Request, call_next):
        ip = request.client.host if request.client else "unknown"
        path = request.url.path
        now = time()
        limit = self._get_limit(path)

        self._clean_old(ip, now)

        if len(self.requests[ip]) >= limit:
            return JSONResponse(
                status_code=429,
                content={
                    "detail": "Too many requests. Please slow down.",
                    "retry_after": self.window,
                },
                headers={"Retry-After": str(self.window)},
            )

        self.requests[ip].append(now)
        return await call_next(request)
