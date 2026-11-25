# Definição da Entrega Final — Questão 6: Previsão de consumo de energia

Este documento define **o que conta como entregue**. Um item só é marcado quando a evidência
indicada existir no repositório, no commit da tag `entrega-05-12-2026`.

## 1. Identificação

| Campo | Valor |
|---|---|
| Projeto | Questão 6 — Sistema de previsão de consumo de energia |
| Repositório | _(link)_ |
| Commit avaliado | _(hash)_ |
| Tag | `entrega-05-12-2026` (criada no commit acima e **nunca movida**) |
| Acesso do professor | Leitura concedida em: _(data)_ |
| Integrantes / matrículas | _(5 nomes e matrículas)_ |
| Envio | Até 04/12/2026, 23h59 (Fortaleza) · Apresentação: 05/12/2026 |

## 2. Produto: o sistema

O avaliador deve conseguir abrir o README, instalar, executar e percorrer o fluxo principal **sem editar código**.

| Requisito | Critério de aceite | Evidência |
|---|---|---|
| Dados externos | Base UCI 235, de janeiro de 2007 a dezembro de 2009, obtida por script | `scripts/baixar_dados.py` e `DADOS.md` |
| Preparação | Agregação diária em kWh, só dias com 1.440 medições, reindexação antes das defasagens, contagem de dias excluídos | `src/energia/dados.py`, `atributos.py` e as contagens no `DADOS.md` |
| Método de IA | Persistência, regressão linear e Ridge, com o alpha escolhido só na validação | `src/energia/modelos.py`, `scripts/treinar.py` e a tabela de validação |
| Interface (web) | Mostra a janela histórica, a previsão e a unidade; permite selecionar o período de avaliação, consultar o teste e exportar | `app/app.py` e capturas de tela no relatório |
| Persistência | Execuções gravadas com entradas, parâmetros, modelo e versão, e resultados; histórico consultável e exportável | `src/energia/persistencia.py` e um arquivo de exemplo exportado |
| Arquitetura | Interface, dados, núcleo de IA e persistência em módulos separados | Estrutura de `src/` e `app/` |
| Reprodução | Instalação e execução testadas em outro computador | `README.md`, `requirements.txt` e o nome de quem testou, com a data |

## 3. Resultados experimentais obrigatórios

Todos devem ser gerados por `scripts/experimentos.py` e salvos em `resultados/`.

- [ ] Tabela com o **MAE e o RMSE dos três métodos** no teste (julho a dezembro de 2009), todos no mesmo conjunto de dias.
- [ ] Tabela da validação (janeiro a junho de 2009) com os alphas testados e o escolhido.
- [ ] Gráfico de observado versus previsto, com **pelo menos 30 dias** do teste.
- [ ] Gráfico ou análise dos resíduos, com os maiores erros comentados.
- [ ] Comparação explícita com a persistência.
- [ ] Contagens: dias totais, dias excluídos por estarem incompletos e amostras por partição.
- [ ] Registro do ambiente: versões do Python e das bibliotecas, sistema operacional e semente.
- [ ] Discussão dos limites da extrapolação: uma única residência, período de 2007 a 2009, mudanças de hábito e sazonalidade.

## 4. Casos de aceitação

Cada caso tem uma entrada, a saída esperada e uma evidência: um teste em `tests/` ou um roteiro reproduzível.

