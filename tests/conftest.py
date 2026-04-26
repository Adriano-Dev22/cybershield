# ============================================================
# CyberShield — Test Fixtures
# ============================================================

import pytest
from fastapi.testclient import TestClient


@pytest.fixture
def sample_events():
    return [
        {"type": "brute_force", "ip": "192.168.1.1", "severity": "high"},
        {"type": "port_scan",   "ip": "10.0.0.1",    "severity": "medium"},
        {"type": "sqli_attempt","ip": "172.16.0.5",  "severity": "critical"},
    ]

@pytest.fixture
def sample_user():
    return {
        "id": 1,
        "username": "test_analyst",
        "ip": "177.10.20.30",
    }
