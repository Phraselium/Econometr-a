"""Rama BM (modelos predictivos y no lineales): utilidades. Datos SOLO vía v2_common.load; sin red; SEED fijo.

Contenido: construcción de variables por familia (información <= origen t), ajuste/predicción genérico
(elastic net, post-lasso plug-in, RF, LightGBM) con efecto fijo por unidad, PDS grupal (Belloni-Chernozhukov-
Hansen), importancias (permutación agrupada, SHAP vía TreeSHAP, ALE) y proyecciones locales por periodo.
Todo el escalado/imputación se ajusta dentro de cada split con datos de entrenamiento (pos+h <= L).
"""
from __future__ import annotations

import sys
import warnings
from dataclasses import dataclass, field
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))
import v2_common as vc  # noqa: E402

warnings.filterwarnings("ignore")
SEED = vc.SEED
H = 4
OUT = ROOT / "output" / "v2" / "BM"
PERIODOS = {"P1_ajuste": ("2008Q1", "2013Q4"), "P2_recuperacion": ("2014Q1", "2019Q4"),
            "P3_covid": ("2020Q1", "2021Q4"), "P4_tipos": ("2022Q1", "2024Q2")}
Q_FIN_TRAIN = "2024Q2"
MIN_T_FIABLE = 20      # nº mínimo de periodos distintos para fiarse de EE Driscoll-Kraay/HAC (exploratorio)

# ------------------------------------------------------------------ familias de variables
FAM_PANEL = {
    "demografia": ["g_pob_total", "g_pob_extranj", "g_pob_20_34"],
    "empleo_renta": ["d4_ln_ocupados", "d4_ln_parados", "d_ln_ocupados", "d4_ln_renta_hog_real"],
    "credito_tipos": ["d4_ln_hipotecas_importe", "d4_ln_hipotecas_n", "d4_ln_compraventas_total",
                      "d4_ln_credito_vivienda_nuevo", "tipo_hip_real", "coste_uso_aprox", "euribor", "dtipo4"],
    "oferta_suelo": ["d4_ln_iniciadas_libres", "d4_ln_terminadas_libres", "d4_ln_p_suelo", "d4_ln_protegida",
                     "d4_ln_permisos", "d4_ln_costes_real"],
    "turismo": ["d4_ln_vut_viviendas"],
    "politica": ["n_eventos", "zona_tensionada_any"],
    "precio_cruzado": ["cruz_d4"],
}
FAM_NAC = {
    "demografia": ["g_pob_total", "g_pob_extranj"],
    "empleo_renta": ["d4_ln_ocupados", "d4_ln_renta_hog_real"],
    "credito_tipos": ["d4_ln_credito_nuevo", "tipo_hip_real", "coste_uso_aprox", "dtipo4"],
    "oferta_suelo": ["d4_ln_permisos", "d4_ln_costes_real"],
    "politica": ["n_eventos"],
    "precio_cruzado": ["cruz_d4"],
}
AR_COLS = [f"dY_l{k}" for k in range(4)]
Q_COLS = ["q2", "q3", "q4"]


def familias_con_ar(fam):
    f = {k: list(v) for k, v in fam.items()}
    f["autorregresivo"] = list(AR_COLS)
    f["estacional"] = list(Q_COLS)
    return f


def _inf_nan(d):
    return d.replace([np.inf, -np.inf], np.nan)


def _nac_cols(nac: pd.DataFrame, tmax: str) -> pd.DataFrame:
    """Series nacionales (información en t) indexadas por trimestre."""
    n = nac.copy()
    n["trimestre"] = n["trimestre"].astype(str)
    n = n[n["trimestre"] <= tmax].drop_duplicates("trimestre").sort_values("trimestre").set_index("trimestre")
    out = pd.DataFrame(index=n.index)
    out["d4_ln_renta_hog_real"] = n["d4_ln_renta_hog_real"]
    out["d4_ln_permisos"] = n["d4_ln_permisos"]
    out["d4_ln_costes_real"] = n["d4_ln_costes"] - n["d4_ln_deflactor"]
    out["dtipo4"] = n["tipo_hip"] - n["tipo_hip"].shift(4)
    ev = [c for c in n.columns if c.startswith("ev_")]
    out["n_eventos"] = n[ev].fillna(0).clip(lower=0).sum(axis=1) if ev else 0.0
    out["d4_ln_ipc_alquiler_nac"] = n["d4_ln_ipc_alquiler"]
    out["d4_ln_p_real_nac"] = n["d4_ln_p_tasado"] - n["d4_ln_deflactor"]
    return out


