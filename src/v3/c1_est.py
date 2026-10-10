"""C1: estimadores (FE de sección + año×municipio, MCO/2SLS), inferencia por clúster, WCB (Webb), Conley,
permutaciones, Oster, Cinelli-Hazlett, Rotemberg. Sin red; semillas explícitas."""
import numpy as np
import pandas as pd
from scipy import spatial, stats

SEED = 20261010
WEBB = np.array([-np.sqrt(1.5), -1.0, -np.sqrt(0.5), np.sqrt(0.5), 1.0, np.sqrt(1.5)])


def _codes(s):
    return pd.factorize(pd.Series(s).astype(str))[0]


def absorb(M, groups, w=None, tol=1e-10, maxit=100):
    """Residuos de M (n×k) tras absorber efectos fijos (proyecciones alternas ponderadas)."""
    M = np.asarray(M, float).copy()
    if not groups:
        return M
    w = np.ones(len(M)) if w is None else np.asarray(w, float)
    info = [(g, g.max() + 1, np.bincount(g, w, g.max() + 1)) for g in groups]
    for _ in range(maxit):
        cambio = 0.0
        for g, n, sw in info:
            m = np.column_stack([np.bincount(g, w * M[:, j], n) for j in range(M.shape[1])]) / sw[:, None]
            M -= m[g]
            cambio = max(cambio, np.abs(m).max())
        if cambio < tol or len(groups) == 1:
            break
    return M


def diferencias(d, cols):
    """Primeras diferencias por sección (panel ordenado por codigo, anio); descarta el primer año."""
    d = d.sort_values(["codigo", "anio"]).copy()
    for c in cols:
        d["d_" + c] = d.groupby("codigo")[c].diff()
    return d.dropna(subset=["d_" + c for c in cols]).reset_index(drop=True)


def _sandwich(xh, e, cl, D):
    S = np.bincount(cl, xh * e, cl.max() + 1)
    return float((S ** 2).sum() / D ** 2), S


def fit(d, x, y="lnalq", z=None, fe="ym", fd=False, w=None, ctrl=None, keep=False):
    """Un regresor de interés x (MCO si z es None; 2SLS con instrumentos z=[...]).
    FE: 'ym' = sección + año×municipio; 'y' = sección + año (con fd=True no hay FE de sección).
    EE por clúster de distrito (CR1), t(G-1)."""
    if fd:
        cols = [y, x] + (list(z) if z else []) + (list(ctrl) if ctrl else [])
        d = diferencias(d, [c for c in cols if c in d.columns])
        y, x = "d_" + y, "d_" + x
        z = ["d_" + c for c in z] if z else None
    grp = []
    if not fd:
        grp.append(_codes(d.codigo))
    grp.append(_codes(d.muni.astype(str) + "_" + d.anio.astype(str)) if fe == "ym" else _codes(d.anio))
    kabs = grp[-1].max() + (0 if fe == "ym" else 0)
    cols = [y, x] + (list(z) if z else []) + (list(ctrl) if ctrl else [])
    wv = None if w is None else np.asarray(w, float)
    M = absorb(d[cols].values, grp, wv)
    if wv is not None:
        M = M * np.sqrt(wv)[:, None]
    nz = len(z) if z else 0
    nc = len(ctrl) if ctrl else 0
    yt, xt = M[:, 0], M[:, 1]
    Zt = M[:, 2:2 + nz] if nz else xt[:, None]
    if nc:
        C = M[:, 2 + nz:]
        P = np.linalg.pinv(C)
        yt, xt = yt - C @ (P @ yt), xt - C @ (P @ xt)
        Zt = Zt - C @ (P @ Zt)
    cl = _codes(d.distrito)
    G = cl.max() + 1
    pi = np.linalg.lstsq(Zt, xt, rcond=None)[0]
    xh = Zt @ pi
    D = float(xh @ xt)
    b = float(xh @ yt) / D
    e = yt - b * xt
    v, S = _sandwich(xh, e, cl, D)
    n = len(yt)
    v *= G / (G - 1) * (n - 1) / max(n - 1 - kabs - nc, 1)
    se = float(np.sqrt(v))
    tc = stats.t.ppf(0.975, G - 1)
    # F de primera etapa (cluster) del instrumento excluido
    F = np.nan
    if nz:
        ex = xt - 0.0
        pc = np.linalg.lstsq(Zt, ex, rcond=None)[0]
        r1 = ex - Zt @ pc
        bread = np.linalg.inv(Zt.T @ Zt)
        Sc = np.column_stack([np.bincount(cl, Zt[:, j] * r1, G) for j in range(Zt.shape[1])])
        V1 = bread @ (Sc.T @ Sc) @ bread * G / (G - 1)
        F = float(pc @ np.linalg.solve(V1, pc))
    out = {"b": b, "se": se, "lo": b - tc * se, "hi": b + tc * se, "p": float(2 * stats.t.sf(abs(b / se), G - 1)),
           "n": n, "G": int(G), "F": F, "kabs": int(kabs + nc),
           "sd_x": float(xt.std()), "r2w": float(1 - (e ** 2).sum() / (yt ** 2).sum())}
    if keep:
        out.update(yt=yt, xt=xt, Zt=Zt, xh=xh, e=e, cl=cl, D=D, d=d)
    return out


