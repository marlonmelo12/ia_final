# Definição da Entrega Final — Questão 2: Otimizador de roteiros turísticos

Este documento define **o que conta como entregue**. Um item só é marcado quando a evidência
indicada existir no repositório, no commit da tag `entrega-05-12-2026`.

## 1. Identificação

| Campo | Valor |
|---|---|
| Projeto | Questão 2 — Otimizador de roteiros turísticos em Fortaleza |
| Repositório | https://github.com/marlonmelo12/ia_final |
| Commit avaliado | _(hash)_ |
| Tag | `entrega-05-12-2026` (criada no commit acima e **nunca movida**) |
| Acesso do professor | Leitura concedida em: _(data)_ |
| Integrantes / matrículas | _(5 nomes e matrículas)_ |
| Envio | Até 04/12/2026, 23h59 (Fortaleza) · Apresentação: 05/12/2026 |

## 2. Produto: o sistema

O avaliador deve conseguir abrir o README, instalar, executar e percorrer o fluxo principal **sem editar código**.

| Requisito | Critério de aceite | Evidência |
|---|---|---|
| Dados externos | POIs do OpenStreetMap em Fortaleza (`attraction`, `museum`, `park`) obtidos com OSMnx por script; 20 locais com nome e localização | `scripts/baixar_dados.py`, `data/pois.csv` e `DADOS.md` |
| Preparação | Filtro de nome, categoria, ponto representativo dos polígonos, duplicados, regra de seleção e contagens | `src/roteiro/dados.py` e as contagens no `DADOS.md` |
| Método de IA | Subida de encosta com reinícios e têmpera simulada implementadas pela equipe, comparadas com a construção gulosa sob o mesmo limite de avaliações | `src/roteiro/subida_encosta.py`, `tempera.py`, `guloso.py`, `vizinhanca.py` e `problema.py` |
| Interface (web) | Recebe partida, tempo disponível e preferências; mostra a sequência, o mapa, o tempo estimado e o retorno; compara os métodos e exporta o roteiro | `app/app.py` e capturas de tela no relatório |
| Persistência | Execuções gravadas com cenário, método, semente, parâmetros e resultado; histórico consultável e exportável | `src/roteiro/persistencia.py` e um arquivo de exemplo exportado |
| Arquitetura | Interface, dados, núcleo de IA e persistência em módulos separados | Estrutura de `src/` e `app/` |
| Reprodução | Instalação e execução testadas em outro computador | `README.md`, `requirements.txt` e o nome de quem testou, com a data |

## 3. Resultados experimentais obrigatórios

Todos devem ser gerados por `scripts/experimentos.py` e salvos em `resultados/`.

- [ ] Tabela dos **10 cenários** (partida, orçamento de 120, 180 ou 240 min e preferências) com as **sementes 0 a 4**.
- [ ] Por cenário e método: **média e desvio-padrão da utilidade**, **proporção de soluções viáveis**, **número de avaliações** e tempo de execução.
- [ ] Prova de que subida de encosta e têmpera usaram o **mesmo limite de avaliações**.
- [ ] Parâmetros declarados: temperatura inicial, resfriamento, parada, número de reinícios, vizinhos por passo e limite de avaliações.
- [ ] Tabela do ajuste (sementes 100 a 104), separada do experimento final.
- [ ] Gráfico de convergência (utilidade × avaliações) e de dispersão entre sementes (estabilidade).
- [ ] Exemplos de falha comentados (por exemplo, cenário em que a busca local não supera o guloso, ou em que poucos locais cabem).
- [ ] Registro do ambiente: versões do Python e das bibliotecas, sistema operacional e máquina.
- [ ] Discussão dos limites: distância em linha reta a 4 km/h, visita fixa de 30 min, preferência por categoria e não por local, cobertura do OSM.

## 4. Casos de aceitação

Cada caso tem uma entrada, a saída esperada e uma evidência: um teste em `tests/` ou um roteiro reproduzível.
Os casos A1 a A4 são exigidos literalmente pelo enunciado.

