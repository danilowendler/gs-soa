"""Serviço de previsão da Refresca (SOA e Web Services · FastAPI)."""
import logging

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.errors import PrevisaoNaoEncontrada
from app.routers import previsoes, saude

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s")

DESCRICAO = (
    "Serviço de previsão da **Refresca** (Vila Mariana, São Paulo). Recebe o resumo do clima de "
    "anteontem, ontem e hoje e responde, com o modelo XGBoost treinado com dados do INMET, se o dia "
    "seguinte tende a ser de calor perigoso para trabalhadores de rua. "
    "É consumido pela API principal em C# (`POST /previsoes`)."
)


def create_app() -> FastAPI:
    app = FastAPI(title="Refresca · Serviço de previsão", version="1.0.0", description=DESCRICAO)
    app.include_router(previsoes.router)
    app.include_router(saude.router)

    @app.exception_handler(PrevisaoNaoEncontrada)
    async def previsao_nao_encontrada(request: Request, erro: PrevisaoNaoEncontrada):
        return JSONResponse(status_code=404, content={"erro": "nao_encontrada", "detalhe": str(erro)})

    return app


app = create_app()
