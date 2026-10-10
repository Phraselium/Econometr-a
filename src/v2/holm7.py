"""Holm sobre las 7 hipótesis confirmatorias (BS; criterio uniforme de docs/v2/decisiones.md).

p de cada hipótesis = la decisión pre-registrada: conjunciones por intersección-unión (máximo de los p);
hipótesis con evaluación sellada: el p conjunto incluye la evaluación sellada (máximo).
TODOS los p se LEEN de los ficheros versionados de cada rama (no se reestima nada). La versión anterior
de este script traía transcritos los p dentro de muestra de H1-H5; ahora se leen y se contrastan con
esos valores transcritos (output/v2/BS/holm7_verificacion.csv). Si difieren, manda el del fichero.
"""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd

R = Path(__file__).resolve().parents[2]
O = R / "output" / "v2"

# Valores que traía transcritos la versión previa del script (solo para auditar; NO se usan en el cálculo)
TRANSCRITOS = {"H1": 0.85, "H2": 0.0018, "H3": 0.029, "H4": 0.046, "H5": 0.97}


def j(rel: str):
    return json.loads((O / rel).read_text())


def leer_p() -> list[dict]:
    ba, bv, bi, bo, bp, bm = (j(f"{r}/resultado.json") for r in ("BA", "BV", "BI", "BO", "BP", "BM"))
    h1s = j("BA/h1_sellado.json")["resultado"]["todas"]
    h2s = j("BV/h2_sellado.json")["resultado"]["PRINCIPAL_todas"]
    h6s = j("BP/h6_sellado.json")["resultado"]["DECISION"]
    h7s = j("BM/h7_sellado.json")["resultado"]
    return [
        dict(hipotesis="H1", rama="BA", p_dentro_muestra=ba["diagnosticos"]["p_H1_IUT_unilateral"],
             p_sellado=h1s["p_vs_AR4"],
             fuente="BA/resultado.json (diagnosticos.p_H1_IUT_unilateral, IUT unilateral +); BA/h1_sellado.json (resultado.todas.p_vs_AR4)"),
        dict(hipotesis="H2", rama="BV", p_dentro_muestra=bv["diagnosticos"]["p_interseccion_union_H2"],
             p_sellado=h2s["p_vs_AR4"],
             fuente="BV/resultado.json (diagnosticos.p_interseccion_union_H2); BV/h2_sellado.json (resultado.PRINCIPAL_todas.p_vs_AR4)"),
        dict(hipotesis="H3", rama="BI", p_dentro_muestra=bi["p_ajustado"]["p_IUT_H3_sin_ajustar_wcb"],
             p_sellado=np.nan, fuente="BI/resultado.json (p_ajustado.p_IUT_H3_sin_ajustar_wcb); coincide con BI/h3_principal.csv"),
        dict(hipotesis="H4", rama="BO", p_dentro_muestra=bo["p_ajustado"]["p_IUT_sin_ajustar"],
             p_sellado=np.nan, fuente="BO/resultado.json (p_ajustado.p_IUT_sin_ajustar); coincide con BO/h4_principal.csv"),
        dict(hipotesis="H5", rama="BP", p_dentro_muestra=bp["diagnosticos"]["p_permutacion_una_cola_post1"],
             p_sellado=np.nan, fuente="BP/resultado.json (diagnosticos.p_permutacion_una_cola_post1: cola del signo esperado, −)"),
        dict(hipotesis="H6", rama="BP", p_dentro_muestra=np.nan, p_sellado=h6s["p_perm_bilateral"],
             fuente="BP/h6_sellado.json (resultado.DECISION.p_perm_bilateral; regla pre-registrada bilateral)"),
        dict(hipotesis="H7", rama="BM", p_dentro_muestra=np.nan,
             p_sellado=min(h7s[k]["p_IUT_Holm"] for k in ("A", "B", "C")),
             fuente="BM/h7_sellado.json (mín. de p_IUT_Holm m=3 sobre A, B, C)"),
    ]


def holm(p: np.ndarray) -> np.ndarray:
    o = np.argsort(p, kind="stable")
    m = len(p)
    adj = np.empty(m)
    run = 0.0
    for rank, i in enumerate(o):
        run = max(run, min(1.0, (m - rank) * p[i]))
        adj[i] = run
    return adj


def calcular(destino: Path | None = None) -> pd.DataFrame:
    destino = destino or (O / "BS")
    destino.mkdir(parents=True, exist_ok=True)
    df = pd.DataFrame(leer_p())
    df["p_hipotesis"] = df[["p_dentro_muestra", "p_sellado"]].max(axis=1, skipna=True)
    df["p_holm7"] = holm(df["p_hipotesis"].to_numpy())
    df["supera_holm7_5pct"] = df["p_holm7"] < 0.05
    df = df.sort_values(["p_hipotesis", "hipotesis"], kind="stable").reset_index(drop=True)
    df = df[["hipotesis", "rama", "p_dentro_muestra", "p_sellado", "fuente", "p_hipotesis", "p_holm7", "supera_holm7_5pct"]]
    df.to_csv(destino / "holm7.csv", index=False)
    # verificación frente a los valores transcritos previamente
    v = []
    for h, t in TRANSCRITOS.items():
        f = float(df.loc[df.hipotesis == h, "p_dentro_muestra"].iloc[0])
        v.append(dict(hipotesis=h, p_transcrito_previo=t, p_fichero=f, diferencia=f - t,
                      coincide_redondeo=abs(f - t) <= 0.5 * 10 ** -(len(str(t).split(".")[1])) + 1e-12,
                      usado="fichero"))
    pd.DataFrame(v).to_csv(destino / "holm7_verificacion.csv", index=False)
    return df


if __name__ == "__main__":
    print(calcular().to_string(index=False))
