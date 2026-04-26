# ============================================================
# CyberShield — Unified Detection Engine
# ============================================================

from datetime import datetime
from typing import Optional

from app.services.rules.port_scan import PortScanDetector
from app.services.rules.sqli_detection import SQLiDetector
from app.services.rules.geo_anomaly import GeoAnomalyDetector
from app.services.scoring import ThreatScorer
from app.services.mitre import MitreEnrichment
from app.services.suppression import AlertSuppressor


class DetectionEngine:
    """
    Unified entry point for all threat detection rules.
    Orchestrates: detection -> scoring -> enrichment -> suppression.
    """

    def __init__(self):
        self.port_scan   = PortScanDetector()
        self.sqli        = SQLiDetector()
        self.geo_anomaly = GeoAnomalyDetector()
        self.suppressor  = AlertSuppressor()
        self.alerts: list[dict] = []

    def analyze_request(
        self,
        ip: str,
        port: Optional[int] = None,
        payload: Optional[str] = None,
        user_id: Optional[int] = None,
        username: Optional[str] = None,
    ) -> list[dict]:
        new_alerts = []

        # Port scan
        if port:
            result = self.port_scan.record(ip, port)
            if result:
                alert = self._build_alert(
                    event_type="port_scan",
                    ip=ip,
                    detail=f"{result.count} ports scanned",
                    modifiers=["external_ip", "repeated_attempts"],
                )
                new_alerts.append(alert)

        # SQLi
        if payload:
            result = self.sqli.analyze(ip, payload)
            if result:
                alert = self._build_alert(
                    event_type="sqli_attempt",
                    ip=ip,
                    detail=f"Pattern: {result.pattern_matched}",
                    modifiers=["external_ip"],
                )
                new_alerts.append(alert)

        # Geo anomaly
        if user_id and username:
            result = self.geo_anomaly.record_login(user_id, username, ip)
            if result:
                alert = self._build_alert(
                    event_type="geo_anomaly",
                    ip=ip,
                    detail=f"Login from {result.login_country}, known: {result.known_country}",
                    modifiers=["external_ip"],
                    username=username,
                )
                new_alerts.append(alert)

        # Filtra suprimidos
        filtered = []
        for alert in new_alerts:
            suppressed = self.suppressor.is_suppressed(
                alert["type"], ip, alert.get("username")
            )
            if not suppressed:
                self.alerts.append(alert)
                filtered.append(alert)

        return filtered

    def _build_alert(
        self,
        event_type: str,
        ip: str,
        detail: str,
        modifiers: list[str],
        username: Optional[str] = None,
    ) -> dict:
        score = ThreatScorer.score(event_type, modifiers)
        alert = {
            "type":       event_type,
            "ip":         ip,
            "username":   username,
            "detail":     detail,
            "score":      score.score,
            "risk_level": score.risk_level,
            "label":      score.label,
            "color":      score.color,
            "timestamp":  datetime.utcnow().isoformat(),
        }
        return MitreEnrichment.enrich_alert(alert)

    def get_all_alerts(self) -> list[dict]:
        return self.alerts

    def get_stats(self) -> dict:
        total = len(self.alerts)
        by_type = {}
        by_risk = {}
        for a in self.alerts:
            by_type[a["type"]] = by_type.get(a["type"], 0) + 1
            by_risk[a["risk_level"]] = by_risk.get(a["risk_level"], 0) + 1
        return {
            "total_alerts": total,
            "by_type": by_type,
            "by_risk_level": by_risk,
        }
