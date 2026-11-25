# Backlog por integrante — Questão 6

Cada item tem um **ID** (use no nome da branch e no commit), um **prazo**, as **dependências** e o
**critério de pronto**. Um item só fica pronto quando o *pull request* for aprovado pelo revisor e
integrado na `main`. Os papéis, a arquitetura e o cronograma estão em `PLANEJAMENTO.md`, e a definição
da entrega em `ENTREGA_FINAL.md`.

**Legenda de prazos:** todas as datas são de 2026. O código congela em **02/12**. A tag e o envio são em **04/12**.

## Mapa de dependências

```
Q2 contratos (25/11) ──┬─► D1..D4 dados ──► A1..A6 atributos ──► M1..M6 modelos ──► I3..I4 interface
                       ├─► I1 esqueleto da interface (dados fictícios)
                       └─► Q3 persistência ───────────────────────────────────────► I6 histórico na interface
```

Enquanto a etapa anterior não fica pronta, cada um trabalha com **dados fictícios no formato do
contrato** (`src/energia/contratos.py`). Assim ninguém fica parado esperando outra parte.

---

## Integrante 1 — Dados (`D`)

**Arquivos sob sua responsabilidade:** `scripts/baixar_dados.py`, `src/energia/dados.py`, `tests/test_agregacao.py`, `DADOS.md`, `data/amostra/`, `relatorio/secoes/01_dados.md`
**Revisa os PRs de:** Integrante 2

| ID | Tarefa | Prazo | Depende de | Pronto quando |
|---|---|---|---|---|
| D1 | Script de download do .zip da UCI, extração em `data/raw/` e cálculo do **SHA-256** | 26/11 | Q2 | Roda em um clone limpo; o hash é impresso e registrado no `DADOS.md` |
| D2 | Leitura otimizada: só `Date`, `Time` e `Global_active_power`; `?` vira NaN; data e hora num único `datetime` | 26/11 | D1 | Lê o arquivo inteiro em menos de 1 min; os tipos estão corretos |
| D3 | Recorte de 2007 a 2009 e agregação diária: `kwh = soma(potência/60)` e `n_medicoes` por dia, gerando `diario.csv` | 27/11 | D2 | `diario.csv` segue o contrato `COLUNAS_DIARIO`; dia com faltas tem `kwh` vazio |
| D4 | Contagens: registros brutos, registros no recorte, faltantes, dias completos e dias excluídos | 27/11 | D3 | As contagens são impressas pelo script e copiadas para o `DADOS.md` |
| D5 | **Verificação manual** de um dia (caso A1) e testes `test_agregacao.py` (casos A1 e A2) | 28/11 | D3 | `pytest tests/test_agregacao.py` passa; o cálculo manual está documentado |
| D6 | `DADOS.md` completo: fonte, URL, data de acesso, licença, hash, contagens, dicionário e recorte | 29/11 | D4 | Todos os campos exigidos no enunciado estão preenchidos |
| D7 | Amostra pequena versionada em `data/amostra/`, para a demonstração sem download | 01/12 | D3 | A interface roda só com a amostra |
| D8 | Seção do relatório "Fonte e qualidade dos dados" e o slide correspondente | 03/12 | D6 | Texto revisado pelo Integrante 5 |

## Integrante 2 — Atributos e divisão (`A`)

**Arquivos sob sua responsabilidade:** `src/energia/atributos.py`, `scripts/preparar_dados.py`, `tests/test_sem_futuro.py`, `tests/test_divisao.py`, `relatorio/secoes/02_representacao.md`
**Revisa os PRs de:** Integrante 3

