# Backlog por integrante — Questão 2

Cada item tem um **ID** (use no nome da branch e no commit), um **prazo**, as **dependências** e o
**critério de pronto**. Um item só fica pronto quando o *pull request* for aprovado pelo revisor e
integrado na `main`. Os papéis, a arquitetura e o cronograma estão em `PLANEJAMENTO.md`, e a definição
da entrega em `ENTREGA_FINAL.md`.

**Legenda de prazos:** todas as datas são de 2026. Os parâmetros congelam em **01/12**, o código em **02/12**. A tag e o envio são em **04/12**.

## Mapa de dependências

```
Q2 contratos (26/11) ──┬─► D1..D4 dados ──────────────┐
                       ├─► P1..P4 problema ─► P5 vizinhança ─► B1..B3 busca local ─► B5 experimento
                       │                    └► P6 guloso ───────────────────────────┘
                       ├─► I1 esqueleto da interface (dados fictícios) ─► I2..I5 interface real
                       └─► Q3 persistência ─────────────────────────────► I6 histórico na interface
```

Enquanto a etapa anterior não fica pronta, cada um trabalha com **dados fictícios no formato do
contrato** (`src/roteiro/contratos.py`). Por exemplo, 5 locais inventados num `pois.csv` de teste.
Assim ninguém fica parado esperando outra parte.

---

## Integrante 1 — Dados (`D`)

**Arquivos sob sua responsabilidade:** `scripts/baixar_dados.py`, `src/roteiro/dados.py`, `tests/test_dados.py`, `data/pois.csv`, `DADOS.md`, `relatorio/secoes/01_dados.md`
**Revisa os PRs de:** Integrante 2

| ID | Tarefa | Prazo | Depende de | Pronto quando |
|---|---|---|---|---|
| D1 | `baixar_features()`: `osmnx.features_from_place(LOCALIDADE, TAGS_OSM)`, salvando o bruto em `data/raw/pois_osm.geojson` e imprimindo o SHA-256 | 26/11 | Q2 | Roda em um clone limpo; a data de acesso, a versão do OSMnx e o hash vão para o `DADOS.md` |
| D2 | Limpeza: só elementos com `name`; categoria pela ordem de `CATEGORIAS`; ponto representativo dos polígonos (decisão 3) | 27/11 | D1 | Todo local tem nome, categoria válida e `lat`/`lon` dentro de Fortaleza |
| D3 | Duplicados (decisão 2) e **seleção dos 20 locais** pela regra da decisão 1, gerando `data/pois.csv` | 27/11 | D2 | `pois.csv` segue `COLUNAS_POIS`; a regra é determinística (duas execuções dão o mesmo arquivo) |
| D4 | Contagens: elementos retornados por categoria e geometria, sem nome, duplicados e selecionados | 27/11 | D3 | As contagens são impressas pelo script e copiadas para o `DADOS.md` |
| D5 | `tests/test_dados.py` (casos A9 e A10) com um GeoDataFrame pequeno montado à mão | 28/11 | D3 | `pytest tests/test_dados.py` passa sem internet |
| D6 | `DADOS.md` completo: fonte, consulta, data de acesso, licença ODbL, atribuição, hash, contagens, dicionário e recorte | 29/11 | D4 | Todos os campos exigidos no enunciado estão preenchidos |
| D7 | Conferir os 20 locais num mapa (nome e posição plausíveis) e registrar qualquer exclusão manual, com motivo | 30/11 | D3 | Lista conferida anexada ao PR |
| D8 | Seção do relatório "Fonte e qualidade dos dados" e o slide correspondente | 03/12 | D6 | Texto revisado pelo Integrante 5 |

## Integrante 2 — Modelo do problema (`P`)

**Arquivos sob sua responsabilidade:** `src/roteiro/problema.py`, `src/roteiro/vizinhanca.py`, `src/roteiro/guloso.py`, `data/cenarios.csv`, `tests/test_problema.py`, `tests/test_vizinhanca.py`, `relatorio/secoes/02_modelo.md`
**Revisa os PRs de:** Integrante 3

