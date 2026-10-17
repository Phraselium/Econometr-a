"""V16-F2.2b · Descomposición del precio (valor tasado MIVAU) en componente común y local, panel provincial trimestral (C4).

Sin lectura causal: el factor es un resumen de comovimiento. Amplía V8-M1 (factor común de 17 CCAA, precio real, periodos P1-P5: ya visto)
a provincias, con los periodos 2007-2013, 2014-2019 y 2020-2026T2.
Muestra: variable valor_tasado (euros/m2, MIVAU) de data/base/hechos.parquet con muestra_sellada_v6 == False, solo filas trimestrales.
Quedan 38 provincias (las 11 selladas de v6 se excluyen, K8; Cantabria (39) no figura en la serie); 33 con serie completa 2006T1-2026T2
(principal); las 5 con huecos en 2012 (16, 32, 34, 40, 42) entran solo en robustez con interpolación lineal del logaritmo (MARCADA).
Tasas: Δ4 ln (interanual, comparable con V8) y Δ ln trimestral. Por periodo: PCA sobre series tipificadas (1.er componente; Bai-Ng ICp2
para el número de factores); cuota de varianza común por provincia (R² con el factor); residuo local; contraste con DynamicFactor de
statsmodels (1 factor, AR(2)) en toda la muestra. Cuota y bandas: bootstrap por bloques de 4 trimestres (SEED=20261010).
Contabilidad exacta del cambio acumulado de ln precio de cada provincia en un periodo (tasas trimestrales): común + local, con un factor
sin centrar (el factor centrado tendría suma cero y no explicaría el cambio acumulado).
"""
from __future__ import annotations

import os

for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS"):
    os.environ.setdefault(_v, "1")

import sys  # noqa: E402
import warnings  # noqa: E402
from pathlib import Path  # noqa: E402

import duckdb  # noqa: E402
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402

RAIZ = Path(__file__).resolve().parents[2]
SEED = 20261010
HECHOS = RAIZ / "data/base/hechos.parquet"
SELLADAS_V6 = ["07", "22", "26", "28", "30", "31", "33", "35", "38", "44", "50"]
PERIODOS = {"2007-2013": ("2007T1", "2013T4"), "2014-2019": ("2014T1", "2019T4"), "2020-2026": ("2020T1", "2026T2")}
CON_HUECOS = ["16", "32", "34", "40", "42"]


def _q(p: str) -> pd.Period:
    return pd.Period(p.replace("T", "Q"), freq="Q")


def cargar_log_precio() -> pd.DataFrame:
    """ln(valor tasado), filas = trimestres 2002T1-2026T2, columnas = provincias NO selladas (con huecos como NaN)."""
    d = duckdb.sql(f"select territorio_codigo c, periodo, valor from '{HECHOS}' where variable='valor_tasado' and nivel='provincia' "
                   "and frecuencia='T' and not muestra_sellada_v6").df()
    d["t"] = d.periodo.map(_q)
    w = d.pivot(index="t", columns="c", values="valor").sort_index()
    w = w.loc[w.index >= _q("2002T1")]
    assert not set(w.columns) & set(SELLADAS_V6), "provincia v6 en el panel"
    return np.log(w)


def cargar_deflactor() -> pd.Series:
    d = duckdb.sql(f"select periodo, valor from '{HECHOS}' where variable='deflactor' and nivel='nacional' and not muestra_sellada_v6 "
                   "and frecuencia='T'").df()
    s = pd.Series(d.valor.values, index=d.periodo.map(_q)).sort_index()
    return np.log(s)


def panel_ccaa_libres() -> pd.DataFrame:
    """ln valor_tasado_ccaa de las CCAA sin provincias selladas (para el puente con V8, que usó 17 CCAA)."""
    t = pd.read_parquet(RAIZ / "data/base/territorios.parquet")
    m = t[t.nivel == "provincia"].set_index("territorio_codigo").cod_ccaa
    prov_por = m.groupby(m).apply(lambda s: set(s.index))
    libres = [c for c, ps in prov_por.items() if not ps & set(SELLADAS_V6)]
    d = duckdb.sql(f"select territorio_codigo c, periodo, valor from '{HECHOS}' where variable='valor_tasado_ccaa' and nivel='ccaa' "
                   "and frecuencia='T' and not muestra_sellada_v6").df()
    d = d[d.c.isin(libres)]
    d["t"] = d.periodo.map(_q)
    return np.log(d.pivot(index="t", columns="c", values="valor").sort_index())


def construir(lp: pd.DataFrame, tipo: str, interpolar: bool = False) -> pd.DataFrame:
    x = lp.copy()
    if interpolar:
        x = x.interpolate(limit_area="inside")
    r = x.diff(4) if tipo == "d4" else x.diff(1)
    return r


def ventana(r: pd.DataFrame, ini: str, fin: str) -> pd.DataFrame:
    x = r.loc[_q(ini):_q(fin)]
    return x.dropna(axis=1, how="any")


# ---------------------------------------------------------------- PCA
def _pca(Z: np.ndarray):
    C = np.corrcoef(Z, rowvar=False)
    w, v = np.linalg.eigh(C)
    o = np.argsort(w)[::-1]
    return w[o], v[:, o]


def estandarizar(X: np.ndarray):
    mu, sd = X.mean(0), X.std(0, ddof=1)
    return (X - mu) / sd, mu, sd