| ID | Tarefa | Prazo | Depende de | Pronto quando |
|---|---|---|---|---|
| A1 | Reindexação do calendário: uma linha por dia, inclusive os excluídos (`kwh` vazio) | 27/11 | Q2 (usar um `diario` fictício até D3 ficar pronto) | Nenhuma data falta entre o início e o fim |
| A2 | Defasagens `lag1`, `lag2`, `lag7` e `media7` calculadas **depois** da reindexação | 28/11 | A1 | Se o dia anterior foi excluído, `lag1` fica vazio |
| A3 | Atributos de calendário do **dia previsto**, com a codificação decidida na reunião de início | 28/11 | A1 | Colunas iguais às de `COLUNAS_ATRIBUTOS` |
| A4 | Descarte de amostras com o alvo ou algum atributo vazio, com contagem | 28/11 | A2 | A contagem de descartes é impressa e registrada |
| A5 | Divisão cronológica pela data do alvo, gerando a coluna `particao` | 29/11 | A4 | Datas iguais às de `contratos.py`; sem sobreposição entre partições |
| A6 | `scripts/preparar_dados.py` gera `atributos.csv` a partir de `diario.csv` | 29/11 | A5, D3 | Roda de ponta a ponta com os dados reais |
| A7 | Testes `test_sem_futuro.py` (casos A3 e A4) e `test_divisao.py` (caso A7) | 29/11 | A5 | `pytest` passa; o teste falha se for introduzido um vazamento proposital |
| A8 | Seção do relatório "Representação e protocolo experimental" e o slide | 03/12 | A7 | Texto revisado pelo Integrante 5 |

## Integrante 3 — Modelagem e avaliação (`M`)

**Arquivos sob sua responsabilidade:** `src/energia/modelos.py`, `src/energia/avaliacao.py`, `scripts/treinar.py`, `scripts/experimentos.py`, `models/`, `resultados/`, `relatorio/secoes/03_resultados.md`
**Revisa os PRs de:** Integrante 1

| ID | Tarefa | Prazo | Depende de | Pronto quando |
|---|---|---|---|---|
| M1 | Referência de persistência (`prev = lag1`) e funções de MAE e RMSE | 29/11 | Q2 (usar `atributos` fictícios) | Métricas conferidas num exemplo pequeno calculado à mão |
| M2 | Regressão linear em um `Pipeline` | 30/11 | A6 | Treina só com a partição `treino` |
| M3 | Ridge: `Pipeline(StandardScaler, Ridge)`, grade de pelo menos 5 alphas, escolha **só na validação** e tabela da validação | 30/11 | M2 | `resultados/validacao.csv` com todos os alphas e o escolhido |
| M4 | Salvar os modelos em `models/*.joblib` com metadados: versão, alpha, datas de treino e lista de atributos | 30/11 | M3 | `carregar_modelo()` devolve o modelo e os metadados |
| M5 | `scripts/treinar.py` reprodutível (caso A9) | 01/12 | M4 | Duas execuções dão os mesmos coeficientes |
| M6 | `scripts/experimentos.py`: **avaliação única no teste**; MAE e RMSE dos 3 métodos; gráfico de pelo menos 30 dias; resíduos; 5 maiores erros | **02/12** | M5 | Tabelas e gráficos salvos em `resultados/` |
| M7 | Registro do ambiente: versões, sistema operacional e semente, em `resultados/ambiente.txt` | 02/12 | M6 | Arquivo gerado automaticamente |
| M8 | Seção do relatório "Algoritmos, resultados e limitações" (incluindo extrapolação) e os slides de resultados | 03/12 | M6 | Os números batem com `resultados/` |

> **Regra:** nada de rodar o teste antes de 02/12. Se precisar de números para testar o código, use a validação.

## Integrante 4 — Interface (`I`)

**Arquivos sob sua responsabilidade:** `app/app.py`, `src/energia/previsao.py`, `tests/test_previsao.py`, `relatorio/secoes/04_interface.md`, `relatorio/capturas/`
**Revisa os PRs de:** Integrante 5

| ID | Tarefa | Prazo | Depende de | Pronto quando |
|---|---|---|---|---|
| I1 | Esqueleto do Streamlit com dados fictícios: as 4 áreas (configurar, executar, explicar, histórico) | 26/11 | Q2 | `streamlit run app/app.py` abre sem erro |
| I2 | `previsao.prever()`, que levanta `HistoricoInsuficiente` com explicação, e `tests/test_previsao.py` (caso A5) | 29/11 | Q2, A2 | O teste passa usando os atributos fictícios |
| I3 | Tela de previsão: escolha da data, janela histórica (gráfico), valor previsto **em kWh** e o modelo usado | 30/11 | I2, M4 | Funciona com o modelo real |
| I4 | Seleção do período de avaliação e consulta ao teste: observado versus previsto, MAE e RMSE do período | 01/12 | I3, M6 | Mostra pelo menos 30 dias; indica com clareza qual período é o teste |
| I5 | Exportação das previsões em CSV | 01/12 | I4 | O arquivo exportado abre corretamente |
| I6 | Histórico de execuções na interface (consultar e exportar) usando `persistencia.py` | 01/12 | Q3 | Cada execução aparece no histórico |
| I7 | Tratamento de entradas inválidas (caso A8): mensagens claras, sem *traceback* | 02/12 | I3 | Captura de tela de cada erro |
| I8 | Capturas de tela, seção do relatório "Arquitetura e interface" e o roteiro da demonstração ao vivo | 03/12 | I7 | Demonstração ensaiada em até 5 min |

