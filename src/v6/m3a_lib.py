"""M3a v6: biblioteca de predicción del ALQUILER de stock (SERPAVI). Sin red, SEED=20261010, un hilo.

Contiene: construcción de paneles y rasgos (igual para entrenamiento y para sellado, que M4 aplica con `predecir_modelo`),
líneas base (persistencia, AR por unidad, M1A-TWFE con tendencia, ECM v1 aproximado), pliegues con embargo, DM-HLN y
fábrica de modelos. Esta librería NO abre data/sealed: la muestra sellada solo la abre M4 con holdout.evaluate_v6.
"""
from __future__ import annotations

import json
import os
import sys
from pathlib import Path

for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS"):
    os.environ.setdefault(_v, "1")
import numpy as np
import pandas as pd
from scipy import stats

RAIZ = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(RAIZ / "src"))
from holdout import CCAA_PROV  # noqa: E402  (solo el diccionario provincia -> CCAA)

SEED = 20261010
PAN = RAIZ / "output/v6/M0/paneles"
OUT = RAIZ / "output/v6/M3A"
FECHA = "2026-10-11"

ALQ_REG = ["ln_pob", "share_ext_pob", "ln_pib_pc", "ln_vut", "ln_terminadas_libres", "ln_iniciadas_libres",
           "n_mun_tensionados", "n_mun_topes_cat"]
MUN_REG = ["ln_pob", "share_ext_pob", "ln_pib_pc", "ln_vut", "ln_terminadas_libres", "ln_iniciadas_libres",
           "tensionada_mun", "tope_cat_mun"]
DIS_REG = ["ln_vut_plazas_dis", "ln_pib_pc"]
PROV_VARS = ["ln_pob", "share_ext_pob", "ln_pib_pc", "ln_terminadas_libres", "ln_iniciadas_libres"]
YCOL = {"provincia": "ln_alq_m2_serpavi_vc", "municipio": "ln_alq_m2_serpavi_mun", "distrito": "ln_alq_m2_serpavi_dis"}
REGS = {"provincia": ALQ_REG, "municipio": MUN_REG, "distrito": DIS_REG}
# regresores de las líneas base econométricas (S1 de M1A: muestra larga sin ln_vut)
REGS_ECO = {"provincia": [r for r in ALQ_REG if r != "ln_vut"], "municipio": [r for r in MUN_REG if r != "ln_vut"],
            "distrito": ["ln_pib_pc"]}
ORIGENES = {"provincia": [2020, 2022], "municipio": [2020, 2022], "distrito": [2018, 2020, 2022]}
NOMBRES = {"provincia": ["prov_alquiler_anual", "prov_compra_anual"],
           "municipio": ["mun_alquiler_anual", "prov_alquiler_anual", "prov_compra_anual"],
           "distrito": ["dis_alquiler_anual", "prov_alquiler_anual", "prov_compra_anual"]}
FAMILIAS = {  # familias de rasgos para la importancia agrupada (descriptiva, C4)
    "autorregresivo": ["y_lag1", "dy_lag1", "dy_lag2", "dy_lag1_prov", "dy_lag1_mun", "y_lag1_rel_prov"],
    "poblacion": ["ln_pob", "share_ext_pob"], "renta": ["ln_pib_pc"],
    "oferta": ["ln_terminadas_libres", "ln_iniciadas_libres"], "turismo_vut": ["ln_vut", "ln_vut_plazas_dis"],
    "regulacion": ["n_mun_tensionados", "n_mun_topes_cat", "tensionada_mun", "tope_cat_mun"],
    "espacial": ["x_m", "y_m"]}
FAM_DE = {v: k for k, vs in FAMILIAS.items() for v in vs}
LGBM_GRID = dict(n_estimators=[100, 200, 400, 600], learning_rate=[0.01, 0.03, 0.05, 0.1], num_leaves=[4, 8, 16, 31],
                 min_child_samples=[5, 10, 20, 50], subsample=[0.7, 1.0], colsample_bytree=[0.5, 0.8, 1.0],
                 reg_lambda=[0.0, 1.0, 10.0])
