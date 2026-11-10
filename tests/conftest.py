from datetime import date, timedelta

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.database import Base, get_db
from app.deps import get_preditor
from app.main import create_app
from app.ml.preditor import HeuristicaCalor


def dias_para(data_prevista: str, indice_calor: float = 33.0, temp_max: float = 31.0) -> list[dict]:
    """Os 3 dias anteriores à data prevista, com valores típicos de um dia quente em São Paulo."""
    alvo = date.fromisoformat(data_prevista)
    return [
        {
            "dia": (alvo - timedelta(days=k)).isoformat(),
            "tempMax": temp_max,
            "tempMin": 19.0,
            "tempMedia": 24.0,
            "umidMedia": 55.0,
            "umidMin": 35.0,
            "indiceCalorMax": indice_calor,
            "pressaoMedia": 924.0,
            "radiacaoTotal": 22000.0,
            "precipTotal": 0.0,
            "ventoMedio": 2.0,
        }
        for k in (3, 2, 1)
    ]


def entrada(data_prevista: str = "2026-11-20", **kwargs) -> dict:
    return {"dataPrevista": data_prevista, "dias": dias_para(data_prevista, **kwargs)}


ENTRADA = entrada()


class PreditorFixo:
    versao = "teste-1.0"
    limiar_sugerido = None

    def __init__(self, valor: float):
        self.valor = valor

    def probabilidade(self, dias) -> float:
        return self.valor


@pytest.fixture(autouse=True)
def sem_limiar_do_ambiente(monkeypatch):
    monkeypatch.delenv("REFRESCA_LIMIAR_PERIGO", raising=False)


@pytest.fixture
def engine():
    motor = create_engine("sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool)
    Base.metadata.create_all(motor)
    yield motor
    motor.dispose()


def _cliente(motor, preditor):
    sessao = sessionmaker(bind=motor, autoflush=False, expire_on_commit=False)

    def db():
        s = sessao()
        try:
            yield s
        finally:
            s.close()

    app = create_app()
    app.dependency_overrides[get_db] = db
    app.dependency_overrides[get_preditor] = lambda: preditor
    return TestClient(app)


@pytest.fixture
def preditor_fixo():
    return PreditorFixo(0.82)


@pytest.fixture
def client(engine, preditor_fixo):
    return _cliente(engine, preditor_fixo)


@pytest.fixture
def client_heuristica(engine):
    return _cliente(engine, HeuristicaCalor())
