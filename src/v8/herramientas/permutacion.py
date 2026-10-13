"""Prueba de permutacion de fechas de corte (placebo de fechas).

Dado un estadistico por tramos (p. ej. diferencia de coeficientes entre periodos) y unas fechas de corte
OBSERVADAS fijadas a priori, compara con conjuntos de fechas aleatorias con el mismo numero de tramos y longitudes
minimas. El p-valor es (1+#)/(1+B) (Monte Carlo) o la proporcion sobre la enumeracion completa de los conjuntos de fechas
cuando su numero es <= n_perm. VALIDEZ APROXIMADA, no exacta: la exactitud en muestra finita exigiria que las fechas
fueran intercambiables bajo H0, lo que en general no se cumple con dependencia serial (el estadistico sin studentizar
depende de la posicion de los cortes); por eso se recomienda el estadistico studentizado y su tamano se mide por Monte
Carlo (output/v8/F3/otros/validacion.md). Dos variantes: `permutacion_cortes` (tramos contiguos, estadistico primero frente a
ultimo por defecto) y `permutacion_tramos` (K tramos NO contiguos, con huecos de longitud fija, y estadisticos sobre los K
tramos: `stat_Q_tramos`, `stat_maxt_tramos`).
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
        modo = "enumeracion_completa"
        B = len(stats)
    else:
        rng = np.random.default_rng(seed)
        stats = np.array([stat_fn(muestrear(n, T, min_len, rng)) for _ in range(n_perm)])
        p = float((1 + np.sum(stats >= s_obs - 1e-12)) / (1 + n_perm))
        modo = "monte_carlo"
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


# =========================================================================== tramos no contiguos y estadisticos sobre K tramos
def cortes_a_tramos(cortes, n):
    """Cortes contiguos -> tramos [(ini, fin)) semiabiertos."""
    lim = (0,) + tuple(int(c) for c in cortes) + (n,)
    return tuple(zip(lim[:-1], lim[1:]))


def _estructura(n, tramos_obs, min_len):
    tr = tuple((int(a), int(b)) for a, b in tramos_obs)
    longs = np.array([b - a for a, b in tr])
    if np.any(longs < min_len):
        raise ValueError("algun tramo observado es mas corto que min_len: las fechas observadas quedarian fuera del soporte")
    if any(tr[i + 1][0] < tr[i][1] for i in range(len(tr) - 1)) or tr[0][0] < 0 or tr[-1][1] > n:
        raise ValueError("tramos solapados o fuera de [0, n]")
    gaps = [tr[0][0]] + [tr[i + 1][0] - tr[i][1] for i in range(len(tr) - 1)]
    return longs, gaps, int(longs.sum() - len(tr) * min_len)


def _tramos_desde_longitudes(longs, gaps):
    out, pos = [], gaps[0]
    for i, L in enumerate(longs):
        out.append((int(pos), int(pos + L)))
        pos += L + (gaps[i + 1] if i + 1 < len(gaps) else 0)
    return tuple(out)


def n_conjuntos_tramos(n, tramos_obs, min_len):
    """Numero de reparticiones validas de los K tramos (huecos fijados a los observados, longitudes >= min_len)."""
    K = len(tramos_obs)
    return math.comb(_estructura(n, tramos_obs, min_len)[2] + K - 1, K - 1)


def permutacion_tramos(stat_fn, n, tramos_obs, min_len, n_perm=2000, seed=SEED):
    """Placebo de fechas con K tramos posiblemente NO contiguos. stat_fn(tramos: tuple[(ini, fin)]) -> float (mayor = mas
    evidencia). Los conjuntos aleatorios conservan el numero de tramos, la longitud de cada hueco entre tramos (y antes del
    primero) y la suma de longitudes, y reparten las longitudes con minimo `min_len` de forma uniforme. p aproximado (ver docstring
    del modulo). Devuelve dict como `permutacion_cortes`."""
    longs, gaps, hol = _estructura(n, tramos_obs, min_len)
    K = len(longs)
    s_obs = float(stat_fn(tuple((int(a), int(b)) for a, b in tramos_obs)))
    tot = math.comb(hol + K - 1, K - 1)
    if tot <= n_perm:
        conjuntos = []
        for c in itertools.combinations_with_replacement(range(hol + 1), K - 1):
            extra = np.diff(np.r_[0, c, hol])
            conjuntos.append(_tramos_desde_longitudes(min_len + extra, gaps))
        st = np.array([stat_fn(t) for t in conjuntos])
        p, modo, B = float(np.mean(st >= s_obs - 1e-12)), "enumeracion_completa", len(st)
    else:
        rng = np.random.default_rng(seed)
        st = np.empty(n_perm)
        for i in range(n_perm):
            comb = np.sort(rng.choice(hol + K - 1, K - 1, replace=False))
            extra = np.diff(np.r_[0, comb - np.arange(K - 1), hol])
            st[i] = stat_fn(_tramos_desde_longitudes(min_len + extra, gaps))
        p, modo, B = float((1 + np.sum(st >= s_obs - 1e-12)) / (1 + n_perm)), "monte_carlo", n_perm
    return {"stat_obs": s_obs, "p": p, "modo": modo, "n_conjuntos": tot, "n_perm": B,
            "cuantil95_perm": float(np.quantile(st, 0.95)), "stats": st}


def _coef_var(y, X, sl, col, se, L):
    Xs, ys = X[sl], y[sl]
    bb = np.linalg.lstsq(Xs, ys, rcond=None)[0]
    r = ys - Xs @ bb
    XtXi = np.linalg.inv(Xs.T @ Xs)
    if se == "homo":
        v = (r @ r / max(len(ys) - Xs.shape[1], 1)) * XtXi[col, col]
    else:  # Newey-West (Bartlett) con L retardos
        G = Xs * r[:, None]
        S = G.T @ G
        for l in range(1, min(L, len(ys) - 1) + 1):
            Gam = G[l:].T @ G[:-l]
            S += (1 - l / (L + 1)) * (Gam + Gam.T)
        v = (XtXi @ S @ XtXi)[col, col]
    return bb[col], v


def stat_Q_tramos(y, X, col=0, se="homo", L=4):
    """Estadistico sobre K tramos: Q de heterogeneidad de Cochran, Q = sum_i w_i (b_i - b_w)^2 con w_i = 1/var(b_i) y b_w la
    media ponderada; contrasta que el coeficiente `col` es el mismo en los K tramos (tramos como lista de (ini, fin)).
    se='homo' (EE homocedasticos) o 'hac' (Newey-West, L retardos; mas robusto a autocorrelacion en tramos largos)."""
    y = np.asarray(y, float)
    X = np.asarray(X, float)

    def f(tramos):
        bv = np.array([_coef_var(y, X, slice(a, b), col, se, L) for a, b in tramos])
        w = 1.0 / bv[:, 1]
        bw = np.sum(w * bv[:, 0]) / np.sum(w)
        return float(np.sum(w * (bv[:, 0] - bw) ** 2))
    return f


def stat_maxt_tramos(y, X, col=0, se="homo", L=4):
    """Estadistico sobre K tramos: maximo, sobre pares de tramos, de |b_i - b_j| / sqrt(v_i + v_j)."""
    y = np.asarray(y, float)
    X = np.asarray(X, float)

    def f(tramos):
        bv = np.array([_coef_var(y, X, slice(a, b), col, se, L) for a, b in tramos])
        K = len(bv)
        return float(max(abs(bv[i, 0] - bv[j, 0]) / np.sqrt(bv[i, 1] + bv[j, 1]) for i in range(K) for j in range(i + 1, K)))
    return f
