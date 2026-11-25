"""Previsão de um dia, usada IGUALMENTE pelo script e pela interface (I2).

Dono: Integrante 4. Ver BACKLOG.md.
"""
from datetime import date

from energia.contratos import HistoricoInsuficiente  # noqa: F401


def prever(data_alvo: date, historico, modelo) -> float:
    """Retorna o kWh previsto para data_alvo.

    Levanta HistoricoInsuficiente (com explicação) se faltar algum dos 7 dias anteriores.
    """
    raise NotImplementedError