## Integrante 5 — Persistência, qualidade e entrega (`Q`)

**Arquivos sob sua responsabilidade:** `src/energia/contratos.py` (guardião), `src/energia/persistencia.py`, `tests/test_persistencia.py`, `tests/test_igualdade.py`, `requirements.txt`, `README.md`, `USO_DE_FERRAMENTAS.md`, `.github/`, `relatorio/relatorio.md`, `relatorio/secoes/05_reproducao.md`
**Revisa os PRs de:** Integrante 4

| ID | Tarefa | Prazo | Depende de | Pronto quando |
|---|---|---|---|---|
| Q1 | Repositório configurado: proteção da `main`, CODEOWNERS e acesso dos 5 integrantes e do professor | 25/11 | — | Ninguém consegue enviar direto para a `main` |
| Q2 | Revisar e congelar `contratos.py` com a equipe: colunas, datas de divisão, exceções | 25/11 | — | PR aprovado pelos 5 integrantes |
| Q3 | `persistencia.py`: SQLite com as funções `salvar_execucao`, `listar_execucoes` e `exportar_execucoes`, e o teste `test_persistencia.py` | 28/11 | Q2 | O teste passa; o banco é criado automaticamente |
| Q4 | Integração contínua (GitHub Actions) rodando o `pytest` em cada PR | 28/11 | Q1 | O PR mostra o status verde ou vermelho |
| Q5 | `test_igualdade.py` (caso A6): previsão do script = previsão da interface | 01/12 | I2, M4 | O teste passa |
| Q6 | `README.md` completo, com instalação e execução **testadas em outro computador** | 03/12 | M5, I7 | Registro de quem testou e quando |
| Q7 | `USO_DE_FERRAMENTAS.md`: bibliotecas, trechos externos e uso de IA generativa | 03/12 | — | Todos os integrantes declararam o próprio uso |
| Q8 | Montagem do relatório (5 a 8 páginas) a partir das seções, mais os slides e o ensaio | 03/12 | D8, A8, M8, I8 | Relatório em PDF dentro do limite de páginas |
| Q9 | Checklist do `ENTREGA_FINAL.md`, tag `entrega-05-12-2026` e envio ao professor | **04/12** | Q8 | Tag enviada e e-mail ou formulário enviado |

---

## Quadro de acompanhamento

Atualize a coluna "Status" no próprio PR, ou crie uma *issue* para cada ID no GitHub
(sugestão: um quadro do GitHub Projects com as colunas *A fazer*, *Fazendo*, *Em revisão* e *Pronto*).

| Integrante | 26/11 | 27/11 | 28/11 | 29/11 | 30/11 | 01/12 | 02/12 | 03/12 |
|---|---|---|---|---|---|---|---|---|
| 1 Dados | D1 D2 | D3 D4 | D5 | D6 | (revisões) | D7 | (correções) | D8 |
| 2 Atributos | (fictícios) | A1 | A2 A3 A4 | A5 A6 A7 | (revisões) | (apoio) | (correções) | A8 |
| 3 Modelos | (fictícios) | (fictícios) | (fictícios) | M1 | M2 M3 M4 | M5 | **M6 M7** | M8 |
| 4 Interface | I1 | I1 | (apoio) | I2 | I3 | I4 I5 I6 | I7 | I8 |
| 5 Qualidade | Q1 Q2 | (revisões) | Q3 Q4 | (revisões) | (revisões) | Q5 | checklist | Q6 Q7 Q8 |
