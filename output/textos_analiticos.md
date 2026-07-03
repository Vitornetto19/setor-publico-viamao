# Diagnóstico Orçamentário de Viamão/RS — Textos Analíticos

**Despesas municipais, 2019–2024** · Disciplina de Finanças do Setor Público (Economia — UFRGS)

Seções sob responsabilidade do Vitor: **3.1** (classificação institucional), **3.2** (classificação
funcional) e **3.3** (maiores credores de 2024). Os textos abaixo são a redação analítica final,
elaborada a partir das tabelas e gráficos gerados pelos notebooks (`notebooks/31_institucional.ipynb`,
`32_funcional.ipynb`, `33_credores.ipynb`) e exportados em [`output/tabelas/`](tabelas/) e
[`output/graficos/`](graficos/).

> **Fonte de todos os dados de despesa:** TCE-RS / SIAPC — Dados Abertos (dados de responsabilidade da
> Prefeitura de Viamão, enviados via SIAPC e **não auditados** pelo Tribunal). Elaboração própria.

---

## Nota metodológica

- **Recorte por operação.** Cada registro do TCE-RS é uma operação de **Empenho (E)**, **Liquidação (L)**
  ou **Pagamento (P)**. As seções 3.1 e 3.2 usam a **despesa liquidada** (`vl_liquidacao`, filtro `L`),
  medida do gasto efetivamente reconhecido no exercício; a seção 3.3 usa a **despesa paga**
  (`vl_pagamento`, filtro `P`), como pede o enunciado.
- **Harmonização por código (P1).** Os *nomes* de órgãos, funções e credores mudam de grafia entre os
  anos; os **códigos** (`cd_orgao_orcamentario`, `cd_funcao`, `cd_credor`) são estáveis. Agrupou-se sempre
  pelo código, rotulando com o nome do ano mais recente — nenhum valor é criado ou estimado.
- **Valores nominais e reais.** Onde se compara ao longo do tempo, os valores nominais são convertidos a
  **preços de dezembro/2024** pelo deflator **IPCA** (IBGE/SIDRA, tabela 1737, variável 69). A inflação
  acumulada de 2019 a 2024 (dez/dez) foi de **33,5%**. Toda variação "real" já desconta essa inflação.
- **População (per capita).** Denominador do gasto per capita (3.2) é a população residente do IBGE.
  Há **quebra de série censitária em 2022**: o Censo recontou **224.112** habitantes, **−12,9%** frente à
  estimativa de 2021 (257.330). É correção de medição, não perda populacional — parte do salto no per
  capita a partir de 2022 é artefato do denominador, e isso está sinalizado no texto.
- **Ausência ≠ zero (P1).** Célula vazia nas tabelas indica que o órgão/função/credor não teve o valor
  correspondente naquele ano (ausência real), nunca um zero inventado.

---

## 3.1 — Despesa por Classificação Institucional

*Variável: despesa liquidada. Tabelas 3.1.A (nominal), 3.1.B (participação %), 3.1.C (variação nominal e
real). Gráfico [`3_1_evolucao_por_orgao.png`](graficos/3_1_evolucao_por_orgao.png).*

### 3.1.a — Qual órgão absorve a maior parcela do orçamento e por quê

A despesa liquidada de Viamão é dominada, de forma estável, por **duas secretarias finalísticas**. Em
2024, a **Secretaria Municipal da Educação** respondeu por **41,5%** do total liquidado (R$ 306,6 milhões)
e a **Secretaria Municipal da Saúde** por **22,4%** (R$ 165,9 milhões) — juntas, cerca de **64%** de todo
o orçamento executado do município. Na sequência aparecem **Obras e Serviços** (9,2%) e as áreas-meio
**Administração** (6,0%) e **Fazenda** (6,7%).

Essa concentração é característica da estrutura fiscal municipal brasileira, e não uma peculiaridade de
Viamão. A Constituição impõe **pisos mínimos de aplicação** — 25% da receita de impostos em **educação**
(art. 212) e 15% em **saúde** (art. 198, EC 29/2000) — e é sobre o município que recaem a rede de ensino
**infantil e fundamental** e a **atenção básica de saúde**. O orçamento municipal é, por desenho
constitucional, um orçamento de educação e saúde.

