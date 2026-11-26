"""D1-D4: obtém os POIs com OSMnx, salva o bruto em data/raw/ e gera data/pois.csv.

Dono: Integrante 1. Ver BACKLOG.md.
"""
import hashlib
from datetime import datetime, timedelta, timezone

import osmnx

from roteiro.contratos import ARQ_OSM_BRUTO, LOCALIDADE, RAIZ, TAGS_OSM
from roteiro.dados import baixar_features

FORTALEZA = timezone(timedelta(hours=-3))


def sha256(caminho):
    h = hashlib.sha256()
    with open(caminho, "rb") as f:
        for bloco in iter(lambda: f.read(1 << 20), b""):
            h.update(bloco)
    return h.hexdigest()


def main():
    acesso = datetime.now(FORTALEZA)
    print(f"Consulta: features_from_place({LOCALIDADE!r}, {TAGS_OSM})")
    bruto = baixar_features()

    print(f"Data de acesso: {acesso:%d/%m/%Y %H:%M} (horário de Fortaleza, UTC-3)")
    print(f"Versão do OSMnx: {osmnx.__version__}")
    print(f"Arquivo bruto: {ARQ_OSM_BRUTO.relative_to(RAIZ).as_posix()}")
    print(f"SHA-256: {sha256(ARQ_OSM_BRUTO)}")
    print(f"Elementos retornados: {len(bruto)}")


if __name__ == "__main__":
    main()
