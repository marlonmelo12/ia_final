"""Casos A2 e A3 (tempo recalculado, orçamento insuficiente) e o guloso (P6). Dono: Integrante 2.

Os locais fictícios ficam sobre o meridiano 0 e o equador. Nesses casos, a distância de
haversine é exatamente R * Δângulo, então o tempo esperado pode ser calculado à mão:
cada 0,01° vale PERNA_MIN minutos a 4 km/h.
"""
import math
import random

import pytest

from roteiro.contratos import DURACAO_VISITA_MIN, RAIO_TERRA_KM, EntradaInvalida
from roteiro.guloso import construir
from roteiro.problema import Avaliador, Cenario, haversine_km

KM_POR_GRAU = 2 * math.pi * RAIO_TERRA_KM / 360  # ≈ 111,19508 km
PERNA_MIN = KM_POR_GRAU * 0.01 / 4 * 60           # 0,01° a 4 km/h ≈ 16,679 min

POIS = [
    {"osm_id": "A", "nome": "Museu A", "categoria": "museum", "lat": 0.01, "lon": 0.0},
    {"osm_id": "B", "nome": "Atração B", "categoria": "attraction", "lat": 0.02, "lon": 0.0},
    {"osm_id": "C", "nome": "Parque C", "categoria": "park", "lat": 0.03, "lon": 0.0},
    {"osm_id": "D", "nome": "Museu D", "categoria": "museum", "lat": 0.0, "lon": 0.01},
]
PREFS = {"museum": 5, "attraction": 3, "park": 1}


def avaliador(orcamento=240.0, prefs=PREFS):
    return Avaliador(POIS, Cenario(0.0, 0.0, orcamento, prefs))


# --- P1: haversine --------------------------------------------------------
def test_haversine_um_grau_de_latitude():
    # Valor calculado à mão: 2πR/360 = 111,19508 km. Erro tolerado: 1 m.
    assert haversine_km(0, 0, 1, 0) == pytest.approx(111.19508, abs=1e-3)


def test_haversine_simetrico_e_zero_no_mesmo_ponto():
    p, q = (-3.7275, -38.5275), (-3.7227, -38.5199)
    assert haversine_km(*p, *q) == pytest.approx(haversine_km(*q, *p))
    assert haversine_km(*p, *p) == 0.0


def test_haversine_ao_longo_do_equador():
    assert haversine_km(0, 0, 0, 0.01) == pytest.approx(KM_POR_GRAU * 0.01, rel=1e-12)


# --- P2: tempo (caso A2) --------------------------------------------------
def test_tempo_roteiro_calculado_a_mao():
    # partida→A (1 perna), A→B (1), B→C (1), C→partida (3) = 6 pernas + 3 visitas
    esperado = 6 * PERNA_MIN + 3 * DURACAO_VISITA_MIN
    assert avaliador().tempo(["A", "B", "C"]) == pytest.approx(esperado, abs=1e-6)


def test_tempo_inclui_o_retorno():
    # Só ida até C seriam 3 pernas; com o retorno são 6.
    assert avaliador().tempo(["C"]) == pytest.approx(6 * PERNA_MIN + DURACAO_VISITA_MIN, abs=1e-6)


def test_ordem_altera_o_tempo():
    # partida→B (2), B→A (1), A→C (2), C→partida (3) = 8 pernas, contra 6 em A, B, C
    av = avaliador()
    assert av.tempo(["B", "A", "C"]) == pytest.approx(8 * PERNA_MIN + 3 * DURACAO_VISITA_MIN, abs=1e-6)
    assert av.tempo(["B", "A", "C"]) > av.tempo(["A", "B", "C"])


def test_roteiro_vazio():
    av = avaliador()
    assert av.tempo([]) == 0.0
    assert av.avaliar([]) == (0.0, 0.0, True)


# --- P3: avaliação, viabilidade e contador --------------------------------
def test_utilidade_soma_as_preferencias_das_categorias():
    utilidade, _, viavel = avaliador().avaliar(["A", "B", "C", "D"])
    assert utilidade == 5 + 3 + 1 + 5
    assert viavel


def test_orcamento_exato_e_viavel_e_um_pouco_menos_nao():
    tempo = avaliador().tempo(["A", "B"])
    assert avaliador(orcamento=tempo).avaliar(["A", "B"])[2]
    assert not avaliador(orcamento=tempo - 1e-6).avaliar(["A", "B"])[2]


def test_inviavel_mantem_utilidade_e_tempo_reais():
    av = avaliador(orcamento=60.0)
    utilidade, tempo, viavel = av.avaliar(["A", "B"])
    assert not viavel
    assert utilidade == 8
    assert tempo == pytest.approx(av.tempo(["A", "B"]))


def test_repeticao_e_inviavel():
    assert not avaliador().avaliar(["A", "B", "A"])[2]


def test_local_desconhecido_e_inviavel():
    utilidade, tempo, viavel = avaliador().avaliar(["A", "X"])
    assert not viavel and tempo == math.inf


def test_contador_sobe_um_por_avaliacao_e_zera():
    av = avaliador()
    for n in range(1, 4):
        av.avaliar(["A"])
        assert av.avaliacoes == n
    av.zerar_contador()
    assert av.avaliacoes == 0


def test_consultas_nao_contam_avaliacoes():
    av = avaliador()
    av.tempo(["A", "B"])
    av.utilidade(["A", "B"])
    av.deslocamento_min(None, "A")
    assert av.avaliacoes == 0


def test_preferencia_faltando_e_entrada_invalida():
    with pytest.raises(EntradaInvalida):
        avaliador(prefs={"museum": 5, "park": 1})


