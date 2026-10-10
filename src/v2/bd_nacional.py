"""BD - descomposición histórica del precio REAL nacional con el ECM v1 real (EXPLORATORIO).

ECM v1 real (output/f2/ecuacion_real.csv; réplica en v2_common.ecm_v1_nacional):
  LP : ln_ipv_real = c + b·[ln_ocupados, tipo_hip_real, ln_permisos_l4, ln_costes_real] + dummies q2-q4 (+ DOLS ±2)
  CP : Δy_t = c + a·ect_{t-1} + q2..q4 + b1·Δln_ocup_{t-1} + b2·Δtipo_hip_{t-1} + b3·Δln_renta_real_t
             + b4·Δy_{t-4} + b5·Δln_credito_nuevo_t + e_t
Reestimado con los datos de ENTRENAMIENTO (≤2024Q2) vía v2_common.load.
(A) Identidad de largo plazo: Δy_P = b·Δx_P + Δ(estacional)_P + Δ(desequilibrio)_P.
(B) Corto plazo: Σ_t Δy_t = Σ_k coef_k Σ_t x_kt + Σ_t e_t (exacta).
IC95: bootstrap de residuos por bloques (bloque 4) con regresores fijos, B reducido por --smoke.
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import bd_lib as L  # noqa: E402

import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402

PERIODOS = L.PERIODOS
XS = ["ln_ocupados", "tipo_hip_real", "ln_permisos_l4", "ln_costes_real"]
ETQ = {"ln_ocupados": "empleo (ocupados)", "tipo_hip_real": "tipo hipotecario real",
       "ln_permisos_l4": "permisos (t-4)", "ln_costes_real": "costes de construcción reales"}


def datos():
    n = L.vc.load("nacional_q_v2")
    n["trimestre"] = n["trimestre"].astype(str)
    n = n[n["trimestre"] <= L.vc.Q_TRAIN_FIN].sort_values("trimestre").reset_index(drop=True)
    n["y"] = n["ln_ipv"] - n["ln_deflactor"]
    n["ln_permisos_l4"] = n["ln_permisos"].shift(4)
    n["ln_costes_real"] = n["ln_costes"] - n["ln_deflactor"]
    n["q2"], n["q3"], n["q4"] = [(n["trimestre"].str[-1] == k).astype(float) for k in "234"]
    return n


def dols(n, k=2):
    """DOLS ±k con dummies trimestrales. Devuelve coef, fitted, residuos, índice de la muestra."""
    D = pd.DataFrame(index=n.index)
    for x in XS:
        dx = n[x].diff()
        for j in range(-k, k + 1):
            D[f"D_{x}_{j}"] = dx.shift(-j)
    X = pd.concat([n[XS], n[["q2", "q3", "q4"]], D], axis=1)
    X.insert(0, "const", 1.0)
    ok = X.notna().all(axis=1) & n["y"].notna()
    b = np.linalg.lstsq(X[ok].values, n.loc[ok, "y"].values, rcond=None)[0]
    par = pd.Series(b, index=X.columns)
    fit = X[ok].values @ b
    return par, X, ok, n.loc[ok, "y"].values - fit


def construir_cp(n, par):
    s = n.copy()
    s["ect"] = s["y"] - par["const"] - (s[XS] * par[XS].values).sum(1) - (s[["q2", "q3", "q4"]] * par[["q2", "q3", "q4"]].values).sum(1)
    s["dy"] = s["y"].diff()
    s["ect_l1"] = s["ect"].shift(1)
    s["d_ocup_l1"] = s["ln_ocupados"].diff().shift(1)
    s["d_tipo_l1"] = s["tipo_hip"].diff().shift(1)
    s["d_renta"] = s["ln_renta_hog_real"].diff()
    s["dy_l4"] = s["dy"].shift(4)
    s["d_cred"] = s["ln_credito_nuevo"].diff()
    return s


CP_X = ["ect_l1", "q2", "q3", "q4", "d_ocup_l1", "d_tipo_l1", "d_renta", "dy_l4", "d_cred"]
CP_ETQ = {"ect_l1": "desequilibrio (ect t-1)", "d_ocup_l1": "empleo (Δ ocupados t-1)",
          "d_tipo_l1": "tipos (Δ tipo hip. t-1)", "d_renta": "renta real (Δ)", "dy_l4": "inercia (Δy t-4)",
          "d_cred": "crédito nuevo (Δ)", "const_estac": "constante + estacionales", "residuo": "residuo"}


def _blocks(rng, e, L_=4):
    n = len(e)
    nb = int(np.ceil(n / L_))
    st = rng.integers(0, n - L_ + 1, nb)
    return np.concatenate([e[s:s + L_] for s in st])[:n]


def ejecutar(B, seed, reg):
    n = datos()
    par, Xd, okd, ed = dols(n)
    s = construir_cp(n, par)
    cols = ["dy"] + CP_X + ["trimestre"]
    sc = s.dropna(subset=["dy"] + CP_X).copy()
    Xcp = np.column_stack([np.ones(len(sc)), sc[CP_X].values])
    ycp = sc["dy"].values
    bcp = np.linalg.lstsq(Xcp, ycp, rcond=None)[0]
    ecp = ycp - Xcp @ bcp
    reg.log("BD", "nacional_ECMv1_real_LP_DOLS", "y=ln_ipv-ln_deflactor ~ " + "+".join(XS) + " + q2-q4 + DOLS±2",
            n.loc[okd, "trimestre"].min(), n.loc[okd, "trimestre"].max(), int(okd.sum()), np.nan, np.nan, np.nan,
            np.nan, par["ln_ocupados"], np.nan, "EXPLORATORIO; réplica de v1 con datos de entrenamiento")
    reg.log("BD", "nacional_ECMv1_real_CP", "Δy ~ " + "+".join(CP_X), sc["trimestre"].min(), sc["trimestre"].max(),
            len(sc), np.nan, np.nan, np.nan, np.nan, bcp[1], np.nan,
            f"EXPLORATORIO; bootstrap de residuos por bloques (4) B={B} seed={seed}")
    tq = sc["trimestre"].values
    per = np.array([L.periodo_de(q) or "" for q in tq])
    # ---------- (B) corto plazo
    def cp_contrib(b, e):
        out = {}
        for p in L.PNAMES:
            m = per == p
            if not m.any():
                continue
            xs = Xcp[m]
            for j, nm in enumerate(["const"] + CP_X):
                pass
            c = {}
            c["desequilibrio (ect t-1)"] = b[1] * xs[:, 1].sum()
            c["constante + estacionales"] = b[0] * m.sum() + (b[2:5] * xs[:, 2:5].sum(0)).sum()
            c["empleo (Δ ocupados t-1)"] = b[5] * xs[:, 5].sum()
            c["tipos (Δ tipo hip. t-1)"] = b[6] * xs[:, 6].sum()
            c["renta real (Δ)"] = b[7] * xs[:, 7].sum()
            c["inercia (Δy t-4)"] = b[8] * xs[:, 8].sum()
            c["crédito nuevo (Δ)"] = b[9] * xs[:, 9].sum()
            c["residuo"] = e[m].sum()
            c["observado"] = ycp[m].sum()
            out[p] = {k: 100 * v for k, v in c.items()}
        return out
    pt = cp_contrib(bcp, ecp)
    rng = np.random.default_rng(seed)
    fit = Xcp @ bcp
    bs = {p: {k: [] for k in pt[p]} for p in pt}
    for _ in range(B):
        ys = fit + _blocks(rng, ecp)
        b2 = np.linalg.lstsq(Xcp, ys, rcond=None)[0]
        c2 = cp_contrib(b2, ycp - Xcp @ b2)   # residuo = dato observado - ajuste con coef. remuestreados
        for p in c2:
            for k, v in c2[p].items():
                bs[p][k].append(v)
    rows = []
    for p in pt:
        for k, v in pt[p].items():
            lo, hi = np.percentile(bs[p][k], [2.5, 97.5])
            rows.append(dict(bloque="corto_plazo_ECM", periodo=p, componente=k, contrib_pp=v, ic95_inf=lo,
                             ic95_sup=hi, pct_observado=100 * v / pt[p]["observado"], observado_pp=pt[p]["observado"],
                             n_trim=int((per == p).sum())))
    cpdf = pd.DataFrame(rows)
    # ---------- (A) identidad de largo plazo
    nn = n.set_index("trimestre")
    def lp_contrib(par_):
        out = {}
        for p, (a, b) in PERIODOS.items():
            b = min(b, L.vc.Q_TRAIN_FIN)
            i0 = list(nn.index).index(a) - 1
            i1 = list(nn.index).index(b)
            dx = nn[XS].iloc[i1] - nn[XS].iloc[i0]
            c = {ETQ[x]: 100 * par_[x] * dx[x] for x in XS}
            q0, q1 = nn[["q2", "q3", "q4"]].iloc[i0].values, nn[["q2", "q3", "q4"]].iloc[i1].values
            c["estacional (dummies)"] = 100 * float(((q1 - q0) * par_[["q2", "q3", "q4"]].values).sum())
            dy = 100 * (nn["y"].iloc[i1] - nn["y"].iloc[i0])
            c["desequilibrio (Δ ect)"] = dy - sum(c.values())
            c["observado"] = dy
            out[p] = c
        return out
    pl = lp_contrib(par)
    # bootstrap: residuos DOLS por bloques, regresores fijos -> b* -> contribuciones LP
    fitd = Xd[okd].values @ par.values
    yd = n.loc[okd, "y"].values
    bsl = {p: {k: [] for k in pl[p]} for p in pl}
    rng = np.random.default_rng(seed + 1)
    Xv = Xd[okd].values
    for _ in range(B):
        ys = fitd + _blocks(rng, ed)
        b2 = pd.Series(np.linalg.lstsq(Xv, ys, rcond=None)[0], index=Xd.columns)
        c2 = lp_contrib(b2)
        for p in c2:
            for k, v in c2[p].items():
                bsl[p][k].append(v)
    rows = []
    for p in pl:
        for k, v in pl[p].items():
            lo, hi = np.percentile(bsl[p][k], [2.5, 97.5])
            rows.append(dict(bloque="largo_plazo_identidad", periodo=p, componente=k, contrib_pp=v, ic95_inf=lo,
                             ic95_sup=hi, pct_observado=100 * v / pl[p]["observado"], observado_pp=pl[p]["observado"],
                             n_trim=np.nan))
    lpdf = pd.DataFrame(rows)
    coef = pd.DataFrame({"parametro": ["LP:" + x for x in XS] + ["CP:const"] + ["CP:" + x for x in CP_X],
                         "coef": list(par[XS]) + list(bcp)})
    return dict(cp=cpdf, lp=lpdf, coef=coef, n_lp=int(okd.sum()), n_cp=len(sc), muestra=(sc["trimestre"].min(), sc["trimestre"].max()))
