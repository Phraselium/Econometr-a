"""M2 v6: incertidumbre de modelo (BMA, elastic net con PDS, multiverso). Determinista, sin red.

Solo lee output/v6/M0/paneles/*_train.csv.gz. Todo C4 (asociativo/predictivo, nada causal).
"""
import itertools
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.linear_model import ElasticNetCV

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))
from econ_utils import Registry  # noqa: E402

SEED = 20261010
FECHA = "2026-10-11"
PAN = ROOT / "output/v6/M0/paneles"
OUT = ROOT / "output/v6/M2"
OUT.mkdir(parents=True, exist_ok=True)
REG = Registry(OUT / "registro.csv")

CP_REG = ["ln_pob", "share_ext_pob", "ln_pib_pc", "paro_tasa", "ln_ocupados_miles", "ln_terminadas_libres",
          "ln_iniciadas_libres", "ln_suelo_pm2_m50k", "ln_vut", "ln_hip_viv_num"]
ALQ_REG = ["ln_pob", "share_ext_pob", "ln_pib_pc", "ln_vut", "ln_terminadas_libres", "ln_iniciadas_libres",
           "n_mun_tensionados", "n_mun_topes_cat"]
DIS_REG = ["ln_vut_plazas_dis", "ln_pib_pc"]
DISPERSAS = ["ln_vut", "ln_suelo_pm2_m50k"]
ISLAS = [7, 35, 38]
SMOKE = "--smoke" in sys.argv


def leer(n):
    return pd.read_csv(PAN / f"{n}_train.csv.gz")


# ---------------------------------------------------------------- datos
def construir(df, unit, y, regs, lag=1, diff=False, excl_islas=False, prov_col=None):
    """Desenlace en t, regresores en t-lag; opcionalmente primeras diferencias. Muestra completa."""
    d = df.copy()
    if excl_islas and prov_col is not None:
        d = d[~d[prov_col].isin(ISLAS)]
    cols = [c for c in regs if c in d.columns]
    base = d[[unit, "anio", y] + cols].copy()
    if lag:
        x = d[[unit, "anio"] + cols].copy()
        x["anio"] = x["anio"] + lag
        base = base[[unit, "anio", y]].merge(x, on=[unit, "anio"], how="inner")
    if diff:
        prev = base.copy()
        prev["anio"] = prev["anio"] + 1
        base = base.merge(prev, on=[unit, "anio"], suffixes=("", "_p"))
        for c in [y] + cols:
            base[c] = base[c] - base[c + "_p"]
        base = base[[unit, "anio", y] + cols]
    if prov_col is not None and prov_col in d.columns:
        base = base.merge(d[[unit, prov_col]].drop_duplicates(unit), on=unit, how="left")
    return base.dropna(subset=[y] + cols).reset_index(drop=True)


def residualizar(M, unit, anio, trend=False, it=200, tol=1e-9):
    """Proyección sobre FE de unidad y año (y tendencia lineal por unidad) por proyecciones alternas."""
    M = M.astype(float).copy()
    u = pd.Series(unit).reset_index(drop=True)
    a = pd.Series(anio).reset_index(drop=True)
    t = a.astype(float)
    tc = t - t.groupby(u).transform("mean")
    den = (tc ** 2).groupby(u).transform("sum").replace(0, np.nan)
    out = M.copy()
    for j in range(M.shape[1]):
        v = pd.Series(M[:, j])
        for _ in range(it):
            v0 = v.copy()
            v = v - v.groupby(u).transform("mean")
            if trend:
                v = v - tc * ((tc * v).groupby(u).transform("sum") / den).fillna(0)
            v = v - v.groupby(a).transform("mean")
            if np.abs(v - v0).max() < tol:
                break
        out[:, j] = v.values
    return out


