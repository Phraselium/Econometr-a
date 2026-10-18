"""Replica ciega lote c (V72-GSADF-*, V71-S3-*). SEED=20261010. Determinista.

Implementacion propia a partir de las definiciones (indicador, periodo, cobertura, fuentes) y los pre-registros.
Entradas: data/processed/nacional_q.csv, data/processed/v7/panel_ccaa_q_v7.csv (panel construido desde data/raw
segun docs/v7/diccionario.md). No se abre data/sealed.
Uso: python3 -I src/v16/replica/v10_c.py
"""
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats

SEED = 20261010
RAIZ = Path(__file__).resolve().parents[3]
SALIDA = RAIZ / "output/v16/replica/v10_c"
NBOOT = 499


# ----------------------------------------------------------------------------- GSADF
def _adf_lags_bic(y, maxp=4):
    """Retardo p de la ADF (constante) en la muestra completa por BIC, mismo n efectivo."""
    dy = np.diff(y)
    best = (np.inf, 0)
    for p in range(maxp + 1):
        t0 = maxp + 1
        rows = np.arange(t0, len(y))
        Z = [np.ones(len(rows)), y[rows - 1]] + [y[rows - j] - y[rows - j - 1] for j in range(1, p + 1)]
        Z = np.column_stack(Z)
        yy = y[rows] - y[rows - 1]
        b = np.linalg.lstsq(Z, yy, rcond=None)[0]
        e = yy - Z @ b
        n = len(yy)
        bic = n * np.log(e @ e / n) + Z.shape[1] * np.log(n)
        if bic < best[0]:
            best = (bic, p)
    return best[1]


def gsadf_stat(Y, p, r0):
    """Y (B,T). Supremo de la t de ADF (constante, p retardos) sobre ventanas [s,e], e-s+1>=r0."""
    Y = np.atleast_2d(Y)
    B, T = Y.shape
    k = 2 + p
    t_idx = np.arange(p + 1, T)  # filas de regresion (indice de tiempo de la variable dependiente)
    dy = np.diff(Y, axis=1)  # dy[:, t-1] = y_t - y_{t-1}
    dep = Y[:, t_idx] - Y[:, t_idx - 1]
    Z = np.empty((B, len(t_idx), k))
    Z[:, :, 0] = 1.0
    Z[:, :, 1] = Y[:, t_idx - 1]
    for j in range(1, p + 1):
        Z[:, :, 1 + j] = Y[:, t_idx - j] - Y[:, t_idx - j - 1]
    # sumas acumuladas
    ZZ = np.einsum("bti,btj->btij", Z, Z)
    Zy = Z * dep[:, :, None]
    yy = dep ** 2
    cZZ = np.concatenate([np.zeros((B, 1, k, k)), np.cumsum(ZZ, axis=1)], axis=1)
    cZy = np.concatenate([np.zeros((B, 1, k)), np.cumsum(Zy, axis=1)], axis=1)
    cyy = np.concatenate([np.zeros((B, 1)), np.cumsum(yy, axis=1)], axis=1)
    sup = np.full(B, -np.inf)
    # fila f corresponde a t = p+1+f. Ventana [s,e] usa filas con t en [s+p+1, e] -> f en [s, e-p-1]
    for e in range(r0 - 1, T):
        starts = np.arange(0, e - r0 + 2)
        f_lo = starts
        f_hi = e - p  # exclusivo (f max = e-p-1)
        n = f_hi - f_lo
        ok = n > k + 1
        starts, f_lo, n = starts[ok], f_lo[ok], n[ok]
        if len(starts) == 0:
            continue
        S = cZZ[:, f_hi][:, None] - cZZ[:, f_lo]  # (B,ns,k,k)
        sy = cZy[:, f_hi][:, None] - cZy[:, f_lo]
        syy = cyy[:, f_hi][:, None] - cyy[:, f_lo]
        try:
            inv = np.linalg.inv(S)
        except np.linalg.LinAlgError:
            inv = np.linalg.pinv(S)
        beta = np.einsum("bsij,bsj->bsi", inv, sy)
        ssr = syy - np.einsum("bsi,bsi->bs", beta, sy)
        ssr = np.maximum(ssr, 1e-300)
        s2 = ssr / (n - k)[None, :]
        se = np.sqrt(s2 * inv[:, :, 1, 1])
        tst = beta[:, :, 1] / se
        sup = np.maximum(sup, tst.max(axis=1))
    return sup


