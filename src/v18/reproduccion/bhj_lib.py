"""Herramientas shift-share de Borusyak, Hull y Jaravel (2022) en Python (V18, E3).

Traducción de ssaggregate.ado (v1.2.2, GPL-3.0, repositorio borusyak/shift-share) y de
la inferencia a nivel de sector de la aplicación ADH. Sin red, sin lectura de datos:
solo recibe arrays/DataFrames. Licencia del código original GPL-3.0; esta traducción
se distribuye con la misma licencia en lo que derive de él.

Funciones:
- residuos_ponderados: residuos de MCP de y sobre X (con constante) con pesos w.
- ssaggregate: agregación a nivel de shock (sector x periodo) de variables
  residualizadas por controles, con ponderación por cuota x peso y sector «faltante».
- iv_cluster: IV exactamente identificado (un regresor endógeno, un instrumento) con
  controles parcializados, ponderado y con varianza robusta por conglomerados.
- ar_ic_nulo_impuesto: intervalo de confianza por inversión de contraste con la
  hipótesis nula impuesta (ssiv_null_imposed.ado), por bisección.
"""
from __future__ import annotations

import numpy as np
import pandas as pd
from scipy import sparse, stats

SEED = 20261010
ALCANCE_TERRITORIAL = "sin lectura de datos"


def _como_matriz(X, n):
    if X is None:
        return np.ones((n, 1))
    X = np.asarray(X, dtype=float)
    if X.ndim == 1:
        X = X[:, None]
    return np.column_stack([np.ones(n), X])


def residuos_ponderados(Y, X, w):
    """Residuos de la regresión ponderada de cada columna de Y sobre [1, X].

    lstsq de mínima norma: los residuos son únicos aunque X sea colineal
    (Stata descarta las colineales; el ajuste es el mismo).
    """
    Y = np.asarray(Y, dtype=float)
    vector = Y.ndim == 1
    if vector:
        Y = Y[:, None]
    w = np.asarray(w, dtype=float)
    Z = _como_matriz(X, Y.shape[0])
    sw = np.sqrt(w)[:, None]
    coef, *_ = np.linalg.lstsq(Z * sw, Y * sw, rcond=None)
    R = Y - Z @ coef
    return R[:, 0] if vector else R


def ssaggregate(V, w, loc, periodo, cuotas, controles=None, addmissing=True,
                sector_faltante=0):
    """Agrega variables a nivel de localización a nivel de shock (sector x periodo).

    V: DataFrame (n_loc x k) de variables a agregar.
    w: pesos por localización (aw=). loc: id único de cada fila (localización-periodo).
    periodo: periodo de cada fila. cuotas: DataFrame largo con columnas
    ['loc', 'sector', 's'] (cuota del sector en la localización-periodo).
    controles: dict {sufijo: matriz de controles}; si None, sin controles
    (solo constante, como Stata: la constante se resta siempre).
    addmissing: añade el sector «faltante» con cuota 1 - sum(cuotas).
    Devuelve DataFrame con columnas sector, periodo, s_n (suma de cuota*peso
    normalizada a 1) y la media ponderada por cuota*peso de cada variable
    residualizada (nombres: variable + sufijo si hay >1 conjunto de controles).
    """
    V = pd.DataFrame(V).reset_index(drop=True)
    n = len(V)
    w = np.asarray(w, dtype=float)
    loc = np.asarray(loc)
    periodo = np.asarray(periodo)
    if controles is None:
        controles = {"": None}
    conjuntos = list(controles.items())
    multiple = len(conjuntos) > 1
    # Residualizar cada variable por cada conjunto de controles
    cols, nombres = [], []
    for sufijo, C in conjuntos:
        R = residuos_ponderados(V.to_numpy(float), C, w)
        for j, v in enumerate(V.columns):
            cols.append(R[:, j])
            nombres.append(f"{v}{sufijo if multiple else ''}")
    R = np.column_stack(cols)

    cuotas = cuotas[["loc", "sector", "s"]].copy()
    if addmissing:
        suma = cuotas.groupby("loc")["s"].sum().reindex(loc).fillna(0.0)
        falt = 1.0 - suma.to_numpy()
        falt[(falt > -1e-5) & (falt <= 0)] = 0.0
        cuotas = pd.concat(
            [cuotas, pd.DataFrame({"loc": loc, "sector": sector_faltante, "s": falt})],
            ignore_index=True)
    pos = pd.Series(np.arange(n), index=loc)
    i_loc = pos.reindex(cuotas["loc"]).to_numpy()
    if np.isnan(i_loc).any():
        raise ValueError("cuotas con localizaciones ausentes en V")
    i_loc = i_loc.astype(int)
    per = periodo[i_loc]
    clave = pd.MultiIndex.from_arrays([cuotas["sector"].to_numpy(), per])
    codigos, unicos = pd.factorize(clave, sort=True)
    sw = cuotas["s"].to_numpy() * w[i_loc]
    S = sparse.csr_matrix((sw, (codigos, i_loc)), shape=(len(unicos), n))
    den = np.asarray(S.sum(axis=1)).ravel()
    num = S @ R
    with np.errstate(invalid="ignore", divide="ignore"):
        medias = num / den[:, None]
    out = pd.DataFrame(medias, columns=nombres)
    out.insert(0, "s_n", den / den.sum())
    out.insert(0, "periodo", [u[1] for u in unicos])
    out.insert(0, "sector", [u[0] for u in unicos])
    return out


