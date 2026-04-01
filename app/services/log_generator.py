from sqlmodel import Session
from app.models.event import SecurityEvent
from app.services.detection import RuleEngine
from faker import Faker
import random
import time
import threading

fake = Faker()
rule_engine = RuleEngine()


def generate_fake_event(db_session: Session):
    """Gera um evento fake e aplica regras de detecção"""
    event_types = ["login", "ssh_attempt", "web_request", "command_execution"]
    
    is_suspicious = random.random() < 0.45   # Chance de gerar alerta

    event = SecurityEvent(
        source_ip=fake.ipv4(),
        username=fake.user_name() if random.random() > 0.35 else None,
        event_type="login" if is_suspicious else random.choice(event_types),
        status="fail" if is_suspicious else random.choice(["success", "fail"]),
        details="Multiple failed login attempts" if is_suspicious else fake.sentence(),
        severity="normal"
    )

    # Aplica regras (brute force, etc)
    event = rule_engine.analyze_event(event, db_session)
    
    db_session.add(event)
    db_session.commit()
    db_session.refresh(event)
    return event


def start_log_generator():
    """Inicia a simulação de logs em background"""
    def background_generator():
        print("🔄 Simulador de ataques iniciado - Gerando logs fake...")
        
        while True:
            try:
                from app.database import engine
                from sqlmodel import Session
                
                with Session(engine) as session:
                    for _ in range(random.randint(2, 6)):   # Gera vários eventos por vez
                        generate_fake_event(session)
                
                time.sleep(random.uniform(2.0, 5.0))
                
            except Exception as e:
                print(f"⚠️ Erro no gerador: {e}")
                time.sleep(5)

    # Inicia em thread separada
    thread = threading.Thread(target=background_generator, daemon=True)
    thread.start()
    print("✅ Thread do gerador de logs iniciada com sucesso!")