# ============================================================
# CyberShield — Event Export to CSV
# ============================================================

import csv
import io
from datetime import datetime
from typing import Any


class CSVExporter:
    """
    Exports security events and alerts to CSV format.
    Supports filtering by date range, severity and event type.
    """

    EVENT_FIELDS = [
        "id",
        "timestamp",
        "type",
        "severity",
        "ip_address",
        "username",
        "description",
        "mitre_technique",
        "mitre_tactic",
        "resolved",
    ]

    AUDIT_FIELDS = [
        "id",
        "timestamp",
        "username",
        "ip_address",
        "action",
        "severity",
        "resource",
        "detail",
        "success",
    ]

    @classmethod
    def events_to_csv(cls, events: list[dict]) -> str:
        """Converts a list of events to CSV string."""
        output = io.StringIO()
        writer = csv.DictWriter(
            output,
            fieldnames=cls.EVENT_FIELDS,
            extrasaction="ignore",
            lineterminator="\n",
        )
        writer.writeheader()
        for event in events:
            row = cls._flatten_event(event)
            writer.writerow(row)
        return output.getvalue()

    @classmethod
    def audit_to_csv(cls, logs: list[dict]) -> str:
        """Converts audit logs to CSV string."""
        output = io.StringIO()
        writer = csv.DictWriter(
            output,
            fieldnames=cls.AUDIT_FIELDS,
            extrasaction="ignore",
            lineterminator="\n",
        )
        writer.writeheader()
        for log in logs:
            writer.writerow(log)
        return output.getvalue()

    @classmethod
    def _flatten_event(cls, event: dict) -> dict:
        """Flattens nested MITRE data into top-level fields."""
        flat = dict(event)
        mitre = event.get("mitre", {})
        flat["mitre_technique"] = mitre.get("technique_id", "")
        flat["mitre_tactic"] = mitre.get("tactic", "")
        return flat

    @classmethod
    def filter_events(
        cls,
        events: list[dict],
        severity: str | None = None,
        event_type: str | None = None,
        since: datetime | None = None,
        until: datetime | None = None,
    ) -> list[dict]:
        """Filters events before export."""
        result = events

        if severity:
            result = [e for e in result if e.get("severity") == severity]

        if event_type:
            result = [e for e in result if e.get("type") == event_type]

        if since:
            result = [
                e for e in result
                if datetime.fromisoformat(str(e.get("timestamp", ""))) >= since
            ]

        if until:
            result = [
                e for e in result
                if datetime.fromisoformat(str(e.get("timestamp", ""))) <= until
            ]

        return result

    @classmethod
    def get_filename(cls, prefix: str = "cybershield_export") -> str:
        """Generates a timestamped filename for the export."""
        ts = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
        return f"{prefix}_{ts}.csv"
