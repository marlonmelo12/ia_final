# Planejamento — Questão 2: Otimizador de roteiros turísticos

**Disciplina:** Inteligência Artificial — UFC Campus Crateús (Prof. Wellington Franco)
**Apresentação:** sábado, 05/12/2026 · **Envio do link:** até sexta, 04/12/2026, 23h59 (Fortaleza)
**Equipe:** 5 integrantes (preencher nomes e matrículas na tabela abaixo)

> A equipe trocou a Questão 6 (previsão de energia) pela Questão 2 em 25/11/2026. As branches
> `dados/D1-download` e `dados/D2-D6-serie-diaria` são da questão antiga e não entram na `main`.

## 1. O que o sistema faz

O usuário informa um **ponto de partida em Fortaleza**, o **tempo disponível** e uma **preferência de 1 a 5
para cada categoria** de local. O sistema monta uma sequência de visitas, sem repetição, que começa e
termina no ponto de partida, cabe no tempo e maximiza a soma das preferências. Três métodos são comparados
nas mesmas condições:

| Método | Papel |
|---|---|
| Construção gulosa (maior ganho de interesse por incremento de tempo) | Referência simples |
| Subida de encosta com reinícios aleatórios | Busca local 1 |
| Têmpera simulada (*simulated annealing*) | Busca local 2 |

### Regras fixadas pelo enunciado (não mudar)

- **Base:** pontos de interesse do OpenStreetMap obtidos com `osmnx.features_from_place("Fortaleza, Ceará, Brazil", tags)`, com as categorias `tourism=attraction`, `tourism=museum` e `leisure=park`.
- **Recorte:** 20 locais distintos, com nome e localização. Se houver menos, usar todos e registrar a contagem. Para polígonos, calcular um ponto representativo. Salvar um CSV com identificador OSM, nome, categoria, latitude e longitude. Registrar o recorte e a atribuição ao OSM.
- **Modelo (hipóteses acadêmicas, não tempos reais):** o roteiro começa e termina no ponto escolhido pelo usuário. Cada visita dura **30 minutos**. O deslocamento é a **distância geodésica dividida por 4 km/h**. Cada categoria recebe uma preferência inteira de 1 a 5.
- **Objetivo:** maximizar a soma das preferências dos locais visitados, sem repetição, respeitando o tempo total **inclusive o retorno**.
- **Orçamentos dos cenários:** 120, 180 e 240 minutos.
- **Solução:** uma lista ordenada de locais. A vizinhança deve incluir **inserção, remoção e troca de posições**.
- **Comparação justa:** subida de encosta e têmpera simulada com o **mesmo limite de avaliações da função objetivo**. Declarar temperatura inicial, resfriamento, parada e número de reinícios. Preservar a **melhor solução viável** encontrada.
- **Experimento:** pelo menos **10 cenários** e as **sementes 0 a 4** para os métodos estocásticos. Comparar média e desvio-padrão da utilidade, proporção de soluções viáveis, número de avaliações, tempo e estabilidade.
- **Resultado mínimo:** nenhum local repetido e tempo dentro do orçamento, ou o sistema informa com clareza que não há solução viável.

### Decisões a registrar no relatório (definir na reunião de 26/11)

1. **Seleção dos 20 locais.** Os POIs ficam espalhados pela cidade e, a 4 km/h, 240 minutos não cobrem Fortaleza inteira. Sugestão: os 20 locais com nome mais próximos de um centro fixo (por exemplo, a Praça do Ferreira, −3.7275, −38.5275), com no mínimo 4 de cada categoria se houver. A regra precisa ser determinística e documentada.
2. **Categoria e duplicados.** Se um elemento tiver mais de uma tag, vale a ordem `museum`, depois `attraction`, depois `park` (já em `contratos.CATEGORIAS`). Elementos com o mesmo nome a menos de 200 m contam como um só local. Registrar quantos foram removidos.
3. **Ponto representativo do polígono.** Sugestão: `representative_point()` do Shapely, que fica sempre dentro do polígono (o centroide pode cair fora em formas côncavas).
4. **Tratamento das restrições.** Sugestão: só aceitar vizinhos viáveis. Um vizinho inviável conta como avaliação, mas é rejeitado. A alternativa é penalizar o excesso de tempo. Escolher uma e justificar.
5. **Solução inicial da busca local.** Sugestão: solução aleatória viável gerada pela semente, e não o resultado do guloso, para que a comparação mostre o que a busca acrescenta. Uma variante que parte do guloso pode entrar como experimento extra.
6. **Parâmetros declarados.** Os valores iniciais estão em `contratos.py` (`MAX_AVALIACOES`, `PARAMS_SUBIDA`, `PARAMS_TEMPERA`). O ajuste usa **só as sementes 100 a 104**. Os parâmetros congelam em 01/12, e o experimento final usa as sementes 0 a 4 uma única vez.
7. **Os 10 cenários.** Combinações de ponto de partida, orçamento (120, 180 e 240, cada um usado em pelo menos 3 cenários) e perfil de preferências (por exemplo, "gosta de museus", "prefere parques", "indiferente"). Ficam fixos em `data/cenarios.csv` antes de qualquer experimento.

