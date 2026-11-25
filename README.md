# Previsão do consumo diário de energia — Questão 6

Trabalho final de Inteligência Artificial, UFC Campus Crateús (Prof. Wellington Franco).

> **Em construção.** Dono deste arquivo: Integrante 5 (item Q6 do `BACKLOG.md`).

Prevê a energia diária (kWh) do dia seguinte de uma residência a partir da base
*UCI Individual Household Electric Power Consumption*, comparando persistência,
regressão linear e Ridge.

## Documentos da equipe
- `PLANEJAMENTO.md`: papéis, arquitetura, cronograma e riscos
- `BACKLOG.md`: tarefas de cada integrante, com prazos e critérios de pronto
- `CONTRIBUTING.md`: fluxo de trabalho no Git (leia antes do primeiro commit)
- `ENTREGA_FINAL.md`: definição do que conta como entregue

## Instalação
```bash
python -m venv .venv
.venv\Scripts\activate      # Linux/Mac: source .venv/bin/activate
pip install -r requirements.txt
pip install -e .
```

## Execução
```bash
python scripts/baixar_dados.py
python scripts/preparar_dados.py
python scripts/treinar.py
python scripts/experimentos.py
streamlit run app/app.py
pytest
```

## Integrantes
| Papel | Nome | Matrícula |
|---|---|---|
| Dados | | |
| Atributos e divisão | | |
| Modelagem e avaliação | | |
| Interface | | |
| Persistência, qualidade e entrega | | |