| # | Caso | Entrada | Saída esperada | Evidência |
|---|---|---|---|---|
| A1 | Nenhum local repetido | Roteiros de todos os métodos e de todos os movimentos da vizinhança | Nenhum `osm_id` aparece duas vezes | `tests/test_vizinhanca.py` e `tests/test_metodos.py` |
| A2 | Tempo recalculado respeita o orçamento | Roteiro devolvido por cada método | Tempo recalculado à parte (deslocamentos + 30 min por visita + retorno) ≤ orçamento, dentro de 1e-6 | `tests/test_problema.py` |
| A3 | Orçamento insuficiente | Orçamento menor que ida + 30 min + volta até o local mais próximo | Roteiro vazio e explicação clara (qual local, quanto tempo falta) | `tests/test_problema.py` e captura de tela |
| A4 | Preferências alteram o roteiro | Mesmo cenário com perfis "museus" e "parques" | Os roteiros mudam e a utilidade reflete as novas preferências | `tests/test_otimizar.py` |
| A5 | Script = interface | Mesmo cenário, método e semente | Roteiros idênticos | `tests/test_igualdade.py` |
| A6 | Reprodutibilidade | Mesmo cenário e mesma semente, duas vezes | Mesmo roteiro e mesma utilidade | `tests/test_metodos.py` |
| A7 | Comparação justa | Subida de encosta e têmpera no mesmo cenário | Nenhum dos dois passa de `MAX_AVALIACOES`; ambos devolvem a melhor solução viável encontrada | `tests/test_metodos.py` |
| A8 | Entrada inválida | Coordenada fora de Fortaleza, orçamento negativo, preferência fora de 1 a 5 | Mensagem de erro compreensível, sem *traceback* | `tests/test_otimizar.py` e captura de tela |
| A9 | Recorte dos dados | `data/pois.csv` | No máximo 20 locais, todos com nome, categoria válida e coordenadas; sem `osm_id` repetido | `tests/test_dados.py` |
| A10 | Ponto representativo | Polígono de parque (teste com geometria montada à mão) | O ponto calculado fica dentro do polígono | `tests/test_dados.py` |

## 5. Arquivos obrigatórios no repositório

- [ ] `README.md` com o problema, o público-alvo, os integrantes, as técnicas, a fonte dos dados, os requisitos e os comandos exatos:
  ```
  pip install -r requirements.txt
  pip install -e .
  python scripts/baixar_dados.py     # opcional: data/pois.csv já vem no repositório
  python scripts/experimentos.py
  streamlit run app/app.py
  pytest
  ```
- [ ] `DADOS.md` com o nome da base, o responsável, a consulta OSMnx, a data de acesso, a licença ODbL e a atribuição, os arquivos usados, o **SHA-256** do bruto e do CSV, as contagens antes e depois do tratamento, o dicionário de atributos e o procedimento do recorte.
- [ ] `USO_DE_FERRAMENTAS.md` com as bibliotecas, os trechos externos e o uso de IA generativa (inclusive o Claude), dizendo onde e como a equipe verificou o que foi gerado.
- [ ] `requirements.txt` com as versões fixadas.
- [ ] `data/pois.csv` e `data/cenarios.csv` versionados, para a demonstração sem internet.
- [ ] Relatório técnico de **5 a 8 páginas** em `relatorio/`, com problema, dados, representação, algoritmos, arquitetura, protocolo, métricas, resultados, limitações, conclusão, referências (Russell e Norvig, busca local e otimização) e **contribuições individuais**.
- [ ] Slides da apresentação.

## 6. Apresentação (05/12/2026)

| Tempo | Conteúdo | Quem apresenta (sugestão) |
|---|---|---|
| 2 min | Problema, usuário e dados | Integrante 1 |
| 4 min | Representação, vizinhança, guloso, subida de encosta e têmpera | Integrantes 2 e 3 |
| 5 min | Demonstração ao vivo: montar um roteiro, mudar as preferências (A4), comparar os métodos, exportar e o caso de orçamento insuficiente (A3) | Integrante 4 |
| 3 min | Comparação experimental (utilidade, viabilidade, avaliações, estabilidade) | Integrante 3 |
| 1 min | Limitações e contribuições | Integrante 5 |
| 5 min | Perguntas | Todos |

A demonstração roda **offline**, com `data/pois.csv` já versionado.

## 7. Checklist final (antes de criar a tag)

- [ ] Clone limpo em outro computador seguindo só o README: tudo funciona.
- [ ] `pytest` passa.
- [ ] Os resultados em `resultados/` correspondem aos números do relatório e dos slides.
- [ ] Não há senhas, caminhos pessoais ou dados brutos grandes no Git.
- [ ] Os 5 integrantes sabem localizar no código e explicar a função objetivo, a vizinhança, o guloso, a subida de encosta, a têmpera e a interface.
- [ ] Tag `entrega-05-12-2026` criada e enviada (`git tag entrega-05-12-2026 && git push origin entrega-05-12-2026`).
- [ ] Link, commit, nomes e matrículas enviados ao professor.
