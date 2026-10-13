"""Factores comunes: PCA con seleccion Bai-Ng (2002) IC_p2 y modelo de factores dinamicos por maxima verosimilitud
(statsmodels DynamicFactorMQ, EM + filtro de Kalman), con cargas, varianza explicada por el factor y su evolucion por
ventanas moviles. Los factores son resumenes estadisticos: no tienen interpretacion causal ni estructural.
"""
from __future__ import annotations

import warnings

import numpy as np
import pandas as pd

SEED = 20261010


def estandariza(X):
    X = np.asarray(X, float)
    return (X - X.mean(0)) / X.std(0, ddof=0)


def bai_ng(X, kmax=8):
    """Criterios IC_p1, IC_p2, IC_p3 de Bai-Ng (2002) sobre datos estandarizados. Devuelve dict con k elegido por cada
    uno (k_ic2 es el recomendado) y la tabla de V(k)."""
    Z = estandariza(X)
    T, N = Z.shape
    kmax = min(kmax, N - 1, T - 1)
    s = np.linalg.svd(Z, compute_uv=False) ** 2
    tot = s.sum()
    V = np.array([(tot - s[:k].sum()) / (N * T) for k in range(0, kmax + 1)])
    k = np.arange(0, kmax + 1)
    g1 = (N + T) / (N * T) * np.log(N * T / (N + T))
    g2 = (N + T) / (N * T) * np.log(min(N, T))
    g3 = np.log(min(N, T)) / min(N, T)
    ic = {f"IC_p{i + 1}": np.log(V) + k * g for i, g in enumerate([g1, g2, g3])}
    out = {n: int(np.argmin(v)) for n, v in ic.items()}
    out["k_ic2"] = out["IC_p2"]
    out["tabla"] = pd.DataFrame({"k": k, "V": V, **ic})
    return out


def pca_factores(X, k):
    """PCA de datos estandarizados. Devuelve factores (T x k, normalizados a varianza 1), cargas (N x k), R2 de cada variable
    sobre los k factores (parte comun) y la parte de la varianza total explicada."""
    Z = estandariza(X)
    T, N = Z.shape
    U, s, Vt = np.linalg.svd(Z, full_matrices=False)
    F = U[:, :k] * np.sqrt(T)
    L = Vt[:k].T * s[:k] / np.sqrt(T)
    com = F @ L.T
    r2_var = (com ** 2).sum(0) / (Z ** 2).sum(0)
    return {"factores": F, "cargas": L, "r2_variable": r2_var, "var_explicada_total": float((s[:k] ** 2).sum() / (s ** 2).sum()),
            "var_explicada_por_factor": (s[:k] ** 2) / (s ** 2).sum()}


def dfm_ml(X, k=1, orden_factor=1, ar1_idio=True, maxiter=200, nombres=None, indice=None):
    """DFM por maxima verosimilitud (DynamicFactorMQ). X: DataFrame (indice temporal con frecuencia M o Q) o array (se asigna
    indice trimestral sintetico). Devuelve cargas, R2 de cada variable sobre cada factor (coeficientes de determinacion
    de statsmodels), factores suavizados, loglik y la varianza total explicada por la parte comun."""
    from statsmodels.tsa.statespace.dynamic_factor_mq import DynamicFactorMQ
    if not isinstance(X, pd.DataFrame):
        X = np.asarray(X, float)
        X = pd.DataFrame(X, columns=nombres or [f"x{i}" for i in range(X.shape[1])],
                         index=indice if indice is not None else pd.period_range("1900Q1", periods=X.shape[0], freq="Q"))
    Z = (X - X.mean()) / X.std(ddof=0)
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        mod = DynamicFactorMQ(Z, factors=k, factor_orders=orden_factor, idiosyncratic_ar1=ar1_idio)
        res = mod.fit(maxiter=maxiter, disp=False)
    cargas = pd.DataFrame({f"f{j}": [res.params[f"loading.{j}->{c}"] for c in Z.columns] for j in range(k)}, index=Z.columns)
    r2 = res.coefficients_of_determination
    r2 = pd.DataFrame(np.asarray(r2), index=Z.columns, columns=[f"f{j}" for j in range(k)])
    sm = np.asarray(res.states.smoothed)[:, :k]
    return {"cargas": cargas, "r2": r2, "r2_total_comun": float(r2.sum(axis=1).mean()), "factores": sm, "loglik": float(res.llf),
            "converge": bool(getattr(res, "mle_retvals", {}).get("converged", True)) if hasattr(res, "mle_retvals") else True}


def evolucion_ventanas(X, k=1, ventana=40, paso=4, metodo="pca"):
    """Varianza explicada por el(los) k primer(os) factor(es) en ventanas moviles. metodo 'pca' (rapido) o 'ml'
    (promedio de R2 de la parte comun por DFM-ML; costoso). Devuelve DataFrame inicio, fin, var_explicada."""
    X = np.asarray(X, float) if not isinstance(X, pd.DataFrame) else X
    n = len(X)
    rows = []
    for a in range(0, n - ventana + 1, paso):
        sub = X.iloc[a:a + ventana] if isinstance(X, pd.DataFrame) else X[a:a + ventana]
        if metodo == "pca":
            v = pca_factores(sub, k)["var_explicada_total"]
        else:
            v = dfm_ml(sub, k)["r2_total_comun"]
        rows.append({"inicio": a, "fin": a + ventana - 1, "var_explicada": float(v)})
    return pd.DataFrame(rows)
