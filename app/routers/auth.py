from fastapi import APIRouter, Depends, HTTPException, status, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlmodel import Session, select
from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta
from typing import Optional
import os
from dotenv import load_dotenv

from app.database import get_session
from app.models.user import User

load_dotenv()

router = APIRouter()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
templates = Jinja2Templates(directory="app/templates")

SECRET_KEY = os.getenv("SECRET_KEY", "supersecretkeychangeme123!")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


# ====================== PÁGINAS HTML ======================
@router.get("/login", response_class=HTMLResponse)
async def login_page():
    return templates.TemplateResponse("login.html", {"request": {}})


@router.get("/register", response_class=HTMLResponse)
async def register_page():
    return templates.TemplateResponse("register.html", {"request": {}})


# ====================== CADASTRO ======================
@router.post("/register")
def register(
    username: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
    session: Session = Depends(get_session)
):
    # Verifica se o usuário já existe
    existing = session.exec(select(User).where(User.username == username)).first()
    if existing:
        raise HTTPException(status_code=400, detail="Usuário já cadastrado")

    hashed_password = get_password_hash(password)
    new_user = User(
        username=username,
        email=email,
        hashed_password=hashed_password
    )

    session.add(new_user)
    session.commit()
    session.refresh(new_user)

    return RedirectResponse(url="/auth/login", status_code=303)


# ====================== LOGIN ======================
@router.post("/login")
def login(
    username: str = Form(...),
    password: str = Form(...),
    session: Session = Depends(get_session)
):
    user = session.exec(select(User).where(User.username == username)).first()

    if not user or not verify_password(password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuário ou senha incorretos"
        )

    # Por enquanto apenas redireciona (JWT será usado depois)
    return RedirectResponse(url="/dashboard", status_code=303)


# Rota simples para logout (opcional)
@router.get("/logout")
def logout():
    return RedirectResponse(url="/", status_code=303)