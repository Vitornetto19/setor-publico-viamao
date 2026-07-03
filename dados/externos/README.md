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
