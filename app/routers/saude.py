from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.database import get_db
from app.deps import get_preditor
from app.ml.preditor import Preditor

router = APIRouter(tags=["Saúde"])


@router.get("/health", summary="Verificar se o serviço e o banco estão no ar")
def health(db: Session = Depends(get_db), preditor: Preditor = Depends(get_preditor)):
    try:
        db.execute(text("SELECT 1"))
        banco = "ok"
    except Exception:
        banco = "indisponivel"
    corpo = {"status": "ok" if banco == "ok" else "falha", "banco": banco, "versaoModelo": preditor.versao}
    return JSONResponse(corpo, status_code=200 if banco == "ok" else 503)
