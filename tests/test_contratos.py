"""Sanidade dos contratos compartilhados. Dono: Integrante 5."""
from energia import contratos as c


def test_particoes_em_ordem_e_sem_sobreposicao():
    assert c.TREINO[1] < c.VALIDACAO[0]
    assert c.VALIDACAO[1] < c.TESTE[0]
    assert c.TREINO[0] == c.INICIO_RECORTE
    assert c.TESTE[1] == c.FIM_RECORTE


def test_atributos_contem_lags_e_calendario():
    for col in c.COLUNAS_LAGS + c.COLUNAS_CALENDARIO:
        assert col in c.COLUNAS_ATRIBUTOS
