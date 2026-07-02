# ETL — Despesas de Viamão/RS (TCE-RS/SIAPC)

Documentação do pipeline de dados (princípio **P3**: todo o ETL é documentado e
reproduzível). O pipeline é **determinístico** e roda em duas etapas, na ordem:

```
etl/01_coleta.py   →   etl/02_processa.py
   (Extração)            (Transformação + Carga)
```

Fonte: **TCE-RS / SIAPC — Dados Abertos** (API CKAN). Os dados são de
responsabilidade da Prefeitura de Viamão, enviados via SIAPC, e **não foram
auditados** pelo Tribunal.

---

## Como reproduzir

```bash
# na raiz do projeto, com o .venv ativo
python etl/01_coleta.py     # baixa os 6 ZIPs (2019–2024) para dados/raw/
python etl/02_processa.py   # gera dados/auditoria/*.xlsx e dados/processed/*.parquet
```

Pré-requisitos: dependências do `requirements.txt` instaladas. A coleta exige
acesso à internet; o processamento roda offline sobre os ZIPs já baixados.

---

## E — Extração (`01_coleta.py`)

- Consulta a API CKAN do TCE-RS (`package_show`) para cada ano de **2019 a 2024**,
  dataset `despesa-orcamentaria-por-empenhos-pm-de-viamao-{ANO}`, e baixa o recurso
  **ZIP** de cada ano para `dados/raw/viamao_despesa_{ANO}.zip`.
- Registra a proveniência de cada arquivo em **`dados/raw/manifest_coleta.csv`**:
  ano, nome, URL, tamanho em bytes, **hash MD5** e data/hora da coleta.
- Ano indisponível é registrado como ausente — **nunca inventado** (P1). A coleta
  falha de forma clara se algum ano não vier (P4).

Os ZIPs em `dados/raw/` **não são modificados** (P2) e não são versionados
(`.gitignore`) — são regeneráveis por este script.

---

## T — Transformação (`02_processa.py`)

### Leitura dos CSVs

Cada ZIP contém um único `63000.csv`. Parâmetros de leitura, **confirmados por
inspeção dos 6 arquivos** (não assumidos):

| Parâmetro | Valor | Observação |
|---|---|---|
| Encoding | `utf-8-sig` | os arquivos trazem BOM (`EF BB BF`) |
| Separador de campo | vírgula `,` | (não é `;`) |
| Separador decimal | ponto `.` | sem separador de milhar (ex.: `2000000.00`) |
| Parser | `pandas.read_csv` respeitando aspas | `historico` é texto livre com vírgulas — `split(',')` corromperia |
| Tipagem na leitura | tudo como `str` (`dtype=str`, `na_filter=False`) | preserva zeros à esquerda de códigos e mantém `''` literal |

### Schema entre anos

Os arquivos de **2019–2021 têm 46 colunas** e os de **2022–2024 têm 48**. As duas
colunas extras a partir de 2022 são `cd_fonte_recurso` e `cd_acomp_exec_orc`,
**fora do escopo** de 3.1/3.2/3.3. O processamento seleciona um **subconjunto
curado comum**, presente e verificado em todos os anos.

### Colunas do dataset normalizado

`ano` (ano do arquivo/exercício), `ano_recebimento`, `mes_recebimento`,
`ano_empenho`, `ano_operacao`, `tipo_operacao`, `tipo_operacao_desc`,
`cd_orgao_orcamentario`, `nome_orgao_orcamentario`, `cd_unidade_orcamentaria`,
`nome_unidade_orcamentaria`, `cd_funcao`, `ds_funcao`, `cd_subfuncao`,
`ds_subfuncao`, `cd_elemento`, `cd_rubrica`, `ds_rubrica`, `cd_credor`,
`nm_credor`, `tp_pessoa`, `cnpj_cpf`, `nr_empenho`, `nr_liquidacao`,
`nr_pagamento`, `vl_empenho`, `vl_liquidacao`, `vl_pagamento`, `dt_empenho`,
`dt_operacao`, `historico`.

Os nomes originais do TCE-RS foram mantidos (já são `snake_case` claros): a
normalização é **seleção + tipagem**, não renomeação — menos transformação, mais
fidelidade à fonte (P1).

### Tipagem aplicada

- **Valores** (`vl_empenho`, `vl_liquidacao`, `vl_pagamento`) → `float`.
  Célula vazia → `NaN`. Conversão com `errors="raise"`: qualquer valor não numérico
  inesperado **quebra o script** (P4) em vez de virar `NaN` silencioso (P1). A
  inspeção confirmou **0 erros de parse** nos 6 anos.
