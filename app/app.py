"""Interface Streamlit. Dono: Integrante 4. Ver BACKLOG.md (I1-I8).

Executar: streamlit run app/app.py
"""
import streamlit as st

st.set_page_config(page_title="Otimizador de roteiros turísticos", layout="wide")
st.title("Otimizador de roteiros turísticos — Fortaleza")
st.caption(
    "Protótipo acadêmico. Visita de 30 min e deslocamento a 4 km/h em linha reta são hipóteses, "
    "não tempos reais de caminhada. Dados: © OpenStreetMap contributors (ODbL)."
)

aba_roteiro, aba_comparar, aba_historico = st.tabs(["Montar roteiro", "Comparar métodos", "Histórico"])
with aba_roteiro:
    st.info("I3: ponto de partida, tempo disponível, preferências 1-5 e método; sequência, mapa, tempo e retorno.")
with aba_comparar:
    st.info("I4/I5: guloso x subida de encosta x têmpera no mesmo cenário; exportação do roteiro.")
with aba_historico:
    st.info("I6: execuções registradas, consulta e exportação.")
