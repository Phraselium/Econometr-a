"""M3b: predicción y ML de la compraventa (precio y volumen por separado). Solo paneles *_train de M0; sin red.
Validación: bloques temporales con embargo (1 año / 4 trimestres), orígenes 2018, 2020, 2022; ajuste de
hiperparámetros con bloques espaciales (5 grupos k-means de centroides) y semilla fija; <=30 configuraciones por familia.
Interpretación descriptiva (C4): sin lectura causal. Un hilo, SEED=20261010.
"""
from __future__ import annotations

import json
import os
import sys
import warnings
from datetime import date
from itertools import combinations
from pathlib import Path

import joblib
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402
from scipy.stats import spearmanr  # noqa: E402

RAIZ = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(RAIZ / "src"))
sys.path.insert(0, str(RAIZ / "src/v6"))
import lightgbm as lgb  # noqa: E402
import m3b_lib as L  # noqa: E402
import shap  # noqa: E402
import statsmodels.api as sm  # noqa: E402
from econ_utils import Registry  # noqa: E402
from sklearn.cluster import KMeans  # noqa: E402
from sklearn.ensemble import RandomForestRegressor  # noqa: E402
from statsmodels.stats.outliers_influence import variance_inflation_factor  # noqa: E402

warnings.filterwarnings("ignore")
SEED = L.SEED
np.random.seed(SEED)
SMOKE = os.environ.get("SMOKE") == "1"
OUT = RAIZ / "output/v6/M3B" if not SMOKE else RAIZ / "output/v6/M3B/_smoke"
PAN = RAIZ / "output/v6/M0/paneles"
for sub in ("modelos", "figuras", "tablas"):
    (OUT / sub).mkdir(parents=True, exist_ok=True)
NCFG = 3 if SMOKE else 30
NCFG_DL = 2 if SMOKE else 8
ORIGS = [2018, 2020, 2022]
REG = Registry(OUT / "registro.csv")
CP_REG = ["ln_pob", "share_ext_pob", "ln_pib_pc", "paro_tasa", "ln_ocupados_miles", "ln_terminadas_libres",
          "ln_iniciadas_libres", "ln_suelo_pm2_m50k", "ln_vut", "ln_hip_viv_num"]
ADL_ANUAL = ["ln_pib_pc", "paro_tasa", "ln_hip_viv_num", "ln_pob"]
FUENTE_P = "valor tasado MIVAU"


# ====================================================================== datos
def lag(df, unit, time, cols, k=1, suf="_l1"):
    s = df[[unit, time] + cols].copy()
    s[time] = s[time] + k
    return s.rename(columns={c: c + suf for c in cols})


def coords():
    cen = pd.read_csv(RAIZ / "data/raw/v5/municipio_centroides_utm30.csv", dtype={"codigo": str})
    cen["cod"] = cen.codigo.str[:2].astype(int)
    pc = cen.groupby("cod")[["x_m", "y_m"]].mean() / 1e5
    cen = cen.set_index("codigo")[["x_m", "y_m"]] / 1e5
    return pc, cen


def cargar():
    pc, cm = coords()
    ca = pd.read_csv(PAN / "prov_compra_anual_train.csv.gz")
    tr = pd.read_csv(PAN / "prov_trim_compra_train.csv.gz")
    nac = pd.read_csv(PAN / "nacional_trim_desc.csv")
    mu = pd.read_csv(PAN / "mun_compra_anual_train.csv.gz")
    est = pd.read_csv(PAN / "prov_estatico.csv", dtype={"cod": int})
    mest = pd.read_csv(PAN / "mun_estatico.csv", dtype={"cod_mun": str})
    return pc, cm, ca, tr, nac, mu, est, mest


def grupos_espaciales(units, xy, k=5):
    km = KMeans(n_clusters=k, n_init=10, random_state=SEED).fit(xy)
    return dict(zip(units, km.labels_.tolist()))


def S_trim(y, other, tr, nac, pc, nombre, mercado, medida, mp):
    tr = tr.copy()
    tr["q"] = tr.anio * 4 + tr.t.str[-1].astype(int) - 1
    nac = nac.copy()
    nac["q"] = nac.t.str[:4].astype(int) * 4 + nac.t.str[-1].astype(int) - 1
    nac["ln_cred_nuevas"] = np.log(nac.credito_viv_nuevas_mill_eur)
    d = tr.merge(nac[["q", "tipo_hip_ecb_pct", "ln_cred_nuevas"]], on="q", how="left").sort_values(["cod", "q"]).reset_index(drop=True)
    g = d.groupby("cod")
    D = pd.DataFrame({"unit": d.cod, "time": d.q, "y": d[y], "qtr": d.q % 4, "prov": d.cod})
    for k in range(1, 5):
        D[f"y{k}"] = g[y].shift(k)
    D["dy"] = D.y - D.y1
    D["dy1"] = D.y1 - D.y2
    nx = ["ln_hip_viv_num", "ln_ipc_alq_idx", "tipo_hip_ecb_pct", "ln_cred_nuevas"]
    for v in nx:
        D[v] = d[v]
        gg = D.groupby("unit")[v]
        D[v + "_l1"] = gg.shift(1)
        D["d_" + v + "_l1"] = gg.shift(1) - gg.shift(2)
    D["other_l1"] = d.groupby("cod")[other].shift(1).to_numpy()
    D = D.dropna().reset_index(drop=True)  # misma muestra que M1b
    D["x"] = D.unit.map(pc.x_m)
    D["yc"] = D.unit.map(pc.y_m)
    X1 = [v + "_l1" for v in nx]
    feats = ["y1", "y2", "y3", "y4", "dy1"] + X1 + ["other_l1", "qtr", "x", "yc"]
    fam = {"rezagos_propios": ["y1", "y2", "y3", "y4", "dy1"], "credito_hipotecas_precio_alq": ["ln_hip_viv_num_l1", "ln_ipc_alq_idx_l1", "other_l1"],
           "nacional_tipos_credito": ["tipo_hip_ecb_pct_l1", "ln_cred_nuevas_l1"], "calendario": ["qtr"], "geografia": ["x", "yc"]}
    base = {"AR": (["y1", "y2", "y3", "y4"], "y"), "ECMv1": (["y1"] + X1 + ["dy1"] + ["d_" + v for v in X1], "dy"),
            "M1b_ADL": (["y1", "y2", "y3", "y4"] + X1, "y")}
    return dict(id=nombre, mercado=mercado, nivel="provincia (trimestral)", medida=y, medida_precio=mp, D=D, feats=feats, fam=fam, base=base,
                ref="AR", ref_adl="M1b_ADL", gap=4, span=8, mult=4, nunit=D.unit.nunique(), fuente=medida, freq="trimestral", pc=pc)