RF_GRID = dict(n_estimators=[100, 200], max_depth=[4, 6, 8, 12, None], min_samples_leaf=[1, 3, 5, 10, 20],
               max_features=[0.3, 0.5, 0.8, 1.0], max_samples=[0.3, 0.5, 0.8])


def ccaa_de(s):
    return s.map(lambda c: CCAA_PROV.get(str(c).zfill(2), "x"))


def leer_train(nombre):
    return pd.read_csv(PAN / f"{nombre}_train.csv.gz",
                       dtype={"cod": str, "cod_prov": str, "cod_mun": str, "distrito": str})


def leer_srcs(extra=None):
    """Paneles de entrenamiento; si `extra` (dict nombre -> DataFrame sellado, que aporta M4) se concatena."""
    srcs = {}
    for n in ("prov_alquiler_anual", "prov_compra_anual", "mun_alquiler_anual", "dis_alquiler_anual"):
        d = leer_train(n)
        if extra and n in extra:
            e = extra[n].copy()
            for c in ("cod", "cod_prov", "cod_mun", "distrito"):
                if c in e:
                    e[c] = e[c].astype(str)
            d = pd.concat([d, e[[c for c in e.columns if c in d.columns]]], ignore_index=True)
            d = d.drop_duplicates(subset=[c for c in ("cod", "cod_mun", "distrito", "anio") if c in d.columns])
        srcs[n] = d
    return srcs


def _centroides():
    c = pd.read_csv(RAIZ / "data/raw/v5/municipio_centroides_utm30.csv", dtype={"codigo": str})
    return c.rename(columns={"codigo": "cod_mun"})[["cod_mun", "x_m", "y_m"]]


def panel_nivel(nivel, srcs):
    """Panel largo con desenlace y, rasgos de nivel (t-1) y metadatos. Regresores en t-1 (etiquetados en t)."""
    alq, cmp_ = srcs["prov_alquiler_anual"], srcs["prov_compra_anual"]
    rt = cmp_[["cod", "anio"] + PROV_VARS].merge(alq[["cod", "anio", "ln_vut", "n_mun_tensionados", "n_mun_topes_cat"]],
                                                 on=["cod", "anio"], how="outer")
    rt["anio"] += 1
    rt = rt.rename(columns={"cod": "cod_prov"})
    y = YCOL[nivel]
    if nivel == "provincia":
        P = alq.rename(columns={"cod": "cod_prov"})[["cod_prov", "anio", y]].merge(rt, on=["cod_prov", "anio"], how="left")
        P["unit"], P["cod_mun"] = P.cod_prov, P.cod_prov
        P["x_m"] = np.nan
        P["y_m"] = np.nan
    elif nivel == "municipio":
        mun = srcs["mun_alquiler_anual"]
        own = mun[["cod_mun", "anio", "tensionada_mun", "tope_cat_mun"]].copy()
        own["anio"] += 1
        P = mun[["cod_mun", "anio", "cod_prov", y]].merge(own, on=["cod_mun", "anio"], how="left")
        P = P.merge(rt, on=["cod_prov", "anio"], how="left").merge(_centroides(), on="cod_mun", how="left")
        P["unit"] = P.cod_mun
    else:
        dis = srcs["dis_alquiler_anual"]
        own = dis[["distrito", "anio", "ln_vut_plazas_dis"]].copy()
        own["anio"] += 1
        P = dis[["distrito", "anio", "cod_prov", y]].merge(own, on=["distrito", "anio"], how="left")
        P = P.merge(rt[["cod_prov", "anio", "ln_pib_pc"]], on=["cod_prov", "anio"], how="left")
        P["cod_mun"] = P.distrito.str[:5]
        P = P.merge(_centroides(), on="cod_mun", how="left")
        P["unit"] = P.distrito
    P = P.rename(columns={y: "y"})
    P["ccaa"] = ccaa_de(P.cod_prov)
    P["anio"] = P.anio.astype(int)
    return P


