"""V7.2-4 · Reverificación del GSADF NACIONAL de v5 (R1B, BK-023) con el MISMO método y la MISMA semilla.

Recalcula las 14 series nacionales (familias fundamentales, referencia y sensibilidad) con las funciones de src/v5/r1b_gsadf.py
(bootstrap recursivo AR(p) estimado, G.NBOOT réplicas: 4.999 desde V16 B-4, 499 hasta la 1.0; SEED + 500 + k en el mismo orden) y el BH por familia, y compara con
output/v5/R1B/tablas/gsadf_corregido.csv (versionado). No modifica output/v5. Escribe output/v7_2/gsadf/reverificacion.csv.
Lee el panel nacional por src/holdout.py (load_full, como r1b_gsadf; el sellado v2 ya está evaluado). Capa C4.
"""
from __future__ import annotations

import os

for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS"):
    os.environ.setdefault(_v, "1")
import sys  # noqa: E402
from pathlib import Path  # noqa: E402

import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402

RAIZ = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(RAIZ / "src"))
sys.path.insert(0, str(RAIZ / "src" / "v5"))
import holdout  # noqa: E402
import r1b_gsadf as G  # noqa: E402

OUT = RAIZ / "output" / "v7_2" / "gsadf"
# el módulo de v5 crea un Registry sobre output/v5/R1B/registro_gsadf.csv que se escribe al salir: se redirige aquí
# (no se toca output/v5) y se registran las 14 especificaciones reverificadas.
G.REG.path = OUT / "registro_reverificacion.csv"


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    nq = holdout.load_full("nacional_q_v2", "V7.2-gsadf-reverifica")
    pan = pd.read_csv(RAIZ / "data/processed/panel_ccaa_q.csv")
    S, _ = G.construir_series(nq, pan)
    ver = pd.read_csv(RAIZ / "output/v5/R1B/tablas/gsadf_corregido.csv")
    filas = []
    for k, (terr, fam, med, s) in enumerate(S):
        if fam == "ccaa":
            continue
        r = G.gsadf_corr(s.to_numpy(), G.NBOOT, G.SEED + 500 + k)
        filas.append(dict(familia=fam, medida=med, T=r["T"], gsadf=r["gsadf"], cv95=r["cv95"], p=r["p"]))
    df = pd.DataFrame(filas)
    df["p_bh"] = np.nan
    for f in df.familia.unique():
        m = df.familia == f
        df.loc[m, "p_bh"] = G.bh(df.p[m].to_numpy())
    v = ver[ver.familia != "ccaa"].reset_index(drop=True)
    assert list(v.medida) == list(df.medida), "orden de series distinto del versionado"
    df["gsadf_v5"], df["cv95_v5"], df["p_v5"], df["p_bh_v5"] = v.gsadf, v.cv95_corr, v.p_corr, v.p_bh
    df["coincide"] = (np.isclose(df.gsadf, df.gsadf_v5, atol=1e-9) & np.isclose(df.cv95, df.cv95_v5, atol=1e-9)
                      & np.isclose(df.p, df.p_v5) & np.isclose(df.p_bh, df.p_bh_v5))
    df["exuberancia_bh05"] = df.p_bh < 0.05
    for r in df.itertuples():
        G.REG.log("gsadf-reverifica", f"gsadf_Nacional_{r.medida}", "GSADF ADF(1); vc bootstrap AR(p) estimado (v5 R1B, reverificación)", "2007Q1", "2026Q2",
                  int(r.T), np.nan, np.nan, np.nan, coef_interes=r.gsadf, p_interes=r.p, notas=f"BH={r.p_bh:.3f}; coincide={bool(r.coincide)}")
    df.round(6).to_csv(OUT / "reverificacion.csv", index=False)
    print(df[["familia", "medida", "gsadf", "cv95", "p", "p_bh", "coincide"]].to_string())
    print(f"coinciden {int(df.coincide.sum())} de {len(df)}")
    return 0 if df.coincide.all() else 1


if __name__ == "__main__":
    sys.exit(main())