def S_anual(y, other, ca, pc, nombre, mercado, mp, medida):
    ca = ca.copy()
    regs = CP_REG
    lg = lag(ca, "cod", "anio", regs + [other])
    D = ca[["cod", "anio", y]].rename(columns={"cod": "unit", "anio": "time", y: "y"}).merge(
        lg.rename(columns={"cod": "unit", "anio": "time"}), on=["unit", "time"], how="left")
    D = D.merge(lag(ca, "cod", "anio", [y], suf="").rename(columns={"cod": "unit", "anio": "time", y: "y1"}), on=["unit", "time"], how="left")
    D = D.dropna(subset=["y", "y1"] + [a + "_l1" for a in ADL_ANUAL]).sort_values(["unit", "time"]).reset_index(drop=True)
    D["prov"] = D.unit
    D["x"] = D.unit.map(pc.x_m)
    D["yc"] = D.unit.map(pc.y_m)
    D = D.rename(columns={other + "_l1": "other_l1"})
    feats = ["y1"] + [c + "_l1" for c in regs] + ["other_l1", "x", "yc"]
    fam = {"rezagos_propios": ["y1"], "demanda_poblacion": ["ln_pob_l1", "share_ext_pob_l1", "ln_vut_l1"],
           "renta_empleo": ["ln_pib_pc_l1", "paro_tasa_l1", "ln_ocupados_miles_l1"],
           "oferta_suelo": ["ln_terminadas_libres_l1", "ln_iniciadas_libres_l1", "ln_suelo_pm2_m50k_l1"],
           "credito_hipotecas": ["ln_hip_viv_num_l1", "other_l1"], "geografia": ["x", "yc"]}
    base = {"AR": (["y1"], "y"), "M1b_ADL": (["y1"] + [a + "_l1" for a in ADL_ANUAL], "y")}
    return dict(id=nombre, mercado=mercado, nivel="provincia (anual)", medida=y, medida_precio=mp, D=D, feats=feats, fam=fam, base=base,
                ref="AR", ref_adl="M1b_ADL", gap=1, span=2, mult=1, nunit=D.unit.nunique(), fuente=medida, freq="anual", pc=pc)


def S_mun(mu, ca, pc, cm, mest):
    mu = mu.copy()
    mu["cod_prov"] = mu.cod_prov.astype(int)
    mu["unit"] = mu.cod_mun.astype(int).map(lambda c: f"{c:05d}")
    mu = mu.dropna(subset=["ln_pm2_tasado_mun"]).rename(columns={"anio": "time", "ln_pm2_tasado_mun": "y"})
    ly = lag(mu, "unit", "time", ["y"], suf="")
    ly = ly.rename(columns={"y": "y1"})
    D = mu.merge(ly, on=["unit", "time"], how="left")
    regs = ["ln_pob", "share_ext_pob", "ln_pib_pc", "paro_tasa", "ln_ocupados_miles", "ln_terminadas_libres", "ln_iniciadas_libres", "ln_vut", "ln_hip_viv_num", "ln_pm2_tasado"]
    lg = lag(ca, "cod", "anio", regs).rename(columns={"cod": "cod_prov", "anio": "time", "ln_pm2_tasado_l1": "prov_y1"})
    D = D.merge(lg, on=["cod_prov", "time"], how="left")
    D = D.dropna(subset=["y1"] + [a + "_l1" for a in ADL_ANUAL]).sort_values(["unit", "time"]).reset_index(drop=True)
    D["prov"] = D.cod_prov
    D["gap_prov"] = D.y1 - D.prov_y1
    D["x"] = D.unit.map(cm.x_m)
    D["yc"] = D.unit.map(cm.y_m)
    D["dist_centro_km"] = D.unit.map(mest.set_index("cod_mun").dist_centro_km)
    pcv = D.cod_prov.map(pc.x_m)
    D = D[pcv.notna() & D.x.notna()].reset_index(drop=True)
    feats = ["y1", "prov_y1", "gap_prov"] + [r + "_l1" for r in regs[:-1]] + ["x", "yc", "dist_centro_km"]
    fam = {"rezagos_propios": ["y1", "gap_prov"], "precio_provincial": ["prov_y1"], "demanda_poblacion": ["ln_pob_l1", "share_ext_pob_l1", "ln_vut_l1"],
           "renta_empleo": ["ln_pib_pc_l1", "paro_tasa_l1", "ln_ocupados_miles_l1"], "oferta": ["ln_terminadas_libres_l1", "ln_iniciadas_libres_l1"],
           "credito_hipotecas": ["ln_hip_viv_num_l1"], "geografia": ["x", "yc", "dist_centro_km"]}
    base = {"AR": (["y1"], "y"), "M1b_ADL": (["y1"] + [a + "_l1" for a in ADL_ANUAL], "y")}
    return dict(id="MUN_PRECIO_ANUAL", mercado="compra (precio)", nivel="municipio (anual)", medida="ln_pm2_tasado_mun", medida_precio=FUENTE_P + " municipal",
                D=D, feats=feats, fam=fam, base=base, ref="AR", ref_adl="M1b_ADL", gap=1, span=2, mult=1, nunit=D.unit.nunique(),
                fuente=FUENTE_P + " municipal", freq="anual", pc=pc, cm=cm)


