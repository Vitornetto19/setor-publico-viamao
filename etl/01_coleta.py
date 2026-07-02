"""etl/01_coleta.py — Fase 2 do pipeline (Extração).

Baixa os ZIPs de "despesa orçamentária por empenhos" da Prefeitura de Viamão/RS
(código TCE-RS 63000) para os anos de 2019 a 2024, direto da API CKAN do TCE-RS,
e registra a proveniência de cada arquivo (URL, nome, hash MD5, data/hora).

Uso:
    python etl/01_coleta.py

Saída:
    dados/raw/viamao_despesa_{ANO}.zip   arquivos originais (não modificar — P2)
    dados/raw/manifest_coleta.csv        registro de proveniência da coleta

Fonte: TCE-RS / SIAPC — https://dados.tce.rs.gov.br/group/despesa
Dados de responsabilidade da Prefeitura de Viamão, enviados via SIAPC e
NÃO auditados pelo Tribunal.
"""

# 1. Imports
from __future__ import annotations

import csv
import hashlib
import sys
from datetime import datetime
from pathlib import Path

import requests

# 2. Constantes (com fonte nos comentários)
# Código do município de Viamão no TCE-RS — aparece nas URLs dos recursos
# (.../municipal/empenhos/{ANO}/63000.csv.zip). Fonte: API CKAN do TCE-RS.
COD_MUNICIPIO_VIAMAO = "63000"

# 2019 a 2024. 2025 é parcial no TCE-RS e fica fora desta coleta
# (ver docs/01_CONTEXTO_PROJETO.md, seção 6).
ANOS = range(2019, 2025)

# API CKAN do TCE-RS (Dados Abertos)
CKAN_PACKAGE_SHOW = "https://dados.tce.rs.gov.br/api/3/action/package_show"
DATASET_ID = "despesa-orcamentaria-por-empenhos-pm-de-viamao-{ano}"  # id do pacote por ano

# Caminhos relativos à raiz do projeto (P5: nunca caminho absoluto do dev)
RAIZ_PROJETO = Path(__file__).resolve().parent.parent
DIR_RAW = RAIZ_PROJETO / "dados" / "raw"
ARQ_MANIFEST = DIR_RAW / "manifest_coleta.csv"

TIMEOUT = 120  # segundos por requisição HTTP
TAMANHO_BLOCO = 8192  # bytes lidos por vez (download em streaming e cálculo de hash)


# 3. Funções
def obter_url_zip(ano: int) -> str:
    """Consulta a API CKAN e devolve a URL do recurso ZIP do dataset do `ano`.

    Levanta RuntimeError se o dataset não existir ou não tiver recurso ZIP —
    ano indisponível é registrado como ausente, nunca inventado (P1).
    """
    dataset_id = DATASET_ID.format(ano=ano)
    resp = requests.get(CKAN_PACKAGE_SHOW, params={"id": dataset_id}, timeout=TIMEOUT)
    resp.raise_for_status()
    payload = resp.json()
    if not payload.get("success"):
        raise RuntimeError(f"CKAN retornou success=False para o dataset {dataset_id}")
    recursos = payload["result"].get("resources", [])
    zips = [r for r in recursos if str(r.get("format", "")).upper() == "ZIP"]
    if not zips:
        formatos = [r.get("format") for r in recursos]
        raise RuntimeError(f"Dataset {dataset_id} sem recurso ZIP (formatos: {formatos})")
    return zips[0]["url"]


def baixar_arquivo(url: str, destino: Path) -> None:
    """Baixa `url` em streaming para `destino` (sobrescreve se já existir)."""
    with requests.get(url, stream=True, timeout=TIMEOUT) as resp:
        resp.raise_for_status()
        with open(destino, "wb") as arq:
            for bloco in resp.iter_content(chunk_size=TAMANHO_BLOCO):
                arq.write(bloco)


def md5_do_arquivo(caminho: Path) -> str:
    """Calcula o hash MD5 de `caminho` lendo em blocos (integridade — P2)."""
    h = hashlib.md5()
    with open(caminho, "rb") as arq:
        for bloco in iter(lambda: arq.read(TAMANHO_BLOCO), b""):
            h.update(bloco)
    return h.hexdigest()


def escrever_manifest(registros: list[dict]) -> None:
    """Grava o manifesto CSV com a proveniência de cada ZIP baixado."""
    campos = ["ano", "arquivo", "url", "tamanho_bytes", "md5", "coletado_em"]
    with open(ARQ_MANIFEST, "w", newline="", encoding="utf-8") as arq:
        escritor = csv.DictWriter(arq, fieldnames=campos)
        escritor.writeheader()
        escritor.writerows(registros)


# 4. main() com prints de progresso (P4)
def main() -> None:
    DIR_RAW.mkdir(parents=True, exist_ok=True)
    registros: list[dict] = []
    anos_ausentes: list[int] = []

    print(f"Coleta — despesas de Viamão/RS (código {COD_MUNICIPIO_VIAMAO})")
    print(f"Anos: {ANOS.start} a {ANOS.stop - 1}")
    print(f"Destino: {DIR_RAW}\n")

    for ano in ANOS:
        print(f"[{ano}] consultando API CKAN...", flush=True)
        try:
            url = obter_url_zip(ano)
        except Exception as erro:  # noqa: BLE001 — registra ausência e segue (P1)
            print(f"[{ano}] INDISPONÍVEL — {erro}\n")
            anos_ausentes.append(ano)
            continue

        destino = DIR_RAW / f"viamao_despesa_{ano}.zip"
        print(f"[{ano}] baixando {url}")
        try:
            baixar_arquivo(url, destino)
        except Exception as erro:  # noqa: BLE001 — falha de rede não invalida os demais anos
            print(f"[{ano}] FALHA no download — {erro}\n")
            anos_ausentes.append(ano)
            continue

        tamanho = destino.stat().st_size
        md5 = md5_do_arquivo(destino)
        registros.append(
            {
                "ano": ano,
                "arquivo": destino.name,
                "url": url,
                "tamanho_bytes": tamanho,
                "md5": md5,
                "coletado_em": datetime.now().isoformat(timespec="seconds"),
            }
        )
        print(f"[{ano}] OK — {tamanho / 1024 / 1024:.2f} MB — MD5 {md5}\n")

    if registros:
        escrever_manifest(registros)

    # 5. Resumo (P4)
    print("=" * 68)
    print("RESUMO DA COLETA")
    print("=" * 68)
    for r in registros:
        print(f"  {r['ano']}  {r['arquivo']:<28} {r['tamanho_bytes'] / 1024 / 1024:>7.2f} MB  {r['md5']}")
    print(f"\n  {len(registros)} de {len(list(ANOS))} anos baixados.")
    if anos_ausentes:
        print(f"  ANOS AUSENTES (registrados, não inventados — P1): {anos_ausentes}")
    print(f"  Manifesto: {ARQ_MANIFEST}")

    # Falha clara se algum ano não veio, sem apagar o que já foi baixado (P4).
    if anos_ausentes:
        sys.exit(f"\nColeta incompleta: anos ausentes {anos_ausentes}.")


if __name__ == "__main__":
    main()
