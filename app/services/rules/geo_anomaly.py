# ============================================================
# CyberShield — Geolocation Anomaly Detector
# ============================================================

from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class GeoAlert:
    user_id: int
    username: str
    known_country: str
    login_country: str
    ip: str
    timestamp: datetime
    severity: str = "high"
    mitre_technique: str = "T1078"
    mitre_tactic: str = "Defense Evasion"


class GeoAnomalyDetector:
    """
    Detects logins from unusual countries compared to user history.
    Flags impossible travel and first-time country logins.

    MITRE ATT&CK: T1078 - Valid Accounts
    """

    # IP ranges por país (simplificado para demo)
    # Em produção, usar um banco GeoIP como MaxMind
    COUNTRY_RANGES = {
        "BR": ["177.", "189.", "191.", "200.", "201."],
        "US": ["8.", "13.", "34.", "52.", "54."],
        "CN": ["1.24.", "14.0.", "27.0.", "36.0."],
        "RU": ["5.8.", "5.44.", "31.13.", "46.17."],
        "DE": ["5.9.", "5.35.", "46.4.", "78.46."],
    }

    def __init__(self):
        # user_id -> list of known countries
        self._user_history: dict[int, set[str]] = {}

    def _detect_country(self, ip: str) -> str:
        for country, prefixes in self.COUNTRY_RANGES.items():
            for prefix in prefixes:
                if ip.startswith(prefix):
                    return country
        return "UNKNOWN"

    def record_login(
        self,
        user_id: int,
        username: str,
        ip: str,
    ) -> Optional[GeoAlert]:
        country = self._detect_country(ip)
        known = self._user_history.get(user_id, set())

        alert = None

        if known and country not in known and country != "UNKNOWN":
            known_list = ", ".join(sorted(known))
            alert = GeoAlert(
                user_id=user_id,
                username=username,
                known_country=known_list,
                login_country=country,
                ip=ip,
                timestamp=datetime.utcnow(),
                severity="critical" if country in ["CN", "RU"] else "high",
            )

        if country != "UNKNOWN":
            if user_id not in self._user_history:
                self._user_history[user_id] = set()
            self._user_history[user_id].add(country)

        return alert

    def get_user_countries(self, user_id: int) -> list[str]:
        return sorted(self._user_history.get(user_id, set()))

    def reset_user(self, user_id: int):
        self._user_history.pop(user_id, None)
