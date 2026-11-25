"""Interface Streamlit. Dono: Integrante 4. Ver BACKLOG.md (I1-I8).

Executar: streamlit run app/app.py
"""
import streamlit as st

st.set_page_config(page_title="Previsão de consumo de energia", layout="wide")
st.title("Previsão do consumo diário de energia")
st.caption("Protótipo acadêmico. Base: UCI Individual Household Electric Power Consumption.")

aba_prever, aba_avaliar, aba_historico = st.tabs(["Prever", "Avaliar período", "Histórico"])
with aba_prever:
    st.info("I3: escolha da data, janela histórica e previsão em kWh.")
with aba_avaliar:
    st.info("I4/I5: observado vs previsto, MAE/RMSE e exportação.")
with aba_historico:
    st.info("I6: execuções registradas.")