| ID | Tarefa | Prazo | Depende de | Pronto quando |
|---|---|---|---|---|
| P1 | `haversine_km()` e matriz de tempos de deslocamento (partida + locais) em minutos, a 4 km/h | 27/11 | Q2 | Distância conferida à mão para um par conhecido (erro < 1 m) |
| P2 | `Avaliador.tempo()`: deslocamentos + 30 min por visita + **retorno** à partida | 27/11 | P1 | Caso A2 passa com um roteiro calculado à mão |
| P3 | `Avaliador.avaliar()`: utilidade, viabilidade (sem repetição e dentro do orçamento) e **contador de avaliações** | 27/11 | P2 | O contador sobe 1 a cada chamada e pode ser zerado |
| P4 | Validação do orçamento insuficiente: se nenhum local cabe sozinho (ida + 30 min + volta), explicar qual é o mais próximo e quanto tempo falta | 28/11 | P2 | Caso A3 passa |
| P5 | Vizinhança: `inserir`, `remover`, `trocar` e `vizinho_aleatorio(rng)`; nunca altera o roteiro original | 28/11 | P3 | Caso A1 passa; os três movimentos são sorteados com a mesma semente de forma reprodutível |
| P6 | Guloso: maior preferência por acréscimo de tempo, com a melhor posição de inserção, até nenhum local caber | 29/11 | P5 | Roteiro viável em todos os cenários; resultado determinístico |
| P7 | `data/cenarios.csv` com os **10 cenários** (decisão 7): partidas, orçamentos 120/180/240 e perfis de preferência | 29/11 | D3 | Cada orçamento aparece em pelo menos 3 cenários; aprovado pela equipe antes de qualquer experimento |
| P8 | Seção do relatório "Representação, função objetivo, vizinhança e guloso" e o slide | 03/12 | P6 | Texto revisado pelo Integrante 5 |

## Integrante 3 — Busca local e experimento (`B`)

**Arquivos sob sua responsabilidade:** `src/roteiro/subida_encosta.py`, `src/roteiro/tempera.py`, `scripts/experimentos.py`, `tests/test_metodos.py`, `resultados/`, `relatorio/secoes/03_metodos_resultados.md`
**Revisa os PRs de:** Integrante 1

| ID | Tarefa | Prazo | Depende de | Pronto quando |
|---|---|---|---|---|
| B1 | Subida de encosta com reinícios: solução inicial (decisão 5), melhor vizinho entre `vizinhos_por_passo` sorteados, parada em ótimo local, reinício até esgotar `MAX_AVALIACOES` | 29/11 | P5 (usar uma vizinhança fictícia antes) | Devolve a melhor viável de todos os reinícios e o histórico |
| B2 | Têmpera simulada: aceitação de Metropolis, resfriamento geométrico, parada por `t_minima` ou por `MAX_AVALIACOES` | 30/11 | P5 | Devolve a **melhor** viável encontrada, não a última |
| B3 | Mesmo limite de avaliações e reprodutibilidade: `tests/test_metodos.py` (casos A6 e A7) | 30/11 | B1, B2 | Nenhum método passa de `MAX_AVALIACOES`; a mesma semente dá o mesmo roteiro |
| B4 | Ajuste dos parâmetros **só com as sementes 100 a 104**, com uma tabela das tentativas; valores finais em `contratos.py` por PR `CONTRATO:` | **01/12** | B3 | `resultados/ajuste.csv` com as configurações testadas e a escolhida |
| B5 | `scripts/experimentos.py`: 10 cenários × 3 métodos × sementes 0 a 4; utilidade (média e desvio-padrão), proporção viável, avaliações, tempo (mediana de 3 medições) e estabilidade | **02/12** | B4, P7 | `resultados/experimento.csv` (uma linha por execução) e `resultados/resumo.csv` |
| B6 | Gráficos: utilidade por cenário e método, convergência (utilidade × avaliações) e dispersão entre sementes; registro do ambiente em `resultados/ambiente.txt` | 02/12 | B5 | Arquivos gerados automaticamente pelo script |
| B7 | Seção do relatório "Métodos, resultados e limitações" (exemplos de falha, hipóteses de 4 km/h em linha reta) e os slides de resultados | 03/12 | B6 | Os números batem com `resultados/` |

> **Regra:** nada de rodar as sementes 0 a 4 antes de 02/12. Para testar o código, use as sementes 100 a 104.

## Integrante 4 — Interface (`I`)

**Arquivos sob sua responsabilidade:** `app/app.py`, `src/roteiro/otimizar.py`, `tests/test_otimizar.py`, `relatorio/secoes/04_interface.md`, `relatorio/capturas/`
**Revisa os PRs de:** Integrante 5

