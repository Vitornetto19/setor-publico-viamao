# TAREFAS — Diagnóstico Orçamentário de Viamão/RS

Roadmap de execução do projeto, organizado em **fases** seguindo o princípio **P4 (baby
steps)**: cada etapa é pequena, verificável e independente, e **não se pula etapa**. A
sequência obrigatória é:

```
01_coleta.py → 02_processa.py → 00_exploratorio → 31_institucional → 32_funcional → 33_credores
```

Legenda: `- [ ]` pendente · `- [x]` concluído. Cada fase tem um **Critério de pronto**.

> Referências: [`docs/01_CONTEXTO_PROJETO.md`](docs/01_CONTEXTO_PROJETO.md),
> [`docs/02_PRINCIPIOS.md`](docs/02_PRINCIPIOS.md), [`docs/03_REQUISITOS_TRABALHO.md`](docs/03_REQUISITOS_TRABALHO.md).

---

## Fase 0 — Setup do projeto ✅ (concluída)

- [x] Verificar ambiente (git, gh, autenticação GitHub)
- [x] Criar `.gitignore`, `.gitattributes`, `README.md`
- [x] Criar scaffold de pastas (`dados/`, `etl/`, `notebooks/`, `output/`)
- [x] Escrever este `TAREFAS.md`
- [x] `git init` + commit inicial + publicar `setor-publico-viamao` no GitHub
- [x] Criar `requirements.txt` (pandas, requests, openpyxl, pyarrow, matplotlib, jupyter)
- [x] Criar ambiente virtual (`.venv`) e instalar dependências; kernel Jupyter registrado

**Critério de pronto:** repositório publicado no GitHub; ambiente Python rodando `import pandas`.

---

## Fase 1 — Organização das pastas e materiais ✅ (concluída)

- [x] Confirmar estrutura de pastas conforme seção 5 do `docs/01_CONTEXTO_PROJETO.md`
- [x] Organizar `docs/`: requisitos (`01/02/03_*.md`) na raiz de `docs/` e materiais-fonte da
      professora (modelo Charqueadas, orientações, tabelas) em `docs/materiais_professora/`
- [x] Conferir que `dados/raw/` e `dados/processed/` estão ignorados pelo git (só `.gitkeep`)

**Critério de pronto:** `git status` limpo; estrutura idêntica à documentada.

---

## Fase 2 — ETL · Coleta (`etl/01_coleta.py`)  — Princípios P2, P3 ✅ (concluída)

- [x] Consultar a API CKAN do TCE-RS: `package_show?id=despesa-orcamentaria-por-empenhos-pm-de-viamao-{ANO}`
- [x] Baixar os ZIPs de **2019 a 2024** → `dados/raw/viamao_despesa_{ANO}.zip` (não modificar)
- [x] Registrar, para cada arquivo: URL, nome, **hash MD5**, data/hora da extração
      (em `dados/raw/manifest_coleta.csv`)
- [x] Print de resumo: anos baixados, tamanho e hash de cada ZIP

**Critério de pronto:** 6 ZIPs em `dados/raw/`; nenhum ano faltando sem justificativa.
**Regra P1:** ano indisponível fica registrado como ausente — nunca inventar.

---

## Fase 3 — ETL · Processamento (`etl/02_processa.py`)  — Princípios P1, P2, P3, P5 ✅ (concluída)

- [x] Extrair e ler os CSVs de cada ZIP (encoding `utf-8-sig` + BOM, separador `,`, decimal `.` — confirmados por inspeção)
- [x] Normalizar colunas-chave (nomes reais do TCE-RS): `nome_orgao_orcamentario`, `ds_funcao`/`cd_funcao`,
      `nm_credor`/`cnpj_cpf`, `vl_empenho`, `vl_liquidacao`, `vl_pagamento`, `tipo_operacao` (E/L/P)
- [x] Converter valores monetários para numérico (`errors="raise"`; 0 erros de parse nos 6 anos)
- [x] Documentar descartes: nenhum registro removido; negativos = estornos (mantidos, somas líquidas);
      duplicatas exatas contadas na aba Metadados; ressalva temporal (`ano_operacao`) documentada
- [x] Gerar **`dados/auditoria/viamao_despesa_{ANO}_auditoria.xlsx`** por ano:
      - Aba **Dados** (todos os registros, colunas padronizadas)
      - Aba **Metadados** (fonte, URL, ZIP original, data/hora, nº de registros, MD5)
- [x] Gerar **`dados/processed/viamao_despesa_consolidado.parquet`** (408.953 linhas × 31 colunas)
- [x] Escrever **`etl/README_ETL.md`** documentando Extração → Transformação → Carregamento
- [x] Print de resumo: linhas por ano, totais de liquidação/pagamento (validados contra o parquet)

**Critério de pronto:** Excel de auditoria por ano + parquet consolidado + README_ETL escrito.
**Regra P1:** nada de `fillna(0)` sem comentário justificando; ausência = `NaN`/`null`.

---

## Fase 4 — Notebook exploratório (`notebooks/00_exploratorio.ipynb`)  — Princípio P6 ✅ (concluída)