### 3.1.b — Como a participação evoluiu e se houve inversão

No **topo do ranking não há inversão**: Educação (1º), Saúde (2º) e Obras e Serviços (3º) mantêm suas
posições em todos os seis anos (Tabela de ranking). As inversões relevantes ocorrem **logo abaixo** e são
economicamente informativas:

- **Obras e Serviços encolhe** de **15,5%** (2019) para **9,2%** (2024) da despesa — uma queda **real de
  −32,4%** no período, isto é, o órgão não apenas perdeu participação como gastou menos em termos reais.
- A **Secretaria da Fazenda salta** de **4,1%** para **6,7%** (crescimento **real de +83,6%**) e
  **ultrapassa a Administração** na disputa pelo 4º/5º lugar em 2024. A Administração, no sentido inverso,
  cai de 7,9% para 6,0% (**real −14,1%**).

No agregado, o município liquidou **+51,1% em termos nominais** de 2019 a 2024, o que equivale a **+13,2%
em termos reais** (descontada a inflação de 33,5%) — ou seja, houve crescimento real do gasto, porém
modesto, concentrado nas áreas finalísticas. O **contexto** ajuda a ler os movimentos: a **pandemia
(2020–2021)** pressionou Saúde e Assistência Social, e as **enchentes no RS (2024)** têm efeito potencial
sobre Obras/Urbanismo — embora, do lado da *liquidação* de 2024, esse efeito ainda apareça de forma
limitada (parte da resposta pode estar em empenhos de 2024/2025 ainda não liquidados).

---

## 3.2 — Despesa por Classificação Funcional (Portaria MP nº 42/1999)

*Variável: despesa liquidada, por função de governo. Tabelas 3.2.A (função, nominal e real), 3.2.B (per
capita Saúde/Educação), 3.2.C (meio vs. fim), 3.2.D (indicadores sociais). Gráficos
[`3_2_evolucao_funcoes.png`](graficos/3_2_evolucao_funcoes.png),
[`3_2_per_capita_saude_educacao.png`](graficos/3_2_per_capita_saude_educacao.png),
[`3_2_meio_vs_fim.png`](graficos/3_2_meio_vs_fim.png).*

> Observação estrutural: por ser um dataset do **Executivo municipal**, não há as funções **Legislativa
> (01)**, **Judiciária (02)** nem **Essencial à Justiça (03)** — a Câmara de Vereadores é ente separado.

### 3.2.a — Qual função apresentou o maior crescimento

Descontada a inflação, o município cresceu **+13,2% real** no total. Entre as funções de **peso material**,
a de maior crescimento real foi **Transporte**, que praticamente **dobrou**: de R$ 9,5 mi (2019) para
R$ 22,1 mi (2024) — **+133,9% nominal / +75,2% real**. Em seguida, **Encargos Especiais** (**+48,9% real**).
Entre as **três maiores** funções, a que mais cresceu em termos reais foi a **Administração** (**+25,2%
real**), acima de **Saúde** (+20,0%) e **Educação** (+17,2%).

*Ressalva de honestidade (P1):* algumas funções exibem variações de três ou quatro dígitos (Comércio e
Serviços, Trabalho, Cultura) apenas porque **partiram de base ínfima em 2019** (próxima de zero) —
crescimento matematicamente enorme, mas economicamente pouco informativo. A Tabela 3.2.A marca esses casos
como "base ínfima" para não induzir a leitura equivocada.

### 3.2.b — Comportamento de Saúde e Educação

- **Saúde:** R$ 103,6 mi → R$ 165,9 mi, **+60,1% nominal / +20,0% real**. Per capita real (base 2024):
  **R$ 542 → R$ 715 por habitante**.
