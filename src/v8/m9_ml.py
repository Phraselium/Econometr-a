#!/usr/bin/env python3
"""V8-F4 M9: ML interpretable SOLO COMO CONTRASTE (pre-registro §9). Capa C4: prediccion != causalidad.

Panel de 17 CCAA trimestral (2009T2-2026T2) + nacional (2003T2-2026T2). Objetivo: crecimiento interanual REAL (log x100) del precio de
compra (valor tasado) y del alquiler (IPC alquiler), deflactados con el IPC general. Predictores por familia con RETARDO de 1 trimestre.
Validacion: 5 bloques temporales hacia delante de 8 trimestres con embargo de 4 (gap), MISMA muestra para todos los modelos;
DM-HLN (h=4 por el solape interanual) frente a AR(4) [FE de CCAA en el panel], AR(4)+factor comun y ECM v1 aproximado (solo nacional).
Presupuesto de hiperparametros (declarado antes, sin seleccion por error fuera de muestra): LightGBM 2 configs x {monotonia, sin} ;
GAM 2 (alfa 10 principal, 100 sensibilidad). Todas se registran.
Uso: python3 src/v8/m9_ml.py [--rapido] [--salida DIR]
"""
from __future__ import annotations

import os

for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS"):
    os.environ[_v] = "1"

import argparse  # noqa: E402
import json  # noqa: E402
import sys  # noqa: E402
import time  # noqa: E402
import warnings  # noqa: E402
from pathlib import Path  # noqa: E402

import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402
from scipy import stats  # noqa: E402

warnings.filterwarnings("ignore")
RAIZ = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(RAIZ / "src"))
sys.path.insert(0, str(RAIZ / "src" / "v8"))
from econ_utils import Registry, dm_test  # noqa: E402
from herramientas import shap_grupos as sg  # noqa: E402
import m67_comun as mc  # noqa: E402

SEED = 20261010
PANEL = RAIZ / "data" / "processed" / "v8" / "panel_ccaa_q_v8.csv"
SCRIPT = "src/v8/m9_ml.py"
PERS = ["P1", "P2", "P3", "P4", "P5"]
FAMS = ["demografia", "empleo_renta", "credito_tipos", "oferta", "demanda_externa", "turismo", "factor_europeo"]
NOTA_C4 = "contraste, no causal (C4): el reparto SHAP describe como el modelo usa las familias; con familias correlacionadas no identifica efectos"

# variable -> familia (panel). Todas entran con retardo 1.
PANEL_VARS = {
    "epa_pob": "demografia",
    "ocupados": "empleo_renta", "tasa_paro": "empleo_renta", "salario_real": "empleo_renta",
    "tipo_hip_real": "credito_tipos", "hip_importe_real": "credito_tipos", "hip_n": "credito_tipos",
    "visados": "oferta", "terminadas": "oferta",
    "tx_extranj": "demanda_externa", "cuota_extranj": "demanda_externa",
    "hpi_ea20": "factor_europeo", "bis_hpi_real": "factor_europeo",
}
TURISMO_VARS = {"turistas": "turismo", "vut": "turismo"}
# monotonia solo donde el signo teorico es claro: tipos (-), empleo (+), poblacion (+)
MONO = {"tipo_hip_real": -1, "ocupados": 1, "epa_pob": 1, "pob_total": 1}
# columnas COMPLETAS del contrato (J13/J21): las que no aplican quedan vacias
COLS_COEF = ["modelo_id", "modulo", "familia_modelo", "mercado", "ambito", "periodo", "dependiente", "transformacion", "medida_precio",
             "variable", "beta", "ee", "tipo_ee", "t", "p", "p_ajustado", "metodo_ajuste", "ic95_lo", "ic95_hi", "beta_std", "elasticidad",
             "n", "r2", "r2_adj", "aic", "bic", "vel_ajuste", "semivida", "coint_p", "bg_p", "bp_p", "jb_p", "reset_p", "cusum_estable",
             "vif_max", "f1_etapa", "ar_lo", "ar_hi", "capa", "n_multiverso", "pct_mismo_signo", "pct_sig_bh", "cumple_regla_m0",
             "cumple_multiverso", "destacado", "motivo_destacado", "script"]
COLS_ATR = ["metodo", "mercado", "ambito", "periodo", "factor", "contribucion_pp", "pct_total", "b68_lo", "b68_hi", "b90_lo", "b90_hi",
            "capa", "notas", "variante", "principal"]
ULTIMO_R0 = "2026Q1"   # R0 (revision F4): P5 = 2022T3-2026T1 en el resumen por periodo
CFG = {"A": dict(num_leaves=8, n_estimators=150, learning_rate=0.05), "B": dict(num_leaves=4, n_estimators=300, learning_rate=0.03)}
ALFAS = {"alfa10": 10.0, "alfa100": 100.0}


# ------------------------------------------------------------------ datos
def d4(s, g=None):
    return 100.0 * (s.groupby(g).diff(4) if g is not None else s.diff(4))


def construir_panel(mercado: str) -> pd.DataFrame:
    p = pd.read_csv(PANEL)
    p["codigo_ine_ccaa"] = p["codigo_ine_ccaa"].astype(int)
    p = p.sort_values(["trimestre", "codigo_ine_ccaa"]).reset_index(drop=True)
    g = p["codigo_ine_ccaa"]
    lipc = np.log(p["ipc_general"])
    infl = 100.0 * (lipc.groupby(g).diff(4))
    X = pd.DataFrame(index=p.index)
    X["epa_pob"] = d4(np.log(p["epa_pob_total"]), g)
    X["ocupados"] = d4(p["ln_ocupados"], g)
    X["tasa_paro"] = p["tasa_paro_epa"]
    X["salario_real"] = d4(p["ln_salario_ccaa"] - lipc, g)
    X["tipo_hip_real"] = p["nac_tipo_hip"] - infl
    X["hip_importe_real"] = d4(p["ln_hip_importe"] - lipc, g)
    X["hip_n"] = d4(p["ln_hip_n"], g)
    X["visados"] = d4(p["ln_visados"], g)
    X["terminadas"] = d4(p["ln_terminadas"], g)
    X["tx_extranj"] = d4(p["ln_tx_extranj_ccaa"], g)
    X["cuota_extranj"] = d4(p["ln_trans_extranjeros"] - p["ln_compraventas"], g)
    X["hpi_ea20"] = d4(p["ln_hpi_ea20"], g)
    X["bis_hpi_real"] = d4(np.log(p["bis_hpi_xm_real"]), g)
    X["turistas"] = d4(p["ln_turistas_ccaa"], g)
    X["vut"] = d4(p["ln_vut_viviendas"], g)
    if mercado == "compra":
        y = d4(p["ln_valor_tasado_ccaa_real"], g)
    else:
        y = d4(p["ln_ipc_alquiler"] - lipc, g)
    df = pd.DataFrame({"t": p["trimestre"], "ccaa": g, "y": y})
    for k in range(1, 5):
        df[f"y{k}"] = y.groupby(g).shift(k)
    cm = y.groupby(p["trimestre"]).transform("mean")  # media transversal contemporanea = factor comun (PC1 ~ media)
    cmq = cm.groupby(g).shift(1)
    df["fc1"] = cmq
    df["fc2"] = cm.groupby(g).shift(2)
    for c in X.columns:
        df[c] = X[c].groupby(g).shift(1)  # retardo de 1 trimestre
    return df


