"""V15-A · estimadores de diferencias en diferencias de H1/H2 (CS 2x2, SDID, PPML, control sintético, cotas de Lee).

Todo es estimación PUNTUAL: la inferencia de SDID (placebo, Webb), Honest DiD y control sintético es NO APTA
(docs/v15/validacion_montecarlo.md; DV15-A, A1). No se calcula ningún p-valor ni IC aquí.
"""
from __future__ import annotations

import numpy as np
import pandas as pd
from scipy.optimize import minimize

from pa_comun import PROC, idx_periodo, periodo_idx

CAT = ("08", "17", "25", "43")
QUARTERS = [idx_periodo(i) for i in range(periodo_idx("2022T2"), periodo_idx("2026T1") + 1)]
PRE7 = QUARTERS[:7]  # 2022T2-2023T4
G1, G4 = "2024T1", "2024T4"


def construir_panel() -> dict:
    """Paneles anchos (municipio x trimestre) de contratos y renta. Solo Cataluña, filtro de la adenda 1 (puntos 2 y 8)."""
    d = pd.read_parquet(PROC / "p6_zonas_tensionadas.parquet")
    z = d[d.variable == "zt_vigente"].groupby("territorio_codigo").periodo.min()
    t = d[(d.frecuencia == "T") & d.variable.isin(["incasol_contratos", "incasol_renta_media"])].copy()
    t = t[t.territorio_codigo.str[:2].isin(CAT) & (t.periodo >= QUARTERS[0]) & (t.periodo <= QUARTERS[-1])]
    w = t.pivot_table(index=["territorio_codigo", "periodo", "desagregacion"], columns="variable", values="valor", aggfunc="first").reset_index()
    w["imp"] = w.incasol_contratos * w.incasol_renta_media
    w["c_con_renta"] = np.where(w.incasol_renta_media.notna(), w.incasol_contratos, 0.0)
    g = w.groupby(["territorio_codigo", "periodo"]).agg(n=("incasol_contratos", "sum"), imp=("imp", "sum"), cr=("c_con_renta", "sum")).reset_index()
    g["renta"] = np.where(g.cr > 0, g.imp / g.cr.where(g.cr > 0), np.nan)
    N = g.pivot(index="territorio_codigo", columns="periodo", values="n").reindex(columns=QUARTERS)
    R = g.pivot(index="territorio_codigo", columns="periodo", values="renta").reindex(columns=QUARTERS)
    ok = N[PRE7].notna().all(axis=1) & (N[PRE7].mean(axis=1) >= 5) & (N[PRE7] > 0).all(axis=1)
    N, R = N[ok], R[ok]
    N = N.fillna(0.0)  # trimestre sin fila posterior = sin contratos (DV15-A, A3b)
    coh = z.reindex(N.index)
    coh = coh.where(coh.isin([G1, G4]), "nunca")
    # municipio con zt en otro trimestre dentro de Cataluña: no existe (comprobado); si existiera quedaria fuera
    return {"N": N, "R": np.log(R), "coh": coh}


def _dif(Y: np.ndarray, base: int, t: int, m: np.ndarray):
    """Media de Y_t - Y_base en las unidades m con ambos valores."""
    d = Y[:, t] - Y[:, base]
    d = d[m & np.isfinite(d)]
    return d.mean() if len(d) else np.nan, len(d)


def cs_celdas(Y: np.ndarray, coh: np.ndarray, qs: list, fin: str, controles: str = "todos", donantes: np.ndarray | None = None):
    """ATT(g,t) de CS para g en {2024T1, 2024T4}. `donantes`: mascara de los nunca tratados admitidos (exclusion por distancia).

    controles: 'todos' = nunca tratados + aun no tratados; 'solo_g4' = solo la cohorte 2024T4 (diseno a1, 2024T2-2024T3 de g=2024T1).
    Devuelve DataFrame g, t, att, n_tr, n_co.
    """
    q = {p: i for i, p in enumerate(qs)}
    nunca = (coh == "nunca") if donantes is None else ((coh == "nunca") & donantes)
    filas = []
    for g, inicio in ((G1, "2024T2"), (G4, G4)):
        mg = coh == g
        b = q[idx_periodo(periodo_idx(g) - 1)]
        for p in qs:
            if p < inicio or p > fin:
                continue
            t = q[p]
            if controles == "solo_g4":
                if g != G1 or p >= G4:
                    continue
                mc = coh == G4
            else:
                mc = nunca | ((coh == G4) & (g == G1) & (periodo_idx(p) < periodo_idx(G4)))
            a, ntr = _dif(Y, b, t, mg)
            c, nco = _dif(Y, b, t, mc)
            filas.append((g, p, a - c, ntr, nco))
    return pd.DataFrame(filas, columns=["g", "t", "att", "n_tr", "n_co"])


def cs_agregar(cel: pd.DataFrame) -> float:
    c = cel.dropna(subset=["att"])
    return float(np.average(c.att, weights=c.n_tr)) if len(c) else np.nan


