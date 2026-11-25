# Planejamento — Questão 6: Previsão de consumo de energia

**Disciplina:** Inteligência Artificial — UFC Campus Crateús (Prof. Wellington Franco)
**Apresentação:** sábado, 05/12/2026 · **Envio do link:** até sexta, 04/12/2026, 23h59 (Fortaleza)
**Equipe:** 5 integrantes (preencher nomes e matrículas na tabela abaixo)

## 1. O que o sistema faz

O sistema prevê a **energia diária (kWh) do dia seguinte** de uma residência, a partir da série
*UCI Individual Household Electric Power Consumption*, e compara três métodos no mesmo teste:

| Método | Papel |
|---|---|
| Persistência (consumo do dia anterior) | Referência ingênua |
| Regressão linear | Modelo 1 |
| Ridge (regularização L2), alpha escolhido na validação | Modelo 2 |

### Regras fixadas pelo enunciado (não mudar)

- **Base:** https://archive.ics.uci.edu/dataset/235/individual+household+electric+power+consumption. Colunas `Date`, `Time` e `Global_active_power` (kW, uma medição por minuto). O marcador `?` vira valor faltante.
- **Período:** de janeiro de 2007 a dezembro de 2009.
- **Alvo:** kWh do dia = soma de (`Global_active_power` / 60) no dia. Só valem **dias completos, com 1.440 medições válidas**. Registrar quantos dias foram excluídos. Nunca usar soma parcial de um dia.
- **Ordem obrigatória:** primeiro reindexar o calendário (um registro por dia, inclusive os faltantes), depois criar as defasagens e só então remover as linhas incompletas. O registro anterior disponível não é necessariamente o dia anterior.
- **Atributos:** consumo de 1, 2 e 7 dias antes, média dos 7 dias anteriores e calendário do dia previsto (dia da semana, mês, fim de semana).
- **Divisão cronológica por data do alvo:** treino em 2007–2008, validação de janeiro a junho de 2009, teste de julho a dezembro de 2009. O teste fica reservado e só entra na avaliação final.
- **Previsão diária no teste:** valores observados de dias passados podem alimentar as defasagens, mas o modelo **não é reajustado**.
- **Métricas:** MAE e RMSE, análise de resíduos, gráficos de pelo menos 30 dias e comparação com a persistência.

### Decisões a registrar no relatório (definir no 1º dia)

1. **Dezembro de 2006.** Os dados de dezembro de 2006 entram só como defasagem dos primeiros dias de 2007, ou ficam fora? Sugestão: deixar fora, seguindo à risca o recorte de 2007 a 2009, e aceitar a perda da primeira semana.
2. **Média dos 7 dias com algum dia excluído.** Sugestão: descartar a amostra se faltar qualquer um dos 7 dias. É mais simples e evita viés.
3. **Modelo final.** Ajustado só com 2007–2008, como o texto pede (sugestão), ou refeito com treino + validação depois de escolher o alpha? Se refizer, documentar.
4. **Codificação do calendário.** One-hot para o dia da semana e o mês, ou seno e cosseno? A escolha deve ser documentada.
5. **Pipeline e semente.** Padronização dentro do `Pipeline` do Ridge, com semente 42 registrada, mesmo que os métodos sejam determinísticos.

## 2. Arquitetura (camadas separadas, como o enunciado exige)

```
projeto/
├── scripts/
│   ├── baixar_dados.py        # baixa o .zip da UCI, confere o SHA-256 e extrai em data/raw/
│   ├── preparar_dados.py      # gera data/processed/diario.csv e atributos.csv
│   ├── treinar.py             # seleciona o alpha na validação e salva models/*.joblib
│   └── experimentos.py        # avaliação final no teste: tabelas e gráficos em resultados/
├── src/energia/
│   ├── dados.py               # leitura, "?"→NaN, agregação diária, filtro de 1.440 medições
│   ├── atributos.py           # reindexação, defasagens, média de 7 dias, calendário, divisão
│   ├── modelos.py             # persistência, LinearRegression, Pipeline(StandardScaler, Ridge)
│   ├── avaliacao.py           # MAE, RMSE, resíduos, gráficos
│   ├── previsao.py            # prevê um dia a partir do histórico; recusa se faltar histórico
│   └── persistencia.py        # SQLite: execuções (entradas, parâmetros, resultados)
├── app/app.py                 # interface Streamlit
├── tests/                     # casos de aceitação automatizados (pytest)
├── data/                      # fora do Git; só uma amostra pequena versionada
├── models/  resultados/
├── README.md  DADOS.md  USO_DE_FERRAMENTAS.md  ENTREGA_FINAL.md
├── relatorio/                 # relatório técnico (5 a 8 páginas)
└── requirements.txt
```

**Stack sugerida:** Python 3.11+, pandas, numpy, scikit-learn, matplotlib ou plotly, Streamlit, joblib, SQLite (módulo padrão `sqlite3`) e pytest.

### Contratos entre os módulos (combinar no 1º dia para todos trabalharem em paralelo)

- `diario.csv` tem as colunas `data` (AAAA-MM-DD), `kwh` (float ou vazio) e `n_medicoes` (int). Há uma linha para cada dia do calendário, inclusive os incompletos.
- `atributos.csv` tem as colunas `data`, `kwh_alvo`, `lag1`, `lag2`, `lag7`, `media7`, os campos de calendário e `particao` (`treino`, `validacao` ou `teste`).
- A função `prever(data_alvo, historico, modelo) -> float` levanta `HistoricoInsuficiente` com uma mensagem explicativa quando falta histórico. Ela é a **mesma** função usada pelo script e pela interface.
- Cada execução gravada no banco tem: data e hora, modelo e versão, período consultado, parâmetros, métricas e caminho da exportação.