- **Educação:** R$ 196,0 mi → R$ 306,6 mi, **+56,4% nominal / +17,2% real**. Per capita real:
  **R$ 1.025 → R$ 1.321 por habitante** — a Educação gasta cerca do **dobro** da Saúde por habitante,
  reflexo do peso da rede de ensino infantil e fundamental.

*Cuidado com o per capita (P1):* o per capita real cresce mais que o gasto agregado real (Saúde +32% vs.
+20%; Educação +29% vs. +17%) **porque a população "cai" de 257 mil (2021) para 224 mil (Censo 2022)**.
Esse recuo é revisão censitária, não perda real — parte do degrau de 2022 em diante é artefato do
denominador.

**Cruzamento com indicadores sociais (Tabela 3.2.D).** Apesar do gasto real crescente e de indicadores de
**acesso** favoráveis — **analfabetismo de 15 anos ou mais de apenas 2,90%** (melhor que RS 3,11% e Brasil
7,00%; Censo 2022) e **IDHM 0,717** ("alto", 2010) —, o **IDESE do bloco Educação de Viamão é baixo (0,558
em 2021)**, um dos piores entre os municípios de mais de 100 mil habitantes da região de Porto Alegre. A
leitura econômica: **mais gasto não se converteu automaticamente em melhor resultado/qualidade** — há uma
questão de **eficiência do gasto**, não apenas de volume. *(Cruzamento ilustrativo, não causal: os
indicadores são de anos distintos — IDHM 2010, IDESE 2021, analfabetismo 2022.)*

### 3.2.c — Funções-meio vs. funções-fim

Classificando as funções entre **meio** (sustentação da máquina pública — Administração, Previdência
Social, Encargos Especiais) e **fim** (entrega direta de serviço — Saúde, Educação, Assistência, Urbanismo,
Transporte etc.), as **funções-fim dominam e são estáveis**: **84,7% (2019) → 83,6% (2024)** da despesa
liquidada, oscilando entre ~81% e ~87%. As funções-meio ficam em **15,3% → 16,4%**, com picos em 2020
(18,3%) e 2023 (18,5%). **Não há inversão:** Viamão mantém forte prioridade na entrega de serviço direto,
coerente com o domínio de Saúde e Educação.

Dentro do grupo "meio" há recomposição: os **Encargos Especiais quase dobram em termos reais (+48,9%)**,
enquanto a **Previdência Social (função 09) desaparece da liquidação em 2024** (presente de 2019 a 2023,
~R$ 5–6 mi/ano) — ausência real a investigar (possível reclassificação do RPPS), não um zero.

---

## 3.3 — Identificação dos Maiores Credores (2024)

*Variável: despesa paga. Tabela 3.3.A (Top 20 de 2024, com % e % acumulado), Tabela 3.3.B (fornecedores
recorrentes 2022–2024), tabela de concentração. Gráfico
[`3_3_concentracao_credores.png`](graficos/3_3_concentracao_credores.png).*

> **Tratamento de credores internos (P1).** A lista de credores mistura **fornecedores de mercado**
> (contratados) com **pagamentos intragovernamentais** que não são contratação: folha de pessoal,
> previdências (IPREV própria, IPE-RS estadual, INSS federal), empresa pública própria (EPTV), tributos
> (Receita Federal, SEFAZ/RS), depósitos judiciais e serviço da dívida (BRDE). Doze `cd_credor` foram
> **classificados explicitamente por código** como intragovernamentais: permanecem na Tabela 3.3.A (que
> responde "maiores credores"), mas são **excluídos** das métricas de concentração e recorrência de
> *fornecedores*.

### 3.3.a — Quem são os maiores credores e de que setor

Um fato estrutural vem antes dos fornecedores: **mais da metade (53,4%) do que Viamão pagou em 2024 não é
contratação de mercado** — é **folha de pessoal** (R$ 294,1 mi, ~40% do total sozinha) somada a **encargos
e transferências obrigatórias** (previdências, tributos, depósitos judiciais, serviço da dívida). Os
**fornecedores de mercado** ficam com os outros **46,6%** (R$ 342,6 mi).