## 2. Arquitetura (camadas separadas, como o enunciado exige)

```
projeto/
├── scripts/
│   ├── baixar_dados.py        # OSMnx → data/raw/pois_osm.geojson → data/pois.csv (20 locais)
│   └── experimentos.py        # 10 cenários × 3 métodos × sementes 0-4 → resultados/
├── src/roteiro/
│   ├── contratos.py           # caminhos, constantes do enunciado, esquemas, exceções
│   ├── dados.py               # filtro de nome, categoria, ponto representativo, duplicados, seleção
│   ├── problema.py            # Cenario, haversine, tempo, utilidade, viabilidade, contador de avaliações
│   ├── vizinhanca.py          # inserção, remoção e troca de posições
│   ├── guloso.py              # construção gulosa (referência)
│   ├── subida_encosta.py      # subida de encosta com reinícios
│   ├── tempera.py             # têmpera simulada
│   ├── otimizar.py            # caminho único: valida a entrada, roda o método e explica o resultado
│   └── persistencia.py        # SQLite: execuções (entradas, parâmetros, resultados)
├── app/app.py                 # interface Streamlit com mapa (pydeck)
├── data/pois.csv  data/cenarios.csv   # pequenos e versionados; a demonstração roda offline
├── tests/                     # casos de aceitação automatizados (pytest)
├── resultados/                # tabelas e gráficos do experimento
├── README.md  DADOS.md  USO_DE_FERRAMENTAS.md  ENTREGA_FINAL.md
├── relatorio/                 # relatório técnico (5 a 8 páginas)
└── requirements.txt
```

**Stack:** Python 3.11+, OSMnx (só para obter os dados), pandas, numpy, matplotlib, Streamlit com pydeck para o mapa, SQLite (módulo padrão `sqlite3`) e pytest.

**Profundidade exigida:** o núcleo dos algoritmos é implementado pela equipe. Nenhuma biblioteca de otimização ou roteamento substitui o guloso, a subida de encosta ou a têmpera.

### Contratos entre os módulos (combinar em 26/11 para todos trabalharem em paralelo)

- `pois.csv` tem as colunas `osm_id`, `nome`, `categoria`, `lat`, `lon`, com no máximo 20 linhas e sem `osm_id` repetido.
- `cenarios.csv` tem as colunas `cenario`, `descricao`, `lat_partida`, `lon_partida`, `orcamento_min`, `pref_museum`, `pref_attraction`, `pref_park`.
- Um roteiro é uma `list` de `osm_id`, sem o ponto de partida (que fica implícito no início e no fim).
- `problema.Avaliador.avaliar(roteiro)` devolve `(utilidade, tempo, viavel)` e **conta** cada chamada. Todos os métodos usam esse contador para respeitar `MAX_AVALIACOES`.
- `otimizar.otimizar(cenario, metodo, semente)` é a **mesma** função usada pelo script e pela interface. Ela levanta `EntradaInvalida` com mensagem clara. Orçamento insuficiente não é erro: devolve um roteiro vazio com a explicação.
- Cada execução gravada no banco tem: data e hora, cenário (partida, orçamento, preferências), método, semente, parâmetros, roteiro, utilidade, tempo total, viabilidade, avaliações e tempo de execução.

## 3. Responsabilidades

Cada integrante é **dono** de uma parte e **revisor** de outra. Todos escrevem a própria seção do relatório e devem conseguir explicar o sistema inteiro na apresentação.

