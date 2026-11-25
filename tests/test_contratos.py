"""Sanidade dos contratos compartilhados. Dono: Integrante 5."""
from roteiro import contratos as c


def test_parametros_do_enunciado():
    assert c.DURACAO_VISITA_MIN == 30
    assert c.VELOCIDADE_KMH == 4
    assert c.ORCAMENTOS_MIN == (120, 180, 240)
    assert c.N_LOCAIS == 20
    assert len(c.SEMENTES_EXPERIMENTO) >= 5


def test_sementes_de_ajuste_separadas_do_experimento():
    assert not set(c.SEMENTES_AJUSTE) & set(c.SEMENTES_EXPERIMENTO)


def test_uma_preferencia_por_categoria():
    for cat in c.CATEGORIAS:
        assert f"pref_{cat}" in c.COLUNAS_CENARIOS
