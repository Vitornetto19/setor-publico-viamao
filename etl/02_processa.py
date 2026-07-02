"""etl/02_processa.py — Fase 3 do pipeline (Transformação + Carga).

Lê os ZIPs coletados na Fase 2 (dados/raw/viamao_despesa_{ANO}.zip), extrai o
CSV interno do TCE-RS, normaliza as colunas de interesse, converte valores
monetários para numérico e gera:

    dados/auditoria/viamao_despesa_{ANO}_auditoria.xlsx   (abas Dados + Metadados)
    dados/processed/viamao_despesa_consolidado.parquet     (todos os anos)

Uso:
    python etl/02_processa.py

Decisões de ETL (todas fundamentadas por inspeção dos arquivos — ver
etl/README_ETL.md):
  - Encoding: utf-8-sig (arquivos vêm com BOM). Separador de campo: vírgula.
  - Separador decimal: ponto, sem separador de milhar (ex.: 2000000.00).
  - tipo_operacao assume exatamente {E, L, P} nos 6 anos (Empenho/Liquidação/Pagamento).
  - Valores negativos são estornos/anulações e são MANTIDOS: as somas são líquidas (P1).
  - Colunas de código e cnpj_cpf são lidas como texto para preservar zeros à esquerda.
  - Ausência de valor vira NaN/NA — nunca 0 sem justificativa (P1).

Fonte: TCE-RS / SIAPC. Dados de responsabilidade da Prefeitura de Viamão,
enviados via SIAPC e NÃO auditados pelo Tribunal.
"""

# 1. Imports
from __future__ import annotations

import csv
import sys
import zipfile
from datetime import datetime
from pathlib import Path

import pandas as pd

# 2. Constantes (com fonte nos comentários)
COD_MUNICIPIO_VIAMAO = "63000"  # código do município no TCE-RS
ANOS = range(2019, 2025)        # 2019 a 2024 (2025 é parcial — fora de escopo)

# Formato dos CSVs do TCE-RS, confirmado por inspeção dos 6 arquivos:
ENCODING_CSV = "utf-8-sig"  # arquivos trazem BOM (efbbbf)
SEP_CSV = ","               # separador de campo é vírgula (decimais usam ponto)

# tipo_operacao: nos 6 anos só ocorrem E/L/P (verificado). Mapa para rótulo legível.
MAPA_TIPO_OPERACAO = {"E": "Empenho", "L": "Liquidação", "P": "Pagamento"}

# Caminhos relativos à raiz do projeto (P5: nunca caminho absoluto do dev)
RAIZ_PROJETO = Path(__file__).resolve().parent.parent
DIR_RAW = RAIZ_PROJETO / "dados" / "raw"
DIR_AUDITORIA = RAIZ_PROJETO / "dados" / "auditoria"
DIR_PROCESSED = RAIZ_PROJETO / "dados" / "processed"
ARQ_MANIFEST = DIR_RAW / "manifest_coleta.csv"
ARQ_PARQUET = DIR_PROCESSED / "viamao_despesa_consolidado.parquet"

# Colunas curadas (subconjunto comum a todos os anos, relevante para 3.1/3.2/3.3).
# Todas confirmadas presentes nos 6 arquivos. Nomes originais do TCE-RS mantidos
# (já são snake_case claros) — normalização = seleção + tipagem, não renomeação.
COLUNAS_TEXTO = [
    "cd_orgao_orcamentario", "nome_orgao_orcamentario",
    "cd_unidade_orcamentaria", "nome_unidade_orcamentaria",
    "cd_funcao", "ds_funcao", "cd_subfuncao", "ds_subfuncao",
    "cd_elemento", "cd_rubrica", "ds_rubrica",
    "cd_credor", "nm_credor", "tp_pessoa", "cnpj_cpf",
    "nr_empenho", "nr_liquidacao", "nr_pagamento",
    "tipo_operacao", "historico",
]
COLUNAS_VALOR = ["vl_empenho", "vl_liquidacao", "vl_pagamento"]
COLUNAS_INTEIRAS = ["ano_recebimento", "mes_recebimento", "ano_empenho", "ano_operacao"]
COLUNAS_DATA = ["dt_empenho", "dt_operacao"]