def construir_nacional(mercado: str):
    d = mc.cargar()
    medida = "tasado" if mercado == "compra" else "ipc_alquiler"
    dep, X, interp, niv = mc.preparar(d, mercado, medida, "ipc", "interanual")
    df = pd.DataFrame({"t": d.index, "y": dep.values}, index=d.index)
    for k in range(1, 5):
        df[f"y{k}"] = dep.shift(k)
    df["fc1"] = dep.shift(1) * 0.0  # sin factor comun transversal en el nacional
    fam = {}
    ventana = [t for t in d.index if "2003Q2" <= t <= "2026Q2"]
    for c in mc.CANDIDATAS:
        xl = X[c.clave].shift(1)
        cob = xl.loc[ventana].notna().mean()
        if cob >= 0.98 and not mc.es_interpolada(X[c.clave], interp[c.clave], ventana):
            df[c.clave] = xl
            fam[c.clave] = c.familia
    nv = niv.copy()
    nv.index = d.index
    return df, fam, nv


def periodo_de(t):
    for k in PERS:
        a, b = mc.PERIODOS[k]
        if a <= t <= b:
            return k
    return "fuera"


def periodo_r0(t):
    """Periodo de un trimestre para el resumen SHAP: igual que periodo_de, pero P5 termina en 2026T1 (R0)."""
    return "fuera" if t > ULTIMO_R0 else periodo_de(t)


def bh(p, q=0.10):
    """p ajustado BH sobre los valores finitos (NaN se conserva)."""
    from scipy.stats import false_discovery_control
    p = pd.Series(p, dtype=float).reset_index(drop=True)
    out = pd.Series(np.nan, index=p.index)
    m = p.notna()
    if m.any():
        out[m] = false_discovery_control(p[m].values, method="bh")
    return out.values


def folds_tiempo(quarters, n_splits=5, test_size=8, gap=4):
    from sklearn.model_selection import TimeSeriesSplit
    q = np.array(sorted(set(quarters)))
    out = []
    for tr, te in TimeSeriesSplit(n_splits=n_splits, test_size=test_size, gap=gap).split(q):
        out.append((set(q[tr]), set(q[te])))
    return out


# ------------------------------------------------------------------ modelos
def monot_vec(cols, activar):
    return [MONO.get(c, 0) if activar else 0 for c in cols]


def fit_lgbm(Xtr, ytr, cfg, mono, seed=SEED):
    m = sg.modelo_lgbm(seed, monotone_constraints=monot_vec(list(Xtr.columns), mono), **CFG[cfg])
    return m.fit(Xtr.values.astype(float), np.asarray(ytr, float))


def fit_ar(dtr, cols, fe):
    A = _ar_mat(dtr, cols, fe, None)
    b = np.linalg.lstsq(A, dtr["y"].values, rcond=None)[0]
    return b


def _ar_mat(d, cols, fe, ccaas):
    A = [np.ones(len(d))] + [d[c].values for c in cols]
    if fe:
        for c in ccaas[1:]:
            A.append((d["ccaa"].values == c).astype(float))
    return np.column_stack(A)


def pred_ar(dtr, dte, cols, fe):
    cc = sorted(dtr["ccaa"].unique()) if fe else None
    b = np.linalg.lstsq(_ar_mat(dtr, cols, fe, cc), dtr["y"].values, rcond=None)[0]
    return _ar_mat(dte, cols, fe, cc) @ b


def pred_gam(dtr, dte, smooth, lin, alpha, df_sp=5):
    from statsmodels.gam.api import BSplines, GLMGam
    mu, sd = dtr[smooth].mean(), dtr[smooth].std(ddof=0).replace(0, 1)
    Ztr = ((dtr[smooth] - mu) / sd).values
    lo, hi = Ztr.min(0), Ztr.max(0)
    Zte = np.clip(((dte[smooth] - mu) / sd).values, lo, hi)
    k = len(smooth)
    bs = BSplines(Ztr, df=[df_sp] * k, degree=[3] * k)
    ex_tr = np.column_stack([np.ones(len(dtr))] + [dtr[c].values for c in lin])
    ex_te = np.column_stack([np.ones(len(dte))] + [dte[c].values for c in lin])
    r = GLMGam(dtr["y"].values, exog=ex_tr, smoother=bs, alpha=[alpha] * k).fit()
    return np.asarray(r.predict(exog=ex_te, exog_smooth=Zte))


def ecm_nacional(dtr, dte, nv):
    cols = ["lvl_o", "lvl_c", "lvl_r"]
    L = pd.DataFrame({"lvl_y": nv["y"], "lvl_o": nv["ocupados"], "lvl_c": nv["costes"], "lvl_r": nv["rdb"]})
    L1 = L.shift(1).add_suffix("_l1")
    D = 100 * nv[["ocupados", "costes", "rdb"]].diff()
    D.columns = ["docup", "dcost", "drdb"]
    aux = pd.concat([L, L1, D], axis=1)
    atr, ate = aux.loc[dtr["t"]], aux.loc[dte["t"]]
    cc = np.linalg.lstsq(np.column_stack([np.ones(len(atr)), atr[cols]]), atr["lvl_y"], rcond=None)[0]

    def ect(a):
        return a["lvl_y_l1"].values - np.column_stack([np.ones(len(a)), a[["lvl_o_l1", "lvl_c_l1", "lvl_r_l1"]]]) @ cc

    def M(a, dd):
        return np.column_stack([np.ones(len(a)), ect(a), a[["docup", "dcost", "drdb"]].values, dd["y1"].values])
    be = np.linalg.lstsq(M(atr, dtr), dtr["y"].values, rcond=None)[0]
    return M(ate, dte) @ be


