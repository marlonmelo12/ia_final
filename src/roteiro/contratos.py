"""Contratos compartilhados entre os módulos (Questão 2: otimizador de roteiros turísticos).

Guardião: Integrante 5. CONGELADO após Q2 (26/11/2026).
Qualquer mudança exige PR com título "CONTRATO:" aprovado pelos 5 integrantes.
"""
from pathlib import Path

# --- Caminhos -------------------------------------------------------------
RAIZ = Path(__file__).resolve().parents[2]
DIR_RAW = RAIZ / "data" / "raw"
DIR_RESULTADOS = RAIZ / "resultados"
ARQ_OSM_BRUTO = DIR_RAW / "pois_osm.geojson"   # saída bruta do OSMnx (fora do Git)
ARQ_POIS = RAIZ / "data" / "pois.csv"          # os 20 locais selecionados (versionado)
ARQ_CENARIOS = RAIZ / "data" / "cenarios.csv"  # os 10 cenários do experimento (versionado)
ARQ_BANCO = RAIZ / "execucoes.db"

# --- Fonte (enunciado, Questão 2) -----------------------------------------
LOCALIDADE = "Fortaleza, Ceará, Brazil"
TAGS_OSM = {"tourism": ["attraction", "museum"], "leisure": ["park"]}
N_LOCAIS = 20
ATRIBUICAO_OSM = "© OpenStreetMap contributors (ODbL) — https://www.openstreetmap.org/copyright"

# Categoria interna de cada local. Se um elemento tiver mais de uma tag,
# vale a primeira desta tupla (decisão 2 do PLANEJAMENTO.md).
CATEGORIAS = ("museum", "attraction", "park")

# --- Modelo definido pelo enunciado (hipóteses acadêmicas) ----------------
DURACAO_VISITA_MIN = 30.0
VELOCIDADE_KMH = 4.0          # deslocamento = distância geodésica / 4 km/h
RAIO_TERRA_KM = 6371.0088     # raio médio, usado na fórmula de haversine
PREFERENCIA_MIN, PREFERENCIA_MAX = 1, 5
ORCAMENTOS_MIN = (120, 180, 240)

# --- Protocolo experimental -----------------------------------------------
SEMENTES_EXPERIMENTO = (0, 1, 2, 3, 4)      # únicas sementes do experimento final
SEMENTES_AJUSTE = (100, 101, 102, 103, 104)  # sementes para ajustar parâmetros antes de 02/12
N_CENARIOS = 10
MAX_AVALIACOES = 5000         # mesmo orçamento de avaliações da função objetivo para HC e SA
METODOS = ("guloso", "subida_reinicios", "tempera")

# Parâmetros declarados (valores iniciais; congelar até 01/12, decisão 6 do PLANEJAMENTO.md)
PARAMS_SUBIDA = {"n_reinicios": 20, "vizinhos_por_passo": 50}
PARAMS_TEMPERA = {"t_inicial": 2.0, "resfriamento": 0.995, "t_minima": 1e-3}

# --- Esquemas dos arquivos ------------------------------------------------
# pois.csv: um local por linha, já selecionado e com ponto representativo
COLUNAS_POIS = ["osm_id", "nome", "categoria", "lat", "lon"]
# cenarios.csv: preferências inteiras de 1 a 5, uma coluna por categoria
COLUNAS_CENARIOS = [
    "cenario", "descricao", "lat_partida", "lon_partida", "orcamento_min",
    *[f"pref_{c}" for c in CATEGORIAS],
]
# Uma linha por visita no roteiro exportado
COLUNAS_ROTEIRO = [
    "ordem", "osm_id", "nome", "categoria", "preferencia",
    "chegada_min", "saida_min", "deslocamento_min",
]


# --- Exceções -------------------------------------------------------------
class SemSolucaoViavel(ValueError):
    """Nenhum local cabe no orçamento (ida + visita + volta); o roteiro é vazio, com explicação."""


class EntradaInvalida(ValueError):
    """Entrada do usuário fora do formato ou dos limites (coordenada, orçamento, preferência)."""
