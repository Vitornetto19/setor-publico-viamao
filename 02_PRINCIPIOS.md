# Princípios do Projeto — Regras Inegociáveis

Este documento define os princípios que **devem ser seguidos em toda e qualquer tarefa** executada neste projeto. Nenhuma instrução pontual pode sobrepor estes princípios.

---

## P1 — Nunca criar dados

**Nenhum valor numérico pode ser inventado, estimado ou imputado sem fonte explícita.**

- Se um dado não está disponível na fonte, registrar como `NaN` ou `null` — nunca preencher com zero, média ou interpolação silenciosa
- Toda transformação sobre os dados originais (deflação pelo IPCA, cálculo per capita, agregação) deve ser explicitamente documentada no código com comentário indicando a fórmula e a fonte dos parâmetros usados
- Proibido usar dados de memória do modelo (ex.: "o IDH de Viamão é X") sem checar a fonte e registrar a referência no notebook
- Se uma tabela do trabalho-modelo (Charqueadas) apresentar um número diferente do calculado via dados brutos, prevalece sempre o dado bruto — nunca ajustar para "bater" com o exemplo

**Exemplo correto:**
```python
# IPCA acumulado 2019→2024 = 41,8% — fonte: IBGE (IPCA anual: 4,31% / 4,52% / 10,06% / 5,79% / 4,62%)
# Calculado como produto: 1.0431 * 1.0452 * 1.1006 * 1.0579 * 1.0462 = 1.418
DEFLATOR_2019 = 1.418
```

---

## P2 — Dados brutos sempre acessíveis via Excel por ano

**Cada ano de dados deve ter um arquivo Excel auditável, gerado automaticamente pelo ETL.**

- O script `etl/02_processa.py` deve gerar `dados/auditoria/viamao_despesa_{ANO}_auditoria.xlsx` para cada ano processado
- Este Excel deve conter:
  - **Aba "Dados":** todos os registros do ano, sem filtro, com colunas padronizadas e os valores monetários em formato numérico correto
  - **Aba "Metadados":** fonte, URL do dataset, nome do arquivo ZIP original, data/hora da extração, total de registros, hash MD5 do arquivo original
- Os arquivos Excel de auditoria são a evidência primária do trabalho — devem poder ser abertos e conferidos manualmente contra qualquer coleta feita à mão no portal do TCE-RS
- Os arquivos ZIP originais devem ser preservados em `dados/raw/` sem modificação

---

## P3 — Documentar o ETL (Extração, Transformação e Carregamento)

**Todo o pipeline de dados deve ser transparente e reproduzível.**

O arquivo `etl/README_ETL.md` deve documentar, para cada etapa:

### Extração
- Qual URL foi acessada
- Qual API foi consultada (endpoint CKAN, parâmetros)
- Data da extração (registrada automaticamente nos metadados)
- Nome e hash do arquivo baixado

### Transformação
- Quais colunas foram renomeadas e por quê (variações de encoding no TCE-RS)
- Como os valores monetários foram convertidos (separador decimal, separador de milhar)
- Como foi calculado o deflator do IPCA (fórmula + fonte dos índices anuais)
- Quais registros foram descartados e por quê (ex.: duplicatas, operações que não são Pagamento)
- Quais joins foram feitos com dados externos (população IBGE, indicadores sociais)

### Carregamento
- Quais arquivos foram gerados
- Onde ficam e o que cada um contém

---

## P4 — Baby Steps

**Cada tarefa deve ser executada em passos pequenos, verificáveis e independentes.**

- Nunca fazer tudo em um único script monolítico
- Cada script/notebook deve ter **uma responsabilidade clara** (coleta, processamento, análise de uma seção)
- Ao final de cada etapa, imprimir um resumo no terminal: quantas linhas foram processadas, quais anos foram encontrados, quais arquivos foram gerados
- Antes de avançar para a análise, sempre verificar os dados intermediários com `df.head()`, `df.describe()` e contagens de valores nulos
- Se uma etapa falhar, deve falhar de forma clara (mensagem de erro descritiva), não silenciosa