| # | Caso | Entrada | Saída esperada | Evidência |
|---|---|---|---|---|
| A1 | Agregação diária correta | Um dia completo escolhido | kWh calculado à mão = kWh do sistema, dentro de 1e-6 | `tests/test_agregacao.py` e o cálculo manual no relatório |
| A2 | Dia incompleto excluído | Dia com menos de 1.440 medições | Não aparece como alvo e é contado como excluído | `tests/test_agregacao.py` |
| A3 | Sem atributos futuros | Qualquer linha de atributos | Todas as defasagens usam datas anteriores à data do alvo | `tests/test_sem_futuro.py` |
| A4 | Defasagem respeita o calendário | Dia cujo dia anterior foi excluído | `lag1` fica faltante e a amostra é descartada; não usa o "registro anterior disponível" | `tests/test_sem_futuro.py` |
| A5 | Histórico insuficiente | Data alvo sem os 7 dias anteriores completos | A interface recusa e explica o motivo | `tests/test_previsao.py` e captura de tela |
| A6 | Script = interface | Mesma data e mesmo modelo | Previsões idênticas | `tests/test_igualdade.py` |
| A7 | Teste reservado | Treino e seleção do alpha | Nenhuma data de julho a dezembro de 2009 é usada no ajuste ou na escolha | `tests/test_divisao.py` |
| A8 | Entrada inválida | Período fora da base ou data mal formatada | Mensagem de erro compreensível, sem *traceback* | Captura de tela |
| A9 | Reprodutibilidade | Executar `treinar.py` duas vezes | Mesmos coeficientes e mesmas métricas | Log no relatório |

## 5. Arquivos obrigatórios no repositório

- [ ] `README.md` com o problema, o público-alvo, os integrantes, as técnicas, a fonte dos dados, os requisitos e os comandos exatos:
  ```
  pip install -r requirements.txt
  python scripts/baixar_dados.py
  python scripts/preparar_dados.py
  python scripts/treinar.py
  python scripts/experimentos.py
  streamlit run app/app.py
  pytest
  ```
- [ ] `DADOS.md` com o nome da base, o responsável, a URL, a data de acesso, a licença (CC BY 4.0, a confirmar na página), os arquivos usados, o **SHA-256** do arquivo baixado, os registros antes e depois do tratamento, o dicionário de atributos e o procedimento do recorte.
- [ ] `USO_DE_FERRAMENTAS.md` com as bibliotecas, os trechos externos e o uso de IA generativa (inclusive o Claude), dizendo onde e como a equipe verificou o que foi gerado.
- [ ] `requirements.txt` com as versões fixadas.
- [ ] Modelos salvos em `models/` ou treinamento totalmente reproduzível.
- [ ] Amostra de dados versionada para a demonstração, já que a base completa fica fora do Git.
- [ ] Relatório técnico de **5 a 8 páginas** em `relatorio/`, com problema, dados, representação, algoritmos, arquitetura, protocolo, métricas, resultados, limitações, conclusão, referências e **contribuições individuais**.
- [ ] Slides da apresentação.

## 6. Apresentação (05/12/2026)

| Tempo | Conteúdo | Quem apresenta (sugestão) |
|---|---|---|
| 2 min | Problema, usuário e dados | Integrante 1 |
| 4 min | Representação, métodos e arquitetura | Integrantes 2 e 3 |
| 5 min | Demonstração ao vivo: previsão, consulta ao teste, exportação e o caso-limite A5 | Integrante 4 |
| 3 min | Comparação experimental (MAE/RMSE, gráfico, resíduos) | Integrante 3 |
| 1 min | Limitações e contribuições | Integrante 5 |
| 5 min | Perguntas | Todos |

A demonstração roda **offline**, com os dados e modelos já preparados.

## 7. Checklist final (antes de criar a tag)

- [ ] Clone limpo em outro computador seguindo só o README: tudo funciona.
- [ ] `pytest` passa.
- [ ] Os resultados em `resultados/` correspondem aos números do relatório e dos slides.
- [ ] Não há senhas, caminhos pessoais ou dados grandes no Git.
- [ ] Os 5 integrantes sabem localizar no código e explicar a agregação, as defasagens, a divisão, os modelos e a interface.
- [ ] Tag `entrega-05-12-2026` criada e enviada (`git tag entrega-05-12-2026 && git push origin entrega-05-12-2026`).
- [ ] Link, commit, nomes e matrículas enviados ao professor.
