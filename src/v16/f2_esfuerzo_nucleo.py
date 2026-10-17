"""V16 fase 2 · núcleo de cálculo (esfuerzo de acceso y descomposiciones contables). Solo descriptivo (C4).

Definiciones (documentadas también en output/v16/f2_esfuerzo/informe.md):
- G (gasto neto) = 12·HH070 − HY070N ; Y (renta neta) = HY020 − HY070N (definición Eurostat de la sobrecarga de coste
  de vivienda: gastos de vivienda netos de ayudas a la vivienda / renta disponible neta de esas ayudas).
  HH070 es mensual; HY020 y HY070N, anuales.
- Sobrecarga 40 % / 30 %: G > 0,40·Y / G > 0,30·Y. Con Y <= 0 y G > 0 se cuenta como sobrecarga.
- Esfuerzo r = min(G/Y, 1); r = 1 si Y <= 0 y G > 0; r = 0 si G <= 0.
- Renta residual: renta equivalente antes = HY020/HX240; después = (HY020 − 12·HH070)/HX240; umbral z = 60 % de la
  mediana ponderada (personas) de la renta equivalente ANTES del gasto, del mismo año. «Cae bajo el umbral por el gasto»:
  antes >= z y después < z.
"""
from __future__ import annotations

import numpy as np
import pandas as pd

SEED = 20261010
CCAA_NOMBRES = {"ES11": "Galicia", "ES12": "Asturias", "ES13": "Cantabria", "ES21": "País Vasco", "ES22": "Navarra",
                "ES23": "La Rioja", "ES24": "Aragón", "ES30": "Madrid", "ES41": "Castilla y León",
                "ES42": "Castilla-La Mancha", "ES43": "Extremadura", "ES51": "Cataluña",
                "ES52": "Comunitat Valenciana", "ES53": "Illes Balears", "ES61": "Andalucía", "ES62": "Murcia",
                "ES63": "Ceuta", "ES64": "Melilla", "ES70": "Canarias"}
TEN = ["prop_sin_hipoteca", "prop_con_hipoteca", "alquiler_mercado", "alquiler_reducido_cesion"]
EDAD = ["16-34", "35-49", "50-64", "65+"]
NAC = ["Espana", "UE", "Resto"]
QUIN = ["Q1", "Q2", "Q3", "Q4", "Q5"]
INDIC_POB = ["sobre40", "sobre30", "cae_bajo_umbral", "pobreza_antes", "pobreza_despues"]
INDIC_ALL = INDIC_POB + ["esfuerzo_medio"]
UNID = {"sobre40": "% de la población", "sobre30": "% de la población", "cae_bajo_umbral": "% de la población",
        "pobreza_antes": "% de la población", "pobreza_despues": "% de la población",
        "esfuerzo_medio": "% de la renta neta (media de hogares)"}


def wmedian(x, w, q=0.5):
    o = np.argsort(x, kind="stable")
    x, w = x[o], w[o]
    c = np.cumsum(w)
    return float(x[min(np.searchsorted(c, q * c[-1]), len(x) - 1)])


def preparar(d: pd.DataFrame) -> pd.DataFrame:
    """Variables derivadas por hogar (una fila por hogar-año)."""
    x = d.copy()
    for c in ("HH020", "HH021", "cuotahip", "HH060", "HY070N"):
        if c not in x.columns:
            x[c] = np.nan
    ten =pd.Series(np.nan, index=x.index)
    old = x.anio <= 2010
    h20 = x.HH020
    ten[old & (h20 == 1)] = np.where(x.cuotahip[old & (h20 == 1)] > 0, 2, 1)   # propiedad: hipoteca = cuota > 0
    ten[old & (h20 == 2)] = 3
    ten[old & (h20.isin([3, 4]))] = 4
    new = ~old
    ten[new] = x.HH021[new].fillna(x.HH020[new])
    ten[new & (ten == 5)] = 4
    x["ten"] = ten.map({1: TEN[0], 2: TEN[1], 3: TEN[2], 4: TEN[3]})
    ay = x.HY070N.fillna(0.0)
    x["G"] = 12 * x.HH070 - ay
    x["Y"] = x.HY020 - ay
    ok = x.G.notna() & x.Y.notna()
    x = x[ok].copy()
    ay = x.HY070N.fillna(0.0)
    x["s40"] = ((x.G > 0.4 * x.Y) & (x.G > 0)).astype(float)
    x["s30"] = ((x.G > 0.3 * x.Y) & (x.G > 0)).astype(float)
    with np.errstate(divide="ignore", invalid="ignore"):
        r = np.where(x.G <= 0, 0.0, np.where(x.Y <= 0, 1.0, np.minimum(x.G / x.Y, 1.0)))
    x["r"] = r
    x["eq_pre"] = x.HY020 / x.HX240
    x["eq_post"] = (x.HY020 - 12 * x.HH070) / x.HX240
    x["wh"] = x.DB090
    x["wp"] = x.pop_w
    x["ccaa"] = x.DB040.astype(str)
    x["edad_g"] = pd.cut(x.edad_sust, [-1, 34.5, 49.5, 64.5, 200], labels=EDAD).astype(object)
    nm = {"1": "Espana", "2": "UE", "3": "Resto", "4": "Resto"}
    x["nac_g"] = x.nac_raw.map(nm)
    # quintiles de renta equivalente antes del gasto, ponderados por personas, por año
    q = pd.Series(index=x.index, dtype=object)
    for y, g in x.groupby("anio"):
        cuts = [wmedian(g.eq_pre.values, g.wp.values, p) for p in (0.2, 0.4, 0.6, 0.8)]
        k = np.searchsorted(cuts, g.eq_pre.values, side="left")
        q[g.index] = np.array(QUIN, dtype=object)[k]
    x["quintil"] = q
    return x.reset_index(drop=True)


