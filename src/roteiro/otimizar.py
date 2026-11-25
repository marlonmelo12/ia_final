"""Caminho ÚNICO de execução, usado igualmente pelo script de experimentos e pela interface (I2).

Dono: Integrante 4. Ver BACKLOG.md.
"""
from roteiro.contratos import EntradaInvalida, SemSolucaoViavel  # noqa: F401


def otimizar(cenario, metodo: str, semente: int | None = None, max_avaliacoes: int | None = None) -> dict:
    """Valida a entrada (EntradaInvalida com mensagem clara), roda o método e devolve:

    {"visitas": [...], "utilidade": float, "tempo_total_min": float, "retorno_min": float,
     "viavel": bool, "avaliacoes": int, "tempo_execucao_s": float, "explicacao": str}

    Orçamento insuficiente NÃO é erro: devolve visitas = [] e a explicação (caso A3).
    """
    raise NotImplementedError
