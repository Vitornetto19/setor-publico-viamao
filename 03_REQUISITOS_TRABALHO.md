# Requisitos do Trabalho — Seções 3.1, 3.2 e 3.3

Este documento descreve **o que precisa ser entregue** em cada seção, com as perguntas exatas da professora, o que os dados devem mostrar, e o padrão de entrega esperado com base no trabalho-modelo (Charqueadas/2022).

---

## Seção 3.1 — Despesa por Classificação Institucional

### Enunciado da professora
> Demonstrar o comportamento da despesa liquidada, no mínimo, nos últimos 7 anos (2019 a 2025), segundo a **classificação institucional**, utilizando dados reais.

### Perguntas que devem ser respondidas

**3.1.a** — Qual órgão, secretaria ou ministério absorve a maior parcela do orçamento? Qual é a participação relativa de cada órgão no orçamento total? Justifique.

**3.1.b** — Como se comportou a participação de cada órgão ao longo do período analisado? Houve alguma inversão na absorção do orçamento público entre os órgãos nesse período? Justifique.

### O que entregar

#### Tabela 3.1.A — Despesa Liquidada por Órgão (R$ nominais)

| Órgão/Secretaria | 2019 | 2020 | 2021 | 2022 | 2023 | 2024 | Var. % (19→24) |
|---|---|---|---|---|---|---|---|
| Secretaria de Saúde | ... | | | | | | |
| Secretaria de Educação | ... | | | | | | |
| ... | | | | | | | |
| **Total** | | | | | | | |

- Valores em R$ mil ou R$ milhões (manter consistência)
- Ordenado pelo valor de 2024 (maior para menor)
- Última linha: total geral

#### Tabela 3.1.B — Participação Relativa por Órgão (%)

| Órgão/Secretaria | 2019 | 2020 | 2021 | 2022 | 2023 | 2024 |
|---|---|---|---|---|---|---|
| Secretaria de Saúde | % | | | | | |
| ... | | | | | | |
| **Total** | 100% | 100% | 100% | 100% | 100% | 100% |

#### Gráfico 3.1 — Evolução da Participação por Órgão

- Tipo: barras empilhadas (100%) ou barras agrupadas
- Eixo X: anos (2019–2024)
- Eixo Y: participação % ou valor absoluto
- Legenda com nome de cada órgão
- Título, fonte (TCE-RS/SIAPC), eixos rotulados

#### Texto de análise

Deve responder:
1. Qual secretaria domina o orçamento e por quê (característica do município)
2. Houve inversão de posições? Em que ano? O que explica?
3. Qual é o contexto econômico que justifica os movimentos (pandemia 2020, enchentes RS 2024, etc.)

### Notas técnicas

- **Variável:** `despesa liquidada` — usar coluna `vl_Liquidacao` (não `vl_Pagamento` e não `vl_Empenho`)
- **Filtro de operação:** tipo = "Liquidação"
- **Agrupamento:** por `nm_OrgaoOrcamentario` (não `nm_UnidadeOrcamentaria`)
- **Valor real:** deflacionar pelo IPCA acumulado (base 2024)

---

## Seção 3.2 — Despesa por Classificação Funcional

### Enunciado da professora
> Demonstrar o comportamento da despesa liquidada, no mínimo, nos últimos 7 anos (2019 a 2025), segundo a **classificação funcional da despesa**, conforme a **Portaria nº 42/1999** do Ministério do Planejamento, utilizando dados reais.

### Perguntas que devem ser respondidas

**3.2.a** — Qual função apresentou o maior crescimento da despesa no período? Justifique.

**3.2.b** — Como se comportaram os gastos nas funções **saúde** e **educação**?
- Em quantos por cento cresceram (nominal e real)?
- Qual foi o gasto per capita em cada ano?
- Cruzar com: taxa de analfabetismo, mortalidade infantil e IDH de Viamão

**3.2.c** — Qual foi o comportamento dos gastos nas funções consideradas **meio** e nas funções consideradas **fim** do Estado? Analise e justifique.

### O que entregar

#### Tabela 3.2.A — Despesa Liquidada por Função (R$ nominais e reais)

| Função | 2019 | 2020 | 2021 | 2022 | 2023 | 2024 | Var. % Nominal | Var. % Real |
|---|---|---|---|---|---|---|---|---|
| Saúde | | | | | | | | |
| Educação | | | | | | | | |
| Administração | | | | | | | | |
| Assistência Social | | | | | | | | |
| Previdência Social | | | | | | | | |
| Urbanismo | | | | | | | | |
| ... | | | | | | | | |
| **Total** | | | | | | | | |

