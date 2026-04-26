# ============================================================
# CyberShield — Port Scan Detection Rule
# ============================================================

from collections import defaultdict
from datetime import datetime, timedelta
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class PortScanAlert:
    ip: str
    ports_scanned: list[int]
    count: int
    first_seen: datetime
    last_seen: datetime
    severity: str
    mitre_technique: str = "T1046"
    mitre_tactic: str = "Discovery"


class PortScanDetector:
    """
    Detects port scanning behavior by tracking how many
    distinct ports a single IP tries to access in a time window.

    MITRE ATT&CK: T1046 - Network Service Discovery
    """

    def __init__(
        self,
        threshold: int = 15,
        window_minutes: int = 5,
    ):
        self.threshold = threshold
        self.window = timedelta(minutes=window_minutes)
        self._records: dict = defaultdict(list)

    def _clean_old(self, ip: str, now: datetime):
        self._records[ip] = [
            (ts, port) for ts, port in self._records[ip]
            if now - ts < self.window
        ]

    def record(self, ip: str, port: int) -> Optional[PortScanAlert]:
        now = datetime.utcnow()
        self._clean_old(ip, now)
        self._records[ip].append((now, port))

        ports = list({p for _, p in self._records[ip]})

        if len(ports) >= self.threshold:
            times = [ts for ts, _ in self._records[ip]]
            severity = (
                "critical" if len(ports) >= 50
                else "high" if len(ports) >= 30
                else "medium"
            )
            return PortScanAlert(
                ip=ip,
                ports_scanned=sorted(ports),
                count=len(ports),
                first_seen=min(times),
                last_seen=max(times),
                severity=severity,
            )
        return None

    def get_stats(self) -> dict:
        return {
            ip: len({p for _, p in records})
            for ip, records in self._records.items()
        }
