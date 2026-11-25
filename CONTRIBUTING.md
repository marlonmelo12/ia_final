# Fluxo de trabalho no Git

O objetivo é que **5 pessoas trabalhem ao mesmo tempo sem conflitos**. As três regras de ouro:

1. **Cada arquivo tem um dono.** Você só edita os arquivos do seu papel. A lista está em `BACKLOG.md` e em `.github/CODEOWNERS`.
2. **Ninguém envia direto para a `main`.** Tudo entra por *pull request* revisado.
3. **Branches pequenas e curtas**: uma por item do backlog, integrada em até 1 ou 2 dias.

## Branches

```
main                      ← sempre funcionando; protegida; só recebe PR
 ├── dados/D3-selecao-pois
 ├── problema/P5-vizinhanca
 ├── busca/B2-tempera
 ├── interface/I1-esqueleto
 ├── qualidade/Q3-persistencia
 └── fix/<descricao>      ← só correções, depois do congelamento em 02/12
```

Formato: `<papel>/<ID>-<descricao-curta>`. Os prefixos são `dados`, `problema`, `busca`, `interface`, `qualidade`, `docs` e `fix`.

## Passo a passo de cada tarefa

```bash
# 1. Comece sempre da main atualizada
git switch main
git pull

# 2. Crie a branch da tarefa
git switch -c busca/B2-tempera

# 3. Trabalhe e faça commits pequenos (com o ID na mensagem)
git add src/roteiro/tempera.py
git commit -m "B2: têmpera simulada guarda a melhor solução viável"

# 4. Antes de abrir o PR, traga as novidades da main (rebase evita commits de merge)
git fetch origin
git rebase origin/main
pytest

# 5. Envie e abra o PR no GitHub
git push -u origin busca/B2-tempera
```

No GitHub, abra o PR para a `main`, preencha o modelo e peça revisão ao revisor indicado no backlog.
A integração é feita com **Squash and merge**, e a branch é apagada depois.

Se o rebase der conflito: resolva no editor, depois `git add <arquivo>` e `git rebase --continue`.
Se ficar confuso, `git rebase --abort` volta tudo como estava. Peça ajuda no grupo.

## Mensagens de commit

`<ID>: <o que mudou, no presente>`. Exemplos:
- `D3: seleciona os 20 locais mais próximos do centro`
- `P2: tempo do roteiro inclui o retorno à partida`
- `fix: mensagem de erro para coordenada fora de Fortaleza`

## Como evitar conflitos

| Situação | Regra |
|---|---|
| `src/roteiro/contratos.py` | Congelado depois do Q2 (26/11). Para mudar, abra um PR com o título `CONTRATO:`, que precisa da aprovação de **todos**. |
| `requirements.txt` | Já tem todas as dependências previstas. Se precisar de outra, peça ao Integrante 5 ou adicione **uma linha** no seu PR, em ordem alfabética. |
| `README.md` | Dono: Integrante 5. Mande o trecho do seu módulo para ele. |
| Relatório | Cada um escreve só em `relatorio/secoes/0X_*.md`. O Integrante 5 monta o arquivo final. |
| Notebooks | Só em `notebooks/<seu-nome>/`, **sem saídas** (limpe antes do commit). Notebook não substitui o código em `src/`. |
| Dados brutos grandes | Nunca vão para o Git (`.gitignore`). As exceções são `data/pois.csv` (Integrante 1) e `data/cenarios.csv` (Integrante 2), pequenos e versionados. |
| Arquivo de outro integrante | Não edite. Abra uma *issue* ou comente no PR do dono. |
| Fim de linha (Windows × Linux) | Já resolvido pelo `.gitattributes`. Não altere. |

## Congelamento (a partir de 02/12)

- A `main` só recebe branches `fix/` e `docs/`.
- Os parâmetros dos métodos congelam em 01/12 (B4). O experimento final, com as sementes 0 a 4, roda **uma única vez**, pelo Integrante 3 (B5).
- Em 04/12, o Integrante 5 cria a tag `entrega-05-12-2026`, que nunca mais é movida.

## Ambiente local

```bash
python -m venv .venv
# Windows:   .venv\Scripts\activate
# Linux/Mac: source .venv/bin/activate
pip install -r requirements.txt
pip install -e .          # deixa o pacote `roteiro` importável em scripts, app e testes
pytest
```
