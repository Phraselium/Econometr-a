"""Utilidades econométricas reutilizables (F2-F6). Sin efectos al importar.

Convenciones: índice trimestral pandas PeriodIndex(freq='Q'); errores HAC Newey-West (maxlags=4);
semilla fija SEED. Todas las funciones leen solo de data/processed.
"""
from __future__ import annotations

import warnings
from pathlib import Path

import numpy as np
import pandas as pd
import statsmodels.api as sm
import statsmodels.formula.api as smf
from scipy import stats
from statsmodels.stats.diagnostic import (acorr_breusch_godfrey, breaks_cusumolsresid,
                                          het_breuschpagan, linear_reset)
from statsmodels.stats.outliers_influence import variance_inflation_factor
from statsmodels.stats.stattools import durbin_watson, jarque_bera

ROOT = Path(__file__).resolve().parents[1]
SEED = 20261009
DUMMIES_Q = ["q2", "q3", "q4"]


# ---------------------------------------------------------------- datos
def load_nacional(desde: str = "2008Q1", hasta: str = "2026Q2") -> pd.DataFrame:
    """Lee data/processed/nacional_q.csv con índice PeriodIndex trimestral y añade derivadas.

    Las derivadas con retardos/adelantos se calculan sobre la serie COMPLETA antes de recortar a
    [desde, hasta], de modo que los retardos usan datos previos a `desde` si existen.
    Derivadas: ln_ipv_real, d_ln_ipv_real, ln_costes_real, ln_permisos_l4, d_ln_permisos_l4,
    d_ln_pob_extranj4 (=d4/4), d_ln_ipv_l1..l4, d_ln_ocupados_l1, d_tipo_hip_l1, tipo22 (escalón
    desde 2022Q3), epa21 (=quiebre_epa_2021). Dummies q2..q4 como float.
    """
    df = pd.read_csv(ROOT / "data" / "processed" / "nacional_q.csv")
    df.index = pd.PeriodIndex(df["trimestre"], freq="Q")
    new = {}
    new["ln_ipv_real"] = df["ln_ipv"] - df["ln_deflactor"]
    new["d_ln_ipv_real"] = new["ln_ipv_real"].diff()
    new["ln_costes_real"] = df["ln_costes"] - df["ln_deflactor"]
    new["ln_permisos_l4"] = df["ln_permisos"].shift(4)
    new["d_ln_permisos_l4"] = df["d_ln_permisos"].shift(4)
    new["d_ln_pob_extranj4"] = df["d4_ln_pob_extranj"] / 4.0
    for k in range(1, 5):
        new[f"d_ln_ipv_l{k}"] = df["d_ln_ipv"].shift(k)
    new["d_ln_ocupados_l1"] = df["d_ln_ocupados"].shift(1)
    new["d_tipo_hip_l1"] = df["d_tipo_hip"].shift(1)
    new["tipo22"] = (df.index >= pd.Period("2022Q3", "Q")).astype(float)
    new["epa21"] = df["quiebre_epa_2021"].astype(float)
    df = df.drop(columns=[c for c in new if c in df.columns])
    for q in ("q1", "q2", "q3", "q4"):
        new[q] = pd.read_csv(ROOT / "data" / "processed" / "nacional_q.csv")[q].astype(float).values
    df = pd.concat([df.drop(columns=[q for q in ("q1", "q2", "q3", "q4") if q in df.columns]),
                    pd.DataFrame(new, index=df.index)], axis=1)
    return df.loc[desde:hasta].copy()


def common_sample(df: pd.DataFrame, cols) -> pd.DataFrame:
    """Muestra común: filas de df sin NaN en TODAS las columnas `cols` (comparar modelos aquí)."""
    return df.dropna(subset=list(cols)).copy()


# ---------------------------------------------------------------- estimación
def ols_hac(formula: str, df: pd.DataFrame, maxlags: int = 4):
    """OLS por fórmula con errores Newey-West (HAC) de `maxlags` retardos."""
    return smf.ols(formula, df).fit(cov_type="HAC", cov_kwds={"maxlags": maxlags})


def tabla(res) -> pd.DataFrame:
    """Coeficientes con EE HAC (los del ajuste), t y p."""
    return pd.DataFrame({"coef": res.params, "EE_HAC": res.bse, "t": res.tvalues, "p": res.pvalues})


def df_md(df: pd.DataFrame, floatfmt: str = ".4g", index: bool = True) -> str:
    """DataFrame a tabla markdown (pipe)."""
    return df.to_markdown(index=index, floatfmt=floatfmt)


def tabla_md(res, floatfmt: str = ".4g") -> str:
    """Tabla markdown de coeficientes: coef, EE HAC, t, p."""
    return df_md(tabla(res), floatfmt)


