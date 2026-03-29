from typing import Dict

MITRE_MAPPING = {
    "brute force": {"tactic": "Credential Access", "technique": "T1110 - Brute Force", "code": "TA0006"},
    "multiple failed logins": {"tactic": "Credential Access", "technique": "T1110 - Brute Force", "code": "TA0006"},
    "failed login": {"tactic": "Credential Access", "technique": "T1110 - Brute Force", "code": "TA0006"},
    "suspicious ip": {"tactic": "Initial Access", "technique": "T1190 - Exploit Public-Facing Application", "code": "TA0001"},
    "multiple accounts": {"tactic": "Credential Access", "technique": "T1110 - Brute Force", "code": "TA0006"},
    "command execution": {"tactic": "Execution", "technique": "T1059 - Command and Scripting Interpreter", "code": "TA0002"},
    "privilege escalation": {"tactic": "Privilege Escalation", "technique": "T1068 - Exploitation for Privilege Escalation", "code": "TA0004"},
}

def get_mitre_info(event_type: str, details: str = "") -> Dict:
    text = (event_type + " " + details).lower()
    
    for key, info in MITRE_MAPPING.items():
        if key in text:
            return info
    
    return {
        "tactic": "Discovery",
        "technique": "Unknown Technique",
        "code": "TA0007"
    }