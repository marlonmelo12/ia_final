"""Casos A1 e A2 (agregação diária e exclusão de dias incompletos). Dono: Integrante 1."""
import math
from datetime import date

import pandas as pd
import pytest

from energia.contratos import COLUNAS_DIARIO, DIR_RAW, MEDICOES_POR_DIA
from energia.dados import agregar_diario, ler_bruto, recortar

ARQ_BRUTO = DIR_RAW / "household_power_consumption.txt"


def _dia(data_iso, potencias):
    """Gera medições por minuto a partir de 00:00 com as potências dadas (None = "?")."""
    inicio = pd.Timestamp(data_iso)
    return pd.DataFrame({
        "momento": [inicio + pd.Timedelta(minutes=i) for i in range(len(potencias))],
        "potencia_kw": [float("nan") if p is None else p for p in potencias],
    })


def test_a1_dia_completo_soma_potencia_sobre_60():
    bruto = _dia("2007-03-01", [1.2] * MEDICOES_POR_DIA)
    diario = agregar_diario(bruto)
    assert list(diario.columns) == COLUNAS_DIARIO
    linha = diario.iloc[0]
    assert linha["data"] == date(2007, 3, 1)
    assert linha["n_medicoes"] == MEDICOES_POR_DIA
    assert linha["kwh"] == pytest.approx(1.2 * 1440 / 60, abs=1e-9)  # 28,8 kWh


def test_a2_dia_com_um_minuto_faltante_fica_sem_kwh():
    potencias = [2.0] * MEDICOES_POR_DIA
    potencias[700] = None
    diario = agregar_diario(_dia("2007-03-02", potencias))
    assert diario.iloc[0]["n_medicoes"] == MEDICOES_POR_DIA - 1
    assert math.isnan(diario.iloc[0]["kwh"])  # nunca soma parcial


def test_a2_dia_sem_nenhuma_medicao_valida_aparece_com_zero():
    diario = agregar_diario(_dia("2007-03-03", [None] * MEDICOES_POR_DIA))
    assert diario.iloc[0]["n_medicoes"] == 0
    assert math.isnan(diario.iloc[0]["kwh"])


def test_minuto_duplicado_conta_uma_vez():
    bruto = _dia("2007-03-04", [1.0] * MEDICOES_POR_DIA)
    bruto = pd.concat([bruto, bruto.iloc[[10]]], ignore_index=True)
    linha = agregar_diario(bruto).iloc[0]
    assert linha["n_medicoes"] == MEDICOES_POR_DIA
    assert linha["kwh"] == pytest.approx(24.0)


def test_recorte_respeita_limites_inclusivos():
    bruto = pd.concat([
        _dia("2006-12-31", [1.0]), _dia("2007-01-01", [1.0]),
        _dia("2009-12-31", [1.0]), _dia("2010-01-01", [1.0]),
    ], ignore_index=True)
    dias = set(recortar(bruto)["momento"].dt.date)
    assert dias == {date(2007, 1, 1), date(2009, 12, 31)}


def test_ler_bruto_converte_interrogacao_em_nan(tmp_path):
    arq = tmp_path / "mini.txt"
    arq.write_text(
        "Date;Time;Global_active_power;Global_reactive_power\n"
        "1/1/2007;00:00:00;2.580;0.136\n"
        "1/1/2007;00:01:00;?;?\n",
        encoding="utf-8",
    )
    bruto = ler_bruto(arq)
    assert list(bruto.columns) == ["momento", "potencia_kw"]
    assert bruto["momento"].iloc[1] == pd.Timestamp("2007-01-01 00:01:00")
    assert bruto["potencia_kw"].iloc[0] == pytest.approx(2.58)
    assert math.isnan(bruto["potencia_kw"].iloc[1])


# --- Verificação manual na base real (caso A1) -------------------------------
# Valores de referência calculados de forma independente com awk sobre o arquivo bruto:
#   awk -F';' -v d="2/1/2007" '$1==d && $3!="?" {s+=$3; n++} END {print n, s/60}' household_power_consumption.txt
REFERENCIA_MANUAL = {
    date(2007, 1, 2): (1440, 21.153933),
    date(2008, 6, 15): (1440, 38.151700),
    date(2007, 1, 14): (1439, None),  # falta 1 minuto -> excluído
}


@pytest.mark.skipif(not ARQ_BRUTO.exists(), reason="base real ausente; rode scripts/baixar_dados.py")
def test_a1_base_real_bate_com_calculo_manual():
    diario = agregar_diario(recortar(ler_bruto(ARQ_BRUTO))).set_index("data")
    assert len(diario) == 1096  # 2007 + 2008 (bissexto) + 2009
    for dia, (n, kwh) in REFERENCIA_MANUAL.items():
        assert diario.loc[dia, "n_medicoes"] == n
        if kwh is None:
            assert math.isnan(diario.loc[dia, "kwh"])
        else:
            assert diario.loc[dia, "kwh"] == pytest.approx(kwh, abs=1e-6)