def ols_cluster(y, X, cl):
    """MCO con errores agrupados (datos ya residualizados). Devuelve beta, se, p."""
    from scipy import stats
    n, k = X.shape
    XtXi = np.linalg.pinv(X.T @ X)
    b = XtXi @ X.T @ y
    e = y - X @ b
    cls = pd.factorize(cl)[0]
    G = cls.max() + 1
    S = np.zeros((k, k))
    sc = np.zeros((G, k))
    np.add.at(sc, cls, X * e[:, None])
    S = sc.T @ sc
    V = XtXi @ S @ XtXi * (G / max(G - 1, 1)) * ((n - 1) / max(n - k, 1))
    se = np.sqrt(np.clip(np.diag(V), 1e-300, None))
    p = 2 * stats.t.sf(np.abs(b / se), max(G - 1, 1))
    return b, se, p


# ---------------------------------------------------------------- BMA
def bma(y, X, nombres, n_fe, g_min_n=None, prior="uniforme"):
    """Enumeración de 2^K modelos, g-prior de Zellner con g = max(N, K^2) (FLS); y, X ya residualizados.
    prior: 'uniforme' sobre modelos o 'betabin' (beta-binomial(1,1) sobre el tamaño)."""
    from math import comb
    N, K = X.shape
    sd = X.std(axis=0)
    Z = X / sd
    y = y - y.mean()
    g = float(max(N, K ** 2))
    neff = N - n_fe
    yy = float(y @ y)
    logpost, stats_ = [], []
    for k in range(K + 1):
        for S in itertools.combinations(range(K), k):
            if k == 0:
                logml, b, V = 0.0, np.zeros(0), np.zeros((0, 0))
                r2 = 0.0
            else:
                Zs = Z[:, list(S)]
                ZtZi = np.linalg.pinv(Zs.T @ Zs)
                bh = ZtZi @ Zs.T @ y
                r2 = float(bh @ (Zs.T @ Zs) @ bh) / yy
                logml = 0.5 * (neff - 1 - k) * np.log1p(g) - 0.5 * (neff - 1) * np.log1p(g * (1 - r2))
                b = g / (1 + g) * bh
                s2 = (yy * (1 - r2) + yy * r2 / (1 + g)) / max(neff - 3, 1)
                V = s2 * g / (1 + g) * ZtZi
            lp = 0.0 if prior == "uniforme" else -np.log((K + 1) * comb(K, k))
            logpost.append(logml + lp)
            stats_.append((S, b, V))
    lp = np.array(logpost)
    w = np.exp(lp - lp.max())
    w /= w.sum()
    pip = np.zeros(K)
    m1 = np.zeros(K)
    m2 = np.zeros(K)
    for wi, (S, b, V) in zip(w, stats_):
        for i, j in enumerate(S):
            pip[j] += wi
            m1[j] += wi * b[i]
            m2[j] += wi * (V[i, i] + b[i] ** 2)
    mean = m1 / sd  # a escala original de X
    sdp = np.sqrt(np.clip(m2 - m1 ** 2, 0, None)) / sd
    # cuantiles aproximados vía mezcla normal por modelo (muestreo determinista)
    rng = np.random.default_rng(SEED)
    idx = rng.choice(len(w), size=4000, p=w)
    draws = np.zeros((4000, K))
    for r, mi in enumerate(idx):
        S, b, V = stats_[mi]
        if len(S):
            draws[r, list(S)] = rng.multivariate_normal(b, V)
    draws /= sd
    return pd.DataFrame({"variable": nombres, "pip": pip, "media_post": mean, "sd_post": sdp,
                         "q025": np.quantile(draws, 0.025, axis=0), "q975": np.quantile(draws, 0.975, axis=0),
                         "prior": prior, "g": g, "n": N})


# ---------------------------------------------------------------- PDS
def folds_bloques(anios, origenes=(2018, 2020, 2022), embargo=1):
    """Entrenamiento: años < origen - embargo; validación: origen y origen+1 (hipotesis.md §5)."""
    a = np.asarray(anios)
    out = []
    for o in origenes:
        tr = np.where(a < o - embargo)[0]
        va = np.where((a >= o) & (a <= o + 1))[0]
        if len(tr) > 10 and len(va) > 5:
            out.append((tr, va))
    return out