# Ordem final das colunas no dataset normalizado.
COLUNAS_SAIDA = (
    ["ano"]
    + COLUNAS_INTEIRAS
    + ["tipo_operacao", "tipo_operacao_desc"]
    + ["cd_orgao_orcamentario", "nome_orgao_orcamentario",
       "cd_unidade_orcamentaria", "nome_unidade_orcamentaria"]
    + ["cd_funcao", "ds_funcao", "cd_subfuncao", "ds_subfuncao"]
    + ["cd_elemento", "cd_rubrica", "ds_rubrica"]
    + ["cd_credor", "nm_credor", "tp_pessoa", "cnpj_cpf"]
    + ["nr_empenho", "nr_liquidacao", "nr_pagamento"]
    + COLUNAS_VALOR
    + COLUNAS_DATA
    + ["historico"]
)


# 3. Funções
def ler_manifest() -> dict[int, dict]:
    """Lê o manifesto da coleta (Fase 2) e indexa a proveniência por ano.

    Levanta RuntimeError se o manifesto não existir — sem coleta, não há o que
    processar (falha clara — P4).
    """
    if not ARQ_MANIFEST.exists():
        raise RuntimeError(
            f"Manifesto não encontrado: {ARQ_MANIFEST}. Rode antes: python etl/01_coleta.py"
        )
    proveniencia: dict[int, dict] = {}
    with open(ARQ_MANIFEST, newline="", encoding="utf-8") as arq:
        for linha in csv.DictReader(arq):
            proveniencia[int(linha["ano"])] = linha
    return proveniencia


def ler_csv_do_zip(ano: int) -> pd.DataFrame:
    """Lê o CSV interno do ZIP do `ano` como texto puro (dtype=str, sem inferência).

    Ler tudo como string preserva zeros à esquerda de códigos e do cnpj_cpf, e
    mantém células vazias como '' (convertidas explicitamente depois). Usa o parser
    CSV do pandas (respeita aspas) — o campo `historico` é texto livre com vírgulas.
    """
    zp = DIR_RAW / f"viamao_despesa_{ano}.zip"
    if not zp.exists():
        raise RuntimeError(f"ZIP ausente: {zp}. Rode antes: python etl/01_coleta.py")
    with zipfile.ZipFile(zp) as z:
        nome_interno = z.namelist()[0]
        if not nome_interno.lower().endswith(".csv"):
            raise RuntimeError(f"{zp} não contém CSV (achou: {nome_interno})")
        with z.open(nome_interno) as f:
            df = pd.read_csv(
                f,
                sep=SEP_CSV,
                encoding=ENCODING_CSV,
                dtype=str,      # tudo como texto; tipagem é explícita em normalizar()
                na_filter=False,  # mantém '' literal em vez de virar NaN aqui
            )
    return df


def _para_numero(serie: pd.Series) -> pd.Series:
    """Converte série de texto monetário para float; '' vira NaN.

    errors='raise': se aparecer um valor não numérico inesperado, o script falha
    de forma clara (P4) em vez de silenciosamente virar NaN (P1). A inspeção
    confirmou 0 erros de parse nos 6 anos.
    """
    return pd.to_numeric(serie.replace("", pd.NA), errors="raise")


def _para_inteiro(serie: pd.Series) -> pd.Series:
    """Converte série de texto para inteiro nullable (Int64); '' vira NA."""
    return pd.to_numeric(serie.replace("", pd.NA), errors="raise").astype("Int64")


def _para_data(serie: pd.Series, ano: int, nome: str) -> pd.Series:
    """Converte 'YYYY-MM-DD' para datetime; '' vira NaT.

    Datas não vazias que não parsearem são reportadas (não silenciadas — P1/P4).
    """
    original_preenchido = (serie != "").sum()
    convertida = pd.to_datetime(serie.replace("", pd.NA), format="%Y-%m-%d", errors="coerce")
    perdidas = int(convertida.isna().sum() - (serie == "").sum())
    if perdidas > 0:
        print(f"    [AVISO {ano}] {perdidas} valores de '{nome}' não parsearam como data (viraram NaT).")
    return convertida