def dols(df: pd.DataFrame, y: str, xs: list[str], fijas: list[str] | None = None, k: int = 2,
         maxlags: int = 4, desde: str | None = None):
    """DOLS de Stock-Watson: y sobre const, xs en niveles, +-k adelantos/retardos de Delta xs.

    `fijas`: regresores deterministas adicionales (dummies) incluidos en la relación de equilibrio.
    Devuelve dict(res, beta (Series xs), const, gamma (fijas), ect (Series sobre TODO df con niveles
    disponibles: y - const - xs*beta - fijas*gamma), n). La muestra de estimación pierde k al final
    por los adelantos. Las diferencias en los bordes de df son NaN: pasar df con historia previa; `desde` fija el inicio
    de la muestra de estimación (la historia previa solo aporta retardos).
    """
    fijas = fijas or []
    cols = {}
    for x in xs:
        dx = df[x].diff()
        for j in range(-k, k + 1):
            cols[f"D_{x}_{j}"] = dx.shift(-j)
    Z = pd.concat([df[[y] + xs + fijas], pd.DataFrame(cols, index=df.index)], axis=1).dropna()
    if desde:
        Z = Z.loc[desde:]
    X = sm.add_constant(Z.drop(columns=[y]))
    res = sm.OLS(Z[y], X).fit(cov_type="HAC", cov_kwds={"maxlags": maxlags})
    beta = res.params[xs]
    gamma = res.params[fijas] if fijas else pd.Series(dtype=float)
    ect = df[y] - res.params["const"] - (df[xs] * beta).sum(axis=1)
    if fijas:
        ect = ect - (df[fijas] * gamma).sum(axis=1)
    return dict(res=res, beta=beta, const=res.params["const"], gamma=gamma, ect=ect, n=int(res.nobs))


# ---------------------------------------------------------------- diagnósticos
def diagnostics(res, df=None) -> dict:
    """Diagnósticos sobre los residuos MCO del modelo (se reajusta sin HAC; los contrastes
    asumen MCO clásico). Devuelve DW, BG(4) p, BP p, JB p, RESET p (potencias 2-3), CUSUM p y VIF max.
    """
    y, X = res.model.endog, res.model.exog
    names = list(res.model.exog_names)
    ols = sm.OLS(y, X).fit()
    out = {"n": int(ols.nobs), "k": int(X.shape[1]), "DW": float(durbin_watson(ols.resid))}
    for key, f in {
        "BG4_p": lambda: acorr_breusch_godfrey(ols, nlags=4)[3],
        "BP_p": lambda: het_breuschpagan(ols.resid, X)[1],
        "JB_p": lambda: jarque_bera(ols.resid)[1],
        "RESET_p": lambda: float(linear_reset(ols, power=[2, 3], test_type="fitted", use_f=True).pvalue),
        "CUSUM_p": lambda: breaks_cusumolsresid(ols.resid, ddof=X.shape[1])[1],
    }.items():
        try:
            out[key] = float(f())
        except Exception:
            out[key] = np.nan
    keep = [i for i, n in enumerate(names)
            if n not in ("Intercept", "const") and not (n[:1] == "q" and n[1:].isdigit())]
    try:
        if len(keep) >= 2:
            Xv = np.column_stack([np.ones(len(y)), X[:, keep]])
            out["VIF_max"] = float(max(variance_inflation_factor(Xv, i + 1) for i in range(len(keep))))
        else:
            out["VIF_max"] = np.nan
    except Exception:
        out["VIF_max"] = np.nan
    return out


def chow(df: pd.DataFrame, formula: str, fecha: str) -> dict:
    """Chow de quiebre en `fecha` (primer trimestre del segundo régimen). F y p; NaN si un tramo
    no tiene más observaciones que parámetros."""
    import patsy
    yy, XX = patsy.dmatrices(formula, df, return_type="dataframe")
    f0 = pd.Period(fecha, "Q")
    m2 = yy.index >= f0
    k = int(np.linalg.matrix_rank(XX.values))
    n1, n2 = int((~m2).sum()), int(m2.sum())

    def rss(a, b):
        beta = np.linalg.lstsq(a, b, rcond=None)[0]
        r = b - a @ beta
        return float(r @ r)
    if n1 <= k or n2 <= k:
        return {"fecha": fecha, "F": np.nan, "p": np.nan, "n1": n1, "n2": n2, "k": k}
    rp = rss(XX.values, yy.values[:, 0])
    r1 = rss(XX.values[~m2], yy.values[~m2, 0])
    r2 = rss(XX.values[m2], yy.values[m2, 0])
    F = ((rp - r1 - r2) / k) / ((r1 + r2) / (n1 + n2 - 2 * k))
    return {"fecha": fecha, "F": float(F), "p": float(stats.f.sf(F, k, n1 + n2 - 2 * k)),
            "n1": n1, "n2": n2, "k": k}