- [x] Contagem de linhas por ano (2019–2024 completos; 408.953 operações)
- [x] Tipos de operação (Empenho, Liquidação, Pagamento) e quantidades (só E/L/P — verificado)
- [x] Lista de **funções** (36) e **órgãos** (25) únicos, com estabilidade entre anos
- [x] Top 10 credores brutos por `vl_pagamento` (antes de qualquer filtro; internos sinalizados p/ 3.3)
- [x] Verificação de nulos nas colunas críticas (valores nulos são estruturais; `cnpj_cpf` ~30% ausente)
- [x] Totais de liquidação e pagamento por ano **conferidos contra os Excels de auditoria** (dif. < R$ 0,01)

**Critério de pronto:** notebook roda do início ao fim; sanity checks batem com a auditoria.
Executado com `nbconvert --execute` (0 erros); conferência automática contra `dados/auditoria/*.xlsx`.

---

## Fase 5 — Seção 3.1 · Institucional (`notebooks/31_institucional.ipynb`)

Variável: `vl_Liquidacao` · filtro tipo = **Liquidação** · agrupar por `nm_OrgaoOrcamentario`.

- [ ] Tabela 3.1.A — despesa liquidada por órgão × ano (R$ nominais), ordenada por 2024
- [ ] Tabela 3.1.B — participação relativa (%) por órgão × ano
- [ ] Variação nominal e **real** (deflator IPCA base 2024) 2019→2024 por órgão
- [ ] Gráfico 3.1 — barras empilhadas da participação por órgão (título, fonte, eixos)
- [ ] Exportar `output/tabelas/3_1_despesa_por_orgao.xlsx` e `output/graficos/3_1_evolucao_por_orgao.png`
- [ ] Texto de análise: 3.1.a (quem domina e por quê) e 3.1.b (houve inversão? contexto)

**Critério de pronto:** 2+ tabelas e 1 gráfico exportados; perguntas 3.1.a/b respondidas.

---

## Fase 6 — Seção 3.2 · Funcional (`notebooks/32_funcional.ipynb`)

Variável: `vl_Liquidacao` · filtro **Liquidação** · agrupar por `nm_Funcao` (Portaria 42/1999).

- [ ] Coletar dados externos **com fonte registrada** (P1): população IBGE por ano, IPCA
      anual, IDH (Atlas Brasil), mortalidade infantil (Datasus), analfabetismo (IBGE), IDESE (DEE/RS)
- [ ] Tabela 3.2.A — despesa por função × ano (nominal e real), variação % nominal e real
- [ ] Tabela 3.2.B — gasto per capita em Saúde e Educação por ano
- [ ] Tabela 3.2.C — funções-meio vs. funções-fim (totais e participação %)
- [ ] Tabela 3.2.D — indicadores sociais de Viamão (dados externos)
- [ ] Gráfico 3.2.A — evolução das principais funções
- [ ] Gráfico 3.2.B — per capita Saúde + Educação (barras duplas por ano)
- [ ] Gráfico 3.2.C — meio vs. fim (barras empilhadas 100%)
- [ ] Exportar `output/tabelas/3_2_despesa_por_funcao.xlsx` e os PNGs em `output/graficos/`
- [ ] Texto de análise: 3.2.a (maior crescimento), 3.2.b (saúde/educação + cruzamento social),
      3.2.c (meio vs. fim); contextualizar pandemia (2020/21) e enchentes RS (2024)

**Critério de pronto:** tabelas A–D + 3 gráficos exportados; perguntas 3.2.a/b/c respondidas;
deflator IPCA documentado.

---

## Fase 7 — Seção 3.3 · Credores (`notebooks/33_credores.ipynb`)

Variável: `vl_Pagamento` · filtro tipo = **Pagamento** · agrupar por `nm_Credor` + `cpf_cnpj_Credor`.

- [ ] Tratar credores internos (Prefeitura/órgão próprio) vs. fornecedores externos
- [ ] Tabela 3.3.A — Top 20 credores de 2024 (nome, CNPJ, valor pago, % do total, % acumulado)
- [ ] Tabela 3.3.B — credores recorrentes (aparecem em 2022, 2023 e 2024)
- [ ] Gráfico 3.3 — concentração dos Top 10 (barras horizontais ou pizza)
- [ ] Exportar `output/tabelas/3_3_maiores_credores_2024.xlsx` e `output/graficos/3_3_concentracao_credores.png`
- [ ] Texto de análise: 3.3.a (quem/qual setor), 3.3.b (concentração — os 5 maiores = X%),
      3.3.c (recorrência à luz da ciência econômica: concorrência, rent-seeking, barreiras à entrada)

**Critério de pronto:** tabelas A/B + gráfico exportados; perguntas 3.3.a/b/c respondidas.

---

## Fase 8 — Fechamento e entrega

- [ ] Rodar o **checklist final** do `docs/03_REQUISITOS_TRABALHO.md`
- [ ] Conferir que toda tabela/gráfico cita fonte ("TCE-RS/SIAPC. Elaboração própria.")
- [ ] Conferir distinção clara entre valores nominais e reais; deflator documentado
- [ ] Verificar que todos os notebooks rodam do início ao fim sem erro
- [ ] Commit e push de cada entregável em `output/`
- [ ] Redigir os textos analíticos finais (fora do código) com base nos outputs

**Critério de pronto:** todos os itens do checklist do `docs/03_REQUISITOS_TRABALHO.md` marcados.
