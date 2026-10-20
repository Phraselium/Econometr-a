"""V18 · inferencia shift-share a nivel de choque (BHJ): envoltorio de bhj_lib para el Monte Carlo.

Sin lectura de datos: recibe arrays. Usa src/v18/reproduccion/bhj_lib.py (ssaggregate, iv_cluster,
ar_ic_nulo_impuesto) sin modificarlo.
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd

SEED = 20261010
ALCANCE_TERRITORIAL = "sin lectura de datos"
RAIZ = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(RAIZ / "src" / "v18" / "reproduccion"))
import bhj_lib  # noqa: E402


def hhi(pesos) -> float:
    """HHI de los pesos de los choques (se normalizan a suma 1)."""
    p = np.asarray(pesos, dtype=float)
    p = p / p.sum()
    return float(np.sum(p ** 2))


def pesos_con_hhi(K: int, objetivo: float, piso: float = 0.002) -> np.ndarray:
    """Pesos omega_k proporcionales a r^k + piso (suma 1) con HHI = objetivo (bisección en r).

    El piso evita choques de peso nulo (r pequeño). Exige 1/K <= objetivo < 1.
    """
    if objetivo < 1.0 / K - 1e-12:
        raise ValueError("HHI inferior al mínimo 1/K")
    k = np.arange(K)
    a, b = 1e-6, 1.0   # r=1: pesos iguales (HHI mínimo); r pequeño: concentración
    for _ in range(100):
        r = (a + b) / 2
        if hhi(r ** k + piso) > objetivo:
            a = r   # demasiado concentrado: acercar r a 1
        else:
            b = r
    w = ((a + b) / 2) ** k + piso
    return w / w.sum()


def bhj_choque(y, x, w_loc, cuotas, g_choque, ar=True, rango=(-10.0, 10.0)):
    """IV shift-share agregado a nivel de choque (un periodo, sector = choque).

    y, x: resultado y regresor por localización; w_loc: pesos (aw); cuotas: array (L, K) de cuotas
    (suma <= 1: el resto es el sector «faltante», con choque 0); g_choque: shocks (K,).
    Control a nivel de localización: la suma de cuotas (BHJ, cuotas incompletas).
    Devuelve dict(beta, se, F1, ic_ar=(izq, der) o None, inf_ar, n_choques, inv_hhi).
    """
    y = np.asarray(y, float)
    L, K = cuotas.shape
    loc = np.arange(L)
    filas = pd.DataFrame({"loc": np.repeat(loc, K), "sector": np.tile(np.arange(1, K + 1), L),
                          "s": cuotas.ravel()})
    z_loc = cuotas @ np.asarray(g_choque, float)
    V = pd.DataFrame({"y": y, "x": np.asarray(x, float), "z": z_loc})
    ag = bhj_lib.ssaggregate(V, w_loc, loc, np.zeros(L, dtype=int), filas,
                             controles={"": cuotas.sum(1)}, addmissing=True, sector_faltante=0)
    sec = ag["sector"].to_numpy()
    g = np.concatenate([[0.0], np.asarray(g_choque, float)])[sec]
    args = (ag["y"].to_numpy(), ag["x"].to_numpy(), g, ag["s_n"].to_numpy(), sec)
    est = bhj_lib.iv_cluster(*args, controles=None, ajuste="G")
    out = {"beta": est["beta"], "se": est["se"], "F1": est["F1"], "n_choques": K,
           "inv_hhi": 1.0 / hhi(ag.loc[ag["sector"] != 0, "s_n"].to_numpy()), "ic_ar": None, "inf_ar": False}
    if ar:
        try:
            out["ic_ar"] = bhj_lib.ar_ic_nulo_impuesto(*args, controles=None, rango=rango, ajuste="G")
        except ValueError:
            out["inf_ar"] = True   # IC fuera del rango: se trata como no acotado
    return out
