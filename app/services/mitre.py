# ============================================================
# CyberShield — MITRE ATT&CK Enrichment Service
# ============================================================

from dataclasses import dataclass
from typing import Optional


@dataclass
class MitreTag:
    technique_id: str
    technique_name: str
    tactic: str
    tactic_id: str
    description: str
    url: str
    severity_hint: str


class MitreEnrichment:
    """
    Enriches security alerts with MITRE ATT&CK framework tags.
    Maps internal event types to techniques and tactics.
    """

    TECHNIQUES: dict[str, MitreTag] = {
        "brute_force": MitreTag(
            technique_id="T1110",
            technique_name="Brute Force",
            tactic="Credential Access",
            tactic_id="TA0006",
            description="Adversary attempts to gain access by guessing credentials.",
            url="https://attack.mitre.org/techniques/T1110/",
            severity_hint="high",
        ),
        "port_scan": MitreTag(
            technique_id="T1046",
            technique_name="Network Service Discovery",
            tactic="Discovery",
            tactic_id="TA0007",
            description="Adversary scans for open ports and running services.",
            url="https://attack.mitre.org/techniques/T1046/",
            severity_hint="medium",
        ),
        "sqli_attempt": MitreTag(
            technique_id="T1190",
            technique_name="Exploit Public-Facing Application",
            tactic="Initial Access",
            tactic_id="TA0001",
            description="Adversary exploits weakness in internet-facing application.",
            url="https://attack.mitre.org/techniques/T1190/",
            severity_hint="critical",
        ),
        "geo_anomaly": MitreTag(
            technique_id="T1078",
            technique_name="Valid Accounts",
            tactic="Defense Evasion",
            tactic_id="TA0005",
            description="Adversary uses compromised credentials from unusual location.",
            url="https://attack.mitre.org/techniques/T1078/",
            severity_hint="high",
        ),
        "data_exfil": MitreTag(
            technique_id="T1041",
            technique_name="Exfiltration Over C2 Channel",
            tactic="Exfiltration",
            tactic_id="TA0010",
            description="Adversary exfiltrates data over the command and control channel.",
            url="https://attack.mitre.org/techniques/T1041/",
            severity_hint="critical",
        ),
        "privilege_escal": MitreTag(
            technique_id="T1068",
            technique_name="Exploitation for Privilege Escalation",
            tactic="Privilege Escalation",
            tactic_id="TA0004",
            description="Adversary exploits software vulnerability to escalate privileges.",
            url="https://attack.mitre.org/techniques/T1068/",
            severity_hint="critical",
        ),
        "c2_beacon": MitreTag(
            technique_id="T1071",
            technique_name="Application Layer Protocol",
            tactic="Command and Control",
            tactic_id="TA0011",
            description="Adversary communicates with compromised systems via C2 channel.",
            url="https://attack.mitre.org/techniques/T1071/",
            severity_hint="critical",
        ),
        "dos_attack": MitreTag(
            technique_id="T1499",
            technique_name="Endpoint Denial of Service",
            tactic="Impact",
            tactic_id="TA0040",
            description="Adversary performs denial of service to degrade availability.",
            url="https://attack.mitre.org/techniques/T1499/",
            severity_hint="high",
        ),
    }

    @classmethod
    def enrich(cls, event_type: str) -> Optional[MitreTag]:
        return cls.TECHNIQUES.get(event_type)

    @classmethod
    def enrich_alert(cls, alert: dict) -> dict:
        event_type = alert.get("type", "")
        tag = cls.enrich(event_type)
        if tag:
            alert["mitre"] = {
                "technique_id":   tag.technique_id,
                "technique_name": tag.technique_name,
                "tactic":         tag.tactic,
                "tactic_id":      tag.tactic_id,
                "url":            tag.url,
                "severity_hint":  tag.severity_hint,
            }
        return alert

    @classmethod
    def list_all(cls) -> list[MitreTag]:
        return list(cls.TECHNIQUES.values())

    @classmethod
    def get_by_tactic(cls, tactic: str) -> list[MitreTag]:
        return [
            t for t in cls.TECHNIQUES.values()
            if t.tactic.lower() == tactic.lower()
        ]