P_ADF = 1  # retardos de la ADF (fijo): reproduce los estadisticos documentados 3,097 y 4,344 (docs/estado_proyecto)


def gsadf_test(y, seed, nboot=NBOOT, chunk=100, p_fijo=P_ADF):
    """y serie en logaritmos. Devuelve (estadistico, p, vc95, p_retardos). Bootstrap AR(p) estimado bajo raiz unitaria."""
    y = np.asarray(y, float)
    T = len(y)
    r0 = int(np.floor(T * (0.01 + 1.8 / np.sqrt(T))))
    p = _adf_lags_bic(y) if p_fijo is None else p_fijo
    stat = gsadf_stat(y[None, :], p, r0)[0]
    dy = np.diff(y)
    # AR(p) con constante en dy
    if p > 0:
        rows = np.arange(p, len(dy))
        X = np.column_stack([np.ones(len(rows))] + [dy[rows - j] for j in range(1, p + 1)])
    else:
        rows = np.arange(0, len(dy))
        X = np.ones((len(rows), 1))
    b = np.linalg.lstsq(X, dy[rows], rcond=None)[0]
    u = dy[rows] - X @ b
    u = u - u.mean()
    rng = np.random.default_rng(seed)
    out = []
    for c0 in range(0, nboot, chunk):
        nb = min(chunk, nboot - c0)
        e = rng.choice(u, size=(nb, len(dy)), replace=True)
        d = np.zeros((nb, len(dy)))
        d[:, :p] = dy[:p]
        for t in range(p, len(dy)):
            m = b[0] + e[:, t - p]
            for j in range(1, p + 1):
                m = m + b[j] * d[:, t - j]
            d[:, t] = m
        Yb = np.concatenate([np.full((nb, 1), y[0]), y[0] + np.cumsum(d, axis=1)], axis=1)
        out.append(gsadf_stat(Yb, p, r0))
    sb = np.concatenate(out)
    pv = (1 + np.sum(sb >= stat)) / (nboot + 1)
    return float(stat), float(pv), float(np.quantile(sb, 0.95)), int(p)


def bh(pvals, q=0.05):
    p = np.asarray(pvals, float)
    m = len(p)
    o = np.argsort(p)
    thr = q * (np.arange(1, m + 1)) / m
    ok = p[o] <= thr
    rej = np.zeros(m, bool)
    if ok.any():
        kmax = np.max(np.where(ok)[0])
        rej[o[: kmax + 1]] = True
    return rej


def holm(pvals, alpha=0.05):
    p = np.asarray(pvals, float)
    m = len(p)
    o = np.argsort(p)
    rej = np.zeros(m, bool)
    for i, idx in enumerate(o):
        if p[idx] <= alpha / (m - i):
            rej[idx] = True
        else:
            break
    return rej


# ----------------------------------------------------------------------------- datos
def cargar():
    nac = pd.read_csv(RAIZ / "data/processed/nacional_q.csv")
    nac = nac[(nac.trimestre >= "2007Q1") & (nac.trimestre <= "2026Q2")].reset_index(drop=True)
    pan = pd.read_csv(RAIZ / "data/processed/v7/panel_ccaa_q_v7.csv", dtype={"codigo_ine_ccaa": str})
    pan = pan[(pan.trimestre >= "2007Q1") & (pan.trimestre <= "2026Q2")].reset_index(drop=True)
    return nac, pan


