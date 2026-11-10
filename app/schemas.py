"""Contratos JSON (Pydantic). Os nomes em camelCase seguem o contrato do README da equipe."""
from datetime import date, datetime, timedelta

from pydantic import BaseModel, ConfigDict, Field, model_validator
from pydantic.alias_generators import to_camel


class CamelModel(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True, from_attributes=True)


class DiaClima(CamelModel):
    """Resumo do clima de um dia (mesmas variáveis usadas no treino do modelo de ML)."""

    dia: date = Field(description="Dia observado (AAAA-MM-DD).")
    temp_max: float = Field(ge=-10, le=50, description="Temperatura máxima do dia, em °C.")
    temp_min: float = Field(ge=-10, le=50, description="Temperatura mínima do dia, em °C.")
    temp_media: float = Field(ge=-10, le=50, description="Temperatura média do dia, em °C.")
    umid_media: float = Field(ge=0, le=100, description="Umidade relativa média, em %.")
    umid_min: float = Field(ge=0, le=100, description="Umidade relativa mínima, em %.")
    indice_calor_max: float = Field(ge=-10, le=70, description="Índice de calor máximo do dia, em °C.")
    pressao_media: float = Field(ge=800, le=1100, description="Pressão média ao nível da estação, em mB.")
    radiacao_total: float = Field(ge=0, le=60000, description="Radiação global somada no dia, em kJ/m².")
    precip_total: float = Field(ge=0, le=500, description="Chuva acumulada no dia, em mm.")
    vento_medio: float = Field(ge=0, le=60, description="Velocidade média do vento, em m/s.")

    @model_validator(mode="after")
    def minima_nao_pode_superar_maxima(self) -> "DiaClima":
        if self.temp_min > self.temp_max:
            raise ValueError(f"tempMin não pode ser maior que tempMax ({self.dia.isoformat()})")
        return self


EXEMPLO_DIAS = [
    {"dia": "2026-11-17", "tempMax": 30.1, "tempMin": 18.2, "tempMedia": 23.5, "umidMedia": 62.0, "umidMin": 38.0,
     "indiceCalorMax": 30.8, "pressaoMedia": 924.6, "radiacaoTotal": 21500, "precipTotal": 0.0, "ventoMedio": 2.0},
    {"dia": "2026-11-18", "tempMax": 31.8, "tempMin": 19.0, "tempMedia": 24.6, "umidMedia": 58.0, "umidMin": 35.0,
     "indiceCalorMax": 32.4, "pressaoMedia": 923.9, "radiacaoTotal": 23100, "precipTotal": 0.0, "ventoMedio": 1.8},
    {"dia": "2026-11-19", "tempMax": 33.0, "tempMin": 19.8, "tempMedia": 25.4, "umidMedia": 55.0, "umidMin": 31.0,
     "indiceCalorMax": 33.9, "pressaoMedia": 923.1, "radiacaoTotal": 24000, "precipTotal": 0.0, "ventoMedio": 2.1},
]


class PrevisaoEntrada(CamelModel):
    """Resumo de anteontem, ontem e hoje; a previsão é para o dia seguinte (dataPrevista)."""

    data_prevista: date = Field(description="Dia que se quer prever (AAAA-MM-DD).")
    dias: list[DiaClima] = Field(min_length=3, max_length=3, description="Os 3 dias anteriores à data prevista.")

    model_config = ConfigDict(json_schema_extra={"example": {"dataPrevista": "2026-11-20", "dias": EXEMPLO_DIAS}})

    @model_validator(mode="after")
    def dias_consecutivos_ate_a_vespera(self) -> "PrevisaoEntrada":
        self.dias = sorted(self.dias, key=lambda d: d.dia)
        esperados = [self.data_prevista - timedelta(days=k) for k in (3, 2, 1)]
        if [d.dia for d in self.dias] != esperados:
            raise ValueError(
                "dias deve trazer os 3 dias consecutivos anteriores à dataPrevista: "
                + ", ".join(d.isoformat() for d in esperados)
            )
        return self


class PrevisaoSaida(CamelModel):
    """Resposta do POST /previsoes (contrato com a API principal)."""

    id: int
    data_prevista: date
    probabilidade: float = Field(ge=0, le=1, description="Probabilidade de o dia ser perigoso.")
    perigoso: bool
    versao_modelo: str

    model_config = ConfigDict(
        json_schema_extra={
            "example": {"id": 42, "dataPrevista": "2026-11-20", "probabilidade": 0.6856, "perigoso": True,
                        "versaoModelo": "xgboost-1.0"}
        }
    )


class PrevisaoDetalhe(PrevisaoSaida):
    """Previsão com os dias de entrada e o momento do registro (consultas GET)."""

    dias: list[DiaClima]
    criado_em: datetime


class ErroResposta(BaseModel):
    erro: str
    detalhe: str