def cs_eventos(Y, coh, qs, donantes=None) -> pd.DataFrame:
    """Coeficientes de estudio de eventos CS por cohorte y trimestre (base g-1, control: nunca tratados + aun no tratados)."""
    q = {p: i for i, p in enumerate(qs)}
    nunca = (coh == "nunca") if donantes is None else ((coh == "nunca") & donantes)
    filas = []
    for g in (G1, G4):
        mg = coh == g
        b = q[idx_periodo(periodo_idx(g) - 1)]
        for p in qs:
            t = q[p]
            if t == b:
                continue
            mc = nunca | ((coh == G4) & (g == G1) & (periodo_idx(p) < periodo_idx(G4)))
            a, ntr = _dif(Y, b, t, mg)
            c, nco = _dif(Y, b, t, mc)
            filas.append((g, p, periodo_idx(p) - periodo_idx(g), a - c, ntr, nco))
    return pd.DataFrame(filas, columns=["g", "t", "e", "coef", "n_tr", "n_co"])


def _simplex_ls(A: np.ndarray, b: np.ndarray, reg: float) -> np.ndarray:
    """min ||A w - b||^2 + reg * ||w||^2, w en el simplex (SLSQP)."""
    n = A.shape[1]
    if n == 1:
        return np.ones(1)
    AtA, Atb = A.T @ A + reg * np.eye(n), A.T @ b
    f = lambda w: w @ AtA @ w - 2 * Atb @ w
    gr = lambda w: 2 * (AtA @ w - Atb)
    r = minimize(f, np.full(n, 1 / n), jac=gr, bounds=[(0, 1)] * n, constraints=[{"type": "eq", "fun": lambda w: w.sum() - 1, "jac": lambda w: np.ones(n)}],
                 method="SLSQP", options={"maxiter": 300, "ftol": 1e-12})
    w = np.clip(r.x, 0, None)
    return w / w.sum()


def sdid(Ytr: np.ndarray, Yco: np.ndarray, pre: list, post: list, extra: list | None = None) -> dict:
    """SDID (Arkhangelsky et al. 2021). Ytr: (n_tr, T), Yco: (n_co, T) sin NaN; pre/post/extra: indices de columnas.

    Devuelve ATT sobre `post` y el efecto por periodo en `extra` (preperiodo de contraste) con los mismos pesos.
    """
    n_tr, n_co, Tpost = len(Ytr), len(Yco), len(post)
    dif = np.diff(Yco[:, pre], axis=1)
    sig = np.std(dif, ddof=1) if dif.size > 1 else 1.0
    zeta = (n_tr * Tpost) ** 0.25 * sig
    ytr = Ytr.mean(axis=0)
    Apre = Yco[:, pre]  # n_co x Tpre
    # pesos de unidad (intercepto: se centra cada serie en el tiempo)
    Ac = (Apre - Apre.mean(axis=1, keepdims=True)).T  # Tpre x n_co
    bc = ytr[pre] - ytr[pre].mean()
    omega = _simplex_ls(Ac, bc, zeta ** 2 * len(pre))
    # pesos de tiempo (centrando entre donantes)
    Bt = Yco[:, pre]
    tgt = Yco[:, post].mean(axis=1)
    Bc = (Bt - Bt.mean(axis=0, keepdims=True))
    tc = tgt - tgt.mean()
    lam = _simplex_ls(Bc, tc, (1e-6 * sig) ** 2 * n_co)
    yco = omega @ Yco  # serie del control sintetico (T,)

    def tau(cols):
        a = ytr[cols].mean() - lam @ ytr[pre]
        c = yco[cols].mean() - lam @ yco[pre]
        return float(a - c)
    out = {"att": tau(post), "omega": omega, "lambda": lam, "n_tr": n_tr, "n_co": n_co,
           "n_donantes_pesos_pos": int((omega > 1e-3).sum()), "rmse_pre": float(np.sqrt(np.mean((ytr[pre] - yco[pre] - np.mean(ytr[pre] - yco[pre])) ** 2)))}
    if extra:
        out["extra"] = {c: float((ytr[c] - lam @ ytr[pre]) - (yco[c] - lam @ yco[pre])) for c in extra}
    return out


def sdid_cohortes(Y: np.ndarray, coh: np.ndarray, qs: list, fin: str, donantes: np.ndarray | None = None, sin_datos_ok: bool = False) -> dict:
    """SDID por cohorte con los nunca tratados como donantes; agrega por numero de tratados x trimestres posteriores.

    Pesos en 2022T2-2023T2; 2023T3-2023T4 = preperiodo de contraste. Panel equilibrado: solo unidades sin NaN en 2022T2-fin.
    """
    q = {p: i for i, p in enumerate(qs)}
    pre = [q[p] for p in qs[:5]]
    contr = [q[p] for p in qs[5:7]]
    cols_ok = [q[p] for p in qs if p <= fin]
    fin_ok = np.isfinite(Y[:, cols_ok]).all(axis=1)
    don = (coh == "nunca") & fin_ok
    if donantes is not None:
        don &= donantes
    res, atts, pesos, extras = {}, [], [], []
    for g, ini in ((G1, "2024T2"), (G4, G4)):
        mg = (coh == g) & fin_ok
        post = [q[p] for p in qs if ini <= p <= fin]
        if mg.sum() == 0 or don.sum() == 0 or not post:
            continue
        r = sdid(Y[mg][:, cols_ok], Y[don][:, cols_ok], pre, post, contr)
        r["g"] = g
        res[g] = r
        atts.append(r["att"])
        pesos.append(mg.sum() * len(post))
        extras.append(np.mean(list(r["extra"].values())))
    if not res:
        return {"att": np.nan, "por_cohorte": {}, "n_donantes": int(don.sum()), "contraste": np.nan}
    return {"att": float(np.average(atts, weights=pesos)), "por_cohorte": {g: float(r["att"]) for g, r in res.items()},
            "n_tr": {g: int(r["n_tr"]) for g, r in res.items()}, "n_donantes": int(don.sum()),
            "contraste": float(np.average(extras, weights=pesos)),
            "rmse_pre": float(np.mean([r["rmse_pre"] for r in res.values()])),
            "donantes_pesos_pos": {g: r["n_donantes_pesos_pos"] for g, r in res.items()}, "_res": res}


