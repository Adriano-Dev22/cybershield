from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from app.database import create_db_and_tables
from app.routers import auth, events, dashboard
from app.services.log_generator import start_log_generator
import uvicorn

app = FastAPI(
    title="CyberShield - Mini SIEM",
    description="Plataforma de monitoramento de segurança inspirada em SIEMs reais",
    version="1.0.0"
)

templates = Jinja2Templates(directory="app/templates")

# Montar arquivos estáticos
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# === ROUTERS ===
app.include_router(auth.router, prefix="/auth", tags=["Autenticação"])
app.include_router(events.router, prefix="", tags=["Eventos"])      # prefix="" porque events.py já tem /api/events
app.include_router(dashboard.router, prefix="/dashboard", tags=["Dashboard"])

@app.on_event("startup")
async def startup_event():
    create_db_and_tables()
    print("🚀 CyberShield iniciado com sucesso!")
    start_log_generator()

@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)