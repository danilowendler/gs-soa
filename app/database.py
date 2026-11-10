"""Conexão com o banco (SQLAlchemy 2.0). O banco padrão é SQLite; troque pela variável
REFRESCA_PREVISAO_DB_URL para usar outro (ex.: PostgreSQL)."""
from collections.abc import Iterator

from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

from app.config import get_settings


class Base(DeclarativeBase):
    pass


def criar_engine(url: str) -> Engine:
    argumentos = {}
    if url.startswith("sqlite"):
        argumentos["connect_args"] = {"check_same_thread": False}
    return create_engine(url, **argumentos)


engine = criar_engine(get_settings().database_url)
SessionLocal = sessionmaker(bind=engine, autoflush=False, expire_on_commit=False)


def get_db() -> Iterator[Session]:
    """Uma sessão por requisição, sempre fechada no final."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