def series_nacionales(nac):
    ln = np.log
    P = {"ipv": nac.ipv.values, "tasado": nac.p_tasado.values}
    A = nac.ipc_alquiler.values
    R = nac.renta_hog.values
    i = nac.tipo_hip.values / 100.0
    ann = i / (1 - (1 + i) ** (-25))
    s = {}
    s["niveles"] = {"ipv": ln(P["ipv"]), "tasado": ln(P["tasado"])}
    s["ratios"] = {
        "ipv/renta": ln(P["ipv"]) - ln(R),
        "tasado/renta": ln(P["tasado"]) - ln(R),
        "ipv/alquiler": ln(P["ipv"]) - ln(A),
        "tasado/alquiler": ln(P["tasado"]) - ln(A),
    }
    s["tipos"] = {
        "ipv/(alquiler/tipo)": ln(P["ipv"]) - ln(A) + ln(i),
        "tasado/(alquiler/tipo)": ln(P["tasado"]) - ln(A) + ln(i),
        "cuota(ipv)/renta": ln(P["ipv"]) + ln(ann) - ln(R),
        "cuota(tasado)/renta": ln(P["tasado"]) + ln(ann) - ln(R),
    }
    return s


def _fam(series, base_seed, p_fijo=P_ADF):
    res = {}
    for k, (nombre, y) in enumerate(series.items()):
        res[nombre] = gsadf_test(y, base_seed + k, p_fijo=p_fijo)
    return res


def _cuenta(res, bhq=0.05):
    ps = [v[1] for v in res.values()]
    return int(np.sum(np.array(ps) < 0.05)), int(bh(ps, bhq).sum())


# ----------------------------------------------------------------------------- GSADF por id
_CACHE = {}


def _nacional():
    if "nac" not in _CACHE:
        nac, _ = cargar()
        s = series_nacionales(nac)
        _CACHE["nac"] = {fam: _fam(ser, SEED + 500 + 100 * j) for j, (fam, ser) in enumerate(s.items())}
    return _CACHE["nac"]


def _ccaa_series(pan, col_precio, desde=None, hasta=None):
    out = {}
    for cc, g in pan.groupby("ccaa", sort=True):
        g = g.sort_values("trimestre")
        if desde:
            g = g[(g.trimestre >= desde) & (g.trimestre <= hasta)]
        p = g[col_precio].astype(float).copy()
        interp = p.isna().any()
        if interp:  # interpolacion log-lineal de huecos interiores (marcada)
            p = np.exp(np.log(p).interpolate(limit_area="inside"))
        a = g.ipc_alquiler.astype(float)
        out[cc] = (np.log(p.values) - np.log(a.values), bool(interp))
    return out


def _var_bic():
    if "bic" not in _CACHE:
        nac, _ = cargar()
        s = series_nacionales(nac)
        _CACHE["bic"] = {fam: _fam(ser, SEED + 500 + 100 * j, None) for j, (fam, ser) in enumerate(s.items())}
    return _CACHE["bic"]


def V72_GSADF_niveles_bh():
    r = _nacional()["niveles"]
    n = _cuenta(r)[1]
    rb = _var_bic()["niveles"]
    return dict(valor=n, min=n, max=n, sens_p_bic=dict(p05=_cuenta(rb)[0], bh=_cuenta(rb)[1]), detalle={k: v for k, v in r.items()})


def V72_GSADF_ratios_bh():
    r = {k: v for k, v in _nacional()["ratios"].items()}
    n = _cuenta(r)[1]
    rb = _var_bic()["ratios"]
    return dict(valor=n, min=n, max=n, sens_p_bic=dict(p05=_cuenta(rb)[0], bh=_cuenta(rb)[1]), detalle=r)


def V72_GSADF_ratios_p05():
    r = _nacional()["ratios"]
    n = _cuenta(r)[0]
    rb = _var_bic()["ratios"]
    return dict(valor=n, min=n, max=n, sens_p_bic=dict(p05=_cuenta(rb)[0], bh=_cuenta(rb)[1]), detalle=r)


def V72_GSADF_tipos_p05():
    r = _nacional()["tipos"]
    n = _cuenta(r)[0]
    rb = _var_bic()["tipos"]
    return dict(valor=n, min=n, max=n, sens_p_bic=dict(p05=_cuenta(rb)[0], bh=_cuenta(rb)[1]), detalle=r)


