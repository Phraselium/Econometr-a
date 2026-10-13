#!/usr/bin/env python3
"""V8-F4 M6: colinealidad y peso relativo de los factores (capa C4: asociacion, NO causalidad).

Ecuacion del crecimiento nacional (interanual y trimestral, log x 100) del precio real de compra (valor tasado) y del alquiler real (IPC
alquiler) sobre UNA variable por familia (src/v8/m67_comun.py). Por periodo P1-P5 y completo:
VIF y Belsley; dominancia LMG/Shapley del R2 con bandas por bootstrap por bloques (B=499, bloque 4) y pesos de Johnson; ortogonalizacion
secuencial en todos los ordenes; indice compuesto (primera componente) como sensibilidad; Granger por bloques y LP-OLS con EWC (C4, predictivos);
BMA por enumeracion de 2^k modelos con BIC; ridge / elastic net con validacion temporal en bloques con embargo; OLS por periodo (coeficientes.csv).
Las atribuciones por dominancia describen la descomposicion del R2: NO son efectos causales.
Uso: python3 src/v8/m6_colinealidad.py [--rapido] [--salida DIR]
"""
from __future__ import annotations

import os

for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS"):
    os.environ[_v] = "1"

import argparse  # noqa: E402
import itertools  # noqa: E402
import json  # noqa: E402
import math  # noqa: E402
import sys  # noqa: E402
import time  # noqa: E402
import warnings  # noqa: E402
from pathlib import Path  # noqa: E402

import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402
import statsmodels.api as sm  # noqa: E402
from scipy import stats  # noqa: E402

RAIZ = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(RAIZ / "src"))
sys.path.insert(0, str(RAIZ / "src" / "v8"))
import m67_comun as C  # noqa: E402
from econ_utils import Registry, dm_test, holm  # noqa: E402
from herramientas import dominancia, lp  # noqa: E402

warnings.filterwarnings("ignore")
SEED = 20261010
SCRIPT = "src/v8/m6_colinealidad.py"
MERCADOS = [("compra", "tasado"), ("alquiler", "ipc_alquiler")]
TRANSF = ["interanual", "trimestral"]
B_BOOT = 499
BLOQUE = 4
ASOC = "asociacion (dominancia del R2), no causal"
VENTANA_P5_FIN = "2026Q1"   # R0: ventana comun de P5 = 2022T3-2026T1 en todos los metodos
ORIENTACION = {"tipo_hip_real": -1}   # tipos: expansivo = baja del tipo (x-1); el resto, «mas es mas presion»


def boot_phi(X, y, B, bloque, seed):
    """LMG absoluto (phi, suma = R2) y B remuestreos por bloques moviles. Devuelve (phi_hat, r2, draws[B, p])."""
    Xv, yv = dominancia._prep(X.values if isinstance(X, pd.DataFrame) else X, y)
    p = Xv.shape[1]
    players = [[j] for j in range(p)]
    cache = dominancia._r2_cache(Xv, yv, players)
    phi = np.asarray(dominancia._shapley_from_cache(cache, p), float)
    rng = np.random.default_rng(seed)
    n = len(yv)
    draws = np.empty((B, p))
    for b in range(B):
        idx = dominancia._boot_idx(n, bloque, rng)
        draws[b] = dominancia._shapley_from_cache(dominancia._r2_cache(Xv[idx], yv[idx], players), p)
    return phi, float(cache[frozenset(range(p))]), draws


def banda_basica(theta, draws, alpha, lo_clip=0.0, hi_clip=1.0):
    """Intervalo bootstrap «basico» centrado (2*theta - q_{1-a/2}, 2*theta - q_{a/2}), recortado a [lo_clip, hi_clip] (J16)."""
    ql, qh = np.quantile(draws, [alpha / 2, 1 - alpha / 2], axis=0)
    return np.clip(2 * theta - qh, lo_clip, hi_clip), np.clip(2 * theta - ql, lo_clip, hi_clip)


def hhmm(t0):
    return f"{(time.perf_counter() - t0) / 60:.1f} min"


def etiqueta_dep(transf, medida):
    return f"{'d4' if transf == 'interanual' else 'd'}_ln_{medida}_real"


def residualizar(y, X, Z):
    """Teorema de Frisch-Waugh: parte de y y X ortogonal a [1, Z]."""
    A = np.column_stack([np.ones(len(y))] + ([Z] if Z is not None and Z.shape[1] else []))
    P = A @ np.linalg.pinv(A.T @ A) @ A.T
    return y - P @ y, X - P @ X


def preparar_celda(d, dq_cache, mercado, medida, transf, periodo):
    """Muestra y variables de una celda (mercado, transformacion, periodo). Devuelve dict con y, X (DataFrame), dummies, motivos, etc."""
    dep, X, ip, niv = C.preparar(d, mercado, medida, "ipc", transf)
    win = C.ventana(d.index, periodo)
    sel, exc = C.elegir_principales(dep, X, ip, win)
    motivos = dict(exc)
    sel, D, mot2 = C.limitar_por_gl(dep, X, sel, win)
    motivos.update(mot2)
    out = {"dep": dep, "Xall": X, "ip": ip, "win": win, "sel": sel, "motivos": motivos, "n": len(D), "D": D}
    if not sel:
        return out
    epa = any(v in C.EPA_VARS for v in sel.values())
    nd = C.dummies_relevantes(D, d, epa, len(sel), transf)
    out["dummies"] = nd
    # variacion acumulada observada del periodo (J5/R0): suma de la tasa trimestral real en la ventana comun W_P; P5 = 2022T3-2026T1
    dq = dq_cache[(mercado, medida)]
    iw = [t for t in D.index if not (periodo == "P5" and t > VENTANA_P5_FIN)]
    out["variacion"] = float(dq.loc[iw].sum())
    out["nW"] = len(iw)
    out["span"] = (D.index[0], D.index[-1])
    return out


def descomponer(D, sel, d, nd):
    """Devuelve y, X (DataFrame) con las ficticias eliminadas por Frisch-Waugh (si las hay)."""
    cols = list(sel.values())
    y = D["dep"].values.astype(float)
    X = D[cols].values.astype(float)
    if nd:
        y, X = residualizar(y, X, d.loc[D.index, nd].values.astype(float))
    return y, pd.DataFrame(X, index=D.index, columns=list(sel.keys()))