def pds(y, X, nombres, anios, cl):
    """Post-double-selection (Belloni, Chernozhukov, Hansen) con elastic net y CV en bloques con embargo.
    Para cada variable de interés j: selección sobre y~controles y x_j~controles; MCO con la unión."""
    rows = []
    fo = folds_bloques(anios)
    if len(fo) < 2:
        fo = None
    K = X.shape[1]
    Zs = (X - X.mean(0)) / X.std(0)

    def sel(t, C):
        if fo is not None:
            cvv = [(tr, va) for tr, va in fo]
        else:
            cvv = 3
        m = ElasticNetCV(l1_ratio=[0.5, 0.9], cv=cvv, alphas=40, max_iter=20000, random_state=SEED)
        m.fit(C, t - t.mean())
        return set(np.where(np.abs(m.coef_) > 1e-10)[0])

    sel_joint = sel(y, Zs)
    for j in range(K):
        oth = [i for i in range(K) if i != j]
        C = Zs[:, oth]
        sy, sx = sel(y, C), sel(Zs[:, j], C)
        U = sorted(set(oth[i] for i in sy | sx))
        Xr = np.column_stack([X[:, j]] + [X[:, i] for i in U])
        b, se, p = ols_cluster(y, Xr, cl)
        rows.append({"variable": nombres[j], "seleccion_enet": j in sel_joint,
                     "n_controles_sel": len(U), "sel_y": [nombres[oth[i]] for i in sorted(sy)],
                     "sel_x": [nombres[oth[i]] for i in sorted(sx)],
                     "coef_pds": b[0], "ic_lo": b[0] - 1.96 * se[0], "ic_hi": b[0] + 1.96 * se[0], "p_pds": p[0]})
    return pd.DataFrame(rows)