def V72_GSADF_ccaa_bh():
    _, pan = cargar()
    res = {}
    k = 0
    for col in ("ipv", "p_tasado"):
        for cc, (y, interp) in _ccaa_series(pan, col).items():
            res[f"{cc}|{col}" + ("|interp" if interp else "")] = gsadf_test(y, SEED + 500 + 1000 + k)
            k += 1
    ps = [v[1] for v in res.values()]
    nbh = int(bh(ps).sum())
    nsin = int(np.sum(np.array(ps) < 0.05))
    return dict(valor=nbh, min=nbh, max=nbh, sin_ajuste=nsin, detalle=res)


def V72_GSADF_ccaa_v6():
    _, pan = cargar()
    # CCAA de entrenamiento v6: las que no contienen provincias selladas (bloques completos de CCAA)
    selladas = {"02", "03", "04", "05", "13", "14", "15", "17"}  # codigo_ine_ccaa con provincias selladas v6/v2
    ser = _ccaa_series(pan, "p_tasado", "2015Q1", "2024Q4")
    cod = pan.drop_duplicates("ccaa").set_index("ccaa").codigo_ine_ccaa.to_dict()
    sel = {c: v for c, v in ser.items() if cod[c] not in selladas and not np.isnan(v[0]).any()}
    res = {c: gsadf_test(v[0], SEED + 500 + 2000 + k) for k, (c, v) in enumerate(sel.items())}
    n = int(np.sum([v[1] < 0.05 for v in res.values()]))
    todas = {c: gsadf_test(v[0], SEED + 500 + 3000 + k) for k, (c, v) in enumerate(ser.items()) if not np.isnan(v[0]).any()}
    n17 = int(np.sum([v[1] < 0.05 for v in todas.values()]))
    return dict(valor=n, min=n, max=n, n_ccaa=len(res), n_con_17_ccaa=n17, detalle=res)


# ----------------------------------------------------------------------------- S3: R2 comun
def V71_S3_comun_r2_compra():
    _, pan = cargar()
    w = pan.pivot(index="trimestre", columns="ccaa", values="ln_ipv")
    d4 = w.diff(4).dropna(how="all")
    media = d4.mean(axis=1)
    r2 = {}
    for c in d4.columns:
        m = d4[c].notna() & media.notna()
        r2[c] = float(np.corrcoef(d4[c][m], media[m])[0, 1] ** 2) * 100
    v = np.array(list(r2.values()))
    # variante: tasa de variacion % en lugar de logaritmos
    w2 = pan.pivot(index="trimestre", columns="ccaa", values="ipv")
    y2 = (w2 / w2.shift(4) - 1).dropna(how="all")
    m2 = y2.mean(axis=1)
    r2b = np.array([np.corrcoef(y2[c][y2[c].notna()], m2[y2[c].notna()])[0, 1] ** 2 * 100 for c in y2.columns])
    return dict(valor=float(np.median(v)), min=float(v.min()), max=float(v.max()),
                variante_tasa_pct=dict(valor=float(np.median(r2b)), min=float(r2b.min()), max=float(r2b.max())),
                n_trim=int(d4.dropna().shape[0]), detalle=r2)


# ----------------------------------------------------------------------------- S3: largo plazo
def _ols(y, X):
    b, *_ = np.linalg.lstsq(X, y, rcond=None)
    e = y - X @ b
    return b, e


def _datos_panel(pan):
    pan = pan.copy()
    pan["tasa_paro"] = pan["tasa_paro_epa"]
    pan["covid"] = pan.trimestre.isin(["2020Q2", "2020Q3", "2020Q4"]).astype(float)
    pan["epa21"] = (pan.trimestre >= "2021Q1").astype(float)
    return pan


def _demean_transversal(pan, cols):
    pan = pan.copy()
    for c in cols:
        pan[c] = pan[c] - pan.groupby("trimestre")[c].transform("mean")
    return pan


