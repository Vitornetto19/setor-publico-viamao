# Contexto do Projeto — Diagnóstico Orçamentário de Viamão/RS

## 1. O que é este projeto

Trabalho acadêmico da disciplina de **Finanças do Setor Público**, desenvolvido em dupla/trio, com análise detalhada das finanças do município de **Viamão/RS** para o período de **2019 a 2025**.

O trabalho é dividido entre três integrantes. Este repositório cobre **exclusivamente a parte do Vitor**, que responde pelas seções:

- **3.1** — Despesa por Classificação Institucional
- **3.2** — Despesa por Classificação Funcional
- **3.3** — Identificação dos Maiores Credores (2024)

---

## 2. Município Analisado — Viamão/RS

| Atributo | Dado |
|---|---|
| Município | Viamão |
| Estado | Rio Grande do Sul |
| Região | Região Metropolitana de Porto Alegre (RMPA) |
| População estimada (2024) | ~232.000 habitantes |
| PIB (2024) | ~R$ 5,5 bilhões |
| PIB per capita | ~R$ 24.700 (bem abaixo da média estadual de R$ 50.700) |
| Composição do PIB | Serviços 44% · Adm. Pública 28,9% · Indústria 15,5% · Agropecuária 2,8% |
| Vínculos formais / população | 8,7% (vs 25,9% no RS) — baixíssima formalidade |

**Característica central para a análise:** a Administração Pública responde por quase 30% do PIB local, o que torna o diagnóstico da despesa pública especialmente relevante para entender a economia do município.

---

## 3. Fonte dos Dados

### Fonte principal — TCE-RS / SIAPC
- **Portal:** https://dados.tce.rs.gov.br/group/despesa
- **Dataset por ano:** `despesa-orcamentaria-por-empenhos-pm-de-viamao-{ANO}`
- **Formato:** arquivos ZIP/CSV, um por ano, por município
- **API:** CKAN — `https://dados.tce.rs.gov.br/api/3/action/package_show?id={dataset_id}`
- **Período disponível:** 2019 a 2024 (2025 parcial)
- **Responsabilidade dos dados:** Prefeitura Municipal de Viamão. Os dados são enviados pelo município ao TCE-RS via sistema SIAPC e não foram auditados pelo Tribunal.

### Fontes complementares
| Dado necessário | Fonte |
|---|---|
| Indicadores sociais (IDH, mortalidade infantil, analfabetismo) | Atlas do Desenvolvimento Humano — atlasbrasil.org.br |
| Mortalidade infantil atualizada | Datasus — datasus.saude.gov.br |
| População anual | IBGE — cidades.ibge.gov.br |
| IPCA anual (deflator) | IBGE |
| IDESE (índice gaúcho) | DEE/RS — dee.rs.gov.br |

---

## 4. O que a Professora Pede — Visão Geral

O trabalho segue o modelo de análise financeira pública aplicada. Com base no **trabalho-modelo de Charqueadas/2022**, o padrão esperado é:

### Estrutura esperada do texto (seções 3.x)
1. **Tabela de dados** — valores nominais e reais (deflacionados pelo IPCA), com anos nas colunas
2. **Gráfico** — de barras ou linhas, bem rotulado, com fonte citada
3. **Análise escrita** — paragrafada, respondendo cada pergunta da professora com base nos dados, cruzando com contexto econômico, social e legislativo

### Padrão visual observado no trabalho-modelo (Charqueadas/2022)
- Tabelas com colunas por ano (2015 a 2021), valores em R$ milhões ou R$ mil, com linha de total e variação percentual
- Gráficos de barras agrupadas ou empilhadas, com legenda, título, fonte e eixos rotulados
- Cada seção tem entre 1 e 3 páginas: tabela + gráfico + texto de análise
- Texto usa linguagem técnica mas acessível, sempre justificando os movimentos com base em dados ou legislação

### Exemplos do trabalho-modelo relevantes para as seções 3.x

**Seção 3.1 — Institucional:**
- Tabela por secretaria/órgão com valor liquidado por ano + participação % no total
- Gráfico de barras mostrando evolução da participação de cada órgão
- Texto identificando qual secretaria domina e se houve inversão de posições

**Seção 3.2 — Funcional:**
- Tabela por função (Saúde, Educação, Administração, etc.) com valores anuais e variação real
- Linha separada para funções-meio vs. funções-fim
- Gráfico de área ou barras empilhadas mostrando composição por função ao longo dos anos
- Análise cruzando gasto per capita em saúde/educação com IDH e mortalidade infantil

**Seção 3.3 — Credores:**
- Tabela com ranking dos maiores credores de 2024: nome, CNPJ, valor pago, % do total
- Verificação de recorrência: os mesmos fornecedores aparecem em anos anteriores?
- Análise econômica: o que a concentração de fornecedores indica?

---

## 5. Estrutura de Pastas do Projeto

```
viamao-despesa/
│
├── docs/                          ← documentos de requisitos (este arquivo e os demais)
│   ├── 01_CONTEXTO_PROJETO.md
│   ├── 02_PRINCIPIOS.md
│   └── 03_REQUISITOS_TRABALHO.md
│
├── dados/
│   ├── raw/                       ← ZIPs originais baixados do TCE-RS (não modificar)
│   │   └── viamao_despesa_{ANO}.zip
│   │
│   ├── auditoria/                 ← Excel limpo por ano para conferência manual
│   │   └── viamao_despesa_{ANO}_auditoria.xlsx
│   │
│   └── processed/                 ← Parquet consolidado para uso nos notebooks
│       └── viamao_despesa_consolidado.parquet
│
├── etl/                           ← scripts de extração, transformação e carga
│   ├── 01_coleta.py               ← baixa ZIPs via CKAN API do TCE-RS
│   ├── 02_processa.py             ← extrai, normaliza, gera auditoria e parquet
│   └── README_ETL.md              ← documentação do pipeline ETL
│
├── notebooks/                     ← análises exploratórias e geração de outputs
│   ├── 00_exploratorio.ipynb      ← visão geral dos dados, sanity checks
│   ├── 31_institucional.ipynb     ← análise da seção 3.1
│   ├── 32_funcional.ipynb         ← análise da seção 3.2
│   └── 33_credores.ipynb          ← análise da seção 3.3
│
└── output/                        ← tabelas e gráficos prontos para o trabalho
    ├── tabelas/
    │   ├── 3_1_despesa_por_orgao.xlsx
    │   ├── 3_2_despesa_por_funcao.xlsx
    │   └── 3_3_maiores_credores_2024.xlsx
    └── graficos/
        ├── 3_1_evolucao_por_orgao.png
        ├── 3_2_evolucao_por_funcao.png
        ├── 3_2_saude_educacao_per_capita.png
        └── 3_3_concentracao_credores.png
```

---

## 6. Período de Análise

- **Mínimo exigido:** 2019 a 2025 (7 anos)
- **Disponível no TCE-RS:** 2019 a 2024 completos; 2025 parcial
- **Decisão:** usar 2019–2024 nos dados do TCE-RS; complementar 2025 com RREO do portal da prefeitura se disponível

---

## 7. Referências e Links

- Portal da Transparência de Viamão: https://www.viamao.rs.gov.br/portal/transparencia
- TCE-RS Dados Abertos: https://dados.tce.rs.gov.br/group/despesa
- Siconfi/STN: https://siconfi.tesouro.gov.br
- Atlas do Desenvolvimento Humano: http://www.atlasbrasil.org.br
- Portaria nº 42/1999 (classificação funcional): referência legal para seção 3.2
- LC nº 173/2020 (Covid-19): relevante para contextualizar 2020/2021
