"""Representação do problema: cenário, distâncias, tempo e função objetivo (P1-P4).

Dono: Integrante 2. Ver BACKLOG.md.

Um roteiro é uma lista ordenada de osm_id, sem repetição. Começa e termina no ponto de partida.
tempo(roteiro) = soma dos deslocamentos (haversine / VELOCIDADE_KMH, inclusive o retorno)
                 + DURACAO_VISITA_MIN * len(roteiro)
utilidade(roteiro) = soma das preferências das categorias visitadas
Viável se não houver repetição, todos os osm_id existirem e tempo(roteiro) <= orcamento_min.
"""
import math
from dataclasses import dataclass

from roteiro.contratos import (
    CATEGORIAS,
    DURACAO_VISITA_MIN,
    RAIO_TERRA_KM,
    VELOCIDADE_KMH,
    EntradaInvalida,
)

# Folga numérica na comparação com o orçamento: um roteiro que gasta exatamente
# o orçamento continua viável mesmo com erro de arredondamento de ponto flutuante.
TOLERANCIA_MIN = 1e-9


@dataclass(frozen=True)
class Cenario:
    lat_partida: float
    lon_partida: float
    orcamento_min: float
    preferencias: dict  # categoria -> inteiro de 1 a 5


def haversine_km(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Distância geodésica (esfera de raio RAIO_TERRA_KM) entre dois pontos em graus."""
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi = phi2 - phi1
    dlambda = math.radians(lon2 - lon1)
    a = math.sin(dphi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(dlambda / 2) ** 2
    return 2 * RAIO_TERRA_KM * math.asin(math.sqrt(min(1.0, a)))


def minutos_de_deslocamento(km: float) -> float:
    """Tempo, em minutos, para percorrer `km` a VELOCIDADE_KMH."""
    return km / VELOCIDADE_KMH * 60.0


def _registros(pois) -> list[dict]:
    """Aceita o DataFrame de pois.csv ou qualquer iterável de dicts com COLUNAS_POIS."""
    if hasattr(pois, "to_dict"):
        return pois.to_dict("records")
    return [dict(p) for p in pois]


class Avaliador:
    """Calcula tempo, utilidade e viabilidade, e CONTA cada avaliação da função objetivo.

    O mesmo contador é usado por todos os métodos, para que o limite MAX_AVALIACOES
    seja idêntico entre subida de encosta e têmpera simulada.

    Só `avaliar()` incrementa o contador. `tempo()`, `utilidade()` e `deslocamento_min()`
    são consultas auxiliares (recálculo nos testes, explicação na interface) e não contam.
    """

    def __init__(self, pois, cenario: Cenario):
        self.cenario = cenario
        faltando = [c for c in CATEGORIAS if c not in cenario.preferencias]
        if faltando:
            raise EntradaInvalida(f"Faltam preferências para as categorias: {', '.join(faltando)}.")

        registros = _registros(pois)
        self.locais = [r["osm_id"] for r in registros]  # ordem do pois.csv
        if len(set(self.locais)) != len(self.locais):
            raise EntradaInvalida("A lista de locais tem osm_id repetido.")

        self.nome = {r["osm_id"]: r["nome"] for r in registros}
        self.categoria = {r["osm_id"]: r["categoria"] for r in registros}
        self.preferencia = {o: cenario.preferencias[c] for o, c in self.categoria.items()}

        # Índice 0 = ponto de partida; 1..n = locais, na ordem de self.locais.
        self._indice = {osm_id: i + 1 for i, osm_id in enumerate(self.locais)}
        pontos = [(cenario.lat_partida, cenario.lon_partida)] + [
            (float(r["lat"]), float(r["lon"])) for r in registros
        ]
        self._matriz = [
            [minutos_de_deslocamento(haversine_km(*p, *q)) for q in pontos] for p in pontos
        ]
        self.avaliacoes = 0

    # --- Consultas (não contam avaliações) --------------------------------
    def deslocamento_min(self, origem, destino) -> float:
        """Minutos entre dois osm_id; None representa o ponto de partida."""
        i = 0 if origem is None else self._indice[origem]
        j = 0 if destino is None else self._indice[destino]
        return self._matriz[i][j]

    def tempo(self, roteiro: list) -> float:
        """Deslocamentos (inclusive ida e retorno à partida) + DURACAO_VISITA_MIN por visita.

        Levanta KeyError se algum osm_id não existir.
        """
        if not roteiro:
            return 0.0
        idx = [self._indice[o] for o in roteiro]
        m = self._matriz
        deslocamento = m[0][idx[0]] + sum(m[a][b] for a, b in zip(idx, idx[1:])) + m[idx[-1]][0]
        return deslocamento + DURACAO_VISITA_MIN * len(roteiro)

    def utilidade(self, roteiro: list) -> float:
        """Soma das preferências das categorias dos locais visitados."""
        return float(sum(self.preferencia[o] for o in roteiro))

    def tempo_minimo_min(self, osm_id) -> float:
        """Menor roteiro possível com este local: ida + DURACAO_VISITA_MIN + volta."""
        return self.tempo([osm_id])

    def diagnosticar_orcamento(self):
        """Caso A3: verifica se algum local cabe sozinho no orçamento.

        Devolve None se pelo menos um local cabe. Se nenhum cabe, não há roteiro viável
        além do vazio, e devolve um dict com o local mais próximo e quanto tempo falta:

            {"osm_id", "nome", "tempo_minimo_min", "orcamento_min", "falta_min", "mensagem"}

        Não conta avaliações: é uma verificação da entrada, feita antes de qualquer método.
        """
        if not self.locais:
            raise EntradaInvalida("Não há locais cadastrados para montar o roteiro.")
        orcamento = self.cenario.orcamento_min
        # Empate no tempo mínimo: vale o primeiro na ordem do pois.csv (determinístico).
        mais_proximo = min(self.locais, key=self.tempo_minimo_min)
        tempo_minimo = self.tempo_minimo_min(mais_proximo)
        if tempo_minimo <= orcamento + TOLERANCIA_MIN:
            return None
        falta = tempo_minimo - orcamento
        mensagem = (
            f"Nenhum local cabe em {orcamento:.0f} min. O mais próximo é "
            f"{self.nome[mais_proximo]}, que exige {tempo_minimo:.1f} min "
            f"(ida e volta a {VELOCIDADE_KMH:g} km/h mais {DURACAO_VISITA_MIN:.0f} min de visita). "
            f"Faltam {falta:.1f} min."
        )
        return {
            "osm_id": mais_proximo,
            "nome": self.nome[mais_proximo],
            "tempo_minimo_min": tempo_minimo,
            "orcamento_min": orcamento,
            "falta_min": falta,
            "mensagem": mensagem,
        }

    # --- Função objetivo (conta) ------------------------------------------
    def avaliar(self, roteiro: list):
        """Incrementa o contador e devolve (utilidade, tempo, viavel).

        Um roteiro inviável continua com a utilidade e o tempo reais: quem decide
        se rejeita ou penaliza é o método de busca (decisão 4 do PLANEJAMENTO.md).
        Um osm_id desconhecido torna o roteiro inviável, com tempo infinito.
        """
        self.avaliacoes += 1
        if any(o not in self._indice for o in roteiro):
            return 0.0, math.inf, False
        tempo = self.tempo(roteiro)
        sem_repeticao = len(set(roteiro)) == len(roteiro)
        viavel = sem_repeticao and tempo <= self.cenario.orcamento_min + TOLERANCIA_MIN
        return self.utilidade(roteiro), tempo, viavel

    def zerar_contador(self) -> None:
        self.avaliacoes = 0