# ====================================================================== familias y presupuesto de hiperparámetros
def cfgs(fam):
    rng = np.random.default_rng({"RF": 1, "GB": 2, "BBF": 3, "MLP": 4, "GCN": 5}[fam] + SEED)
    out = []
    for _ in range(NCFG_DL if fam in ("MLP", "GCN") else NCFG):
        if fam == "RF":
            out.append(dict(max_depth=int(rng.choice([2, 3, 4, 6, 8, 12])), min_samples_leaf=int(rng.choice([1, 3, 5, 10, 20])),
                            max_features=float(rng.choice([0.3, 0.5, 0.7, 1.0]))))
        elif fam == "GB":
            out.append(dict(num_leaves=int(rng.choice([3, 4, 7, 15])), learning_rate=float(rng.choice([0.02, 0.05, 0.1])),
                            n_estimators=int(rng.choice([50, 100, 200, 400])), min_child_samples=int(rng.choice([5, 10, 20, 30])),
                            subsample=float(rng.choice([0.7, 0.85, 1.0])), colsample_bytree=float(rng.choice([0.5, 0.7, 1.0])),
                            reg_lambda=float(rng.choice([0.0, 1.0, 10.0]))))
        elif fam == "BBF":
            out.append(dict(max_depth=int(rng.choice([2, 3, 4, 5])), min_samples_leaf=int(rng.choice([3, 5, 10, 20])),
                            max_features=float(rng.choice([0.5, 0.7, 1.0])), n_trees=int(rng.choice([50, 100]))))
        else:
            out.append(dict(hidden=int(rng.choice([16, 32, 64])), dropout=float(rng.choice([0.0, 0.1, 0.3])),
                            wd=float(rng.choice([1e-4, 1e-3, 1e-2])), lr=float(rng.choice([1e-3, 3e-3, 1e-2])), epochs=int(rng.choice([100, 200]))))
    return out


def make(fam, c):
    if fam == "RF":
        return RandomForestRegressor(n_estimators=20 if SMOKE else 150, random_state=SEED, n_jobs=1, **c)
    if fam == "GB":
        return lgb.LGBMRegressor(random_state=SEED, n_jobs=1, verbose=-1, deterministic=True, force_row_wise=True, subsample_freq=1, **c)
    if fam == "BBF":
        return L.BBF(seed=SEED, **c)
    return L.Tab(seed=SEED, **c)


def tune(fam, X, y, g, nunit_grp):
    """Selección por bloques espaciales (grupos k-means) dentro del entrenamiento. Devuelve (mejor cfg, rmse por cfg)."""
    cs = cfgs(fam)
    ug = np.unique(g)
    sc = []
    for c in cs:
        e = []
        for k in ug:
            te = g == k
            if te.sum() == 0 or (~te).sum() < 10:
                continue
            m = make(fam, c).fit(X[~te], y[~te])
            e.append(((m.predict(X[te]) - y[te]) ** 2).mean())
        sc.append(float(np.sqrt(np.mean(e))))
    return cs[int(np.argmin(sc))], sc, cs


# ====================================================================== hierárquico (MixedLM, sustituto declarado de PyMC/NumPyro)
def mixed(trn, val, ret=False):
    cov = ["y1"] + [a + "_l1" for a in ADL_ANUAL[:3]]
    mu_ = trn[cov].mean()
    T, V = trn.copy(), val.copy()
    T["dy"] = T.y - T.y1
    T[cov] = T[cov] - mu_
    V[cov] = V[cov] - mu_
    md = sm.MixedLM.from_formula("dy ~ " + " + ".join(cov), groups="prov", re_formula="~ y1 + ln_pib_pc_l1", vc_formula={"mun": "0 + C(unit)"}, data=T)
    r = md.fit(reml=True, method=["lbfgs"], maxiter=200)
    fe = r.fe_params
    pr = fe["Intercept"] + V[cov].to_numpy() @ fe[cov].to_numpy()
    re = r.random_effects
    add = np.zeros(len(V))
    for i, (p, y1c, pib) in enumerate(zip(V.prov, V.y1, V.ln_pib_pc_l1)):
        if p in re:
            s = re[p]
            add[i] = s.get("prov", 0) + s.get("y1", 0) * y1c + s.get("ln_pib_pc_l1", 0) * pib
    out = val.y1.to_numpy() + pr + add
    return (out, r, re) if ret else out


# ====================================================================== DL municipal
def tensor_mun(S, ref_rows):
    D = S["D"]
    units = sorted(D.unit.unique())
    times = sorted(D.time.unique())
    ui = {u: i for i, u in enumerate(units)}
    ti = {t: i for i, t in enumerate(times)}
    D["ni"] = D.unit.map(ui)
    D["ti"] = D.time.map(ti)
    xy = np.array([[S["cm"].loc[u, "x_m"], S["cm"].loc[u, "y_m"]] for u in units])
    return units, times, L.knn_adj(xy, 5)


