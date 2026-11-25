"""Leitura da base UCI, recorte 2007-2009 e agregação diária em kWh (D2-D4).

Dono: Integrante 1. Ver BACKLOG.md.

Regras (enunciado, Questão 6):
- usar Date, Time e Global_active_power (kW, uma medição por minuto);
- o marcador "?" vira valor faltante;
- energia do minuto em kWh = potência (kW) / 60; energia do dia = soma dos minutos;
- só valem dias completos, com 1.440 medições válidas; nunca usar soma parcial de um dia.
"""
from datetime import date

import pandas as pd

from energia.contratos import (
    COLUNAS_DIARIO,
    FIM_RECORTE,
    INICIO_RECORTE,
    MEDICOES_POR_DIA,
)

COLUNAS_FONTE = ["Date", "Time", "Global_active_power"]


def ler_bruto(caminho) -> pd.DataFrame:
    """D2: lê só as colunas necessárias; "?" vira NaN.

    Retorna DataFrame com colunas `momento` (datetime64) e `potencia_kw` (float).
    """
    bruto = pd.read_csv(
        caminho,
        sep=";",
        usecols=COLUNAS_FONTE,
        na_values=["?"],
        dtype={"Date": "string", "Time": "string", "Global_active_power": "float64"},
        engine="c",
    )
    momento = pd.to_datetime(bruto["Date"] + " " + bruto["Time"], format="%d/%m/%Y %H:%M:%S")
    return pd.DataFrame({"momento": momento, "potencia_kw": bruto["Global_active_power"]})


def recortar(bruto: pd.DataFrame, inicio: date = INICIO_RECORTE, fim: date = FIM_RECORTE) -> pd.DataFrame:
    """Mantém as medições com data entre `inicio` e `fim`, inclusive."""
    dia = bruto["momento"].dt.date
    return bruto.loc[(dia >= inicio) & (dia <= fim)].reset_index(drop=True)


def agregar_diario(bruto: pd.DataFrame) -> pd.DataFrame:
    """D3: uma linha por dia que aparece nas medições, com COLUNAS_DIARIO.

    - `n_medicoes`: minutos distintos com potência válida no dia;
    - `kwh`: soma de potência/60, preenchido SÓ quando n_medicoes == 1.440.

    Timestamps duplicados (se houver) contam uma única vez, mantendo a primeira leitura.
    A reindexação para o calendário completo é feita no módulo de atributos (A1).
    """
    validas = (
        bruto.dropna(subset=["potencia_kw"])
        .drop_duplicates(subset="momento", keep="first")
        .assign(data=lambda d: d["momento"].dt.normalize(), kwh_minuto=lambda d: d["potencia_kw"] / 60)
    )
    dias = bruto["momento"].dt.normalize().drop_duplicates().sort_values()

    por_dia = validas.groupby("data").agg(kwh=("kwh_minuto", "sum"), n_medicoes=("kwh_minuto", "size"))
    diario = por_dia.reindex(dias.values).rename_axis("data").reset_index()
    diario["n_medicoes"] = diario["n_medicoes"].fillna(0).astype(int)
    diario.loc[diario["n_medicoes"] != MEDICOES_POR_DIA, "kwh"] = float("nan")
    diario["data"] = diario["data"].dt.date
    return diario[COLUNAS_DIARIO]


def contar(bruto: pd.DataFrame, recorte: pd.DataFrame, diario: pd.DataFrame) -> dict:
    """D4: contagens para o DADOS.md e o relatório."""
    incompletos = diario[diario["kwh"].isna()]
    return {
        "registros_brutos": len(bruto),
        "periodo_bruto": f"{bruto['momento'].min()} a {bruto['momento'].max()}",
        "registros_no_recorte": len(recorte),
        "faltantes_no_recorte": int(recorte["potencia_kw"].isna().sum()),
        "timestamps_duplicados": int(recorte["momento"].duplicated().sum()),
        "dias_no_recorte": len(diario),
        "dias_completos": int(diario["kwh"].notna().sum()),
        "dias_excluidos": len(incompletos),
        "dias_sem_nenhuma_medicao": int((incompletos["n_medicoes"] == 0).sum()),
    }


def gerar_diario(caminho_bruto, destino) -> dict:
    """D3/D4: lê o bruto, recorta 2007-2009, agrega por dia, salva o CSV e retorna as contagens."""
    bruto = ler_bruto(caminho_bruto)
    recorte = recortar(bruto)
    diario = agregar_diario(recorte)
    destino.parent.mkdir(parents=True, exist_ok=True)
    diario.to_csv(destino, index=False, float_format="%.6f")
    return contar(bruto, recorte, diario)


if __name__ == "__main__":
    from energia.contratos import ARQ_DIARIO, DIR_RAW

    contagens = gerar_diario(DIR_RAW / "household_power_consumption.txt", ARQ_DIARIO)
    print(f"Gerado: {ARQ_DIARIO}")
    for chave, valor in contagens.items():
        print(f"  {chave}: {valor}")
