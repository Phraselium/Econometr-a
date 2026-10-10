"""Descarga series de Eurostat (API de difusión, JSON-stat 2.0) a data/raw en formato largo.

Uso (desde la raíz del repo):
    python src/fetch_eurostat.py          # respeta la caché por archivo
    FORCE=1 python src/fetch_eurostat.py  # vuelve a descargar todo

Notas:
- Los filtros multivaluados se envían como parámetros repetidos (?purchase=A&purchase=B).
  Las listas separadas por comas no funcionan en este endpoint (devuelven dimensiones vacías).
- Cada archivo de salida admite una lista de candidatos de filtros; se usa el primero que
  devuelve valores. Si ninguno funciona, el fallo se anota en docs/fuentes_fallidas.md.
"""
from __future__ import annotations

import datetime as dt
import re
from urllib.parse import urlencode

import pandas as pd

from utils_fetch import ROOT, cached, get, save

BASE = "https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/"
FUENTE = "Eurostat"
FALLIDAS = ROOT / "docs" / "fuentes_fallidas.md"

NUTS2_ES = [
    "ES11", "ES12", "ES13", "ES21", "ES22", "ES23", "ES24", "ES30", "ES41", "ES42",
    "ES43", "ES51", "ES52", "ES53", "ES61", "ES62", "ES63", "ES64", "ES70",
]


def parse_periodo(p: str) -> dt.date:
    """'2008-Q1' -> 2008-01-01; '2008-M03' -> 2008-03-01; '2008-S2' -> 2008-07-01; '2008' -> 2008-01-01."""
    if m := re.fullmatch(r"(\d{4})-Q([1-4])", p):
        return dt.date(int(m[1]), 3 * int(m[2]) - 2, 1)
    if m := re.fullmatch(r"(\d{4})-M?(\d{2})", p):
        return dt.date(int(m[1]), int(m[2]), 1)
    if m := re.fullmatch(r"(\d{4})-S([12])", p):
        return dt.date(int(m[1]), 1 if m[2] == "1" else 7, 1)
    if re.fullmatch(r"\d{4}", p):
        return dt.date(int(p), 1, 1)
    raise ValueError(f"periodo no reconocido: {p!r}")


def _codigos(dim: dict) -> list[str]:
    """Lista de códigos de una dimensión ordenada por posición (category.index: código -> posición)."""
    idx = dim["category"]["index"]
    if isinstance(idx, list):
        return list(idx)
    inv = {pos: code for code, pos in idx.items()}
    return [inv[p] for p in range(len(idx))]


