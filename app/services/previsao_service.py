"""Casos de uso: orquestra preditor, regra de negócio e repositório."""
import json
import logging
from datetime import date

from app.domain.previsao import Previsao
from app.errors import PrevisaoNaoEncontrada
from app.ml.preditor import Preditor
from app.repositories.previsao_repository import PrevisaoRepository
from app.schemas import PrevisaoEntrada

log = logging.getLogger("refresca.previsao")


class PrevisaoService:
    def __init__(self, repositorio: PrevisaoRepository, preditor: Preditor, limiar_perigo: float):
        self._repo = repositorio
        self._preditor = preditor
        self._limiar = limiar_perigo

    def prever(self, entrada: PrevisaoEntrada) -> Previsao:
        dias = [d.model_dump(by_alias=True, mode="json") for d in entrada.dias]
        ontem = entrada.dias[-1]
        probabilidade = min(1.0, max(0.0, round(self._preditor.probabilidade(dias), 4)))
        previsao = Previsao(
            data=entrada.data_prevista,
            temperatura_max_ontem=ontem.temp_max,
            temperatura_min_ontem=ontem.temp_min,
            umidade_media_ontem=ontem.umid_media,
            vento_medio_ontem=ontem.vento_medio,
            dias_json=json.dumps(dias, ensure_ascii=False),
            probabilidade=probabilidade,
            perigoso=Previsao.e_perigosa(probabilidade, self._limiar),
            versao_modelo=self._preditor.versao,
        )
        salva = self._repo.adicionar(previsao)
        log.info("previsao id=%s data=%s p=%.4f limiar=%.2f perigoso=%s modelo=%s",
                 salva.id, salva.data, salva.probabilidade, self._limiar, salva.perigoso, salva.versao_modelo)
        return salva

    def obter(self, previsao_id: int) -> Previsao:
        previsao = self._repo.obter(previsao_id)
        if previsao is None:
            raise PrevisaoNaoEncontrada(f"Previsão {previsao_id} não encontrada")
        return previsao

    def listar(self, data: date | None, limite: int, deslocamento: int) -> list[Previsao]:
        return self._repo.listar(data, limite, deslocamento)

    def da_data(self, data: date) -> Previsao:
        previsao = self._repo.ultima_da_data(data)
        if previsao is None:
            raise PrevisaoNaoEncontrada(f"Nenhuma previsão registrada para {data.isoformat()}")
        return previsao
