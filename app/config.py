"""Configuração do serviço. Tudo vem de variáveis de ambiente (ou de um arquivo .env)."""
import os
from dataclasses import dataclass

try:  # python-dotenv é opcional: sem ele, só as variáveis de ambiente valem
    from dotenv import load_dotenv

    load_dotenv()
except ImportError:  # pragma: no cover
    pass


@dataclass(frozen=True)
class Settings:
    database_url: str
    modelo_path: str | None
    metadados_path: str | None
    limiar_perigo: float | None


def get_settings() -> Settings:
    limiar = os.getenv("REFRESCA_LIMIAR_PERIGO", "").strip()
    return Settings(
        database_url=os.getenv("REFRESCA_PREVISAO_DB_URL", "sqlite:///./refresca_previsao.db"),
        modelo_path=os.getenv("REFRESCA_MODELO_PATH") or None,
        metadados_path=os.getenv("REFRESCA_METADADOS_PATH") or None,
        # Vazio = usa o limiar escolhido no notebook de ML (metadados.json), ou 0,5 na heurística.
        limiar_perigo=float(limiar) if limiar else None,
    )