def gcn_arrays(S, rows, med, mu, sd, T, N):
    D = S["D"]
    F = len(S["feats"])
    X = np.zeros((T, N, F), np.float32)
    Y = np.zeros((T, N), np.float32)
    M = np.zeros((T, N), bool)
    Xr = D[S["feats"]].to_numpy(float)
    Xr = (np.where(np.isnan(Xr), med, Xr) - mu) / sd
    X[D.ti.to_numpy(), D.ni.to_numpy()] = Xr
    Y[D.ti.to_numpy(), D.ni.to_numpy()] = (D.y - D.y1).to_numpy()
    M[D.ti.to_numpy(), D.ni.to_numpy()] = False
    mrows = D.index.isin(rows)
    M[D.ti.to_numpy()[mrows], D.ni.to_numpy()[mrows]] = True
    return X, Y, M


def gcn_fold(S, A, T, N, trn, val, cfg, grp, inner=False):
    D = S["D"]
    Xtr = trn[S["feats"]].to_numpy(float)
    med = np.nan_to_num(np.nanmedian(Xtr, 0))
    Xf = np.where(np.isnan(Xtr), med, Xtr)
    mu, sd = Xf.mean(0), Xf.std(0)
    sd = np.where(sd < 1e-6, 1.0, sd)
    X, Y, M = gcn_arrays(S, trn.index, med, mu, sd, T, N)
    gm = lambda rows: (D.loc[rows, "ti"].to_numpy(), D.loc[rows, "ni"].to_numpy())  # noqa: E731
    ys = float(np.std(Y[M]) + 1e-9)
    if not inner:
        m = L.GCN(A, seed=SEED, **cfg).fit(X, Y / ys, M)
        P = m.predict(X) * ys
        return P[gm(val.index)]
    sc = []
    for k in np.unique(grp):
        te = grp == k
        tr_idx = trn.index[~te]
        Mk = np.zeros_like(M)
        a, b = gm(tr_idx)
        Mk[a, b] = True
        m = L.GCN(A, seed=SEED, **cfg).fit(X, Y / ys, Mk)
        P = m.predict(X) * ys
        a, b = gm(trn.index[te])
        sc.append(((P[a, b] - (trn.y - trn.y1)[te].to_numpy()) ** 2).mean())
    return float(np.sqrt(np.mean(sc)))


# ====================================================================== bucle de validación
def split(S, orig):
    D = S["D"]
    o = orig * S["mult"]
    trn = D[D.time < o - S["gap"]]
    val = D[(D.time >= o) & (D.time < o + S["span"])]
    val = val[val.unit.isin(set(trn.unit))]
    return trn, val


def pdp_family_perm(model, Xv, yv, fam, rng, nrep=10):
    base = np.sqrt(((model.predict(Xv) - yv) ** 2).mean())
    out = {}
    for g, cols in fam.items():
        idx = [Xv.columns.get_loc(c) for c in cols if c in Xv.columns]
        ds = []
        for _ in range(nrep):
            Z = Xv.copy()
            perm = rng.permutation(len(Z))
            Z.iloc[:, idx] = Xv.iloc[perm, idx].to_numpy()
            ds.append(np.sqrt(((model.predict(Z) - yv) ** 2).mean()) - base)
        out[g] = float(np.mean(ds))
    return out


def evaluar(S, hp_log):
    D = S["D"]
    units = sorted(D.unit.unique())
    xy = np.array([[S["pc"].loc[u, "x_m"], S["pc"].loc[u, "y_m"]] if S["nivel"].startswith("prov") else [S["cm"].loc[u, "x_m"], S["cm"].loc[u, "y_m"]] for u in units])
    gmap = grupos_espaciales(units, xy, 5)
    S["gmap"] = gmap
    fams = ["RF", "GB", "BBF"]
    mun = S["id"] == "MUN_PRECIO_ANUAL"
    if mun:
        S["units"], S["times"], A = tensor_mun(S, None)
    pred = {}  # modelo -> list de arrays
    meta = []
    fold_models = []
    score_cfg = {f: [] for f in fams + (["MLP", "GCN"] if mun else [])}
    cfg_sel = {}
    for orig in ORIGS:
        trn, val = split(S, orig)
        meta.append(val[["unit", "time", "prov"]].assign(fold=orig, y=val.y.to_numpy(), y1=val.y1.to_numpy()))
        # --- líneas base
        pred.setdefault("persistencia", []).append(val.y1.to_numpy())
        if S["freq"] == "trimestral":
            pred.setdefault("estacional_y_t-4", []).append(val.y4.to_numpy())
        for b, (xs, tg) in S["base"].items():
            pred.setdefault(b, []).append(L.fe_baseline(trn, val, xs, tg))
        Xtr, ytr = trn[S["feats"]].to_numpy(float), (trn.y - trn.y1).to_numpy()
        Xv = val[S["feats"]]
        g = trn.unit.map(gmap).to_numpy()
        fm = {}
        for f in fams:
            c, sc, cs = tune(f, Xtr, ytr, g, 5)
            score_cfg[f].append(sc)
            cfg_sel[(f, orig)] = c
            m = make(f, c).fit(Xtr, ytr)
            pred.setdefault(f, []).append(val.y1.to_numpy() + m.predict(Xv.to_numpy(float)))
            fm[f] = m
        fold_models.append((orig, trn, val, fm))
        if mun:
            try:
                pred.setdefault("MixedLM_jerarquico", []).append(mixed(trn, val))
            except Exception as e:  # noqa: BLE001
                print("MixedLM falló", orig, e)
                pred.setdefault("MixedLM_jerarquico", []).append(np.full(len(val), np.nan))
            Tn, Nn = len(S["times"]), len(S["units"])
            cm_ = cfgs("MLP")
            sc = []
            for c in cm_:
                e = []
                for k in np.unique(g):
                    te = g == k
                    mm = L.Tab(seed=SEED, **c).fit(Xtr[~te], ytr[~te])
                    e.append(((mm.predict(Xtr[te]) - ytr[te]) ** 2).mean())
                sc.append(float(np.sqrt(np.mean(e))))
            score_cfg["MLP"].append(sc)
            cb = cm_[int(np.argmin(sc))]
            mm = L.Tab(seed=SEED, n_seeds=3, **cb).fit(Xtr, ytr)
            pred.setdefault("DL_MLP_tabular", []).append(val.y1.to_numpy() + mm.predict(Xv.to_numpy(float)))
            cg = cfgs("GCN")
            sc = [gcn_fold(S, A, Tn, Nn, trn, val, c, g, inner=True) for c in cg]
            score_cfg["GCN"].append(sc)
            cb = cg[int(np.argmin(sc))]
            pred.setdefault("DL_GCN_espacial", []).append(val.y1.to_numpy() + gcn_fold(S, A, Tn, Nn, trn, val, cb, g))
    for f, arr in score_cfg.items():
        arr = np.array(arr)  # folds x cfg
        cs = cfgs(f)
        for i, c in enumerate(cs):
            hp_log.append(dict(setting=S["id"], familia=f, cfg=i, params=json.dumps(c, sort_keys=True), rmse_interno_medio=float(arr[:, i].mean())))
    M = pd.concat(meta).reset_index(drop=True)
    P = {k: np.concatenate(v) for k, v in pred.items()}
    return M, P, fold_models, cfg_sel