def wcb(yt, xt, xh, cl, reps=999, seed=SEED, peso="webb"):
    """Wild cluster bootstrap (restringido, nulo β=0) con pesos de Webb; p simétrica y valor crítico |t*|."""
    G = cl.max() + 1
    D = float(xh @ xt)
    Sze = np.bincount(cl, xh * yt, G)
    Szx = np.bincount(cl, xh * xt, G)
    rng = np.random.default_rng(seed)
    W = rng.choice(WEBB, size=(G, reps)) if peso == "webb" else rng.choice([-1.0, 1.0], size=(G, reps))
    b = (W.T @ Sze) / D
    r = W * Sze[:, None] - b[None, :] * Szx[:, None]
    t_star = np.abs(b / np.sqrt((r ** 2).sum(0) / D ** 2 * G / (G - 1)))
    b0 = (xh @ yt) / D
    e0 = yt - b0 * xt
    S0 = np.bincount(cl, xh * e0, G)
    t0 = abs(b0) / np.sqrt((S0 ** 2).sum() / D ** 2 * G / (G - 1))
    return {"p": float((1 + (t_star >= t0).sum()) / (reps + 1)), "crit": float(np.quantile(t_star, 0.95)),
            "reps": reps}


def conley(res, xy, radio=1000.0):
    """EE de Conley (núcleo Bartlett, radio en m, entre centroides de sección); la correlación serial dentro de
    la sección entra por la suma de scores de la sección. xy: DataFrame codigo,x,y. No lleva corrección G/(G-1)."""
    d = res["d"]
    sc = pd.Series(res["xh"] * res["e"]).groupby(d.codigo.values).sum()
    c = xy.set_index("codigo").reindex(sc.index)
    ok = c.x.notna().values
    s = sc.values
    meat = float((s ** 2).sum())
    pts = c.loc[ok, ["x", "y"]].values
    tree = spatial.cKDTree(pts)
    pares = tree.query_pairs(radio, output_type="ndarray")
    if len(pares):
        dist = np.linalg.norm(pts[pares[:, 0]] - pts[pares[:, 1]], axis=1)
        si = s[ok]
        meat += 2 * float(((1 - dist / radio) * si[pares[:, 0]] * si[pares[:, 1]]).sum())
    se = float(np.sqrt(max(meat, 0)) / abs(res["D"]))
    return {"se": se, "p": float(2 * stats.norm.sf(abs(res["b"] / se))), "pares": int(len(pares)),
            "sin_coord": int((~ok).sum())}