def bma_celda(y, X, kmax):
    """Enumeracion de todos los modelos con k<=kmax regresores (variables tipificadas), BIC y probabilidades posteriores de inclusion."""
    n, p = X.shape
    Z = (X.values - X.values.mean(0)) / X.values.std(0, ddof=0)
    yz = (y - y.mean()) / y.std(ddof=0)
    filas = []
    for k in range(0, min(kmax, p) + 1):
        for S in itertools.combinations(range(p), k):
            if k:
                A = Z[:, list(S)]
                b = np.linalg.lstsq(A, yz, rcond=None)[0]
                rss = float(((yz - A @ b) ** 2).sum())
            else:
                b, rss = np.array([]), float((yz ** 2).sum())
            bic = n * np.log(max(rss, 1e-12) / n) + (k + 1) * np.log(n)
            filas.append((S, b, bic, 1 - rss / float(yz @ yz)))
    bics = np.array([f[2] for f in filas])
    w = np.exp(-0.5 * (bics - bics.min()))
    w /= w.sum()
    pip = np.zeros(p)
    pm = np.zeros(p)
    for wi, (S, b, _, _) in zip(w, filas):
        for j, s in enumerate(S):
            pip[s] += wi
            pm[s] += wi * b[j]
    return filas, w, pip, pm


def penalizados(y, X, n_splits, test_size, gap, seed=SEED):
    """Ridge y elastic net con CV temporal con embargo (TimeSeriesSplit con gap). Devuelve coeficientes tipificados y alpha."""
    from sklearn.linear_model import ElasticNetCV, RidgeCV
    from sklearn.model_selection import TimeSeriesSplit
    mu, sd = X.mean(0), X.std(0, ddof=0)
    Z = (X - mu) / sd
    cv = TimeSeriesSplit(n_splits=n_splits, test_size=test_size, gap=gap)
    rg = RidgeCV(alphas=np.logspace(-2, 3, 30), cv=cv).fit(Z, y - y.mean())
    en = ElasticNetCV(l1_ratio=[0.2, 0.5, 0.8, 0.95], cv=cv, max_iter=20000, random_state=seed, alphas=40).fit(Z, y - y.mean())
    return rg, en, sd


def oos_bloques(cell_y, Z, niv, ecm=True):
    """Validacion fuera de muestra en bloques con embargo (TimeSeriesSplit: 5 bloques de 8 trimestres, gap=4) en la MISMA muestra para
    AR(4), ECM v1 (aproximado) y los modelos de factores (ajuste condicional: usan los factores contemporaneos, NO es un pronostico puro)."""
    from sklearn.linear_model import ElasticNetCV, RidgeCV
    from sklearn.model_selection import TimeSeriesSplit
    y = cell_y.rename("y")
    df = pd.DataFrame({"y": y})
    for k in range(1, 5):
        df[f"y{k}"] = y.shift(k)
    for c in Z.columns:
        df[f"z_{c}"] = Z[c]
    dn = 100 * niv[["ocupados", "costes", "rdb"]].diff()
    df["docup"], df["dcost"], df["drdb"] = dn["ocupados"], dn["costes"], dn["rdb"]
    df["lvl_y"], df["lvl_o"], df["lvl_c"], df["lvl_r"] = niv["y"], niv["ocupados"], niv["costes"], niv["rdb"]
    df["lvl_y_l1"], df["lvl_o_l1"], df["lvl_c_l1"], df["lvl_r_l1"] = niv["y"].shift(1), niv["ocupados"].shift(1), niv["costes"].shift(1), niv["rdb"].shift(1)
    df = df.dropna()
    n = len(df)
    zc = [f"z_{c}" for c in Z.columns]
    ts = TimeSeriesSplit(n_splits=5, test_size=8, gap=4)
    errs = {m: [] for m in ("ar4", "ecm_v1", "ols_factores", "ridge", "enet")}
    idx_test = []
    for tr, te in ts.split(df):
        dtr, dte = df.iloc[tr], df.iloc[te]
        idx_test += list(dte.index)
        ar_c = ["y1", "y2", "y3", "y4"]
        b = np.linalg.lstsq(np.column_stack([np.ones(len(dtr)), dtr[ar_c]]), dtr["y"], rcond=None)[0]
        errs["ar4"] += list(dte["y"].values - np.column_stack([np.ones(len(dte)), dte[ar_c]]) @ b)
        # ECM v1 aproximado: ECT de los niveles (ocupados, costes, renta) estimados en el train; dy ~ ect_{t-1} + dX + dy_{t-1}
        Ltr = np.column_stack([np.ones(len(dtr)), dtr[["lvl_o", "lvl_c", "lvl_r"]]])
        cc = np.linalg.lstsq(Ltr, dtr["lvl_y"], rcond=None)[0]

        def ect(dd, cc=cc):
            return dd["lvl_y_l1"].values - np.column_stack([np.ones(len(dd)), dd[["lvl_o_l1", "lvl_c_l1", "lvl_r_l1"]]]) @ cc

        Etr = np.column_stack([np.ones(len(dtr)), ect(dtr), dtr[["docup", "dcost", "drdb", "y1"]]])
        be = np.linalg.lstsq(Etr, dtr["y"], rcond=None)[0]
        Ete = np.column_stack([np.ones(len(dte)), ect(dte), dte[["docup", "dcost", "drdb", "y1"]]])
        errs["ecm_v1"] += list(dte["y"].values - Ete @ be)
        mu, sd = dtr[zc].mean(), dtr[zc].std(ddof=0)
        Ztr, Zte = ((dtr[zc] - mu) / sd).values, ((dte[zc] - mu) / sd).values
        bo = np.linalg.lstsq(np.column_stack([np.ones(len(dtr)), Ztr]), dtr["y"], rcond=None)[0]
        errs["ols_factores"] += list(dte["y"].values - np.column_stack([np.ones(len(dte)), Zte]) @ bo)
        icv = TimeSeriesSplit(n_splits=3, test_size=6, gap=4)
        rg = RidgeCV(alphas=np.logspace(-2, 3, 30), cv=icv).fit(Ztr, dtr["y"].values)
        errs["ridge"] += list(dte["y"].values - rg.predict(Zte))
        en = ElasticNetCV(l1_ratio=[0.2, 0.5, 0.8, 0.95], cv=icv, max_iter=20000, random_state=SEED, alphas=30).fit(Ztr, dtr["y"].values)
        errs["enet"] += list(dte["y"].values - en.predict(Zte))
    errs = {k: np.array(v) for k, v in errs.items()}
    return errs, idx_test, n


