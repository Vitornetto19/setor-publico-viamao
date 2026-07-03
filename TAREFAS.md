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

## Fase 5 — Seção 3.1 · Institucional (`notebooks/31_institucional.ipynb`) ✅ (concluída)

Variável: `vl_liquidacao` · filtro tipo = **Liquidação** · agrupar por **órgão** (harmonizado por `cd_orgao_orcamentario`).

- [x] Tabela 3.1.A — despesa liquidada por órgão × ano (R$ nominais), ordenada por 2024 + Var.% nominal
- [x] Tabela 3.1.B — participação relativa (%) por órgão × ano (colunas somam 100%)
- [x] Tabela 3.1.C — variação nominal e **real** (deflator IPCA base dez/2024) 2019→2024 por órgão
- [x] Gráfico 3.1 — barras empilhadas 100% da participação (8 maiores + Demais; paleta colorblind-safe, 300 DPI)
- [x] Exportar `output/tabelas/3_1_despesa_por_orgao.xlsx` (5 abas) e `output/graficos/3_1_evolucao_por_orgao.png`
- [x] Texto de análise: 3.1.a (Educação+Saúde ≈63%) e 3.1.b (Obras 16%→9%; Fazenda ultrapassa Administração)

**Critério de pronto:** 2+ tabelas e 1 gráfico exportados; perguntas 3.1.a/b respondidas.
Notas: órgãos harmonizados por código (17 códigos vs 25 grafias); IPCA registrado em `dados/externos/`
(IBGE/SIDRA, fonte); inflação acum. 2019→2024 = 33,5%; total município +51,1% nominal / +13,2% real.
Executado com `nbconvert --execute` (0 erros); totais conferidos contra a auditoria.

---

## Fase 6 — Seção 3.2 · Funcional (`notebooks/32_funcional.ipynb`) ✅ (concluída)

Variável: `vl_liquidacao` · filtro **Liquidação** · agrupar por **função** (harmonizada por `cd_funcao`, Portaria 42/1999).

- [x] Coletar dados externos **com fonte registrada** (P1): população IBGE por ano, IPCA
      anual, IDH (Atlas Brasil), mortalidade infantil (IBGE Cidades), analfabetismo (IBGE Censo 2022), IDESE (DEE/RS)
- [x] Tabela 3.2.A — despesa por função × ano (nominal), variação % nominal e **real** (deflator IPCA)
- [x] Tabela 3.2.B — gasto per capita em Saúde e Educação por ano (nominal e real)
- [x] Tabela 3.2.C — funções-meio vs. funções-fim (totais e participação %)
- [x] Tabela 3.2.D — indicadores sociais de Viamão (dados externos)
- [x] Gráfico 3.2.A — evolução das principais funções (6 maiores, valores reais)
- [x] Gráfico 3.2.B — per capita Saúde + Educação (barras duplas por ano, reais)
- [x] Gráfico 3.2.C — meio vs. fim (barras empilhadas 100%)
- [x] Exportar `output/tabelas/3_2_despesa_por_funcao.xlsx` (6 abas) e os 3 PNGs em `output/graficos/`
- [x] Texto de análise: 3.2.a (maior crescimento), 3.2.b (saúde/educação + cruzamento social),
      3.2.c (meio vs. fim); contextualizar pandemia (2020/21) e enchentes RS (2024)

**Critério de pronto:** tabelas A–D + 3 gráficos exportados; perguntas 3.2.a/b/c respondidas;
deflator IPCA documentado.
Notas: funções harmonizadas por código (18 códigos vs 36 grafias — só caixa/acento); **sem função
Legislativa/Judiciária** (dataset é do Executivo). Achados: maior crescimento real entre funções
materiais = **Transporte** (+75,2%); Saúde +20,0% e Educação +17,2% reais; per capita real Saúde
R$542→715 e Educação R$1.025→1.321. **Funções-fim dominam e estáveis (84,7%→83,6%)**, sem inversão.
**Ressalva censitária (P1):** o Censo 2022 revisou a população −12,9% (quebra de série); parte do
salto no per capita em 2022+ é artefato do denominador — documentado. **Previdência Social some da
liquidação em 2024** (ausência real, não zero). Executado com `nbconvert` (0 erros).

---

## Fase 7 — Seção 3.3 · Credores (`notebooks/33_credores.ipynb`) ✅ (concluída)

Variável: `vl_pagamento` · filtro tipo = **Pagamento** · agrupar por `cd_credor` (chave estável; nome/CNPJ do registro).

- [x] Tratar credores internos (Prefeitura/órgão próprio) vs. fornecedores externos
- [x] Tabela 3.3.A — Top 20 credores de 2024 (nome, CNPJ, valor pago, % do total, % acumulado)
- [x] Tabela 3.3.B — credores recorrentes (aparecem em 2022, 2023 e 2024)
- [x] Gráfico 3.3 — concentração dos Top 10 (barras horizontais + "Demais"; paleta colorblind-safe, 300 DPI)
- [x] Exportar `output/tabelas/3_3_maiores_credores_2024.xlsx` (5 abas) e `output/graficos/3_3_concentracao_credores.png`
- [x] Texto de análise: 3.3.a (quem/qual setor), 3.3.b (concentração — os 5 maiores = X%),
      3.3.c (recorrência à luz da ciência econômica: concorrência, rent-seeking, barreiras à entrada)

**Critério de pronto:** tabelas A/B + gráfico exportados; perguntas 3.3.a/b/c respondidas.
Notas: agrupamento por `cd_credor` (0 nulos; nome harmonizado pelo ano mais recente). **Tratamento de internos (P1):**
12 `cd_credor` classificados explicitamente como **intragovernamentais** (folha, previdências IPREV/INSS/IPE-RS,
EPTV, tributos Receita/SEFAZ, depósitos judiciais, serviço da dívida no BRDE) — mantidos na 3.3.A, excluídos das
métricas de fornecedores. Achados: **folha = 40,0%** do pago; **intragov. = 53,4%**, **fornecedores de mercado = 46,6%**
(R$ 342,6 mi, 2.355 credores). Concentração entre fornecedores: 5 maiores **36,2%**, 20 maiores **62,4%**. Maior
fornecedor = **Instituto Socio-Educacional da Biodiversidade** (saúde terceirizada, R$ 36,9 mi). Recorrência: **404
fornecedores** pagos nos 3 anos (8,8%) concentram **~67%** do pago a fornecedores em 2024. Ressalvas: `vl_pagamento` ≠
liquidação (restos a pagar); os dados mostram **padrão** (concentração+recorrência), **não conduta** — rent-seeking
exigiria olhar os processos licitatórios. Executado com `nbconvert --execute` (0 erros).

---

## Fase 8 — Fechamento e entrega

- [ ] Rodar o **checklist final** do `docs/03_REQUISITOS_TRABALHO.md`
- [ ] Conferir que toda tabela/gráfico cita fonte ("TCE-RS/SIAPC. Elaboração própria.")
- [ ] Conferir distinção clara entre valores nominais e reais; deflator documentado
- [ ] Verificar que todos os notebooks rodam do início ao fim sem erro
- [ ] Commit e push de cada entregável em `output/`
- [ ] Redigir os textos analíticos finais (fora do código) com base nos outputs

**Critério de pronto:** todos os itens do checklist do `docs/03_REQUISITOS_TRABALHO.md` marcados.
