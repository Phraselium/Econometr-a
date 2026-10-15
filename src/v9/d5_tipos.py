"""V9 F3 · D5 shocks de política monetaria del BCE × exposición a hipotecas a tipo variable (EXPLORATORIO, C4).
Pre-registro: docs/v9/hipotesis.md (D5) y addendum A1.8.

y_{i,t+h} - y_{i,t-1} = α_i + δ_t + β_h (shock_t × e_i) + Σ_{l=1..4} γ_l Δy_{i,t-l} + ε,  h = 0..12 trimestres.
y = log precio residencial nominal (BIS, índice 2010 = 100) o log IPCA de alquileres (media trimestral).
shock_t = suma trimestral de MP_median (Jarociński y Karadi, mensual; no redistribuible); e_i = cuota media de nuevos
préstamos a tipo variable o fijación ≤1 año en 2003-2007 (BCE RAI), estandarizada. Muestra 2008T1-2025T3.
Errores de Driscoll-Kraay (linearmodels, kernel, ancho de banda h + 4). Robustez: shock CBI; 2008-2019; sin España.
Salidas: output/v9/d5/{tabla_d5.csv, proyeccion_local.csv, resultado.json, registry.csv, fig_d5.png}.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import matplotlib
import numpy as np
import pandas as pd
from linearmodels.panel import PanelOLS

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import paneles as P  # noqa: E402
from econ_utils import Registry  # noqa: E402

OUT = P.RAIZ / "output" / "v9" / "d5"
REG = Registry(OUT / "registry.csv")
H_MAX = 12


def datos() -> tuple[pd.DataFrame, pd.Series, pd.DataFrame]:
    eu = P.europa()
    jk = eu["jk"].copy()
    jk["q"] = pd.PeriodIndex(jk.periodo, freq="M").asfreq("Q").astype(str)
    shocks = jk.groupby("q")[["MP_median", "CBI_median"]].sum()
    rai = eu["rai"]
    expo = rai[(rai.periodo >= "2003-01") & (rai.periodo <= "2007-12")].groupby("pais").valor.mean()
    bis = eu["bis"].pivot_table(index="q", columns="territorio", values="valor")
    hicp = eu["hicp"].copy()
    hicp["q"] = pd.PeriodIndex(hicp.periodo, freq="M").asfreq("Q").astype(str)
    hicp = hicp.groupby(["q", "pais"]).valor.mean().unstack()
    paises = [p for p in P.ZONA_EURO if p in bis.columns and p in expo.index]
    y = pd.concat({"precio": np.log(bis[paises]), "alquiler": np.log(hicp.reindex(columns=paises))}, axis=1)
    return y, expo.loc[paises], shocks


def lp(y: pd.DataFrame, e: pd.Series, shock: pd.Series, h: int, q0: str, q1: str) -> dict:
    filas = []
    qs = list(y.index)
    for p in y.columns:
        s = y[p]
        dy = s.diff()
        for i, q in enumerate(qs):
            if not (q0 <= q <= q1) or i + h >= len(qs) or i < 5:
                continue
            fila = {"pais": p, "q": q, "y": s.iloc[i + h] - s.iloc[i - 1], "x": shock.get(q, np.nan) * e[p]}
            for lag in range(1, 5):
                fila[f"l{lag}"] = dy.iloc[i - lag]
            filas.append(fila)
    d = pd.DataFrame(filas).dropna()
    d["t"] = pd.PeriodIndex(d.q, freq="Q").to_timestamp()
    d = d.set_index(["pais", "t"])
    m = PanelOLS(d.y, d[["x", "l1", "l2", "l3", "l4"]], entity_effects=True, time_effects=True)
    r = m.fit(cov_type="kernel", kernel="bartlett", bandwidth=h + 4)
    return {"beta": float(r.params["x"]), "se": float(r.std_errors["x"]), "p": float(r.pvalues["x"]), "N": int(r.nobs),
            "paises": int(d.index.get_level_values(0).nunique())}


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    y, expo, shocks = datos()
    e = (expo - expo.mean()) / expo.std()
    filas, tabla = [], []
    especs = [("principal", "MP_median", "2008Q1", "2025Q3", None),
              ("shock CBI (información del banco central)", "CBI_median", "2008Q1", "2025Q3", None),
              ("muestra 2008-2019", "MP_median", "2008Q1", "2019Q4", None),
              ("sin España", "MP_median", "2008Q1", "2025Q3", "ES")]
    for res_nom in ("precio", "alquiler"):
        for etiqueta, shk, q0, q1, excl in especs:
            yy = y[res_nom]
            if excl:
                yy = yy.drop(columns=excl)
            yy = yy.dropna(how="all", axis=1)
            for h in range(H_MAX + 1):
                r = lp(yy, e, shocks[shk], h, q0, q1)
                filas.append({"resultado": res_nom, "especificacion": etiqueta, "h": h, **r})
                REG.log("v9-D5", f"{res_nom}|{etiqueta}|h{h}", "LP: Δ_h log y ~ shock×expo + 4 retardos + FE país y trimestre",
                        q0, q1, r["N"], np.nan, np.nan, np.nan, coef_interes=r["beta"], p_interes=r["p"], notas="exploratorio")
    L = pd.DataFrame(filas)
    L.to_csv(OUT / "proyeccion_local.csv", index=False, float_format="%.5f")
    for _, rr in L[L.h.isin([4, 8])].iterrows():
        tabla.append({"diseno": "D5", "hipotesis": "exploratoria", "resultado": f"Δ log {rr.resultado} (h = {rr.h})",
                      "especificacion": rr.especificacion, "beta": rr.beta, "se": rr.se, "ic95_lo": rr.beta - 1.96 * rr.se,
                      "ic95_hi": rr.beta + 1.96 * rr.se, "p": rr.p, "N_unidades": rr.paises, "N_obs": rr.N, "confirmatoria": False})
    T = pd.DataFrame(tabla)
    T.to_csv(OUT / "tabla_d5.csv", index=False, float_format="%.5f")
    fig, ax = plt.subplots(1, 2, figsize=(10, 3.6))
    for j, res_nom in enumerate(("precio", "alquiler")):
        s = L[(L.resultado == res_nom) & (L.especificacion == "principal")]
        ax[j].plot(s.h, s.beta, "o-", ms=3)
        ax[j].fill_between(s.h, s.beta - 1.96 * s.se, s.beta + 1.96 * s.se, alpha=0.2)
        ax[j].axhline(0, color="grey", lw=0.8)
        ax[j].set_xlabel("trimestres tras el shock")
        ax[j].set_title(f"Δ log {res_nom}: shock MP × 1 DE de exposición", fontsize=9)
    fig.suptitle("D5 (exploratorio, C4): proyecciones locales, 18 países de la zona euro, IC 95 % Driscoll-Kraay. "
                 "Fuente: BIS, Eurostat, BCE, Jarociński-Karadi; elaboración propia", fontsize=7)
    fig.tight_layout()
    fig.savefig(OUT / "fig_d5.png", dpi=130)
    plt.close(fig)
    pr = T[T.especificacion == "principal"]
    res = {"rama": "v9/d5", "pregunta": "¿Es mayor la variación de precios y alquileres asociada a los shocks del BCE en países con más hipotecas a tipo variable?",
           "capa": "C4 (exploratorio; sin potencia)", "datos": "BIS RPP, Eurostat IPCA alquiler, BCE RAI, shocks JK",
           "N": int(pr.N_unidades.max()), "metodo": "Proyecciones locales en panel con efectos fijos de país y trimestre; Driscoll-Kraay",
           "estimacion": pr[["resultado", "beta"]].to_dict("records"), "ic95": pr[["ic95_lo", "ic95_hi"]].values.tolist(),
           "p_ajustado": "BH exploratorio en output/v9/f3/tabla_capas.csv", "nivel_evidencia": "EXPLORATORIO",
           "diagnosticos": {"exposicion_2003_2007": expo.round(2).to_dict()},
           "fuera_muestra": {"modelo": None, "rmse": None, "dm_vs_ar4": None},
           "notas": "Shocks JK no redistribuibles (make datos_terceros); solo se publican coeficientes."}
    (OUT / "resultado.json").write_text(json.dumps(res, ensure_ascii=False, indent=1, default=float), encoding="utf-8")
    REG.flush()
    with pd.option_context("display.width", 250):
        print(T.to_string())
    return 0


if __name__ == "__main__":
    sys.exit(main())
