# ============================================================
# CyberShield — Unit Tests: Detection Rules
# ============================================================

from app.services.rules.port_scan import PortScanDetector
from app.services.rules.sqli_detection import SQLiDetector
from app.services.rules.geo_anomaly import GeoAnomalyDetector
from app.services.scoring import ThreatScorer
from app.services.mitre import MitreEnrichment


class TestPortScanDetector:
    def test_no_alert_below_threshold(self):
        detector = PortScanDetector(threshold=15)
        for port in range(10):
            result = detector.record("1.2.3.4", port)
        assert result is None

    def test_alert_above_threshold(self):
        detector = PortScanDetector(threshold=5)
        result = None
        for port in range(10):
            result = detector.record("1.2.3.4", port)
        assert result is not None
        assert result.ip == "1.2.3.4"
        assert result.count >= 5

    def test_different_ips_dont_interfere(self):
        detector = PortScanDetector(threshold=5)
        for port in range(4):
            detector.record("1.1.1.1", port)
            result = detector.record("2.2.2.2", port)
        assert result is None


class TestSQLiDetector:
    def test_detects_union_select(self):
        result = SQLiDetector.analyze("1.2.3.4", "' UNION SELECT * FROM users--")
        assert result is not None
        assert result.severity == "critical"

    def test_detects_boolean_blind(self):
        result = SQLiDetector.analyze("1.2.3.4", "' OR 1=1--")
        assert result is not None

    def test_clean_input_not_flagged(self):
        result = SQLiDetector.analyze("1.2.3.4", "normal search query")
        assert result is None

    def test_time_based_detected(self):
        result = SQLiDetector.analyze("1.2.3.4", "'; SLEEP(5)--")
        assert result is not None


class TestThreatScorer:
    def test_brute_force_score(self):
        result = ThreatScorer.score("brute_force")
        assert result.score >= 60

    def test_modifiers_increase_score(self):
        base = ThreatScorer.score("port_scan")
        with_mod = ThreatScorer.score("port_scan", ["known_bad_ip", "repeated_attempts"])
        assert with_mod.score > base.score

    def test_score_capped_at_100(self):
        result = ThreatScorer.score("c2_beacon", ["known_bad_ip", "privileged_target", "repeated_attempts"])
        assert result.score <= 100

    def test_score_never_negative(self):
        result = ThreatScorer.score("unknown", ["internal_ip", "whitelisted_user", "low_confidence"])
        assert result.score >= 0


class TestMitreEnrichment:
    def test_enriches_known_event(self):
        tag = MitreEnrichment.enrich("brute_force")
        assert tag is not None
        assert tag.technique_id == "T1110"

    def test_returns_none_for_unknown(self):
        tag = MitreEnrichment.enrich("unknown_event_xyz")
        assert tag is None

    def test_enrich_alert_adds_mitre_field(self):
        alert = {"type": "sqli_attempt", "ip": "1.2.3.4"}
        enriched = MitreEnrichment.enrich_alert(alert)
        assert "mitre" in enriched
        assert enriched["mitre"]["technique_id"] == "T1190"
