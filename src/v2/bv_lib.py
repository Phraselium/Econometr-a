"""Rama BV (compra): utilidades. Datos SOLO vía v2_common.load. Sin red; determinista (SEED=20261010)."""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import sparse, stats

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))
import v2_common as vc  # noqa: E402
from econ_utils import Registry, holm  # noqa: E402

SEED = vc.SEED
OUT = ROOT / "output" / "v2" / "BV"
PERIODOS = {"P1_ajuste": ("2008Q1", "2013Q4"), "P2_recuperacion": ("2014Q1", "2019Q4"),
            "P3_covid": ("2020Q1", "2021Q4"), "P4_tipos": ("2022Q1", "2024Q2")}


def bh(pvals: dict) -> dict:
    items = sorted(pvals.items(), key=lambda kv: kv[1])
    m = len(items)
    out, run = {}, 1.0
    for i in range(m - 1, -1, -1):
        k, p = items[i]
        run = min(run, p * m / (i + 1))
        out[k] = run
    return out


# ------------------------------------------------------------------ datos
def preparar_panel(pan: pd.DataFrame, nac: pd.DataFrame) -> pd.DataFrame:
    """Añade: precio real (deflactor nacional de nacional_q_v2), exposición hipotecaria 2005-2007
    (importe hipotecario por habitante, media 2005Q1-2007Q4, fija por provincia; z-score entre
    provincias de entrenamiento) y las variables derivadas de H2."""
    d = pan.copy()
    d["trimestre"] = d["trimestre"].astype(str)
    d = d[d["trimestre"] <= vc.Q_TRAIN_FIN].copy()
    n = nac.copy()
    n["trimestre"] = n["trimestre"].astype(str)
    n = n.drop_duplicates("trimestre").set_index("trimestre")
    d["ln_defl"] = d["trimestre"].map(n["ln_deflactor"])
    d["d4_ln_defl"] = d["trimestre"].map(n["d4_ln_deflactor"])
    d["ln_p_real"] = d["ln_p_tasado"] - d["ln_defl"]
    d["d4_ln_p_real"] = d["d4_ln_p_tasado"] - d["d4_ln_defl"]
    pc = d["hipotecas_importe"] / d["pob_total"]
    m = d["trimestre"].between("2005Q1", "2007Q4")
    ex = pc[m].groupby(d.loc[m, "cod_prov"]).mean()
    d["expo_raw"] = d["cod_prov"].map(ex)
    d["expo"] = (d["expo_raw"] - ex.mean()) / ex.std(ddof=0)
    d["cu_x_expo"] = d["coste_uso_aprox"] * d["expo"]
    d = d.sort_values(["cod_prov", "trimestre"]).reset_index(drop=True)
    d["hip_l4"] = d.groupby("cod_prov")["d4_ln_hipotecas_importe"].shift(4)
    return d


def periodo_de(t: str):
    for k, (a, b) in PERIODOS.items():
        if a <= t <= b:
            return k
    return None


