"""Analisis de multiverso: rejilla de especificaciones OLS/HAC, registro de TODAS en el Registry y resumen por variable.

No es inferencia causal: resume la sensibilidad de beta a decisiones razonables del analista. Todas las
especificaciones corridas se registran (incluidas las no significativas) en src/econ_utils.Registry; tambien las
FALLIDAS (muestra insuficiente o error de ajuste), con su motivo en `notas` ("FALLIDA: ...") y en specs.attrs["fallidas"].
Tope por defecto: 50.000 especificaciones (pre-registro, seccion 9).
"""
from __future__ import annotations

import itertools
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import statsmodels.api as sm
from statsmodels.stats.multitest import multipletests

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "src"))
SEED = 20261010


def _rejilla(opciones):
    claves = list(opciones)
    return [dict(zip(claves, v)) for v in itertools.product(*[opciones[k] for k in claves])]


def correr_multiverso(df, opciones, registry=None, fase="v8_multiverso", max_specs=50_000, seed=SEED, alpha=0.05):
    """Corre la rejilla `opciones` = {"dep": [...], "x": [...], "controles": [[...],...], "muestra": [(ini,fin)|None,...],
    "hac": [lags,...]} (claves ausentes toman un valor por defecto). Devuelve (specs DataFrame, truncado:bool, n_rejilla).

    Si la rejilla excede `max_specs` (50.000 por defecto), se muestrea sin reemplazo de forma determinista (seed) y se
    declara truncado. Las especificaciones fallidas no entran en `specs` pero se registran en el Registry (notas
    "FALLIDA: motivo") y se devuelven en specs.attrs["fallidas"] (DataFrame id, dep, x, motivo).
    """
    op = {"dep": opciones["dep"], "x": opciones["x"], "controles": opciones.get("controles", [[]]),
          "muestra": opciones.get("muestra", [None]), "hac": opciones.get("hac", [4])}
    grid = _rejilla(op)
    n_rej = len(grid)
    truncado = n_rej > max_specs
    if truncado:
        idx = np.sort(np.random.default_rng(seed).choice(n_rej, max_specs, replace=False))
        grid = [grid[i] for i in idx]
    filas = []
    fallidas = []

    def fallo(mid, g, form, motivo, ini="", fin="", n=0):
        fallidas.append({"id": mid, "dep": g["dep"], "x": g["x"], "controles": "+".join(g["controles"]),
                         "muestra": str(g["muestra"]), "hac": g["hac"], "motivo": motivo})
        if registry is not None:
            registry.log(fase, mid, form, ini, fin, n, np.nan, np.nan, np.nan, notas=f"FALLIDA: {motivo};x={g['x']};hac={g['hac']}")

    for i, g in enumerate(grid):
        d = df if g["muestra"] is None else df.loc[g["muestra"][0]:g["muestra"][1]]
        cols = [g["dep"], g["x"]] + list(g["controles"])
        d = d.dropna(subset=list(dict.fromkeys(cols)))
        Xc = [g["x"]] + [c for c in g["controles"] if c != g["x"]]
        mid = f"mv_{i:05d}"
        form = f"{g['dep']} ~ {' + '.join(Xc)}"
        if len(d) < len(Xc) + 8:
            fallo(mid, g, form, f"muestra insuficiente (n={len(d)} < {len(Xc) + 8})", n=len(d))
            continue
        X = sm.add_constant(d[Xc].astype(float).values, has_constant="add")
        try:
            r = sm.OLS(d[g["dep"]].astype(float).values, X).fit(cov_type="HAC", cov_kwds={"maxlags": int(g["hac"])})
        except Exception as ex:  # noqa: BLE001
            fallo(mid, g, form, f"error de ajuste ({type(ex).__name__}: {str(ex)[:80]})", n=len(d))
            continue
        ini, fin = d.index[0], d.index[-1]
        if registry is not None:
            registry.log(fase, mid, form, ini, fin, int(r.nobs), float(r.rsquared_adj), float(r.aic), float(r.bic),
                         coef_interes=float(r.params[1]), p_interes=float(r.pvalues[1]),
                         notas=f"x={g['x']};hac={g['hac']};ncontroles={len(g['controles'])}")
        filas.append({"id": mid, "dep": g["dep"], "x": g["x"], "n_controles": len(g["controles"]),
                      "controles": "+".join(g["controles"]), "muestra": str(g["muestra"]), "hac": g["hac"], "n": int(r.nobs),
                      "beta": float(r.params[1]), "se": float(r.bse[1]), "p": float(r.pvalues[1])})
    specs = pd.DataFrame(filas)
    if len(specs):
        # BH sobre TODAS las especificaciones corridas (conservador: familia completa)
        specs["p_bh"] = multipletests(specs["p"].values, method="fdr_bh")[1]
    specs.attrs.update({"truncado": truncado, "n_rejilla": n_rej, "alpha": alpha, "fallidas": pd.DataFrame(fallidas)})
    return specs, truncado, n_rej


def resumen_multiverso(specs, alpha=0.05, lo=0.025, hi=0.975):
    """Por variable de interes (y dependiente): mediana de beta, intervalo [lo,hi] de percentiles, % mismo signo que la
    mediana, % significativo al 5% sin ajuste y % significativo tras BH con el mismo signo que la mediana."""
    out = []
    for (dep, x), g in specs.groupby(["dep", "x"]):
        med = g["beta"].median()
        sg = np.sign(med)
        out.append({"dep": dep, "x": x, "n_specs": len(g), "mediana": med, "p_lo": g["beta"].quantile(lo),
                    "p_hi": g["beta"].quantile(hi), "pct_mismo_signo": float((np.sign(g["beta"]) == sg).mean()),
                    "pct_sig_raw": float((g["p"] < alpha).mean()),
                    "pct_sig_bh": float(((g["p_bh"] < alpha) & (np.sign(g["beta"]) == sg)).mean())})
    return pd.DataFrame(out)