# ------------------------------------------------------------------ evaluacion fuera de muestra
def evaluar_oos(df, fams_cols, fam_of, mercado, ambito, nv=None, rapido=False):
    """Devuelve (oos_pred DataFrame con una columna por modelo, dict de modelos). Misma muestra de prueba para todos."""
    cols_f = list(fams_cols)
    ar4 = ["y1", "y2", "y3", "y4"]
    arfc = ar4 + ["fc1", "fc2"] if ambito != "nacional" else ar4
    panel = ambito != "nacional"
    folds = folds_tiempo(df["t"], n_splits=5 if not rapido else 3)
    filas = []
    for tr_q, te_q in folds:
        dtr, dte = df[df["t"].isin(tr_q)], df[df["t"].isin(te_q)]
        # embargo adicional: el objetivo de entrenamiento no puede solapar con el primer trimestre de prueba (gap=4 ya lo garantiza)
        P = pd.DataFrame({"t": dte["t"].values, "ccaa": dte["ccaa"].values if panel else 0, "y": dte["y"].values})
        P["ar4"] = pred_ar(dtr, dte, ar4, panel)
        if panel:
            P["ar4_fc"] = pred_ar(dtr, dte, arfc, True)
        else:
            P["ecm_v1"] = ecm_nacional(dtr, dte, nv)
        Xf_tr, Xf_te = dtr[cols_f], dte[cols_f]
        Xa_cols = cols_f + ar4 + (["fc1"] if panel else [])
        for cfg in ("A", "B"):
            for mono in (True, False):
                tag = f"{cfg}{'m' if mono else 'n'}"
                m = fit_lgbm(Xf_tr, dtr["y"], cfg, mono)
                P[f"lgbm_fam_{tag}"] = m.predict(Xf_te.values.astype(float))
                m = fit_lgbm(dtr[Xa_cols], dtr["y"], cfg, mono)
                P[f"lgbm_ar_{tag}"] = m.predict(dte[Xa_cols].values.astype(float))
        for nom, al in ALFAS.items():
            P[f"gam_fam_{nom}"] = pred_gam(dtr, dte, cols_f, [], al)
            P[f"gam_ar_{nom}"] = pred_gam(dtr, dte, cols_f, ar4 + (["fc1"] if panel else []), al)
        filas.append(P)
    return pd.concat(filas, ignore_index=True)


def metricas(P, bases, ambito):
    """RMSE y DM-HLN (h=4) por modelo. Pérdida media transversal por trimestre (panel)."""
    modelos = [c for c in P.columns if c not in ("t", "ccaa", "y")]
    E = {m: (P["y"] - P[m]) for m in modelos}
    filas = []
    for m in modelos:
        rmse = float(np.sqrt(np.mean(E[m] ** 2)))
        fila = {"modelo": m, "rmse": rmse, "n_test": len(P), "n_trim": P["t"].nunique()}
        for b in bases:
            if m == b:
                fila[f"dm_vs_{b}"] = np.nan
                fila[f"p_vs_{b}"] = np.nan
                continue
            l1 = (E[m] ** 2).groupby(P["t"]).mean()
            l2 = (E[b] ** 2).groupby(P["t"]).mean()
            r = dm_test(np.sqrt(l1.values), np.sqrt(l2.values), h=4)
            fila[f"dm_vs_{b}"] = r["DM"]
            fila[f"p_vs_{b}"] = r["p"]
        filas.append(fila)
    M = pd.DataFrame(filas)
    M["base_mas_exigente"] = M[M["modelo"].isin(bases)].sort_values("rmse")["modelo"].iloc[0]
    be = M.loc[M["modelo"] == M["base_mas_exigente"].iloc[0], "rmse"].iloc[0]
    exig = M["base_mas_exigente"].iloc[0]
    pe = [r[f"p_vs_{exig}"] if m != exig else np.nan for m, r in zip(M["modelo"], M.to_dict("records"))]
    de = [r[f"dm_vs_{exig}"] if m != exig else np.nan for m, r in zip(M["modelo"], M.to_dict("records"))]
    M["dm_vs_exigente"], M["p_vs_exigente"] = de, pe
    M["predice_mejor"] = [(m not in bases) and (r < be) and (p < 0.05) and (d < 0) for m, r, p, d in zip(M["modelo"], M["rmse"], pe, de)]
    return M


# ------------------------------------------------------------------ SHAP por periodo con bandas
def bloques_tiempo(quarters_idx, T, L, rng):
    n = int(np.ceil(T / L))
    st = rng.integers(0, T - L + 1, n)
    return (st[:, None] + np.arange(L)[None, :]).ravel()[:T]


def shap_periodos(d, cols, grupos, B, cfg="A", mono=True, mascara=None):
    """Ajusta en toda la muestra el modelo SOLO FAMILIAS (sin retardos de y), SHAP agrupado por familia, medias por periodo y
    bandas por bootstrap de bloques de 4 trimestres (reajuste en cada replica). J12 (a): el SHAP de cada replica se evalua SOLO en sus
    filas dentro de la bolsa (trimestres remuestreados, sin repetir), para que la banda quede centrada en el punto (sin atenuacion fuera de
    la bolsa). `mascara` (opcional) restringe el resumen a las filas con dato (turismo)."""
    X = d[cols].reset_index(drop=True)
    y = d["y"].values
    tt = d["t"].values
    per = np.array([periodo_r0(t) for t in tt])
    if mascara is not None:
        per = np.where(np.asarray(mascara), per, "fuera")
    quarters = sorted(set(tt))
    qi = {q: np.where(tt == q)[0] for q in quarters}
    Tper = {pr: len(set(tt[(per != "fuera") if pr == "completo" else (per == pr)])) for pr in PERS + ["completo"]}
    m0 = fit_lgbm(X, y, cfg, mono)
    sv0 = sg.shap_valores(m0, X)
    imp0, impvar, g0 = sg.shap_grupos(m0, X, grupos, sv=sv0)
    pred0 = m0.predict(X.values.astype(float))
    base0 = float(np.mean(pred0 - sv0.sum(1)))

    def resumen(g, pred, rows):
        """g: DataFrame de SHAP por familia con indice = posicion global de `rows`."""
        out = {}
        sel = np.zeros(len(y), bool)
        sel[rows] = True
        gg = g.copy()
        gg.index = rows
        for pr in PERS + ["completo"]:
            msk = sel & ((per != "fuera") if pr == "completo" else (per == pr))
            if msk.sum() == 0:
                continue
            idx = np.where(msk)[0]
            gm = gg.loc[idx]
            res = float(np.mean(y[idx] - pred[np.searchsorted(rows, idx)]))
            out[pr] = (gm.mean(), gm.abs().mean(), res)
        return out

    punt = resumen(g0, pred0, np.arange(len(y)))
    rng = np.random.default_rng(SEED)
    reps = []
    L = 4
    for b in range(B):
        ib = bloques_tiempo(None, len(quarters), L, rng)
        rows = np.concatenate([qi[quarters[j]] for j in ib])
        mb = fit_lgbm(X.iloc[rows], y[rows], cfg, mono, seed=SEED + b + 1)
        bag = np.unique(rows)                       # filas dentro de la bolsa, sin repetir
        Xb = X.iloc[bag]
        svb = sg.shap_valores(mb, Xb)
        _, _, gb = sg.shap_grupos(mb, Xb, grupos, sv=svb)
        reps.append(resumen(gb, mb.predict(Xb.values.astype(float)), bag))
    return {"punt": punt, "reps": reps, "base": base0, "imp": imp0, "modelo": m0, "X": X, "y": y, "per": per, "g": g0, "sv": sv0, "T": Tper}