def jsonstat_a_largo(j: dict) -> pd.DataFrame:
    """Parser JSON-stat 2.0 genérico.

    - 'value' es un dict índice-plano -> valor. El índice recorre el producto cartesiano de
      las dimensiones en el orden de 'id' (la última dimensión varía más rápido).
      Las celdas ausentes en 'value' se convierten en NaN.
    - Cada dimensión no temporal se decodifica a una columna con su código.
    - 'serie' = concatenación ('|') de los códigos de las dimensiones no temporales.
    - 'periodo' = código temporal original; 'fecha' = primer día del periodo (ISO).
    - 'unidad' = etiqueta de la dimensión 'unit' (o su código si no tiene etiqueta).
    """
    ids, sizes = j["id"], j["size"]
    if "time" not in ids:
        raise ValueError("el dataset no tiene dimensión temporal 'time'")
    dims = {d: _codigos(j["dimension"][d]) for d in ids}
    for d, n in zip(ids, sizes):
        if len(dims[d]) != n:
            raise ValueError(f"dimensión {d}: size={n} pero {len(dims[d])} categorías")

    strides = [1] * len(sizes)
    for i in range(len(sizes) - 2, -1, -1):
        strides[i] = strides[i + 1] * sizes[i + 1]
    total = 1
    for n in sizes:
        total *= n

    valores = j.get("value", {})
    etiquetas_unidad = j["dimension"].get("unit", {}).get("category", {}).get("label", {}) \
        if "unit" in ids else {}
    no_tiempo = [d for d in ids if d != "time"]

    rows = []
    for k in range(total):
        cod = {d: dims[d][(k // strides[i]) % sizes[i]] for i, d in enumerate(ids)}
        if isinstance(valores, dict):
            v = valores.get(str(k))
        else:
            v = valores[k] if k < len(valores) else None
        rows.append({**{d: cod[d] for d in no_tiempo}, "periodo": cod["time"], "valor": v})

    df = pd.DataFrame(rows, columns=no_tiempo + ["periodo", "valor"])
    df["valor"] = pd.to_numeric(df["valor"], errors="coerce")
    df["fecha"] = df["periodo"].map(lambda p: parse_periodo(p).isoformat())
    df["serie"] = df[no_tiempo].astype(str).agg("|".join, axis=1)
    if "unit" in no_tiempo:
        df["unidad"] = df["unit"].map(lambda c: etiquetas_unidad.get(c, c))
    else:
        df["unidad"] = ""
    return df


def _pares(filtros: dict, **extra) -> list[tuple[str, str]]:
    pares: list[tuple[str, str]] = []
    for k, v in filtros.items():
        for val in (v if isinstance(v, (list, tuple)) else [v]):
            pares.append((k, val))
    pares.extend(extra.items())
    return pares


def _url(dataset: str, filtros: dict, **extra) -> str:
    return BASE + dataset + "?" + urlencode(_pares(filtros, **extra))


def _descargar(dataset: str, filtros: dict) -> tuple[pd.DataFrame, str, str]:
    """Petición pequeña previa (verifica endpoint y última fecha) y luego descarga completa."""
    url_small = _url(dataset, filtros, lastTimePeriod=1)
    df_small = jsonstat_a_largo(get(url_small))
    ultimo = df_small.loc[df_small["valor"].notna(), "periodo"].max() if df_small["valor"].notna().any() else None
    if ultimo is None:
        raise ValueError("la petición pequeña no devuelve valores")

    url = _url(dataset, filtros)
    df = jsonstat_a_largo(get(url))
    if df.empty or df["valor"].notna().sum() == 0:
        raise ValueError("la respuesta completa no contiene valores")
    return df, url, str(ultimo)


def _recortar_vacios(df: pd.DataFrame) -> pd.DataFrame:
    """Quita los periodos vacíos al inicio y al final de cada serie (celdas no publicadas).
    Los NaN internos se conservan tal cual. Las series sin ningún valor se descartan."""
    partes = []
    for _, g in df.groupby("serie", sort=False):
        con_valor = g.loc[g["valor"].notna(), "fecha"]
        if con_valor.empty:
            continue
        partes.append(g[(g["fecha"] >= con_valor.min()) & (g["fecha"] <= con_valor.max())])
    return pd.concat(partes, ignore_index=True)


def _registrar_fallo(nombre: str, dataset: str, errores: list[tuple[str, str]]) -> None:
    FALLIDAS.parent.mkdir(parents=True, exist_ok=True)
    nuevo = not FALLIDAS.exists()
    with FALLIDAS.open("a", encoding="utf-8") as f:
        if nuevo:
            f.write("# Fuentes fallidas\n\n")
        f.write(f"## {nombre} (dataset {dataset})\n")
        for url, err in errores:
            f.write(f"- URL probada: {url}\n  - Error: {err}\n")
        f.write("- Alternativa propuesta: consultar las dimensiones válidas del dataset "
                "(petición sin filtros con lastTimePeriod) y ajustar los filtros.\n\n")


def procesar(nombre: str, dataset: str, candidatos: list[dict]) -> bool:
    if cached(nombre):
        return True
    errores: list[tuple[str, str]] = []
    for i, filtros in enumerate(candidatos):
        try:
            df, url, ultimo = _descargar(dataset, filtros)
        except Exception as e:  # noqa: BLE001
            errores.append((_url(dataset, filtros), str(e)))
            print(f"[fallo] {nombre} candidato {i + 1}: {e}")
            continue
        antes = len(df)
        df = _recortar_vacios(df.assign(fuente=FUENTE, url=url))
        print(f"[info] {nombre}: {antes - len(df)} filas vacías de inicio/fin recortadas")
        save(df, nombre, FUENTE)
        alt = "" if i == 0 else f" (alternativa {i + 1})"
        print(f"[info] {nombre}: última publicación {ultimo}{alt}; filtros {filtros}")
        return True
    _registrar_fallo(nombre, dataset, errores)
    print(f"[FALLO] {nombre}: sin candidatos válidos; ver docs/fuentes_fallidas.md")
    return False


SERIES = [
    # 1. Renta disponible bruta de hogares (S14_S15), trimestral. SCA; NSA como alternativa.
    ("eurostat_renta_hogares.csv", "nasq_10_nf_tr", [
        {"geo": "ES", "sector": "S14_S15", "na_item": "B6G", "direct": "RECV",
         "unit": "CP_MEUR", "s_adj": "SCA"},
        {"geo": "ES", "sector": "S14_S15", "na_item": "B6G", "direct": "RECV",
         "unit": "CP_MEUR", "s_adj": "NSA"},
    ]),
    # 2. Permisos de construcción de viviendas (BPRM_DW), trimestral, índice 2021=100.
    ("eurostat_permisos.csv", "sts_cobp_q", [
        {"geo": "ES", "indic_bt": "BPRM_DW", "cpa2_1": "CPA_F41001_X_410014",
         "s_adj": "SCA", "unit": "I21"},
    ]),
    # 3. Costes de construcción de edificios residenciales (COST), trimestral, NSA.
    ("eurostat_costes.csv", "sts_copi_q", [
        {"geo": "ES", "indic_bt": "COST", "cpa2_1": "CPA_F41001_X_410014",
         "unit": "I21", "s_adj": "NSA"},
    ]),
    # 4. Índice de precios de vivienda: total, obra nueva (DW_NEW) y existente (DW_EXST).
    #    En Eurostat el código de obra nueva es DW_NEW (no NEW).
    ("eurostat_hpi.csv", "prc_hpi_q", [
        {"geo": "ES", "purchase": ["TOTAL", "DW_NEW", "DW_EXST"],
         "unit": ["I15_Q", "RCH_A"]},
    ]),
    # 5. Inmigración anual a ES por ciudadanía (todas las categorías de citizen), agedef=REACH.
    ("eurostat_inmigracion_anual.csv", "migr_imm1ctz", [
        {"geo": "ES", "age": "TOTAL", "sex": "T", "agedef": "REACH"},
    ]),
    # 6. Empleo anual NUTS2 de España (opcional).
    ("eurostat_empleo_nuts2.csv", "lfst_r_lfe2en2", [
        {"geo": NUTS2_ES, "sex": "T", "age": "Y15-64", "nace_r2": "TOTAL", "unit": "THS_PER"},
    ]),
    # 7. Producción en construcción (PRD, F, SCA), trimestral, índice 2021=100.
    ("eurostat_produccion_construccion.csv", "sts_copr_q", [
        {"geo": "ES", "indic_bt": "PRD", "nace_r2": "F", "s_adj": "SCA", "unit": "I21"},
    ]),
]


def main() -> None:
    resultados = {nombre: procesar(nombre, dataset, cands) for nombre, dataset, cands in SERIES}
    fallos = [n for n, ok in resultados.items() if not ok]
    print(f"[resumen] {len(resultados) - len(fallos)}/{len(resultados)} archivos OK"
          + (f"; fallos: {fallos}" if fallos else ""))


if __name__ == "__main__":
    main()