def _ecm_group(g, y, xs, p, q, ctrl):
    """Forma ECM sin restricciones. Devuelve (phi, theta[], z-regresores) con theta=-beta/phi."""
    Y = g[y].values
    X = g[xs].values
    T = len(Y)
    dY = np.diff(Y)
    dX = np.diff(X, axis=0)
    t0 = max(p, q, 1)  # primera fila usable (indice de tiempo)
    rows = np.arange(t0, T)
    cols = [np.ones(len(rows)), Y[rows - 1]] + [X[rows - 1, j] for j in range(len(xs))]
    for l in range(1, p):
        cols.append(dY[rows - 1 - l])
    for l in range(0, q):
        for j in range(len(xs)):
            cols.append(dX[rows - 1 - l, j])
    for c in ctrl:
        cols.append(g[c].values[rows])
    Z = np.column_stack(cols)
    dep = dY[rows - 1]
    b, e = _ols(dep, Z)
    k1 = 2 + len(xs)
    phi = b[1]
    theta = -b[2:k1] / phi
    return phi, theta, Z, dep, e, rows


def _sbc_comun(pan, y, xs, ctrl, grid):
    mejor = (np.inf, None)
    for p, q in grid:
        tot, n = 0.0, 0
        for _, g in pan.groupby("ccaa"):
            g = g.dropna(subset=[y] + xs + ctrl).sort_values("trimestre")
            phi, th, Z, dep, e, rows = _ecm_group(g, y, xs, p, q, ctrl)
            tot += len(dep) * np.log(e @ e / len(dep)) + Z.shape[1] * np.log(len(dep))
            n += 1
        if tot / n < mejor[0]:
            mejor = (tot / n, (p, q))
    return mejor[1]


def _mg(pan_dm, y, xs, p, q, ctrl):
    th, phis = [], []
    for _, g in pan_dm.groupby("ccaa"):
        g = g.dropna(subset=[y] + xs + ctrl).sort_values("trimestre")
        phi, t, *_ = _ecm_group(g, y, xs, p, q, ctrl)
        th.append(t)
        phis.append(phi)
    th = np.array(th)
    return th, np.array(phis)


def _pmg(pan_dm, y, xs, p, q, ctrl, iters=60):
    grupos = []
    for _, g in pan_dm.groupby("ccaa"):
        g = g.dropna(subset=[y] + xs + ctrl).sort_values("trimestre")
        grupos.append(g)
    # preparar por grupo: dep, y_{t-1}, x_{t-1}, regresores de corto plazo
    prep = []
    for g in grupos:
        Y = g[y].values
        X = g[xs].values
        T = len(Y)
        dY = np.diff(Y)
        dX = np.diff(X, axis=0)
        t0 = max(p, q, 1)
        rows = np.arange(t0, T)
        sr = [np.ones(len(rows))]
        for l in range(1, p):
            sr.append(dY[rows - 1 - l])
        for l in range(0, q):
            for j in range(len(xs)):
                sr.append(dX[rows - 1 - l, j])
        for c in ctrl:
            sr.append(g[c].values[rows])
        W = np.column_stack(sr)
        M = np.eye(len(rows)) - W @ np.linalg.pinv(W)
        prep.append((M @ dY[rows - 1], M @ Y[rows - 1], M @ X[rows - 1, :]))
    # inicializar con theta de MG-medio via mediana de pooled OLS en niveles
    theta = np.zeros(len(xs))
    phis = np.full(len(prep), -0.1)
    sig = np.ones(len(prep))
    for _ in range(iters):
        for i, (dy, yl, xl) in enumerate(prep):
            z = yl - xl @ theta
            ph = (z @ dy) / (z @ z)
            r = dy - ph * z
            phis[i], sig[i] = ph, r @ r / len(dy)
        A = np.zeros((len(xs), len(xs)))
        bvec = np.zeros(len(xs))
        for i, (dy, yl, xl) in enumerate(prep):
            Xi = -phis[i] * xl
            yi = dy - phis[i] * yl
            A += Xi.T @ Xi / sig[i]
            bvec += Xi.T @ yi / sig[i]
        new = np.linalg.solve(A, bvec)
        if np.max(np.abs(new - theta)) < 1e-10:
            theta = new
            break
        theta = new
    return theta, phis


