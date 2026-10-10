"""D2 v3: fianzas de alquiler depositadas en Incasòl (Generalitat de Catalunya), por municipio.

Flujo de CONTRATOS NUEVOS de alquiler (registro de fianzas), distinto del stock IRPF de SERPAVI.
Fuente: Socrata analisi.transparenciacatalunya.cat, dataset qww9-bvhh (Preu mitjà del lloguer d'habitatges per municipi).
Campos: any, periode (ventana temporal: trimestres, semestres, acumulados o anual), codi_territorial (INE 5 dígitos),
habitatges (nº de contratos depositados en la banda), renda (renta media de la banda, EUR/mes), tram_preus (banda de precio).

Salida: data/raw/v3/incasol_fianzas_municipio_v3.csv.gz (formato largo, una fila por municipio x periodo x banda x variable).
Las filas con 'renda' vacía se mantienen como NaN (no se imputan). Las bandas cambian de definición entre años: no se empalman.
Caché: si el fichero de salida existe no se vuelve a descargar (FORCE=1 para rehacer).
"""
from __future__ import annotations

import gzip
import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import utils_fetch as uf  # noqa: E402

BASE = "https://analisi.transparenciacatalunya.cat/resource/qww9-bvhh.json"
URL = "https://analisi.transparenciacatalunya.cat/d/qww9-bvhh"
FUENTE = "Incasòl - Registre de fiances de lloguer (Socrata qww9-bvhh)"
NAME = "v3/incasol_fianzas_municipio_v3.csv.gz"
DEST = uf.RAW / NAME

# Ventana: mes inicial y mes final del periodo (para fecha = inicio del periodo)
MES = {"gener": 1, "febrer": 2, "març": 3, "abril": 4, "maig": 5, "juny": 6, "juliol": 7,
       "agost": 8, "setembre": 9, "octubre": 10, "novembre": 11, "desembre": 12}


def descargar() -> list[dict]:
    filas, off = [], 0
    while True:
        r = uf.get(BASE, params={"$limit": 50000, "$offset": off, "$order": ":id"}, as_json=True)
        filas += r
        if len(r) < 50000:
            break
        off += 50000
    return filas


def main() -> None:
    if DEST.exists() and not uf.FORCE:
        print(f"[cache] {DEST.relative_to(uf.ROOT)}")
        return
    DEST.parent.mkdir(parents=True, exist_ok=True)
    rows = descargar()
    df = pd.DataFrame(rows)
    assert {"any", "periode", "codi_territorial", "habitatges", "tram_preus"} <= set(df.columns), df.columns
    df["habitatges"] = pd.to_numeric(df["habitatges"], errors="coerce")
    df["renda"] = pd.to_numeric(df.get("renda"), errors="coerce")
    partes = df["periode"].str.split("-", n=1, expand=True)
    df["mes_ini"] = partes[0].map(MES)
    df["mes_fin"] = partes[1].map(MES)
    if df["mes_ini"].isna().any() or df["mes_fin"].isna().any():
        raise ValueError("periodo no reconocido: " + str(df.loc[df["mes_ini"].isna(), "periode"].unique()))
    df["fecha"] = pd.to_datetime(dict(year=df["any"].astype(int), month=df["mes_ini"], day=1)).dt.strftime("%Y-%m-%d")
    df["periodo"] = df["any"].astype(int).astype(str) + " " + df["periode"]
    df["codigo"] = df["codi_territorial"].astype(str).str.zfill(5)
    df["territorio"] = df["nom_territori"]
    df["nivel"] = "MUN"
    df["unidad"] = "contratos"
    df["fuente"] = FUENTE
    df["url"] = URL
    df["banda"] = df["tram_preus"].str.replace(" ", "")
    base = ["fecha", "periodo", "territorio", "nivel", "codigo", "banda", "fuente", "url"]
    n_df = df.assign(serie="INCASOL_FIANZAS_" + df["codigo"] + "_n_contratos_" + df["banda"],
                     valor=df["habitatges"], unidad="contratos")
    r_df = df.assign(serie="INCASOL_FIANZAS_" + df["codigo"] + "_renta_media_" + df["banda"],
                     valor=df["renda"], unidad="EUR/mes")
    # Total municipal por periodo (suma de bandas de contratos; sin imputar)
    tot = (df.groupby(["fecha", "periodo", "territorio", "codigo"], as_index=False)["habitatges"].sum(min_count=1)
             .rename(columns={"habitatges": "valor"}))
    tot["serie"] = "INCASOL_FIANZAS_" + tot["codigo"] + "_n_contratos_TOTAL_bandas"
    tot["unidad"] = "contratos"
    tot["fuente"] = FUENTE
    tot["url"] = URL
    tot["nivel"] = "MUN"
    tot["banda"] = "TOTAL_bandas"
    cols = ["fecha", "periodo", "serie", "valor", "unidad", "fuente", "url", "territorio", "nivel", "codigo", "banda"]
    out = pd.concat([n_df[cols], r_df[cols], tot[cols]], ignore_index=True)
    out = out.sort_values(["serie", "fecha"])
    with gzip.open(DEST, "wt", encoding="utf-8", newline="") as fh:
        out.to_csv(fh, index=False)
    na = int(out["valor"].isna().sum())
    print(f"[ok] {DEST.relative_to(uf.ROOT)}: {len(out)} filas, {out['serie'].nunique()} series, "
          f"{out['fecha'].min()} -> {out['fecha'].max()}, NaN={na}, municipios={out['codigo'].nunique()}")
    print(f"[bytes] {DEST.stat().st_size/1e6:.1f} MB")


if __name__ == "__main__":
    main()