# ---------------------------------------------------------------- multiverso
def conjuntos_controles(regs, rng):
    nuc = [r for r in regs if r not in DISPERSAS]
    conj = {"todos": list(regs), "nucleo_sin_dispersas": nuc}
    if len(regs) > 3:
        for i in range(4):
            k = int(rng.integers(max(2, len(regs) // 2), len(regs)))
            conj[f"aleat{i}"] = sorted(rng.choice(regs, k, replace=False).tolist())
    return conj


def multiverso(df, unit, y_list, regs, prov_col, etiqueta, dims, capa_mat):
    """Cada especificación es una regresión conjunta; se guarda el coeficiente de cada variable incluida."""
    rng = np.random.default_rng(SEED)
    conj = conjuntos_controles(regs, rng)
    recs = []
    sid = 0
    for (cn, cs), tr, dif, lag, yv, isl in itertools.product(
            conj.items(), dims["trend"], dims["diff"], dims["lag"], y_list, dims["islas"]):
        d = construir(df, unit, yv, cs, lag=lag, diff=dif, excl_islas=isl, prov_col=prov_col)
        if len(d) < 30 or d[unit].nunique() < 5:
            continue
        cs2 = [c for c in cs if c in d.columns and d[c].std() > 0]
        if not cs2:
            continue
        M = residualizar(d[[yv] + cs2].values, d[unit].values, d["anio"].values, trend=tr and not dif)
        # si hay diferencias: FE de año sobre diferencias (la tendencia en niveles pasa a constante de unidad)
        if dif and tr:
            M = residualizar(d[[yv] + cs2].values, d[unit].values, d["anio"].values, trend=False)
        yy, XX = M[:, 0], M[:, 1:]
        if np.linalg.matrix_rank(XX) < XX.shape[1]:
            continue
        cl = d[prov_col].values if prov_col in d.columns else d[unit].values
        b, se, p = ols_cluster(yy, XX, cl)
        sid += 1
        for v, bi, si, pi in zip(cs2, b, se, p):
            recs.append({"spec": sid, "mercado_nivel": etiqueta, "variable": v, "controles": cn, "tendencia": tr,
                         "diferencias": dif, "lag": lag, "desenlace": yv, "sin_islas": isl, "n": len(d),
                         "coef": bi, "se": si, "p": pi})
            REG.log("M2_multiverso", f"{etiqueta}|spec{sid}|{v}",
                    f"{yv}~{'+'.join(cs2)}|ctrl={cn},tend={tr},dif={dif},lag={lag},islas_excl={isl}",
                    d["anio"].min(), d["anio"].max(), len(d), np.nan, np.nan, np.nan, np.nan, bi, pi,
                    "C4 asociativo")
    return pd.DataFrame(recs)


def bh(pv, q=0.10):
    p = np.asarray(pv, float)
    n = len(p)
    o = np.argsort(p)
    adj = np.empty(n)
    adj[o] = np.minimum.accumulate((p[o] * n / (np.arange(n) + 1))[::-1])[::-1]
    return np.clip(adj, 0, 1)


def resumen_multiverso(mv):
    g = mv.groupby("variable")
    out = g.agg(n_spec=("coef", "size"), mediana=("coef", "median"),
                p25=("coef", lambda s: s.quantile(.25)), p75=("coef", lambda s: s.quantile(.75)),
                pct_sig05=("p", lambda s: 100 * (s < .05).mean())).reset_index()
    sg = []
    for v, s in g["coef"]:
        sg.append(100 * (np.sign(s) == np.sign(s.median())).mean())
    out["pct_mismo_signo"] = sg
    return out


# ---------------------------------------------------------------- ejecución por mercado y nivel
def preparar_nivel(df, unit, y, regs, lag=1, prov_col=None):
    d = construir(df, unit, y, regs, lag=lag, prov_col=prov_col)
    regs_ok = [c for c in regs if c in d.columns and d[c].std() > 0]
    return d, regs_ok


def correr(nombre, df, unit, y, regs, prov_col, y_alt, dims, mercado, nivel, medida):
    print(f"== {nombre}", flush=True)
    res = {"nombre": nombre, "mercado": mercado, "nivel": nivel, "medida_precio": medida, "desenlace": y}
    variantes = {"completa": list(regs), "nucleo": [r for r in regs if r not in DISPERSAS]}
    bm, pd_all = [], []
    for vn, rv in variantes.items():
        if vn == "nucleo" and rv == list(regs):
            continue
        d, rv = preparar_nivel(df, unit, y, rv, prov_col=prov_col)
        if len(d) < 30:
            continue
        nfe = d[unit].nunique() + d["anio"].nunique() - 1
        M = residualizar(d[[y] + rv].values, d[unit].values, d["anio"].values)
        yy, XX = M[:, 0], M[:, 1:]
        cl = d[prov_col].values if prov_col in d.columns else d[unit].values
        for pr in ["uniforme", "betabin"]:
            b = bma(yy, XX, rv, nfe, prior=pr)
            b["muestra"] = vn
            bm.append(b)
            for _, r in b.iterrows():
                REG.log("M2_BMA", f"{nombre}|{vn}|{pr}|{r.variable}", f"{y}~{'+'.join(rv)} (FE unidad+año, g=max(N,K^2))",
                        d["anio"].min(), d["anio"].max(), len(d), np.nan, np.nan, np.nan, np.nan, r.media_post,
                        np.nan, f"PIP={r.pip:.3f}; C4")
        pp = pds(yy, XX, rv, d["anio"].values, cl)
        pp["muestra"] = vn
        pp["n"] = len(d)
        pd_all.append(pp)
        for _, r in pp.iterrows():
            REG.log("M2_PDS", f"{nombre}|{vn}|{r.variable}", f"PDS enet CV bloques embargo 1a: {y}", d["anio"].min(),
                    d["anio"].max(), len(d), np.nan, np.nan, np.nan, np.nan, r.coef_pds, r.p_pds, "C4")
    mv = multiverso(df, unit, [y] + y_alt, regs, prov_col, nombre, dims, "C4")
    mv["p_bh"] = bh(mv["p"].values) if len(mv) else []
    res_mv = resumen_multiverso(mv) if len(mv) else pd.DataFrame()
    return res, pd.concat(bm), pd.concat(pd_all), mv, res_mv


def main():
    stats_dir = OUT / "tablas"
    stats_dir.mkdir(exist_ok=True)
    pa = leer("prov_alquiler_anual")
    pc = leer("prov_compra_anual")
    pa["cod_prov"] = pa["cod"]
    pc["cod_prov"] = pc["cod"]
    # los regresores de demanda y oferta viven en el panel de compra (misma clave cod, anio)
    ex = ["ln_pob", "share_ext_pob", "ln_pib_pc", "ln_terminadas_libres", "ln_iniciadas_libres"]
    pa = pa.merge(pc[["cod", "anio"] + ex], on=["cod", "anio"], how="left")
    pa_prov = pa
    dims_p = {"trend": [False, True], "diff": [False, True], "lag": [0, 1], "islas": [False, True]}
    dims_m = {"trend": [False, True], "diff": [False, True], "lag": [1], "islas": [False]}
    if SMOKE:
        dims_p = {"trend": [False], "diff": [False], "lag": [1], "islas": [False]}
        dims_m = dims_p
    # municipios y distritos: regresores provinciales se unen por provincia y año
    ma = leer("mun_alquiler_anual").merge(pa_prov[["cod_prov", "anio"] + [r for r in ALQ_REG if r not in ("n_mun_tensionados", "n_mun_topes_cat")]],
                                          on=["cod_prov", "anio"], how="left")
    ma["n_mun_tensionados"] = ma["tensionada_mun"]
    ma["n_mun_topes_cat"] = ma["tope_cat_mun"]
    mc = leer("mun_compra_anual").merge(pc[["cod_prov", "anio"] + CP_REG], on=["cod_prov", "anio"], how="left")
    di = leer("dis_alquiler_anual").merge(pa[["cod_prov", "anio", "ln_pib_pc"]], on=["cod_prov", "anio"], how="left")
    if SMOKE:
        ma = ma[ma.cod_prov.isin(sorted(ma.cod_prov.unique())[:8])]
        di = di[di.cod_prov.isin(sorted(di.cod_prov.unique())[:5])]
    jobs = [
        ("alq_stock_prov", pa, "cod", "ln_alq_m2_serpavi_vc", ALQ_REG, "cod_prov",
         ["ln_alq_mes_serpavi_vc", "ln_ipc_alq_idx"], dims_p, "alquiler de stock", "provincia", None),
        ("compra_precio_prov", pc, "cod", "ln_pm2_tasado", CP_REG, "cod_prov",
         ["ln_pm2_registradores"], dims_p, "precio de compra", "provincia", "valor tasado MIVAU"),
        ("compra_volumen_prov", pc, "cod", "ln_cv_etdp", CP_REG, "cod_prov",
         ["ln_cv_registradores"], dims_p, "volumen de compra", "provincia", None),
        ("alq_stock_mun", ma, "cod_mun", "ln_alq_m2_serpavi_mun", ALQ_REG, "cod_prov", [], dims_m,
         "alquiler de stock", "municipio", None),
        ("compra_precio_mun", mc, "cod_mun", "ln_pm2_tasado_mun", CP_REG, "cod_prov", [], dims_m,
         "precio de compra", "municipio", "valor tasado MIVAU municipal"),
        ("alq_stock_dis", di, "distrito", "ln_alq_m2_serpavi_dis", DIS_REG, "cod_prov", [], dims_m,
         "alquiler de stock", "distrito", None),
    ]
    todo = {}
    for j in jobs:
        res, bm, pdf, mv, rm = correr(*j)
        todo[res["nombre"]] = (res, bm, pdf, mv, rm)
        bm.to_csv(stats_dir / f"bma_{res['nombre']}.csv", index=False)
        pdf.drop(columns=[]).to_csv(stats_dir / f"pds_{res['nombre']}.csv", index=False)
        rm.to_csv(stats_dir / f"multiverso_resumen_{res['nombre']}.csv", index=False)
        mv.to_csv(stats_dir / f"multiverso_{res['nombre']}.csv.gz", index=False)
    REG.flush()
    import pickle
    with open(OUT / (".tmp_todo.pkl" if not SMOKE else ".tmp_smoke.pkl"), "wb") as f:
        pickle.dump(todo, f)


if __name__ == "__main__":
    main()
