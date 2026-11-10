"""
Monta as variáveis do modelo da Refresca a partir do resumo de 3 dias.

Este módulo é usado pelo serviço de previsão (repositório de SOA) e reproduz
exatamente as variáveis criadas na seção 4 do notebook `refresca_ml.ipynb`.
O notebook confere, na seção 9, que os dois cálculos dão o mesmo resultado.

Uso no serviço de previsão:

    import joblib, json
    from preparar_variaveis import montar_variaveis, como_linha

    modelo = joblib.load("modelo/modelo_refresca.joblib")
    meta = json.load(open("modelo/metadados.json", encoding="utf-8"))

    variaveis = montar_variaveis(corpo_da_requisicao["dias"])
    prob = modelo.predict_proba(como_linha(variaveis, meta["variaveis"]))[0, 1]
    perigoso = prob >= meta["limiar_alerta"]   # limiar escolhido no notebook, seção 6.1
"""

from __future__ import annotations

import math
from datetime import date

LIMITE_PERIGO = 32.0

# Campo no JSON do contrato (camelCase) -> nome usado no notebook
CAMPOS_DIA = {
    "tempMax": "temp_max",
    "tempMin": "temp_min",
    "tempMedia": "temp_media",
    "umidMedia": "umid_media",
    "umidMin": "umid_min",
    "indiceCalorMax": "ic_max",
    "pressaoMedia": "pressao_media",
    "radiacaoTotal": "radiacao_total",
    "precipTotal": "precip_total",
    "ventoMedio": "vento_medio",
}


def _converter_dia(dia: dict) -> dict:
    convertido = {"dia": date.fromisoformat(str(dia["dia"])[:10])}
    for campo_json, nome in CAMPOS_DIA.items():
        if campo_json in dia:
            convertido[nome] = float(dia[campo_json])
        elif nome in dia:
            convertido[nome] = float(dia[nome])
        else:
            raise ValueError(f"Campo obrigatório ausente: {campo_json}")
    return convertido


def montar_variaveis(dias: list[dict], limite_perigo: float = LIMITE_PERIGO) -> dict:
    """
    Recebe o resumo diário de 3 dias consecutivos, em qualquer ordem:
    anteontem, ontem e hoje. Devolve as variáveis do modelo para prever AMANHÃ.
    """
    if len(dias) != 3:
        raise ValueError("Envie exatamente 3 dias consecutivos: anteontem, ontem e hoje.")
    d = sorted((_converter_dia(x) for x in dias), key=lambda x: x["dia"])
    anteontem, ontem, hoje = d
    if (ontem["dia"] - anteontem["dia"]).days != 1 or (hoje["dia"] - ontem["dia"]).days != 1:
        raise ValueError("Os 3 dias precisam ser consecutivos.")

    def perigoso(x: dict) -> float:
        return 1.0 if x["ic_max"] >= limite_perigo else 0.0

    variaveis = {nome: hoje[nome] for nome in CAMPOS_DIA.values()}
    variaveis["perigoso_hoje"] = perigoso(hoje)
    for nome in ["temp_max", "ic_max", "umid_media", "temp_min"]:
        variaveis[f"{nome}_ontem"] = ontem[nome]
        variaveis[f"{nome}_anteontem"] = anteontem[nome]
    variaveis["temp_max_media_3d"] = (anteontem["temp_max"] + ontem["temp_max"] + hoje["temp_max"]) / 3
    variaveis["ic_max_media_3d"] = (anteontem["ic_max"] + ontem["ic_max"] + hoje["ic_max"]) / 3
    variaveis["dias_perigosos_3d"] = perigoso(anteontem) + perigoso(ontem) + perigoso(hoje)
    variaveis["var_pressao"] = hoje["pressao_media"] - ontem["pressao_media"]
    variaveis["var_temp_max"] = hoje["temp_max"] - ontem["temp_max"]
    dia_do_ano = hoje["dia"].timetuple().tm_yday
    variaveis["sazon_sen"] = math.sin(2 * math.pi * dia_do_ano / 365.25)
    variaveis["sazon_cos"] = math.cos(2 * math.pi * dia_do_ano / 365.25)
    return variaveis


def como_linha(variaveis: dict, ordem: list[str]):
    """Converte o dicionário numa tabela de 1 linha, na ordem esperada pelo modelo."""
    import pandas as pd

    return pd.DataFrame([[variaveis[nome] for nome in ordem]], columns=ordem)