def _step_g(df, var, unit_col):
    """Crecimiento interanual de la población 'en escalera': último 1 de enero OBSERVADO (sin interpolar)."""
    s = df[var].where(df[f"{var}_metodo"] == "observado")
    if unit_col:
        s = s.groupby(df[unit_col]).transform(lambda x: x.ffill(limit=3))
        ls = np.log(s)
        return ls - ls.groupby(df[unit_col]).shift(4)
    s = s.ffill(limit=3)
    ls = np.log(s)
    return ls - ls.shift(4)


def preparar_panel(pan: pd.DataFrame, nac: pd.DataFrame, objetivo: str, tmax: str = Q_FIN_TRAIN) -> pd.DataFrame:
    """Panel provincial con las variables de las familias. objetivo 'B' (alquiler) o 'C' (compra real)."""
    d = pan.copy()
    d["trimestre"] = d["trimestre"].astype(str)
    d["cod_prov"] = d["cod_prov"].astype(str)
    d = d[d["trimestre"] <= tmax].sort_values(["cod_prov", "trimestre"]).reset_index(drop=True)
    nc = _nac_cols(nac, tmax)
    for c in nc.columns:
        d[c] = d["trimestre"].map(nc[c])
    for v in ("pob_total", "pob_extranj", "pob_20_34"):
        d[f"g_{v}"] = _step_g(d, v, "cod_prov")
    d["zona_tensionada_any"] = d["zona_tensionada_any"].fillna(0.0)
    if objetivo == "B":      # el predictor cruzado del alquiler es el precio de compra real
        d["cruz_d4"] = d["d4_ln_p_tasado"] - d["trimestre"].map(_defl_d4(nac))
    else:                    # el del precio de compra es el alquiler
        d["cruz_d4"] = d["d4_ln_ipc_alquiler"]
    d["unidad"] = d["cod_prov"]
    return _inf_nan(d)


def _defl_d4(nac):
    n = nac.copy()
    n["trimestre"] = n["trimestre"].astype(str)
    return n.drop_duplicates("trimestre").set_index("trimestre")["d4_ln_deflactor"]


def preparar_nacional(nac: pd.DataFrame, tmax: str = Q_FIN_TRAIN) -> pd.DataFrame:
    n = nac.copy()
    n["trimestre"] = n["trimestre"].astype(str)
    n = n[n["trimestre"] <= tmax].drop_duplicates("trimestre").sort_values("trimestre").reset_index(drop=True)
    nc = _nac_cols(nac, tmax)
    for c in nc.columns:
        n[c] = n["trimestre"].map(nc[c])
    n["g_pob_total"] = _step_g(n, "pob_total", None)
    n["g_pob_extranj"] = _step_g(n, "pob_extranj", None)
    n["cruz_d4"] = n["d4_ln_ipc_alquiler_nac"]
    n["unidad"] = "ES"
    return _inf_nan(n)


def construir_long(d: pd.DataFrame, objetivo: str, fam: dict, nac_ref: pd.DataFrame | None = None):
    """Rejilla unidad x periodo (v2_common._grid) con lvl, dY, yh, AR(4), dummies del trimestre objetivo y
    las variables de las familias en `fam`. Devuelve (long, per, units, columnas_variables)."""
    if objetivo == "A":
        lvl = vc._lvl_fn("ln_ipv", True)
    elif objetivo == "B":
        lvl = vc._lvl_fn("ipc_alquiler", False)
    else:
        lvl = vc._lvl_fn("p_tasado", True, nac_ref)
    long, per, units = vc._grid(d, lvl)
    l = long["lvl"]
    long["dY"] = l - vc._g(long, l, 1)
    long["yh"] = vc._g(long, l, -H) - l
    for k in range(4):
        long[f"dY_l{k}"] = vc._g(long, long["dY"], k) if k else long["dY"]
    qd = vc._qdum(long["trimestre"].values, H)       # trimestre del OBJETIVO (t+h)
    for c in Q_COLS:
        long[c] = qd[c].values
    cols = [c for v in fam.values() for c in v]
    for c in cols:
        if c not in long.columns:
            long[c] = np.nan
    return long, per, units, cols


