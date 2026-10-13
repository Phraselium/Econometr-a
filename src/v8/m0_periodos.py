#!/usr/bin/env python3
"""V8-F4 M0: periodos y regla de «efecto por periodo» (hipotesis.md §8, con docs/v8/desviaciones.md).

Analisis principal: ecuaciones por tramo (P1-P5 pre-registrados) del crecimiento interanual del precio real de compra
(valor tasado MIVAU) y del alquiler real (IPC) sobre representantes de las familias de factores; EE HAC. Sin busqueda.
Confirmaciones (deteccion SOLO con series nacionales de credito, tipos y actividad): Bai-Perron (bootstrap sieve-AR),
Markov switching (k por BIC; bootstrap LR informativo), umbral de Hansen (bootstrap sieve-AR). Permutacion de fechas
(2.000 conjuntos). Capa C4 siempre (asociacion); nivel «ASOCIACION ROBUSTA» solo si cumple la regla completa.
Uso: python3 src/v8/m0_periodos.py [--rapido] [--salida DIR]
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
import statsmodels.api as sm  # noqa: E402

RAIZ = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(RAIZ / "src"))
sys.path.insert(0, str(RAIZ / "src" / "v8"))
from econ_utils import Registry, dm_test  # noqa: E402
from herramientas import permutacion as perm  # noqa: E402
from herramientas import regimenes as reg  # noqa: E402

warnings.filterwarnings("ignore")
SEED = 20261010
DATOS = RAIZ / "data" / "processed" / "v8" / "nacional_q_v8.csv"
SCRIPT = "src/v8/m0_periodos.py"
PERIODOS = {"P1": ("1995Q1", "2007Q4"), "P2": ("2008Q3", "2013Q4"), "P3": ("2014Q1", "2019Q4"),
            "P4": ("2020Q2", "2022Q2"), "P5": ("2022Q3", "2026Q2")}
FIN_TRAIN = "2013Q4"
L_HAC = 4
MIN_LEN = 8

# variable -> (familia, columna origen, transformacion, nota)
BASE = {
    "d4_pob_total": ("demografia", "d4_ln_pob_total", "d4_ln*100", "interpolada (semestral->trimestral), marcada"),
    "d4_pib_vol": ("empleo_renta", "d4_ln_pib_vol_idx", "d4_ln*100", ""),
    "tipo_hip_real": ("credito_tipos", "tipo_hip_real_bde", "nivel (pp)", "tipo BdE menos inflacion interanual"),
    "d4_credito_vivienda_real": ("credito_tipos", "d4_ln_credito_stock_bde_real", "d4_ln*100", "saldo a hogares para vivienda, real"),
    "d4_terminadas": ("oferta", "d4_ln_terminadas", "d4_ln*100", "1995-2007 anual/4 (desagregacion marcada)"),
}
EXTRA = {
    "d4_hpi_ea19": ("factor_europeo", "d4_ln_hpi_ea19", "d4_ln*100", ["P2", "P3", "P4", "P5"]),
    "d4_tx_extranj": ("demanda_externa", "d4_ln_tx_extranj", "d4_ln*100", ["P2", "P3", "P4", "P5"]),
    "d4_turistas": ("turismo", "d4_ln_turistas", "d4_ln*100", ["P4", "P5"]),
}
TH_Q = {"tipo_hip_real": "tipo_hip_real_bde", "d4_credito_nuevo_real": "d4_ln_credito_nuevo_real",
        "d4_ocupados_SUSTITUTO_paro": "d4_ln_ocupados"}
DET_SERIES = {"d4_credito_vivienda_real": "d4_ln_credito_stock_bde_real", "tipo_hip_real": "tipo_hip_real_bde",
              "d4_pib_vol": "d4_ln_pib_vol_idx"}
MERCADOS = {"compra": ("d4_ln_p_tasado_real", "valor tasado MIVAU, real (IPC general)", "d4_ln_ipv_real"),
            "alquiler": ("d4_ln_ipc_alquiler_real", "IPC alquiler, real (IPC general)", None)}


# ------------------------------------------------------------------ utilidades
def md_tabla(df: pd.DataFrame, fmt: str = "{:.3f}") -> str:
    cols = [str(c) for c in df.columns]
    out = ["| " + " | ".join(cols) + " |", "|" + "|".join("---" for _ in cols) + "|"]
    for _, r in df.iterrows():
        out.append("| " + " | ".join(("" if (isinstance(v, float) and v != v) else fmt.format(v) if isinstance(v, (float, np.floating)) else str(v)) for v in r.values) + " |")
    return "\n".join(out)


def cargar() -> pd.DataFrame:
    return pd.read_csv(DATOS).set_index("trimestre")


def marco(d: pd.DataFrame) -> pd.DataFrame:
    F = pd.DataFrame(index=d.index)
    F["y_compra"] = 100 * d["d4_ln_p_tasado_real"]
    F["y_alquiler"] = 100 * d["d4_ln_ipc_alquiler_real"]
    F["y_ipv"] = 100 * d["d4_ln_ipv_real"]
    for k, (_, col, tr, *_r) in {**BASE, **EXTRA}.items():
        F[k] = d[col] if tr.startswith("nivel") else 100 * d[col]
    return F


def qpos(idx, q):
    return list(idx).index(q) if q in idx else None


def tramos_en(idx, nombres):
    """Tramos [ini, fin) en posiciones de `idx` (solo la parte del periodo dentro de la muestra)."""
    out = {}
    for P in nombres:
        a, b = PERIODOS[P]
        pos = [i for i, q in enumerate(idx) if a <= q <= b]
        if pos:
            out[P] = (pos[0], pos[-1] + 1)
    return out


def ols_hac(y, X, L=L_HAC):
    return sm.OLS(y, X).fit(cov_type="HAC", cov_kwds={"maxlags": L, "use_correction": True}, use_t=True)


def signo(b):
    return 0 if (b != b or b == 0) else (1 if b > 0 else -1)


# ------------------------------------------------------------------ estimacion por tramo
def ecuacion(F, ycol, xs, periodos):
    """Muestra comun (sin NaN) de ycol y xs; estima por tramo. Devuelve dict con la muestra, tramos y ajustes."""
    S = F[[ycol] + xs].dropna()
    X = sm.add_constant(S[xs].reset_index(drop=True))
    y = S[ycol].reset_index(drop=True)
    tr = tramos_en(list(S.index), periodos)
    fits = {}
    for P, (a, b) in tr.items():
        k = X.shape[1]
        if b - a < k + 1:
            continue
        fits[P] = ols_hac(y.iloc[a:b].values, X.iloc[a:b].values)
    return {"S": S, "X": X, "y": y, "tr": tr, "fits": fits, "xs": xs, "ycol": ycol}


def p_perm_periodo(E, var, P, n_perm, seed):
    """Permutacion de fechas con el estadistico por periodo (desviaciones.md). Devuelve (p, modo, stat_obs)."""
    tr = E["tr"]
    nombres = list(tr.keys())
    if P not in nombres or len(nombres) < 2:
        return np.nan, "no_evaluable", np.nan
    j = nombres.index(P)
    col = 1 + E["xs"].index(var)
    y, X = E["y"].values, E["X"].values

    def stat(tramos):
        bv = np.array([perm._coef_var(y, X, slice(a, b), col, "hac", L_HAC) for a, b in tramos])
        v = np.maximum(bv[:, 1], 1e-12)
        w = 1.0 / v
        m = np.arange(len(bv)) != j
        bw = (w[m] * bv[m, 0]).sum() / w[m].sum()
        vw = 1.0 / w[m].sum()
        return abs(bv[j, 0] - bw) / np.sqrt(v[j] + vw)
    try:
        r = perm.permutacion_tramos(stat, len(y), [tr[n] for n in nombres], MIN_LEN, n_perm=n_perm, seed=seed)
    except ValueError as e:
        return np.nan, f"no_evaluable:{e}", np.nan
    return r["p"], r["modo"], r["stat_obs"]


def q_global(E, var, n_perm, seed):
    tr = E["tr"]
    nombres = list(tr.keys())
    if len(nombres) < 2:
        return np.nan, np.nan
    col = 1 + E["xs"].index(var)
    f = perm.stat_Q_tramos(E["y"].values, E["X"].values, col=col, se="hac", L=L_HAC)
    try:
        r = perm.permutacion_tramos(f, len(E["y"]), [tr[n] for n in nombres], MIN_LEN, n_perm=n_perm, seed=seed)
    except ValueError:
        return np.nan, np.nan
    return r["stat_obs"], r["p"]


# ------------------------------------------------------------------ deteccion de regimenes
def serie_det(d, col):
    return (d[col] if col == "tipo_hip_real_bde" else 100 * d[col]).dropna()


def etiquetas_contiguas(idx, cortes):
    lab = np.zeros(len(idx), int)
    for c in cortes:
        lab[c:] += 1
    return pd.Series(lab, index=idx, dtype=float)


def detectar(d, B_bp, B_th, B_ms, hasta=None, desde=None, ventana="completa", fila_log=None):
    """Devuelve (filas de periodos_detectados, lista de regimenes{metodo, serie, etiquetas, detectado})."""
    filas, regs = [], []

    def recorta(s):
        if hasta:
            s = s[s.index <= hasta]
        if desde:
            s = s[s.index >= desde]
        return s
    for nom, col in DET_SERIES.items():
        y = recorta(serie_det(d, col))
        # --- Bai-Perron (desplazamiento de media), sieve-AR
        if len(y) >= 30:
            r = reg.bai_perron(y.values, None, max_cortes=4, trim=0.15, B=B_bp, seed=SEED, boot="sieve")
            m = r["m_udmax"]
            cortes = list(r["cortes"][m]) if m > 0 else []
            fechas = [y.index[c] for c in cortes]
            det = m > 0
            filas.append({"metodo": "bai_perron", "particion": ventana, "serie": nom, "observable_umbral": "", "detectado": det,
                          "n_regimenes": m + 1 if det else 1, "corte_o_regimen": ";".join(fechas) if det else "sin_ruptura",
                          "fechas": f"{y.index[0]}..{y.index[-1]}", "ic": "no disponible (la herramienta no calcula IC de fechas)",
                          "p": r["p_UDmax"], "notas": f"UDmax={r['UDmax']:.2f}, cv95 boot={r['cv95_UDmax_boot']:.2f}; m por BIC={r['m_bic']}; potencia baja con series persistentes (Y7)"})
            regs.append({"metodo": "BP", "serie": nom, "detectado": det, "etiquetas": etiquetas_contiguas(list(y.index), cortes) if det else None,
                         "ventana": ventana})
            if fila_log:
                fila_log(f"BP_{ventana}_{nom}", y, r["p_UDmax"], f"m_udmax={m}")
        # --- Markov switching (media y varianza), k por BIC
        if len(y) >= 30:
            try:
                fits = {kk: reg.ms_fit(y.values, kk, search_reps=3, seed=SEED) for kk in (2, 3)}
                bic = {kk: fits[kk]["bic"] for kk in fits}
                bic[1] = float(-2 * np.sum(__import__("scipy.stats", fromlist=["norm"]).norm.logpdf(y.values, y.mean(), y.std())) + 2 * np.log(len(y)))
                kb = min(bic, key=bic.get)
                p_lr = np.nan
                if B_ms > 0 and ventana == "completa":
                    try:
                        p_lr = reg.ms_contraste_regimenes(y.values, 1, 2, B=B_ms, search_reps=2, seed=SEED)["p"]
                    except Exception:
                        p_lr = np.nan
                det = kb >= 2
                et = None
                par = ""
                if det:
                    f = fits[kb]
                    et = pd.Series(np.argmax(f["prob_suavizada"], axis=1).astype(float), index=y.index)
                    mus = [f["params"].get(f"const[{i}]", np.nan) for i in range(kb)]
                    # ordena regimenes por media (etiqueta 0 = media mas baja)
                    orden = np.argsort(mus)
                    et = et.map({int(o): i for i, o in enumerate(orden)})
                    par = "; ".join(f"R{i}: mu={mus[o]:.2f}, dur={f['duraciones'][o]:.1f}" for i, o in enumerate(orden))
                filas.append({"metodo": "markov_switching", "particion": ventana, "serie": nom, "observable_umbral": "", "detectado": det,
                              "n_regimenes": kb, "corte_o_regimen": par if det else "1 regimen (BIC)",
                              "fechas": f"{y.index[0]}..{y.index[-1]}", "ic": "no aplica", "p": p_lr,
                              "notas": f"BIC k=1/2/3: {bic[1]:.1f}/{bic[2]:.1f}/{bic[3]:.1f}; p = bootstrap LR 1 vs 2 INFORMATIVO (potencia 0,40 en F3)"})
                regs.append({"metodo": "MS", "serie": nom, "detectado": det, "etiquetas": et, "ventana": ventana,
                             "fit": fits[kb] if det else None})
            except Exception as e:  # noqa: BLE001
                filas.append({"metodo": "markov_switching", "particion": ventana, "serie": nom, "observable_umbral": "", "detectado": False,
                              "n_regimenes": np.nan, "corte_o_regimen": "fallo", "fechas": "", "ic": "", "p": np.nan,
                              "notas": f"fallo de convergencia: {type(e).__name__}"})
        # --- umbral de Hansen: AR(1) con umbral en una observable pre-registrada (rezagada)
        for qn, qcol in TH_Q.items():
            q = recorta(serie_det(d, qcol))
            Z = pd.concat([y.rename("y"), y.shift(1).rename("y1"), q.shift(1).rename("q1")], axis=1).dropna()
            if len(Z) < 30:
                continue
            Xv = np.column_stack([np.ones(len(Z)), Z["y1"].values])
            try:
                r = reg.umbral_hansen(Z["y"].values, Xv, Z["q1"].values, trim=0.15, B=B_th, seed=SEED, boot="sieve")
            except Exception as e:  # noqa: BLE001
                filas.append({"metodo": "umbral_hansen", "particion": ventana, "serie": nom, "observable_umbral": qn, "detectado": False,
                              "n_regimenes": np.nan, "corte_o_regimen": "fallo", "fechas": "", "ic": "", "p": np.nan, "notas": f"fallo: {type(e).__name__}"})
                continue
            det = r["p_linealidad"] < 0.05
            et = pd.Series(np.where(Z["q1"].values <= r["gamma"], 0.0, 1.0), index=Z.index) if det else None
            filas.append({"metodo": "umbral_hansen", "particion": ventana, "serie": nom, "observable_umbral": qn, "detectado": det,
                          "n_regimenes": 2 if det else 1, "corte_o_regimen": f"gamma={r['gamma']:.3f} (bajo n={r['n_bajo']}, alto n={r['n_alto']})" if det else "lineal",
                          "fechas": f"{Z.index[0]}..{Z.index[-1]}", "ic": f"[{r['ic_gamma'][0]:.3f}, {r['ic_gamma'][1]:.3f}] (LR, Hansen 2000)",
                          "p": r["p_linealidad"], "notas": ("observable SUSTITUTA de la tasa de paro (no pre-registrada); " if "SUSTITUTO" in qn else "") + f"supLR={r['sup_LR']:.2f}, cv95 boot={r['cv95_boot']:.2f}; boot sieve-AR"})
            regs.append({"metodo": "UMBRAL", "serie": f"{nom}|{qn}", "detectado": det, "etiquetas": et, "ventana": ventana,
                         "gamma": r["gamma"], "qcol": qcol, "ycol": col})
    return filas, regs


def aplica_entrenamiento(d, regs_train):
    """Segunda particion: clasifica 2014-ultimo con gamma (umbral) y parametros MS estimados en 1995-2013."""
    out = []
    for r in regs_train:
        if not r["detectado"] or r["metodo"] == "BP":
            continue
        if r["metodo"] == "UMBRAL":
            q = serie_det(d, r["qcol"]).shift(1)
            q = q[q.index > FIN_TRAIN].dropna()
            et = pd.Series(np.where(q.values <= r["gamma"], 0.0, 1.0), index=q.index)
            out.append({"metodo": "UMBRAL", "serie": r["serie"], "etiquetas": et, "detectado": True, "ventana": "test"})
        else:
            col = DET_SERIES[r["serie"]]
            y = serie_det(d, col)
            y = y[y.index > FIN_TRAIN]
            f = r["fit"]
            k = f["k"]
            mus = np.array([f["params"].get(f"const[{i}]", np.nan) for i in range(k)])
            s2 = np.array([f["params"].get(f"sigma2[{i}]", f["params"].get("sigma2", np.nan)) for i in range(k)])
            orden = np.argsort(mus)
            ll = np.column_stack([-0.5 * np.log(s2[o]) - 0.5 * (y.values - mus[o]) ** 2 / s2[o] for o in orden])
            et = pd.Series(np.argmax(ll, axis=1).astype(float), index=y.index)
            out.append({"metodo": "MS", "serie": r["serie"], "etiquetas": et, "detectado": True, "ventana": "test"})
    return out


def replica_train_test(d, regs_train, regs_test_clas):
    """Filas informativas de replica: orden de medias por regimen (MS) / diferencia de medias (umbral) en test."""
    filas = []
    for r in regs_test_clas:
        if r["metodo"] == "UMBRAL":
            nom, qn = r["serie"].split("|")
            y = serie_det(d, DET_SERIES[nom])
            et = r["etiquetas"]
            ygr = y.reindex(et.index)
            a, b = ygr[et == 0].dropna(), ygr[et == 1].dropna()
            if len(a) >= MIN_LEN and len(b) >= MIN_LEN:
                dif = b.mean() - a.mean()
                tr_ = [x for x in regs_train if x["metodo"] == "UMBRAL" and x["serie"] == r["serie"]][0]
                yt = serie_det(d, DET_SERIES[nom])
                yt = yt[yt.index <= FIN_TRAIN]
                qt = serie_det(d, tr_["qcol"]).shift(1).reindex(yt.index)
                lo, hi = yt[qt <= tr_["gamma"]].dropna(), yt[qt > tr_["gamma"]].dropna()
                dif_tr = hi.mean() - lo.mean() if len(lo) and len(hi) else np.nan
                t = ols_hac(np.r_[a.values, b.values], sm.add_constant(np.r_[np.zeros(len(a)), np.ones(len(b))]))
                filas.append({"metodo": "umbral_hansen", "serie": r["serie"], "dif_media_train": dif_tr, "dif_media_test": dif,
                              "t_hac_test": float(t.tvalues[1]), "mismo_signo": bool(np.sign(dif) == np.sign(dif_tr)), "n_bajo_test": len(a), "n_alto_test": len(b)})
            else:
                filas.append({"metodo": "umbral_hansen", "serie": r["serie"], "dif_media_train": np.nan, "dif_media_test": np.nan,
                              "t_hac_test": np.nan, "mismo_signo": None, "n_bajo_test": len(a), "n_alto_test": len(b)})
        else:
            y = serie_det(d, DET_SERIES[r["serie"]])
            et = r["etiquetas"]
            ygr = y.reindex(et.index)
            medias = [ygr[et == i].mean() if (et == i).sum() >= 3 else np.nan for i in sorted(et.unique())]
            ok = all(np.diff([m for m in medias if m == m]) > 0) if sum(m == m for m in medias) >= 2 else None
            filas.append({"metodo": "markov_switching", "serie": r["serie"], "dif_media_train": np.nan, "dif_media_test": np.nan,
                          "t_hac_test": np.nan, "mismo_signo": ok, "n_bajo_test": int((et == 0).sum()), "n_alto_test": int((et != 0).sum())})
    return filas


# ------------------------------------------------------------------ confirmaciones
def signos_en_regimen(E, etiquetas, P, minimo_extra=6):
    """Signos de los coeficientes en la muestra del regimen que contiene la mayoria del periodo P (None si no evaluable)."""
    S, xs = E["S"], E["xs"]
    if etiquetas is None or P not in E["tr"]:
        return None
    a, b = E["tr"][P]
    qs = list(S.index[a:b])
    lab = etiquetas.reindex(qs).dropna()
    if len(lab) < max(3, 0.5 * len(qs)):
        return None
    m = lab.mode().iloc[0]
    mask = (etiquetas.reindex(S.index) == m).values
    if mask.sum() < len(xs) + 1 + minimo_extra:
        return None
    fit = ols_hac(E["y"].values[mask], E["X"].values[mask])
    return {v: signo(fit.params[1 + i]) for i, v in enumerate(xs)}


def confirmaciones(E, regs, P, var, ventana):
    """Por metodo (BP, MS, UMBRAL): 'si' / 'no' / 'no_evaluable' segun mayoria estricta de series evaluables."""
    sp = signo(E["fits"][P].params[1 + E["xs"].index(var)]) if P in E["fits"] else 0
    res = {}
    for met in ("BP", "MS", "UMBRAL"):
        votos = []
        for r in regs:
            if r["metodo"] != met or not r["detectado"] or r["ventana"] != ventana:
                continue
            s = signos_en_regimen(E, r["etiquetas"], P)
            if s is not None:
                votos.append(s[var] == sp and sp != 0)
        res[met] = "no_evaluable" if not votos else ("si" if sum(votos) > len(votos) / 2 else "no")
    return res


# ------------------------------------------------------------------ fuera de muestra (bloques con embargo)
def fuera_de_muestra(F, ycol, xs, K=5, embargo=4):
    S = F[[ycol] + xs].dropna()
    cols = {f"L{j}": F[ycol].shift(j).reindex(S.index) for j in range(1, 5)}
    Z = pd.concat([S, pd.DataFrame(cols)], axis=1).dropna()
    n = len(Z)
    per = pd.Series("T", index=Z.index)
    for P, (a, b) in PERIODOS.items():
        per[(Z.index >= a) & (Z.index <= b)] = P
    y = Z[ycol].values
    Lg = Z[[f"L{j}" for j in range(1, 5)]].values
    X = Z[xs].values
    Xc = (X - X.mean(0)) / X.std(0)
    D = np.column_stack([(per.values == P).astype(float) for P in PERIODOS])
    inter = np.column_stack([Xc * D[:, [i]] for i in range(5)])
    disenos = {"AR4": np.column_stack([np.ones(n), Lg]),
               "AR4+X_comun": np.column_stack([np.ones(n), Lg, Xc]),
               "AR1+X_por_periodo": np.column_stack([np.ones(n), Lg[:, :1], Xc, inter, D[:, :]])}
    cortes = np.linspace(0, n, K + 1).astype(int)
    err = {k: np.full(n, np.nan) for k in disenos}
    for i in range(K):
        a, b = cortes[i], cortes[i + 1]
        te = np.arange(a, b)
        tr = np.array([t for t in range(n) if t < a - embargo or t >= b + embargo])
        for k, M in disenos.items():
            beta = np.linalg.lstsq(M[tr], y[tr], rcond=None)[0]
            err[k][te] = y[te] - M[te] @ beta
    out = {"n": n, "bloques": K, "embargo": embargo, "muestra": f"{Z.index[0]}..{Z.index[-1]}", "rmse": {}, "dm_vs_ar4": {}}
    for k in disenos:
        out["rmse"][k] = float(np.sqrt(np.mean(err[k] ** 2)))
    for k in ("AR4+X_comun", "AR1+X_por_periodo"):
        r = dm_test(err[k], err["AR4"], h=1)
        out["dm_vs_ar4"][k] = {"DM_HLN": r["DM"], "p": r["p"], "mean_d": r["mean_d"]}
    return out


# ------------------------------------------------------------------ principal
def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--rapido", action="store_true")
    ap.add_argument("--salida", default=str(RAIZ / "output" / "v8" / "M0"))
    a = ap.parse_args(argv)
    t0 = time.time()
    rapido = a.rapido
    out = Path(a.salida)
    out.mkdir(parents=True, exist_ok=True)
    B_bp, B_th, B_ms, N_PERM = (19, 19, 0, 99) if rapido else (299, 299, 29, 2000)
    d = cargar()
    F = marco(d)
    REG = Registry(out / "registro.csv")

    def log_det(modelo_id, y, p, notas):
        REG.log("M0_deteccion", modelo_id, "deteccion de regimenes (serie nacional credito/tipos/actividad)", y.index[0], y.index[-1], len(y),
                np.nan, np.nan, np.nan, np.nan, np.nan, p, notas)

    # ---------- deteccion
    filas_det, regs = detectar(d, B_bp, B_th, B_ms, ventana="completa", fila_log=log_det)
    f_tr, regs_tr = detectar(d, max(B_bp // 2, 9), max(B_th // 2, 9), 0, hasta=FIN_TRAIN, ventana="train_1995_2013")
    f_te, regs_te = detectar(d, max(B_bp // 2, 9), max(B_th // 2, 9), 0, desde="2014Q1", ventana="test_2014_ult")
    # solo BP en test independiente interesa; umbral/MS en test se reportan igualmente como informativos
    regs_clas = aplica_entrenamiento(d, regs_tr)
    for r in regs_clas:
        r["ventana"] = "test"
    filas_rep = replica_train_test(d, regs_tr, regs_clas)
    det_df = pd.DataFrame(filas_det + f_tr + f_te)
    det_df.to_csv(out / "periodos_detectados.csv", index=False)
    pd.DataFrame(filas_rep).to_csv(out / "replica_segunda_particion.csv", index=False)
    for f in filas_det + f_tr + f_te:
        REG.log("M0_deteccion", f"{f['metodo']}|{f['particion']}|{f['serie']}|{f['observable_umbral']}", "deteccion", "", "", 0,
                np.nan, np.nan, np.nan, np.nan, np.nan, f["p"], f"detectado={f['detectado']}; {f['corte_o_regimen']}")

    # ---------- ecuaciones por tramo
    base_xs = list(BASE)
    specs = []   # (nombre, mercado, ycol, xs, periodos, vars_reportar)
    for mk, (yc, _, _) in MERCADOS.items():
        ycol = "y_" + mk
        specs.append(("base", mk, ycol, base_xs, list(PERIODOS), base_xs))
        for ev, (_, _, _, pers) in EXTRA.items():
            specs.append((f"ext_{ev}", mk, ycol, base_xs + [ev], pers, [ev]))
    filas_coef, filas_regla, filas_q = [], [], []
    ecs = {}
    qcache = {}
    for (nom, mk, ycol, xs, pers, repvars) in specs:
        E = ecuacion(F, ycol, xs, pers)
        ecs[(nom, mk)] = E
        # alternativa (IPV) para compra
        Ealt = ecuacion(F, "y_ipv", xs, pers) if mk == "compra" else None
        # confirmaciones por periodo (ventana completa y segunda particion)
        for P, fit in E["fits"].items():
            a_, b_ = E["tr"][P]
            idx = list(E["S"].index)
            X_ = E["X"].iloc[a_:b_]
            y_ = E["y"].iloc[a_:b_]
            sd_y = float(y_.std()) if len(y_) > 1 else np.nan
            ci = fit.conf_int()
            formula = f"{ycol} ~ " + " + ".join(xs)
            REG.log("M0_tramos", f"M0_{mk}_{nom}_{P}", formula, idx[a_], idx[b_ - 1], int(fit.nobs),
                    float(fit.rsquared_adj), float(fit.aic), float(fit.bic), np.nan, float(fit.params[1]), float(fit.pvalues[1]),
                    f"HAC NW({L_HAC}); gl={int(fit.df_resid)}" + ("; P4 imprecisa" if P == "P4" else ""))
            for v in repvars:
                i = 1 + xs.index(v)
                filas_coef.append({
                    "modelo_id": f"M0_{mk}_{nom}_{P}", "modulo": "M0", "familia_modelo": "ols_tramos_hac" if nom == "base" else f"ols_tramos_hac_ampliada({v})",
                    "mercado": mk, "ambito": "nacional", "periodo": P, "dependiente": ycol, "transformacion": "d4_ln*100",
                    "medida_precio": MERCADOS[mk][1], "variable": v, "beta": float(fit.params[i]), "ee": float(fit.bse[i]),
                    "tipo_ee": f"HAC-NW({L_HAC}), t({int(fit.df_resid)})", "t": float(fit.tvalues[i]), "p": float(fit.pvalues[i]),
                    "ic95_lo": float(ci[i, 0]), "ic95_hi": float(ci[i, 1]),
                    "beta_std": float(fit.params[i] * X_.iloc[:, i].std() / sd_y) if sd_y == sd_y and sd_y > 0 else np.nan,
                    "n": int(fit.nobs), "r2": float(fit.rsquared), "r2_adj": float(fit.rsquared_adj), "aic": float(fit.aic), "bic": float(fit.bic),
                    "capa": "C4", "_spec": nom})
                # --- regla
                sp = signo(fit.params[i])
                pp, modo, st = p_perm_periodo(E, v, P, N_PERM, SEED)
                conf = confirmaciones(E, regs, P, v, "completa")
                n_conf = sum(c == "si" for c in conf.values())
                # alternativa
                if Ealt is not None and P in Ealt["fits"] and Ealt["fits"][P].df_resid >= 1:
                    sa = signo(Ealt["fits"][P].params[1 + xs.index(v)])
                    alt = "si" if (sa == sp and sp != 0) else "no"
                else:
                    sa, alt = 0, "no_evaluable"
                # segunda particion (solo periodos de test)
                if P in ("P3", "P4", "P5"):
                    cs = confirmaciones(E, regs_clas, P, v, "test")
                    vals = [c for m_, c in cs.items() if m_ in ("MS", "UMBRAL") and c != "no_evaluable"]
                    seg = "no_evaluable" if not vals else ("si" if "si" in vals else "no")
                else:
                    seg = "n/a (ventana de deteccion)"
                if alt == "no_evaluable":
                    cumple = "no_evaluable"
                else:
                    cumple = "si" if (sp != 0 and n_conf >= 1 and pp == pp and pp < 0.05 and alt == "si") else "no"
                if (nom, mk, v) not in qcache:
                    qcache[(nom, mk, v)] = q_global(E, v, N_PERM, SEED)
                q_obs, q_p = qcache[(nom, mk, v)]
                filas_regla.append({"mercado": mk, "periodo": P, "variable": v, "signo_principal": sp, "conf_BP": conf["BP"], "conf_MS": conf["MS"],
                                    "conf_umbral": conf["UMBRAL"], "n_confirmaciones": n_conf, "p_perm": pp, "modo_perm": modo, "signo_alternativa": sa if alt != "no_evaluable" else np.nan,
                                    "alternativa": "IPV" if mk == "compra" else "SERPAVI (anual): no evaluable", "alt_mismo_signo": alt,
                                    "segunda_particion": seg, "cumple": cumple, "familia": (BASE.get(v) or EXTRA.get(v))[0], "especificacion": nom,
                                    "p_Q_global_variable": q_p})
                if P == list(E["tr"])[0]:
                    filas_q.append({"mercado": mk, "especificacion": nom, "variable": v, "Q": q_obs, "p_perm_Q": q_p})
    coef = pd.DataFrame(filas_coef)
    regla = pd.DataFrame(filas_regla)
    # BH (q = 0,10) sobre todos los p de coeficientes (familia exploratoria); sin const
    from scipy.stats import false_discovery_control
    coef["p_ajustado"] = false_discovery_control(coef["p"].fillna(1).values, method="bh")
    coef["metodo_ajuste"] = "BH"
    # cumple_regla_m0 en coeficientes
    clave = regla.set_index(["mercado", "periodo", "variable", "especificacion"])["cumple"]
    coef["cumple_regla_m0"] = [clave.get((r.mercado, r.periodo, r.variable, r._spec), "") for r in coef.itertuples()]
    ORD = ["modelo_id", "modulo", "familia_modelo", "mercado", "ambito", "periodo", "dependiente", "transformacion", "medida_precio", "variable", "beta", "ee", "tipo_ee",
           "t", "p", "p_ajustado", "metodo_ajuste", "ic95_lo", "ic95_hi", "beta_std", "elasticidad", "n", "r2", "r2_adj", "aic", "bic", "vel_ajuste", "semivida",
           "coint_p", "bg_p", "bp_p", "jb_p", "reset_p", "cusum_estable", "vif_max", "f1_etapa", "ar_lo", "ar_hi", "capa", "n_multiverso", "pct_mismo_signo",
           "pct_sig_bh", "cumple_regla_m0", "cumple_multiverso", "destacado", "motivo_destacado", "script"]
    for c in ORD:
        if c not in coef:
            coef[c] = np.nan
    coef["script"] = SCRIPT
    coef[ORD].to_csv(out / "coeficientes.csv", index=False)
    regla.to_csv(out / "regla_m0.csv", index=False)
    pd.DataFrame(filas_q).to_csv(out / "heterogeneidad_Q.csv", index=False)

    # ---------- fuera de muestra
    fm = {mk: fuera_de_muestra(F, "y_" + mk, base_xs, K=5) for mk in MERCADOS}
    for mk, r in fm.items():
        for k, v in r["rmse"].items():
            REG.log("M0_oos", f"M0_oos_{mk}_{k}", k, r["muestra"].split("..")[0], r["muestra"].split("..")[1], r["n"], np.nan, np.nan, np.nan, v, np.nan,
                    r["dm_vs_ar4"].get(k, {}).get("p", np.nan), "bloques con embargo; condicional (X contemporaneo)")
    REG.flush()

    # ---------- resultado.json y resumen
    cumplen = regla[regla.cumple == "si"]
    nev = int((regla.cumple == "no_evaluable").sum())
    sig_bh = coef[coef.p_ajustado < 0.10]
    det_ok = det_df[(det_df.particion == "completa") & (det_df.detectado == True)]  # noqa: E712
    res = {
        "rama": "v8/M0", "pregunta": "¿Hay efectos por periodo (P1-P5) de las familias de factores sobre el precio real de compra y el alquiler real que cumplan la regla de §8?",
        "capa": "C4",
        "datos": f"data/processed/v8/nacional_q_v8.csv; compra {int(ecs[('base','compra')]['S'].shape[0])} trimestres ({ecs[('base','compra')]['S'].index[0]}-{ecs[('base','compra')]['S'].index[-1]}), alquiler {int(ecs[('base','alquiler')]['S'].shape[0])} ({ecs[('base','alquiler')]['S'].index[0]}-{ecs[('base','alquiler')]['S'].index[-1]})",
        "N": {"compra": int(ecs[("base", "compra")]["S"].shape[0]), "alquiler": int(ecs[("base", "alquiler")]["S"].shape[0])},
        "metodo": "OLS por tramo con EE HAC (principal); confirmaciones Bai-Perron/MS/umbral con bootstrap sieve-AR; permutacion de fechas (2.000); BH q=0,10",
        "estimacion": {"n_coeficientes": int(len(coef)), "n_efectos_cumplen_regla": int(len(cumplen)), "n_no_evaluable": nev,
                       "cumplen": cumplen[["mercado", "periodo", "variable"]].to_dict("records")},
        "ic95": "ver coeficientes.csv (ic95_lo, ic95_hi por tramo)",
        "p_ajustado": {"metodo": "BH q=0,10", "n_coef_sig_bh": int(len(sig_bh)), "de": int(len(coef))},
        "nivel_evidencia": "ASOCIACION ROBUSTA solo para los efectos que cumplen la regla; el resto EXPLORATORIO. Sin lenguaje causal.",
        "diagnosticos": {"detecciones_significativas": det_ok[["metodo", "serie", "observable_umbral", "p"]].to_dict("records"),
                         "nota_potencia": "BP 0,32-0,42 y permutacion con 5 tramos conservadora (Y7): un no rechazo no prueba ausencia; P4 (9 trimestres) imprecisa"},
        "fuera_muestra": {"modelo": "ecuacion por periodo (AR1+X por periodo) y X comun frente a AR(4), bloques con embargo (condicional, X contemporaneo)",
                          "rmse": {mk: fm[mk]["rmse"] for mk in fm}, "dm_vs_ar4": {mk: fm[mk]["dm_vs_ar4"] for mk in fm},
                          "detalle": {mk: {k: fm[mk][k] for k in ("n", "bloques", "embargo", "muestra")} for mk in fm},
                          "ecm_v1": "no evaluable en M0 (no es un modelo de prediccion); M4 contiene el ECM de largo plazo"},
        "notas": "Capa C4 siempre (asociacion). Variables: demografia=d4 poblacion (interpolada), empleo_renta=d4 PIB vol, credito_tipos=tipo real + d4 credito vivienda, oferta=d4 terminadas (1995-2007 anual/4). "
                 "Tasa de paro no disponible: sustituta d4 ocupados (exploratoria). SERPAVI nacional trimestral no existe: alquiler `no_evaluable` en la regla. Ver docs/v8/desviaciones.md.",
        "segundos": round(time.time() - t0, 1), "rapido": rapido,
    }
    (out / "resultado.json").write_text(json.dumps(res, indent=2, ensure_ascii=False, default=str))
    rb = regla[regla.especificacion == "base"][["mercado", "periodo", "variable", "signo_principal", "n_confirmaciones", "p_perm", "alt_mismo_signo", "cumple"]]
    md = [f"# M0 periodos (C4, asociación; {'RÁPIDO' if rapido else 'completo'})", "",
          f"Muestras: compra {res['N']['compra']} trimestres, alquiler {res['N']['alquiler']}. Efectos que cumplen la regla de §8: **{len(cumplen)}** de {len(regla)} evaluados; "
          f"{nev} `no_evaluable` (alquiler: SERPAVI anual; extras sin IPV). Sin lenguaje causal; C4 siempre.", "",
          "## Detecciones significativas (serie nacional de crédito, tipos o actividad)", "",
          md_tabla(det_ok[["metodo", "serie", "observable_umbral", "n_regimenes", "corte_o_regimen", "p"]]) if len(det_ok) else "Ninguna.", "",
          "## Regla por (mercado, periodo, variable) — ecuación base", "", md_tabla(rb), "",
          "## Fuera de muestra (bloques con embargo, RMSE)", "", "```", json.dumps({mk: fm[mk]["rmse"] for mk in fm}, indent=1), "```", "",
          "Límites: BP con potencia 0,32-0,42; permutación de 5 tramos conservadora; P4 tiene 9 trimestres y 3 gl (imprecisa); el signo de una confirmación no exige significación. "
          "Desviaciones: docs/v8/desviaciones.md (2026-10-13, M0)."]
    (out / "resumen.md").write_text("\n".join(md))
    print(f"M0 ok en {time.time() - t0:.0f}s; cumplen regla: {len(cumplen)}/{len(regla)}")
    return res


if __name__ == "__main__":
    main()