def _csdl(pan, y, xs, pT=4):
    """CS-DL (Chudik et al. 2016): y sobre x en niveles, pT retardos de dx y promedios transversales."""
    pan = pan.sort_values(["ccaa", "trimestre"])
    cs = pan.groupby("trimestre")[[y] + xs].mean()
    cs.columns = ["cs_" + c for c in cs.columns]
    dcs = cs[["cs_" + c for c in xs]].diff()
    out = []
    for _, g in pan.groupby("ccaa"):
        g = g.dropna(subset=[y] + xs).sort_values("trimestre").set_index("trimestre")
        Y = g[y]
        cols = {"c": pd.Series(1.0, index=g.index)}
        for c in xs:
            cols[c] = g[c]
        for c in xs:
            dx = g[c].diff()
            for l in range(pT):
                cols[f"d{c}{l}"] = dx.shift(l)
        for c in cs.columns:
            cols[c] = cs[c].reindex(g.index)
        for c in dcs.columns:
            for l in range(pT):
                cols[f"d{c}{l}"] = dcs[c].shift(l).reindex(g.index)
        D = pd.DataFrame(cols)
        D["y"] = Y
        D = D.dropna()
        b, _ = _ols(D["y"].values, D.drop(columns="y").values)
        out.append(b[1:1 + len(xs)])
    return np.array(out)


def V71_S3_largo_confirmadas():
    _, pan = cargar()
    pan = _datos_panel(pan)
    pan["ln_ocupados"] = pan["ln_ocupados"]
    hip = "ln_hip_importe"
    ctrl_c = ["d_ln_compraventas", "covid", "epa21"]
    ctrl_a = ["d_ln_hip_importe", "covid", "epa21"]
    H = [  # id, mercado, y, xs, ctrl, indice del coeficiente, signo
        ("H7-A1", "A", "ln_ipc_alquiler", ["ln_ocupados", "ln_pob_total"], ctrl_a, 0, +1, "F-A"),
        ("H7-A2", "A", "ln_ipc_alquiler", ["ln_ocupados", "ln_pob_total"], ctrl_a, 1, +1, "F-A"),
        ("H7-A3", "A", "ln_ipc_alquiler", ["tasa_paro"], ctrl_a, 0, -1, "F-A"),
        ("H7-C1", "C", "ln_ipv", ["ln_ocupados", hip, "ln_pob_total"], ctrl_c, 0, +1, "F-C"),
        ("H7-C2", "C", "ln_ipv", ["ln_ocupados", hip, "ln_pob_total"], ctrl_c, 1, +1, "F-C"),
        ("H7-C3", "C", "ln_ipv", ["ln_ocupados", hip, "ln_pob_total"], ctrl_c, 2, +1, "F-C"),
        ("H7-C4", "C", "ln_ipv", ["tasa_paro", hip], ctrl_c, 0, -1, "F-C"),
    ]
    grid = [(p, q) for p in range(1, 5) for q in range(1, 5)]
    res = []
    cacheSBC = {}
    for hid, mk, y, xs, ctrl, idx, sg, fam in H:
        todas = sorted(set([y] + xs + [c for c in ctrl if not c.startswith(("covid", "epa"))]))
        pdm = _demean_transversal(pan, [c for c in todas])
        key = (y, tuple(xs))
        if key not in cacheSBC:
            cacheSBC[key] = _sbc_comun(pdm.dropna(subset=todas), y, xs, ctrl, grid)
        p, q = cacheSBC[key]
        th, phis = _mg(pdm, y, xs, p, q, ctrl)
        t = th[:, idx]
        mg = t.mean()
        se = t.std(ddof=1) / np.sqrt(len(t))
        tst = mg / se
        pv = stats.t.sf(sg * tst, len(t) - 1)  # unilateral en la direccion de H1
        thp, _ = _pmg(pdm, y, xs, p, q, ctrl)
        cs = _csdl(pan, y, xs)[:, idx]
        res.append(dict(id=hid, fam=fam, pq=(p, q), mg=float(mg), mg_se=float(se), p=float(pv),
                        pmg=float(thp[idx]), csdl=float(cs.mean()), csdl_p=float(stats.t.sf(sg * cs.mean() / (cs.std(ddof=1) / np.sqrt(len(cs))), len(cs) - 1)),
                        signo=sg))
    for fam in ("F-A", "F-C"):
        ii = [i for i, r in enumerate(res) if r["fam"] == fam]
        rej = holm([res[i]["p"] for i in ii])
        for i, rj in zip(ii, rej):
            res[i]["holm_rechaza"] = bool(rj)
    for r in res:
        r["confirmada"] = bool(r["holm_rechaza"] and np.sign(r["mg"]) == r["signo"] == np.sign(r["pmg"]) == np.sign(r["csdl"]))
    n = int(sum(r["confirmada"] for r in res))
    return dict(valor=n, min=n, max=n, detalle=res)