# ------------------------------------------------------------------ especificaciones y ajuste
@dataclass(frozen=True)
class Spec:
    nombre: str
    clase: str                     # enet | postlasso | rf | lgbm
    params: tuple = ()
    rank: int = 2                  # complejidad (regla_H7.md)
    orden: int = 0                 # orden dentro de la clase (rejilla de menor a mayor flexibilidad)

    @property
    def p(self):
        return dict(self.params)


def specs_enet():
    out = []
    i = 0
    for l1 in (0.3, 0.7):
        for a in (0.4, 0.15, 0.05, 0.02, 0.005):          # de más a menos penalización
            out.append(Spec(f"EN_l1{l1}_a{a}", "enet", (("l1_ratio", l1), ("alpha", a)), 2, i))
            i += 1
    return out


def specs_rf():
    return [Spec(f"RF_d{d}_l{l}", "rf", (("max_depth", d), ("min_samples_leaf", l)), 5, i)
            for i, (d, l) in enumerate([(4, 40), (4, 10), (8, 40), (8, 10)])]


def specs_lgbm():
    return [Spec(f"LGBM_nl{nl}_n{n}", "lgbm", (("num_leaves", nl), ("n_estimators", n)), 6, i)
            for i, (nl, n) in enumerate([(4, 150), (4, 400), (12, 150), (12, 400)])]


SPEC_PL = Spec("PostLasso", "postlasso", (), 1, 0)


def lasso_bch(y, X, c=1.1, gamma=None, forced=()):
    """Lasso con penalización plug-in de Belloni-Chernozhukov-Hansen. X, y ya estandarizados/centrados.
    Devuelve (índices seleccionados, coeficientes)."""
    from sklearn.linear_model import Lasso
    n, p = X.shape
    if p == 0:
        return np.array(sorted(set(forced)), int), np.zeros(0)
    gamma = gamma if gamma is not None else 0.1 / np.log(max(n, p, 3))
    lam_q = stats.norm.ppf(1 - gamma / (2 * p))
    sig = np.std(y)
    beta = np.zeros(p)
    for _ in range(3):
        alpha = max(c * sig * lam_q / np.sqrt(n), 1e-8)
        m = Lasso(alpha=alpha, fit_intercept=False, max_iter=5000, tol=1e-6).fit(X, y)
        beta = m.coef_
        r = y - X @ beta
        sig = max(np.sqrt(np.mean(r ** 2)), 1e-8)
    sel = np.where(np.abs(beta) > 1e-10)[0]
    return np.unique(np.concatenate([sel, np.array(list(forced), int)])).astype(int), beta


@dataclass
class Fit:
    spec: Spec
    cols: list
    med: pd.Series
    mu: pd.Series
    sd: pd.Series
    sdy: float
    model: object
    sel: np.ndarray | None = None
    ols: np.ndarray | None = None
    fe: dict = field(default_factory=dict)
    n_train: int = 0

    def _z(self, X: pd.DataFrame):
        Xi = X[self.cols].astype(float).fillna(self.med)
        return (Xi - self.mu) / self.sd

    def predict_raw(self, X: pd.DataFrame) -> np.ndarray:
        """Predicción SIN efecto fijo (en unidades de y)."""
        c = self.spec.clase
        if c == "enet":
            return self.sdy * self.model.predict(self._z(X).values)
        if c == "postlasso":
            Z = self._z(X).values[:, self.sel]
            Z1 = np.column_stack([np.ones(len(Z)), Z])
            return self.sdy * (Z1 @ self.ols)
        if c == "rf":
            return self.sdy * self.model.predict(X[self.cols].astype(float).fillna(self.med).values)
        if c == "lgbm":
            return self.sdy * self.model.predict(X[self.cols].astype(float).values)
        raise ValueError(c)


def _lgbm(p):
    import lightgbm as lgb
    return lgb.LGBMRegressor(n_estimators=p["n_estimators"], learning_rate=0.03, num_leaves=p["num_leaves"],
                             min_child_samples=30, subsample=0.8, subsample_freq=1, colsample_bytree=0.8,
                             reg_lambda=1.0, random_state=SEED, n_jobs=1, deterministic=True,
                             force_row_wise=True, verbose=-1)


