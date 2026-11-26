# Registro dos dados

> Dono: Integrante 1 (itens D1, D4 e D6 do `BACKLOG.md`).

| Campo | Valor |
|---|---|
| Base | Pontos de interesse do OpenStreetMap, município de Fortaleza |
| Responsável | OpenStreetMap Foundation e colaboradores do OpenStreetMap |
| URL / acesso | `osmnx.features_from_place("Fortaleza, Ceará, Brazil", tags)` — https://osmnx.readthedocs.io/en/stable/user-reference.html (seção *features*) |
| Tags consultadas | `tourism=attraction`, `tourism=museum`, `leisure=park` |
| Data de acesso | 26/11/2026 16:14 (horário de Fortaleza, UTC-3) |
| Licença / condições de uso | Open Database License (ODbL) 1.0 — atribuição: "© OpenStreetMap contributors", https://www.openstreetmap.org/copyright |
| Versão do OSMnx | 2.2.0 (Python 3.15.2, geopandas 1.2.0, shapely 2.2.0) |
| Arquivo bruto | `data/raw/pois_osm.geojson` (fora do Git), SHA-256 `45079035c73ea1c4dcc1000c4a8f4871829a73f9e60cdbbc41abc502a5a6c1e2`. O OSM muda com o tempo, então uma consulta em outra data pode gerar outro hash. |
| Arquivo utilizado | `data/pois.csv` (versionado), com SHA-256 |
| Elementos retornados (total e por categoria e tipo de geometria) | 651 no total: 31 com `tourism` e 622 com `leisure`, sendo 616 Polygon, 18 Point, 16 MultiPolygon e 1 LineString. O detalhe por categoria entra no D4. |
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