def pca_periodo(X: np.ndarray) -> dict:
    """PCA de series tipificadas. Devuelve cuota PC1, cuota 2 factores, R² por columna, factor, cargas y residuo (en unidades tipificadas)."""
    Z, mu, sd = estandarizar(X)
    w, v = _pca(Z)
    T, N = Z.shape
    f = Z @ v[:, 0]
    if v[:, 0].sum() < 0:
        f, vv = -f, -v[:, 0]
    else:
        vv = v[:, 0]
    f = (f - f.mean()) / f.std(ddof=1)
    lam = np.array([np.polyfit(f, Z[:, i], 1)[0] for i in range(N)])
    e = Z - np.outer(f, lam)
    r2 = 1 - e.var(0, ddof=1) / Z.var(0, ddof=1)
    return {"cuota1": w[0] / w.sum(), "cuota2": w[:2].sum() / w.sum(), "w": w, "f": f, "lam": lam, "r2": r2, "e": e, "mu": mu, "sd": sd,
            "Z": Z, "T": T, "N": N}


def bai_ng_icp2(X: np.ndarray, kmax: int = 4) -> int:
    """Número de factores por Bai y Ng (2002) ICp2 (datos tipificados)."""
    Z, _, _ = estandarizar(X)
    T, N = Z.shape
    w, v = _pca(Z)
    kmax = min(kmax, N - 1, T - 1)
    pen = (N + T) / (N * T) * np.log(min(N, T))
    best, bk = np.inf, 0
    for k in range(0, kmax + 1):
        if k == 0:
            V = (Z**2).mean()
        else:
            F = Z @ v[:, :k]
            res = Z - F @ v[:, :k].T
            V = (res**2).mean()
        ic = np.log(V) + k * pen
        if ic < best:
            best, bk = ic, k
    return bk


def cuota_bootstrap(X: np.ndarray, B: int, rng: np.random.Generator, L: int = 4) -> np.ndarray:
    """Bootstrap por bloques móviles (longitud L) de la cuota del 1.er componente."""
    T = X.shape[0]
    nb = int(np.ceil(T / L))
    out = np.empty(B)
    for b in range(B):
        st = rng.integers(0, T - L + 1, nb)
        idx = np.concatenate([np.arange(s, s + L) for s in st])[:T]
        Z, _, _ = estandarizar(X[idx])
        w = np.linalg.eigvalsh(np.corrcoef(Z, rowvar=False))
        out[b] = w[-1] / w.sum()
    return out


def cuota_nula(T: int, N: int, B: int, rng: np.random.Generator) -> np.ndarray:
    out = np.empty(B)
    for b in range(B):
        w = np.linalg.eigvalsh(np.corrcoef(rng.standard_normal((T, N)), rowvar=False))
        out[b] = w[-1] / w.sum()
    return out


# ---------------------------------------------------------------- DFM
def dfm_statsmodels(X: np.ndarray, maxiter: int = 150):
    """DynamicFactor de statsmodels: 1 factor AR(2), errores idiosincráticos independientes. Devuelve (factor suavizado tipificado, convergió)."""
    import statsmodels.api as sm
    Z, _, _ = estandarizar(X)
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        mod = sm.tsa.DynamicFactor(Z, k_factors=1, factor_order=2, error_order=0, error_cov_type="diagonal")
        res = mod.fit(method="lbfgs", maxiter=maxiter, disp=False)
    f = np.asarray(res.factors.smoothed[0], dtype=float)
    f = (f - f.mean()) / f.std(ddof=1)
    return f, bool(res.mle_retvals.get("converged", False)), float(res.llf)


def r2_con_factor(Z: np.ndarray, f: np.ndarray) -> np.ndarray:
    c = np.array([np.corrcoef(f, Z[:, i])[0, 1] for i in range(Z.shape[1])])
    return c**2


# ---------------------------------------------------------------- contabilidad exacta del nivel
def contabilidad_nivel(X: np.ndarray, cols: list[str], periodo: str) -> pd.DataFrame:
    """Cambio acumulado de ln precio en el periodo (suma de tasas trimestrales) = común + local, exacto.
    Factor SIN centrar (SVD de X/escala, escala = raíz de la media de cuadrados por provincia) para que el factor lleve la tendencia media:
    común_i = Σ_t s_i·v_i·d·u_t ; local_i = Σ_t (X_it − s_i·v_i·d·u_t). Puntos de ln x100. La cuota no centrada es la parte de la suma
    de cuadrados que recoge el 1.er factor."""
    s = np.sqrt((X**2).mean(0))
    Y = X / s
    U, d, Vt = np.linalg.svd(Y, full_matrices=False)
    u, v = U[:, 0], Vt[0]
    if v.sum() < 0:
        u, v = -u, -v
    fit = np.outer(u, v) * d[0] * s
    comun = fit.sum(0)
    total = X.sum(0)
    out = pd.DataFrame({"provincia": cols, "periodo": periodo, "cambio_ln_x100": 100 * total, "comun": 100 * comun,
                        "local": 100 * (total - comun)})
    out["cuota_no_centrada"] = d[0] ** 2 / (d**2).sum()
    out["error_identidad"] = out.cambio_ln_x100 - (out.comun + out.local)
    return out


def correlacion_residuos(e: np.ndarray, cols: list[str], ccaa: dict) -> dict:
    C = np.corrcoef(e, rowvar=False)
    iu = np.triu_indices(len(cols), 1)
    mismo = np.array([ccaa.get(cols[i]) == ccaa.get(cols[j]) for i, j in zip(*iu)])
    v = C[iu]
    return {"corr_residual_media": float(v.mean()), "corr_residual_misma_ccaa": float(v[mismo].mean()) if mismo.any() else np.nan,
            "corr_residual_distinta_ccaa": float(v[~mismo].mean()), "pares_misma_ccaa": int(mismo.sum())}
