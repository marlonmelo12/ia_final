"""Leitura da base UCI, recorte 2007-2009 e agregação diária em kWh (D2-D4).

Dono: Integrante 1. Ver BACKLOG.md.
"""
import pandas as pd


def ler_bruto(caminho) -> pd.DataFrame:
    """D2: lê Date, Time e Global_active_power; "?" vira NaN; retorna coluna datetime."""
    raise NotImplementedError


def agregar_diario(bruto: pd.DataFrame) -> pd.DataFrame:
    """D3: retorna COLUNAS_DIARIO; kwh vazio quando n_medicoes < MEDICOES_POR_DIA."""
    raise NotImplementedError
