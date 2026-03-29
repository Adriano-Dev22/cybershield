from collections import defaultdict
import time
from sqlmodel import Session
from app.models.event import SecurityEvent
from app.models.alert import Alert
from app.services.mitre_mapper import get_mitre_info

class RuleEngine:
    def __init__(self):
        self.failed_logins = defaultdict(list)   # ip -> list of timestamps

    def analyze_event(self, event: SecurityEvent, session: Session) -> SecurityEvent:
        """Aplica regras de detecção e retorna o evento atualizado"""
        
        # Regra 1: Brute Force (5 tentativas falhas em 60 segundos)
        if event.event_type.lower() == "login" and event.status.lower() == "fail":
            self.failed_logins[event.source_ip].append(time.time())
            # Remove tentativas antigas (> 60s)
            self.failed_logins[event.source_ip] = [
                t for t in self.failed_logins[event.source_ip] 
                if time.time() - t < 60
            ]
            
            if len(self.failed_logins[event.source_ip]) >= 5:
                event.severity = "critical"
                mitre = get_mitre_info("brute force")
                event.mitre_tactic = mitre["tactic"]
                event.mitre_technique = mitre["technique"]
                
                # Cria alerta
                alert = Alert(
                    event_id=event.id if event.id else 0,
                    title="🚨 Brute Force Attack Detected",
                    description=f"IP {event.source_ip} realizou {len(self.failed_logins[event.source_ip])} tentativas de login falhas em menos de 60 segundos.",
                    severity="critical",
                    mitre_tactic=mitre["tactic"]
                )
                session.add(alert)
                session.commit()

        # Regra 2: IP acessando múltiplas contas
        elif "multiple accounts" in event.details.lower():
            event.severity = "suspicious"
            mitre = get_mitre_info("multiple accounts")
            event.mitre_tactic = mitre["tactic"]
            event.mitre_technique = mitre["technique"]

        return event