# Otimizador de roteiros turísticos em Fortaleza — Questão 2

Trabalho final de Inteligência Artificial, UFC Campus Crateús (Prof. Wellington Franco).

> **Em construção.** Dono deste arquivo: Integrante 5 (item Q6 do `BACKLOG.md`).

Monta uma sequência de visitas a pontos de interesse de Fortaleza (OpenStreetMap) que começa e termina
no ponto de partida do visitante, cabe no tempo disponível e maximiza a soma das preferências dele por
categoria. Compara a construção gulosa, a subida de encosta com reinícios e a têmpera simulada.

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
python scripts/baixar_dados.py     # opcional: data/pois.csv já vem no repositório
python scripts/experimentos.py
streamlit run app/app.py
pytest
```

## Dados
© OpenStreetMap contributors, licença ODbL (https://www.openstreetmap.org/copyright). Detalhes em `DADOS.md`.

## Integrantes
| Papel | Nome | Matrícula |
|---|---|---|
| Dados | | |
| Modelo do problema | | |
| Busca local e experimento | | |
| Interface | | |
| Persistência, qualidade e entrega | | |