def permutacion(res_base, d, xcol, reps=999, seed=SEED, instr=False):
    """Placebo de tratamiento: permuta la trayectoria (4 años) de VUT entre secciones DENTRO del municipio
    (999). Si instr=True permuta el instrumento (xcol) y deja x. Devuelve fracción con |t|>1.96 (tamaño),
    p de aleatorización del coeficiente real y la media del placebo. Solo FE 'ym' sin pesos, panel balanceado."""
    d = d.sort_values(["codigo", "anio"]).reset_index(drop=True)
    ns = d.codigo.nunique()
    T = 4
    mun = _codes(d.muni.values[::T])
    path = d[xcol].values.reshape(ns, T)
    cl_s = _codes(d.distrito.values[::T])
    yt, xt = res_base["yt"], res_base["xt"]
    cl = np.repeat(cl_s, T)
    G = cl.max() + 1
    my = pd.Series(mun).values
    # centrado: x̃ = x − media sección − media muni-año + media muni (válido con muni constante por bloques)
    msz = np.bincount(mun, minlength=mun.max() + 1)
    rng = np.random.default_rng(seed)
    bs, ts = [], []
    xt_iv = xt
    for _ in range(reps):
        order = np.lexsort((rng.random(ns), my))
        P = np.empty_like(path)
        P[np.argsort(my, kind="stable")] = path[order]          # permutación dentro de cada bloque municipal
        sm = P.mean(1, keepdims=True)
        mt = np.vstack([np.bincount(mun, P[:, t], len(msz)) for t in range(T)]).T / msz[:, None]
        mm = mt.mean(1, keepdims=True)
        Xt = (P - sm - mt[mun] + mm[mun]).reshape(-1)
        xh = Xt
        xx = Xt if not instr else xt_iv
        D = float(xh @ xx)
        b = float(xh @ yt) / D
        e = yt - b * xx
        S = np.bincount(cl, xh * e, G)
        se = np.sqrt((S ** 2).sum() / D ** 2 * G / (G - 1))
        bs.append(b)
        ts.append(b / se)
    bs, ts = np.array(bs), np.array(ts)
    return {"size5": float((np.abs(ts) > 1.96).mean()), "mean": float(bs.mean()), "sd": float(bs.std()),
            "p_rand": float((1 + (np.abs(bs) >= abs(res_base["b"])).sum()) / (reps + 1)), "reps": reps}


def oster_rv(d, x, y, ctrl_cols, fe="ym", z=None, rmax_f=1.3):
    """δ de Oster (R_max = 1,3·R̃, R² intra-FE) y valor de robustez RV_q=1 de Cinelli-Hazlett (t de clúster,
    dof=n−k) frente al R² parcial del mejor covariable (máx. entre Y~c|D,resto y D~c|resto).
    Controles = covariables censales × dummies de año (3 por covariable)."""
    d = d.copy()
    cc = []
    for c in ctrl_cols:
        s = (d[c] - d[c].mean()) / d[c].std()
        for a in (2022, 2023, 2024):
            nm = f"{c}_x{a}"
            d[nm] = s * (d.anio == a)
            cc.append(nm)
    d = d.dropna(subset=cc)
    corto = fit(d, x, y, z=z, fe=fe)
    largo = fit(d, x, y, z=z, fe=fe, ctrl=cc, keep=True)
    r_c, r_l = corto["r2w"], largo["r2w"]
    rmax = min(rmax_f * r_l, 1.0)
    den = (corto["b"] - largo["b"]) * (rmax - r_l)
    delta = float(largo["b"] * (r_l - r_c) / den) if abs(den) > 1e-15 else np.inf
    dof = largo["n"] - largo["kabs"] - 1
    t = largo["b"] / largo["se"]
    f = abs(t) / np.sqrt(dof)
    rv = float(0.5 * (np.sqrt(f ** 4 + 4 * f ** 2) - f ** 2))
    # R² parciales de cada covariable (grupo de 3 dummies de año)
    best_y = best_d = 0.0
    det = {}
    for c in ctrl_cols:
        otros = [k for k in cc if not k.startswith(c + "_x")]
        mine = [k for k in cc if k.startswith(c + "_x")]
        rr = fit(d, x, y, z=z, fe=fe, ctrl=otros, keep=True)
        # Y ~ c | D, resto: R² parcial de las dummies en la regresión de y sobre x, resto y c
        M = absorb(d[[y, x] + otros + mine].values, [_codes(d.codigo), _codes(d.muni.astype(str) + "_"
                                                                              + d.anio.astype(str))
                                                     if fe == "ym" else _codes(d.anio)])
        Ymat, Xm = M[:, 0], M[:, 1:]
        k0 = 1 + len(otros)
        A0 = Xm[:, :k0]
        r0 = Ymat - A0 @ np.linalg.lstsq(A0, Ymat, rcond=None)[0]
        r1 = Ymat - Xm @ np.linalg.lstsq(Xm, Ymat, rcond=None)[0]
        ry = 1 - (r1 ** 2).sum() / (r0 ** 2).sum()
        # D ~ c | resto (sin D)
        B0 = Xm[:, 1:k0]
        xr = Xm[:, 0]
        q0 = xr - B0 @ np.linalg.lstsq(B0, xr, rcond=None)[0] if B0.shape[1] else xr
        B1 = np.column_stack([B0, Xm[:, k0:]]) if B0.shape[1] else Xm[:, k0:]
        q1 = xr - B1 @ np.linalg.lstsq(B1, xr, rcond=None)[0]
        rd = 1 - (q1 ** 2).sum() / (q0 ** 2).sum()
        det[c] = {"r2_y": float(ry), "r2_d": float(rd)}
        best_y, best_d = max(best_y, ry), max(best_d, rd)
        del rr
    return {"b_corto": corto["b"], "b_largo": largo["b"], "se_largo": largo["se"], "r2w_corto": r_c,
            "r2w_largo": r_l, "delta_oster": delta, "t": float(t), "RV_q1": rv, "r2_mejor_cov_y": float(best_y),
            "r2_mejor_cov_d": float(best_d), "mejor_cov": max(det, key=lambda k: max(det[k].values())),
            "detalle": det}