def metricas(S, M, P):
    rows = []
    err = {k: M.y.to_numpy() - v for k, v in P.items()}
    agg = {k: pd.Series(e ** 2).groupby([M.fold.to_numpy(), M.time.to_numpy()]).mean().to_numpy() for k, e in err.items()}
    lvl = float(np.exp(S["D"].y).mean())
    for k, e in err.items():
        ok = ~np.isnan(e)
        rm = float(np.sqrt(np.nanmean(e ** 2)))
        r = dict(setting=S["id"], modelo=k, n_val=int(ok.sum()), rmse_ln=rm, rmse_pct=100 * (np.exp(rm) - 1), mae_ln=float(np.nanmean(np.abs(e))),
                 rmse_abs=lvl * rm, n_periodos_DM=len(agg[k]))
        for rf in ("persistencia", S["ref"], S["ref_adl"], "ECMv1", "GB"):
            if rf in P and rf != k and not np.isnan(agg[k]).any():
                d = L.dm_hln(agg[k], agg[rf], 1)
                r[f"dm_vs_{rf}"], r[f"p_vs_{rf}"] = d["DM"], d["p"]
        rows.append(r)
    t = pd.DataFrame(rows)
    for rf in ("persistencia", S["ref"], S["ref_adl"]):
        c = f"p_vs_{rf}"
        if c in t:
            m = t[c].notna()
            t.loc[m, c + "_BH"] = L.bh(t.loc[m, c].to_numpy())
    # por pliegue
    pf = []
    for k, e in err.items():
        for fo in ORIGS:
            mk = (M.fold == fo).to_numpy()
            pf.append(dict(setting=S["id"], modelo=k, fold=fo, rmse_ln=float(np.sqrt(np.nanmean(e[mk] ** 2)))))
    return t, pd.DataFrame(pf)