def test_osm_id_repetido_nos_pois_e_entrada_invalida():
    with pytest.raises(EntradaInvalida):
        Avaliador(POIS + [POIS[0]], Cenario(0.0, 0.0, 240.0, PREFS))


# --- P4: orçamento insuficiente (caso A3) ---------------------------------
# A e D ficam a 1 perna da partida: o menor roteiro possível é 2 pernas + 1 visita.
MINIMO_MIN = 2 * PERNA_MIN + DURACAO_VISITA_MIN  # ≈ 63,36 min


def test_a3_orcamento_insuficiente_explica_local_e_falta():
    av = avaliador(orcamento=30.0)
    diag = av.diagnosticar_orcamento()
    assert diag["osm_id"] == "A"  # empata com D; vale a ordem do pois.csv
    assert diag["nome"] == "Museu A"
    assert diag["tempo_minimo_min"] == pytest.approx(MINIMO_MIN, abs=1e-6)
    assert diag["falta_min"] == pytest.approx(MINIMO_MIN - 30.0, abs=1e-6)
    assert "Museu A" in diag["mensagem"] and "Faltam 33.4 min" in diag["mensagem"]


def test_a3_nenhum_roteiro_nao_vazio_e_viavel():
    av = avaliador(orcamento=30.0)
    assert av.diagnosticar_orcamento() is not None
    assert not any(av.avaliar([o])[2] for o in av.locais)


def test_orcamento_exato_do_local_mais_proximo_nao_e_insuficiente():
    assert avaliador(orcamento=MINIMO_MIN).diagnosticar_orcamento() is None
    assert avaliador(orcamento=MINIMO_MIN - 1e-6).diagnosticar_orcamento() is not None


def test_diagnostico_nao_conta_avaliacoes():
    av = avaliador(orcamento=30.0)
    av.diagnosticar_orcamento()
    assert av.avaliacoes == 0


def test_sem_locais_e_entrada_invalida():
    with pytest.raises(EntradaInvalida):
        Avaliador([], Cenario(0.0, 0.0, 240.0, PREFS)).diagnosticar_orcamento()


def test_aceita_dataframe_do_pois_csv():
    pd = pytest.importorskip("pandas")
    av = Avaliador(pd.DataFrame(POIS), Cenario(0.0, 0.0, 240.0, PREFS))
    assert av.tempo(["A", "B", "C"]) == pytest.approx(avaliador().tempo(["A", "B", "C"]))


# --- P6: construção gulosa ------------------------------------------------
MUSEUS = {"museum": 5, "attraction": 1, "park": 1}
PARQUES = {"museum": 1, "attraction": 1, "park": 5}


def pois_aleatorios(semente, n=20):
    """Locais fictícios espalhados ~3 km em volta da Praça do Ferreira."""
    rng = random.Random(semente)
    return [
        {
            "osm_id": f"P{i}",
            "nome": f"Local {i}",
            "categoria": rng.choice(["museum", "attraction", "park"]),
            "lat": -3.7275 + rng.uniform(-0.03, 0.03),
            "lon": -38.5275 + rng.uniform(-0.03, 0.03),
        }
        for i in range(n)
    ]


def test_guloso_calculado_a_mao_com_empate():
    # Com 70 min só A ou D cabem (63,36 min cada); empatam, e vale A pela ordem.
    assert construir(avaliador(orcamento=70.0, prefs=MUSEUS)) == ["A"]


def test_guloso_preferencias_alteram_o_roteiro():
    # Com 135 min: C sozinho custa 130,08 min. Para quem prefere parques,
    # C (5 / 130,08) vence A (1 / 63,36); para quem prefere museus, A vence e
    # depois entra o museu D (partida→A→D→partida ≈ 116,9 min). [D, A] e [A, D] têm
    # o mesmo tempo (é o mesmo trajeto ao contrário), e o empate fica com a posição 0.
    parques = construir(avaliador(orcamento=135.0, prefs=PARQUES))
    museus = construir(avaliador(orcamento=135.0, prefs=MUSEUS))
    assert parques == ["C"]
    assert museus == ["D", "A"]


def test_guloso_orcamento_insuficiente_devolve_vazio():
    assert construir(avaliador(orcamento=30.0)) == []


@pytest.mark.parametrize("orcamento", [120, 180, 240])
@pytest.mark.parametrize("prefs", [MUSEUS, PARQUES, {"museum": 3, "attraction": 3, "park": 3}])
def test_guloso_viavel_maximal_e_deterministico(orcamento, prefs):
    pois = pois_aleatorios(100)
    av = Avaliador(pois, Cenario(-3.7275, -38.5275, orcamento, prefs))
    roteiro = construir(av)

    assert roteiro, "algum local deveria caber"
    assert len(set(roteiro)) == len(roteiro)                 # A1
    assert av.tempo(roteiro) <= orcamento + 1e-6              # A2
    # Maximal: nenhum local restante cabe em nenhuma posição.
    for local in set(av.locais) - set(roteiro):
        for pos in range(len(roteiro) + 1):
            assert av.tempo(roteiro[:pos] + [local] + roteiro[pos:]) > orcamento
    # Determinístico (base do A6).
    assert construir(Avaliador(pois, Cenario(-3.7275, -38.5275, orcamento, prefs))) == roteiro


def test_guloso_conta_as_avaliacoes_no_avaliador():
    av = avaliador(orcamento=240.0)
    construir(av)
    # Passo 1: 4 locais x 1 posição; cada passo seguinte testa mais candidatos.
    assert av.avaliacoes >= 4