def ajustar(long: pd.DataFrame, posL: int, cols: list, spec: Spec, units_train, h: int = H,
            min_n: int = 6) -> Fit | None:
    """Ajuste con filas de entrenamiento pos+h <= posL de las unidades de entrenamiento. Objetivo: y menos la
    media de la unidad (efecto fijo) dividido por la DE (todo con datos de entrenamiento)."""
    tr = ((long["pos"] + h <= posL) & long["yh"].notna() & long[AR_COLS].notna().all(axis=1)
          & long["unidad"].isin(list(units_train)))
    if tr.sum() < min_n:
        return None
    D = long.loc[tr]
    fe = D.groupby("unidad")["yh"].mean().to_dict()
    yc = D["yh"].values - D["unidad"].map(fe).values
    sdy = float(np.std(yc)) or 1.0
    yz = yc / sdy
    X = D[cols].astype(float)
    ok = X.notna().any(axis=0)
    cols = [c for c in cols if ok[c]]
    X = X[cols]
    med = X.median().fillna(0.0)
    Xi = X.fillna(med)
    mu = Xi.mean()
    sd = Xi.std(ddof=0).replace(0, 1.0).fillna(1.0)
    Z = ((Xi - mu) / sd).values
    f = Fit(spec, cols, med, mu, sd, sdy, None, fe=fe, n_train=int(tr.sum()))
    p = spec.p
    if spec.clase == "enet":
        from sklearn.linear_model import ElasticNet
        f.model = ElasticNet(alpha=p["alpha"], l1_ratio=p["l1_ratio"], max_iter=20000, tol=1e-6,
                             random_state=SEED).fit(Z, yz)
    elif spec.clase == "postlasso":
        forced = [cols.index(c) for c in AR_COLS if c in cols]
        sel, _ = lasso_bch(yz, Z, forced=forced)
        Zs = np.column_stack([np.ones(len(Z)), Z[:, sel]])
        f.sel, f.ols = sel, np.linalg.lstsq(Zs, yz, rcond=None)[0]
    elif spec.clase == "rf":
        from sklearn.ensemble import RandomForestRegressor
        f.model = RandomForestRegressor(n_estimators=300, max_depth=p["max_depth"],
                                        min_samples_leaf=p["min_samples_leaf"], max_features=0.5,
                                        random_state=SEED, n_jobs=4).fit(Xi.values, yz)
    elif spec.clase == "lgbm":
        f.model = _lgbm(p).fit(X.values, yz)
    else:
        raise ValueError(spec.clase)
    return f


def predecir_filas(f: Fit, long: pd.DataFrame, posL: int, test_pos, units_train, units_extra=(), h: int = H):
    """Predicciones (con efecto fijo) para los orígenes `test_pos`. Las unidades extra (selladas) reciben
    FE = media(y) - media(f(x)) en su propia historia con pos+h <= posL (no influyen en el ajuste).
    Devuelve (filas, predicción sin FE, vector fe)."""
    te = (long["pos"].isin(set(test_pos)) & long[AR_COLS].notna().all(axis=1)
          & long["unidad"].isin(list(units_train) + list(units_extra)))
    sub = long.loc[te]
    if sub.empty:
        return None
    raw = f.predict_raw(sub)
    fe = sub["unidad"].map(f.fe).astype(float).values
    for u in units_extra:
        hist = ((long["unidad"] == u) & (long["pos"] + h <= posL) & long["yh"].notna()
                & long[AR_COLS].notna().all(axis=1))
        if hist.sum() < 4:
            fe[(sub["unidad"] == u).values] = np.nan
            continue
        Hh = long.loc[hist]
        fe[(sub["unidad"] == u).values] = float(Hh["yh"].mean() - f.predict_raw(Hh).mean())
    return sub, raw, fe


def a_frame(sub, pred, per, etiqueta, sid, h=H):
    return pd.DataFrame({"periodo": sub["trimestre"].values,
                         "periodo_obj": [per[p + h] if p + h < len(per) else None for p in sub["pos"]],
                         "unidad": sub["unidad"].values, "y_real": sub["yh"].values, "y_pred": pred,
                         "modelo": etiqueta, "split": sid, "h": h})


def correr_bloques(long, per, splits, cols, spec: Spec, units, etiqueta=None, h: int = H, guardar=None):
    """Predicciones fuera de muestra por split (formato v2_common). `guardar(sid, f, sub, raw, fe)` opcional."""
    rows = []
    for sid, (itr, ite) in enumerate(splits):
        posL = int(itr[-1])
        f = ajustar(long, posL, cols, spec, units, h)
        if f is None:
            continue
        r = predecir_filas(f, long, posL, ite, units, (), h)
        if r is None:
            continue
        sub, raw, fe = r
        rows.append(a_frame(sub, raw + fe, per, etiqueta or spec.nombre, sid, h))
        if guardar is not None:
            guardar(sid, f, sub, raw, fe)
    cols_out = ["periodo", "periodo_obj", "unidad", "y_real", "y_pred", "modelo", "split", "h"]
    return pd.concat(rows, ignore_index=True) if rows else pd.DataFrame(columns=cols_out)