def tablas_shap(res, mercado, ambito, metodo="shap", fams=None, nota_extra="", variante="lgbm_A_monotono", principal="si", periodos=None):
    """contribucion_pp = media interanual de la contribucion SHAP x T/4 (aproximacion declarada de la variacion acumulada, suma de tasas
    trimestrales reales log x100; T = trimestres del periodo en la muestra, P5 hasta 2026T1). Bandas = percentiles de las replicas (en bolsa)."""
    atr, rk = [], []
    fams = fams or list(res["g"].columns)
    for pr, (c, ab, rs) in res["punt"].items():
        if periodos is not None and pr not in periodos:
            continue
        reps = [r[pr] for r in res["reps"] if pr in r]
        if not reps:
            continue
        esc = res["T"][pr] / 4.0
        C = pd.DataFrame([r[0] for r in reps])[fams]
        A = pd.DataFrame([r[1] for r in reps])[fams]
        tot = ab[fams].sum()
        for f in fams:
            q = np.quantile(C[f], [0.05, 0.16, 0.84, 0.95]) * esc
            atr.append(dict(metodo=metodo, mercado=mercado, ambito=ambito, periodo=pr, factor=f, contribucion_pp=float(c[f]) * esc,
                            pct_total=float(100 * ab[f] / tot) if tot > 0 else np.nan, b68_lo=q[1], b68_hi=q[2], b90_lo=q[0], b90_hi=q[3],
                            capa="C4", variante=variante, principal=principal,
                            notas=f"{NOTA_C4}; contribucion_pp = media interanual de la contribucion SHAP x T/4 (T={res['T'][pr]} trimestres; aproximacion declarada de la variacion acumulada); "
                                  f"pct_total (%) = cuota de |SHAP| medio; bandas = percentiles del bootstrap de bloques de 4 trimestres (B={len(reps)}), reajuste del modelo, "
                                  f"SHAP evaluado en las filas dentro de la bolsa (J12){nota_extra}"))
        qr = np.quantile([r[2] for r in reps], [0.05, 0.16, 0.84, 0.95]) * esc
        atr.append(dict(metodo=metodo, mercado=mercado, ambito=ambito, periodo=pr, factor="residuo", contribucion_pp=float(rs) * esc, pct_total=np.nan,
                        b68_lo=qr[1], b68_hi=qr[2], b90_lo=qr[0], b90_hi=qr[3], capa="C4", variante=variante, principal=principal,
                        notas=f"{NOTA_C4}; residuo = (tasa observada media - prediccion media) x T/4; error de ajuste dentro de muestra"))
        # ranking por |SHAP| medio de familia
        R = A.rank(axis=1, ascending=False, method="average")
        for f in fams:
            rk.append(dict(mercado=mercado, ambito=ambito, periodo=pr, factor=f, rango_mediano=float(R[f].median()),
                           prob_primero=float((R[f] == R.min(axis=1)).mean()), imp_abs_pp=float(ab[f]), rango_punto=float(ab[fams].rank(ascending=False)[f]),
                           B=len(reps)))
    return pd.DataFrame(atr), pd.DataFrame(rk)


def punto_en_banda(atr):
    """J12: cuantos puntos caen fuera de su banda (68 y 90 %)."""
    a = atr[atr["b68_lo"].notna()]
    f68 = int(((a["contribucion_pp"] < a["b68_lo"]) | (a["contribucion_pp"] > a["b68_hi"])).sum())
    f90 = int(((a["contribucion_pp"] < a["b90_lo"]) | (a["contribucion_pp"] > a["b90_hi"])).sum())
    return {"filas": int(len(a)), "fuera_b68": f68, "fuera_b90": f90}


# ------------------------------------------------------------------ DML manual con cross-fitting por bloques con embargo
def dml(df, treat, controles, mercado, ambito, rapido=False):
    from sklearn.ensemble import HistGradientBoostingRegressor
    d = df.dropna(subset=["y", treat] + controles).reset_index(drop=True)
    qs = sorted(d["t"].unique())
    K = 5
    bl = np.array_split(np.arange(len(qs)), K)
    Yt = np.zeros(len(d))
    Dt = np.zeros(len(d))
    W = d[controles].values
    for k in range(K):
        te_q = {qs[i] for i in bl[k]}
        lo, hi = min(bl[k]) - 4, max(bl[k]) + 4  # embargo de 4 trimestres a ambos lados
        tr_q = {qs[i] for i in range(len(qs)) if i < lo or i > hi}
        te = d["t"].isin(te_q).values
        tr = d["t"].isin(tr_q).values
        for tgt, arr in (("y", Yt), (treat, Dt)):
            mdl = HistGradientBoostingRegressor(max_depth=3, max_iter=100 if not rapido else 30, learning_rate=0.05, random_state=SEED)
            mdl.fit(W[tr], d.loc[tr, tgt].values)
            arr[te] = d.loc[te, tgt].values - mdl.predict(W[te])
    cl = d["t"].values

    def cluster_reg(Z, yv):
        b = np.linalg.lstsq(Z, yv, rcond=None)[0]
        e = yv - Z @ b
        ZtZi = np.linalg.pinv(Z.T @ Z)
        G = sorted(set(cl))
        S = np.zeros((Z.shape[1], Z.shape[1]))
        for g in G:
            s = Z[cl == g].T @ e[cl == g]
            S += np.outer(s, s)
        V = ZtZi @ S @ ZtZi * len(G) / (len(G) - 1)
        se = np.sqrt(np.diag(V))
        p = 2 * stats.t.sf(np.abs(b / se), len(G) - 1)
        return b, se, p, len(G)
    b, se, p, G = cluster_reg(Dt[:, None], Yt)
    out = [dict(periodo="completo", beta=float(b[0]), ee=float(se[0]), p=float(p[0]), n=len(d), n_trim=G)]
    per = np.array([periodo_de(t) for t in d["t"]])
    pp = [k for k in PERS if (per == k).sum() >= 17 * 6]
    if pp:
        Z = np.column_stack([Dt * (per == k) for k in pp])
        msk = np.isin(per, pp)
        cl_b = cl
        cl = cl_b[msk]
        b2, se2, p2, _ = cluster_reg(Z[msk], Yt[msk])
        cl = cl_b
        for k, bb, ss, ppv in zip(pp, b2, se2, p2):
            out.append(dict(periodo=k, beta=float(bb), ee=float(ss), p=float(ppv), n=int((per == k).sum()), n_trim=int(len(set(d.loc[per == k, "t"])))))
    R = pd.DataFrame(out)
    R["ic95_lo"] = R["beta"] - stats.t.ppf(0.975, max(G - 1, 1)) * R["ee"]
    R["ic95_hi"] = R["beta"] + stats.t.ppf(0.975, max(G - 1, 1)) * R["ee"]
    R["mercado"], R["ambito"], R["variable"] = mercado, ambito, treat
    return R