def celdas(g: pd.DataFrame):
    """Devuelve lista (dim, categoria, mascara booleana) para un año."""
    out = [("Total", "Espana", np.ones(len(g), bool))]
    for dim, col, cats in [("CCAA", "ccaa", sorted(CCAA_NOMBRES)), ("Quintil", "quintil", QUIN), ("Edad", "edad_g", EDAD),
                           ("Tenencia", "ten", TEN), ("Nacionalidad", "nac_g", NAC)]:
        for c in cats:
            out.append((dim, c if dim != "CCAA" else c, (g[col] == c).values))
    return out


def bootstrap_anio(g: pd.DataFrame, B: int, seed: int):
    """Estimación y B réplicas (remuestreo de hogares con reposición) de todas las celdas e indicadores de un año.

    Devuelve dict (dim, cat, indicador) -> vector de longitud B+1 (posición 0 = muestra completa) y dict n por celda.
    El umbral de pobreza se recalcula en cada réplica; la pertenencia a quintil se fija con la muestra completa.
    """
    rng = np.random.default_rng([seed, int(g.anio.iloc[0])])
    cl = celdas(g)
    n = len(g)
    wp, wh = g.wp.values, g.wh.values
    s40, s30, r = g.s40.values, g.s30.values, g.r.values
    pre, post = g.eq_pre.values, g.eq_post.values
    M = np.stack([m for _, _, m in cl]).astype(float)   # celdas x n
    keys = [(d, c) for d, c, _ in cl]
    res = {(d, c, i): np.full(B + 1, np.nan) for d, c in keys for i in INDIC_ALL}
    nobs = {(d, c): int(m.sum()) for d, c, m in cl}
    for b in range(B + 1):
        idx = np.arange(n) if b == 0 else rng.integers(0, n, n)
        z = 0.6 * wmedian(pre[idx], wp[idx])
        Mi = M[:, idx]
        wpi, whi = wp[idx], wh[idx]
        den_p = Mi @ wpi
        den_h = Mi @ whi
        pa, pd_ = (pre[idx] < z), (post[idx] < z)
        inds = {"sobre40": s40[idx], "sobre30": s30[idx], "cae_bajo_umbral": (~pa & pd_).astype(float),
                "pobreza_antes": pa.astype(float), "pobreza_despues": pd_.astype(float)}
        with np.errstate(divide="ignore", invalid="ignore"):
            for i, v in inds.items():
                val = 100 * (Mi @ (wpi * v)) / den_p
                for k, (d, c) in enumerate(keys):
                    res[(d, c, i)][b] = val[k]
            val = 100 * (Mi @ (whi * r[idx])) / den_h
            for k, (d, c) in enumerate(keys):
                res[(d, c, "esfuerzo_medio")][b] = val[k]
    return res, nobs


def resumen_celda(v: np.ndarray, n: int, min_n: int = 50, max_cv: float = 0.30):
    est = v[0]
    rep = v[1:][np.isfinite(v[1:])]
    if len(rep) < 10 or not np.isfinite(est):
        return dict(estimacion=est, se=np.nan, ic_lo=np.nan, ic_hi=np.nan, cv=np.nan, estado="suprimida")
    se = float(rep.std(ddof=1))
    lo, hi = np.percentile(rep, [2.5, 97.5])
    cv = se / abs(est) if est != 0 else np.inf
    estado = "publicable" if (n >= min_n and cv <= max_cv) else "suprimida"
    return dict(estimacion=est, se=se, ic_lo=float(lo), ic_hi=float(hi), cv=cv, estado=estado)


