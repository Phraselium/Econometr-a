"""V17 · Fase 2 · Tabla comparativa de la lectura convencional (análisis a posteriori).

Une las tablas de inferencia convencional de los grupos (output/v17/lectura_bde/<grupo>/inferencia.csv). Normaliza la regla de
publicación y comprueba que se cumple: ninguna fila con un tamaño real mayor que el 15 % lleva inferencia publicable. Si existe
docs/v17/mejor_estimacion.csv (B4, juicio experto por canal), lo añade por canal.

Salidas: output/v17/lectura_bde/tabla_comparativa.{csv,md}, con las columnas capa del proyecto | lectura convencional |
distorsión | mejor estimación | confianza. Determinista; sin red.
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd

RAIZ = Path(__file__).resolve().parents[2]
LB = RAIZ / "output" / "v17" / "lectura_bde"
GRUPOS = ("v15_v16_micro", "series_v8_v9_v12")
B4 = RAIZ / "docs" / "v17" / "mejor_estimacion.csv"
TOPE = 0.15
NORMA = {"si": "publicable", "sí": "publicable", "no_fiable": "no fiable", "no (no fiable)": "no fiable",
         "sin_medir": "con reserva (distorsión sin medir)", "con reserva (sin medir)": "con reserva (distorsión sin medir)"}


def cargar() -> pd.DataFrame:
    partes = []
    for g in GRUPOS:
        p = LB / g / "inferencia.csv"
        if p.exists():
            partes.append(pd.read_csv(p).assign(grupo=g))
    d = pd.concat(partes, ignore_index=True)
    d["regla"] = d.publicable.map(NORMA).fillna("no recalculado (ya tenía inferencia o es contable)")
    return d


def comprobar(d: pd.DataFrame) -> list[str]:
    t = pd.to_numeric(d.tamano_real, errors="coerce")
    mal = d[(t > TOPE) & (d.regla == "publicable")]
    return [f"{r.grupo}/{r.id_resultado}: tamaño real {r.tamano_real} > 15 % y marcado publicable" for r in mal.itertuples()]


def lectura(r) -> str:
    if r.regla != "publicable" and not r.regla.startswith("con reserva"):
        return "solo estimación puntual"
    if pd.isna(r.p_conv):
        return "sin p (ver nota)"
    ic = "" if pd.isna(r.ic95_lo) else f"; IC 95 % [{r.ic95_lo:.4g}; {r.ic95_hi:.4g}]"
    return f"p = {r.p_conv:.3g}{ic}"


def main() -> int:
    d = cargar()
    err = comprobar(d)
    if err:
        print("\n".join(err))
        return 1
    d["lectura_convencional"] = [lectura(r) for r in d.itertuples()]
    d["distorsion"] = [("sin medir" if pd.isna(t) else f"tamaño real {100 * float(t):.1f} % al 5 % nominal")
                       for t in pd.to_numeric(d.tamano_real, errors="coerce")]
    if B4.exists():
        b4 = pd.read_csv(B4)
        d = d.merge(b4[["pregunta", "canal", "mejor_estimacion", "confianza"]], on="pregunta", how="left")
    else:
        d["canal"] = d["mejor_estimacion"] = d["confianza"] = np.nan
    cols = ["version", "id_resultado", "pregunta", "canal", "estimacion_publicada", "unidad", "capa_proyecto", "lectura_convencional",
            "distorsion", "regla", "p_holm_pregunta", "p_bh_pregunta", "mejor_estimacion", "confianza", "grupo"]
    t = d[cols]
    t.to_csv(LB / "tabla_comparativa.csv", index=False)
    n = t.regla.value_counts().to_dict()
    L = ["# V17 · Fase 2 · Lectura convencional frente a las capas del proyecto", "",
         "Análisis a posteriori (V17). Generado por src/v17/f2_lectura_bde.py a partir de output/v17/lectura_bde/<grupo>/inferencia.csv. "
         "La lectura convencional es la inferencia que usaría un trabajo publicado. Se muestra junto a la distorsión medida en el Monte Carlo "
         "del repositorio y no cambia la capa del proyecto. Regla: si el tamaño real supera el 15 %, no se publica (solo estimación puntual).",
         "", "Recuento: " + "; ".join(f"{k}: {v}" for k, v in n.items()) + ".", "",
         "| Versión | Resultado | Pregunta | Estimación | Capa del proyecto | Lectura convencional | Distorsión | Regla | p Holm (pregunta) | "
         "Mejor estimación (B4) | Confianza |", "|---|---|---|---|---|---|---|---|---|---|---|"]
    for r in t.itertuples():
        est = "" if pd.isna(r.estimacion_publicada) else f"{r.estimacion_publicada:.4g} {'' if pd.isna(r.unidad) else r.unidad}"
        ph = "" if pd.isna(r.p_holm_pregunta) else f"{r.p_holm_pregunta:.3g}"
        me = "" if pd.isna(r.mejor_estimacion) else r.mejor_estimacion
        co = "" if pd.isna(r.confianza) else r.confianza
        L.append(f"| {r.version} | {r.id_resultado} | {r.pregunta} | {est} | {r.capa_proyecto} | {r.lectura_convencional} | {r.distorsion} | "
                 f"{r.regla} | {ph} | {me} | {co} |")
    (LB / "tabla_comparativa.md").write_text("\n".join(L) + "\n", encoding="utf-8")
    print(f"f2_lectura_bde V17: {len(t)} filas; {n}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