| # | Papel | Responsável por | Entrega principal | Revisa | Seção do relatório |
|---|---|---|---|---|---|
| 1 | **Dados** | Consulta OSMnx, bruto salvo com hash, filtro de nome, categoria, ponto representativo dos polígonos, duplicados, seleção dos 20 locais, contagens, atribuição OSM | `scripts/baixar_dados.py`, `src/roteiro/dados.py`, `data/pois.csv`, `DADOS.md` | Integrante 2 | Fonte e qualidade dos dados |
| 2 | **Modelo do problema** | Haversine, tempo com retorno, utilidade, viabilidade, contador de avaliações, vizinhança (inserção, remoção, troca), construção gulosa, os 10 cenários | `problema.py`, `vizinhanca.py`, `guloso.py`, `data/cenarios.csv` | Integrante 3 | Representação, função objetivo, vizinhança e guloso |
| 3 | **Busca local e experimento** | Subida de encosta com reinícios, têmpera simulada, mesmo limite de avaliações, melhor viável preservada, ajuste com as sementes 100 a 104, experimento final, tabelas e gráficos | `subida_encosta.py`, `tempera.py`, `scripts/experimentos.py`, `resultados/` | Integrante 1 | Métodos, resultados e limitações |
| 4 | **Interface** | Streamlit: partida, tempo, preferências, método e semente; sequência, mapa, tempo estimado, retorno e utilidade; comparação dos métodos; exportação; mensagens de erro claras | `app/app.py`, `src/roteiro/otimizar.py` | Integrante 5 | Arquitetura e interface |
| 5 | **Persistência, qualidade e entrega** | Banco de execuções (histórico e exportação), testes dos casos de aceitação, igualdade script = interface, `requirements.txt`, README testado em **outro computador**, `USO_DE_FERRAMENTAS.md`, Git e tag. Também coordena o relatório e os slides | `persistencia.py`, `tests/`, `README.md`, `ENTREGA_FINAL.md` em dia | Integrante 4 | Reprodução, verificações e conclusão (e edição final do relatório) |

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
| **Qua 25/11** | Troca de questão | Equipe avisada da mudança para a Questão 2. Leitura das páginas 4 e 5 do enunciado. |
| **Qui 26/11** | Início | Papéis confirmados. Decisões da seção 1 tomadas. `contratos.py` aprovado. (1) Consulta OSMnx funcionando. (4) Esqueleto da interface com dados fictícios. (5) Esquema do banco. |
| **Sex 27/11** | Dados e modelo | (1) `pois.csv` com os 20 locais e as contagens. (2) Haversine, tempo, utilidade e viabilidade com testes. |
| **Sáb 28 – Dom 29/11** | Vizinhança e referência | (2) Vizinhança, guloso e `cenarios.csv`. (3) Subida de encosta funcionando num cenário de ajuste. |
| **Seg 30/11** | Busca local | (3) Têmpera simulada e o mesmo limite de avaliações. (4) Interface usando os métodos reais e o mapa. |
| **Ter 01/12** | Integração | Fluxo completo pela interface: configurar, executar, explicar e exportar. (5) Histórico gravado e consultável. (3) **Parâmetros congelados.** |
| **Qua 02/12** | **Congelamento do código** | (3) Experimento final, uma única vez, com as sementes 0 a 4. (5) Todos os casos de aceitação passando. Daqui em diante, só correções. |
| **Qui 03/12** | Documentação | Relatório de 5 a 8 páginas montado. README testado em outro computador. Slides prontos. |
| **Sex 04/12** | Envio | Ensaio cronometrado da apresentação. Tag `entrega-05-12-2026` criada. Link, commit, nomes e matrículas enviados até 23h59. |
| **Sáb 05/12** | **Apresentação** | 15 min de apresentação e 5 min de perguntas. |

### Rotina da equipe
- Reunião rápida diária de 15 minutos: o que fiz, o que farei, o que está me bloqueando.
- Cada parte entra por *pull request* na `main`, revisado pelo revisor indicado na tabela.
- **Ajuste de parâmetros só com as sementes 100 a 104.** As sementes 0 a 4 ficam para o experimento final.

## 5. Riscos e como reduzir

| Risco | Como reduzir |
|---|---|
| Overpass (servidor do OSM) lento ou fora do ar | Baixar uma vez, guardar o bruto em `data/raw/` e versionar `data/pois.csv`. A interface e os testes nunca consultam a internet. |
| Locais muito distantes: quase nenhum roteiro cabe no orçamento | Regra de seleção pelos mais próximos de um centro (decisão 1). Conferir que o guloso visita alguns locais com 120 minutos. |
| Comparação injusta entre os métodos | Um único `Avaliador` que conta as avaliações, e um teste que confere o mesmo limite para todos (A7). |
| Têmpera devolve a última solução, e não a melhor | Guardar sempre a melhor viável. Há um teste para isso. |
| Divergência entre o roteiro do script e o da interface | Uma única função `otimizar()` e um teste de igualdade (A5). |
| Busca local não supera o guloso | Isso não tira ponto: o resultado deve ser discutido honestamente no relatório. Com 20 locais, o guloso pode ficar perto do ótimo. |
| Integrante sem disponibilidade | Revisores conhecem a parte do dono e podem assumir. |
| Internet na apresentação | Dados versionados e mapa com fundo opcional; a demonstração roda sem rede. |