def tabla_anio(res, nobs, anio):
    filas = []
    for (d, c, i), v in res.items():
        s = resumen_celda(v, nobs[(d, c)])
        motivo = ""
        if s["estado"] == "suprimida":
            motivo = "n<50" if nobs[(d, c)] < 50 else "CV>30%"
        filas.append(dict(anio=anio, dimension=d, categoria=c, indicador=i, unidad=UNID[i], n_hogares=nobs[(d, c)],
                          motivo_supresion=motivo, **s))
    return filas


def bh(p):
    p = np.asarray(p, float)
    n = len(p)
    o = np.argsort(p)
    adj = np.empty(n)
    run = 1.0
    for rank in range(n, 0, -1):
        j = o[rank - 1]
        run = min(run, p[j] * n / rank)
        adj[j] = run
    return adj


# ------------------------------------------------------------------------------------------ descomposiciones
def diseno(g: pd.DataFrame):
    """Matriz X con grupos de variables para las descomposiciones; columnas: const, ln_renta, edad, edad2, tam, UE, Resto, regiones."""
    ln = np.log(np.clip(g.Y.values, 1000.0, None))
    ed = g.edad_sust.values
    cols = {"const": np.ones(len(g)), "ln_renta": ln, "edad": ed, "edad2": ed ** 2 / 100.0, "tam": g.HX040.values,
            "nac_UE": (g.nac_g == "UE").values.astype(float), "nac_Resto": (g.nac_g == "Resto").values.astype(float)}
    for c in sorted(CCAA_NOMBRES):
        if c != "ES61":   # referencia: Andalucía
            cols["reg_" + c] = (g.ccaa == c).values.astype(float)
    X = pd.DataFrame(cols, index=g.index)
    grupos = {"renta": ["ln_renta"], "edad": ["edad", "edad2"], "tamano_hogar": ["tam"],
              "nacionalidad": ["nac_UE", "nac_Resto"], "region": [c for c in X.columns if c.startswith("reg_")]}
    return X, grupos


def wls(X, y, w):
    sw = np.sqrt(w)
    A = X * sw[:, None]
    beta, *_ = np.linalg.lstsq(A, y * sw, rcond=None)
    return beta


def wmean(X, w):
    return (X * w[:, None]).sum(0) / w.sum()


def logit_w(X, d, w, it=25):
    b = np.zeros(X.shape[1])
    b[0] = np.log(np.average(d, weights=w) / (1 - np.average(d, weights=w)))
    for _ in range(it):
        eta = np.clip(X @ b, -30, 30)
        p = 1 / (1 + np.exp(-eta))
        W = w * p * (1 - p) + 1e-12
        z = eta + (d - p) / np.maximum(p * (1 - p), 1e-12)
        bn = np.linalg.solve((X * W[:, None]).T @ X + 1e-8 * np.eye(len(b)), (X * W[:, None]).T @ z)
        if np.max(np.abs(bn - b)) < 1e-8:
            b = bn
            break
        b = bn
    return b


def wq(y, w, q):
    return wmedian(y, w, q)


def rif(y, w, tau):
    q = wq(y, w, tau)
    neff = w.sum() ** 2 / (w ** 2).sum()
    sd = np.sqrt(np.average((y - np.average(y, weights=w)) ** 2, weights=w))
    iqr = wq(y, w, 0.75) - wq(y, w, 0.25)
    h = 0.9 * min(sd, iqr / 1.34 if iqr > 0 else sd) * neff ** (-0.2)
    h = max(h, 1e-4)
    f = np.sum(w * np.exp(-0.5 * ((y - q) / h) ** 2)) / (w.sum() * h * np.sqrt(2 * np.pi))
    return q + (tau - (y <= q).astype(float)) / max(f, 1e-6), q


ESTAD = [("media", None), ("p10", 0.10), ("p50", 0.50), ("p90", 0.90)]