# ------------------------------------------------------------------ importancias
def perm_grupos(f: Fit, sub: pd.DataFrame, raw: np.ndarray, fe: np.ndarray, fam: dict, reps: int = 5,
                seed: int = SEED):
    """Permutación AGRUPADA por familia (columnas de la familia permutadas juntas por filas) sobre un bloque de
    test. Devuelve DataFrame (fila x familia) con Δ error cuadrático (media de `reps` permutaciones)."""
    rng = np.random.default_rng(seed)
    y = sub["yh"].values
    ok = ~np.isnan(y)
    base = (y - (raw + fe)) ** 2
    res = {}
    for fn, cs in fam.items():
        cs = [c for c in cs if c in f.cols]
        if not cs:
            continue
        d = np.zeros(len(sub))
        for _ in range(reps):
            idx = rng.permutation(len(sub))
            X2 = sub.copy()
            X2[cs] = sub[cs].values[idx]
            d += (y - (f.predict_raw(X2) + fe)) ** 2 - base
        res[fn] = d / reps
    return pd.DataFrame(res, index=sub.index)[ok]


def shap_grupos(f: Fit, sub: pd.DataFrame, fam: dict):
    """TreeSHAP (LightGBM pred_contrib) agregado por familia: contribución firmada por fila (unidades de y)."""
    X = sub[f.cols].astype(float).values
    c = f.model.booster_.predict(X, pred_contrib=True)[:, :-1] * f.sdy
    out = {}
    for fn, cs in fam.items():
        ix = [f.cols.index(x) for x in cs if x in f.cols]
        if ix:
            out[fn] = c[:, ix].sum(axis=1)
    return pd.DataFrame(out, index=sub.index), pd.DataFrame(c, index=sub.index, columns=f.cols)


def ale_1d(predict, X: pd.DataFrame, col: str, bins: int = 10):
    """ALE de primer orden con cuantiles (Apley y Zhu 2020). predict(DataFrame)->array."""
    x = X[col].astype(float)
    q = np.unique(np.nanquantile(x, np.linspace(0, 1, bins + 1)))
    if len(q) < 3:
        return pd.DataFrame({"x": q, "ale": 0.0})
    k = np.clip(np.searchsorted(q, x.values, side="right") - 1, 0, len(q) - 2)
    eff = np.zeros(len(q) - 1)
    cnt = np.zeros(len(q) - 1)
    for j in range(len(q) - 1):
        m = (k == j) & ~np.isnan(x.values)
        if not m.any():
            continue
        lo, hi = X[m].copy(), X[m].copy()
        lo[col], hi[col] = q[j], q[j + 1]
        eff[j] = np.mean(predict(hi) - predict(lo))
        cnt[j] = m.sum()
    ale = np.concatenate([[0.0], np.cumsum(eff)])
    centro = np.sum(0.5 * (ale[1:] + ale[:-1]) * cnt) / max(cnt.sum(), 1)
    return pd.DataFrame({"x": q, "ale": ale - centro})


def periodo_de(t: str):
    for k, (a, b) in PERIODOS.items():
        if a <= t <= b:
            return k
    return "P0_pre2008"


# ------------------------------------------------------------------ PDS grupal e inferencia por periodo
def _within(df, cols, unit):
    if unit is None:
        return df[cols] - df[cols].mean()
    return df[cols] - df.groupby(unit)[cols].transform("mean")


def _ols_dk(y, X, time, maxlags=4):
    import statsmodels.api as sm
    X1 = sm.add_constant(X, has_constant="add")
    m = sm.OLS(y, X1)
    tt = pd.factorize(pd.Series(time))[0]
    try:
        if len(np.unique(tt)) == len(tt):          # serie única (nacional): HAC de Newey-West
            return m.fit(cov_type="HAC", cov_kwds={"maxlags": maxlags})
        return m.fit(cov_type="hac-groupsum",
                     cov_kwds={"time": tt, "maxlags": min(maxlags, max(len(np.unique(tt)) - 2, 1))})
    except Exception:  # noqa: BLE001
        return m.fit(cov_type="HC1")