**Sequência obrigatória:**
```
01_coleta.py  →  verificar dados/raw/
02_processa.py  →  verificar dados/auditoria/ e dados/processed/
00_exploratorio.ipynb  →  sanity check dos dados
31_institucional.ipynb  →  análise 3.1
32_funcional.ipynb  →  análise 3.2
33_credores.ipynb  →  análise 3.3
```

Nunca pular etapas. Se o parquet não existe, não rodar o notebook de análise.

---

## P5 — Clean Code

**O código deve ser legível por qualquer pessoa com conhecimento básico de Python.**

### Nomenclatura
- Variáveis e funções em `snake_case`, em português quando o contexto for de negócio (`valor_liquidado`, `nome_orgao`, `calcular_per_capita`)
- Constantes em `UPPER_SNAKE_CASE` com comentário explicando de onde vêm (`POPULACAO_2024 = 232_000  # IBGE estimativa`)
- Nomes de arquivos sempre com o padrão `{municipio}_{tipo}_{ano}_{sufixo}.{ext}`

### Estrutura dos scripts ETL
```python
# Sempre nesta ordem:
# 1. Imports
# 2. Constantes (com fonte nos comentários)
# 3. Funções (pequenas, com docstring)
# 4. Bloco main() com prints de progresso
# 5. if __name__ == "__main__": main()
```

### Estrutura dos notebooks
- Cada célula faz **uma coisa só**
- Primeira célula: imports e constantes
- Células de dados: sempre terminar com `.head()` ou resumo para inspeção visual
- Células de gráfico: sempre incluir `plt.title()`, `plt.xlabel()`, `plt.ylabel()`, `plt.tight_layout()` e salvar em `output/graficos/`
- Última célula de cada seção: exportar a tabela final para `output/tabelas/`

### Proibições
- Sem `print("debug")` esquecido
- Sem células de notebook em ordem errada (o notebook deve rodar do início ao fim sem erro)
- Sem `pd.read_csv(...)` com caminho absoluto da máquina do desenvolvedor — sempre usar `Path` relativo à raiz do projeto
- Sem `df.fillna(0)` sem comentário explicando por que zero é o valor correto naquele contexto

---

## P6 — Notebooks de Análise Exploratória e de Resultados

**A pasta `notebooks/` é o coração do projeto analítico.**

### `00_exploratorio.ipynb` — deve conter obrigatoriamente:
- Contagem de linhas por ano
- Tipos de operação disponíveis (Empenho, Liquidação, Pagamento) e quantidades
- Lista de funções únicas encontradas nos dados
- Lista de órgãos únicos
- Top 10 credores brutos (antes de qualquer filtro)
- Verificação de nulos nas colunas críticas
- Totais de liquidação e pagamento por ano (para conferência com os Excels de auditoria)

### `31_institucional.ipynb` — deve gerar:
- Tabela: despesa liquidada por órgão × ano (valores nominais em R$)
- Tabela: participação relativa de cada órgão por ano (%)
- Tabela: variação nominal e real 2019→2024 por órgão
- Gráfico: barras empilhadas com evolução da participação por órgão
- Exportar: `output/tabelas/3_1_despesa_por_orgao.xlsx`
- Exportar: `output/graficos/3_1_evolucao_por_orgao.png`

### `32_funcional.ipynb` — deve gerar:
- Tabela: despesa liquidada por função × ano (nominal e real)
- Tabela: gasto per capita em Saúde e Educação por ano
- Tabela: funções-meio vs. funções-fim (totais anuais e participação %)
- Gráfico: evolução das funções principais ao longo do período
- Gráfico: gasto per capita Saúde + Educação com linha de tendência
- Exportar: `output/tabelas/3_2_despesa_por_funcao.xlsx`
- Exportar: `output/graficos/3_2_evolucao_por_funcao.png`

### `33_credores.ipynb` — deve gerar:
- Tabela: Top 20 credores de 2024 (nome, CNPJ, valor pago, % do total, % acumulado)
- Tabela: credores recorrentes (aparecem em 3+ anos)
- Gráfico: concentração dos Top 10 credores (% do total pago)
- Exportar: `output/tabelas/3_3_maiores_credores_2024.xlsx`
- Exportar: `output/graficos/3_3_concentracao_credores.png`