def descomponer(a: pd.DataFrame, b: pd.DataFrame, ycol="r"):
    """Descomposición contable del cambio de `ycol` entre la muestra a (inicial) y b (final). Devuelve dict plano.

    OB dos pliegues con coeficientes de referencia agrupados (con indicador de año); OB tres pliegues (dotaciones,
    coeficientes, interacción) con coeficientes del año inicial; DFL (reponderación logit; efectos composición y
    estructura) para media, p10, p50, p90; RIF (FFL) para p10, p50, p90 con referencia agrupada.
    """
    Xa, gr = diseno(a)
    Xb, _ = diseno(b)
    ya, yb = a[ycol].values, b[ycol].values
    wa, wb = a.wh.values, b.wh.values
    Xa_, Xb_ = Xa.values, Xb.values
    out = {}
    xa, xb = wmean(Xa_, wa), wmean(Xb_, wb)
    b0, b1 = wls(Xa_, ya, wa), wls(Xb_, yb, wb)
    Xp = np.vstack([np.column_stack([Xa_, np.zeros(len(ya))]), np.column_stack([Xb_, np.ones(len(yb))])])
    bp = wls(Xp, np.r_[ya, yb], np.r_[wa, wb])[:-1]
    dx = xb - xa
    tot = float(xb @ b1 - xa @ b0)
    out["media|total"] = tot
    out["OB2|atribuido"] = float(dx @ bp)
    out["OB2|no_atribuido"] = float(xb @ (b1 - bp) + xa @ (bp - b0))
    out["OB3|dotaciones"] = float(dx @ b0)
    out["OB3|coeficientes"] = float(xa @ (b1 - b0))
    out["OB3|interaccion"] = float(dx @ (b1 - b0))
    cn = list(Xa.columns)
    for g_, cols in gr.items():
        ii = [cn.index(c) for c in cols]
        out[f"OB2det|{g_}"] = float(dx[ii] @ bp[ii])
    # DFL
    Xl = np.vstack([Xa_, Xb_])[:, 1:]
    Xl = np.column_stack([np.ones(len(Xl)), Xl])
    dd = np.r_[np.zeros(len(ya)), np.ones(len(yb))]
    ww = np.r_[wa / wa.sum(), wb / wb.sum()]
    bl = logit_w(Xl, dd, ww)
    p = 1 / (1 + np.exp(-np.clip(Xl[: len(ya)] @ bl, -30, 30)))
    psi = p / (1 - p)
    wcf = wa * psi
    wcf = wcf * wa.sum() / wcf.sum()
    for nm, tau in ESTAD:
        f = (lambda y, w: float(np.average(y, weights=w))) if tau is None else (lambda y, w, t=tau: wq(y, w, t))
        s0, s1, scf = f(ya, wa), f(yb, wb), f(ya, wcf)
        out[f"DFL|{nm}|total"] = s1 - s0
        out[f"DFL|{nm}|composicion"] = scf - s0
        out[f"DFL|{nm}|estructura"] = s1 - scf
    out["DFL|ess_ratio"] = float(wcf.sum() ** 2 / (wcf ** 2).sum() / (wa.sum() ** 2 / (wa ** 2).sum()))
    # RIF
    for nm, tau in ESTAD[1:]:
        ra, qa = rif(ya, wa, tau)
        rb, qb = rif(yb, wb, tau)
        c0, c1 = wls(Xa_, ra, wa), wls(Xb_, rb, wb)
        cp = wls(Xp, np.r_[ra, rb], np.r_[wa, wb])[:-1]
        e = float(dx @ cp)
        out[f"RIF|{nm}|total"] = qb - qa
        out[f"RIF|{nm}|atribuido"] = e
        out[f"RIF|{nm}|no_atribuido"] = float(xb @ (c1 - cp) + xa @ (cp - c0))
        out[f"RIF|{nm}|aprox"] = (qb - qa) - (float(xb @ c1 - xa @ c0))
        for g_, cols in gr.items():
            ii = [cn.index(c) for c in cols]
            out[f"RIFdet|{nm}|{g_}"] = float(dx[ii] @ cp[ii])
    return out


def directa(a: pd.DataFrame, b: pd.DataFrame, gcol="G"):
    """Identidad exacta de la razón de medias R = Ḡ/Ȳ (pesos de hogar):
    R1−R0 = ΔḠ/Ȳ0 [gasto] + Ḡ0·Δ(1/Ȳ) [renta] + ΔḠ·Δ(1/Ȳ) [interacción]; y en logs Δln R = Δln Ḡ − Δln Ȳ."""
    Ga, Ya = np.average(a[gcol], weights=a.wh), np.average(a.Y, weights=a.wh)
    Gb, Yb = np.average(b[gcol], weights=b.wh), np.average(b.Y, weights=b.wh)
    R0, R1 = Ga / Ya, Gb / Yb
    dG, di = Gb - Ga, 1 / Yb - 1 / Ya
    return {"R0": 100 * R0, "R1": 100 * R1, "dR": 100 * (R1 - R0), "gasto": 100 * dG / Ya, "renta": 100 * Ga * di,
            "interaccion": 100 * dG * di, "dlnG": np.log(Gb / Ga), "dlnY": np.log(Yb / Ya), "dlnR": np.log(R1 / R0),
            "G0": Ga, "G1": Gb, "Y0": Ya, "Y1": Yb}