## 3. Responsabilidades

Cada integrante é **dono** de uma parte e **revisor** de outra. Todos escrevem a própria seção do relatório e devem conseguir explicar o sistema inteiro na apresentação.

| # | Papel | Responsável por | Entrega principal | Revisa | Seção do relatório |
|---|---|---|---|---|---|
| 1 | **Dados** | Download, SHA-256, leitura, `?`→NaN, recorte 2007–2009, agregação diária, filtro de 1.440 medições, contagem de dias excluídos, **verificação manual de um dia** (planilha ou cálculo à parte) | `scripts/baixar_dados.py`, `src/energia/dados.py`, `DADOS.md` | Integrante 2 | Fonte e qualidade dos dados |
| 2 | **Atributos e divisão** | Reindexação do calendário, defasagens 1/2/7, média de 7 dias, calendário do dia previsto, divisão cronológica, teste automatizado de **ausência de atributos futuros** | `src/energia/atributos.py`, `scripts/preparar_dados.py` | Integrante 3 | Representação e protocolo experimental |
| 3 | **Modelagem e avaliação** | Persistência, regressão linear, Ridge com pelo menos 5 alphas escolhidos só na validação, avaliação final no teste, MAE/RMSE, resíduos, gráficos de 30 dias ou mais, limites da extrapolação | `src/energia/modelos.py`, `avaliacao.py`, `scripts/treinar.py`, `scripts/experimentos.py`, `models/`, `resultados/` | Integrante 1 | Algoritmos, resultados e limitações |
| 4 | **Interface** | Streamlit com janela histórica, previsão e unidade (kWh), seleção do período de avaliação, consulta ao teste, exportação em CSV, recusa explicada quando falta histórico, mensagens de erro claras | `app/app.py`, `src/energia/previsao.py` | Integrante 5 | Arquitetura e interface |
| 5 | **Persistência, qualidade e entrega** | Banco de execuções (histórico e exportação), testes dos casos de aceitação, igualdade entre a previsão do script e a da interface, `requirements.txt`, README testado em **outro computador**, `USO_DE_FERRAMENTAS.md`, Git e tag. Também coordena o relatório e os slides | `src/energia/persistencia.py`, `tests/`, `README.md`, `ENTREGA_FINAL.md` em dia | Integrante 4 | Reprodução, verificações e conclusão (e edição final do relatório) |

| # | Nome | Matrícula |
|---|---|---|
| 1 | | |
| 2 | | |
| 3 | | |
| 4 | | |
| 5 | | |

## 4. Cronograma (de 25/11 a 05/12/2026)

| Data | Marco | O que precisa estar pronto |
|---|---|---|
| **Qua 25/11** | Início | Repositório criado e todos com acesso. Papéis confirmados. Decisões da seção 1 tomadas. Contratos combinados. |
| **Qui 26/11** | Dados brutos | (1) Download com hash registrado e leitura funcionando. (4) Esqueleto da interface com dados fictícios. (5) Esquema do banco e `requirements.txt` inicial. |
| **Sex 27/11** | Série diária | (1) `diario.csv` com a contagem de dias excluídos e a verificação manual de um dia. (2) Rascunho das defasagens. |
| **Sáb 28 – Dom 29/11** | Atributos e referência | (2) `atributos.csv` com as partições e o teste de "sem futuro" passando. (3) Persistência avaliada na validação. |
| **Seg 30/11** | Modelos | (3) Regressão linear e Ridge com o alpha escolhido na validação. Modelos salvos. (4) Interface usando o modelo real. |
| **Ter 01/12** | Integração | Fluxo completo pela interface: configurar, prever, explicar e exportar. (5) Histórico gravado e consultável. |
| **Qua 02/12** | **Congelamento do código** | (3) Avaliação final no teste, feita uma única vez, com tabelas e gráficos. (5) Todos os casos de aceitação passando. Daqui em diante, só correções. |
| **Qui 03/12** | Documentação | Relatório de 5 a 8 páginas montado. README testado em outro computador. Slides prontos. |
| **Sex 04/12** | Envio | Ensaio cronometrado da apresentação. Tag `entrega-05-12-2026` criada. Link, commit, nomes e matrículas enviados até 23h59. |
| **Sáb 05/12** | **Apresentação** | 15 min de apresentação e 5 min de perguntas. |

### Rotina da equipe
- Reunião rápida diária de 15 minutos: o que fiz, o que farei, o que está me bloqueando.
- Cada parte entra por *pull request* na `main`, revisado pelo revisor indicado na tabela.
- **Ninguém olha o resultado do teste antes de 02/12.** A escolha de alpha e de atributos usa só a validação.

## 5. Riscos e como reduzir

| Risco | Como reduzir |
|---|---|
| Arquivo grande (cerca de 130 MB) e leitura lenta | Ler só as colunas necessárias e salvar a série diária processada. A interface lê apenas o processado. |
| Vazamento temporal nas defasagens | Reindexar antes de criar as defasagens e manter um teste automatizado de "sem futuro" (integrante 2). |
| Divergência entre a previsão do script e a da interface | Uma única função `prever()` e um teste de igualdade (integrante 5). |
| Ridge não supera a persistência | Isso não tira ponto: o resultado deve ser discutido honestamente no relatório. |
| Integrante sem disponibilidade | Revisores conhecem a parte do dono e podem assumir. |
| Internet na apresentação | Dados e modelos prontos localmente, sem download na hora da demonstração. |