# ====================================================================== interpretación (descriptiva, C4)
def interpretar(S, fold_models, cfg_full, Xfull, yfull, gfull):
    D = S["D"]
    feats = S["feats"]
    ID = S["id"]
    rng = np.random.default_rng(SEED)
    # modelo GB final sobre todo el entrenamiento
    gb = make("GB", cfg_full["GB"]).fit(Xfull.to_numpy(float), yfull)
    pf = lambda Z: gb.predict(Z[feats].to_numpy(float) if hasattr(Z, "columns") else Z)  # noqa: E731
    sv = shap.TreeExplainer(gb).shap_values(Xfull.to_numpy(float))
    sh = pd.DataFrame(np.abs(sv), columns=feats)
    sh["prov"] = D.prov.to_numpy()
    sh_prov = sh.groupby("prov")[feats].mean()
    sh_prov["total"] = sh_prov.sum(1)
    sh_prov.to_csv(OUT / f"tablas/shap_por_provincia_{ID}.csv")
    top = sh[feats].mean().sort_values(ascending=False)
    # estabilidad entre pliegues: SHAP medio absoluto y permutación agrupada por pliegue
    vecs, perms = [], []
    for orig, trn, val, fm in fold_models:
        m = fm["GB"]
        v = np.abs(shap.TreeExplainer(m).shap_values(trn[feats].to_numpy(float))).mean(0)
        vecs.append(v)
        perms.append(pdp_family_perm(m, val[feats], (val.y - val.y1).to_numpy(), S["fam"], rng))
    est = [spearmanr(a, b)[0] for a, b in combinations(vecs, 2)]
    pp = pd.DataFrame(perms, index=[f[0] for f in fold_models])
    pp.to_csv(OUT / f"tablas/permutacion_agrupada_{ID}.csv")
    pp_rank = [spearmanr(pp.iloc[i], pp.iloc[j])[0] for i, j in combinations(range(len(pp)), 2)]
    # VIF (colinealidad)
    Z = Xfull.copy()
    Z = Z.fillna(Z.median())
    Z = Z.loc[:, Z.std() > 0]
    Z = (Z - Z.mean()) / Z.std()
    vif = pd.Series([variance_inflation_factor(Z.to_numpy(), i) for i in range(Z.shape[1])], index=Z.columns, name="VIF")
    vif.to_csv(OUT / f"tablas/vif_{ID}.csv")
    # ALE y PDP de las 3 variables con más SHAP
    ale, pdp = {}, {}
    for c in top.index[:3]:
        a = L.ale_1d(lambda Z_: gb.predict(Z_[feats].to_numpy(float)), Xfull, c)
        p = L.pdp_1d(lambda Z_: gb.predict(Z_[feats].to_numpy(float)), Xfull, c)
        if a is not None:
            a.to_csv(OUT / f"tablas/ale_{ID}_{c}.csv", index=False)
            ale[c] = a
        p.to_csv(OUT / f"tablas/pdp_{ID}_{c}.csv", index=False)
        pdp[c] = p
    # figura determinista
    fig, ax = plt.subplots(2, 2, figsize=(11, 8))
    pp.mean().sort_values().plot.barh(ax=ax[0, 0], xerr=pp.std().reindex(pp.mean().sort_values().index))
    ax[0, 0].set_title("Permutación agrupada: aumento de RMSE (ln), media y sd entre pliegues", fontsize=8)
    sh_prov["total"].sort_values().tail(15).plot.barh(ax=ax[0, 1])
    ax[0, 1].set_title("|SHAP| medio total por provincia (cod), 15 mayores", fontsize=8)
    for j, c in enumerate(list(ale)[:2]):
        a_ = ale[c]
        ax[1, j].plot(a_.x, a_.ale, label="ALE")
        ax[1, j].plot(pdp[c].x, pdp[c].pdp - pdp[c].pdp.mean(), "--", label="PDP centrado")
        ax[1, j].set_title(f"{c}", fontsize=8)
        ax[1, j].legend(fontsize=7)
    fig.suptitle(f"{ID}: descriptivo (C4), sin lectura causal; VIF máx {vif.max():.0f}", fontsize=9)
    fig.tight_layout()
    fig.savefig(OUT / f"figuras/interpretacion_{ID}.png", dpi=110, metadata={"Software": None})
    plt.close(fig)
    return dict(top_shap=top.head(5).round(4).to_dict(), spearman_shap_entre_pliegues=[round(float(x), 3) for x in est],
                spearman_perm_entre_pliegues=[round(float(x), 3) for x in pp_rank], vif_max=float(vif.max()), vif_n_gt10=int((vif > 10).sum()),
                vif_top=vif.sort_values(ascending=False).head(4).round(1).to_dict(), aviso_colinealidad="VIF>10 en %d de %d variables" % ((vif > 10).sum(), len(vif)))