def shift(p, base="2108", nivel="muni", rel=True):
    """Instrumento shift-share leave-one-out: z_it = cuota inicial (VUT/100 viviendas en la oleada base) ×
    crecimiento del VUT del resto (sin la propia sección) del municipio ('muni') o de la provincia ('prov').
    rel=True: crecimiento relativo (V_t/V_0 − 1); rel=False: variación por 100 viviendas. Devuelve copia con z."""
    s = p.copy()
    col = "muni" if nivel == "muni" else "prov"
    s["share0"] = 100 * s["vut_" + base] / s.viv
    t = s.groupby([col, "anio"]).agg(V=("vut", "sum"), H=("viv", "sum")).reset_index()
    b0 = s.drop_duplicates("codigo").groupby(col).agg(V0=("vut_" + base, "sum"))
    s = s.merge(t, on=[col, "anio"]).join(b0, on=col)
    s["Vr"] = s.V - s.vut
    s["Hr"] = s.H - s.viv
    s["Vr0"] = s.V0 - s["vut_" + base]
    if rel:
        g = s.Vr / s.Vr0.where(s.Vr0 > 0) - 1
    else:
        g = 100 * s.Vr / s.Hr - 100 * s.Vr0 / s.Hr
    s["z"] = s.share0 * g
    s = s.replace([np.inf, -np.inf], np.nan).dropna(subset=["z"])
    ok = s.groupby("codigo").anio.nunique()
    return s[s.codigo.isin(ok[ok == 4].index)].sort_values(["codigo", "anio"]).reset_index(drop=True)


def rotemberg(d, x, y, fe="ym"):
    """Pesos de Rotemberg (GPSS): un instrumento por ciudad (z·1{muni=k}); α_k = π_k·(Z_k'x)/Σ, β_k = Z_k'y/Z_k'x."""
    munis = sorted(d.muni.unique())
    cols = []
    d = d.copy()
    for m in munis:
        d["z_" + m] = d.z * (d.muni == m)
        cols.append("z_" + m)
    grp = [_codes(d.codigo), _codes(d.muni.astype(str) + "_" + d.anio.astype(str)) if fe == "ym" else _codes(d.anio)]
    M = absorb(d[[y, x] + cols].values, grp)
    yt, xt, Z = M[:, 0], M[:, 1], M[:, 2:]
    pi = np.linalg.lstsq(Z, xt, rcond=None)[0]
    zx = Z.T @ xt
    alpha = pi * zx / (pi * zx).sum()
    beta = (Z.T @ yt) / zx
    return pd.DataFrame({"ciudad": munis, "alpha": alpha, "beta_k": beta, "F_k_cuota": zx})