def diagnosticos_ols(res, A):
    from statsmodels.stats.diagnostic import acorr_breusch_godfrey, breaks_cusumolsresid, het_breuschpagan, linear_reset
    from statsmodels.stats.stattools import jarque_bera
    out = dict(bg_p=np.nan, bp_p=np.nan, jb_p=np.nan, reset_p=np.nan, cusum_estable=np.nan)
    for k, f in (("bg_p", lambda: acorr_breusch_godfrey(res, nlags=int(min(4, max(1, res.nobs // 6))), store=False, result_object=False)[1]),
                 ("bp_p", lambda: het_breuschpagan(res.resid, A)[1]),
                 ("jb_p", lambda: jarque_bera(res.resid)[1]),
                 ("reset_p", lambda: float(linear_reset(res, power=2, use_f=True).pvalue)),
                 ("cusum_estable", lambda: bool(breaks_cusumolsresid(res.resid, ddof=A.shape[1])[1] > 0.05))):
        try:
            out[k] = f()
        except Exception:  # noqa: BLE001
            pass
    return out


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--rapido", action="store_true")
    ap.add_argument("--salida", default=str(RAIZ / "output" / "v8" / "M6"))
    a = ap.parse_args(argv)
    t0 = time.perf_counter()
    out = Path(a.salida)
    out.mkdir(parents=True, exist_ok=True)
    reg = Registry(out / "registro.csv")
    d = C.cargar()
    B = 49 if a.rapido else B_BOOT
    cells_periodos = ["completo", "P3"] if a.rapido else list(C.PERIODOS)
    mercados = MERCADOS[:1] if a.rapido else MERCADOS
    dq_cache = {}
    for merc, med in MERCADOS:
        dq_cache[(merc, med)] = C.preparar(d, merc, med, "ipc", "trimestral")[0]

    coef_rows, attr_rows, vif_rows, bel_rows, joh_rows, ort_rows, comp_rows = [], [], [], [], [], [], []
    gr_rows, lp_rows, bma_rows, pen_rows, oos_rows, muestras = [], [], [], [], [], []
    modelo_n = 0
    for merc, med in mercados:
        for transf in TRANSF:
            for per in cells_periodos:
                cel = preparar_celda(d, dq_cache, merc, med, transf, per)
                sel, D, nd = cel["sel"], cel["D"], cel.get("dummies", [])
                clave = f"{merc}|{transf}|{per}"
                muestras.append({"mercado": merc, "transformacion": transf, "periodo": per, "n": cel["n"],
                                 "ini": cel.get("span", ("", ""))[0], "fin": cel.get("span", ("", ""))[1],
                                 "familias_incluidas": ";".join(sel), "variables": ";".join(sel.values()),
                                 "familias_excluidas": ";".join(f"{k}: {v}" for k, v in cel["motivos"].items()),
                                 "ficticias_en_OLS": ";".join(nd), "variacion_acumulada_pp": cel.get("variacion", np.nan)})
                if not sel:
                    continue
                y, Xr = descomponer(D, sel, d, nd)
                k = len(sel)
                dep_lab = etiqueta_dep(transf, med)
                nota_base = f"n={cel['n']} ({cel['span'][0]}-{cel['span'][1]}); ficticias partializadas: {','.join(nd) or 'ninguna'}"
                # ---------------- OLS (EWC) -> coeficientes
                cols = list(sel.values())
                A = np.column_stack([np.ones(cel["n"]), D[cols].values] + ([d.loc[D.index, nd].values] if nd else []))
                yy = D["dep"].values
                ew = C.ewc_ols(yy, A)
                res = sm.OLS(yy, A).fit()
                vifd = dominancia.colinealidad(D[cols].values, list(sel.keys())) if k > 1 else None
                vifmax = float(vifd["vif"].max()) if vifd else 1.0
                diag = diagnosticos_ols(res, A)
                nombres = ["const"] + list(sel.values()) + nd
                fams = [None] + list(sel.keys()) + [None] * len(nd)
                modelo_n += 1
                mid = f"M6_ols_{merc}_{transf}_{per}"
                tcrit = stats.t.ppf(0.975, ew["q"])
                for j, nm in enumerate(nombres):
                    sx = A[:, j].std(ddof=0) if j else np.nan
                    ok_el = nm in C.POR_CLAVE and C.POR_CLAVE[nm].tipo == "ln"
                    coef_rows.append({
                        "modelo_id": mid, "modulo": "M6", "familia_modelo": "ols_familias", "mercado": merc, "ambito": "nacional", "periodo": per,
                        "dependiente": dep_lab, "transformacion": transf, "medida_precio": med, "variable": nm, "factor": fams[j],
                        "beta": ew["beta"][j], "ee": ew["se"][j], "tipo_ee": "EWC", "t": ew["t"][j], "p": ew["p"][j],
                        "ic95_lo": ew["beta"][j] - tcrit * ew["se"][j], "ic95_hi": ew["beta"][j] + tcrit * ew["se"][j],
                        "beta_std": ew["beta"][j] * sx / yy.std(ddof=0) if j else np.nan, "elasticidad": ew["beta"][j] if (ok_el and j) else np.nan,
                        "n": cel["n"], "r2": res.rsquared, "r2_adj": res.rsquared_adj, "aic": res.aic, "bic": res.bic,
                        **diag, "vif_max": vifmax, "capa": "C4", "script": SCRIPT})
                reg.log("M6", mid, f"{dep_lab} ~ {' + '.join(nombres[1:])}", D.index[0], D.index[-1], cel["n"], res.rsquared_adj, res.aic, res.bic,
                        notas=f"OLS EWC; {merc};{transf};{per}; capa C4")
                # ---------------- VIF y Belsley (sobre las variables de las familias)
                if k > 1:
                    for fam, v in zip(sel.keys(), vifd["vif"].values):
                        vif_rows.append({"mercado": merc, "transformacion": transf, "periodo": per, "factor": fam, "variable": sel[fam],
                                         "vif": float(v), "ci_max": vifd["ci_max"], "n": cel["n"],
                                         "dependencias_belsley": "; ".join(f"CI={ci:.1f}: {'+'.join(vs)}" for ci, vs in vifd["dependencias"])})
                    bt = vifd["belsley"].copy()
                    bt.insert(0, "n", cel["n"])
                    bt.insert(0, "periodo", per)
                    bt.insert(0, "transformacion", transf)
                    bt.insert(0, "mercado", merc)
                    bel_rows.append(bt)
                # ---------------- dominancia / Johnson / ortogonalizacion
                if k >= 2:
                    s90 = dominancia.shapley_r2(Xr, y)
                    phi, r2, dr = boot_phi(Xr, y, B, BLOQUE, SEED)
                    var = cel["variacion"]
                    metodo = "dominancia" if transf == "interanual" else "dominancia_trimestral"
                    prin = "si" if transf == "interanual" else "no"
                    var_lab = f"{transf}_ipc_{med}"
                    escala = cel["nW"] / 4.0 if transf == "interanual" else float(cel["nW"])
                    b68 = banda_basica(phi, dr, 0.32, 0.0, 1.0)
                    b90 = banda_basica(phi, dr, 0.10, 0.0, 1.0)
                    r2d = dr.sum(1)
                    rb68 = banda_basica(np.array([1 - r2]), (1 - r2d)[:, None], 0.32)
                    rb90 = banda_basica(np.array([1 - r2]), (1 - r2d)[:, None], 0.10)
                    for j, fam in enumerate(sel):
                        v_ = sel[fam]
                        ew_b = ew["beta"][1 + j]
                        dx = float(D[v_].mean()) - (float(cel["Xall"][v_].mean()) if C.POR_CLAVE[v_].tipo == "nivel" else 0.0)
                        parc = float(ew_b * dx * escala)
                        lo68, hi68 = sorted((b68[0][j] * var, b68[1][j] * var))
                        lo90, hi90 = sorted((b90[0][j] * var, b90[1][j] * var))
                        attr_rows.append({"metodo": metodo, "mercado": merc, "ambito": "nacional", "periodo": per, "factor": fam,
                                          "contribucion_pp": phi[j] * var, "pct_total": 100 * phi[j], "b68_lo": lo68, "b68_hi": hi68,
                                          "b90_lo": lo90, "b90_hi": hi90, "capa": "C4",
                                          "notas": (f"{ASOC}; contribucion_pp = cuota LMG x R2 x variacion acumulada ({var:.1f} pp log x100, suma de la tasa "
                                                    f"trimestral real en la ventana comun R0: {cel['nW']} trimestres); R2={r2:.3f}; variable={v_}; bandas: bootstrap "
                                                    f"por bloques (B={B}, bloque {BLOQUE}) «basico» centrado (2*est - q) del LMG absoluto; {transf}; {nota_base}"),
                                          "cuota_lmg": float(s90.loc[fam, "share"]), "r2": r2, "delta_y_pp": var,
                                          "signo_parcial": int(np.sign(parc)), "contrib_parcial_pp": parc,
                                          "orientacion": ORIENTACION.get(v_, 1), "variante": var_lab, "principal": prin})
                    attr_rows.append({"metodo": metodo, "mercado": merc, "ambito": "nacional", "periodo": per, "factor": "residuo",
                                      "contribucion_pp": (1 - r2) * var, "pct_total": 100 * (1 - r2),
                                      "b68_lo": min(rb68[0][0] * var, rb68[1][0] * var), "b68_hi": max(rb68[0][0] * var, rb68[1][0] * var),
                                      "b90_lo": min(rb90[0][0] * var, rb90[1][0] * var), "b90_hi": max(rb90[0][0] * var, rb90[1][0] * var), "capa": "C4",
                                      "notas": f"{ASOC}; residuo = (1 - R2) x variacion; R2={r2:.3f}; nunca entra en el ranking (R1); {transf}; {nota_base}",
                                      "cuota_lmg": np.nan, "r2": r2, "delta_y_pp": var, "signo_parcial": 0, "contrib_parcial_pp": np.nan,
                                      "orientacion": 1, "variante": var_lab, "principal": prin})
                    for fam, why in cel["motivos"].items():
                        attr_rows.append({"metodo": metodo, "mercado": merc, "ambito": "nacional", "periodo": per, "factor": fam,
                                          "contribucion_pp": np.nan, "pct_total": np.nan, "b68_lo": np.nan, "b68_hi": np.nan, "b90_lo": np.nan,
                                          "b90_hi": np.nan, "capa": "C4", "notas": f"EXCLUIDA: {why}; {transf}",
                                          "cuota_lmg": np.nan, "r2": np.nan, "delta_y_pp": np.nan, "signo_parcial": 0, "contrib_parcial_pp": np.nan,
                                          "orientacion": 1, "variante": var_lab, "principal": prin})
                    jw = dominancia.johnson_rw(Xr, y)
                    for fam in sel:
                        joh_rows.append({"mercado": merc, "transformacion": transf, "periodo": per, "factor": fam, "variable": sel[fam],
                                         "peso_johnson": float(jw.loc[fam, "peso"]), "cuota_johnson": float(jw.loc[fam, "share"]),
                                         "cuota_dominancia": float(s90.loc[fam, "share"]), "r2": r2})
                    ort = dominancia.ortogonalizacion_secuencial(Xr, y, max_vars=7)["resumen"]
                    for fam in sel:
                        ort_rows.append({"mercado": merc, "transformacion": transf, "periodo": per, "factor": fam, "variable": sel[fam],
                                         "n_ordenes": math.factorial(k),
                                         "r2_inc_media": ort.loc[fam, "media"], "r2_inc_min": ort.loc[fam, "minimo"], "r2_inc_max": ort.loc[fam, "maximo"],
                                         "r2_primero": ort.loc[fam, "primero"], "r2_ultimo": ort.loc[fam, "ultimo"],
                                         "rango_minmax": ort.loc[fam, "maximo"] - ort.loc[fam, "minimo"], "r2_total": r2})
                    reg.log("M6", f"M6_dom_{merc}_{transf}_{per}", f"shapley_r2({dep_lab} ~ {'+'.join(sel.values())})", D.index[0], D.index[-1],
                            cel["n"], np.nan, np.nan, np.nan, notas=f"R2={r2:.4f};B={B}")
                    # ---------------- indice compuesto (sensibilidad)
                    for fam in ("credito_tipos", "empleo_renta"):
                        if fam not in sel:
                            continue
                        cand = [c for c, ipo in C.candidatas_viables(fam, cel["dep"], cel["Xall"], cel["ip"], cel["win"])
                                if cel["Xall"].loc[D.index, c].notna().all()]
                        if len(cand) < 2:
                            continue
                        M = cel["Xall"].loc[D.index, cand]
                        Zc = (M - M.mean()) / M.std(ddof=0)
                        U, S_, Vt = np.linalg.svd(Zc.values, full_matrices=False)
                        pc = U[:, 0] * S_[0]
                        if np.corrcoef(pc, Zc[sel[fam]])[0, 1] < 0:
                            pc = -pc
                        Xc = D[list(sel.values())].copy()
                        Xc[sel[fam]] = pc
                        if nd:
                            yc, Xcr = residualizar(D["dep"].values, Xc.values, d.loc[D.index, nd].values.astype(float))
                        else:
                            yc, Xcr = D["dep"].values, Xc.values
                        Xcr = pd.DataFrame(Xcr, index=D.index, columns=list(sel.keys()))
                        sc = dominancia.shapley_r2(Xcr, yc)
                        vc = dominancia.colinealidad(Xcr.values, list(sel.keys()))
                        comp_rows.append({"mercado": merc, "transformacion": transf, "periodo": per, "factor": fam, "variables_pc1": ";".join(cand),
                                          "var_explicada_pc1": float(S_[0] ** 2 / (S_ ** 2).sum()), "cuota_base": float(s90.loc[fam, "share"]),
                                          "cuota_compuesto": float(sc.loc[fam, "share"]), "r2_base": r2, "r2_compuesto": float(sc.attrs["r2"]),
                                          "vif_max_base": vifmax, "vif_max_compuesto": float(vc["vif"].max()), "n": cel["n"], "capa": "C4"})
                # ---------------- BMA
                kmax = cel["n"] - 1 - len(nd) - C.GL_MIN
                filas, w, pip, pm = bma_celda(y, Xr, kmax)
                for i, ((S, bco, bic, r2m), wi) in enumerate(zip(filas, w)):
                    reg.log("M6", f"M6_bma_{merc}_{transf}_{per}_{i:03d}", f"{dep_lab} ~ {'+'.join(list(sel.keys())[s] for s in S) or '1'}",
                            D.index[0], D.index[-1], cel["n"], np.nan, np.nan, float(bic), notas=f"BMA peso={wi:.4g}")
                for j, fam in enumerate(sel):
                    bma_rows.append({"mercado": merc, "transformacion": transf, "periodo": per, "factor": fam, "variable": sel[fam], "pip": pip[j],
                                     "beta_std_post_media": pm[j], "beta_std_post_media_condicional": pm[j] / pip[j] if pip[j] > 1e-9 else np.nan,
                                     "n_modelos": len(filas), "k_max": min(kmax, k), "n": cel["n"], "capa": "C4"})
                # ---------------- penalizados (solo celdas con n suficiente)
                if cel["n"] >= 24 and k >= 2:
                    ts = max(3, cel["n"] // 8)
                    rg, en, sd = penalizados(y, Xr.values, n_splits=3, test_size=ts, gap=4)
                    for j, fam in enumerate(sel):
                        pen_rows.append({"mercado": merc, "transformacion": transf, "periodo": per, "factor": fam, "variable": sel[fam],
                                         "ridge_beta_std": rg.coef_[j] / y.std(ddof=0) * 1.0, "ridge_alpha": rg.alpha_,
                                         "enet_beta_std": en.coef_[j] / y.std(ddof=0), "enet_alpha": en.alpha_, "enet_l1_ratio": en.l1_ratio_,
                                         "n": cel["n"], "cv": f"TimeSeriesSplit(3, test_size={ts}, gap=4)", "capa": "C4"})
                        reg.log("M6", f"M6_pen_{merc}_{transf}_{per}_{fam}", f"ridge/enet {dep_lab} ~ {sel[fam]}", D.index[0], D.index[-1], cel["n"],
                                np.nan, np.nan, np.nan, coef_interes=float(rg.coef_[j] / y.std(ddof=0)), notas="coef ridge tipificado")
                # ---------------- fuera de muestra (solo trimestral, completo)
                if transf == "trimestral" and per == "completo":
                    _, _, _, niv = C.preparar(d, merc, med, "ipc", "trimestral")
                    Zs = cel["Xall"][list(sel.values())]
                    try:
                        errs, idx_t, n_oos = oos_bloques(cel["dep"], Zs, niv)
                        base = errs["ar4"]
                        fam_p = {}
                        for m in ("ecm_v1", "ols_factores", "ridge", "enet"):
                            fam_p[(m, "ar4")] = dm_test(errs[m], errs["ar4"], h=1)["p"]
                            if m != "ecm_v1":
                                fam_p[(m, "ecm_v1")] = dm_test(errs[m], errs["ecm_v1"], h=1)["p"]
                        hol = holm({f"{m}|{b}": p for (m, b), p in fam_p.items()})
                        for m in errs:
                            r = {"mercado": merc, "periodo": per, "modelo": m, "n_oos": len(errs[m]), "n_muestra": n_oos,
                                 "rmse": float(np.sqrt(np.mean(errs[m] ** 2))), "rmse_ar4": float(np.sqrt(np.mean(base ** 2))),
                                 "rmse_ecm_v1": float(np.sqrt(np.mean(errs["ecm_v1"] ** 2)))}
                            for b in ("ar4", "ecm_v1"):
                                if m == b:
                                    continue
                                dm = dm_test(errs[m], errs[b], h=1)
                                r[f"dm_vs_{b}"] = dm["DM"]
                                r[f"p_dm_vs_{b}"] = dm["p"]
                                r[f"p_holm_vs_{b}"] = hol.get(f"{m}|{b}", np.nan)
                            r["nota"] = ("ajuste condicional en bloques con embargo (5 bloques de 8 trimestres, gap=4); los modelos de factores usan los "
                                         "factores contemporaneos: no es un pronostico puro; ECM v1 reconstruido de forma aproximada (ocupados, costes, renta)")
                            oos_rows.append(r)
                            reg.log("M6", f"M6_oos_{merc}_{m}", f"oos {m}", C.PERIODOS["completo"][0], C.PERIODOS["completo"][1], len(errs[m]),
                                    np.nan, np.nan, np.nan, rmse_oos=r["rmse"], notas="OOS bloques+embargo")
                    except Exception as ex:  # noqa: BLE001
                        oos_rows.append({"mercado": merc, "periodo": per, "modelo": "FALLIDA", "nota": f"{type(ex).__name__}: {ex}"})
                # ---------------- Granger por bloques y LP-OLS (EWC): solo trimestral; predictivos, NO causales
                if transf == "trimestral" and per in ("completo", "P1", "P2", "P3"):
                    lnp = d[C.NOMINAL[(merc, med)]] - d["ln_ipc_general"]
                    yl = 100 * lnp
                    g = cel["dep"]
                    p_lag = 4 if per == "completo" else 2
                    for fam, v in sel.items():
                        xs = cel["Xall"][v]
                        win = cel["win"]
                        df_ = pd.DataFrame({"y": g, "x": xs}).loc[win]
                        for dire, (a_, b_) in {"x->dep": ("y", "x"), "dep->x": ("x", "y")}.items():
                            Z = pd.DataFrame({"a": df_[a_]})
                            for L in range(1, p_lag + 1):
                                Z[f"a{L}"] = df_[a_].shift(L)
                                Z[f"b{L}"] = df_[b_].shift(L)
                            Z = Z.dropna()
                            kk = 2 * p_lag + 1
                            if len(Z) - kk < 8:
                                gr_rows.append({"mercado": merc, "periodo": per, "factor": fam, "variable": v, "sentido": dire, "p_lags": p_lag,
                                                "n": len(Z), "F": np.nan, "p": np.nan, "nota": "n insuficiente"})
                                continue
                            Xg = sm.add_constant(Z.drop(columns="a"))
                            rg_ = sm.OLS(Z["a"], Xg).fit(cov_type="HC1")
                            R = np.zeros((p_lag, Xg.shape[1]))
                            for L in range(1, p_lag + 1):
                                R[L - 1, list(Xg.columns).index(f"b{L}")] = 1
                            ft = rg_.f_test(R)
                            gr_rows.append({"mercado": merc, "periodo": per, "factor": fam, "variable": v, "sentido": dire, "p_lags": p_lag,
                                            "n": len(Z), "F": float(np.squeeze(ft.fvalue)), "p": float(ft.pvalue), "nota": "predictivo, NO causal"})
                            reg.log("M6", f"M6_granger_{merc}_{per}_{fam}_{dire}", f"Granger {dire} {v}", Z.index[0], Z.index[-1], len(Z),
                                    np.nan, np.nan, np.nan, p_interes=float(ft.pvalue), notas="Granger (HC1); predictivo")
                        # LP-OLS con EWC, h=4-8, respuesta acumulada del nivel (log x100) a 1 pp de crecimiento trimestral del factor
                        sub = pd.DataFrame({"yl": yl, "g": g, "x": xs}).loc[win]
                        ctrl = np.column_stack([sub["g"].shift(1), sub["g"].shift(2), sub["x"].shift(1), sub["x"].shift(2)])
                        try:
                            r = lp.lp_agregado(sub["yl"].values, sub["x"].values, controles=ctrl, hs=(4, 8), rezagos=0, acumulado=True, ewc=True)
                            rr = r.iloc[0]
                            q = max(int(np.floor(0.4 * rr["n"] ** (2 / 3))), 2)
                            tt = rr["beta"] / rr["se"]
                            if rr["n"] - 6 < 10:
                                raise ValueError(f"n={int(rr['n'])} insuficiente")
                            lp_rows.append({"mercado": merc, "periodo": per, "factor": fam, "variable": v, "horizonte": "4-8", "beta": rr["beta"],
                                            "ee": rr["se"], "ic95_lo": rr["lo"], "ic95_hi": rr["hi"], "p": float(2 * stats.t.sf(abs(tt), q)),
                                            "n": int(rr["n"]), "capa": "C4",
                                            "nota": "LP-OLS EWC (cobertura 0,78-0,84 en F3): bandas aproximadas; asociacion dinamica, NO causal"})
                            reg.log("M6", f"M6_lp_{merc}_{per}_{fam}", f"LP-OLS EWC h=4-8 {v}", sub.index[0], sub.index[-1], int(rr["n"]),
                                    np.nan, np.nan, np.nan, coef_interes=float(rr["beta"]), p_interes=float(2 * stats.t.sf(abs(tt), q)), notas="LP EWC; C4")
                        except Exception as ex:  # noqa: BLE001
                            lp_rows.append({"mercado": merc, "periodo": per, "factor": fam, "variable": v, "horizonte": "4-8", "beta": np.nan,
                                            "n": np.nan, "capa": "C4", "nota": f"FALLIDA: {type(ex).__name__}: {str(ex)[:80]}"})
                print(f"[M6] {clave} n={cel['n']} k={k} ({hhmm(t0)})", flush=True)

    # --------------------------------------------------------------- ajustes BH y escritura
    coef = pd.DataFrame(coef_rows)
    if len(coef):
        coef["p_ajustado"] = C.bh(coef["p"].values)   # J21: BH sobre TODOS los p (constante y ficticias incluidas)
        coef["metodo_ajuste"] = np.where(coef["p"].notna(), "BH", "")
        # cruce con el multiverso M7 si existe (por mercado, periodo, factor)
        rm = RAIZ / "output" / "v8" / "M7" / "resumen_multiverso.csv"
        if rm.exists() and not a.rapido:
            mv = pd.read_csv(rm)
            mv = mv[mv["variable"] == "TODAS"][["mercado", "periodo", "factor", "n_multiverso", "pct_mismo_signo", "pct_sig_bh", "cumple_multiverso"]]
            coef = coef.merge(mv, on=["mercado", "periodo", "factor"], how="left")
        for c_ in ("n_multiverso", "pct_mismo_signo", "pct_sig_bh", "cumple_multiverso"):
            if c_ not in coef:
                coef[c_] = np.nan
        for c_ in ("coint_p", "vel_ajuste", "semivida", "f1_etapa", "ar_lo", "ar_hi", "cumple_regla_m0", "destacado", "motivo_destacado"):
            coef[c_] = np.nan
    ORD = ["modelo_id", "modulo", "familia_modelo", "mercado", "ambito", "periodo", "dependiente", "transformacion", "medida_precio", "variable", "factor",
           "beta", "ee", "tipo_ee", "t", "p", "p_ajustado", "metodo_ajuste", "ic95_lo", "ic95_hi", "beta_std", "elasticidad", "n", "r2", "r2_adj", "aic",
           "bic", "vel_ajuste", "semivida", "coint_p", "bg_p", "bp_p", "jb_p", "reset_p", "cusum_estable", "vif_max", "f1_etapa", "ar_lo", "ar_hi", "capa",
           "n_multiverso", "pct_mismo_signo", "pct_sig_bh", "cumple_regla_m0", "cumple_multiverso", "destacado", "motivo_destacado", "script"]
    if len(coef):
        coef = coef[ORD]
    coef.to_csv(out / "coeficientes.csv", index=False)
    atr = pd.DataFrame(attr_rows)
    extras = ["cuota_lmg", "r2", "delta_y_pp", "signo_parcial", "contrib_parcial_pp", "orientacion"]
    atr = atr[[c for c in atr.columns if c not in extras + ["variante", "principal"]] + extras + ["variante", "principal"]]
    atr.to_csv(out / "atribucion.csv", index=False)
    voto = voto_dominancia(atr)
    voto.to_csv(out / "voto_dominancia.csv", index=False)
    pd.DataFrame(vif_rows).to_csv(out / "colinealidad.csv", index=False)
    (pd.concat(bel_rows) if bel_rows else pd.DataFrame()).to_csv(out / "belsley.csv", index=False)
    pd.DataFrame(joh_rows).to_csv(out / "pesos_johnson.csv", index=False)
    pd.DataFrame(ort_rows).to_csv(out / "ortogonalizacion.csv", index=False)
    pd.DataFrame(comp_rows).to_csv(out / "indice_compuesto.csv", index=False)
    gr = pd.DataFrame(gr_rows)
    if len(gr):
        gr["p_bh"] = np.nan
        for dire in gr["sentido"].unique():
            m = (gr["sentido"] == dire) & gr["p"].notna()
            gr.loc[m, "p_bh"] = C.bh(gr.loc[m, "p"].values)
        gr["capa"] = "C4"
        gr["p_ajustado"] = gr["p_bh"]
        gr["metodo_ajuste"] = np.where(gr["p"].notna(), "BH", "")
    gr.to_csv(out / "granger.csv", index=False)
    lpd = pd.DataFrame(lp_rows)
    if len(lpd):
        lpd["p_bh"] = np.nan
        m = lpd["p"].notna()
        lpd.loc[m, "p_bh"] = C.bh(lpd.loc[m, "p"].values)
        lpd["p_ajustado"] = lpd["p_bh"]
        lpd["metodo_ajuste"] = np.where(lpd["p"].notna(), "BH", "")
    lpd.to_csv(out / "lp_agregado.csv", index=False)
    pd.DataFrame(bma_rows).to_csv(out / "bma.csv", index=False)
    pd.DataFrame(pen_rows).to_csv(out / "penalizados.csv", index=False)
    oos = pd.DataFrame(oos_rows)
    oos.to_csv(out / "fuera_muestra.csv", index=False)
    pd.DataFrame(muestras).to_csv(out / "muestras.csv", index=False)
    reg.flush()
    escribir_resultado(out, a, atr, coef, oos, gr, lpd, pd.DataFrame(bma_rows), pd.DataFrame(vif_rows), pd.DataFrame(ort_rows), pd.DataFrame(muestras),
                       time.perf_counter() - t0, len(reg.rows))
    print(f"[M6] fin en {hhmm(t0)}; registro={len(reg.rows)} filas", flush=True)
    return out


def escribir_resultado(out, a, atr, coef, oos, gr, lpd, bma, vif, ort, mue, seg, nreg):
    est = {}
    if len(atr):
        base = atr[(atr["metodo"] == "dominancia") & atr["pct_total"].notna() & (atr["factor"] != "residuo")]
        for (merc, per), g in base.groupby(["mercado", "periodo"]):
            g = g.sort_values("pct_total", ascending=False)
            top = g.iloc[0]
            seg2 = g.iloc[1] if len(g) > 1 else None
            est[f"{merc}|{per}"] = {"factor_mayor_cuota": top["factor"], "cuota_pct": round(float(top["pct_total"]), 1),
                                    "b90_contribucion_pp": [round(float(top["b90_lo"]), 2), round(float(top["b90_hi"]), 2)],
                                    "segundo": (seg2["factor"] if seg2 is not None else None),
                                    "cuota_segundo_pct": (round(float(seg2["pct_total"]), 1) if seg2 is not None else None),
                                    "bandas_se_solapan_con_el_segundo": bool(seg2 is not None and top["b90_lo"] <= seg2["b90_hi"] and seg2["b90_lo"] <= top["b90_hi"])}
    fb = atr[atr["pct_total"].notna() & (atr["factor"] != "residuo")]
    fuera68 = int(((fb["contribucion_pp"] < fb["b68_lo"] - 1e-9) | (fb["contribucion_pp"] > fb["b68_hi"] + 1e-9)).sum())
    fuera90 = int(((fb["contribucion_pp"] < fb["b90_lo"] - 1e-9) | (fb["contribucion_pp"] > fb["b90_hi"] + 1e-9)).sum())
    bandas_info = {"n_puntos": int(len(fb)), "fuera_b68": fuera68, "fuera_b90": fuera90,
                                 "metodo": "bootstrap por bloques «basico» centrado (2*est - q) del LMG absoluto (J16); antes percentil: 22 de 128 fuera de b68"}
    fm = {"modelo": None, "rmse": None, "dm_vs_ar4": None}
    if len(oos) and "rmse" in oos:
        o = oos[(oos["mercado"] == "compra") & (oos["modelo"].isin(["ols_factores", "ridge", "enet", "ecm_v1"]))]
        if len(o):
            mj = o.sort_values("rmse").iloc[0]
            fm = {"modelo": f"{mj['modelo']} (compra, trimestral, completo)", "rmse": float(mj["rmse"]), "rmse_ar4": float(mj["rmse_ar4"]),
                  "dm_vs_ar4": {"DM_HLN": float(mj.get("dm_vs_ar4", np.nan)), "p": float(mj.get("p_dm_vs_ar4", np.nan)),
                                "p_holm": float(mj.get("p_holm_vs_ar4", np.nan))}}
    j = {"rama": "M6", "pregunta": "Peso relativo de los factores en el crecimiento del precio real de compra y del alquiler real (nacional), "
         "colinealidad y robustez de la atribucion al orden/forma de las variables",
         "capa": "C4", "datos": "data/processed/v8/nacional_q_v8.csv (una variable por familia; ver muestras.csv)",
         "N": {"min": int(mue["n"].min()), "max": int(mue["n"].max())} if len(mue) else None,
         "metodo": "VIF y Belsley; dominancia LMG/Shapley del R2 con bootstrap por bloques (B=%d, bloque 4); Johnson; ortogonalizacion en todos los ordenes; "
                   "PC1; Granger y LP-OLS EWC (C4); BMA (BIC); ridge/enet con TimeSeriesSplit y embargo; OLS EWC por periodo" % (49 if a.rapido else B_BOOT),
         "estimacion": est,
         "ic95": "bandas b68/b90 de la contribucion (cuota LMG x R2 x variacion) por bootstrap por bloques «basico» en atribucion.csv; IC95 de OLS (EWC, t(q)) en coeficientes.csv",
         "p_ajustado": {"metodo": "BH (q=0,10)", "coeficientes_BH_min": float(coef["p_ajustado"].min()) if len(coef) and coef["p_ajustado"].notna().any() else None,
                        "granger_BH_min": float(gr["p_bh"].min()) if len(gr) and "p_bh" in gr and gr["p_bh"].notna().any() else None,
                        "lp_BH_min": float(lpd["p_bh"].min()) if len(lpd) and "p_bh" in lpd and lpd["p_bh"].notna().any() else None},
         "nivel_evidencia": "EXPLORATORIO (asociacion; C4). Sin lenguaje causal: la dominancia descompone el R2, Granger es predictivo y las LP-OLS no estan identificadas",
         "diagnosticos": {"vif_max": float(vif["vif"].max()) if len(vif) else None, "n_celdas": int(len(mue)),
                          "n_celdas_con_dominancia": int(ort[["mercado", "transformacion", "periodo"]].drop_duplicates().shape[0]) if len(ort) else 0,
                          "bandas_dominancia": bandas_info, "p4_impreciso": "P4 (9 trimestres): solo 3 familias por GL; declarado impreciso", "filas_registro": nreg},
         "fuera_muestra": fm,
         "notas": ["contribucion_pp = cuota LMG x R2 x variacion acumulada (pp log x100, ventana comun R0; P5 = 2022T3-2026T1); fila `residuo` = (1-R2) x variacion; "
                   "signo_parcial = signo de beta_f x dx_f (tasas: dx = media de la tasa del periodo; tipo real en nivel: media del periodo menos media historica), "
                   "contrib_parcial_pp = beta_f x dx_f x (nW/4 interanual; nW trimestral); voto de la dominancia en voto_dominancia.csv (R2).",
                   "Ficticia EPA 2021 = impulso (4 trimestres 2021T1-T4 en tasas interanuales; 2021T1 en trimestrales), J1/J17.",
                   "Las cuotas de dominancia describen la division del R2 entre variables colineales; no son efectos.",
                   "Granger y LP-OLS (EWC) son C4; las bandas de LP-OLS tienen cobertura 0,78-0,84 en F3.",
                   "Interpoladas excluidas de la muestra principal; familias sin datos suficientes excluidas y anotadas en muestras.csv.",
                   "El ECM v1 se reconstruye de forma aproximada (ocupados, costes, renta, dy_{t-1}); no es el script original."],
         }
    (out / "tiempos.json").write_text(json.dumps({"segundos": round(seg, 1)}))
    (out / "resultado.json").write_text(json.dumps(j, ensure_ascii=False, indent=2, default=str))
    L = ["# M6 - colinealidad y peso relativo (capa C4: asociacion)", "",
         "Ecuacion del crecimiento nacional (log x 100) con una variable por familia; precio real de compra (valor tasado) y alquiler real (IPC alquiler). "
         "La dominancia (LMG/Shapley) reparte el R2 y NO es una atribucion causal.", "",
         "## Mayor cuota de R2 por mercado y periodo (interanual, bandas b90 de la contribucion en pp)", "",
         "| mercado | periodo | factor | cuota LMG x R2 % | b90 contribucion pp | segundo (cuota %) | bandas solapadas |", "|---|---|---|---|---|---|---|"]
    for k_, v in est.items():
        m_, p_ = k_.split("|")
        L.append(f"| {m_} | {p_} | {v['factor_mayor_cuota']} | {v['cuota_pct']} | {v['b90_contribucion_pp'][0]} a {v['b90_contribucion_pp'][1]} | "
                 f"{v['segundo']} ({v['cuota_segundo_pct']}) | {'si' if v['bandas_se_solapan_con_el_segundo'] else 'no'} |")
    L += ["", f"VIF maximo observado: {resultado_num(vif['vif'].max()) if len(vif) else 'n/d'}. P4 (9 trimestres) se declara impreciso (solo 3 familias por GL).",
          "Colinealidad: ver colinealidad.csv y belsley.csv; ortogonalizacion en todos los ordenes (rango min-max) en ortogonalizacion.csv; PC1 en indice_compuesto.csv.",
          "Granger (predictivo, no causal) en granger.csv; LP-OLS EWC h=4-8 (C4) en lp_agregado.csv; BMA en bma.csv; ridge/enet en penalizados.csv.",
          f"Fuera de muestra (compra, trimestral, completo; bloques con embargo): {json.dumps(fm, ensure_ascii=False, default=str)}.",
          "Reglas: sin lenguaje causal; interpoladas fuera de la muestra principal; familias sin cobertura excluidas (muestras.csv)."]
    (out / "resumen.md").write_text("\n".join(L) + "\n")


def voto_dominancia(atr):
    """R2 (revision F4): vota el factor de mayor cuota LMG cuya contribucion parcial tenga el signo de la variacion de P_Y; si ninguno, abstiene.
    Solo la dominancia interanual principal; P1-P5. Tipos orientados x-1: el signo del producto beta*dx no depende de la orientacion."""
    filas = []
    base = atr[(atr["metodo"] == "dominancia") & (atr["factor"] != "residuo") & atr["pct_total"].notna()]
    for merc in ("compra", "alquiler"):
        for per in ("P1", "P2", "P3", "P4", "P5"):
            g = base[(base["mercado"] == merc) & (base["periodo"] == per)].sort_values("cuota_lmg", ascending=False)
            if g.empty:
                filas.append({"mercado": merc, "periodo": per, "factor_votado": "abstiene", "cuota_lmg": np.nan, "signo_delta_y": np.nan,
                              "delta_y_pp": np.nan, "r2": np.nan, "n_factores": 0, "ranking_cuota": "", "impreciso": per == "P4" or (merc == "alquiler" and per == "P1"),
                              "nota": "sin datos o sin dominancia en la celda"})
                continue
            sy = int(np.sign(g["delta_y_pp"].iloc[0]))
            ok = g[g["signo_parcial"] == sy]
            top = ok.iloc[0] if len(ok) else None
            filas.append({"mercado": merc, "periodo": per, "factor_votado": (top["factor"] if top is not None else "abstiene"),
                          "cuota_lmg": (float(top["cuota_lmg"]) if top is not None else np.nan), "signo_delta_y": sy,
                          "delta_y_pp": float(g["delta_y_pp"].iloc[0]), "r2": float(g["r2"].iloc[0]), "n_factores": int(len(g)),
                          "ranking_cuota": " > ".join(f"{r.factor}({r.cuota_lmg:.2f};{'+' if r.signo_parcial > 0 else '-'})" for r in g.itertuples()),
                          "impreciso": per == "P4", "nota": ("el de mayor cuota tiene signo contrario: vota el siguiente" if top is not None and top["factor"] != g["factor"].iloc[0]
                                                            else ("ningun factor con el signo de delta_y" if top is None else ""))})
    return pd.DataFrame(filas)


def resultado_num(x):
    return f"{float(x):.1f}"


if __name__ == "__main__":
    main()