def normalizar(df: pd.DataFrame, ano: int) -> tuple[pd.DataFrame, dict]:
    """Seleciona colunas curadas, tipa valores/inteiros/datas e adiciona `ano` e rótulo.

    Devolve o DataFrame normalizado e um dicionário de estatísticas para o resumo.
    """
    # Confere que tipo_operacao só tem códigos conhecidos (P1: não inventar rótulo).
    tipos_encontrados = set(df["tipo_operacao"].unique())
    desconhecidos = tipos_encontrados - set(MAPA_TIPO_OPERACAO)
    if desconhecidos:
        raise RuntimeError(f"{ano}: tipo_operacao inesperado {desconhecidos} (fora de E/L/P).")

    out = pd.DataFrame(index=df.index)
    out["ano"] = ano  # ano do arquivo/exercício da coleta (chave temporal primária)

    for c in COLUNAS_INTEIRAS:
        out[c] = _para_inteiro(df[c])

    out["tipo_operacao"] = df["tipo_operacao"]
    out["tipo_operacao_desc"] = df["tipo_operacao"].map(MAPA_TIPO_OPERACAO)

    # Colunas de texto: '' vira NA (ausência real — P1), demais mantidas como estão.
    for c in COLUNAS_TEXTO:
        if c in ("tipo_operacao",):
            continue
        out[c] = df[c].replace("", pd.NA)

    for c in COLUNAS_VALOR:
        out[c] = _para_numero(df[c])

    for c in COLUNAS_DATA:
        out[c] = _para_data(df[c], ano, c)

    out = out[COLUNAS_SAIDA]

    # Estatísticas para o resumo e os metadados de auditoria.
    stats = {
        "ano": ano,
        "linhas": len(out),
        "por_tipo": df["tipo_operacao"].value_counts().to_dict(),
        "soma_liquidacao": float(out["vl_liquidacao"].sum()),
        "soma_pagamento": float(out["vl_pagamento"].sum()),
        "soma_empenho": float(out["vl_empenho"].sum()),
        "neg_liquidacao": int((out["vl_liquidacao"] < 0).sum()),
        "neg_pagamento": int((out["vl_pagamento"] < 0).sum()),
        "cnpj_ausente": int(out["cnpj_cpf"].isna().sum()),
        "duplicatas_exatas": int(out.duplicated().sum()),
        "anos_operacao": df["ano_operacao"].value_counts().to_dict(),
    }
    return out, stats


def gerar_auditoria_excel(df_ano: pd.DataFrame, ano: int, meta_coleta: dict, stats: dict) -> Path:
    """Gera o Excel de auditoria do `ano` com abas Dados e Metadados (P2)."""
    destino = DIR_AUDITORIA / f"viamao_despesa_{ano}_auditoria.xlsx"

    por_tipo = stats["por_tipo"]
    metadados = [
        ("Município", f"Viamão/RS (código TCE-RS {COD_MUNICIPIO_VIAMAO})"),
        ("Fonte", "TCE-RS / SIAPC — Dados Abertos (API CKAN)"),
        ("Responsabilidade", "Prefeitura de Viamão (dados não auditados pelo TCE)"),
        ("Dataset CKAN", f"despesa-orcamentaria-por-empenhos-pm-de-viamao-{ano}"),
        ("URL do recurso ZIP", meta_coleta.get("url", "")),
        ("Arquivo ZIP original", meta_coleta.get("arquivo", "")),
        ("Tamanho ZIP (bytes)", meta_coleta.get("tamanho_bytes", "")),
        ("MD5 do ZIP", meta_coleta.get("md5", "")),
        ("Coletado em", meta_coleta.get("coletado_em", "")),
        ("Encoding / separador", f"{ENCODING_CSV} / '{SEP_CSV}'"),
        ("Nº de registros", stats["linhas"]),
        ("Registros Empenho (E)", por_tipo.get("E", 0)),
        ("Registros Liquidação (L)", por_tipo.get("L", 0)),
        ("Registros Pagamento (P)", por_tipo.get("P", 0)),
        ("Soma vl_empenho (líquida, R$)", round(stats["soma_empenho"], 2)),
        ("Soma vl_liquidacao (líquida, R$)", round(stats["soma_liquidacao"], 2)),
        ("Soma vl_pagamento (líquida, R$)", round(stats["soma_pagamento"], 2)),
        ("Registros com valor negativo (estorno)",
         f"liq={stats['neg_liquidacao']}, pag={stats['neg_pagamento']}"),
        ("cnpj_cpf ausente (registros)", stats["cnpj_ausente"]),
        ("Duplicatas exatas (mantidas)", stats["duplicatas_exatas"]),
        ("Gerado por", "etl/02_processa.py"),
        ("Gerado em", datetime.now().isoformat(timespec="seconds")),
    ]
    df_meta = pd.DataFrame(metadados, columns=["campo", "valor"])

    with pd.ExcelWriter(destino, engine="openpyxl") as writer:
        df_ano.to_excel(writer, sheet_name="Dados", index=False)
        df_meta.to_excel(writer, sheet_name="Metadados", index=False)
    return destino


