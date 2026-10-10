"""D2 v3: alquiler medio mensual de viviendas habituales arrendadas por código postal, Comunidad de Madrid.

Fuente: datos.comunidad.madrid, dataset 1934258 (CSV ;-separado, latin-1). Solo códigos postales con >200 viviendas arrendadas.
ORIGEN DE LOS DATOS NO VERIFICADO en la ficha del dataset (¿registro de fianzas o declaraciones?): se marca así en 'fuente'.
Nivel: código postal (CP). No es municipio ni distrito; el cruce con distrito queda pendiente.
Salida: data/raw/v3/madrid_alquiler_cp_v3.csv.gz. Caché por fichero original (FORCE=1 para rehacer).
"""
from __future__ import annotations

import gzip
import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import utils_fetch as uf  # noqa: E402

URL = "https://datos.comunidad.madrid/dataset/c9b49b8c-47a5-4deb-83b5-080b582fda7e/resource/54fbc230-31fd-4cf3-9673-7a85fed2a784/download/alquiler-medio-mensual-de-viviendas-habituales-arrendadas.csv"
ORIG = uf.RAW / "v3_orig" / "madrid_alquiler_cp_1934258.csv"
DEST = uf.RAW / "v3" / "madrid_alquiler_cp_v3.csv.gz"
FUENTE = "Comunidad de Madrid - Alquiler medio mensual de viviendas habituales arrendadas por CP (datos.comunidad.madrid 1934258; origen no verificado)"


def main() -> None:
    if DEST.exists() and not uf.FORCE:
        print(f"[cache] {DEST.relative_to(uf.ROOT)}")
        return
    uf.download(URL, ORIG)
    df = pd.read_csv(ORIG, sep=";", encoding="latin-1", dtype=str)
    df.columns = ["anio", "concepto", "tipo_territorio", "codigo_raw", "territorio_raw", "valor", "unidad", "estado"]
    df = df[df["concepto"].str.startswith("Alquiler medio", na=False)].copy()
    df["cp"] = df["concepto"].str.extract(r"código postal (\d{5})")[0]
    df["territorio"] = df["concepto"].str.extract(r"código postal \d{5}-(.*)$")[0].str.strip()
    df["valor"] = pd.to_numeric(df["valor"].str.replace(",", ".", regex=False), errors="coerce")
    df["anio"] = df["anio"].astype(int)
    out = pd.DataFrame({
        "fecha": df["anio"].astype(str) + "-01-01", "periodo": df["anio"].astype(str),
        "serie": "MADRID_ALQ_CP_" + df["cp"] + "_alquiler_medio_mensual",
        "valor": df["valor"], "unidad": "EUR/mes", "fuente": FUENTE, "url": URL,
        "territorio": df["territorio"], "nivel": "CP", "codigo": df["cp"],
    }).sort_values(["serie", "fecha"])
    DEST.parent.mkdir(parents=True, exist_ok=True)
    with gzip.open(DEST, "wt", encoding="utf-8", newline="") as fh:
        out.to_csv(fh, index=False)
    print(f"[ok] {DEST.relative_to(uf.ROOT)}: {len(out)} obs, {out['serie'].nunique()} series, "
          f"años {sorted(out['anio'].unique().tolist()) if 'anio' in out else out['periodo'].unique().tolist()}, NaN={int(out['valor'].isna().sum())}")


if __name__ == "__main__":
    main()
