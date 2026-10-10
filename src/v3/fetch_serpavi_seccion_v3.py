"""D2 v3: SERPAVI (MIVAU, stock de contratos de alquiler declarados en IRPF) a nivel de sección censal y distrito censal, nacional, 2011-2024.

NOTA: SERPAVI es el STOCK de contratos declarados en el IRPF (Modelo 100), no el flujo de contratos nuevos;
por construcción amortigua los cambios de precio (las medianas incluyen contratos vigentes firmados en años anteriores).

Fuente: el mismo xlsx oficial usado en v2 (url en data/raw/pdf/serpavi_v2_municipios.csv.gz).
Hojas usadas: 'Secciones censales' y 'Distritos'; 'Municipios' solo para el cuadre sección -> municipio.
Salidas (formato largo, csv.gz): data/raw/v3/serpavi_secciones_nacional_v3.csv.gz y serpavi_distritos_nacional_v3.csv.gz.
Caché: el xlsx original se reutiliza si existe (FORCE=1 para redescargar).
"""
from __future__ import annotations

import gzip
import re
import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import utils_fetch as uf  # noqa: E402

ROOT = uf.ROOT
RAW_V3 = uf.RAW / "v3"
ORIG = uf.RAW / "pdf" / "originales" / "serpavi_bd_2011-2024.xlsx"
URL = ("https://cdn.mivau.gob.es/portal-web-mivau/vivienda/serpavi/"
       "2026-03-09_bd_SERPAVI_2011-2024%20-%20DEFINITIVO%20WEB.xlsx")
FUENTE = "MIVAU-SERPAVI (AEAT IRPF, stock de contratos declarados)"
SEED = 20261010

# Prefijo de variable -> (unidad, nombre corto)
PAT = re.compile(r"^(BI_ALVHEPCO_TV[CU]|ALQM2_LV_(?:M|25|75)_V[CU]|ALQTBID12_(?:M|25|75)_V[CU]|SLVM2_(?:M|25|75)_V[CU])_(\d{2})$")
UNIDAD = {"BI": "viviendas", "ALQM2": "EUR/m2/mes", "ALQTBID12": "EUR/mes", "SLVM2": "m2"}


def unidad_de(var: str) -> str:
    for k, u in UNIDAD.items():
        if var.startswith(k):
            return u
    raise ValueError(var)


def a_largo(df: pd.DataFrame, cod_col: str, nivel: str, nombre_col: str) -> pd.DataFrame:
    cols = [c for c in df.columns if isinstance(c, str) and PAT.match(c)]
    base = df[[cod_col, nombre_col, "CPRO", "CUMUN"]].copy()
    base.columns = ["codigo", "nombre", "cpro", "cumun"]
    wide = pd.concat([base, df[cols].apply(pd.to_numeric, errors="coerce")], axis=1)
    long = wide.melt(id_vars=["codigo", "nombre", "cpro", "cumun"], value_vars=cols,
                     var_name="campo", value_name="valor").dropna(subset=["valor"])
    m = long["campo"].str.extract(PAT)
    long["variable"] = m[0]
    long["anio"] = 2000 + m[1].astype(int)
    long["fecha"] = pd.to_datetime(long["anio"].astype(str) + "-01-01").dt.strftime("%Y-%m-%d")
    long["periodo"] = long["anio"].astype(str)
    long["unidad"] = long["variable"].map(unidad_de)
    long["serie"] = "SERPAVI_" + nivel + "_" + long["codigo"].astype(str) + "_" + long["variable"]
    long["fuente"] = FUENTE
    long["url"] = URL
    long["territorio"] = long["nombre"]
    long["nivel"] = nivel
    long["codigo"] = long["codigo"].astype(str)
    long["cuadre_cumun"] = long["cumun"]
    return long.drop(columns=["campo", "anio", "cpro", "variable", "nombre"])


def main() -> None:
    if not ORIG.exists() or ORIG.stat().st_size == 0 or uf.FORCE:
        uf.download(URL, ORIG)
    else:
        print(f"[cache] {ORIG.relative_to(ROOT)}")
    RAW_V3.mkdir(parents=True, exist_ok=True)
    xl = pd.ExcelFile(ORIG, engine="openpyxl")
    sec = xl.parse("Secciones censales", dtype=str)
    dis = xl.parse("Distritos", dtype=str)
    mun = xl.parse("Municipios", dtype=str)

    # Secciones: codigo CUSEC (10 dígitos, CPRO+CUMUN+sección); nombre = municipio
    sec["CUSEC"] = sec["CUSEC"].astype(str).str.zfill(10)
    ls = a_largo(sec, "CUSEC", "SEC", "LITMUN")
    dis["CUDIS"] = dis["CUDIS"].astype(str)
    ld = a_largo(dis, "CUDIS", "DIS", "LITMUN")

    # Cuadre: suma de secciones de cada municipio = total municipal (recuento de inmuebles en alquiler, VC+VU)
    cnt = ls[ls["serie"].str.contains("BI_ALVHEPCO")].copy()
    cnt["cumun"] = cnt["codigo"].str[:5]
    suma = cnt.groupby(["cumun", "fecha"])["valor"].sum().rename("suma_secciones")
    mun = mun.rename(columns={"CUMUN": "cumun"})
    mun["cumun"] = mun["cumun"].astype(str).str.zfill(5)
    mv = [c for c in mun.columns if isinstance(c, str) and re.match(r"^BI_ALVHEPCO_TV[CU]_\d{2}$", c)]
    mlong = mun[["cumun"] + mv].melt(id_vars="cumun", var_name="c", value_name="total_mun")
    mlong["total_mun"] = pd.to_numeric(mlong["total_mun"], errors="coerce")
    mlong["fecha"] = "20" + mlong["c"].str[-2:] + "-01-01"
    mtot = mlong.groupby(["cumun", "fecha"])["total_mun"].sum(min_count=1)
    cu = pd.concat([suma, mtot], axis=1).dropna()
    diff = (cu["suma_secciones"] - cu["total_mun"]).abs()
    cuadre = {
        "n_municipio_anio": int(len(cu)),
        "pct_exacto": round(float((diff < 0.5).mean()) * 100, 2) if len(cu) else None,
        "max_abs_dif": float(diff.max()) if len(cu) else None,
    }
    print("[cuadre secciones->municipio]", cuadre)

    p_sec = RAW_V3 / "serpavi_secciones_nacional_v3.csv.gz"
    p_dis = RAW_V3 / "serpavi_distritos_nacional_v3.csv.gz"
    ls = ls.drop(columns=["cuadre_cumun"])
    ld = ld.drop(columns=["cuadre_cumun"])
    cols = ["fecha", "periodo", "serie", "valor", "unidad", "fuente", "url", "territorio", "nivel", "codigo"]
    for df, p in [(ls, p_sec), (ld, p_dis)]:
        df = df[cols].sort_values(["serie", "fecha"])
        with gzip.open(p, "wt", encoding="utf-8", newline="") as fh:
            df.to_csv(fh, index=False)
        print(f"[ok] {p.relative_to(ROOT)}: {len(df)} obs, {df['serie'].nunique()} series, "
              f"{df['fecha'].min()} -> {df['fecha'].max()}, {p.stat().st_size/1e6:.1f} MB")
    print("[cuadre json]", cuadre)


if __name__ == "__main__":
    main()
