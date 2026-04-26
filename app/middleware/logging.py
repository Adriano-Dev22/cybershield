# ============================================================
# CyberShield — Request Logging Middleware
# ============================================================

import time
import uuid

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

import logging

logger = logging.getLogger("cybershield.requests")
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)


class RequestLoggingMiddleware(BaseHTTPMiddleware):
    """
    Logs every incoming request with:
    - Request ID (UUID)
    - Method and path
    - Client IP
    - Response status code
    - Response time in ms
    """

    async def dispatch(self, request: Request, call_next):
        request_id = str(uuid.uuid4())[:8]
        ip = request.client.host if request.client else "unknown"
        method = request.method
        path = request.url.path
        start = time.perf_counter()

        logger.info(f"[{request_id}] --> {method} {path} from {ip}")

        try:
            response = await call_next(request)
            elapsed = (time.perf_counter() - start) * 1000
            logger.info(
                f"[{request_id}] <-- {response.status_code} "
                f"{method} {path} ({elapsed:.1f}ms)"
            )
            response.headers["X-Request-ID"] = request_id
            return response
        except Exception as e:
            elapsed = (time.perf_counter() - start) * 1000
            logger.error(
                f"[{request_id}] ERR {method} {path} "
                f"({elapsed:.1f}ms) — {e}"
            )
            raise
