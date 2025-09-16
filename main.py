import os
from datetime import datetime, timedelta
from typing import Generator

from fastapi import FastAPI, HTTPException, Depends, Response
from fastapi.staticfiles import StaticFiles
from fastapi.responses import PlainTextResponse, RedirectResponse
from pydantic import BaseModel
from jose import jwt
from passlib.context import CryptContext
from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.orm import sessionmaker, declarative_base, Session

# --- CONFIG ---
BASE_DIR = os.path.dirname(__file__)
PRIVATE_KEY_PATH = os.getenv("PRIVATE_KEY_PATH", os.path.join(BASE_DIR, "keys", "private.pem"))
PUBLIC_KEY_PATH = os.getenv("PUBLIC_KEY_PATH", os.path.join(BASE_DIR, "keys", "public.pem"))
ALGORITHM = "RS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 15

# --- LOAD KEYS ---
with open(PRIVATE_KEY_PATH, "rb") as f:
    PRIVATE_KEY = f.read()
with open(PUBLIC_KEY_PATH, "rb") as f:
    PUBLIC_KEY = f.read()

# --- PASSWORD HASH ---
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# --- DATABASE (sqlite simple) ---
DATABASE_URL = f"sqlite:///{os.path.join(BASE_DIR, 'db.sqlite3')}"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)

Base.metadata.create_all(bind=engine)

def get_db() -> Generator:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# --- Pydantic schemas ---
class RegisterSchema(BaseModel):
    username: str
    email: str
    password: str

class LoginSchema(BaseModel):
    username: str
    password: str

# --- APP ---
app = FastAPI(title="Exemplo Login FastAPI (RS256 JWT)")

# serve frontend estático
app.mount("/static", StaticFiles(directory="frontend"), name="static")

# rota raiz redireciona para frontend
@app.get("/")
def root():
    return RedirectResponse(url="/static/index.html")

@app.post("/register", status_code=201)
def register(payload: RegisterSchema, db: Session = Depends(get_db)):
    if db.query(User).filter((User.username == payload.username) | (User.email == payload.email)).first():
        raise HTTPException(status_code=400, detail="Username ou email já cadastrado")
    hashed = pwd_context.hash(payload.password)
    user = User(username=payload.username, email=payload.email, hashed_password=hashed)
    db.add(user)
    db.commit()
    db.refresh(user)
    return {"message": "Usuário criado com sucesso", "user_id": user.id}

@app.post("/login")
def login(payload: LoginSchema, response: Response, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == payload.username).first()
    if not user or not pwd_context.verify(payload.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Credenciais inválidas")
    now = datetime.utcnow()
    exp = now + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    token_payload = {
        "sub": user.username,
        "email": user.email,
        "user_id": user.id,
        "iat": int(now.timestamp()),
        "exp": int(exp.timestamp())
    }
    token = jwt.encode(token_payload, PRIVATE_KEY, algorithm=ALGORITHM)
    response.set_cookie("access_token", token, max_age=ACCESS_TOKEN_EXPIRE_MINUTES * 60, httponly=False, path="/")
    return {"access_token": token, "token_type": "bearer", "expires_in": ACCESS_TOKEN_EXPIRE_MINUTES * 60}

@app.get("/public_key", response_class=PlainTextResponse)
def public_key():
    """Frontend usa esta chave pública para verificar assinatura do JWT (RS256)."""
    return PUBLIC_KEY.decode("utf-8")
