"""Replica ciega V16 de H5 (P9): combinacion DFM+BVAR+LASSO+ARDL frente a AR(4).

Especificacion principal: delta log valor tasado nacional, h=1, ventana expansiva
desde 2003T1, DM-HLN unilateral. Solo lee data/processed/v15 (p9_prediccion, p2_fundamentales).
Escrito desde la ficha (preregistro v15, adenda, DV15-B-1..4), sin mirar src/v15.
"""
import json
import warnings
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats
from sklearn.linear_model import Lasso

warnings.filterwarnings("ignore")
SEED = 20261010
np.random.seed(SEED)
ROOT = Path("/home/user/Econometr-a")
OUT = ROOT / "output/v16/replica/h5"
OUT.mkdir(parents=True, exist_ok=True)

p9 = pd.read_parquet(ROOT / "data/processed/v15/p9_prediccion.parquet")
p2 = pd.read_parquet(ROOT / "data/processed/v15/p2_fundamentales.parquet")


def nac(df, var):
    d = df[(df.nivel == "nacional") & (df.variable == var)]
    return d.set_index("periodo")["valor"].sort_index()


qs = [f"{y}T{q}" for y in range(1995, 2027) for q in range(1, 5)][:126]  # 1995T1..2026T2
D = pd.DataFrame(index=qs)
for v in ["p_tasado", "compraventas", "visados", "ocupados", "credito_nuevo", "ipv"]:
    D[v] = nac(p9, v).reindex(qs)
# hipotecas: suma de provincias de entrenamiento (trimestrales)
h = p9[(p9.variable == "hip_n") & (p9.nivel == "provincia") & (p9.periodo.str.len() == 6)]
D["hip_n"] = h.groupby("periodo")["valor"].sum().reindex(qs)
D["infl"] = nac(p2, "inflacion_ipc_yoy").reindex(qs)
D["tipo_real"] = nac(p2, "tipo_hip_real").reindex(qs)
D["renta_real"] = nac(p2, "renta_hog_real").reindex(qs)
# DV15-B-1: visados 2016T2 y 2017T2 por interpolacion loglineal
D["visados"] = np.exp(np.log(D["visados"]).interpolate(limit_area="inside"))

L = np.log
y_lv = L(D.p_tasado)
D["y"] = y_lv.diff()
D["dcv"] = L(D.compraventas).diff()
D["dhip"] = L(D.hip_n).diff()
D["dvis"] = L(D.visados).diff()
D["docu"] = L(D.ocupados).diff()
D["dcred"] = L(D.credito_nuevo).diff()
D["dtipo"] = D.tipo_real.diff()
D["drenta"] = L(D.renta_real).diff()
# IPC acumulado a partir de la inflacion interanual (base 1995 = 0)
lp = pd.Series(np.nan, index=qs)
for i, q in enumerate(qs):
    if np.isnan(D.infl.iloc[i]):
        lp.iloc[i] = np.nan
        continue
    prev = lp.iloc[i - 4] if i >= 4 else 0.0
    if i >= 4 and np.isnan(prev):
        prev = 0.0
    lp.iloc[i] = prev + np.log1p(D.infl.iloc[i] / 100)
D["lreal"] = y_lv - lp
D["lo"] = L(D.ocupados)
D["lvis4"] = L(D.visados).shift(4)

idx = {q: i for i, q in enumerate(qs)}
i2003 = idx["2003T1"]
XCOLS = ["dcv", "dhip", "dvis", "dtipo", "docu", "infl", "dcred"]
BV = ["y", "dcv", "dhip", "tipo_real", "docu", "infl"]
first_complete = max(D[c].first_valid_index() and idx[D[c].first_valid_index()] for c in XCOLS)
Y = D["y"].values


def ols(X, y):
    return np.linalg.lstsq(X, y, rcond=None)[0]


def f_ar4(o):
    rows = [s for s in range(i2003 - 1, o) if s - 3 >= 0]  # s -> target s+1 >= 2003T1
    X = np.array([[1, Y[s], Y[s - 1], Y[s - 2], Y[s - 3]] for s in rows])
    b = ols(X, Y[[s + 1 for s in rows]])
    return b @ np.array([1, Y[o], Y[o - 1], Y[o - 2], Y[o - 3]])


def f_rw(o):
    return np.mean(Y[i2003: o + 1])