def rasgos(P, nivel):
    """Rasgos autorregresivos (solo pasado) y retardos espaciales; objetivo dy = y - y_lag1."""
    s = P[["unit", "anio", "y"]].dropna().copy()
    out = P.copy()
    for k in (1, 2, 3):
        t = s.rename(columns={"y": f"y_l{k}"}).assign(anio=s.anio + k)[["unit", "anio", f"y_l{k}"]]
        out = out.merge(t, on=["unit", "anio"], how="left")
    out["y_lag1"] = out.y_l1
    out["dy_lag1"] = out.y_l1 - out.y_l2
    out["dy_lag2"] = out.y_l2 - out.y_l3
    out["dy"] = out.y - out.y_lag1
    out["dy_lag1_prov"] = out.groupby(["cod_prov", "anio"]).dy_lag1.transform("mean")
    out["y_lag1_rel_prov"] = out.y_lag1 - out.groupby(["cod_prov", "anio"]).y_lag1.transform("mean")
    if nivel == "distrito":
        out["dy_lag1_mun"] = out.groupby(["cod_mun", "anio"]).dy_lag1.transform("mean")
    else:
        out["dy_lag1_mun"] = np.nan
    return out.drop(columns=["y_l1", "y_l2", "y_l3"])


def columnas_x(nivel):
    cols = ["y_lag1", "dy_lag1", "dy_lag2", "dy_lag1_prov", "y_lag1_rel_prov"] + REGS[nivel]
    if nivel == "distrito":
        cols += ["dy_lag1_mun"]
    if nivel != "provincia":
        cols += ["x_m", "y_m"]
    return cols


def cargar(nivel, extra=None):
    srcs = leer_srcs(extra)
    return rasgos(panel_nivel(nivel, srcs), nivel)


# ------------------------------------------------------------------ pliegues
def pliegues(nivel, anio_max):
    """Origen o: entrenamiento años <= o-2, embargo o-1, validación o y o+1 (hipotesis.md §5)."""
    return [(o, o - 2, [a for a in (o, o + 1) if a <= anio_max]) for o in ORIGENES[nivel]]


def bloques_espaciales(df, k=4):
    cc = sorted(df.ccaa.unique())
    mapa = {c: i % k for i, c in enumerate(cc)}
    return df.ccaa.map(mapa)


# ------------------------------------------------------------------ DM-HLN
def dm_hln(e1, e2, h=1):
    d = np.asarray(e1, float) ** 2 - np.asarray(e2, float) ** 2
    n = len(d)
    if n < 3 or np.allclose(d, 0):
        return float("nan"), float("nan"), n
    dc = d - d.mean()
    lrv = dc @ dc / n
    for lag in range(1, h):
        lrv += 2 * (1 - lag / h) * (dc[lag:] @ dc[:-lag]) / n
    dm = d.mean() / np.sqrt(lrv / n) * np.sqrt((n + 1 - 2 * h + h * (h - 1) / n) / n)
    return float(dm), float(2 * stats.t.sf(abs(dm), n - 1)), n


def holm(p):
    p = np.asarray(p, float)
    o = np.argsort(np.where(np.isnan(p), 2, p))
    m = int(np.sum(~np.isnan(p)))
    out = np.full(len(p), np.nan)
    run = 0.0
    for r, i in enumerate(o[:m]):
        run = max(run, (m - r) * p[i])
        out[i] = min(1.0, run)
    return out