def V71_S3_R6_e_ayuda_demanda_compra_precio10a():
    return None  # no reproducible desde la ficha (ver diagnostico)


# ----------------------------------------------------------------------------- principal
def _publicado():
    df = pd.read_csv(RAIZ / "output/v5/cifras_clave.csv")
    return df.set_index("id")


def main():
    np.random.seed(SEED)
    SALIDA.mkdir(parents=True, exist_ok=True)
    pub = _publicado()
    fun = {
        "V72-GSADF-ccaa-bh": V72_GSADF_ccaa_bh,
        "V72-GSADF-ccaa-v6": V72_GSADF_ccaa_v6,
        "V72-GSADF-niveles-bh": V72_GSADF_niveles_bh,
        "V72-GSADF-ratios-bh": V72_GSADF_ratios_bh,
        "V72-GSADF-ratios-p05": V72_GSADF_ratios_p05,
        "V72-GSADF-tipos-p05": V72_GSADF_tipos_p05,
        "V71-S3-R6-e_ayuda_demanda-compra-precio10a": V71_S3_R6_e_ayuda_demanda_compra_precio10a,
        "V71-S3-comun-r2-compra": V71_S3_comun_r2_compra,
        "V71-S3-largo-confirmadas": V71_S3_largo_confirmadas,
    }
    sal = []
    for i, f in fun.items():
        r = f()
        pr = pub.loc[i]
        item = dict(id=i, publicado=dict(valor=float(pr.valor), min=float(pr["min"]), max=float(pr["max"])))
        if r is None:
            item["replica"] = dict(valor=None, min=None, max=None)
            item["veredicto"] = "NO REPRODUCIBLE DESDE LA FICHA"
            item["diagnostico"] = ("La fila de cifras_clave solo da el indicador y las fuentes ('R6 v7; rejilla A4 v5; T3 v5.1; R4 v7'); no hay ficha en el anexo. "
                                   "Faltan: dosis de la ayuda por CCAA, regla de incidencia/traslado al precio (elasticidades), "
                                   "extracciones de la rejilla A4 y semilla, y el vinculo con T3 y R4 (documentado solo en output/v7/R6/metodo.md, fuera del alcance permitido).")
        else:
            det = r.pop("detalle", None)
            item["replica"] = dict(valor=r["valor"], min=r["min"], max=r["max"])
            item["extra"] = {k: v for k, v in r.items() if k not in ("valor", "min", "max")}
            item["detalle"] = det
            ok = all(_cerca(item["publicado"][k], item["replica"][k], i) for k in ("valor", "min", "max"))
            item["veredicto"] = "COINCIDE" if ok else "DISCREPA"
            item["diagnostico"] = DIAG.get(i, "")
        sal.append(item)
        print(i, item["publicado"], item["replica"], item["veredicto"], flush=True)
    (SALIDA / "resultado.json").write_text(json.dumps(sal, indent=1, ensure_ascii=False, default=_js))
    return sal