Entre os **fornecedores contratados**, o maior é o **Instituto Socio-Educacional da Biodiversidade**
(R$ 36,9 mi, 5,0% do total pago) — uma **OSC de saúde** que opera serviços terceirizados do SUS municipal —,
ao lado da **Organização da Sociedade Civil IN Saúde** (R$ 29,1 mi) e da **ADRA**. Vêm em seguida
**alimentação/benefícios** (Pluxee, ex-Sodexo, R$ 32,8 mi), **gestão de frota** (QFrotas), **obras e
pavimentação** (Construmetal, Melque, DCS-CL, Construtora LF), **resíduos e limpeza urbana** (CRVR,
Coleturb, Omega) e **transporte coletivo** (Empresa de Transporte Coletivo Viamão). Ou seja: os grandes
contratos concentram-se em **saúde terceirizada, alimentação escolar, limpeza urbana, obras e transporte**.

### 3.3.b — Há concentração de pagamentos?

Sim, forte no topo. **Sobre o total pago**, a folha sozinha é 40,0%; os **5 maiores credores somam 59,4%**,
os **10 maiores 67,1%** e o **Top 20 chega a 76,7%** (coluna "% acumulado" da Tabela 3.3.A — a curva tipo
Lorenz). Isolando **apenas os fornecedores de mercado** (R$ 342,6 mi, cerca de **2.355 credores distintos**),
a concentração permanece alta: o maior fornecedor pesa **10,8%**, os **5 maiores 36,2%**, os **10 maiores
48,6%** e os **20 maiores 62,4%** de tudo que se paga a fornecedores. Em síntese: **cerca de 20 fornecedores
ficam com quase dois terços** dos pagamentos a fornecedores, enquanto uma **cauda longa** de milhares de
pequenos credores divide o restante.

### 3.3.c — Há recorrência? Leitura à luz da ciência econômica

Sim, e é a regra, não a exceção: **404 fornecedores foram pagos nos três anos (2022, 2023 e 2024)** — apenas
**8,8%** dos que aparecem no triênio, mas concentrando **cerca de 67%** de tudo que se pagou a fornecedores
em 2024 (Tabela 3.3.B). Os grandes contratos de **saúde terceirizada (institutos/OSCs), limpeza urbana,
alimentação e transporte** reaparecem ano após ano.

**Interpretação econômica:**

- **Eficiência (custos de transição e economias de escala/aprendizado):** recontratar quem já opera um
  serviço continuado — um hospital, a coleta de lixo, a merenda — pode ser racional, porque trocar de
  operador tem custo e risco. Recorrência, por si só, **não** é sinônimo de irregularidade.
- **Barreiras à entrada e contestabilidade (Baumol):** recorrência elevada em mercados de **poucos
  participantes** liga o alerta. Se sempre concorrem os mesmos, o poder de mercado do incumbente cresce e o
  preço tende a se afastar do competitivo — um mercado pouco *contestável*.
- **Rent-seeking / captura do Estado (Stigler, Tullock):** no limite, concentração somada a recorrência é o
  ambiente típico em que fornecedores com relação estável investem em **influência** em vez de eficiência, e
  editais podem ser desenhados para restringir a concorrência.
- **Ressalva de honestidade (P1):** os dados de *pagamento* mostram **padrão** (concentração + recorrência),
  **não conduta**. Distinguir "incumbente eficiente" de "captura" exige examinar os **processos
  licitatórios** (modalidade, número de concorrentes, dispensas e inexigibilidades), o que está **fora do
  escopo** destes dados. O que os dados sustentam é que **o mercado de fornecedores de Viamão é concentrado
  e estável** — condição que *merece* escrutínio concorrencial.

**Observação de fronteira.** `vl_pagamento` ≠ despesa do exercício: pagamentos podem quitar empenhos de anos
anteriores (restos a pagar), de modo que o ranking de "pagos em 2024" não coincide com o de "liquidado em
2024" — mas é exatamente o que a pergunta pede (maiores credores **pagos**).

---

Fonte dos dados: **TCE-RS / SIAPC**. Elaboração própria.
