"""Acesso ao banco: só consultas e gravações, sem regra de negócio."""
from datetime import date

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.domain.previsao import Previsao


class PrevisaoRepository:
    def __init__(self, db: Session):
        self._db = db

    def adicionar(self, previsao: Previsao) -> Previsao:
        self._db.add(previsao)
        self._db.commit()
        self._db.refresh(previsao)
        return previsao

    def obter(self, previsao_id: int) -> Previsao | None:
        return self._db.get(Previsao, previsao_id)

    def listar(self, data: date | None, limite: int, deslocamento: int) -> list[Previsao]:
        consulta = select(Previsao).order_by(Previsao.id.desc()).limit(limite).offset(deslocamento)
        if data is not None:
            consulta = consulta.where(Previsao.data == data)
        return list(self._db.scalars(consulta))

    def ultima_da_data(self, data: date) -> Previsao | None:
        consulta = select(Previsao).where(Previsao.data == data).order_by(Previsao.id.desc()).limit(1)
        return self._db.scalars(consulta).first()
