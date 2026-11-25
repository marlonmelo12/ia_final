# Registro dos dados

> Dono: Integrante 1 (itens D1, D4 e D6 do `BACKLOG.md`).

## Fonte

| Campo | Valor |
|---|---|
| Base | Individual Household Electric Power Consumption |
| Responsáveis (criadores) | Georges Hebrail e Alice Berard |
| Repositório | UCI Machine Learning Repository (doada em 29/08/2012) |
| URL da página | https://archive.ics.uci.edu/dataset/235/individual+household+electric+power+consumption |
| URL do arquivo | https://archive.ics.uci.edu/static/public/235/individual+household+electric+power+consumption.zip |
| DOI | https://doi.org/10.24432/C58K54 |
| Data de acesso | 25/11/2026 (download às 17:37 UTC) |
| Licença | Creative Commons Attribution 4.0 International (CC BY 4.0). Permite redistribuir com atribuição. |
| Citação | Hebrail, G. & Berard, A. (2006). *Individual Household Electric Power Consumption* [Dataset]. UCI Machine Learning Repository. https://doi.org/10.24432/C58K54 |
| Conteúdo | Medições por minuto de uma residência em Sceaux (a 7 km de Paris, França), de dezembro de 2006 a novembro de 2010 |

## Arquivos utilizados

| Arquivo | Tamanho (bytes) | SHA-256 |
|---|---|---|
| `individual_household_electric_power_consumption.zip` | 20.640.916 | `9f84b46ade8a2d8e1286ec4b2b6c2987a45a755c59f263be3b3b3d10dfbda3ff` |
| `household_power_consumption.txt` (extraído do .zip) | 132.960.755 | `4259c9d7ece5dbee9ab8d53682baac68d791c864f0f64a52b4043cb3b90894b7` |

Os arquivos ficam em `data/raw/` e **não** vão para o Git. Para obtê-los, rode `python scripts/baixar_dados.py`, que imprime os hashes. Confira se são iguais aos da tabela.

## Contagens (antes e depois do tratamento)

| Etapa | Quantidade |
|---|---|
| Registros brutos (minutos), de 16/12/2006 17:24 a 26/11/2010 21:02 | 2.075.259 |
| Registros brutos com `Global_active_power` faltante (`?`) | 25.979 (1,25%) |
| Registros no recorte (de 01/01/2007 00:00 a 31/12/2009 23:59) | 1.578.240 (= 1.096 dias × 1.440 minutos) |
| Registros faltantes no recorte | 8.346 |
| Timestamps duplicados no recorte | 0 |
| Dias no recorte | 1.096 (365 + 366 + 365; todos presentes no arquivo) |
| **Dias completos (1.440 medições válidas): usados como alvo** | **1.041** |
| **Dias excluídos (incompletos)** | **55** |

Distribuição das medições válidas nos 55 dias excluídos:

| Medições válidas | Dias |
|---|---|
| 1.439 | 26 |
| 1.438 | 12 |
| 1.434 a 1.437 | 3 |
| 1.397 a 1.419 | 5 |
| 1.310 e 1.370 | 2 |
| 549 a 985 | 3 |
| 21 e 30 | 2 |
| 0 (dia inteiro sem medição) | 2 |

**Limitação:** 38 dos 55 dias excluídos perderam só 1 ou 2 minutos. A regra de 1.440 medições vem do
enunciado e evita somas parciais, mas descarta dias quase completos. Essas exclusões também afetam as
defasagens dos dias seguintes (ver `PLANEJAMENTO.md`, decisão 2).

## Dicionário de atributos

**Na fonte** (separador `;`; faltante = `?`; data **sem zeros à esquerda**, por exemplo `2/1/2007`):

| Coluna | Descrição (página da UCI) | Unidade | Usada? |
|---|---|---|---|
| `Date` | Data, formato dd/mm/aaaa | — | Sim |
| `Time` | Hora, formato hh:mm:ss | — | Sim |
| `Global_active_power` | Potência ativa global da residência, média do minuto | kW | **Sim** |
| `Global_reactive_power` | Potência reativa global, média do minuto | kW | Não |
| `Voltage` | Tensão média do minuto | V | Não |
| `Global_intensity` | Corrente média do minuto | A | Não |
| `Sub_metering_1` | Submedição da cozinha | Wh | Não |
| `Sub_metering_2` | Submedição da lavanderia | Wh | Não |
| `Sub_metering_3` | Submedição do aquecedor de água e do ar-condicionado | Wh | Não |

**Gerado: `data/processed/diario.csv`** (contrato `COLUNAS_DIARIO` em `src/energia/contratos.py`):

| Coluna | Tipo | Descrição |
|---|---|---|
| `data` | data (AAAA-MM-DD) | Dia do calendário, de 2007-01-01 a 2009-12-31; uma linha por dia |
| `kwh` | float ou vazio | Energia do dia = Σ(`Global_active_power` / 60) nos 1.440 minutos. **Vazio** se o dia estiver incompleto |
| `n_medicoes` | int | Minutos com `Global_active_power` válido no dia (0 a 1.440) |

## Procedimento de reprodução do recorte

```bash
python scripts/baixar_dados.py     # baixa, extrai e imprime os SHA-256
python -m energia.dados            # gera data/processed/diario.csv e imprime as contagens
pytest tests/test_agregacao.py     # casos A1/A2 e conferência manual na base real
```

Passos implementados em `src/energia/dados.py`:

1. Ler apenas `Date`, `Time` e `Global_active_power`; o marcador `?` vira valor faltante.
2. Combinar data e hora em um `datetime` (`%d/%m/%Y %H:%M:%S`).
3. Manter as medições de 01/01/2007 a 31/12/2009, inclusive.
4. Descartar faltantes. Timestamps repetidos contariam uma vez só, mas não há nenhum.
5. Converter cada minuto em energia: kWh = kW / 60. Agrupar por dia, somando a energia e contando os minutos válidos.
6. Manter `kwh` apenas nos dias com exatamente 1.440 medições válidas. Nos demais, `kwh` fica vazio e o dia **continua no arquivo**, para que a reindexação e as defasagens (módulo de atributos, A1/A2) enxerguem a lacuna.

### Verificação manual (caso A1)

Cálculo independente, sem pandas, direto sobre o arquivo bruto:

```bash
awk -F';' -v d="2/1/2007" '$1==d && $3!="?" {s+=$3; n++} END {printf "n=%d kWh=%.6f\n", n, s/60}' data/raw/household_power_consumption.txt
```

| Dia | Medições válidas | Σ kW | kWh (manual) | kWh (`diario.csv`) |
|---|---|---|---|---|
| 02/01/2007 | 1.440 | 1.269,236 | 21,153933 | 21,153933 |
| 15/06/2008 | 1.440 | 2.289,102 | 38,151700 | 38,151700 |
| 14/01/2007 | 1.439 | 3.007,816 | — (excluído) | vazio |

Esses valores são verificados automaticamente em `tests/test_agregacao.py::test_a1_base_real_bate_com_calculo_manual`.
