# ============================================================
# CyberShield — Threat Severity Scoring System
# ============================================================

from dataclasses import dataclass
from enum import Enum
from typing import Optional


class RiskLevel(str, Enum):
    INFO     = "info"
    LOW      = "low"
    MEDIUM   = "medium"
    HIGH     = "high"
    CRITICAL = "critical"


@dataclass
class ScoreResult:
    score: int           # 0-100
    risk_level: RiskLevel
    label: str
    color: str           # para o frontend
    factors: list[str]   # o que influenciou o score


class ThreatScorer:
    """
    Scores threats from 0 to 100 based on multiple factors.

    0-19:   Info
    20-39:  Low
    40-59:  Medium
    60-79:  High
    80-100: Critical
    """

    # Pesos base por tipo de evento
    BASE_SCORES = {
        "brute_force":      65,
        "port_scan":        55,
        "sqli_attempt":     75,
        "geo_anomaly":      60,
        "malware":          85,
        "data_exfil":       90,
        "privilege_escal":  80,
        "c2_beacon":        95,
        "dos_attack":       70,
        "unknown":          30,
    }

    # Modificadores
    MODIFIERS = {
        "after_hours":        +10,   # fora do horário comercial
        "repeated_attempts":  +15,   # múltiplas tentativas
        "privileged_target":  +20,   # alvo é admin/root
        "external_ip":        +10,   # IP externo
        "known_bad_ip":       +25,   # IP em blacklist
        "first_occurrence":   -5,    # primeira vez visto
        "internal_ip":        -10,   # IP interno
        "whitelisted_user":   -15,   # usuário na whitelist
        "low_confidence":     -10,   # baixa confiança na detecção
    }

    @classmethod
    def score(
        cls,
        event_type: str,
        modifiers: Optional[list[str]] = None,
    ) -> ScoreResult:
        base = cls.BASE_SCORES.get(event_type, 30)
        factors = [f"Base score for '{event_type}': {base}"]
        total = base

        for mod in (modifiers or []):
            if mod in cls.MODIFIERS:
                delta = cls.MODIFIERS[mod]
                total += delta
                sign = "+" if delta > 0 else ""
                factors.append(f"Modifier '{mod}': {sign}{delta}")

        total = max(0, min(100, total))

        if total < 20:
            risk = RiskLevel.INFO
            label = "Informational"
            color = "#6b7280"
        elif total < 40:
            risk = RiskLevel.LOW
            label = "Low Risk"
            color = "#22c55e"
        elif total < 60:
            risk = RiskLevel.MEDIUM
            label = "Medium Risk"
            color = "#f59e0b"
        elif total < 80:
            risk = RiskLevel.HIGH
            label = "High Risk"
            color = "#ef4444"
        else:
            risk = RiskLevel.CRITICAL
            label = "Critical Threat"
            color = "#7c3aed"

        return ScoreResult(
            score=total,
            risk_level=risk,
            label=label,
            color=color,
            factors=factors,
        )

    @classmethod
    def score_bulk(
        cls,
        events: list[dict],
    ) -> list[ScoreResult]:
        return [
            cls.score(
                e.get("type", "unknown"),
                e.get("modifiers", []),
            )
            for e in events
        ]
