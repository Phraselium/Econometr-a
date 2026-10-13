"""Prueba de permutacion de fechas de corte.

Dado un estadistico por tramos (p. ej. diferencia de coeficientes entre periodos) y unas fechas de corte
OBSERVADAS fijadas a priori, compara con conjuntos de fechas aleatorias con el mismo numero de tramos y longitudes
minimas. p-valor exacto: enumeracion completa si el numero de conjuntos validos <= n_perm; si no, Monte Carlo
con correccion (1+#)/(1+B), que es un p-valor exacto de permutacion (valido en muestra finita).
Si las fechas observadas se eligieron mirando los datos, el estadistico debe ser el SUP sobre la busqueda.
"""
from __future__ import annotations

import itertools
import math

import numpy as np

SEED = 20261010


def n_conjuntos(n, n_tramos, min_len):
    """Numero de conjuntos validos de cortes: C(n - m*(T) + T - 1, T - 1) con T = n_tramos."""
    holgura = n - n_tramos * min_len
    if holgura < 0:
        return 0
    return math.comb(holgura + n_tramos - 1, n_tramos - 1)


def _cortes_desde_longitudes(longs):
    return tuple(int(c) for c in np.cumsum(longs)[:-1])


def enumerar(n, n_tramos, min_len):
    holgura = n - n_tramos * min_len
    for c in itertools.combinations_with_replacement(range(holgura + 1), n_tramos - 1):
        # reparto de holgura: incrementos entre cortes
        extra = np.diff(np.r_[0, c, holgura])
        yield _cortes_desde_longitudes(min_len + extra)


def muestrear(n, n_tramos, min_len, rng):
    """Conjunto de cortes uniforme sobre los validos (estrellas y barras)."""
    holgura = n - n_tramos * min_len
    # uniformidad: multiconjunto = combinacion sin repeticion de holgura+n_tramos-1 elementos
    comb = np.sort(rng.choice(holgura + n_tramos - 1, n_tramos - 1, replace=False))
    c = comb - np.arange(n_tramos - 1)
    extra = np.diff(np.r_[0, c, holgura])
    return _cortes_desde_longitudes(min_len + extra)


def permutacion_cortes(stat_fn, n, cortes_obs, min_len, n_perm=2000, seed=SEED, dos_colas=False):
    """p-valor de permutacion de fechas. stat_fn(cortes:tuple)->float (mayor = mas evidencia de ruptura).

    cortes_obs: indices de inicio de cada tramo posterior al primero (p. ej. (60,) = tramos [0,60) y [60,n)).
    """
    cortes_obs = tuple(int(c) for c in cortes_obs)
    T = len(cortes_obs) + 1
    s_obs = float(stat_fn(cortes_obs))
    tot = n_conjuntos(n, T, min_len)
    if tot <= n_perm:
        stats = np.array([stat_fn(c) for c in enumerar(n, T, min_len)])
        p = float(np.mean(stats >= s_obs - 1e-12))
        modo = "enumeracion_exacta"
        B = len(stats)
    else:
        rng = np.random.default_rng(seed)
        stats = np.array([stat_fn(muestrear(n, T, min_len, rng)) for _ in range(n_perm)])
        p = float((1 + np.sum(stats >= s_obs - 1e-12)) / (1 + n_perm))
        modo = "monte_carlo_exacto"
        B = n_perm
    return {"stat_obs": s_obs, "p": p, "modo": modo, "n_conjuntos": tot, "n_perm": B,
            "cuantil95_perm": float(np.quantile(stats, 0.95)), "stats": stats}


def stat_dif_coef(y, X, col=0, tramos_comp=(0, -1)):
    """Fabrica de estadistico: |beta_col(tramo b) - beta_col(tramo a)| con OLS por tramos. X ya incluye constante si se desea."""
    y = np.asarray(y, float)
    X = np.asarray(X, float)
    n = len(y)

    def f(cortes):
        lim = (0,) + tuple(cortes) + (n,)
        b = []
        for a in tramos_comp:
            i = a if a >= 0 else len(lim) - 1 + a
            sl = slice(lim[i], lim[i + 1])
            b.append(np.linalg.lstsq(X[sl], y[sl], rcond=None)[0][col])
        return abs(b[1] - b[0])
    return f


def stat_t_dif_coef(y, X, col=0, tramos_comp=(0, -1)):
    """Version STUDENTIZADA de stat_dif_coef: |t| de la diferencia de coeficientes (EE homocedasticos por tramo). Es (casi)
    pivotal respecto a las fechas, de modo que el contraste de permutacion tiene tamano proximo al nominal; la version sin
    studentizar es conservadora porque las fechas aleatorias cercanas a los bordes producen diferencias mas variables."""
    y = np.asarray(y, float)
    X = np.asarray(X, float)
    n = len(y)

    def f(cortes):
        lim = (0,) + tuple(cortes) + (n,)
        b, v = [], []
        for a in tramos_comp:
            i = a if a >= 0 else len(lim) - 1 + a
            sl = slice(lim[i], lim[i + 1])
            Xs, ys = X[sl], y[sl]
            bb = np.linalg.lstsq(Xs, ys, rcond=None)[0]
            r = ys - Xs @ bb
            s2 = r @ r / max(len(ys) - Xs.shape[1], 1)
            b.append(bb[col])
            v.append(s2 * np.linalg.inv(Xs.T @ Xs)[col, col])
        return abs(b[1] - b[0]) / np.sqrt(v[0] + v[1])
    return f
