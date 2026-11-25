"""Contratos compartilhados entre os módulos.

Guardião: Integrante 5. CONGELADO após Q2 (25/11/2026).
Qualquer mudança exige PR com título "CONTRATO:" aprovado pelos 5 integrantes.
"""
from datetime import date
from pathlib import Path

# --- Caminhos -------------------------------------------------------------
RAIZ = Path(__file__).resolve().parents[2]
DIR_RAW = RAIZ / "data" / "raw"
DIR_PROCESSADO = RAIZ / "data" / "processed"
DIR_AMOSTRA = RAIZ / "data" / "amostra"
DIR_MODELOS = RAIZ / "models"
DIR_RESULTADOS = RAIZ / "resultados"
ARQ_DIARIO = DIR_PROCESSADO / "diario.csv"
ARQ_ATRIBUTOS = DIR_PROCESSADO / "atributos.csv"
ARQ_BANCO = RAIZ / "execucoes.db"

# --- Fonte ----------------------------------------------------------------
URL_BASE = (
    "https://archive.ics.uci.edu/static/public/235/"
    "individual+household+electric+power+consumption.zip"
)
MEDICOES_POR_DIA = 1440
SEMENTE = 42

# --- Recorte e divisão cronológica (por data do ALVO) ---------------------
INICIO_RECORTE = date(2007, 1, 1)
FIM_RECORTE = date(2009, 12, 31)
TREINO = (date(2007, 1, 1), date(2008, 12, 31))
VALIDACAO = (date(2009, 1, 1), date(2009, 6, 30))
TESTE = (date(2009, 7, 1), date(2009, 12, 31))

# --- Esquemas dos arquivos ------------------------------------------------
# diario.csv: uma linha por dia do calendário (inclusive incompletos)
COLUNAS_DIARIO = ["data", "kwh", "n_medicoes"]

# atributos.csv: uma linha por dia-alvo válido
COLUNAS_LAGS = ["lag1", "lag2", "lag7", "media7"]
# Codificação final do calendário: decisão 4 do PLANEJAMENTO.md
COLUNAS_CALENDARIO = ["dia_semana", "mes", "fim_de_semana"]
COLUNAS_ATRIBUTOS = ["data", "kwh_alvo", *COLUNAS_LAGS, *COLUNAS_CALENDARIO, "particao"]
PARTICOES = ("treino", "validacao", "teste")

UNIDADE = "kWh"
MODELOS = ("persistencia", "linear", "ridge")


# --- Exceções -------------------------------------------------------------
class HistoricoInsuficiente(ValueError):
    """Faltam os 7 dias completos anteriores necessários para prever a data pedida."""


class EntradaInvalida(ValueError):
    """Entrada do usuário fora do formato ou do período da base."""
