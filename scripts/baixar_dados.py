"""D1: baixa o .zip da UCI, extrai em data/raw/ e imprime o SHA-256.

Dono: Integrante 1. Ver BACKLOG.md.

Uso:
    python scripts/baixar_dados.py            # baixa (se ainda não existir) e extrai
    python scripts/baixar_dados.py --forcar   # baixa de novo mesmo se o .zip existir
"""
import argparse
import hashlib
import sys
import zipfile
from datetime import datetime, timezone

import requests

from energia.contratos import DIR_RAW, URL_BASE

ARQ_ZIP = DIR_RAW / "individual_household_electric_power_consumption.zip"
ARQ_TXT = "household_power_consumption.txt"


def sha256(caminho, bloco=1 << 20) -> str:
    h = hashlib.sha256()
    with open(caminho, "rb") as f:
        while parte := f.read(bloco):
            h.update(parte)
    return h.hexdigest()


def baixar(url, destino) -> None:
    temporario = destino.with_suffix(".parcial")
    with requests.get(url, stream=True, timeout=60) as resp:
        resp.raise_for_status()
        with open(temporario, "wb") as f:
            for parte in resp.iter_content(chunk_size=1 << 20):
                f.write(parte)
    temporario.replace(destino)


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--forcar", action="store_true", help="baixa novamente o .zip")
    args = parser.parse_args(argv)

    DIR_RAW.mkdir(parents=True, exist_ok=True)

    if args.forcar or not ARQ_ZIP.exists():
        print(f"Baixando {URL_BASE}")
        try:
            baixar(URL_BASE, ARQ_ZIP)
        except requests.RequestException as erro:
            print(f"Falha no download: {erro}", file=sys.stderr)
            return 1
        print(f"Acesso em: {datetime.now(timezone.utc):%Y-%m-%d %H:%M} UTC")
    else:
        print(f"Usando arquivo existente: {ARQ_ZIP.name} (use --forcar para baixar de novo)")

    with zipfile.ZipFile(ARQ_ZIP) as z:
        if ARQ_TXT not in z.namelist():
            print(f"{ARQ_TXT} não encontrado no .zip: {z.namelist()}", file=sys.stderr)
            return 1
        z.extract(ARQ_TXT, DIR_RAW)

    print(f"Arquivo .zip:    {ARQ_ZIP.name} ({ARQ_ZIP.stat().st_size:,} bytes)")
    print(f"SHA-256 (.zip):  {sha256(ARQ_ZIP)}")
    txt = DIR_RAW / ARQ_TXT
    print(f"Arquivo extraído: {txt.name} ({txt.stat().st_size:,} bytes)")
    print(f"SHA-256 (.txt):  {sha256(txt)}")
    print("Registre os hashes e a data de acesso em DADOS.md.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
