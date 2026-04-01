from fastapi import APIRouter, Depends
from sqlmodel import Session

from app.database import get_session
from app.services.log_generator import generate_fake_event

router = APIRouter()

@router.post("/api/events/generate")
def generate_logs_manual(session: Session = Depends(get_session)):
    """Gera logs manualmente (botão no dashboard)"""
    for _ in range(8):
        generate_fake_event(session)
    return {"status": "success", "message": "Logs gerados com sucesso!"}