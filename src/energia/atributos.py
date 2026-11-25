"""Reindexação do calendário, defasagens, calendário do alvo e divisão cronológica (A1-A6).

Dono: Integrante 2. Ver BACKLOG.md.
"""
import pandas as pd


def reindexar_calendario(diario: pd.DataFrame) -> pd.DataFrame:
    """A1: uma linha por dia; dias ausentes com kwh vazio."""
    raise NotImplementedError


def construir_atributos(diario: pd.DataFrame) -> pd.DataFrame:
    """A2-A5: retorna COLUNAS_ATRIBUTOS, sem linhas com valores ausentes."""
    raise NotImplementedError