- **Inteiros** (`ano_*`, `mes_recebimento`) → `Int64` (nullable).
- **Datas** (`dt_empenho`, `dt_operacao`) → `datetime` (`YYYY-MM-DD`); vazio → `NaT`.
  Datas não vazias que não parseiam são reportadas, não silenciadas.
- **Códigos e `cnpj_cpf`** → mantidos como **texto** (preservam formato, ex.:
  `cd_elemento = 3.1.90.01`).

### Estrutura dos registros (importante para as análises)

Cada linha é **uma operação** e `tipo_operacao` assume exatamente **`E`/`L`/`P`**
(Empenho / Liquidação / Pagamento) nos 6 anos. A coluna de valor correspondente é
a preenchida; as outras ficam vazias. Portanto:

- **Seções 3.1 e 3.2** → filtrar `tipo_operacao == "L"` e somar `vl_liquidacao`.
- **Seção 3.3** → filtrar `tipo_operacao == "P"` e somar `vl_pagamento`.

### Decisões de dados (P1)

- **Valores negativos são estornos/anulações e foram MANTIDOS.** Há milhares por
  ano (ex.: 2024 — 1.501 liquidações e 1.524 pagamentos negativos). Descartá-los
  inflaria os totais; as somas geradas são **líquidas**. Nenhum `fillna(0)` foi
  aplicado.
- **`cnpj_cpf` ausente em ~30% dos registros** (123.809 de 408.953 no total).
  Ausência = `NaN` (P1); `nm_credor`, ao contrário, está 100% preenchido. A fonte
  **não guarda zeros à esquerda** do CNPJ/CPF (ex.: TRT-4 = `2520619000152`); o
  valor é preservado verbatim. Padronização para 14 dígitos, se necessária, é
  decisão da análise 3.3 e será documentada lá.
- **Descartes:** nenhum registro é descartado nesta etapa. Duplicatas exatas são
  apenas **contadas e reportadas** (na aba Metadados de cada auditoria), não
  removidas — a fonte pode conter operações legítimas idênticas, e o filtro por
  tipo/escopo é feito nas fases de análise, não no ETL.

### Ressalva temporal (crítica para 3.1/3.2/3.3)

O arquivo de um ano contém operações cujo `ano_operacao` é de **anos anteriores**
(restos a pagar / ajustes). Proporção de operações do próprio ano dentro de cada
arquivo:

| Arquivo | Do próprio ano | De outros anos |
|---|---|---|
| 2019 | 88,0% | 12,0% |
| 2020 | 83,0% | 17,0% |
| 2021 | 86,3% | 13,7% |
| 2022 | 92,5% | 7,5% |
| 2023 | 96,2% | 3,8% |
| 2024 | 96,8% | 3,2% |

Por isso o dataset **preserva** `ano` (ano do arquivo/exercício), `ano_recebimento`,
`ano_operacao` e `ano_empenho`. A escolha da chave temporal ("despesa do exercício"
vs. "operações datadas no ano") é feita — e justificada — em cada fase de análise.

---

## C — Carga (saídas)

### `dados/auditoria/viamao_despesa_{ANO}_auditoria.xlsx` (evidência primária — P2)

Um Excel por ano, com duas abas:

- **Dados** — todos os registros do ano, colunas padronizadas.
- **Metadados** — fonte, URL do recurso, ZIP original, tamanho, **MD5**, data/hora
  da coleta, encoding/separador, contagem por tipo (E/L/P), somas líquidas de
  empenho/liquidação/pagamento, nº de negativos, `cnpj_cpf` ausentes e duplicatas.

São **regeneráveis** (script determinístico + ZIPs com MD5 no manifest) e, por isso
e pelo tamanho (~60 MB no total), **não são versionados** (`.gitignore`).

### `dados/processed/viamao_despesa_consolidado.parquet`

Todos os anos empilhados (408.953 linhas × 31 colunas), formato Parquet
(`pyarrow`). É o insumo dos notebooks de análise. Regenerável — **não versionado**.

### Checagem de integridade

As somas por ano no Parquet conferem com o resumo impresso pelo `02_processa.py`:

| Ano | Liquidação (R$) | Pagamento (R$) |
|---|---:|---:|
| 2019 | 489.488.993,67 | 441.581.461,90 |
| 2020 | 554.619.153,77 | 526.196.573,05 |
| 2021 | 620.202.152,14 | 590.205.606,57 |
| 2022 | 683.783.421,80 | 665.733.559,66 |
| 2023 | 675.417.284,70 | 662.235.805,44 |
| 2024 | 739.475.339,09 | 734.914.063,59 |

Valores **nominais** (sem deflação). A conversão para valores reais (deflator IPCA,
base 2024) é feita nas fases de análise e documentada lá.

---

Fonte dos dados: **TCE-RS/SIAPC**. Elaboração própria.