#### Tabela 3.2.B — Gasto Per Capita: Saúde e Educação

| Ano | Pop. Viamão | Gasto Saúde (R$) | Per Capita Saúde | Gasto Educação (R$) | Per Capita Educação |
|---|---|---|---|---|---|
| 2019 | | | | | |
| ... | | | | | |
| 2024 | | | | | |

#### Tabela 3.2.C — Funções-Meio vs. Funções-Fim

Classificação conforme definição econômica:

**Funções-Meio** (suporte à máquina pública):
- Legislativa
- Administração
- Previdência Social
- Encargos Especiais
- Judiciária / Essencial à Justiça

**Funções-Fim** (entrega direta de serviços à população):
- Saúde
- Educação
- Assistência Social
- Habitação
- Saneamento
- Transporte
- Urbanismo
- Segurança Pública
- Cultura / Esporte / Lazer

| Tipo | 2019 | 2020 | 2021 | 2022 | 2023 | 2024 | Part. % 2019 | Part. % 2024 |
|---|---|---|---|---|---|---|---|---|
| Funções-Meio | | | | | | | | |
| Funções-Fim | | | | | | | | |
| **Total** | | | | | | | | |

#### Tabela 3.2.D — Indicadores Sociais de Viamão (dados externos)

| Indicador | Ano ref. | Viamão | RS | Brasil | Fonte |
|---|---|---|---|---|---|
| IDH | 2010 | | | | Atlas Brasil/PNUD |
| Taxa de analfabetismo (%) | mais recente | | | | IBGE/Censo |
| Mortalidade infantil (por mil NV) | mais recente | | | | Datasus |
| IDESE | mais recente | | | | DEE/RS |

#### Gráfico 3.2.A — Evolução das Principais Funções

- Tipo: linhas ou barras agrupadas
- Funções a exibir: Saúde, Educação, Administração, Assistência Social (as 4 maiores)
- Eixo Y: R$ (nominais ou reais — indicar)
- Incluir nota sobre deflator se usar valores reais

#### Gráfico 3.2.B — Gasto Per Capita Saúde + Educação (2019–2024)

- Tipo: barras duplas (uma barra Saúde, uma barra Educação) por ano
- Eixo Y: R$/habitante

#### Gráfico 3.2.C — Funções-Meio vs. Funções-Fim (participação %)

- Tipo: barras empilhadas 100%
- Deve mostrar a tendência de priorização do gasto ao longo do tempo

#### Texto de análise

Deve responder:
1. Qual função cresceu mais e por quê
2. Crescimento nominal e real de saúde e educação, com gasto per capita
3. Cruzamento com os indicadores sociais: o crescimento do gasto melhorou os indicadores?
4. Análise funções-meio vs. funções-fim: o município está priorizando a entrega de serviços ou a máquina administrativa?
5. Contextualizar com: pandemia (2020/2021), enchentes no RS (2024 — pode ter impactado urbanismo/habitação)

### Notas técnicas

- **Variável:** `despesa liquidada` — coluna `vl_Liquidacao`
- **Filtro:** tipo de operação = "Liquidação"
- **Agrupamento:** por `nm_Funcao` (código `cd_Funcao`)
- **Referência normativa:** Portaria nº 42/1999 do MP — define as funções e subfunções
- **Deflator IPCA:** aplicar para calcular variação real; documentar índices usados
- **Dados de população:** buscar no IBGE para cada ano do período
- **Indicadores sociais:** coletar manualmente no Atlas Brasil e Datasus; inserir na Tabela 3.2.D

---

## Seção 3.3 — Identificação dos Maiores Credores

### Enunciado da professora
> Identificar, na classificação da despesa do ente estudado, quais foram os **maiores credores no ano de 2024**. Apresentar, na forma de tabela, o nome dos principais credores contratados pelo ente público.
>
> Considerando a disponibilidade da relação de todos os credores dos últimos anos, é possível identificar se o Poder Público vem contratando repetidamente a mesma empresa ou grupo para prestar determinado serviço? Em caso afirmativo, o que isso indica? Reflita sobre essa questão à luz da pesquisa e da ciência econômica.

### Perguntas que devem ser respondidas

**3.3.a** — Quem são os maiores credores do município em 2024? Qual é a participação de cada um no total pago?

