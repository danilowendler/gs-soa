from datetime import date

from fastapi import APIRouter, Depends, Query

from app.deps import get_service
from app.schemas import ErroResposta, PrevisaoDetalhe, PrevisaoEntrada, PrevisaoSaida
from app.services.previsao_service import PrevisaoService

router = APIRouter(prefix="/previsoes", tags=["Previsões"])
NAO_ENCONTRADA = {404: {"model": ErroResposta, "description": "Previsão não encontrada"}}


@router.post(
    "",
    response_model=PrevisaoSaida,
    status_code=201,
    summary="Prever se o dia será de calor perigoso",
    description="Recebe as observações de ontem, calcula a probabilidade, grava a previsão e a devolve. "
    "Chamado pela API principal (C#).",
)
def criar_previsao(entrada: PrevisaoEntrada, service: PrevisaoService = Depends(get_service)):
    return service.prever(entrada)


@router.get("", response_model=list[PrevisaoDetalhe], summary="Listar previsões (mais recentes primeiro)")
def listar_previsoes(
    data: date | None = Query(None, description="Filtra pelo dia previsto (AAAA-MM-DD)."),
    limite: int = Query(50, ge=1, le=200),
    deslocamento: int = Query(0, ge=0),
    service: PrevisaoService = Depends(get_service),
):
    return service.listar(data, limite, deslocamento)


@router.get(
    "/data/{data}",
    response_model=PrevisaoDetalhe,
    responses=NAO_ENCONTRADA,
    summary="Última previsão registrada para um dia",
)
def previsao_da_data(data: date, service: PrevisaoService = Depends(get_service)):
    return service.da_data(data)


@router.get("/{previsao_id}", response_model=PrevisaoDetalhe, responses=NAO_ENCONTRADA, summary="Buscar previsão por id")
def obter_previsao(previsao_id: int, service: PrevisaoService = Depends(get_service)):
    return service.obter(previsao_id)
