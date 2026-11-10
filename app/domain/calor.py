"""Regras de calor do domínio Refresca (sem dependência de framework)."""
import math

# Faixas da NOAA, as mesmas do contrato entre as partes (README).
LIMITE_ATENCAO_C = 27.0
LIMITE_PERIGO_C = 32.0


def indice_calor_celsius(temperatura_c: float, umidade: float) -> float:
    """Índice de calor (NOAA/Rothfusz) a partir de temperatura (°C) e umidade relativa (%)."""
    t = temperatura_c * 9 / 5 + 32
    rh = umidade
    simples = 0.5 * (t + 61.0 + (t - 68.0) * 1.2 + rh * 0.094)
    if (simples + t) / 2 < 80:
        ic = simples
    else:
        ic = (
            -42.379
            + 2.04901523 * t
            + 10.14333127 * rh
            - 0.22475541 * t * rh
            - 0.00683783 * t * t
            - 0.05481717 * rh * rh
            + 0.00122874 * t * t * rh
            + 0.00085282 * t * rh * rh
            - 0.00000199 * t * t * rh * rh
        )
        if rh < 13 and 80 <= t <= 112:
            ic -= ((13 - rh) / 4) * math.sqrt((17 - abs(t - 95)) / 17)
        elif rh > 85 and 80 <= t <= 87:
            ic += ((rh - 85) / 10) * ((87 - t) / 5)
    return (ic - 32) * 5 / 9


def nivel_do_indice(indice_c: float) -> str:
    """normal | atencao | perigo, conforme o contrato do README."""
    if indice_c >= LIMITE_PERIGO_C:
        return "perigo"
    if indice_c >= LIMITE_ATENCAO_C:
        return "atencao"
    return "normal"