**3.3.b** — Há concentração de pagamentos em poucos fornecedores? O que isso indica?

**3.3.c** — O Poder Público contrata repetidamente as mesmas empresas? O que isso indica à luz da ciência econômica? (concorrência, captura do Estado, eficiência alocativa, barreiras à entrada)

### O que entregar

#### Tabela 3.3.A — Maiores Credores de Viamão em 2024

| Ranking | Nome do Credor | CNPJ | Valor Pago (R$) | % do Total | % Acumulado |
|---|---|---|---|---|---|
| 1 | | | | | |
| 2 | | | | | |
| ... | | | | | |
| 20 | | | | | |
| **Total geral pago** | | | | 100% | |

- Ordenado por valor pago decrescente
- Incluir % acumulado para mostrar concentração (tipo curva de Lorenz)
- Incluir separação visual entre credores pessoa jurídica e pessoa física

#### Tabela 3.3.B — Credores Recorrentes (2022–2024)

| Nome do Credor | CNPJ | Valor 2022 | Valor 2023 | Valor 2024 | Nº de anos |
|---|---|---|---|---|---|
| | | | | | |

- Filtrar apenas credores que aparecem nos 3 anos
- Ordenar por valor total acumulado

#### Gráfico 3.3 — Concentração dos Top 10 Credores (2024)

- Tipo: barras horizontais ou pizza (top 10 + "demais")
- Mostrar claramente o % do total que cada um representa

#### Texto de análise

Deve responder:
1. Quem são os maiores credores e a que setor pertencem (saúde, limpeza, construção, etc.)
2. Há concentração? Medir: os 5 maiores representam X% do total pago
3. Há recorrência? Nomear as empresas que aparecem repetidamente
4. Análise econômica: o que a recorrência indica?
   - Pode refletir eficiência (empresa consolidada, boa relação custo-benefício)
   - Pode indicar captura do Estado (rent-seeking), barreiras à entrada no mercado local
   - Pode indicar falta de concorrência nos processos licitatórios
   - Recomenda-se citar ao menos um conceito de economia pública ou organização industrial

### Notas técnicas

- **Variável:** `despesa paga` — coluna `vl_Pagamento`
- **Filtro:** tipo de operação = "Pagamento"
- **Agrupamento:** por `nm_Credor` + `cpf_cnpj_Credor`
- **Ano-base:** 2024 para o ranking principal
- **Recorrência:** cruzar com 2022 e 2023 (mínimo)
- **Atenção:** separar Prefeitura Municipal (órgão próprio) de fornecedores externos — empenhos internos podem aparecer na lista de credores e devem ser tratados

---

## Padrão de Entrega

### Cada seção deve ter:
1. **1 a 3 tabelas** geradas pelo notebook, exportadas para `output/tabelas/`
2. **1 a 2 gráficos** gerados pelo notebook, exportados para `output/graficos/`
3. **Texto analítico** a ser redigido com base nos outputs (não faz parte do código)

### Formatação das tabelas no trabalho final
- Fonte: Times New Roman 11 ou Arial 10
- Valores monetários: R$ com separador de milhar (ponto) e sem centavos, ex.: R$ 45.823.000
- Percentuais: com 1 ou 2 casas decimais, ex.: 23,4%
- Variação: sinal explícito (+12,3% ou −4,1%)
- Citar sempre: "Fonte: TCE-RS/SIAPC. Elaboração própria."

### Formatação dos gráficos no trabalho final
- Resolução mínima: 300 DPI para impressão
- Incluir sempre: título, subtítulo com período, legenda, fonte, eixos com unidade
- Paleta de cores: preferencialmente escala de azuis ou cores institucionais da UFRGS
- Exportar como `.png` em `output/graficos/`

---

## Checklist Final

Antes de considerar a seção concluída, verificar:

- [ ] Os dados vieram do TCE-RS (não foram digitados manualmente)
- [ ] O Excel de auditoria por ano existe em `dados/auditoria/`
- [ ] O notebook roda do início ao fim sem erro
- [ ] Todas as tabelas estão exportadas em `output/tabelas/`
- [ ] Todos os gráficos estão exportados em `output/graficos/`
- [ ] Cada tabela e gráfico tem citação de fonte
- [ ] Os valores nominais e reais estão claramente distinguidos
- [ ] O deflator IPCA está documentado no notebook
- [ ] As perguntas da professora estão todas respondidas nos textos
