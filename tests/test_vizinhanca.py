"""Caso A1 (nenhum local repetido). Dono: Integrante 2."""
import random
from collections import Counter

import pytest

from roteiro.vizinhanca import (
    MOVIMENTOS,
    inserir,
    movimentos_aplicaveis,
    remover,
    sortear_movimento,
    trocar,
    vizinho_aleatorio,
)

LOCAIS = [f"L{i}" for i in range(20)]


def _geradores(semente):
    """Os dois tipos de rng aceitos pela vizinhança."""
    yield random.Random(semente)
    np = pytest.importorskip("numpy")
    yield np.random.default_rng(semente)


# --- Movimentos individuais -----------------------------------------------
def test_inserir():
    assert inserir(["A", "B"], "X", 0) == ["X", "A", "B"]
    assert inserir(["A", "B"], "X", 1) == ["A", "X", "B"]
    assert inserir(["A", "B"], "X", 2) == ["A", "B", "X"]
    assert inserir([], "X", 0) == ["X"]


def test_remover():
    assert remover(["A", "B", "C"], 0) == ["B", "C"]
    assert remover(["A", "B", "C"], 2) == ["A", "B"]


def test_trocar():
    assert trocar(["A", "B", "C"], 0, 2) == ["C", "B", "A"]


def test_inserir_local_ja_presente_e_erro():
    with pytest.raises(ValueError):
        inserir(["A", "B"], "A", 1)


@pytest.mark.parametrize(
    "chamada",
    [
        lambda r: inserir(r, "X", 4),
        lambda r: inserir(r, "X", -1),
        lambda r: remover(r, 3),
        lambda r: remover([], 0),
        lambda r: trocar(r, 0, 3),
    ],
)
def test_posicao_invalida_e_erro(chamada):
    with pytest.raises(IndexError):
        chamada(["A", "B", "C"])


def test_movimentos_nunca_alteram_o_original():
    original = ["A", "B", "C"]
    copia = list(original)
    inserir(original, "X", 1)
    remover(original, 1)
    trocar(original, 0, 2)
    for rng in _geradores(100):
        for _ in range(50):
            vizinho_aleatorio(original, ["A", "B", "C", "X", "Y"], rng)
    assert original == copia


# --- Movimentos aplicáveis ------------------------------------------------
def test_movimentos_aplicaveis_nos_casos_limite():
    assert movimentos_aplicaveis([], LOCAIS) == ["inserir"]
    assert movimentos_aplicaveis(["L0"], LOCAIS) == ["inserir", "remover"]
    assert movimentos_aplicaveis(["L0", "L1"], LOCAIS) == list(MOVIMENTOS)
    assert movimentos_aplicaveis(list(LOCAIS), LOCAIS) == ["remover", "trocar"]


def test_sem_locais_e_roteiro_vazio_e_erro():
    with pytest.raises(ValueError):
        vizinho_aleatorio([], [], random.Random(100))


# --- Caso A1: passeio aleatório longo, sem repetição ----------------------
@pytest.mark.parametrize("semente", [100, 101, 102])
def test_a1_nenhum_vizinho_repete_local(semente):
    for rng in _geradores(semente):
        roteiro, vistos = [], Counter()
        for _ in range(2000):
            movimento, roteiro = sortear_movimento(roteiro, LOCAIS, rng)
            vistos[movimento] += 1
            assert len(set(roteiro)) == len(roteiro)
            assert set(roteiro) <= set(LOCAIS)
        assert set(vistos) == set(MOVIMENTOS)


def test_trocar_sorteado_muda_a_ordem_e_mantem_os_locais():
    rng = random.Random(100)
    roteiro = ["L0", "L1", "L2", "L3"]
    trocas = 0
    for _ in range(500):
        movimento, novo = sortear_movimento(roteiro, roteiro, rng)  # nada a inserir
        if movimento == "trocar":
            trocas += 1
            assert novo != roteiro and sorted(novo) == sorted(roteiro)
    assert trocas > 0


# --- Reprodutibilidade (base do caso A6) ----------------------------------
def _sequencia(rng, passos=300):
    roteiro, saida = [], []
    for _ in range(passos):
        roteiro = vizinho_aleatorio(roteiro, LOCAIS, rng)
        saida.append(tuple(roteiro))
    return saida


def test_mesma_semente_mesma_sequencia_de_vizinhos():
    assert _sequencia(random.Random(100)) == _sequencia(random.Random(100))
    np = pytest.importorskip("numpy")
    assert _sequencia(np.random.default_rng(100)) == _sequencia(np.random.default_rng(100))


def test_sementes_diferentes_geram_sequencias_diferentes():
    assert _sequencia(random.Random(100)) != _sequencia(random.Random(101))
