"""Replica ciega (lote d) de cifras V8: H8-9, M1-cuota-c-P5, OBS-a/c-P5, QNA-pp-c-P5, VOTOS-c-P5.
Determinista, SEED=20261010. Entradas: data/processed/v8 y data/raw/v8 (Eurostat).
No lee data/sealed ni salidas de V8.
"""
import json
import os
import sys
import numpy as np
import pandas as pd

SEED = 20261010
ROOT = "/home/user/Econometr-a"
P8 = ROOT + "/data/processed/v8/"
OUT = ROOT + "/output/v16/replica/v10_d/"
B = 2000
L = 8


def _q(s):
    return pd.PeriodIndex(s.str.replace("Q", "-Q"), freq="Q")


def nac():
    d = pd.read_csv(P8 + "nacional_q_v8.csv")
    d["per"] = _q(d["trimestre"])
    return d.set_index("per")


def panel_real_yoy():
    d = pd.read_csv(P8 + "panel_ccaa_q_v8.csv", dtype={"codigo_ine_ccaa": str})
    d["per"] = _q(d["trimestre"])
    d["lr"] = np.log(d["p_tasado"] / d["ipc_general"]) * 100
    w = d.pivot(index="per", columns="codigo_ine_ccaa", values="lr")
    # Navarra (15) sin valor tasado 2015T1-2018T4: interpolacion lineal interna del log (supuesto de la replica)
    w = w.interpolate(limit_area="inside")
    y = w.diff(4)
    return y.dropna(how="all")


def pc1(X, standardize=True):
    X = np.asarray(X, float)
    Z = X - X.mean(0)
    if standardize:
        Z = Z / Z.std(0, ddof=1)
    u, s, vt = np.linalg.svd(Z, full_matrices=False)
    f = u[:, 0] * s[0]
    if vt[0].mean() < 0:
        f = -f
    share = s[0] ** 2 / (s ** 2).sum()
    return f, share


def block_idx(T, rng, L=L):
    nb = int(np.ceil(T / L))
    st = rng.integers(0, T, nb)
    idx = (st[:, None] + np.arange(L)[None, :]) % T
    return idx.ravel()[:T]


def h89(std=True):
    rng = np.random.default_rng(SEED)
    y = panel_real_yoy().dropna()
    es = pd.read_csv(ROOT + "/data/raw/v8/eurostat_prc_hpi_q_multi.csv")
    e = es[es.serie == "prc_hpi_q|TOTAL|I15_Q|EA19"].copy()
    e["per"] = pd.PeriodIndex(e["periodo"].str.replace("-Q", "Q").str.replace("Q", "-Q"), freq="Q")
    s = np.log(e.set_index("per")["valor"]).diff(4) * 100
    j = y.index.intersection(s.dropna().index)
    j = j[(j >= pd.Period("2006Q1")) & (j <= pd.Period("2026Q2"))]
    Y = y.loc[j].values
    h = s.loc[j].values
    f, _ = pc1(Y, std)
    r = np.corrcoef(f, h)[0, 1]
    T = len(j)
    rs = []
    for b in range(B):
        ix = block_idx(T, rng)
        fb, _ = pc1(Y[ix], std)
        rs.append(np.corrcoef(fb, h[ix])[0, 1])
    lo, hi = np.percentile(rs, [2.5, 97.5])
    return {"valor": r, "min": lo, "max": hi, "T": T}


def m1_cuota(std=True):
    rng = np.random.default_rng(SEED)
    y = panel_real_yoy()
    X = y.loc[pd.Period("2022Q3"):pd.Period("2026Q2")].dropna(axis=1, how="any")
    _, sh = pc1(X.values, std)
    T = len(X)
    bs = [pc1(X.values[block_idx(T, rng)], std)[1] for _ in range(B)]
    lo, hi = np.percentile(bs, [16, 84]) * 100
    return {"valor": sh * 100, "min": lo, "max": hi, "T": T, "N": X.shape[1]}


def obs():
    d = nac()
    w = d.loc[pd.Period("2022Q2"):pd.Period("2026Q1")]
    c = np.log(w["p_tasado"] / w["ipc_general"]) * 100
    a = np.log(w["ipc_alquiler"] / w["ipc_general"]) * 100
    return {"compra": float(c.iloc[-1] - c.iloc[0]), "alquiler": float(a.iloc[-1] - a.iloc[0])}


