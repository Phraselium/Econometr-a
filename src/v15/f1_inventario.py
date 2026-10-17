"""V15-F1.1 · Inventario único de variables → docs/v15/inventario_variables.csv y .md. Determinista; sin red; solo lee.

Una fila por variable × nivel territorial × frecuencia de la base completa (data/base/hechos.parquet, V10-V14), con:
- frecuencia, primer y último periodo, número de periodos y de territorios, filas;
- fuente, unidad, licencia y si es redistribuible (data/base/variables.parquet);
- vintage: ediciones distintas y fecha_dato más reciente;
- porcentaje de imputación: filas cuyo metodo_dato es interpolación, reconstrucción o estimación (no observación directa);
- porcentaje de filas posteriores al pre-registro de V9 (posterior_prereg);
- definición exacta y rupturas: de docs/v15/inventario_anotaciones.csv (anotación por familia de variables, hecha por el
  subagente inventariador a partir de los documentos del repositorio; «no consta» si no hay anotación).
Además, los ficheros de data/raw y data/manual que no están en la base (docs/v13/datos_inventario.csv) se listan aparte, con
su clase de licencia, para que nada quede fuera del inventario. Nunca lee la muestra sellada (el inventario la excluye).
"""
from __future__ import annotations

import csv
import fnmatch
import sys
from pathlib import Path

import duckdb
import pandas as pd

RAIZ = Path(__file__).resolve().parents[2]
SAL = RAIZ / "docs" / "v15"
IMPUTA = r"interpol|reconstru|estimad|imput|supuesto|derivada \(stl\)"


def base() -> pd.DataFrame:
    con = duckdb.connect()
    con.execute("SET threads TO 2")
    q = f"""
    SELECT variable, nivel, frecuencia,
           min(periodo) AS primer_periodo, max(periodo) AS ultimo_periodo,
           count(DISTINCT periodo) AS n_periodos, count(DISTINCT territorio_codigo) AS n_territorios, count(*) AS filas,
           count(DISTINCT edicion) AS n_ediciones, max(fecha_dato) AS fecha_dato_max,
           round(100.0 * avg(CASE WHEN regexp_matches(lower(coalesce(metodo_dato, '')), '{IMPUTA}') THEN 1 ELSE 0 END), 2) AS pct_imputado,
           round(100.0 * avg(CASE WHEN posterior_prereg THEN 1 ELSE 0 END), 2) AS pct_posterior_prereg,
           string_agg(DISTINCT metodo_dato, ' | ') AS metodos
    FROM read_parquet('{RAIZ / "data/base/hechos.parquet"}')
    GROUP BY 1, 2, 3 ORDER BY 1, 2, 3"""
    d = con.execute(q).df()
    v = pd.read_parquet(RAIZ / "data/base/variables.parquet")[["variable", "fuente", "unidad", "capa", "licencia", "redistribuible", "definicion"]]
    d = d.merge(v, on="variable", how="left")
    d["metodos"] = d.metodos.str.slice(0, 160)
    return d


def anotaciones(d: pd.DataFrame) -> pd.DataFrame:
    f = SAL / "inventario_anotaciones.csv"
    d["concepto"] = d["definicion_exacta"] = d["rupturas"] = d["fuente_documento"] = "no consta"
    if not f.exists():
        return d
    an = list(csv.DictReader(f.open(encoding="utf-8")))
    for i, var in d.variable.items():
        for a in an:   # la primera familia cuyo patrón (glob) encaja con la variable
            pats = [p.strip() for p in a["familia_o_prefijo"].split(",")]
            if any(fnmatch.fnmatch(var, p) for p in pats):
                for c in ("concepto", "definicion_exacta", "rupturas", "fuente_documento"):
                    d.at[i, c] = a.get(c) or "no consta"
                break
    return d


def fuera_de_base() -> pd.DataFrame:
    inv = pd.read_csv(RAIZ / "docs/v13/datos_inventario.csv")
    inv = inv[inv.fichero.str.startswith(("data/raw/", "data/manual/")) & ~inv.fichero.str.contains("_manifest")]
    return inv[["fichero", "carpeta", "clase", "fuente", "licencia", "motivo"]].sort_values("fichero")


