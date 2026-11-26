"""Vizinhança do roteiro: inserção, remoção e troca de posições (P5).

Dono: Integrante 2. Ver BACKLOG.md.

Todos os movimentos devolvem uma lista NOVA e nunca alteram o roteiro recebido.
A inserção só usa locais que ainda não estão no roteiro, então nenhum movimento
cria repetição (caso A1). A viabilidade de tempo NÃO é verificada aqui: isso é
papel de `problema.Avaliador.avaliar()`, que conta a avaliação.

O `rng` pode ser `random.Random(semente)` ou `numpy.random.default_rng(semente)`:
os sorteios usam só índices inteiros, e a mesma semente gera a mesma sequência.
"""

MOVIMENTOS = ("inserir", "remover", "trocar")


def inserir(roteiro: list, local, posicao: int) -> list:
    """Insere `local` antes da posição `posicao` (0 = primeiro, len = último)."""
    if local in roteiro:
        raise ValueError(f"O local {local!r} já está no roteiro.")
    if not 0 <= posicao <= len(roteiro):
        raise IndexError(f"Posição de inserção {posicao} fora de 0..{len(roteiro)}.")
    novo = list(roteiro)
    novo.insert(posicao, local)
    return novo


def remover(roteiro: list, posicao: int) -> list:
    """Remove o local da posição `posicao`."""
    if not 0 <= posicao < len(roteiro):
        raise IndexError(f"Posição de remoção {posicao} fora de 0..{len(roteiro) - 1}.")
    return roteiro[:posicao] + roteiro[posicao + 1:]


def trocar(roteiro: list, i: int, j: int) -> list:
    """Troca de lugar os locais das posições i e j."""
    n = len(roteiro)
    if not (0 <= i < n and 0 <= j < n):
        raise IndexError(f"Posições de troca ({i}, {j}) fora de 0..{n - 1}.")
    novo = list(roteiro)
    novo[i], novo[j] = novo[j], novo[i]
    return novo


def movimentos_aplicaveis(roteiro: list, todos_os_locais: list) -> list[str]:
    """Movimentos possíveis, na ordem de MOVIMENTOS.

    inserir: há algum local fora do roteiro; remover: o roteiro não está vazio;
    trocar: o roteiro tem pelo menos 2 locais.
    """
    no_roteiro = set(roteiro)
    aplicaveis = []
    if any(l not in no_roteiro for l in todos_os_locais):
        aplicaveis.append("inserir")
    if roteiro:
        aplicaveis.append("remover")
    if len(roteiro) >= 2:
        aplicaveis.append("trocar")
    return aplicaveis


def _sortear(rng, n: int) -> int:
    """Inteiro uniforme em 0..n-1, para random.Random ou numpy.random.Generator."""
    if hasattr(rng, "integers"):
        return int(rng.integers(n))
    return rng.randrange(n)


def sortear_movimento(roteiro: list, todos_os_locais: list, rng) -> tuple[str, list]:
    """Sorteia um movimento aplicável (com a mesma chance) e devolve (nome, novo_roteiro)."""
    aplicaveis = movimentos_aplicaveis(roteiro, todos_os_locais)
    if not aplicaveis:
        raise ValueError("Nenhum movimento possível: não há locais para inserir.")
    movimento = aplicaveis[_sortear(rng, len(aplicaveis))]

    if movimento == "inserir":
        no_roteiro = set(roteiro)
        fora = [l for l in todos_os_locais if l not in no_roteiro]
        local = fora[_sortear(rng, len(fora))]
        return movimento, inserir(roteiro, local, _sortear(rng, len(roteiro) + 1))
    if movimento == "remover":
        return movimento, remover(roteiro, _sortear(rng, len(roteiro)))

    # trocar: duas posições distintas, sorteadas uniformemente
    i = _sortear(rng, len(roteiro))
    j = _sortear(rng, len(roteiro) - 1)
    if j >= i:
        j += 1
    return movimento, trocar(roteiro, i, j)


def vizinho_aleatorio(roteiro: list, todos_os_locais: list, rng) -> list:
    """Sorteia um dos três movimentos e devolve um novo roteiro (nunca altera o original)."""
    return sortear_movimento(roteiro, todos_os_locais, rng)[1]