# ------------------------------------------------------------------ MCO con FE y cluster
class FE:
    """MCO con efectos fijos (dummies) vía FWL y covarianza cluster CR1."""

    def __init__(self, df, y, xs, cluster="cod_prov", fe_ent=True, fe_time=True, extra_fe=None, tcol="trimestre"):
        cols = [y] + list(xs) + [cluster, tcol] + ([extra_fe] if extra_fe else [])
        d = df.dropna(subset=[c for c in cols if c in df]).copy()
        d = d.sort_values([cluster, tcol]).reset_index(drop=True)
        self.d, self.xs, self.y = d, list(xs), y
        D = []
        if fe_ent:
            D.append(pd.get_dummies(d[cluster], dtype=float).values)
        if fe_time:
            D.append(pd.get_dummies(d[tcol], dtype=float, drop_first=fe_ent).values)
        if extra_fe:
            D.append(pd.get_dummies(d[extra_fe], dtype=float, drop_first=bool(D)).values)
        self.D = np.hstack(D) if D else np.zeros((len(d), 0))
        self.N, self.k = len(d), len(xs)
        X, Y = d[xs].values.astype(float), d[y].values.astype(float)
        if self.D.shape[1]:
            self.Dp = np.linalg.pinv(self.D)
            self.Xt = X - self.D @ (self.Dp @ X)
            self.Yt = Y - self.D @ (self.Dp @ Y)
        else:
            self.Dp, self.Xt, self.Yt = None, X, Y
        self.A = self.Xt.T @ self.Xt
        self.Ai = np.linalg.inv(self.A)
        self.beta = self.Ai @ self.Xt.T @ self.Yt
        self.res = self.Yt - self.Xt @ self.beta
        cl = d[cluster].values
        self.cl_codes, self.cl_u = pd.factorize(cl)
        self.G = len(self.cl_u)
        self.C = sparse.csr_matrix((np.ones(self.N), (self.cl_codes, np.arange(self.N))), shape=(self.G, self.N))
        rk = np.linalg.matrix_rank(self.D) if self.D.shape[1] else 0
        self.f = self.G / (self.G - 1) * (self.N - 1) / (self.N - self.k - max(rk - (self.G if fe_ent else 0), 0))
        S = self.C @ (self.Xt * self.res[:, None])
        self.cov = self.f * self.Ai @ (S.T @ S) @ self.Ai
        self.se = np.sqrt(np.diag(self.cov))
        self.t = self.beta / self.se
        self.p = 2 * stats.t.sf(np.abs(self.t), self.G - 1)

    def tabla(self):
        ci = stats.t.ppf(0.975, self.G - 1) * self.se
        return pd.DataFrame({"var": self.xs, "coef": self.beta, "se": self.se, "t": self.t, "p": self.p,
                             "ic95_inf": self.beta - ci, "ic95_sup": self.beta + ci})

    def wild_cluster_boot(self, j, B=9999, seed=SEED, chunk=500):
        """Wild cluster bootstrap restringido (WCR), pesos de Webb de 6 puntos; p bilateral para H0: beta_j=0."""
        rng = np.random.default_rng(seed + 17 * j)
        keep = [i for i in range(self.k) if i != j]
        Xr = self.Xt[:, keep]
        br = np.linalg.lstsq(Xr, self.Yt, rcond=None)[0] if keep else np.zeros(0)
        ur = self.Yt - (Xr @ br if keep else 0)
        aj = self.Ai[j]
        z = self.Xt @ aj
        webb = np.array([-np.sqrt(1.5), -1, -np.sqrt(0.5), np.sqrt(0.5), 1, np.sqrt(1.5)])
        tabs, done = [], 0
        while done < B:
            b = min(chunk, B - done)
            w = webb[rng.integers(0, 6, size=(self.G, b))][self.cl_codes]   # N x b
            wu = w * ur[:, None]
            delta = (aj @ self.Xt.T) @ wu                                     # b (coef j: a_j' X~' wu)
            Xwu = self.Xt.T @ wu                                              # k x b
            e = wu - (self.D @ (self.Dp @ wu) if self.Dp is not None else 0)
            e = e - self.Xt @ (self.Ai @ Xwu)
            c = self.C @ (z[:, None] * e)
            var = self.f * (c ** 2).sum(axis=0)
            tabs.append(delta / np.sqrt(var))
            done += b
        ts = np.concatenate(tabs)
        return float((np.abs(ts) >= abs(self.t[j])).mean())


def hac_ols(y, X, lags=4):
    import statsmodels.api as sm
    return sm.OLS(y, sm.add_constant(X)).fit(cov_type="HAC", cov_kwds={"maxlags": lags})


# ------------------------------------------------------------------ modelos fuera de muestra
_g = vc._g


def feat_panel(cfg: str):
    """Constructor de features (información en el origen t). cfg in C1..C6 (declaradas en bv_main)."""
    def f(long):
        cols = []
        ar = cfg in ("C1", "C2", "C3", "C5", "C6")
        if ar:
            cols += vc._feat_ar4(long)
        if cfg in ("C1", "C2", "C3", "C4"):
            cols += ["d4_ln_hipotecas_importe"]
        if cfg == "C5":
            long["hip_l4"] = _g(long, long["d4_ln_hipotecas_importe"], 4)
            cols += ["hip_l4"]
        if cfg in ("C2", "C3", "C4", "C5"):
            cols += ["d4_ln_ocupados"]
        if cfg in ("C3", "C4", "C5", "C6"):
            cols += ["coste_uso_aprox", "cu_x_expo"]
        return cols
    return f


def feat_nac(cfg: str):
    def f(long):
        long["dcred"] = long["ln_credito_nuevo"] - _g(long, long["ln_credito_nuevo"], 1)
        long["dhipn"] = np.log(long["hipotecas_importe_nac"]) - _g(long, np.log(long["hipotecas_importe_nac"]), 1)
        long["dcons"] = np.log(long["credito_nuevo_consumo_bde"]) - _g(long, np.log(long["credito_nuevo_consumo_bde"]), 1)
        long["doth"] = np.log(long["credito_nuevo_otros_bde"]) - _g(long, np.log(long["credito_nuevo_otros_bde"]), 1)
        long["dcu"] = long["coste_uso_aprox"] - _g(long, long["coste_uso_aprox"], 1)
        ar = vc._feat_ar4(long)
        return {"N1": ar + ["dcred"], "N2": ar + ["dhipn", "dcu"],
                "N3": ar + ["dcred", "dcons", "doth", "dcu"], "N4": ["dY_l0", "dcred", "dcu"]}[cfg]
    return f


def run_panel_model(pan, nac, cfg, h=4, desde="2012Q1", min_train=8, splits=None):
    return vc._run(pan, "cod_prov", h, splits, desde, min_train, 4, 4, vc._lvl_fn("p_tasado", True, nac),
                   feat_panel(cfg), f"BV_{cfg}")


def run_nac_model(nac, cfg, h=4, desde="2012Q1", min_train=8):
    return vc._run(nac, None, h, None, desde, min_train, 4, 4, vc._lvl_fn("p_tasado", True), feat_nac(cfg),
                   f"BV_{cfg}")
