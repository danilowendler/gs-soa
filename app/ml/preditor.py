"""Preditores de dia de calor perigoso.

Contrato: receber o resumo de 3 dias (anteontem, ontem e hoje) e devolver a probabilidade
(0 a 1) de o dia seguinte ser perigoso. Há dois preditores:

* ModeloXGBoost: o modelo treinado no repositório de ML (modelo_refresca.json + metadados.json).
* HeuristicaCalor: linha de base sem treino, usada quando o modelo não está configurado.
"""
import json
import math
import os
from typing import Protocol

from app.domain.calor import LIMITE_PERIGO_C
from app.errors import ModeloIndisponivel
from app.ml.preparar_variaveis import como_linha, montar_variaveis


class Preditor(Protocol):
    versao: str
    limiar_sugerido: float | None

    def probabilidade(self, dias: list[dict]) -> float: ...


class HeuristicaCalor:
    """Sem treino: compara o índice de calor máximo de hoje com o limite de perigo da NOAA (32 °C)
    por uma curva sigmoide. Serve de linha de base, não de modelo final."""

    versao = "heuristica-1.0"
    limiar_sugerido = None
    ESCALA = 1.5  # °C de índice de calor que separam ~73% de ~27% de probabilidade

    def probabilidade(self, dias: list[dict]) -> float:
        hoje = max(dias, key=lambda d: str(d["dia"]))
        return 1.0 / (1.0 + math.exp(-(float(hoje["indiceCalorMax"]) - LIMITE_PERIGO_C) / self.ESCALA))


class ModeloXGBoost:
    """Carrega o modelo no formato nativo do XGBoost e os metadados gerados pelo notebook de ML.

    O XGBoost precisa ser exatamente da versão usada no treino (ver requirements.txt): o mesmo
    arquivo dá probabilidades diferentes em outras versões.
    """

    def __init__(self, caminho_modelo: str, caminho_metadados: str):
        for caminho in (caminho_modelo, caminho_metadados):
            if not os.path.isfile(caminho):
                raise ModeloIndisponivel(f"Arquivo não encontrado: {caminho}")
        try:
            import xgboost

            with open(caminho_metadados, encoding="utf-8") as arquivo:
                metadados = json.load(arquivo)
            self._variaveis: list[str] = list(metadados["variaveis"])
            self.limiar_sugerido: float | None = float(metadados["limiar_alerta"])
            self.versao = f"xgboost-{metadados.get('versao', '1.0')}"

            versao_treino = metadados.get("xgboost")
            if versao_treino and versao_treino != xgboost.__version__:
                raise ModeloIndisponivel(
                    f"O modelo foi treinado com xgboost {versao_treino}, mas está instalado o "
                    f"{xgboost.__version__}. Instale a versão do requirements.txt."
                )

            self._booster = xgboost.Booster()
            self._booster.load_model(caminho_modelo)
        except ModeloIndisponivel:
            raise
        except Exception as erro:  # arquivo corrompido, biblioteca ausente, metadados incompletos...
            raise ModeloIndisponivel(f"Não foi possível carregar o modelo: {erro}") from erro

    def probabilidade(self, dias: list[dict]) -> float:
        linha = como_linha(montar_variaveis(dias), self._variaveis)
        return float(self._booster.inplace_predict(linha)[0])


def criar_preditor(modelo_path: str | None, metadados_path: str | None = None) -> Preditor:
    if modelo_path:
        metadados = metadados_path or os.path.join(os.path.dirname(modelo_path), "metadados.json")
        return ModeloXGBoost(modelo_path, metadados)
    return HeuristicaCalor()