def ppml(N: np.ndarray, coh: np.ndarray, qs: list, fin: str, donantes: np.ndarray | None = None) -> dict:
    """PPML con efectos de municipio y trimestre; efecto por cohorte (forma de Wooldridge) y agregado ponderado.

    Cohorte 2024T1: se omite su observacion de 2024T1 (resolucion del 16-3-2024); efecto desde 2024T2.
    Cohorte 2024T4: efecto desde 2024T4. Devuelve cambio porcentual 100*(exp(tau)-1).
    """
    import statsmodels.api as sm
    keep = (coh != "nunca") | (donantes if donantes is not None else np.ones(len(coh), bool))
    idx = np.where(keep)[0]
    cols = [i for i, p in enumerate(qs) if p <= fin]
    filas = []
    for u in idx:
        for c in cols:
            p = qs[c]
            if coh[u] == G1 and p == G1:
                continue
            d1 = float(coh[u] == G1 and p >= "2024T2")
            d4 = float(coh[u] == G4 and p >= G4)
            filas.append((u, c, N[u, c], d1, d4))
    df = pd.DataFrame(filas, columns=["u", "t", "y", "d1", "d4"])
    X = pd.concat([df[["d1", "d4"]], pd.get_dummies(df.u, prefix="u", drop_first=True, dtype=float), pd.get_dummies(df.t, prefix="t", drop_first=True, dtype=float)], axis=1)
    m = sm.GLM(df.y.values, X.values, family=sm.families.Poisson()).fit(maxiter=100)
    t1, t4 = float(m.params[0]), float(m.params[1])
    n1, n4 = int(df.d1.sum()), int(df.d4.sum())
    agg = (n1 * (np.exp(t1) - 1) + n4 * (np.exp(t4) - 1)) / (n1 + n4) * 100
    # TWFE simple (un solo indicador) como referencia
    X2 = X.copy()
    X2["d"] = X2.d1 + X2.d4
    X2 = X2.drop(columns=["d1", "d4"])
    X2 = X2[["d"] + [c for c in X2.columns if c != "d"]]
    m2 = sm.GLM(df.y.values, X2.values, family=sm.families.Poisson()).fit(maxiter=100)
    return {"att_pct": float(agg), "tau_g1": t1, "tau_g4": t4, "pct_g1": float(100 * (np.exp(t1) - 1)), "pct_g4": float(100 * (np.exp(t4) - 1)),
            "twfe_pct": float(100 * (np.exp(m2.params[0]) - 1)), "n_obs": len(df), "convergio": bool(m.converged)}


def sintetico_unidad(y_u: np.ndarray, Yco: np.ndarray, pre: list, post: list) -> float:
    """Control sintetico clasico (simplex, sin regularizacion): efecto medio posterior en log."""
    w = _simplex_ls(Yco[:, pre].T, y_u[pre], 0.0)
    return float(np.mean(y_u[post] - w @ Yco[:, post]))


def lee_cotas(delta_tr: np.ndarray, s_tr: np.ndarray, delta_co: np.ndarray, s_co: np.ndarray) -> dict:
    """Cotas de Lee (2009) del efecto sobre la variacion de la renta, con selección = renta observada en todos los trimestres posteriores."""
    p1, p0 = s_tr.mean(), s_co.mean()
    d1, d0 = np.sort(delta_tr[s_tr == 1]), delta_co[s_co == 1]
    m0 = d0.mean()
    if p1 > p0:
        q = (p1 - p0) / p1
        k = int(round(q * len(d1)))
        inf = d1[: len(d1) - k].mean() - m0
        sup = d1[k:].mean() - m0
    elif p1 < p0:
        d0s = np.sort(d0)
        q = (p0 - p1) / p0
        k = int(round(q * len(d0s)))
        inf = d1.mean() - d0s[k:].mean()
        sup = d1.mean() - d0s[: len(d0s) - k].mean()
    else:
        inf = sup = d1.mean() - m0
    return {"lim_inf": float(inf), "lim_sup": float(sup), "p_obs_tratados": float(p1), "p_obs_controles": float(p0), "sin_recorte": float(d1.mean() - m0)}
