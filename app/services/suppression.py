# ============================================================
# CyberShield — Alert Suppression Rules
# ============================================================

from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import Optional
import hashlib


@dataclass
class SuppressionRule:
    id: str
    name: str
    event_type: str
    ip_address: Optional[str]    # None = qualquer IP
    username: Optional[str]      # None = qualquer usuário
    duration_minutes: int
    reason: str
    created_at: datetime = field(default_factory=datetime.utcnow)
    created_by: str = "system"

    @property
    def expires_at(self) -> datetime:
        return self.created_at + timedelta(minutes=self.duration_minutes)

    @property
    def is_active(self) -> bool:
        return datetime.utcnow() < self.expires_at

    @property
    def remaining_minutes(self) -> int:
        delta = self.expires_at - datetime.utcnow()
        return max(0, int(delta.total_seconds() / 60))


class AlertSuppressor:
    """
    Suppresses repeated or known-safe alerts to reduce noise.

    Use cases:
    - Suppress alerts from known scanners (e.g. security team tools)
    - Suppress during maintenance windows
    - Suppress after alert is acknowledged
    - Suppress low-confidence repeated alerts
    """

    def __init__(self):
        self._rules: dict[str, SuppressionRule] = {}
        self._suppressed_count: dict[str, int] = {}

    def add_rule(
        self,
        name: str,
        event_type: str,
        duration_minutes: int,
        reason: str,
        ip_address: Optional[str] = None,
        username: Optional[str] = None,
        created_by: str = "system",
    ) -> SuppressionRule:
        rule_id = self._make_id(event_type, ip_address, username)
        rule = SuppressionRule(
            id=rule_id,
            name=name,
            event_type=event_type,
            ip_address=ip_address,
            username=username,
            duration_minutes=duration_minutes,
            reason=reason,
            created_by=created_by,
        )
        self._rules[rule_id] = rule
        return rule

    def remove_rule(self, rule_id: str) -> bool:
        if rule_id in self._rules:
            del self._rules[rule_id]
            return True
        return False

    def is_suppressed(
        self,
        event_type: str,
        ip_address: Optional[str] = None,
        username: Optional[str] = None,
    ) -> Optional[SuppressionRule]:
        """Returns the matching rule if alert should be suppressed."""
        self._clean_expired()

        for rule in self._rules.values():
            if not rule.is_active:
                continue
            if rule.event_type != event_type:
                continue
            if rule.ip_address and rule.ip_address != ip_address:
                continue
            if rule.username and rule.username != username:
                continue

            # Incrementa contador de supressões
            self._suppressed_count[rule.id] = (
                self._suppressed_count.get(rule.id, 0) + 1
            )
            return rule

        return None

    def get_active_rules(self) -> list[SuppressionRule]:
        self._clean_expired()
        return list(self._rules.values())

    def get_suppression_stats(self) -> dict:
        return {
            rule_id: {
                "rule": self._rules[rule_id].name,
                "suppressed": count,
            }
            for rule_id, count in self._suppressed_count.items()
            if rule_id in self._rules
        }

    def _clean_expired(self):
        expired = [
            rid for rid, rule in self._rules.items()
            if not rule.is_active
        ]
        for rid in expired:
            del self._rules[rid]

    def _make_id(
        self,
        event_type: str,
        ip: Optional[str],
        username: Optional[str],
    ) -> str:
        raw = f"{event_type}:{ip}:{username}"
        return hashlib.md5(raw.encode()).hexdigest()[:12]
