# Dados externos (com fonte registrada — P1)

Dados **não** originários do TCE-RS, coletados manualmente de fontes oficiais e
usados nas análises (deflação, per capita, indicadores sociais). Ao contrário de
`dados/raw`, `dados/processed` e `dados/auditoria` (regeneráveis pelo ETL e
gitignorados), estes arquivos são **curados à mão** e **versionados** — reproduzi-los
exige voltar à fonte. Cada arquivo tem sua proveniência documentada aqui.

---

## `ipca_anual_ibge.csv` — IPCA, variação acumulada no ano

Índice de deflação usado para converter valores nominais em reais (base 2024) nas
seções 3.1 e 3.2.

| Coluna | Significado |
|---|---|
| `ano` | Ano de referência |
| `ipca_acumulado_ano_pct` | IPCA acumulado no ano (variação % dez/dez) |

**Fonte:** IBGE — Sistema IBGE de Recuperação Automática (SIDRA).
Tabela **1737** (IPCA), variável **69** — *IPCA · Variação acumulada no ano*,
valor de **dezembro** de cada ano (acumulado dos 12 meses).

**URLs da API (verificação):**
- 2020–2024: `https://apisidra.ibge.gov.br/values/t/1737/n1/all/v/69/p/last%2072/d/v69%202`
- 2019: `https://apisidra.ibge.gov.br/values/t/1737/n1/all/v/69/p/201912/d/v69%202`

**Valores (conferidos na fonte em 2026-07-02):**

| Ano | IPCA acum. no ano (%) |
|---|---|
| 2019 | 4,31 |
| 2020 | 4,52 |
| 2021 | 10,06 |
| 2022 | 5,79 |
| 2023 | 4,62 |
| 2024 | 4,83 |

**Uso (deflator base dez/2024):** para trazer um valor nominal do ano *Y* a preços
de 2024, multiplica-se pelo fator acumulado da inflação posterior a *Y*:

```
fator_real(Y) = Π_{k=Y+1}^{2024} (1 + IPCA_k / 100)      # fator_real(2024) = 1
valor_real_2024 = valor_nominal_Y × fator_real(Y)
```

O cálculo é feito e documentado no notebook `notebooks/31_institucional.ipynb`.

---

## `populacao_viamao_ibge.csv` — População residente de Viamão por ano

Denominador do gasto **per capita** de Saúde e Educação (Seção 3.2).

| Coluna | Significado |
|---|---|
| `ano` | Ano de referência |
| `populacao` | População residente estimada/contada |
| `tipo_fonte` | Metodologia da cifra naquele ano (ver ressalva abaixo) |

**Fonte:** IBGE — Estimativas da População (tabela SIDRA **6579**, variável 9324) e
**Censo Demográfico 2022** (tabela SIDRA **4714**, variável 93). Código do município = **4323002**.

**Valores (conferidos na fonte em 2026-07-02):**

| Ano | População | Origem |
|---|---|---|
| 2019 | 255.224 | Estimativa IBGE (projeção base Censo 2010) |
| 2020 | 256.302 | Estimativa IBGE (projeção base Censo 2010) |
| 2021 | 257.330 | Estimativa IBGE (projeção base Censo 2010) |
| 2022 | 224.112 | **Censo 2022 (contagem)** |
| 2023 | 228.078 | Interpolação geométrica (ver nota) |
| 2024 | 232.113 | Estimativa IBGE (base Censo 2022) |

> **⚠ Ressalva metodológica (quebra de série em 2022) — P1.**
> As estimativas de 2019–2021 usavam a **projeção do Censo 2010** e estavam
> **superestimadas**: o Censo 2022 recontou a população em **224.112**, uma revisão
> de **−12,9%** frente à estimativa de 2021 (257.330). Essa queda é **correção de
> medição, não perda populacional real**. Consequência: o gasto per capita a partir
> de 2022 é calculado sobre uma base menor (corrigida pelo censo), então **parte de
> qualquer salto no per capita em 2022 reflete a revisão do denominador**, não uma
> mudança de gasto. A análise trata os biênios pré e pós-censo com essa cautela.
>
> **2023:** o IBGE **não publicou** estimativa municipal para 2023 (ano seguinte ao
> censo). O valor 228.078 é **interpolação geométrica própria** entre o Censo 2022
> (224.112) e a Estimativa 2024 (232.113): `224112 × (232113/224112)^(1/2)`.
> Marcado como `interpolacao_*` na coluna `tipo_fonte` — é a única cifra da série
> **não observada diretamente na fonte**, e está rotulada como tal.

---

## `indicadores_sociais_viamao.csv` — Indicadores sociais de Viamão

Dados de contexto para a Tabela 3.2.D e para o cruzamento social da Seção 3.2.b
(o gasto crescente em saúde/educação melhorou os indicadores?). São indicadores
**pontuais** (não uma série anual), cada um no ano de referência disponível.

| Coluna | Significado |
|---|---|
| `indicador` | Nome do indicador |
| `ano_ref` | Ano de referência do dado |
| `viamao` / `rs` / `brasil` | Valor para o município, o estado e o país (vazio = não coletado) |
| `unidade` | Unidade de medida |
| `fonte` | Origem oficial |

**Proveniência por indicador (conferido em 2026-07-02):**

- **IDHM (2010) = 0,717** (Viamão, "alto"); RS 0,746; Brasil 0,727. Fonte: **Atlas do
  Desenvolvimento Humano no Brasil** (PNUD/IPEA/Fundação João Pinheiro, Atlas 2013,
  base Censo 2010). É o IDHM municipal mais recente disponível (não há edição pós-2010).
  Viamão: 247º no RS, 1.398º no Brasil.
- **Taxa de analfabetismo 15+ (2022):** Viamão **2,90%**, RS 3,11%, Brasil 7,00%.
  Derivada da taxa de alfabetização do **Censo 2022** (IBGE, SIDRA tabela **9543**):
  analfabetismo = 100 − alfabetização (Viamão 97,10%; RS 96,89%; Brasil 93,00%).
- **Mortalidade infantil = 13,44 por mil nascidos vivos.** Fonte: **IBGE Cidades**
  (indicador municipal). Cifra pontual disponível no portal; para série anual, a fonte
  primária seria o Datasus (SIM/Sinasc), de acesso via formulário. Usada só como contexto.
- **IDESE — bloco Educação (2021) = 0,558** (Viamão). Fonte: **DEE-RS / FEE**
  (Carta de Conjuntura). Um dos piores resultados entre municípios com mais de 100 mil
  habitantes da região de Porto Alegre. IDESE geral do RS em 2021 = 0,762 (referência).
