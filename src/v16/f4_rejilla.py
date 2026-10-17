"""V16-F4 · Rejilla multiescala FIJA para el control de falsos descubrimientos (adenda del pre-registro V16, puntos R1-R2 y A4-A5).

Parte de output/v16/potencia/rejilla_candidata.csv y la cierra antes de estimar:
- solo dimensiones con exposición territorial definida: Q1 (zona tensionada), Q2 (porcentaje de vivienda turística INE),
  Q3 (crecimiento predicho de la población extranjera, shift-share), Q4 (Red Natura × choque de demanda) y Q6 (tipo general del ITP);
  Q5, Q7 y Q9 no tienen exposición territorial y se estudian solo en su pregunta (fuera de la rejilla);
- solo escalas sección, distrito, municipio y provincia (sin nación; sin CCAA: tras excluir las 8 CCAA de v6 quedan 9 < 10);
- recuento de unidades tras holdout.unidad_sellada_v16 (v6 + V15 + V16) y filas no marcadas como muestra v6; celdas con < 10
  unidades fuera;
- una exposición, una ventana y UNA especificación principal por celda (efectos fijos de unidad y periodo, exposición continua,
  errores agrupados por la unidad superior); las demás variantes son robustez y no entran en el denominador del control.
Escribe output/v16/potencia/rejilla_fija.csv. Solo cuenta unidades: no estima nada. Determinista y sin red.
"""
from __future__ import annotations

import sys
from pathlib import Path

import duckdb
import pandas as pd

RAIZ = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(RAIZ / "src"))
import holdout  # noqa: E402

CAND = RAIZ / "output" / "v16" / "potencia" / "rejilla_candidata.csv"
SAL = RAIZ / "output" / "v16" / "potencia" / "rejilla_fija.csv"
FUENTES = [RAIZ / "data" / "base" / "hechos.parquet"] + sorted((RAIZ / "data" / "processed" / "v16").glob("*.parquet"))
MIN_UNIDADES = 10
ESCALAS = ("seccion", "distrito", "municipio", "provincia")
EXPOSICION = {
    "regulación del alquiler (Q1)": ("Q1", "zona tensionada vigente (0/1; en provincia: cuota de población en zona)", "2019-2025"),
    "vivienda turística (Q2)": ("Q2", "porcentaje de vivienda turística INE (media anual), estandarizado", "2021-2024"),
    "inmigración (Q3)": ("Q3", "crecimiento predicho de la población extranjera (cuotas 2003 × choques nacionales sin la unidad)", "2011-2024"),
    "oferta y restricciones (Q4)": ("Q4", "% de superficie en Red Natura × choque de demanda de Q3", "2018-2025"),
    "fiscalidad de la compra (Q6)": ("Q6", "tipo general del ITP de su CCAA (puntos)", "2011-2024"),
}
# celdas que repiten una hipótesis confirmatoria de V15 (misma exposición, resultado y escala): fuera hasta su evaluación (adenda R13)
REPITEN_V15 = {("Q1", "municipio", "incasol_renta_media"): "H1", ("Q1", "municipio", "incasol_contratos"): "H2",
               ("Q2", "seccion", "serpavi_alquiler_m2_mediana"): "H3", ("Q2", "seccion", "serpavi_alquiler_mes_mediana"): "H3",
               ("Q3", "municipio", "serpavi_alquiler_m2_mediana"): "H4"}
AGRUPA = {"seccion": "municipio", "distrito": "municipio", "municipio": "provincia", "provincia": "provincia (wild bootstrap de Webb)"}


def _unidades(variable: str, nivel: str) -> int:
    cods = set()
    for f in FUENTES:
        try:
            d = duckdb.sql(f"SELECT DISTINCT territorio_codigo FROM read_parquet('{f}') WHERE variable = '{variable}' AND nivel = '{nivel}'"
                           " AND NOT coalesce(muestra_sellada_v6, false)").df()
        except duckdb.Error:      # parquets sin esas columnas (tablas de correspondencia)
            continue
        cods |= set(d.territorio_codigo.astype(str))
    if not cods:
        return 0
    s = pd.Series(sorted(cods))
    return int((~holdout.unidad_sellada_v16(s, nivel)).sum())


def main() -> int:
    c = pd.read_csv(CAND, dtype=str)
    c = c[c.dimension.isin(EXPOSICION) & c.escala.isin(ESCALAS)].copy()
    cache: dict[tuple[str, str], int] = {}
    filas = []
    for r in c.itertuples():
        k = (r.resultado, r.escala)
        if k not in cache:
            cache[k] = _unidades(*k)
        n = cache[k]
        q, expo, ventana = EXPOSICION[r.dimension]
        filas.append({"celda": f"{q}|{r.escala}|{r.resultado}", "pregunta": q, "escala": r.escala, "resultado": r.resultado,
                      "familia_resultado": r.familia_resultado, "exposicion": expo, "ventana": ventana,
                      "especificacion_principal": f"Δ/log del resultado ~ exposición + EF de unidad y periodo; errores agrupados por {AGRUPA[r.escala]}",
                      "unidades_entrenamiento": n,
                      "en_rejilla": n >= MIN_UNIDADES and (q, r.escala, r.resultado) not in REPITEN_V15,
                      "motivo_fuera": (f"repite {REPITEN_V15[(q, r.escala, r.resultado)]} de V15" if (q, r.escala, r.resultado) in REPITEN_V15
                                       else "" if n >= MIN_UNIDADES else f"{n} unidades de entrenamiento (< {MIN_UNIDADES})")})
    out = pd.DataFrame(filas).sort_values(["pregunta", "escala", "resultado"]).reset_index(drop=True)
    out.to_csv(SAL, index=False, lineterminator="\n")
    dentro = out[out.en_rejilla]
    print(f"f4_rejilla: {len(out)} celdas candidatas, {len(dentro)} en la rejilla fija; por pregunta: "
          f"{dentro.groupby('pregunta').size().to_dict()}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
