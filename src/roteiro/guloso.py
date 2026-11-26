"""Construção gulosa: prioriza ganho de interesse por incremento de tempo (P6).

Dono: Integrante 2. Ver BACKLOG.md.

A cada passo, testa todo local ainda não visitado em toda posição de inserção e fica com o
candidato VIÁVEL de maior razão

    preferência do local / acréscimo de tempo do roteiro

(o acréscimo inclui o desvio no trajeto e os 30 min da visita, então é sempre > 0).
Para quando nenhum local cabe em nenhuma posição.

Empates: vale o primeiro candidato encontrado, ou seja, o local que vem antes na ordem
do pois.csv e, para o mesmo local, a menor posição. O resultado é determinístico.

Cada candidato passa por `avaliador.avaliar()`, então `avaliador.avaliacoes` registra
quantas avaliações o guloso gastou, comparável com as da busca local.
"""

# Diferença mínima de razão para trocar de candidato (evita que ruído de ponto
# flutuante desfaça a regra de desempate).
_EPS = 1e-12


def construir(avaliador) -> list:
    """A cada passo insere o local (e a posição) com maior preferência / acréscimo de tempo
    que mantém o roteiro viável. Para quando nenhum local cabe."""
    roteiro: list = []
    tempo_atual = 0.0
    while True:
        visitados = set(roteiro)
        melhor = None  # (razao, candidato, tempo)
        for local in avaliador.locais:
            if local in visitados:
                continue
            for posicao in range(len(roteiro) + 1):
                candidato = roteiro[:posicao] + [local] + roteiro[posicao:]
                _, tempo, viavel = avaliador.avaliar(candidato)
                if not viavel:
                    continue
                razao = avaliador.preferencia[local] / (tempo - tempo_atual)
                if melhor is None or razao > melhor[0] + _EPS:
                    melhor = (razao, candidato, tempo)
        if melhor is None:
            return roteiro
        _, roteiro, tempo_atual = melhor
