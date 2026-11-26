"""Obtenção e preparação dos pontos de interesse do OpenStreetMap (D2-D4).

Dono: Integrante 1. Ver BACKLOG.md.
"""
import pandas as pd

from roteiro.contratos import ARQ_OSM_BRUTO, LOCALIDADE, RAIZ, TAGS_OSM


def baixar_features(destino=ARQ_OSM_BRUTO):
    """Chama osmnx.features_from_place(LOCALIDADE, TAGS_OSM), salva o bruto em GeoJSON
    e devolve o GeoDataFrame.

    O índice (element, id) do OSMnx vira a coluna `osm_id` no formato "node/123".
    Colunas com listas ou dicionários (por exemplo `nodes` dos ways) viram texto,
    porque o GeoJSON só aceita valores simples nas propriedades.
    """
    import osmnx as ox

    ox.settings.cache_folder = str(RAIZ / "cache")
    bruto = ox.features_from_place(LOCALIDADE, TAGS_OSM)

    bruto = bruto.reset_index()
    bruto.insert(0, "osm_id", bruto["element"] + "/" + bruto["id"].astype(str))
    bruto = bruto.drop(columns=["element", "id"])
    composto = (list, dict, set, tuple)
    for col in bruto.columns.drop("geometry"):
        bruto[col] = bruto[col].map(lambda v: str(v) if isinstance(v, composto) else v)
    bruto = bruto.sort_values("osm_id").reset_index(drop=True)

    destino.parent.mkdir(parents=True, exist_ok=True)
    bruto.to_file(destino, driver="GeoJSON")
    return bruto


def preparar_pois(bruto) -> pd.DataFrame:
    """Filtra locais com nome, define a categoria, calcula o ponto representativo dos
    polígonos, remove duplicados e seleciona N_LOCAIS pela regra da decisão 1.

    Devolve um DataFrame com as colunas COLUNAS_POIS.
    """
    raise NotImplementedError


def carregar_pois() -> pd.DataFrame:
    """Lê data/pois.csv e valida as colunas."""
    raise NotImplementedError
