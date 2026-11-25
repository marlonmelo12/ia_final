"""Obtenção e preparação dos pontos de interesse do OpenStreetMap (D2-D4).

Dono: Integrante 1. Ver BACKLOG.md.
"""
import pandas as pd


def baixar_features():
    """Chama osmnx.features_from_place(LOCALIDADE, TAGS_OSM) e devolve o GeoDataFrame bruto."""
    raise NotImplementedError


def preparar_pois(bruto) -> pd.DataFrame:
    """Filtra locais com nome, define a categoria, calcula o ponto representativo dos
    polígonos, remove duplicados e seleciona N_LOCAIS pela regra da decisão 1.

    Devolve um DataFrame com as colunas COLUNAS_POIS.
    """
    raise NotImplementedError


def carregar_pois() -> pd.DataFrame:
    """Lê data/pois.csv e valida as colunas."""
    raise NotImplementedError