def bh(p):
    p = np.asarray(p, float)
    m = int(np.sum(~np.isnan(p)))
    o = np.argsort(np.where(np.isnan(p), 2, p))
    out = np.full(len(p), np.nan)
    prev = 1.0
    for r in range(m - 1, -1, -1):
        i = o[r]
        prev = min(prev, p[i] * m / (r + 1))
        out[i] = prev
    return out


# ------------------------------------------------------------------ líneas base
def pred_persistencia(tr, va):
    return va.y_lag1.to_numpy(float)


def pred_ar(tr, va, pmax=4):
    """AR(p) por unidad sobre niveles (p=1..4 por AIC según T); sin T suficiente -> persistencia.
    Los retardos de validación son los valores observados (predicción a 1 paso)."""
    ys = {u: g.sort_values("anio").set_index("anio").y.dropna() for u, g in tr.groupby("unit")}
    full = {}
    for u, g in pd.concat([tr, va]).groupby("unit"):
        full[u] = g.set_index("anio").y.dropna()
    coef = {}
    for u, s in ys.items():
        n = len(s)
        best = None
        for p in range(1, pmax + 1):
            if n - p < 2 * p + 2:
                break
            v = s.to_numpy()
            Y = v[p:]
            X = np.column_stack([np.ones(n - p)] + [v[p - j:n - j] for j in range(1, p + 1)])
            b, *_ = np.linalg.lstsq(X, Y, rcond=None)
            rss = float(np.sum((Y - X @ b) ** 2)) + 1e-12
            aic = (n - p) * np.log(rss / (n - p)) + 2 * (p + 1)
            if best is None or aic < best[0]:
                best = (aic, p, b)
        if best is not None:
            coef[u] = best[1:]
    out = np.full(len(va), np.nan)
    for i, (u, a, yl) in enumerate(zip(va.unit, va.anio, va.y_lag1)):
        if u in coef:
            p, b = coef[u]
            lags = [full[u].get(a - j, np.nan) for j in range(1, p + 1)]
            if not np.any(np.isnan(lags)):
                out[i] = b[0] + float(np.dot(b[1:], lags))
                continue
        out[i] = yl
    return out


def pred_twfe(tr, va, regs):
    """M1A (S1): EF de unidad + tendencia común + regresores t-1, MCO intra-unidad; predice nivel en unidades vistas."""
    cols = regs + ["anio", "y"]
    t = tr.dropna(subset=cols).copy()
    t = t[t.groupby("unit").y.transform("size") >= 2]
    X = t[regs + ["anio"]].to_numpy(float)
    mu = t.groupby("unit")[regs + ["anio", "y"]].transform("mean")
    Xd = X - mu[regs + ["anio"]].to_numpy(float)
    yd = t.y.to_numpy(float) - mu.y.to_numpy(float)
    b, *_ = np.linalg.lstsq(Xd, yd, rcond=None)
    mm = t.groupby("unit")[regs + ["anio", "y"]].mean()
    out = np.full(len(va), np.nan)
    ok = va[regs + ["anio"]].notna().all(axis=1).to_numpy() & va.unit.isin(mm.index).to_numpy()
    v = va[ok]
    m = mm.loc[v.unit]
    out[ok] = m.y.to_numpy() + (v[regs + ["anio"]].to_numpy(float) - m[regs + ["anio"]].to_numpy(float)) @ b
    return out


def pred_ecm(tr, va, regs):
    """ECM v1 aproximado (como en M1A): dy = a + rho*y_lag1 + X_{t-1} b, MCO agrupado."""
    cols = regs + ["y_lag1", "dy"]
    t = tr.dropna(subset=cols)
    X = np.column_stack([np.ones(len(t)), t.y_lag1, t[regs].to_numpy(float)])
    b, *_ = np.linalg.lstsq(X, t.dy.to_numpy(float), rcond=None)
    out = np.full(len(va), np.nan)
    ok = va[regs + ["y_lag1"]].notna().all(axis=1).to_numpy()
    v = va[ok]
    out[ok] = v.y_lag1.to_numpy(float) + np.column_stack([np.ones(len(v)), v.y_lag1, v[regs].to_numpy(float)]) @ b
    return out