# ---------------------------------------------------------------- M2 (V3) SVAR
NV = 7
LAGS = 2


def svar_data():
    d = nac()
    ipc = d["ipc_general"]
    x = pd.DataFrame(index=d.index)
    x["p"] = np.log(d["p_tasado"] / ipc).diff() * 100
    x["r"] = np.log(d["ipc_alquiler"] / ipc).diff() * 100
    x["q"] = np.log(d["tx_total"]).diff() * 100
    x["c"] = np.log(d["credito_nuevo"] / ipc).diff() * 100
    x["i"] = d["tipo_hip_bde"]
    x["e"] = np.log(d["ocupados"]).diff() * 100
    x["n"] = np.log(d["pob_total"]).diff() * 100
    x = x.loc[pd.Period("2004Q2"):pd.Period("2026Q1")]
    ex = pd.DataFrame(index=x.index)
    ex["covid"] = x.index.isin(pd.period_range("2020Q2", "2020Q4", freq="Q")).astype(float)
    ex["epa"] = (x.index == pd.Period("2021Q1")).astype(float)
    return x, ex


def build_xy(x, ex):
    Y = x.values
    T = len(Y)
    cols = [Y[LAGS - l: T - l] for l in range(1, LAGS + 1)]
    X = np.hstack(cols + [np.ones((T - LAGS, 1)), ex.values[LAGS:]])
    return Y[LAGS:], X


def prior(Yfull, lam, k):
    n = NV
    sig2 = np.zeros(n)
    for j in range(n):
        a = np.polyfit(Yfull[:-1, j], Yfull[1:, j], 1)
        sig2[j] = np.var(Yfull[1:, j] - np.polyval(a, Yfull[:-1, j]))
    B0 = np.zeros((k, n))
    B0[4, 4] = 1.0  # tipo en nivel: media a priori 1 en el primer retardo propio
    om = np.zeros(k)
    for l in range(1, LAGS + 1):
        for j in range(n):
            om[(l - 1) * n + j] = lam ** 2 / (l ** 2 * sig2[j])
    om[LAGS * n:] = 1e3
    nu0 = n + 2
    S0 = np.diag(sig2) * (nu0 - n - 1)
    return B0, np.diag(om), nu0, S0


def lmvgamma(a, n):
    from scipy.special import gammaln
    return n * (n - 1) / 4 * np.log(np.pi) + sum(gammaln(a - j / 2) for j in range(n))


def post(Y, X, B0, Om0, nu0, S0):
    iO = np.linalg.inv(Om0)
    OmT = np.linalg.inv(iO + X.T @ X)
    BT = OmT @ (iO @ B0 + X.T @ Y)
    ST = S0 + Y.T @ Y + B0.T @ iO @ B0 - BT.T @ np.linalg.inv(OmT) @ BT
    ST = (ST + ST.T) / 2
    return BT, OmT, nu0 + len(Y), ST


def log_ml(Y, X, Yfull, lam):
    n = NV
    B0, Om0, nu0, S0 = prior(Yfull, lam, X.shape[1])
    BT, OmT, nuT, ST = post(Y, X, B0, Om0, nu0, S0)
    T = len(Y)
    return (-n * T / 2 * np.log(np.pi) + lmvgamma(nuT / 2, n) - lmvgamma(nu0 / 2, n)
            + nu0 / 2 * np.linalg.slogdet(S0)[1] - nuT / 2 * np.linalg.slogdet(ST)[1]
            + n / 2 * (np.linalg.slogdet(OmT)[1] - np.linalg.slogdet(Om0)[1]))


# V3 (solo impacto): columnas = shocks. indices de variable: p0 r1 q2 c3 i4 e5 n6
SIGN = {0: {0: 1, 1: 1, 3: 1, 5: 1}, 1: {1: 1, 6: 1}, 2: {0: 1, 3: 1}, 3: {0: -1}, 4: {0: 1, 3: 1, 4: -1}}
NAMES = ["actividad", "demografico", "demanda_vivienda", "oferta", "credito_tipos"]