# ====================================================================== principal
def main():
    pc, cm, ca, tr, nac, mu, est, mest = cargar()
    settings = [
        S_trim("ln_pm2_tasado", "ln_cv_etdp", tr, nac, pc, "PROV_PRECIO_TRIM", "compra (precio)", FUENTE_P, FUENTE_P),
        S_trim("ln_cv_etdp", "ln_pm2_tasado", tr, nac, pc, "PROV_VOL_TRIM", "compra (volumen)", "compraventas INE ETDP", None),
        S_anual("ln_pm2_tasado", "ln_cv_etdp", ca, pc, "PROV_PRECIO_ANUAL", "compra (precio)", FUENTE_P, FUENTE_P),
        S_anual("ln_cv_etdp", "ln_pm2_tasado", ca, pc, "PROV_VOL_ANUAL", "compra (volumen)", None, "compraventas INE ETDP"),
        S_anual("ln_pm2_registradores", "ln_cv_etdp", ca, pc, "PROV_PRECIO_ANUAL_REGISTRADORES", "compra (precio)", "Registradores (robustez)", "Registradores pm2"),
        S_mun(mu, ca, pc, cm, mest),
    ]
    hp_log, met, pfold, interp, finales, regs_cfg = [], [], [], {}, [], {}
    for S in settings:
        print(S["id"], len(S["D"]), flush=True)
        M, P, fmod, sel = evaluar(S, hp_log)
        t, pf = metricas(S, M, P)
        met.append(t)
        pfold.append(pf)
        D = S["D"]
        Xfull = D[S["feats"]]
        yfull = (D.y - D.y1).to_numpy()
        gfull = D.unit.map(S["gmap"]).to_numpy()
        # selección y ajuste finales con TODO el entrenamiento
        cfg_full, fams_fit = {}, {}
        for f in ("RF", "GB", "BBF"):
            c, _, _ = tune(f, Xfull.to_numpy(float), yfull, gfull, 5)
            cfg_full[f] = c
            fams_fit[f] = make(f, c).fit(Xfull.to_numpy(float), yfull)
        interp[S["id"]] = interpretar(S, fmod, cfg_full, Xfull, yfull, gfull)
        cand = t[t.modelo.isin(["RF", "GB", "BBF"])].sort_values("rmse_ln").iloc[0]
        fam_f = cand.modelo
        nombre = {"RF": "random_forest", "GB": "lightgbm", "BBF": "bosque_bootstrap_bayesiano"}[fam_f]
        mid = f"{S['id']}__{nombre}"
        ruta = OUT / "modelos" / f"{mid}.joblib"
        spec = dict(id=mid, setting=S["id"], familia=nombre, sustituto_de="BART" if fam_f == "BBF" else None, hiperparametros=cfg_full[fam_f],
                    features=S["feats"], objetivo=f"delta = {S['medida']}_t - y_(t-1); prediccion de nivel = y1 + modelo(features)", semilla=SEED,
                    entrenamiento=f"{S['freq']} {int(D.time.min())}-{int(D.time.max())}, N={len(D)}", capa="C4",
                    predecir="m3b_run.predecir(ruta, df_features) -> delta; sumar y1")
        joblib.dump(dict(model=fams_fit[fam_f], spec=spec), ruta, compress=0)
        ls = t[t.modelo == S["ref"]].rmse_ln.iloc[0]
        finales.append(dict(id=mid, mercado=S["mercado"], nivel=S["nivel"], medida=S["medida"], medida_precio=S["medida_precio"],
                            ruta=str(ruta.relative_to(RAIZ)), familia=nombre, rmse_ln_cv_bloques=float(cand.rmse_ln), rmse_ln_linea_base=float(ls),
                            bate_linea_base_rmse=bool(cand.rmse_ln < ls), linea_base=S["ref"],
                            rmse_ln_persistencia=float(t[t.modelo == "persistencia"].rmse_ln.iloc[0]),
                            bate_persistencia_rmse=bool(cand.rmse_ln < t[t.modelo == "persistencia"].rmse_ln.iloc[0]),
                            p_dm_vs_persistencia=float(cand.get("p_vs_persistencia", np.nan)), p_dm_vs_M1b_ADL=float(cand.get("p_vs_M1b_ADL", np.nan)), p_dm_vs_ref=float(cand.get(f"p_vs_{S['ref']}", np.nan)), especificacion=spec))
        if S["id"] == "MUN_PRECIO_ANUAL":
            _, r, re = mixed(D, D.iloc[-5:], ret=True)
            pd.DataFrame({k: v for k, v in re.items()}).T.to_csv(OUT / "tablas/jerarquico_efectos_por_provincia.csv")
            r.summary().tables[1].to_csv(OUT / "tablas/jerarquico_efectos_fijos.csv")
            interp["jerarquico"] = dict(sustituto="MixedLM (statsmodels) en lugar de PyMC/NumPyro (no instalados)", re_cov=r.cov_re.round(5).to_dict(), converged=bool(r.converged))
        for _, rw in t.iterrows():
            REG.log("OOS", f"{S['id']}|{rw.modelo}", f"{rw.modelo} bloques+embargo {S['gap']}{'a' if S['mult'] == 1 else 'tr'}, orígenes 2018/20/22", D.time.min(), D.time.max(),
                    int(rw.n_val), np.nan, np.nan, np.nan, rw.rmse_ln, rw.get(f"dm_vs_{S['ref']}", np.nan), rw.get(f"p_vs_{S['ref']}", np.nan),
                    json.dumps(dict(mae_ln=round(rw.mae_ln, 5), medida_precio=S["medida_precio"], p_BH=float(rw.get(f"p_vs_{S['ref']}_BH", np.nan))), ensure_ascii=False))
    hp = pd.DataFrame(hp_log)
    hp.to_csv(OUT / "tablas/hiperparametros_presupuesto.csv", index=False)
    for _, r in hp.iterrows():
        REG.log("HP", f"{r.setting}|{r.familia}|cfg{r.cfg}", r.params, "", "", 0, np.nan, np.nan, np.nan, r.rmse_interno_medio, np.nan, np.nan, "bloques espaciales internos")
    T = pd.concat(met)
    T.to_csv(OUT / "tablas/modelos_metricas.csv", index=False)
    pd.concat(pfold).to_csv(OUT / "tablas/rmse_por_pliegue.csv", index=False)
    REG.flush()
    json.dump(finales, open(OUT / "modelos_finales.json", "w"), indent=1, ensure_ascii=False, default=float)
    json.dump(interp, open(OUT / "tablas/interpretacion_resumen.json", "w"), indent=1, ensure_ascii=False, default=float)
    figura_global(T)
    salidas(T, finales, interp, hp, settings)


def predecir(ruta, df):
    """Carga un modelo final y devuelve el delta previsto sobre ln(y) (sumar y1 para obtener el nivel)."""
    o = joblib.load(ruta)
    return o["model"].predict(df[o["spec"]["features"]].to_numpy(float))


def figura_global(T):
    ids = T.setting.unique()
    fig, ax = plt.subplots(1, len(ids), figsize=(3.2 * len(ids), 4), sharey=False)
    for a, s in zip(np.atleast_1d(ax), ids):
        t = T[T.setting == s].sort_values("rmse_pct")
        a.barh(t.modelo, t.rmse_pct)
        a.set_title(s, fontsize=7)
        a.tick_params(labelsize=6)
    fig.suptitle("RMSE (%) en validación por bloques con embargo (orígenes 2018, 2020, 2022)", fontsize=9)
    fig.tight_layout()
    fig.savefig(OUT / "figuras/rmse_por_modelo.png", dpi=110, metadata={"Software": None})
    plt.close(fig)