def pds_familia(d: pd.DataFrame, fam: dict, fname: str, unit: str | None, tcol: str = "trimestre"):
    """Post-double-selection grupal para la familia `fname`: controles = resto de variables (otras familias, AR,
    estacional). Devuelve dict con n, nº de controles seleccionados y Wald conjunto (EE Driscoll-Kraay o
    HAC(4)). EXPLORATORIO: colinealidad alta entre variables de la misma y de distintas familias."""
    ds = [c for c in fam[fname] if c in d.columns and d[c].notna().sum() > 0]
    ws = [c for k, v in fam.items() if k != fname for c in v if c in d.columns and d[c].notna().sum() > 0]
    if not ds:
        return {"n": 0, "estado": "sin datos"}
    use = d.dropna(subset=["yh"] + ds).copy()
    ds = [c for c in ds if use[c].std() > 0]
    if len(use) < 25 or not ds:
        return {"n": int(len(use)), "estado": "n insuficiente"}
    ws = [c for c in ws if use[c].notna().sum() > 0 and use[c].std() > 0]
    use[ws] = use[ws].fillna(use[ws].median())
    ws = [c for c in ws if use[c].std() > 0]
    cols = ["yh"] + ds + ws
    W = _within(use, cols, unit)
    Wz = (W - W.mean()) / W.std(ddof=0).replace(0, 1)
    Zw = Wz[ws].values
    sel = set(lasso_bch(Wz["yh"].values, Zw)[0].tolist())
    for c in ds:
        sel |= set(lasso_bch(Wz[c].values, Zw)[0].tolist())
    sel = sorted(sel)
    X = pd.concat([Wz[ds], Wz[[ws[i] for i in sel]]], axis=1)
    rango_ok = bool(np.linalg.matrix_rank(X.values) == X.shape[1])
    r = _ols_dk(Wz["yh"].values, X.values, use[tcol].values)
    k = len(ds)
    b, V = np.asarray(r.params)[1:1 + k], np.asarray(r.cov_params())[1:1 + k, 1:1 + k]
    try:
        wald = float(b @ np.linalg.solve(V, b))
        p = float(stats.chi2.sf(wald, k))
    except np.linalg.LinAlgError:
        wald, p = np.nan, np.nan
    n_t = int(use[tcol].nunique())
    p_crudo = p
    fiable = bool(rango_ok and n_t >= MIN_T_FIABLE)   # con T < 20 los EE de Driscoll-Kraay no son fiables
    if not fiable:
        p = np.nan
    return {"p_crudo_no_fiable": p_crudo, "fiable": fiable, "n": int(len(use)), "n_periodos": int(use[tcol].nunique()), "k_familia": k, "n_controles_sel": len(sel),
            "rango_completo": rango_ok, "wald": wald, "p": p, "coef": {c: float(x) for c, x in zip(ds, b)}, "estado": "ok"}


def lp_periodo(d: pd.DataFrame, regs: list, unit: str | None, tcol: str = "trimestre"):
    """Proyección local por periodo: yh ~ regs + AR(4) + estacional (FE de unidad). EE Driscoll-Kraay/HAC(4)."""
    base = d.dropna(subset=["yh"] + AR_COLS)
    regs = [c for c in regs if c in base.columns and len(base) and base[c].notna().mean() >= 0.8]
    use = base.dropna(subset=regs).copy()
    regs = [c for c in regs if use[c].std() > 0]
    ctrl = AR_COLS + [q for q in Q_COLS if use[q].std() > 0]
    if len(use) < 20 + len(regs) + len(ctrl) or not regs:
        return None
    W = _within(use, ["yh"] + regs + ctrl, unit)
    r = _ols_dk(W["yh"].values, W[regs + ctrl].values, use[tcol].values)
    se = np.asarray(r.bse)[1:1 + len(regs)]
    b = np.asarray(r.params)[1:1 + len(regs)]
    nt = int(use[tcol].nunique())
    fi = nt >= MIN_T_FIABLE
    return [dict(var=c, coef=float(bb), ee=float(ss), t=float(bb / ss) if ss > 0 else np.nan,
                 p=float(2 * stats.norm.sf(abs(bb / ss))) if (ss > 0 and fi) else np.nan, n=int(len(use)),
                 n_periodos=nt, fiable=fi) for c, bb, ss in zip(regs, b, se)]
