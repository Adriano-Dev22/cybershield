from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlmodel import Session, select

from app.database import get_session
from app.models.event import SecurityEvent
from app.models.alert import Alert

router = APIRouter()

# Templates deve ser definido aqui para evitar erro "templates is not defined"
templates = Jinja2Templates(directory="app/templates")


@router.get("/", response_class=HTMLResponse)
async def dashboard_page(request: Request, session: Session = Depends(get_session)):
    """Página principal do Dashboard"""
    events = session.exec(
        select(SecurityEvent).order_by(SecurityEvent.timestamp.desc())
    ).all()
    
    alerts = session.exec(
        select(Alert).order_by(Alert.timestamp.desc())
    ).all()

    unique_ips = len({event.source_ip for event in events})

    return templates.TemplateResponse("dashboard.html", {
        "request": request,
        "events": events,
        "alerts": alerts,
        "unique_ips": unique_ips
    })