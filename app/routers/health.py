# ============================================================
# CyberShield — Health Check Endpoint
# ============================================================

import os
import platform
import time
from datetime import datetime

from fastapi import APIRouter

router = APIRouter(prefix="/api", tags=["System"])

START_TIME = time.time()


@router.get("/health", summary="System health check")
async def health_check():
    """
    Returns the current health status of the CyberShield system.
    Used by load balancers, Docker and monitoring tools.
    """
    uptime_seconds = int(time.time() - START_TIME)
    uptime_str = _format_uptime(uptime_seconds)

    return {
        "status": "healthy",
        "version": "0.1.0",
        "timestamp": datetime.utcnow().isoformat(),
        "uptime": uptime_str,
        "uptime_seconds": uptime_seconds,
        "system": {
            "python": platform.python_version(),
            "os": platform.system(),
            "pid": os.getpid(),
        },
        "services": {
            "database": _check_database(),
            "detection_engine": "online",
            "auth": "online",
        },
    }


@router.get("/health/live", summary="Liveness probe")
async def liveness():
    """Simple liveness probe — returns 200 if app is running."""
    return {"alive": True}


@router.get("/health/ready", summary="Readiness probe")
async def readiness():
    """Readiness probe — checks if app is ready to serve traffic."""
    db_ok = _check_database() == "online"
    return {
        "ready": db_ok,
        "database": "online" if db_ok else "offline",
    }


def _check_database() -> str:
    try:
        import sqlite3
        conn = sqlite3.connect("cybershield.db", timeout=2)
        conn.execute("SELECT 1")
        conn.close()
        return "online"
    except Exception:
        return "offline"


def _format_uptime(seconds: int) -> str:
    days = seconds // 86400
    hours = (seconds % 86400) // 3600
    minutes = (seconds % 3600) // 60
    secs = seconds % 60
    parts = []
    if days:
        parts.append(f"{days}d")
    if hours:
        parts.append(f"{hours}h")
    if minutes:
        parts.append(f"{minutes}m")
    parts.append(f"{secs}s")
    return " ".join(parts)