| ID | Tarefa | Prazo | Depende de | Pronto quando |
|---|---|---|---|---|
| I1 | Esqueleto do Streamlit com dados fictícios: as 4 áreas (configurar, executar, explicar, histórico) | 26/11 | Q2 | `streamlit run app/app.py` abre sem erro |
| I2 | `otimizar.otimizar()`: valida a entrada, chama o método, monta a resposta com a explicação; `tests/test_otimizar.py` (casos A4 e A8) | 29/11 | Q2, P3 | O teste passa usando locais fictícios |
| I3 | Tela do roteiro: partida (um local da lista ou latitude/longitude), tempo disponível, preferências 1 a 5, método e semente; mostra a **sequência** com chegada e saída, o **tempo estimado**, o **retorno**, a **utilidade** e o **mapa** com o trajeto (pydeck) | 30/11 | I2, D3 | Funciona com os 20 locais reais |
| I4 | Comparação dos três métodos no mesmo cenário: tabela com utilidade, tempo, viabilidade e avaliações, e os três roteiros no mapa | 01/12 | I3, B2 | Mostra com clareza qual método venceu e por quanto |
| I5 | Exportação do roteiro em CSV (`COLUNAS_ROTEIRO`) e JSON | 01/12 | I3 | O arquivo exportado abre corretamente e traz o cenário junto |
| I6 | Histórico de execuções na interface (consultar e exportar) usando `persistencia.py` | 01/12 | Q3 | Cada execução aparece no histórico |
| I7 | Entradas inválidas e orçamento insuficiente (casos A3 e A8): mensagens claras, sem *traceback* | 02/12 | I3 | Captura de tela de cada caso |
| I8 | Capturas de tela, seção do relatório "Arquitetura e interface" e o roteiro da demonstração ao vivo | 03/12 | I7 | Demonstração ensaiada em até 5 min |

## Integrante 5 — Persistência, qualidade e entrega (`Q`)

**Arquivos sob sua responsabilidade:** `src/roteiro/contratos.py` (guardião), `src/roteiro/persistencia.py`, `tests/test_persistencia.py`, `tests/test_igualdade.py`, `tests/test_contratos.py`, `requirements.txt`, `README.md`, `USO_DE_FERRAMENTAS.md`, `.github/`, `relatorio/relatorio.md`, `relatorio/secoes/05_reproducao.md`
**Revisa os PRs de:** Integrante 4

| ID | Tarefa | Prazo | Depende de | Pronto quando |
|---|---|---|---|---|
| Q1 | Repositório configurado: proteção da `main`, CODEOWNERS com os usuários reais e acesso dos 5 integrantes e do professor | 26/11 | — | Ninguém consegue enviar direto para a `main` |
| Q2 | Revisar e congelar `contratos.py` com a equipe: colunas, constantes do enunciado, sementes, limite de avaliações, exceções | 26/11 | — | PR aprovado pelos 5 integrantes |
| Q3 | `persistencia.py`: SQLite com `salvar_execucao`, `listar_execucoes` e `exportar_execucoes` (o roteiro gravado como JSON), e o teste `test_persistencia.py` | 28/11 | Q2 | O teste passa; o banco é criado automaticamente |
| Q4 | Integração contínua (GitHub Actions) rodando o `pytest` em cada PR | 28/11 | Q1 | O PR mostra o status verde ou vermelho |
| Q5 | `test_igualdade.py` (caso A5): roteiro do script = roteiro da interface, com o mesmo cenário e a mesma semente | 01/12 | I2, B2 | O teste passa |
| Q6 | `README.md` completo, com instalação e execução **testadas em outro computador** | 03/12 | B5, I7 | Registro de quem testou e quando |
| Q7 | `USO_DE_FERRAMENTAS.md`: bibliotecas, trechos externos e uso de IA generativa | 03/12 | — | Todos os integrantes declararam o próprio uso |
| Q8 | Montagem do relatório (5 a 8 páginas) a partir das seções, mais os slides e o ensaio | 03/12 | D8, P8, B7, I8 | Relatório em PDF dentro do limite de páginas |
| Q9 | Checklist do `ENTREGA_FINAL.md`, tag `entrega-05-12-2026` e envio ao professor | **04/12** | Q8 | Tag enviada e e-mail ou formulário enviado |

---

## Quadro de acompanhamento

Atualize a coluna "Status" no próprio PR, ou crie uma *issue* para cada ID no GitHub
(sugestão: um quadro do GitHub Projects com as colunas *A fazer*, *Fazendo*, *Em revisão* e *Pronto*).

| Integrante | 26/11 | 27/11 | 28/11 | 29/11 | 30/11 | 01/12 | 02/12 | 03/12 |
|---|---|---|---|---|---|---|---|---|
| 1 Dados | D1 | D2 D3 D4 | D5 | D6 | D7 | (revisões) | (correções) | D8 |
| 2 Problema | (fictícios) | P1 P2 P3 | P4 P5 | P6 P7 | (revisões) | (apoio) | (correções) | P8 |
| 3 Busca local | (fictícios) | (fictícios) | (fictícios) | B1 | B2 B3 | **B4** | **B5 B6** | B7 |
| 4 Interface | I1 | I1 | (apoio) | I2 | I3 | I4 I5 I6 | I7 | I8 |
| 5 Qualidade | Q1 Q2 | (revisões) | Q3 Q4 | (revisões) | (revisões) | Q5 | checklist | Q6 Q7 Q8 |