DIAG = {
    "V72-GSADF-ccaa-bh": "Estimador: la ficha no fija retardos de la ADF, el tratamiento del termino constante en el bootstrap ni el tamano de familia de BH. Con p=1 (que reproduce los estadisticos nacionales documentados 3,097 y 4,344) la replica da 26 series con p<0,05 y 23 tras BH sobre las 34; con p por BIC, 13 sin ajuste y 0 tras BH. El recuento es muy sensible a la especificacion y no converge a 7. Navarra (valor tasado con huecos 2015-2018) interpolada log-linealmente en la replica.",
    "V72-GSADF-ccaa-v6": "Coincide en el recuento (0) con la muestra de entrenamiento v6 reconstruida (9 CCAA sin provincias selladas, no 11: la cobertura de 11 CCAA no es derivable de la ficha); con las 17 CCAA tambien 0 (Navarra sin tasado en 2015-2018 excluida). Coincidencia debil: ninguna serie se acerca al VC.",
    "V72-GSADF-niveles-bh": "Estimador/bootstrap: con p=1 el valor tasado rechaza (p~0,01) y el IPV no (p~0,06-0,07 en varias semillas); con p=0 ambos rechazan, con p=2 o BIC solo el tasado. La cifra publicada (2) solo se obtiene con p=0; no se puede fijar desde la ficha.",
    "V72-GSADF-ratios-bh": "Estimador: con p=1, IPV/renta (p~0,01) y valor tasado/alquiler (p~0,015) sobreviven a BH de 4; con BIC 0 (coincide); con p=0 serian 3. El resultado cambia con el retardo de la ADF; la ficha no lo fija. Posible diferencia tambien en el definicion de renta (renta_hog nominal nacional de nacional_q).",
    "V72-GSADF-ratios-p05": "Estimador: con p=1, 2 de 4 (IPV/renta y tasado/alquiler; IPV/alquiler p=0,05-0,07 queda en el limite); publicado 3. Con BIC 1, con p=0 3 (IPV/renta no, p=0,09). Sensible al retardo; no determinable desde la ficha.",
    "V72-GSADF-tipos-p05": "Coincide (0 de 4) con tipo hipotecario nacional (nacional_q.tipo_hip), valor de referencia alquiler/tipo y cuota de anualidad a 25 anos sobre renta. Definicion exacta de las 2 'series' de la ficha no fijada (la replica usa 2 precios x 2 referencias); el 0 se obtiene con p=1 y con BIC (no probado con otros p).",
    "V71-S3-comun-r2-compra": "Coincide: R2 de la regresion de d4 ln IPV de cada CCAA sobre la media de las 17 CCAA (incluida ella), 2008T1-2026T2 (74 trimestres), mediana y rango entre CCAA, en %. Variante con tasa % en vez de log-diferencias: 93,7 (82,1-97,8).",
    "V71-S3-largo-confirmadas": "Coincide en 0 de 7: MG con demeaning transversal, ECM no restringido ARDL(1,1) por SBC comun (rejilla 1-4), p unilateral t(16) y Holm por familia; solo H7-C3 es significativa sin ajuste (p=0,044), no tras Holm. PMG de verosimilitud concentrada y CS-DL (pT=4) simplificados; sin bootstrap del PMG (solo el signo). Coincidencia en el recuento, no en las magnitudes (no publicadas).",
}


def _cerca(a, b, i):
    if a != a:  # publicado sin dato
        return True
    if i.startswith(("V72-GSADF", "V71-S3-largo")):
        return a == b
    return abs(a - b) <= 0.01 * abs(a)


def _js(o):
    if isinstance(o, (np.integer,)):
        return int(o)
    if isinstance(o, (np.floating,)):
        return float(o)
    if isinstance(o, (np.bool_,)):
        return bool(o)
    if isinstance(o, np.ndarray):
        return o.tolist()
    return str(o)


if __name__ == "__main__":
    sys.exit(0 if main() else 1)