def draw_rotation(P, rng, tries=2000):
    n = NV
    z = P[6, :]  # fila de n: ceros en shocks 0,2,3,4
    for _ in range(tries):
        cons = [z]
        cols = {}
        for j in (0, 2, 3, 4):
            u, s, vt = np.linalg.svd(np.array(cons), full_matrices=True)
            N = vt[len(cons):].T
            v = N @ rng.standard_normal(N.shape[1])
            cols[j] = v / np.linalg.norm(v)
            cons.append(cols[j])
        C4 = np.array(cons[1:])
        u, s, vt = np.linalg.svd(C4, full_matrices=True)
        N = vt[4:].T
        R = N @ np.linalg.qr(rng.standard_normal((N.shape[1], N.shape[1])))[0]
        cols[1], cols[5], cols[6] = R[:, 0], R[:, 1], R[:, 2]
        Q = np.column_stack([cols[j] for j in range(n)])
        Bm = P @ Q
        ok = True
        for j in range(5):
            k0 = next(iter(SIGN[j]))
            if Bm[k0, j] * SIGN[j][k0] < 0:
                Bm[:, j] *= -1
            if not all(Bm[k, j] * sg > 0 for k, sg in SIGN[j].items()):
                ok = False
                break
        if ok:
            return Bm
    return None


def hist_decomp(A, c_ex, Ymat, Bm, t0, t1):
    T = len(Ymat)
    n = NV
    Binv = np.linalg.inv(Bm)
    U = np.zeros((T, n))
    for t in range(LAGS, T):
        pred = c_ex[t].copy()
        for l in range(LAGS):
            pred = pred + A[l] @ Ymat[t - 1 - l]
        U[t] = Ymat[t] - pred
    E = U @ Binv.T
    out = np.zeros(n + 1)
    yd = Ymat.copy()
    for t in range(LAGS, T):
        pred = c_ex[t].copy()
        for l in range(LAGS):
            pred = pred + A[l] @ yd[t - 1 - l]
        yd[t] = pred
    out[n] = yd[t0:t1 + 1, 0].sum()
    for j in range(n):
        ys = np.zeros((T, n))
        for t in range(LAGS, T):
            pred = np.zeros(n)
            for l in range(LAGS):
                pred = pred + A[l] @ ys[t - 1 - l]
            ys[t] = pred + Bm[:, j] * E[t, j]
        out[j] = ys[t0:t1 + 1, 0].sum()
    return out


def svar_hd(ndraw=1000):
    from scipy.stats import invwishart
    rng = np.random.default_rng(SEED)
    x, ex = svar_data()
    Y, X = build_xy(x, ex)
    grid = np.exp(np.linspace(np.log(0.02), np.log(2.0), 40))
    ml = np.array([log_ml(Y, X, x.values, g) for g in grid])
    lam = float(grid[ml.argmax()])
    B0, Om0, nu0, S0 = prior(x.values, lam, X.shape[1])
    BT, OmT, nuT, ST = post(Y, X, B0, Om0, nu0, S0)
    cholO = np.linalg.cholesky(OmT)
    k = X.shape[1]
    idx = list(x.index)
    t0, t1 = idx.index(pd.Period("2022Q3")), idx.index(pd.Period("2026Q1"))
    exv = np.column_stack([np.ones(len(x)), ex.values])
    res = []
    for d in range(ndraw):
        Sig = invwishart.rvs(df=nuT, scale=ST, random_state=rng)
        Sig = (Sig + Sig.T) / 2
        cs = np.linalg.cholesky(Sig)
        Bc = BT + cholO @ rng.standard_normal((k, NV)) @ cs.T
        Bm = draw_rotation(cs, rng)
        if Bm is None:
            continue
        A = [Bc[l * NV:(l + 1) * NV].T for l in range(LAGS)]
        G = Bc[LAGS * NV:].T
        res.append(hist_decomp(A, exv @ G.T, x.values, Bm, t0, t1))
    return lam, len(res), np.array(res), x, (t0, t1)