def md(d: pd.DataFrame, f: pd.DataFrame) -> str:
    por = d.groupby("concepto").agg(variables=("variable", "nunique"), filas=("filas", "sum")).sort_values("variables", ascending=False)
    L = ["# V15 · Inventario único de variables (fase 1.1)", "",
         "Generado por `python3 src/v15/f1_inventario.py` desde data/base/hechos.parquet (base V10-V14), data/base/variables.parquet y "
         "docs/v15/inventario_anotaciones.csv. La tabla completa está en [inventario_variables.csv](inventario_variables.csv): una fila por "
         "variable × nivel × frecuencia. Los ficheros de datos versionados de data/raw y data/manual (con su clase de licencia), en "
         "[inventario_ficheros_fuera_base.csv](inventario_ficheros_fuera_base.csv).", "",
         f"- Variables distintas: {d.variable.nunique()}; combinaciones variable × nivel × frecuencia: {len(d)}; filas: {int(d.filas.sum()):,}.".replace(",", "."),
         f"- Con alguna imputación (interpolación, reconstrucción o estimación): {int((d.pct_imputado > 0).sum())} combinaciones; "
         f"con más del 20 % imputado: {int((d.pct_imputado > 20).sum())}.",
         f"- Sin anotación de definición o rupturas: {int((d.definicion_exacta == 'no consta').sum())} combinaciones (se completan en la auditoría).",
         f"- No redistribuibles: {d[d.redistribuible.eq(False)].variable.nunique()} variables.",
         f"- Ficheros de datos versionados (data/raw y data/manual; docs/v13/datos_inventario.csv): {len(f)} (clase a: {int((f.clase == 'a').sum())}, b: {int((f.clase == 'b').sum())}, c: {int((f.clase == 'c').sum())}).", "",
         "## Por concepto", "", "| Concepto | Variables | Filas |", "|---|---|---|"]
    L += [f"| {k} | {r.variables} | {int(r.filas):,} |".replace(",", ".") for k, r in por.iterrows()]
    L += ["", "## Variables con más del 20 % de filas imputadas (solo en robustez, regla A del plan)", "",
          "| Variable | Nivel | Frecuencia | % imputado | Métodos |", "|---|---|---|---|---|"]
    for r in d[d.pct_imputado > 20].sort_values("pct_imputado", ascending=False).itertuples():
        L.append(f"| {r.variable} | {r.nivel} | {r.frecuencia} | {r.pct_imputado} | {str(r.metodos).replace('|', '/')[:80]} |")
    L += ["", "## Rupturas anotadas", "", "| Familia | Rupturas | Documento |", "|---|---|---|"]
    rup = d[d.rupturas != "no consta"].drop_duplicates("rupturas")
    for r in rup.itertuples():
        L.append(f"| {r.variable} | {str(r.rupturas).replace('|', '/')} | {r.fuente_documento} |")
    return "\n".join(L) + "\n"


def main() -> int:
    d = anotaciones(base())
    f = fuera_de_base()
    cols = ["variable", "concepto", "nivel", "frecuencia", "primer_periodo", "ultimo_periodo", "n_periodos", "n_territorios", "filas",
            "fuente", "unidad", "capa", "licencia", "redistribuible", "n_ediciones", "fecha_dato_max", "pct_imputado", "pct_posterior_prereg",
            "definicion_exacta", "rupturas", "definicion", "metodos", "fuente_documento"]
    d[cols].to_csv(SAL / "inventario_variables.csv", index=False)
    f.to_csv(SAL / "inventario_ficheros_fuera_base.csv", index=False)
    (SAL / "inventario_variables.md").write_text(md(d, f), encoding="utf-8")
    print(f"f1_inventario: {d.variable.nunique()} variables, {len(d)} combinaciones, {len(f)} ficheros fuera de la base")
    return 0


if __name__ == "__main__":
    sys.exit(main())