def f_ecm(o):
    # ECT por DOLS(+-2) con datos hasta el origen
    cols = ["lo", "tipo_real", "lvis4"]
    ts = list(range(i2003 + 4, o - 1))  # holgura para leads/lags
    Z = D[cols].values
    rows, yy = [], []
    for t in ts:
        if t - 2 < 1 or t + 2 > o:
            continue
        r = [1] + list(Z[t])
        for k in range(-2, 3):
            r += list(Z[t + k] - Z[t + k - 1])
        rows.append(r)
        yy.append(D["lreal"].values[t])
    rows = np.array(rows)
    yy = np.array(yy)
    b = ols(rows, yy)
    ect = D["lreal"].values - (b[0] + Z @ b[1:4])
    srows, sy = [], []
    for s in range(i2003 + 4, o):
        r = [1, D.docu.values[s], D.dtipo.values[s], D.drenta.values[s], Y[s - 3], D.dcred.values[s], ect[s]]
        srows.append(r)
        sy.append(Y[s + 1])
    srows = np.array(srows)
    sy = np.array(sy)
    ok = ~np.isnan(srows).any(1) & ~np.isnan(sy)
    bb = ols(srows[ok], sy[ok])
    r = np.array([1, D.docu.values[o], D.dtipo.values[o], D.drenta.values[o], Y[o - 3], D.dcred.values[o], ect[o]])
    return r @ bb


def feats(o_rows, extra_lags=0):
    pass


def f_dfm(o):
    S = list(range(first_complete, o))  # s -> target s+1<=o
    X = D[XCOLS].values
    mu = X[first_complete: o + 1].mean(0)
    sd = X[first_complete: o + 1].std(0, ddof=1)
    Zs = (X[first_complete: o + 1] - mu) / sd
    u, s_, vt = np.linalg.svd(Zs, full_matrices=False)
    F = Zs @ vt[:2].T
    Fm = {first_complete + k: F[k] for k in range(len(F))}
    A = np.array([[1, *Fm[s], Y[s]] for s in S])
    b = ols(A, Y[[s + 1 for s in S]])
    return b @ np.array([1, *Fm[o], Y[o]])


def f_lasso(o):
    S = list(range(first_complete + 3, o))
    X = D[XCOLS].values

    def row(s):
        return np.concatenate([X[s], [Y[s], Y[s - 1], Y[s - 2], Y[s - 3]]])

    A = np.array([row(s) for s in S])
    yy = Y[[s + 1 for s in S]]
    n = len(S)
    alphas = np.logspace(-5, -2, 12)
    # validacion temporal con embargo de 4 trimestres
    folds = [int(n * f) for f in (0.5, 0.65, 0.8)]
    errs = np.zeros(len(alphas))
    cnt = 0
    for k in folds:
        te = list(range(k, min(k + max(3, int(n * 0.15)), n)))
        tr = list(range(0, max(k - 4, 0)))
        if len(tr) < 8 or not te:
            continue
        m = A[tr].mean(0)
        sg = A[tr].std(0, ddof=1) + 1e-12
        ym = yy[tr].mean()
        for j, a in enumerate(alphas):
            mod = Lasso(alpha=a, max_iter=50000).fit((A[tr] - m) / sg, yy[tr] - ym)
            p = mod.predict((A[te] - m) / sg) + ym
            errs[j] += np.mean((yy[te] - p) ** 2)
        cnt += 1
    a = alphas[int(np.argmin(errs))] if cnt else alphas[5]
    m = A.mean(0)
    sg = A.std(0, ddof=1) + 1e-12
    mod = Lasso(alpha=a, max_iter=50000).fit((A - m) / sg, yy - yy.mean())
    return mod.predict(((row(o) - m) / sg)[None])[0] + yy.mean()


def f_ardl(o):
    best = None
    X = D[["dcv", "dhip"]].values
    smin = first_complete + 4
    S = list(range(smin, o))
    yy = Y[[s + 1 for s in S]]
    n = len(S)
    for ny in range(1, 5):
        for nx in range(1, 5):
            def row(s, ny=ny, nx=nx):
                return np.concatenate([[1], [Y[s - k] for k in range(ny)],
                                       *[X[s - k] for k in range(nx)]])
            A = np.array([row(s) for s in S])
            k = A.shape[1]
            if n <= k + 2:
                continue
            b = ols(A, yy)
            rss = np.sum((yy - A @ b) ** 2)
            bic = n * np.log(rss / n) + k * np.log(n)
            if best is None or bic < best[0]:
                best = (bic, b, row)
    return best[1] @ best[2](o)