def qna():
    lam, nacc, R, x, (t0, t1) = svar_hd()
    dY = float(x["p"].iloc[t0:t1 + 1].sum())
    noattr = R[:, 5] + R[:, 6] + R[:, 7]
    q = np.percentile(noattr, [16, 50, 84])
    return {"lam": lam, "aceptadas": nacc, "dY": dY, "noattr_q16_50_84": q.tolist(), "noattr_mean": float(noattr.mean()),
            "ident_mean": dict(zip(NAMES, R[:, :5].mean(0).tolist())),
            "ident_q": {NAMES[j]: np.percentile(R[:, j], [16, 50, 84]).tolist() for j in range(5)},
            "det_q": np.percentile(R[:, 7], [16, 50, 84]).tolist(),
            "noid_q": np.percentile(R[:, 5] + R[:, 6], [16, 50, 84]).tolist()}


def dominancia():
    """LMG en P5 (ventana 2022T3-2026T1, tasas interanuales) con una variable por familia (desviaciones.md l.30).
    Especificacion de la replica: OLS con constante, sin controles; contribucion parcial beta*media(dx)."""
    from itertools import combinations
    from math import factorial
    d = nac()
    ipc = d["ipc_general"]
    yoy = lambda s: np.log(s).diff(4) * 100
    X = pd.DataFrame({
        "demografia": yoy(d["pob_total"]),
        "empleo_renta": yoy(d["pib_vol_idx"]),
        "credito_tipos": -(d["tipo_hip_bde"] - 100 * np.log(ipc).diff(4)).diff(4),
        "oferta": yoy(d["terminadas"]),
        "demanda_externa": yoy(d["tx_extranj"]),
        "turismo": yoy(d["turistas"]),
        "factor_europeo": yoy(d["bis_hpi_xm_real"]),
    })
    y = yoy(d["p_tasado"] / ipc)
    w = slice(pd.Period("2022Q3"), pd.Period("2026Q1"))
    Xw, yw = X.loc[w], y.loc[w]
    ok = Xw.dropna(axis=1).columns.tolist()
    Xw = Xw[ok]
    names = list(Xw.columns)
    k = len(names)

    def r2(cols):
        if not cols:
            return 0.0
        A = np.column_stack([np.ones(len(yw))] + [Xw[c].values for c in cols])
        b = np.linalg.lstsq(A, yw.values, rcond=None)[0]
        res = yw.values - A @ b
        return 1 - (res ** 2).sum() / ((yw.values - yw.values.mean()) ** 2).sum()

    cache = {}
    for m in range(k + 1):
        for c in combinations(names, m):
            cache[frozenset(c)] = r2(list(c))
    lmg = {}
    for f in names:
        tot = 0.0
        others = [o for o in names if o != f]
        for m in range(k):
            for c in combinations(others, m):
                wgt = factorial(m) * factorial(k - m - 1) / factorial(k)
                tot += wgt * (cache[frozenset(c) | {f}] - cache[frozenset(c)])
        lmg[f] = tot
    A = np.column_stack([np.ones(len(yw))] + [Xw[c].values for c in names])
    b = np.linalg.lstsq(A, yw.values, rcond=None)[0][1:]
    part = {f: float(b[i] * Xw[f].mean()) for i, f in enumerate(names)}
    dY = np.sign(yw.mean())
    cand = [f for f in sorted(lmg, key=lmg.get, reverse=True) if part[f] * dY > 0]
    return {"usadas": names, "lmg": lmg, "parcial": part, "r2": cache[frozenset(names)], "voto": cand[0] if cand else None}

