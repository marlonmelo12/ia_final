# Registro dos dados

> Dono: Integrante 1 (itens D1, D4 e D6 do `BACKLOG.md`).

| Campo | Valor |
|---|---|
| Base | Pontos de interesse do OpenStreetMap, município de Fortaleza |
| Responsável | OpenStreetMap Foundation e colaboradores do OpenStreetMap |
| URL / acesso | `osmnx.features_from_place("Fortaleza, Ceará, Brazil", tags)` — https://osmnx.readthedocs.io/en/stable/user-reference.html (seção *features*) |
| Tags consultadas | `tourism=attraction`, `tourism=museum`, `leisure=park` |
| Data de acesso | |
| Licença / condições de uso | Open Database License (ODbL) 1.0 — atribuição: "© OpenStreetMap contributors", https://www.openstreetmap.org/copyright |
| Versão do OSMnx | |
| Arquivo bruto | `data/raw/pois_osm.geojson` (fora do Git) e o SHA-256 dele |
| Arquivo utilizado | `data/pois.csv` (versionado), com SHA-256 |
| Elementos retornados (total e por categoria e tipo de geometria) | |
| Após filtro de nome | |
| Após remoção de duplicados | |
| Selecionados | 20 (ou todos, se houver menos; registrar a contagem) |

## Dicionário de atributos (`data/pois.csv`)

| Coluna | Tipo | Descrição |
|---|---|---|
| `osm_id` | texto | Tipo e identificador OSM, por exemplo `node/123` ou `way/456` |
| `nome` | texto | Tag `name` |
| `categoria` | texto | `museum`, `attraction` ou `park` (ordem de prioridade se houver mais de uma tag) |
| `lat`, `lon` | float | Ponto representativo (WGS84); para polígonos, ver o procedimento |

## Procedimento de reprodução do recorte

<!-- Filtro de nome, regra de deduplicação, ponto representativo dos polígonos,
     regra de seleção dos 20 locais (decisão 1 do PLANEJAMENTO.md) e o comando exato. -->

## Hipóteses do modelo (não são dados observados)

Visita de 30 minutos, deslocamento pela distância geodésica a 4 km/h e preferências inteiras de 1 a 5
por categoria. São hipóteses acadêmicas do enunciado, e não tempos reais de caminhada pelas ruas.
