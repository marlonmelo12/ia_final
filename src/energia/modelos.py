"""Persistência, regressão linear e Ridge; seleção de alpha na validação (M1-M4).

Dono: Integrante 3. Ver BACKLOG.md.
"""


def treinar(atributos, nome_modelo: str, **params):
    """M2/M3: ajusta usando somente a partição "treino"."""
    raise NotImplementedError


def salvar_modelo(modelo, metadados: dict, nome: str) -> None:
    """M4: salva em DIR_MODELOS/<nome>.joblib com metadados (versão, alpha, datas, atributos)."""
    raise NotImplementedError


def carregar_modelo(nome: str):
    """M4: retorna (modelo, metadados)."""
    raise NotImplementedError