def bai_perron(y: pd.Series, X: pd.DataFrame, max_bkps: int = 3, min_size: int = 12) -> dict:
    """Bai-Perron con ruptures (programación dinámica, coste 'linear'); nº de quiebres por BIC.
    X debe incluir la constante. Devuelve dict(n_bkps, fechas (primer trimestre del nuevo régimen),
    bic {nb: valor}). Los nb con algún tramo <= nº de parámetros se omiten."""
    import ruptures as rpt
    yv, Xv = np.asarray(y, float), np.asarray(X, float)
    n, p = Xv.shape
    algo = rpt.Dynp(model="linear", min_size=min_size, jump=1).fit(np.column_stack([yv, Xv]))
    bic, bk = {}, {}
    for nb in range(0, max_bkps + 1):
        try:
            b = [0] + (algo.predict(n_bkps=nb) if nb > 0 else [n])
        except Exception:
            continue
        if min(np.diff(b)) <= p:
            continue
        rss = 0.0
        for a, c in zip(b[:-1], b[1:]):
            beta = np.linalg.lstsq(Xv[a:c], yv[a:c], rcond=None)[0]
            r = yv[a:c] - Xv[a:c] @ beta
            rss += float(r @ r)
        bic[nb] = n * np.log(rss / n) + ((nb + 1) * p + nb) * np.log(n)
        bk[nb] = b[1:-1]
    best = min(bic, key=bic.get)
    return {"n_bkps": best, "fechas": [str(y.index[i]) for i in bk[best]], "bic": bic}


def dm_test(e1, e2, h: int = 1) -> dict:
    """Diebold-Mariano (pérdida cuadrática) con varianza HAC Bartlett (h-1 retardos) y corrección de
    Harvey-Leybourne-Newbold; p con t(n-1). d = e1^2 - e2^2: estadístico < 0 => el modelo 1 predice mejor."""
    e1, e2 = np.asarray(e1, float), np.asarray(e2, float)
    d = e1 ** 2 - e2 ** 2
    n = len(d)
    dbar = d.mean()
    dc = d - dbar
    lrv = dc @ dc / n
    for l in range(1, h):
        lrv += 2 * (1 - l / h) * (dc[l:] @ dc[:-l]) / n
    dm = dbar / np.sqrt(lrv / n)
    hlnc = np.sqrt((n + 1 - 2 * h + h * (h - 1) / n) / n)
    st = dm * hlnc
    return {"DM": float(st), "p": float(2 * stats.t.sf(abs(st), n - 1)), "mean_d": float(dbar), "n": n}


# ---------------------------------------------------------------- registro
class Registry:
    """Registro de búsqueda en CSV (append). `reset=True` reescribe desde cero."""
    COLS = ["fase", "modelo_id", "formula", "muestra_ini", "muestra_fin", "n", "r2_adj", "aic", "bic",
            "rmse_oos", "coef_interes", "p_interes", "notas"]

    def __init__(self, path, reset: bool = False):
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        if reset and self.path.exists():
            self.path.unlink()
        if not self.path.exists():
            pd.DataFrame(columns=self.COLS).to_csv(self.path, index=False)

    def log(self, fase, modelo_id, formula, muestra_ini, muestra_fin, n, r2_adj, aic, bic,
            rmse_oos=np.nan, coef_interes=np.nan, p_interes=np.nan, notas=""):
        row = pd.DataFrame([[fase, modelo_id, formula, str(muestra_ini), str(muestra_fin), n, r2_adj,
                             aic, bic, rmse_oos, coef_interes, p_interes, notas]], columns=self.COLS)
        row.to_csv(self.path, mode="a", header=False, index=False)

    def read(self) -> pd.DataFrame:
        return pd.read_csv(self.path)

    def log_res(self, fase, modelo_id, formula, res, interes=None, rmse_oos=np.nan, notas=""):
        """Atajo: registra un resultado de statsmodels (coef de interés = `interes` si existe)."""
        idx = res.model.data.row_labels
        ci = res.params.get(interes, np.nan) if interes else np.nan
        pi = res.pvalues.get(interes, np.nan) if interes else np.nan
        self.log(fase, modelo_id, formula, idx[0], idx[-1], int(res.nobs), res.rsquared_adj, res.aic,
                 res.bic, rmse_oos, ci, pi, notas)


def holm(pvals: dict) -> dict:
    """Ajuste de Holm para un dict nombre->p."""
    items = sorted(pvals.items(), key=lambda kv: kv[1])
    m, out, run = len(items), {}, 0.0
    for i, (k, p) in enumerate(items):
        run = max(run, min(1.0, (m - i) * p))
        out[k] = run
    return out


warnings.filterwarnings("ignore", category=FutureWarning)