def _parcializar(M, controles, w):
    return residuos_ponderados(M, controles, w)


def iv_cluster(y, x, g, w, cluster, controles=None, ajuste="G"):
    """IV exactamente identificado ponderado con varianza por conglomerados.

    controles: matriz (se añade constante). ajuste: 'G' = G/(G-1) (sin dof de N),
    'stata_small' = G/(G-1)*(N-1)/(N-K), 'ninguno'.
    Devuelve dict(beta, se, F_primera_etapa, n, G).
    """
    y, x, g, w = (np.asarray(a, dtype=float) for a in (y, x, g, w))
    n = len(y)
    M = residuos_ponderados(np.column_stack([y, x, g]), controles, w)
    yt, xt, gt = M[:, 0], M[:, 1], M[:, 2]
    a = np.sum(w * gt * xt)
    beta = np.sum(w * gt * yt) / a
    u = yt - beta * xt
    cl = pd.factorize(np.asarray(cluster))[0]
    G = cl.max() + 1
    score = np.bincount(cl, weights=w * gt * u, minlength=G)
    var = np.sum(score ** 2) / a ** 2
    k = _como_matriz(controles, n).shape[1] + 1
    if ajuste == "G":
        var *= G / (G - 1)
    elif ajuste == "stata_small":
        var *= G / (G - 1) * (n - 1) / (n - k)
    # primera etapa: x sobre g (parcializado), mismo cluster
    pi = np.sum(w * gt * xt) / np.sum(w * gt * gt)
    v = xt - pi * gt
    sc1 = np.bincount(cl, weights=w * gt * v, minlength=G)
    var1 = np.sum(sc1 ** 2) / np.sum(w * gt * gt) ** 2
    if ajuste == "G":
        var1 *= G / (G - 1)
    elif ajuste == "stata_small":
        var1 *= G / (G - 1) * (n - 1) / (n - k)
    return {"beta": beta, "se": float(np.sqrt(var)), "F1": pi ** 2 / var1, "n": n, "G": int(G)}


def _p_nulo(y, x, g, w, cl, G, controles, b0, ajuste):
    M = residuos_ponderados(np.column_stack([y - b0 * x, g]), controles, w)
    e, gt = M[:, 0], M[:, 1]
    score = np.bincount(cl, weights=w * gt * e, minlength=G)
    m = score.sum()
    var = np.sum(score ** 2)
    if ajuste == "G":
        var *= G / (G - 1)
    return stats.chi2.sf(m ** 2 / var, 1)


def ar_ic_nulo_impuesto(y, x, g, w, cluster, controles=None, rango=(-4.0, 4.0),
                        alfa=0.05, tol=1e-3, maxit=30, ajuste="G"):
    """IC por inversión del contraste de exogeneidad de g con H0 impuesta (bisección).

    Traduce ssiv_null_imposed.ado. Devuelve (izquierda, derecha).
    """
    y, x, g, w = (np.asarray(a, dtype=float) for a in (y, x, g, w))
    cl = pd.factorize(np.asarray(cluster))[0]
    G = cl.max() + 1
    beta = iv_cluster(y, x, g, w, cluster, controles, ajuste)["beta"]
    p = lambda b: _p_nulo(y, x, g, w, cl, G, controles, b, ajuste)
    ext = []
    for lado in ("izq", "der"):
        l, r = (rango[0], beta) if lado == "izq" else (beta, rango[1])
        pl, pr = p(l), p(r)
        if not (min(pl, pr) <= alfa <= max(pl, pr)):
            raise ValueError("IC fuera del rango dado")
        it = 0
        while r - l > 2 * tol and it < maxit:
            mid = (l + r) / 2
            pm = p(mid)
            if min(pl, pm) <= alfa <= max(pl, pm):
                r, pr = mid, pm
            else:
                l, pl = mid, pm
            it += 1
        ext.append((l + r) / 2)
    return ext[0], ext[1]