def salidas(T, finales, interp, hp, settings):
    hoy = "2026-10-11"  # v6.2: fecha fija de la ejecución de v6 (antes date.today(): la salida cambiaba según el día)
    h = T[T.setting == "PROV_PRECIO_TRIM"].set_index("modelo")
    best = h.loc[[m for m in h.index if m in ("RF", "GB", "BBF")]].rmse_ln.idxmin()
    ar4 = h.loc["AR"]
    resumen = {}
    for s, g in T.groupby("setting"):
        gi = g.set_index("modelo")
        ml = gi.loc[[m for m in gi.index if m in ("RF", "GB", "BBF")]].rmse_ln.idxmin()
        ref = gi.loc["AR"]
        dl = gi.loc[[m for m in gi.index if m.startswith("DL_")]] if any(m.startswith("DL_") for m in gi.index) else None
        resumen[s] = dict(mejor_ML=ml, rmse_pct_mejor_ML=round(float(gi.loc[ml].rmse_pct), 3), rmse_pct_AR=round(float(ref.rmse_pct), 3),
                          rmse_pct_persistencia=round(float(gi.loc["persistencia"].rmse_pct), 3), rmse_pct_ADL=round(float(gi.loc["M1b_ADL"].rmse_pct), 3),
                          dm_vs_AR=float(gi.loc[ml].get("dm_vs_AR", np.nan)), p_dm_vs_AR=float(gi.loc[ml].get("p_vs_AR", np.nan)),
                          dm_vs_ADL=float(gi.loc[ml].get("dm_vs_M1b_ADL", np.nan)), p_dm_vs_ADL=float(gi.loc[ml].get("p_vs_M1b_ADL", np.nan)),
                          rmse_pct_ECMv1=(round(float(gi.loc["ECMv1"].rmse_pct), 3) if "ECMv1" in gi.index else None))
        if dl is not None:
            gbp = gi.loc["GB"].rmse_ln
            resumen[s]["DL"] = {m: dict(rmse_pct=round(float(r.rmse_pct), 3), bate_GB_rmse=bool(r.rmse_ln < gbp),
                                        dm_vs_GB=float(r.get("dm_vs_GB", np.nan)), p_dm_vs_GB=float(r.get("p_vs_GB", np.nan)))
                                for m, r in dl.iterrows()}
            resumen[s]["MixedLM_rmse_pct"] = round(float(gi.loc["MixedLM_jerarquico"].rmse_pct), 3)
    json.dump(resumen, open(OUT / "tablas/resumen_por_setting.json", "w"), indent=1, ensure_ascii=False, default=float)
    res = dict(
        rama="v6/M3b", modulo="M3b", mercado="compra", medida_precio=dict(principal=FUENTE_P, robustez=["Registradores (provincia anual)"],
                                                                         no_usadas="índice triangulado A23 e IPV INE: solo nacional/CCAA, sin panel provincial ni municipal; Notariado: solo C. Valenciana"),
        pregunta="¿Predicen mejor que AR y M1b_ADL, fuera de muestra, el precio y el volumen de la compraventa los modelos de ML, el jerárquico o el DL?",
        capa="C4", datos="output/v6/M0/paneles/{prov_trim_compra,prov_compra_anual,mun_compra_anual}_train; sin muestra sellada",
        N={s.get("id"): int(len(s["D"])) for s in settings}, metodo="RF, LightGBM, bosque bootstrap bayesiano (sustituto de BART), MixedLM (sustituto de PyMC), MLP y GCN (solo municipal); validación por bloques temporales con embargo (orígenes 2018/20/22) y selección por bloques espaciales; DM-HLN",
        estimacion=resumen, ic95=None, p_ajustado="BH sobre las pruebas DM de cada setting (columna p_vs_*_BH en tablas/modelos_metricas.csv)",
        nivel_evidencia="EXPLORATORIO (C4): predicción, no causalidad", diagnosticos=interp,
        fuera_muestra=dict(modelo=best, rmse=float(h.loc[best].rmse_ln), rmse_pct=float(h.loc[best].rmse_pct), setting="PROV_PRECIO_TRIM",
                           rmse_AR4=float(ar4.rmse_ln), dm_vs_ar4=float(h.loc[best].get("dm_vs_AR", np.nan)), p_dm_vs_ar4=float(h.loc[best].get("p_vs_AR", np.nan)),
                           dm_vs_m1b_adl=float(h.loc[best].get("dm_vs_M1b_ADL", np.nan)), p_dm_vs_m1b_adl=float(h.loc[best].get("p_vs_M1b_ADL", np.nan))),
        notas=["Resultado de predicción y exploratorio; SHAP, ALE y dependencia parcial son descriptivos y no admiten lectura causal.",
               "Presupuesto: 30 configuraciones por familia (RF, LightGBM, bosque bootstrap bayesiano) y 8 por red; registro en registro.csv y tablas/hiperparametros_presupuesto.csv.",
               "Paneles anuales: solo 6 periodos de validación para el DM; baja potencia. El pliegue 2018 anual entrena con un único año de objetivo (2016).",
               "Panel municipal: N≈1.9k filas (200 municipios), no 20.000; el DL se evalúa con ese tamaño.",
               "Fecha de ejecución " + hoy])
    json.dump(res, open(OUT / "resultado.json", "w"), indent=1, ensure_ascii=False, default=float)
    hechos = []
    for s, r in resumen.items():
        fe = "2024T4" if "TRIM" in s else "2024"
        for k, lab in (("rmse_pct_mejor_ML", f"RMSE % del mejor ML ({r['mejor_ML']})"), ("rmse_pct_AR", "RMSE % AR"), ("rmse_pct_ADL", "RMSE % M1b_ADL (FE agrupado)")):
            sub = T[(T.setting == s)]
            hechos.append(dict(id=f"m3b_{s}_{k}", indicador=f"{s}: {lab}, validación por bloques con embargo", valor=r[k], min=None, max=None, unidad="% (RMSE de ln)",
                               periodo="orígenes 2018/2020/2022", cobertura=f"{int(sub.n_val.iloc[0])} predicciones", fuentes="MIVAU/INE ETDP (paneles M0 train)", capa="C4",
                               fecha_dato=fe))
    json.dump(hechos, open(OUT / "hechos.json", "w"), indent=1, ensure_ascii=False)



if __name__ == "__main__":
    main()