# 4. main() com prints de progresso (P4)
def main() -> None:
    DIR_AUDITORIA.mkdir(parents=True, exist_ok=True)
    DIR_PROCESSED.mkdir(parents=True, exist_ok=True)

    proveniencia = ler_manifest()

    print("Processamento — despesas de Viamão/RS")
    print(f"Anos: {ANOS.start} a {ANOS.stop - 1}")
    print(f"Auditoria: {DIR_AUDITORIA}")
    print(f"Consolidado: {ARQ_PARQUET}\n")

    partes: list[pd.DataFrame] = []
    resumo: list[dict] = []

    for ano in ANOS:
        print(f"[{ano}] lendo CSV do ZIP...", flush=True)
        bruto = ler_csv_do_zip(ano)
        print(f"[{ano}] {len(bruto)} linhas, {bruto.shape[1]} colunas brutas — normalizando...")
        df_ano, stats = normalizar(bruto, ano)

        meta_coleta = proveniencia.get(ano, {})
        if not meta_coleta:
            print(f"    [AVISO {ano}] sem entrada no manifesto — metadados de coleta ficarão vazios.")
        caminho_xlsx = gerar_auditoria_excel(df_ano, ano, meta_coleta, stats)
        print(f"[{ano}] auditoria -> {caminho_xlsx.name}  "
              f"(liq R$ {stats['soma_liquidacao']:,.2f} | pag R$ {stats['soma_pagamento']:,.2f})\n")

        partes.append(df_ano)
        resumo.append(stats)

    consolidado = pd.concat(partes, ignore_index=True)
    consolidado.to_parquet(ARQ_PARQUET, engine="pyarrow", index=False)

    # 5. Resumo (P4)
    print("=" * 78)
    print("RESUMO DO PROCESSAMENTO")
    print("=" * 78)
    print(f"{'ano':>5} {'linhas':>8} {'E':>7} {'L':>7} {'P':>7} "
          f"{'liquidação (R$)':>20} {'pagamento (R$)':>20}")
    for s in resumo:
        pt = s["por_tipo"]
        print(f"{s['ano']:>5} {s['linhas']:>8} {pt.get('E', 0):>7} {pt.get('L', 0):>7} "
              f"{pt.get('P', 0):>7} {s['soma_liquidacao']:>20,.2f} {s['soma_pagamento']:>20,.2f}")
    print("-" * 78)
    print(f"{'TOTAL':>5} {len(consolidado):>8} "
          f"{sum(s['por_tipo'].get('E', 0) for s in resumo):>7} "
          f"{sum(s['por_tipo'].get('L', 0) for s in resumo):>7} "
          f"{sum(s['por_tipo'].get('P', 0) for s in resumo):>7} "
          f"{sum(s['soma_liquidacao'] for s in resumo):>20,.2f} "
          f"{sum(s['soma_pagamento'] for s in resumo):>20,.2f}")

    # Ressalva temporal (P1): quanto de cada arquivo é de operações de anos anteriores.
    print("\nRessalva temporal — distribuição de ano_operacao dentro de cada arquivo:")
    for s in resumo:
        ano = s["ano"]
        do_ano = s["anos_operacao"].get(str(ano), s["anos_operacao"].get(ano, 0))
        total = s["linhas"]
        outros = total - do_ano
        print(f"  arquivo {ano}: {do_ano} operações de {ano} ({do_ano/total:.1%}) "
              f"e {outros} de outros anos.")

    print(f"\nConsolidado salvo: {ARQ_PARQUET} ({len(consolidado)} linhas)")
    print(f"Auditorias em: {DIR_AUDITORIA}")

    # Nota P1: valores negativos são estornos/anulações e foram mantidos; as somas
    # acima são LÍQUIDAS. Nenhum fillna(0) foi aplicado — ausência = NaN/NA.


if __name__ == "__main__":
    main()
