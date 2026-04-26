# ============================================================
# CyberShield — SQL Injection Detection Rule
# ============================================================

import re
from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class SQLiAlert:
    ip: str
    payload: str
    pattern_matched: str
    severity: str
    timestamp: datetime
    mitre_technique: str = "T1190"
    mitre_tactic: str = "Initial Access"


class SQLiDetector:
    """
    Detects SQL injection attempts in log entries and request params.

    MITRE ATT&CK: T1190 - Exploit Public-Facing Application
    """

    PATTERNS = {
        "union_select": (
            r"(\bUNION\b.{0,20}\bSELECT\b)",
            "critical",
        ),
        "comment_bypass": (
            r"(--|#|\/\*|\*\/)",
            "high",
        ),
        "boolean_blind": (
            r"(\bOR\b\s+\d+\s*=\s*\d+|\bAND\b\s+\d+\s*=\s*\d+)",
            "high",
        ),
        "stacked_queries": (
            r"(;\s*(SELECT|INSERT|UPDATE|DELETE|DROP|CREATE))",
            "critical",
        ),
        "time_based": (
            r"(SLEEP\s*\(|WAITFOR\s+DELAY|BENCHMARK\s*\()",
            "high",
        ),
        "error_based": (
            r"(EXTRACTVALUE|UPDATEXML|FLOOR\(RAND)",
            "medium",
        ),
        "schema_enum": (
            r"(information_schema|sys\.tables|pg_catalog)",
            "medium",
        ),
    }

    _compiled = {
        name: (re.compile(pattern, re.IGNORECASE), severity)
        for name, (pattern, severity) in PATTERNS.items()
    }

    @classmethod
    def analyze(cls, ip: str, payload: str) -> Optional[SQLiAlert]:
        for name, (pattern, severity) in cls._compiled.items():
            if pattern.search(payload):
                return SQLiAlert(
                    ip=ip,
                    payload=payload[:500],
                    pattern_matched=name,
                    severity=severity,
                    timestamp=datetime.utcnow(),
                )
        return None

    @classmethod
    def analyze_bulk(cls, ip: str, payloads: list[str]) -> list[SQLiAlert]:
        alerts = []
        for payload in payloads:
            result = cls.analyze(ip, payload)
            if result:
                alerts.append(result)
        return alerts

    @classmethod
    def get_pattern_names(cls) -> list[str]:
        return list(cls.PATTERNS.keys())