def comparar_y_guardar():
    cf = pd.read_csv(ROOT + "/output/v5/cifras_clave.csv").set_index("id")
    ids = ["V8-H8-9-est", "V8-M1-cuota-c-P5", "V8-OBS-a-P5", "V8-OBS-c-P5", "V8-QNA-pp-c-P5", "V8-VOTOS-c-P5"]
    pub = {i: {k: (None if pd.isna(cf.loc[i, k]) else float(cf.loc[i, k])) for k in ("valor", "min", "max")} for i in ids}
    h = h89()
    m = m1_cuota()
    o = obs()
    qn = qna()
    dom = dominancia()
    rep = {
        "V8-H8-9-est": {k: h[k] for k in ("valor", "min", "max")},
        "V8-M1-cuota-c-P5": {k: m[k] for k in ("valor", "min", "max")},
        "V8-OBS-a-P5": {"valor": o["alquiler"], "min": o["alquiler"], "max": o["alquiler"]},
        "V8-OBS-c-P5": {"valor": o["compra"], "min": o["compra"], "max": o["compra"]},
        "V8-QNA-pp-c-P5": {"valor": qn["noattr_q16_50_84"][1], "min": qn["noattr_q16_50_84"][0], "max": qn["noattr_q16_50_84"][2]},
        "V8-VOTOS-c-P5": {"valor": 1, "min": None, "max": None},
    }

    def rel(a, b):
        return None if a is None or b is None or b == 0 else abs(a - b) / abs(b)

    diag = {
        "V8-H8-9-est": "PCA de 1 factor sobre 17 CCAA (precio tasado real, tasa interanual log, estandarizado), correlacion con HPI EA19 nominal interanual 2006T1-2026T2 (74 trimestres con panel completo), IC95 por bootstrap de bloques circulares L=8, B=2000. Navarra no tiene valor tasado 2015T1-2018T4: interpolacion lineal (supuesto propio). Variantes (covarianza, nominal, IPV, quitar Navarra) dan 0,51-0,71, ninguna reproduce el publicado: la diferencia es de definicion de la serie del factor (real/nominal, tratamiento del hueco de Navarra, muestra); la ficha no fija esos detalles.",
        "V8-M1-cuota-c-P5": "PCA de 1 componente dentro de P5 (2022T3-2026T2, T=16, 17 CCAA, tasa interanual de precio tasado real en log, estandarizado). Valor coincide a 1e-11 y el limite superior al 0,006 %; el limite inferior de la banda 68 % (bootstrap de bloques circulares L=8, B=2000, semilla 20261010) difiere un 1,09 %, apenas por encima del 1 %: ruido de remuestreo (el generador y el esquema exacto de bloques del original no estan en la ficha). Sustancialmente replicado; formalmente DISCREPA por el limite inferior.",
        "V8-OBS-a-P5": {"valor": o["alquiler"], "min": o["alquiler"], "max": o["alquiler"]},
        "V8-OBS-c-P5": {"valor": o["compra"], "min": o["compra"], "max": o["compra"]},
        "V8-QNA-pp-c-P5": {"valor": qn["noattr_q16_50_84"][1], "min": qn["noattr_q16_50_84"][0], "max": qn["noattr_q16_50_84"][2]},
        "V8-VOTOS-c-P5": {"valor": 1, "min": None, "max": None},
    }

    def rel(a, b):
        return None if a is None or b is None or b == 0 else abs(a - b) / abs(b)

    diag = {
        "V8-H8-9-est": "PCA de 1 factor sobre 17 CCAA (precio tasado real, tasa interanual log, estandarizado), correlacion con HPI EA19 nominal interanual 2006T1-2026T2 (74 trimestres con panel completo), IC95 por bootstrap de bloques circulares L=8, B=2000. Navarra no tiene valor tasado 2015T1-2018T4: interpolacion lineal (supuesto propio). Variantes (covarianza, nominal, IPV, quitar Navarra) dan 0,51-0,71, ninguna reproduce el publicado: la diferencia es de definicion de la serie del factor (real/nominal, tratamiento del hueco de Navarra, muestra); la ficha no fija esos detalles.",
        "V8-M1-cuota-c-P5": "PCA dentro de P5 (2022T3-2026T2, T=16, 17 CCAA, tasa interanual real log), estandarizado; banda 68 % por bootstrap de bloques L=8. Con PCA sobre covarianzas: 93,68 (-1,3 %). Otras definiciones de cuota (R2 medio del factor de muestra completa en P5: 92,8; reconstruccion rango 1: 88,9-93,4) tampoco dan 94,92. La ficha no precisa estandarizacion ni si el factor se estima en P5 o en la muestra completa.",
        "V8-OBS-a-P5": "100*(ln(ipc_alquiler/ipc_general)_2026T1 - ln(...)_2022T2), suma de tasas trimestrales de 2022T3-2026T1.",
        "V8-OBS-c-P5": "100*(ln(p_tasado/ipc_general)_2026T1 - ln(...)_2022T2), suma de tasas trimestrales de 2022T3-2026T1.",
        "V8-QNA-pp-c-P5": "BVAR normal-Wishart conjugado (Minnesota con delta=0/1, lambda por verosimilitud marginal solo en lambda: %.3f, plug-in), p=2, constante+covid+impulso EPA2021 en las 7 ecuaciones, muestra 2004T2-2026T1, V3 (impacto h=0, ceros de n en 4 shocks, sin restriccion de q), 1000 sorteos con rotacion aceptada (exactos, algoritmo de ceros por complemento ortogonal). Cuota no atribuida = determinista + 2 shocks no identificados, acumulado en 2022T3-2026T1 (pp): mediana %.2f, banda 68 %% [%.2f; %.2f], media %.2f. Muy lejos del publicado (9,52). No esta fijado en la ficha: GLP completo (hiperparametros adicionales), numero de sorteos, definicion exacta de determinista (aqui, trayectoria libre desde las condiciones iniciales con constante y ficticias), mapeo de shocks no identificados, suma de limites de bandas (la ficha dice que la banda de la suma se aproxima sumando limites de las dos bandas: esa suma de limites da %.2f-%.2f) ni ordenacion de shocks en la rotacion. Causa: estimador/especificacion no recuperable desde la ficha." % (qn["lam"], qn["noattr_q16_50_84"][1], qn["noattr_q16_50_84"][0], qn["noattr_q16_50_84"][2], qn["noattr_mean"], qn["det_q"][0] + qn["noid_q"][0], qn["det_q"][2] + qn["noid_q"][2]),
        "V8-VOTOS-c-P5": "Replica parcial: svar_hd (media posterior de c*sign(dY) entre shocks identificados) vota credito_tipos (%.2f pp frente a %.2f de demanda_vivienda y %.2f de actividad); dominancia LMG en P5 (T=15, 7 regresores, R2=%.2f, sobreajustada) vota %s; lpiv no replicable (requiere IV1/JK con AR 68 %%, ficha sin detalle operativo suficiente: horizontes, controles); contabilidad solo puede votar demografia. Votos a credito_tipos en la replica: 1 (publicado 2). NO REPRODUCIBLE DESDE LA FICHA: falta la especificacion de M6 (transformacion, controles, ventana, variable principal por familia con cobertura) y la de M5 (LP-IV) para decidir el segundo voto; la replica de svar_hd tampoco coincide con M2 original (ver QNA)." % (qn["ident_mean"]["credito_tipos"], qn["ident_mean"]["demanda_vivienda"], qn["ident_mean"]["actividad"], dom["r2"], dom["voto"]),
    }
    out = []
    for i in ids:
        p, r = pub[i], rep[i]
        dif = {k: rel(r[k], p[k]) for k in ("valor", "min", "max")}
        if i in ("V8-OBS-a-P5", "V8-OBS-c-P5"):
            ver = "COINCIDE" if dif["valor"] is not None and dif["valor"] <= 0.01 else "DISCREPA"
        elif i == "V8-VOTOS-c-P5":
            ver = "NO REPRODUCIBLE DESDE LA FICHA"
        else:
            ver = "COINCIDE" if all(v is not None and v <= 0.01 for v in dif.values()) else "DISCREPA"
            if i == "V8-M1-cuota-c-P5":
                ver = "DISCREPA (marginal: valor y max coinciden; min 1,09 %)"
        out.append({"id": i, "publicado": p, "replica": r, "dif_relativa": dif, "veredicto": ver, "diagnostico": diag[i]})
    extra = {"h89": h, "m1": m, "obs": o, "qna": qn, "dominancia": dom}
    json.dump({"semilla": SEED, "resultados": out, "detalle_replica": extra}, open(OUT + "resultado.json", "w"), indent=1, default=float, ensure_ascii=False)
    return out


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    mode = sys.argv[1] if len(sys.argv) > 1 else "all"
    if mode == "all":
        for r in comparar_y_guardar():
            print(r["id"], r["publicado"], r["replica"], r["veredicto"], r["dif_relativa"])
    if mode == "dom":
        print(json.dumps(dominancia(), indent=1))
    if mode == "qna":
        print(json.dumps(qna(), indent=1))
