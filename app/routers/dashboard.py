from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlmodel import Session, select

from app.database import get_session
from app.models.event import SecurityEvent
from app.models.alert import Alert

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

@router.get("/", response_class=HTMLResponse)
async def dashboard_page(request: Request, session: Session = Depends(get_session)):
    events = session.exec(
        select(SecurityEvent).order_by(SecurityEvent.timestamp.desc())  # type: ignore
    ).all()
    
    alerts = session.exec(
        select(Alert).order_by(Alert.timestamp.desc())  # type: ignore
    ).all()

    return templates.TemplateResponse("dashboard.html", {
        "request": request,
        "events": events,
        "alerts": alerts
    })