# ------------------------------------------------------------------ ALE / perm / interacciones / sustituto
def interpretacion(d, cols, grupos, mercado, ambito, rapido):
    X = d[cols].reset_index(drop=True)
    y = d["y"].values
    m = fit_lgbm(X, y, "A", True)
    ale = []
    for c in cols:
        a = sg.ale_1d(m.predict, X, c, K=15)
        a["variable"] = c
        a["familia"] = [k for k, v in grupos.items() if c in v][0]
        a["tipo"] = "ale"
        a = a.rename(columns={"ale": "valor"})
        pdp = sg.pdp_1d(m.predict, X, c, n_grid=15).rename(columns={"pdp": "valor"})
        pdp["variable"], pdp["familia"], pdp["tipo"] = c, a["familia"].iloc[0], "pdp"
        ale += [a, pdp]
    ALE = pd.concat(ale, ignore_index=True)
    ALE["mercado"], ALE["ambito"] = mercado, ambito
    I = sg.interacciones_shap(m, X, grupos, max_n=150 if rapido else 300)
    I = I.stack().rename("shap_inter_abs").reset_index().rename(columns={"level_0": "familia_a", "level_1": "familia_b"})
    I["mercado"], I["ambito"] = mercado, ambito
    S = sg.sustituto(m, X, 3)
    cor = X.corr().abs()
    cmax = float(np.nanmax(np.where(np.eye(len(cols)) == 1, np.nan, cor.values)))
    return ALE, I, S, cmax


def perm_oos(df, cols, grupos, folds, mercado, ambito, n_rep):
    acc = []
    for tr_q, te_q in folds:
        dtr, dte = df[df["t"].isin(tr_q)], df[df["t"].isin(te_q)]
        m = fit_lgbm(dtr[cols], dtr["y"], "A", True)
        acc.append(sg.perm_agrupada(m, dte[cols].reset_index(drop=True), dte["y"].values, grupos, n_rep=n_rep))
    P = pd.concat(acc, axis=1).mean(axis=1).rename("delta_rmse").reset_index().rename(columns={"index": "factor"})
    P["mercado"], P["ambito"] = mercado, ambito
    P["nota"] = "permutacion agrupada fuera de muestra (media de los bloques de prueba); aviso: familias correlacionadas"
    return P