def rmse(e):
    e = np.asarray(e, float)
    return float(np.sqrt(np.nanmean(e ** 2)))


def mae(e):
    return float(np.nanmean(np.abs(np.asarray(e, float))))


# ------------------------------------------------------------------ modelos
def crear_modelo(familia, cfg):
    cfg = dict(cfg)
    if familia == "rf":
        from sklearn.ensemble import RandomForestRegressor
        return RandomForestRegressor(random_state=SEED, n_jobs=1, bootstrap=True, **cfg)
    import lightgbm as lgb
    return lgb.LGBMRegressor(random_state=SEED, n_jobs=1, num_threads=1, deterministic=True, force_row_wise=True,
                             subsample_freq=1, verbose=-1, **cfg)


def muestrear_configs(grid, n, seed=SEED):
    rng = np.random.default_rng(seed)
    out, vistos = [], set()
    while len(out) < n:
        c = {k: v[int(rng.integers(len(v)))] for k, v in grid.items()}
        c = {k: (None if x is None else (x.item() if hasattr(x, "item") else x)) for k, x in c.items()}
        key = json.dumps(c, sort_keys=True)
        if key not in vistos:
            vistos.add(key)
            out.append(c)
    return out


def ajustar_predecir(familia, cfg, tr, va, cols):
    tr = tr.dropna(subset=["dy"])
    X = tr[cols].to_numpy(float)
    m = crear_modelo(familia, cfg)
    if familia == "rf":
        X = np.nan_to_num(X, nan=-9.0)  # RF: NaN como categoría fuera de rango (determinista)
        Xv = np.nan_to_num(va[cols].to_numpy(float), nan=-9.0)
    else:
        Xv = va[cols].to_numpy(float)
    m.fit(X, tr.dy.to_numpy(float))
    return va.y_lag1.to_numpy(float) + m.predict(Xv), m


def predecir_modelo(modelo_id, extra_sellado):
    """Punto de entrada para M4. `extra_sellado`: dict nombre -> DataFrame leído por holdout.evaluate_v6
    (solo los nombres de NOMBRES[nivel]). Devuelve DataFrame(unit, anio, y, y_lag1, pred, unidad_vista_en_train)."""
    import joblib
    ficha = json.loads((OUT / "modelos" / f"{modelo_id}.json").read_text())
    nivel = ficha["nivel"]
    P = cargar(nivel, extra_sellado)
    tr_units = set(panel_nivel(nivel, leer_srcs()).unit)
    claves = extra_sellado[NOMBRES[nivel][0]]
    kcol = {"provincia": "cod", "municipio": "cod_mun", "distrito": "distrito"}[nivel]
    ks = set(zip(claves[kcol].astype(str), claves.anio.astype(int)))
    obj = P[[k in ks for k in zip(P.unit, P.anio)]].dropna(subset=["y", "y_lag1"]).copy()
    cols = ficha["variables"]
    fam = ficha["familia"]
    if fam in ("rf", "gb"):
        m = joblib.load(OUT / ficha["ruta_modelo"])
        X = obj[cols].to_numpy(float)
        X = np.nan_to_num(X, nan=-9.0) if fam == "rf" else X
        obj["pred"] = obj.y_lag1 + m.predict(X)
    elif fam == "mixto":
        import m3a_bayes as B
        obj["pred"] = B.predecir_mixto(OUT / ficha["ruta_modelo"], obj)
    else:
        import m3a_dl as D
        obj["pred"] = D.predecir_dl(OUT / ficha["ruta_modelo"], ficha, P, obj)
    obj["unidad_vista_en_train"] = obj.unit.isin(tr_units)
    return obj[["unit", "anio", "y", "y_lag1", "pred", "unidad_vista_en_train"]]
