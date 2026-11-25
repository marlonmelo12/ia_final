"""Vizinhança do roteiro: inserção, remoção e troca de posições (P5).

Dono: Integrante 2. Ver BACKLOG.md.
"""


def inserir(roteiro: list, local, posicao: int) -> list:
    raise NotImplementedError


def remover(roteiro: list, posicao: int) -> list:
    raise NotImplementedError


def trocar(roteiro: list, i: int, j: int) -> list:
    raise NotImplementedError


def vizinho_aleatorio(roteiro: list, todos_os_locais: list, rng) -> list:
    """Sorteia um dos três movimentos e devolve um novo roteiro (nunca altera o original)."""
    raise NotImplementedError
