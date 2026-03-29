from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from typing import List

from app.database import get_session
from app.models.event import SecurityEvent

router = APIRouter()

@router.get("/", response_model=List[SecurityEvent])
def get_all_events(session: Session = Depends(get_session)):
    """Retorna todos os eventos de segurança"""
    events = session.exec(select(SecurityEvent)).all()
    return events

@router.post("/")
def create_event(event: SecurityEvent, session: Session = Depends(get_session)):
    """Cria um novo evento (usado internamente pelo gerador)"""
    session.add(event)
    session.commit()
    session.refresh(event)
    return event

@router.get("/recent")
def get_recent_events(limit: int = 50, session: Session = Depends(get_session)):
    """Retorna os eventos mais recentes"""
    events = session.exec(
        select(SecurityEvent).order_by(SecurityEvent.timestamp.desc())
    ).all()[:limit]
    return events