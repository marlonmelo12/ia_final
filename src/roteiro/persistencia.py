"""Registro das execuções em SQLite: salvar, listar e exportar (Q3).

Dono: Integrante 5. Ver BACKLOG.md.
"""


def salvar_execucao(entrada: dict, parametros: dict, resultado: dict) -> int:
    """Grava cenário, método, semente, parâmetros e resultado (roteiro incluso) e retorna o id."""
    raise NotImplementedError


def listar_execucoes():
    raise NotImplementedError


def exportar_execucoes(caminho) -> None:
    raise NotImplementedError