# ------------------------------------------------------------------ principal
def main(rapido=False, salida=None):
    t0 = time.time()
    out = Path(salida) if salida else RAIZ / "output" / "v8" / "M9"
    out.mkdir(parents=True, exist_ok=True)
    reg = Registry(out / "registro.csv")
    B = 12 if rapido else 200
    B_est = 6 if rapido else 30
    n_rep = 2 if rapido else 5
    atr_all, rk_all, oos_all, dml_all, ale_all, int_all, perm_all, est_all, sens_all, sus = [], [], [], [], [], [], [], [], [], {}
    diag = {}
    contexts = []
    paneles = {}
    turismo_diag = {}
    banda_diag = {}
    for mercado in ("compra", "alquiler"):
        dfp = construir_panel(mercado)
        paneles[mercado] = dfp          # J13: un panel por mercado (antes se reutilizaba el del ultimo bucle)
        cols_f = list(PANEL_VARS)
        d = dfp.dropna(subset=["y", "y1", "y2", "y3", "y4", "fc1", "fc2"] + cols_f).reset_index(drop=True)
        d["periodo"] = d["t"].map(periodo_de)
        contexts.append((mercado, "ccaa_panel", d, cols_f, dict(PANEL_VARS), None))
        dn, famn, nv = construir_nacional(mercado)
        coln = list(famn)
        dnn = dn.dropna(subset=["y", "y1", "y2", "y3", "y4"] + coln).reset_index(drop=True)
        dnn["ccaa"] = 0
        contexts.append((mercado, "nacional", dnn, coln, famn, nv))

    for mercado, ambito, d, cols, fam_of, nv in contexts:
        ts = time.time()
        grupos = {}
        for c in cols:
            grupos.setdefault(fam_of[c], []).append(c)
        grupos = {k: grupos[k] for k in FAMS if k in grupos}
        panel = ambito != "nacional"
        print(f"[M9] {mercado}/{ambito}: n={len(d)}, trimestres={d['t'].nunique()} ({d['t'].min()}..{d['t'].max()}), familias={list(grupos)}", flush=True)
        # ---- fuera de muestra
        P = evaluar_oos(d, cols, fam_of, mercado, ambito, nv=nv, rapido=rapido)
        bases = ["ar4", "ar4_fc"] if panel else ["ar4", "ecm_v1"]
        M = metricas(P, bases, ambito)
        M.insert(0, "ambito", ambito)
        M.insert(0, "mercado", mercado)
        oos_all.append(M)
        pe_bases = [f"{b}" for b in bases]
        for r in M.to_dict("records"):
            fam_mod = "base" if r["modelo"] in bases else ("gam" if r["modelo"].startswith("gam") else "lightgbm")
            reg.log("M9", f"m9_{mercado}_{ambito}_{r['modelo']}", f"y_t ~ {r['modelo']}(X_(t-1))", d["t"].min(), d["t"].max(), int(r["n_test"]),
                    np.nan, np.nan, np.nan, r["rmse"], np.nan, r.get("p_vs_exigente", np.nan),
                    f"{fam_mod}; fuera de muestra 5 bloques de 8 trimestres con embargo 4; DM-HLN h=4 frente a la base mas exigente ({r['base_mas_exigente']}); "
                    f"p_vs_exigente en la columna p_interes; C4; contraste")
        diag[f"{mercado}/{ambito}"] = {"n": int(len(d)), "trimestres": [d["t"].min(), d["t"].max()], "n_test": int(len(P)), "bases": bases}
        # ---- SHAP por periodo con bandas (modelo solo familias, config A con monotonia = principal)
        res = shap_periodos(d, cols, grupos, B, "A", True)
        atr, rk = tablas_shap(res, mercado, ambito, fams=list(grupos))
        banda_diag[f"{mercado}/{ambito}"] = punto_en_banda(atr)
        atr_all.append(atr)
        rk_all.append(rk)
        reg.log("M9", f"m9_{mercado}_{ambito}_shap_periodos", "SHAP agrupado, LGBM A monotono, solo familias", d["t"].min(), d["t"].max(), len(d), np.nan, np.nan,
                np.nan, np.nan, np.nan, np.nan, f"bootstrap de bloques B={B}; C4")
        # ---- sensibilidad del ranking: A sin monotonia, B con y sin
        imp_ref = res["imp"]
        for cfg, mono in (("A", False), ("B", True), ("B", False)):
            mm = fit_lgbm(d[cols].reset_index(drop=True), d["y"].values, cfg, mono)
            imp, _, _ = sg.shap_grupos(mm, d[cols].reset_index(drop=True), grupos)
            rho = stats.spearmanr(imp_ref.reindex(imp.index), imp)[0] if len(imp) > 2 else np.nan
            for f in imp.index:
                sens_all.append(dict(mercado=mercado, ambito=ambito, variante=f"{cfg}{'_monotono' if mono else '_sin_monotonia'}", factor=f, imp_abs_pp=float(imp[f]),
                                     rango=int(list(imp.index).index(f) + 1), spearman_vs_principal=rho))
            reg.log("M9", f"m9_{mercado}_{ambito}_sens_{cfg}_{'mono' if mono else 'libre'}", "SHAP agrupado sensibilidad", d["t"].min(), d["t"].max(), len(d),
                    np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, "sensibilidad al hiperparametro / monotonia")
        for f in imp_ref.index:
            sens_all.append(dict(mercado=mercado, ambito=ambito, variante="A_monotono (principal)", factor=f, imp_abs_pp=float(imp_ref[f]),
                                 rango=int(list(imp_ref.index).index(f) + 1), spearman_vs_principal=1.0))
        # ---- estabilidad del ranking (herramienta, bootstrap por bloques de 4 trimestres)
        Xs = d[cols].reset_index(drop=True)
        mono_v = monot_vec(cols, True)
        ee = sg.estabilidad_ranking(Xs, d["y"].values, grupos,
                                    fit_fn=lambda seed=SEED, mv=mono_v: sg.modelo_lgbm(seed, monotone_constraints=mv),
                                    B=B_est, bloque=(17 * 4 if panel else 4))
        for f in ee["ranking"]:
            est_all.append(dict(mercado=mercado, ambito=ambito, factor=f, rango_ref=ee["ranking"].index(f) + 1,
                                pct_misma_pos_bootstrap=float(ee["pct_misma_pos_bootstrap"][f]), pct_misma_pos_pliegues=float(ee["pct_misma_pos_pliegues"][f]),
                                pct_ranking_completo_bootstrap=ee["pct_ranking_completo_bootstrap"], pct_ranking_completo_pliegues=ee["pct_ranking_completo_pliegues"],
                                B=B_est))
        # ---- interpretacion
        ALE, I, S, cmax = interpretacion(d, cols, grupos, mercado, ambito, rapido)
        ale_all.append(ALE)
        int_all.append(I)
        sus[f"{mercado}/{ambito}"] = {"fidelidad_r2": S["fidelidad_r2"], "reglas": S["reglas"], "max_corr_abs_entre_variables": cmax}
        perm_all.append(perm_oos(d, cols, grupos, folds_tiempo(d["t"], 5 if not rapido else 3), mercado, ambito, n_rep))
        # ---- GAM: ajuste completo para coeficientes de suavizado (solo registro de la especificacion)
        # ---- DML (solo panel)
        if panel:
            dd = d.copy()
            for treat, lab in (("tipo_hip_real", "credito_tipos"), ("epa_pob", "demografia")):
                ctrl = [c for c in cols if c != treat] + ["y1", "y2", "y3", "y4"]
                R = dml(dd, treat, ctrl, mercado, ambito, rapido)
                R["familia"] = lab
                dml_all.append(R)
                r0 = R.iloc[0]
                reg.log("M9", f"m9_{mercado}_{ambito}_dml_{treat}", f"DML parcial: y ~ theta*{treat}; nuisance HGB, cross-fitting por bloques con embargo 4",
                        d["t"].min(), d["t"].max(), int(r0["n"]), np.nan, np.nan, np.nan, np.nan, r0["beta"], r0["p"], "C4: sin identificacion; EE cluster por trimestre")
            # sensibilidad con turismo (NaN nativos), solo atribucion; panel DEL MERCADO (J13) y solo periodos con cobertura >= 70 %
            dt = paneles[mercado].dropna(subset=["y", "y1", "y2", "y3", "y4", "fc1", "fc2"] + cols).reset_index(drop=True)
            colt = cols + list(TURISMO_VARS)
            fam_t = {**fam_of, **TURISMO_VARS}
            gt = {}
            for c in colt:
                gt.setdefault(fam_t[c], []).append(c)
            gt = {k: gt[k] for k in FAMS if k in gt}
            tiene = dt["turistas"].notna().values
            ccaa_t = set(dt.loc[tiene, "ccaa"])
            per_t = np.array([periodo_r0(t) for t in dt["t"]])
            cob_per = {}
            for pr in PERS:
                sel = (per_t == pr) & dt["ccaa"].isin(ccaa_t).values
                cob_per[pr] = float(tiene[sel].mean()) if sel.sum() else 0.0
            ok_per = [pr for pr in PERS if cob_per[pr] >= 0.70]
            turismo_diag[mercado] = {"ccaa_con_turismo": len(ccaa_t), "cobertura_por_periodo": {k: round(v, 3) for k, v in cob_per.items()},
                                                                   "periodos_reportados": ok_per}
            rt = shap_periodos(dt, colt, gt, max(B // 3, 8), "A", True, mascara=tiene)
            at, rkt = tablas_shap(rt, mercado, ambito, metodo="shap_sens_turismo", fams=list(gt), variante="lgbm_A_monotono_turismo_nan", principal="no",
                                  periodos=ok_per,
                                  nota_extra=f"; sensibilidad con turismo ({len(ccaa_t)} CCAA desde 2016T4, NaN nativos de LightGBM; resumen solo en filas con dato de turismo; "
                                             "periodos con cobertura >= 70 %); SHAP de turismo solo informativo")
            atr_all.append(at[at["factor"].isin(["turismo"])])
            reg.log("M9", f"m9_{mercado}_{ambito}_sens_turismo", "SHAP con turismo NaN nativo", dt["t"].min(), dt["t"].max(), len(dt), np.nan, np.nan, np.nan,
                    np.nan, np.nan, np.nan, f"sensibilidad turismo; panel de {mercado}; periodos {ok_per}")
        print(f"[M9] {mercado}/{ambito} listo en {time.time() - ts:.0f}s", flush=True)

    # ---- escritura
    ATR = pd.concat(atr_all, ignore_index=True)[COLS_ATR]
    ATR.to_csv(out / "atribucion.csv", index=False)
    pd.concat(rk_all, ignore_index=True).to_csv(out / "ranking_shap.csv", index=False)
    OOS = pd.concat(oos_all, ignore_index=True)
    for c_ in [c for c in OOS.columns if c.startswith("p_vs_")]:
        OOS[c_.replace("p_vs_", "p_ajustado_vs_")] = bh(OOS[c_].values)
    OOS["metodo_ajuste"] = "BH"
    be_ = OOS.groupby(["mercado", "ambito"]).apply(lambda g: g.loc[g["modelo"] == g["base_mas_exigente"].iloc[0], "rmse"].iloc[0])
    OOS["predice_mejor_bh"] = [(m not in ("ar4", "ar4_fc", "ecm_v1")) and (r < be_[(mer, am)]) and (pa < 0.10) and (dm < 0)
                               for m, r, pa, dm, mer, am in zip(OOS["modelo"], OOS["rmse"], OOS["p_ajustado_vs_exigente"], OOS["dm_vs_exigente"], OOS["mercado"], OOS["ambito"])]
    OOS.to_csv(out / "oos.csv", index=False)
    pd.DataFrame(est_all).to_csv(out / "estabilidad_ranking.csv", index=False)
    pd.DataFrame(sens_all).to_csv(out / "sensibilidad_ranking.csv", index=False)
    pd.concat(ale_all, ignore_index=True).to_csv(out / "ale_pdp.csv", index=False)
    pd.concat(int_all, ignore_index=True).to_csv(out / "interacciones_shap.csv", index=False)
    pd.concat(perm_all, ignore_index=True).to_csv(out / "importancia_permutacion.csv", index=False)
    (out / "sustituto.json").write_text(json.dumps(sus, ensure_ascii=False, indent=1, default=float))
    D = pd.concat(dml_all, ignore_index=True)
    D["p_ajustado"] = mc.bh(D["p"].values, 0.10)
    D["metodo_ajuste"] = "BH"
    D["capa"] = "C4"
    D["modulo"], D["familia_modelo"], D["tipo_ee"], D["script"] = "M9", "dml_manual", "cluster por trimestre", SCRIPT
    D["modelo_id"] = [f"m9_dml_{m}_{v}" for m, v in zip(D["mercado"], D["variable"])]
    D["dependiente"] = "crecimiento interanual real (log x100)"
    D["transformacion"] = "d4 log x100, retardo 1"
    D["medida_precio"] = np.where(D["mercado"] == "compra", "valor tasado real", "IPC alquiler real")
    D["t"] = D["beta"] / D["ee"]
    D["r2"] = np.nan
    D.reindex(columns=COLS_COEF).to_csv(out / "coeficientes.csv", index=False)   # columnas completas del contrato; vacias si no aplican

    # ---- resultado.json
    fm = {}
    for (mer, amb), g in OOS.groupby(["mercado", "ambito"]):
        bases = diag[f"{mer}/{amb}"]["bases"]
        gi = g.set_index("modelo")
        exig = g["base_mas_exigente"].iloc[0]
        fm[f"{mer}/{amb}"] = {
            "modelo": "lgbm_ar_Am (principal predictivo); lgbm_fam_Am (principal explicativo); gam_ar_alfa10; gam_fam_alfa10",
            "rmse": {m: round(float(gi.loc[m, "rmse"]), 4) for m in gi.index},
            "dm_vs_ar4": {m: {"DM": None if pd.isna(gi.loc[m, "dm_vs_ar4"]) else round(float(gi.loc[m, "dm_vs_ar4"]), 3),
                              "p": None if pd.isna(gi.loc[m, "p_vs_ar4"]) else round(float(gi.loc[m, "p_vs_ar4"]), 4)} for m in gi.index if m not in ("ar4",)},
            "base_mas_exigente": exig,
            "predice_mejor_que_la_base_mas_exigente": sorted(gi.index[gi["predice_mejor"]].tolist()),
            "predice_mejor_con_p_BH": sorted(gi.index[gi["predice_mejor_bh"]].tolist()),
        }
    dml_est = {f"{r.mercado}/{r.variable}": {"beta": round(r.beta, 4), "ee": round(r.ee, 4), "p_BH": round(r.p_ajustado, 3)} for r in D[D["periodo"] == "completo"].itertuples()}
    per_atr = ATR[(ATR["metodo"] == "shap") & (ATR["periodo"].isin(PERS)) & (ATR["ambito"] == "ccaa_panel") & (ATR["factor"] != "residuo")]
    est = {f"{r.mercado}/{r.periodo}/{r.factor}": round(r.contribucion_pp, 3) for r in per_atr.itertuples()}
    res_json = {
        "rama": "M9", "pregunta": "Que familias de variables usa un modelo de ML interpretable (LightGBM, GAM) para predecir el crecimiento real del precio de compra y del alquiler, y supera a AR(4)/ECM v1 fuera de muestra? (contraste, no causal)",
        "capa": "C4", "datos": "panel_ccaa_q_v8.csv (17 CCAA, codigo INE), nacional_q_v8.csv",
        "N": {k: v["n"] for k, v in diag.items()},
        "metodo": "LightGBM (monotonia en tipos, empleo, poblacion; sensibilidad sin monotonia), GLMGam (splines), SHAP agrupado por familia, permutacion agrupada fuera de muestra, ALE/PDP, interacciones SHAP, sustituto depth 3, estabilidad por bootstrap de bloques, DML manual con cross-fitting por bloques con embargo (C4)",
        "estimacion": {"shap_contribucion_media_pp_panel": est, "dml_theta_completo": dml_est},
        "ic95": "bandas 68/90 % por bootstrap de bloques en atribucion.csv; IC95 de DML en coeficientes.csv",
        "p_ajustado": {"metodo": "BH", "q": 0.10, "dml": {r.variable + "/" + r.mercado: round(r.p_ajustado, 3) for r in D[D["periodo"] == "completo"].itertuples()}},
        "nivel_evidencia": "EXPLORATORIO (C4)",
        "diagnosticos": {"muestras": diag, "sustituto_fidelidad_r2": {k: round(v["fidelidad_r2"], 3) for k, v in sus.items()},
                         "estabilidad": "estabilidad_ranking.csv", "retardos": "todos los predictores con retardo de 1 trimestre",
                         "presupuesto_hiperparametros": "LGBM 2 configs x 2 (monotonia) ; GAM 2 alfas; sin seleccion por error fuera de muestra"},
        "fuera_muestra": fm,
        "notas": [NOTA_C4, "Ningun modelo se presenta como explicacion si no supera a la base mas exigente; DML sin identificacion (C4)",
                  "Variables comunes en el tiempo (tipos, europeas) aportan T observaciones independientes efectivas, no 17xT",
                  "econml no usado: DML manual con bloques con embargo (docs/v8/desviaciones.md)"],
    }
    res_json["diagnosticos"]["shap_punto_en_banda"] = banda_diag
    res_json["diagnosticos"]["turismo_cobertura"] = turismo_diag
    res_json["diagnosticos"]["B_shap"] = B
    res_json["notas"].append("contribucion_pp de SHAP = media interanual x T/4 (aproximacion declarada de la variacion acumulada, log x100); P5 hasta 2026T1; "
                             "bandas con SHAP evaluado dentro de la bolsa (J12); turismo solo en periodos con cobertura >= 70 % y con el panel de cada mercado (J13)")
    (out / "resultado.json").write_text(json.dumps(res_json, ensure_ascii=False, indent=1, default=float))
    (out / "tiempos.json").write_text(json.dumps({"segundos": round(time.time() - t0, 1)}))
    escribir_resumen(out, OOS, ATR, D, sus, pd.DataFrame(est_all), res_json)
    reg.flush()
    print(f"[M9] terminado en {time.time() - t0:.0f}s")


def escribir_resumen(out, OOS, ATR, D, sus, EST, rj):
    L = ["# M9 - ML interpretable como contraste (C4)", "",
         "Contraste, no causal: ningun resultado de SHAP, importancias ni DML se lee como efecto. Capa C4 (EXPLORATORIO).", "",
         "## Fuera de muestra (5 bloques de 8 trimestres, embargo 4; DM-HLN h=4)", ""]
    for (mer, amb), g in OOS.groupby(["mercado", "ambito"]):
        exig = g["base_mas_exigente"].iloc[0]
        gi = g.set_index("modelo")
        top = gi[~gi.index.isin(["ar4", "ar4_fc", "ecm_v1"])].sort_values("rmse").head(3)
        bases = [m for m in ("ar4", "ar4_fc", "ecm_v1") if m in gi.index]
        L.append(f"- {mer}/{amb}: RMSE bases " + ", ".join(f"{m} {gi.loc[m, 'rmse']:.2f}" for m in bases) + f" (mas exigente: {exig}); mejores ML: "
                 + ", ".join(f"{m} {r.rmse:.2f} (p DM vs exigente {r.p_vs_exigente:.2f})" for m, r in top.iterrows())
                 + f". Predicen mejor: {', '.join(gi.index[gi['predice_mejor']]) or 'ninguno'}.")
    L += ["", "## Atribucion SHAP (modelo solo familias, panel; contribucion media pp; ver atribucion.csv con bandas)", ""]
    a = ATR[(ATR["metodo"] == "shap") & (ATR["ambito"] == "ccaa_panel") & (ATR["periodo"] == "P5") & (ATR["factor"] != "residuo")]
    for mer, g in a.groupby("mercado"):
        g = g.reindex(g["contribucion_pp"].abs().sort_values(ascending=False).index)
        L.append(f"- {mer} P5: " + "; ".join(f"{r.factor} {r.contribucion_pp:+.2f} [{r.b68_lo:+.2f}, {r.b68_hi:+.2f}]" for r in g.itertuples()))
    L += ["", "## DML manual (C4, sin identificacion)", ""]
    for r in D[D["periodo"] == "completo"].itertuples():
        L.append(f"- {r.mercado}, {r.variable}: theta {r.beta:+.3f} (EE {r.ee:.3f}), p BH {r.p_ajustado:.2f}")
    L += ["", "## Estabilidad del ranking y sustituto", ""]
    for k, v in sus.items():
        L.append(f"- {k}: fidelidad R2 del sustituto {v['fidelidad_r2']:.2f}; correlacion maxima entre variables {v['max_corr_abs_entre_variables']:.2f}")
    if len(EST):
        e = EST.groupby(["mercado", "ambito"])[["pct_ranking_completo_bootstrap", "pct_ranking_completo_pliegues"]].first()
        for (mer, amb), r in e.iterrows():
            L.append(f"- {mer}/{amb}: ranking completo reproducido en {100 * r.iloc[0]:.0f} % de replicas bootstrap y {100 * r.iloc[1]:.0f} % de pliegues")
    L += ["", "## Limites", "",
          "- Predictores con retardo de 1 trimestre; panel 2009T2-2026T2 (P1 solo en el nacional, desde 2003T2). Variables comunes en el tiempo aportan pocas observaciones independientes.",
          "- ECM v1 solo aproximado y solo nacional. Turismo solo en sensibilidad. Presupuesto de hiperparametros declarado y sin seleccion por error fuera de muestra."]
    (out / "resumen.md").write_text("\n".join(L) + "\n")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--rapido", action="store_true")
    ap.add_argument("--salida", default=None)
    a = ap.parse_args()
    main(a.rapido, a.salida)
