"""Representação do problema: cenário, distâncias, tempo e função objetivo (P1-P4).

Dono: Integrante 2. Ver BACKLOG.md.

Um roteiro é uma lista ordenada de osm_id, sem repetição. Começa e termina no ponto de partida.
tempo(roteiro) = soma dos deslocamentos (haversine / VELOCIDADE_KMH, inclusive o retorno)
                 + DURACAO_VISITA_MIN * len(roteiro)
utilidade(roteiro) = soma das preferências das categorias visitadas
Viável se não houver repetição e tempo(roteiro) <= orcamento_min.
"""
from dataclasses import dataclass


@dataclass(frozen=True)
class Cenario:
    lat_partida: float
    lon_partida: float
    orcamento_min: float
    preferencias: dict  # categoria -> inteiro de 1 a 5


def haversine_km(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    raise NotImplementedError


class Avaliador:
    """Calcula tempo, utilidade e viabilidade, e CONTA cada avaliação da função objetivo.

    O mesmo contador é usado por todos os métodos, para que o limite MAX_AVALIACOES
    seja idêntico entre subida de encosta e têmpera simulada.
    """

    def __init__(self, pois, cenario: Cenario):
        raise NotImplementedError

    def tempo(self, roteiro: list) -> float:
        raise NotImplementedError

    def avaliar(self, roteiro: list):
        """Incrementa o contador e devolve (utilidade, tempo, viavel)."""
        raise NotImplementedError
