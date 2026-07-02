# Diagnóstico Orçamentário de Viamão/RS — Despesas (2019–2024)

Trabalho acadêmico da disciplina de **Finanças do Setor Público** (Economia — UFRGS),
com análise das **despesas** do município de **Viamão/RS**.

> Este repositório cobre **exclusivamente a parte do Vitor**, responsável pelas seções:
>
> - **3.1** — Despesa por Classificação Institucional
> - **3.2** — Despesa por Classificação Funcional
> - **3.3** — Identificação dos Maiores Credores (2024)

## Fonte dos dados

- **Principal:** TCE-RS / SIAPC — Dados Abertos ([dados.tce.rs.gov.br](https://dados.tce.rs.gov.br/group/despesa)),
  dataset `despesa-orcamentaria-por-empenhos-pm-de-viamao-{ANO}`, via API CKAN.
- **Complementares:** IBGE (população, IPCA), Atlas Brasil/PNUD (IDH), Datasus
  (mortalidade infantil), DEE/RS (IDESE).

Dados de responsabilidade da Prefeitura de Viamão, enviados ao TCE-RS e **não auditados**
pelo Tribunal.

## Estrutura

```
docs/         requisitos do trabalho (01/02/03_*.md)
docs/materiais_professora/  materiais-fonte da professora (modelo Charqueadas, orientações, tabelas)
dados/raw/        ZIPs originais do TCE-RS (não versionados)
dados/auditoria/  Excel auditável por ano (evidência primária)
dados/processed/  Parquet consolidado (não versionado)
etl/          scripts de coleta e processamento (01_coleta.py, 02_processa.py)
notebooks/    análises (00 exploratório, 31 institucional, 32 funcional, 33 credores)
output/       tabelas e gráficos prontos para o trabalho
```

## Como o projeto é executado

O pipeline segue **baby steps** e uma sequência obrigatória (coleta → processamento →
exploração → análises). O passo a passo completo, com critérios de pronto, está em
**[`TAREFAS.md`](TAREFAS.md)**.

## Princípios inegociáveis

Nenhum dado é inventado ou estimado sem fonte; todo o ETL é documentado e reproduzível.
Detalhes em [`docs/02_PRINCIPIOS.md`](docs/02_PRINCIPIOS.md).

---

Fonte dos dados: **TCE-RS/SIAPC**. Elaboração própria.