def f_bvar(o):
    Zb = D[BV].values
    S = list(range(first_complete + 2, o))

    def row(s):
        return np.concatenate([Zb[s], Zb[s - 1]])

    A = np.array([row(s) for s in S])
    yy = Y[[s + 1 for s in S]]
    am, asd = A.mean(0), A.std(0, ddof=1) + 1e-12
    As = (A - am) / asd
    ym = yy.mean()
    yc = yy - ym
    # sigma2: varianza residual de un AR(1) del objetivo
    Xa = np.column_stack([np.ones(len(S)), Y[S]])
    ba = ols(Xa, yy)
    s2 = np.var(yy - Xa @ ba, ddof=2)
    sy2 = np.var(yy, ddof=1)
    lag = np.array([1] * 6 + [2] * 6)
    best = None
    for lam in [0.05, 0.1, 0.2, 0.5, 1, 2]:
        V = np.diag(sy2 * lam ** 2 / lag ** 2)
        C = s2 * np.eye(len(S)) + As @ V @ As.T
        sign, ld = np.linalg.slogdet(C)
        ll = -0.5 * (ld + yc @ np.linalg.solve(C, yc))
        if best is None or ll > best[0]:
            best = (ll, lam, V)
    V = best[2]
    P = np.linalg.inv(As.T @ As / s2 + np.linalg.inv(V))
    beta = P @ As.T @ yc / s2
    return ((row(o) - am) / asd) @ beta + ym


MODELS = {"DFM": f_dfm, "BVAR": f_bvar, "LASSO": f_lasso, "ARDL": f_ardl}
first_origin = idx["2013T1"]
last_origin = len(qs) - 2
rec = []
for o in range(first_origin, last_origin + 1):
    r = {"origen": qs[o], "objetivo": qs[o + 1], "y": Y[o + 1]}
    for k, f in {**MODELS, "AR4": f_ar4, "ECM": f_ecm, "RW": f_rw}.items():
        r[k] = f(o)
    rec.append(r)
R = pd.DataFrame(rec)
R["COMB"] = R[list(MODELS)].mean(1)
E = {k: (R.y - R[k]).values for k in list(MODELS) + ["AR4", "ECM", "RW", "COMB"]}
P = len(R)
mse = {k: float(np.mean(v ** 2)) for k, v in E.items()}
ratio = {k: mse[k] / mse["AR4"] for k in mse}

d = E["AR4"] ** 2 - E["COMB"] ** 2  # >0 si la combinacion mejora
dbar = d.mean()
var = np.sum((d - dbar) ** 2) / P  # gamma0 (h=1)
dm = dbar / np.sqrt(var / P)
hln = dm * np.sqrt((P + 1 - 2 + 0) / P)
pval = float(1 - stats.t.cdf(hln, P - 1))

# comparacion
REF = {"P": 51, "razon_ecm": 1.70, "p_dm": 0.894}
rel = abs(ratio["COMB"] - REF["razon_ecm"]) / REF["razon_ecm"]
mismo_P = P == REF["P"]
concl = (pval < 0.05) == (REF["p_dm"] < 0.05)
veredicto = "COINCIDE" if (mismo_P and rel <= 0.10 and concl) else "DISCREPA"
res = {
    "rama": "v16/replica", "pregunta": "H5 (P9) replica ciega", "capa": "C4 predictivo",
    "datos": "data/processed/v15/p9_prediccion.parquet, p2_fundamentales.parquet",
    "N": P, "metodo": "combinacion media simple DFM+BVAR+LASSO+ARDL vs AR(4); h=1; expansiva; DM-HLN unilateral",
    "estimacion": {"razon_ECM_comb_AR4": ratio["COMB"], "ECM": mse, "razones": ratio, "DM_HLN_t": float(hln)},
    "ic95": None, "p_ajustado": None, "p_dm_hln_unilateral": pval,
    "nivel_evidencia": "DESCRIPTIVO", "primer_origen": qs[first_origin], "primer_objetivo": R.objetivo.iloc[0],
    "ultimo_objetivo": R.objetivo.iloc[-1],
    "comparacion": {"referencia": REF, "P_igual": mismo_P, "dif_rel_razon": rel,
                    "conclusion_5pct_igual": concl, "veredicto": veredicto},
    "notas": "SEED=20261010; sin sellada.",
}
(OUT / "resultado.json").write_text(json.dumps(res, indent=2, ensure_ascii=False))
R.to_csv(OUT / "errores.csv", index=False)
print(json.dumps(res, indent=2, ensure_ascii=False))
