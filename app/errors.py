"""Exceções de negócio. Os handlers em main.py as transformam em respostas HTTP."""


class PrevisaoNaoEncontrada(Exception):
    """Nenhuma previsão com o id ou a data informados."""


class ModeloIndisponivel(RuntimeError):
    """O arquivo do modelo treinado foi configurado, mas não pôde ser carregado."""
