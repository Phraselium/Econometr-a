"""Punto 10 · TOST de equivalencia: tamaño en el borde de la región de equivalencia (±Δ).

Δ = magnitud de referencia del punto 3; EE derivado del MDE80 de output/v16/potencia/potencia.csv (EE = MDE80/2,8).
Solo se lee esa tabla de potencia (no resultados). Uso: python tost.py [R]
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from src.v16.montecarlo import _comun_series as C  # noqa: E402

ALFA = 0.05


def razones_repositorio():
    p = pd.read_csv(C.RAIZ / "output" / "v16" / "potencia" / "potencia.csv")
    q = p[p.mde80_pct.notna() & p.ref_pct.notna()]
    r = (q.ref_pct / (q.mde80_pct / 2.8)).values
    return r


def tost_rechaza(rng, R, k, df, theta_rel):
    """k = Δ/EE; theta_rel = θ/Δ. EE con df grados de libertad (df=None: EE conocido)."""
    est = k * theta_rel + rng.standard_normal(R)           # EE = 1, Δ = k
    if df is None:
        se = np.ones(R); crit = stats.norm.ppf(1 - ALFA)
    else:
        se = np.sqrt(rng.chisquare(df, R) / df); crit = stats.t.ppf(1 - ALFA, df)
    return (((est + k) / se) > crit) & (((est - k) / se) < -crit)


def main(R=20000):
    razones = razones_repositorio()
    filas = []
    for df in (12, 37, None):
        for k in (0.5, 1, 1.5, 2, 2.5, 3, 3.5, 4, 5, 6, 8):
            rng = C.rng(8, int(k * 10) + (0 if df is None else df * 1000))
            tam = float(tost_rechaza(rng, R, k, df, 1.0).mean())
            tam2 = float(tost_rechaza(rng, R, k, df, -1.0).mean())
            pot0 = float(tost_rechaza(rng, R, k, df, 0.0).mean())
            pot_m = float(tost_rechaza(rng, R, k, df, 0.5).mean())
            v = C.veredicto(tam, R)
            filas.append({"df": "inf" if df is None else df, "delta_sobre_EE": k, "tamano_borde": tam, "tamano_borde_neg": tam2,
                          "potencia_theta0": pot0, "potencia_theta_mitad": pot_m, "apto": v["veredicto"] == "APTO"})
    t = pd.DataFrame(filas)
    # mínima razón Δ/EE con tamaño en [0,04; 0,06] para df=12 (clusters: 13 provincias) y df=37 (N=38)
    umbral = {}
    for df in (12, 37, "inf"):
        s = t[(t.df == df) & t.apto]
        umbral[str(df)] = float(s.delta_sobre_EE.min()) if len(s) else None
    dentro = {str(df): float(np.mean([bool(t[(t.df == df) & (t.delta_sobre_EE == k)].apto.iloc[0])
                                      for k in [min([0.5, 1, 1.5, 2, 2.5, 3, 3.5, 4, 5, 6, 8], key=lambda z: abs(z - x)) for x in razones]]))
              for df in (12, 37, "inf")}
    # tamaño aproximado por razón del repositorio (interpolación al k más cercano de la rejilla)
    tam_repo = {str(df): [float(t[(t.df == df)].iloc[(t[(t.df == df)].delta_sobre_EE - x).abs().argmin()].tamano_borde) for x in razones] for df in (12, 37, "inf")}
    n0 = {df: int(sum(1 for z in v if z < 0.04)) for df, v in tam_repo.items()}
    fallos = [f"tamaño en el borde < 0,04 (hasta 0,0) para Δ/EE pequeña: {n0['12']} de {len(razones)} diseños del repositorio con tamaño < 0,04 (df=12)",
              f"APTO solo si Δ/EE >= {umbral['12']} (df=12), {umbral['37']} (df=37)"]
    glob = {"veredicto": "NO APTO como regla general; APTO condicionado a Δ/EE >= umbral (en otro caso «no concluyente»)", "fallos": fallos}
    r = C.resultado_base("tost", "Nulo informativo (adenda punto 10)", {"R": R, "razones_repositorio": len(razones)}, "TOST (dos pruebas t unilaterales al 5 %)")
    r["estimacion"] = {"umbral_delta_sobre_EE_apto": umbral, "razon_repositorio_mediana": float(np.median(razones)),
                       "razon_repositorio_min_max": [float(razones.min()), float(razones.max())],
                       "tamano_borde_df12_a_razon_mediana": float(np.median(tam_repo["12"])), "cobertura": "no aplica (prueba)"}
    r["ic95"] = C.ic_binomial(0.05, R)
    r["diagnosticos"] = {"veredicto": glob, "razones_repositorio": [round(float(x), 2) for x in razones], "tamano_por_razon_df12": tam_repo["12"],
                         "proporcion_diseños_apta": dentro}
    r["notas"] = ["Referencia del repositorio: EE = MDE80/2,8 (potencia.csv, 15 filas con magnitud de referencia); Δ = ref_pct.",
                  "La adenda no nombra alternativa: sin magnitud o con Δ/EE bajo el umbral, el resultado es «no concluyente»."]
    md = (f"## Resultados (R={R} por celda)\n\n" + t.round(4).to_markdown(index=False)
          + f"\n\nRazones Δ/EE del repositorio: mediana {np.median(razones):.2f}, rango [{razones.min():.2f}; {razones.max():.2f}].\n\n"
          f"**Veredicto: {glob['veredicto']}**. {'; '.join(fallos)}\n")
    C.escribir_salidas("tost", r, t, md)
    print(umbral, dentro, np.round(razones, 2), glob)


if __name__ == "__main__":
    main(*[int(x) for x in sys.argv[1:]])
