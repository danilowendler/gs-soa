"""Injeção de dependências do FastAPI (nos testes, tudo isto é substituído)."""
from functools import lru_cache

from fastapi import Depends
from sqlalchemy.orm import Session

from app.config import get_settings
from app.database import get_db
from app.ml.preditor import Preditor, criar_preditor
from app.repositories.previsao_repository import PrevisaoRepository
from app.services.previsao_service import PrevisaoService

LIMIAR_PADRAO = 0.5


@lru_cache
def get_preditor() -> Preditor:
    configuracao = get_settings()
    return criar_preditor(configuracao.modelo_path, configuracao.metadados_path)


def limiar_para(preditor: Preditor) -> float:
    """Ordem de prioridade: variável de ambiente, limiar do notebook de ML, 0,5."""
    configurado = get_settings().limiar_perigo
    if configurado is not None:
        return configurado
    return preditor.limiar_sugerido if preditor.limiar_sugerido is not None else LIMIAR_PADRAO


def get_service(db: Session = Depends(get_db), preditor: Preditor = Depends(get_preditor)) -> PrevisaoService:
    return PrevisaoService(PrevisaoRepository(db), preditor, limiar_para(preditor))
