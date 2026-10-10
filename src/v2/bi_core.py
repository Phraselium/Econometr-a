"""BI · núcleo: construcción del panel shift-share y estimadores (2SLS cluster, WCB Webb, Rotemberg,
BHJ, AKM0, Hansen). Datos SOLO vía v2_common.load. Sin red; SEED fijo."""
from __future__ import annotations

import sys
from pathlib import Path

import warnings
import numpy as np
import pandas as pd
from scipy import stats

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import v2_common as vc  # noqa: E402

warnings.filterwarnings("ignore", category=pd.errors.PerformanceWarning)
SEED = vc.SEED
GRUPOS = ["europa", "africa", "norteamerica", "asia", "centroamerica_caribe", "oceania", "sudamerica",
          "apatridas"]
GRUPOS5 = {"europa": ["europa"], "africa": ["africa"], "america": ["norteamerica", "centroamerica_caribe", "sudamerica"],
           "asia": ["asia"], "otros": ["oceania", "apatridas"]}
COSTA = {"03", "04", "07", "08", "12", "15", "17", "18", "20", "21", "29", "30", "33", "35", "36", "38", "39",
         "43", "46", "48", "51", "52"}   # provincias con litoral/insulares (clasificación geográfica externa)


# ----------------------------------------------------------------- datos
def _stocks(d: pd.DataFrame) -> dict:
    s = {"africa": d["pob_nac_de_africa"], "norteamerica": d["pob_nac_de_america_del_norte"],
         "asia": d["pob_nac_de_asia"], "centroamerica_caribe": d["pob_nac_de_centro_america_y_caribe"],
         "oceania": d["pob_nac_de_oceania"], "sudamerica": d["pob_nac_de_sudamerica"],
         "apatridas": d["pob_nac_apatridas"]}
    # Europa: UE28 + resto (hasta 2020) o UE27 + resto (desde 2021): la suma es coherente en el tiempo
    eu = d[["pob_nac_pais_de_la_ue28_sin_espana", "pob_nac_pais_de_europa_menos_ue28"]].sum(axis=1, min_count=2)
    eu2 = d[["pob_nac_pais_de_la_ue27_2020_sin_espana", "pob_nac_pais_de_europa_menos_ue27_2020"]].sum(axis=1, min_count=2)
    s["europa"] = eu.fillna(eu2)
    return s


def construir_panel(anio_ini=2009, anio_fin=2021) -> tuple[pd.DataFrame, dict]:
    """Panel provincia-año con x, z (y z por grupo), resultados y características 2002.
    Devuelve (df largo 2002..último año, meta)."""
    d = vc.load("panel_prov_a").sort_values(["cod_prov", "anio"]).reset_index(drop=True)
    nq = vc.load("nacional_q_v2")
    nq["anio"] = nq["trimestre"].astype(str).str[:4].astype(int)
    defl = nq[nq["trimestre"].astype(str) <= vc.Q_TRAIN_FIN].groupby("anio")["ln_deflactor"].mean()
    d["ln_defl"] = d["anio"].map(defl)
    g = d.groupby("cod_prov")
    d["pop_l"] = g["pob_total"].shift(1)
    d["pop_l2"] = g["pob_total"].shift(2)
    S = _stocks(d)
    for k in GRUPOS:
        d[f"S_{k}"] = S[k]
    for k in GRUPOS:
        d[f"dS_{k}"] = d.groupby("cod_prov")[f"S_{k}"].diff()
    # cuotas FIJAS 2002 (sobre el conjunto de provincias de entrenamiento = "España" disponible)
    d02 = d[d["anio"] == 2002].set_index("cod_prov")
    share = pd.DataFrame({k: d02[f"S_{k}"] / d02[f"S_{k}"].sum() for k in GRUPOS})
    # shock nacional del grupo (sobre provincias de entrenamiento) y leave-one-out
    tot = {k: d.groupby("anio")[f"dS_{k}"].transform("sum") for k in GRUPOS}
    for k in GRUPOS:
        sh = d["cod_prov"].map(share[k])
        d[f"sh_{k}"] = sh
        d[f"shock_{k}"] = tot[k]                                    # g_gt (nacional, con todas)
        d[f"zg_{k}"] = 100 * sh * (tot[k] - d[f"dS_{k}"]) / d["pop_l"]   # componente LOO, pp de pob
        # versión alineada con el año del flujo: variación del stock t+1 - t (stock a 1 enero)
        dfw = d.groupby("cod_prov")[f"dS_{k}"].shift(-1)
        totf = dfw.groupby(d["anio"]).transform("sum")
        d[f"zgf_{k}"] = 100 * sh * (totf - dfw) / d["pop_l"]
    d["z"] = d[[f"zg_{k}" for k in GRUPOS]].sum(axis=1, min_count=len(GRUPOS))
    d["z_fwd"] = d[[f"zgf_{k}" for k in GRUPOS]].sum(axis=1, min_count=len(GRUPOS))
    for k5, ks in GRUPOS5.items():
        d[f"z5_{k5}"] = d[[f"zg_{k}" for k in ks]].sum(axis=1, min_count=len(ks))
    d["x"] = 100 * d["inmig_flujo"] / d["pop_l"]
    d["x_l1"] = d.groupby("cod_prov")["x"].shift(1) * d["pop_l"] / d["pop_l2"]  # flujo_{t-1}/pob_{t-2}
    d["z_l1"] = d.groupby("cod_prov")["z"].shift(1)
    d["x_stock"] = 100 * d.groupby("cod_prov")["pob_extranj"].diff() / d["pop_l"]
    d["y_alq"] = 100 * d.groupby("cod_prov")["ipc_alquiler"].transform(lambda s: np.log(s).diff())
    lp = np.log(d["p_tasado"]) - d["ln_defl"]
    d["y_pre"] = 100 * lp.groupby(d["cod_prov"]).diff()
    d["y_dif"] = d["y_alq"] - d["y_pre"]
    d["y_alq_l1"] = d.groupby("cod_prov")["y_alq"].shift(1)
    # características 2002 (previas)
    c = pd.DataFrame(index=d02.index)
    c["ln_pob02"] = np.log(d02["pob_total"])
    c["extr02"] = 100 * d02["pob_extranj"] / d02["pob_total"]
    c["paro02"] = 100 * d02["parados"] / (d02["parados"] + d02["ocupados"])
    p0 = d[d["anio"].between(2002, 2004)].groupby("cod_prov")["p_tasado"].mean()
    c["ln_p02"] = np.log(p0)
    c["costa"] = [float(i in COSTA) for i in c.index]
    vut = d[d["anio"] == 2020].set_index("cod_prov")
    c["vut20_pm"] = 1000 * vut["vut_viviendas"] / vut["pob_total"]
    for col in c.columns:
        d[col] = d["cod_prov"].map(c[col])
    meta = dict(share=share, car=c, anio_ini=anio_ini, anio_fin=anio_fin)
    return d, meta


def muestra(d, cols, a0=2009, a1=2021):
    m = d[d["anio"].between(a0, a1)].dropna(subset=cols).copy()
    return m.reset_index(drop=True)


# ----------------------------------------------------------------- álgebra FE
class FE:
    """Proyector sobre dummies de provincia y año (y tendencias provinciales opcionales)."""

    def __init__(self, m: pd.DataFrame, tend=False, anio_fe=True):
        P = pd.get_dummies(m["cod_prov"], dtype=float)
        parts = [P.values]
        if anio_fe:
            A = pd.get_dummies(m["anio"], dtype=float).iloc[:, 1:]
            parts.append(A.values)
        if tend:
            t = (m["anio"] - m["anio"].mean()).values[:, None]
            parts.append(P.values * t)
        D = np.hstack(parts)
        Q, R = np.linalg.qr(D)
        rk = int((np.abs(np.diag(R)) > 1e-8 * np.abs(R).max()).sum())
        U, s, _ = np.linalg.svd(D, full_matrices=False)
        self.Q = U[:, s > 1e-8 * s.max()]
        self.k = self.Q.shape[1]
        self.cl = pd.factorize(m["cod_prov"])[0]
        self.G = int(self.cl.max() + 1)
        self.n = len(m)

    def r(self, a):
        a = np.asarray(a, float)
        return a - self.Q @ (self.Q.T @ a)


def _csum(cl, G, a):
    out = np.zeros((G,) + a.shape[1:])
    np.add.at(out, cl, a)
    return out


def iv(yt, Xt, Zt, fe: FE):
    """2SLS sobre variables ya residualizadas (FWL). Devuelve dict con beta, V (cluster CR1), e, xhat."""
    yt = np.asarray(yt, float).reshape(-1)
    Xt = np.asarray(Xt, float).reshape(len(yt), -1)
    Zt = np.asarray(Zt, float).reshape(len(yt), -1)
    PZ = Zt @ np.linalg.pinv(Zt.T @ Zt) @ Zt.T
    Xh = PZ @ Xt
    A = np.linalg.inv(Xh.T @ Xt)
    b = A @ (Xh.T @ yt)
    e = yt - Xt @ b
    sc = _csum(fe.cl, fe.G, Xh * e[:, None])
    G, n, K = fe.G, fe.n, fe.k + Xt.shape[1]
    f = G / (G - 1) * (n - 1) / (n - K)
    V = f * A @ (sc.T @ sc) @ A.T
    return dict(b=b, V=V, e=e, Xh=Xh, A=A, sc=sc, f=f, se=np.sqrt(np.diag(V)))


def tp(t, G):
    return 2 * stats.t.sf(abs(t), G - 1)


def primera_etapa(xt, Zt, fe: FE):
    """F cluster-robusto (Wald) de los instrumentos excluidos en la primera etapa."""
    Zt = np.asarray(Zt, float).reshape(len(xt), -1)
    pi = np.linalg.lstsq(Zt, xt, rcond=None)[0]
    u = xt - Zt @ pi
    A = np.linalg.inv(Zt.T @ Zt)
    sc = _csum(fe.cl, fe.G, Zt * u[:, None])
    G, n = fe.G, fe.n
    f = G / (G - 1) * (n - 1) / (n - fe.k - Zt.shape[1])
    V = f * A @ (sc.T @ sc) @ A.T
    F = float(pi @ np.linalg.solve(V, pi) / len(pi))
    return dict(F=F, pi=pi, se=np.sqrt(np.diag(V)), r2p=float(1 - (u @ u) / (xt @ xt)))


# ----------------------------------------------------------------- Wild cluster bootstrap (WRE, Webb)
WEBB = np.array([-np.sqrt(1.5), -1, -np.sqrt(.5), np.sqrt(.5), 1, np.sqrt(1.5)])


def wcb_wre(y, x, z, fe: FE, beta0=0.0, B=9999, seed=SEED, chunk=1000):
    """Bootstrap-t restringido (WRE, Davidson-MacKinnon 2010; Roodman et al. 2019) con pesos de Webb de
    6 puntos por cluster y 2SLS de un instrumento. Devuelve t observado y p (dos colas, cola derecha)."""
    yt, xt, zt = fe.r(y), fe.r(x), fe.r(z)
    r = iv(yt, xt, zt, fe)
    t_obs = (r["b"][0] - beta0) / r["se"][0]
    u1 = yt - beta0 * xt                 # residuo estructural restringido (ya sin FE: FWL)
    u1 = fe.r(u1)
    pi = (zt @ xt) / (zt @ zt)
    v = xt - zt * pi                    # residuo de la forma reducida de x (no restringido)
    rng = np.random.default_rng(seed)
    tb = np.empty(B)
    done = 0
    G, n, K = fe.G, fe.n, fe.k + 1
    f = G / (G - 1) * (n - 1) / (n - K)
    while done < B:
        m = min(chunk, B - done)
        w = WEBB[rng.integers(0, 6, size=(G, m))][fe.cl]            # n x m (mismo peso en el cluster)
        x_s = zt[:, None] * pi + v[:, None] * w
        y_s = beta0 * x_s + u1[:, None] * w
        x_s = x_s - fe.Q @ (fe.Q.T @ x_s)
        y_s = y_s - fe.Q @ (fe.Q.T @ y_s)
        den = zt @ x_s
        b = (zt @ y_s) / den
        e = y_s - x_s * b
        # varianza cluster IV con xhat = zt * (zt'x/zt'zt)
        xh = zt[:, None] * (den / (zt @ zt))[None, :]
        sc = _csum(fe.cl, G, xh * e)
        var = f * (sc ** 2).sum(0) / (xh * x_s).sum(0) ** 2
        tb[done:done + m] = (b - beta0) / np.sqrt(var)
        done += m
    p2 = float((np.sum(np.abs(tb) >= abs(t_obs)) + 1) / (B + 1))
    pr = float((np.sum(tb >= t_obs) + 1) / (B + 1))
    return dict(t=float(t_obs), p2=p2, p_right=pr, B=B)


def ar_set(yt, xt, zt, fe: FE, grid):
    """Conjunto de confianza de Anderson-Rubin (cluster) por inversión en rejilla (nivel 5 %, t(G-1))."""
    crit = stats.t.ppf(0.975, fe.G - 1)
    ok = []
    for b0 in grid:
        r = iv(yt - b0 * xt, zt.reshape(-1, 1) * 0 + zt.reshape(-1, 1), zt, fe)   # reducida de (y-b0 x) sobre z
        # iv con X=Z e instrumento Z equivale a MCO de (y-b0 x) sobre z
        if abs(r["b"][0] / r["se"][0]) <= crit:
            ok.append(b0)
    return (float(min(ok)), float(max(ok))) if ok else (np.nan, np.nan)


# ----------------------------------------------------------------- Hansen J, Rotemberg, BHJ, AKM0
def hansen_j(yt, xt, Zt, fe: FE):
    Zt = np.asarray(Zt, float)
    L = Zt.shape[1]
    r1 = iv(yt, xt, Zt, fe)
    e = r1["e"]
    n = fe.n

    def S(e_):
        sc = _csum(fe.cl, fe.G, Zt * e_[:, None])
        return sc.T @ sc / n
    W = np.linalg.pinv(S(e))
    xz = Zt.T @ xt.reshape(-1, 1)
    b = float((xz.T @ W @ (Zt.T @ yt)).item() / (xz.T @ W @ xz).item())
    e2 = yt - b * xt
    gbar = Zt.T @ e2 / n
    W2 = np.linalg.pinv(S(e2))
    J = float(n * gbar @ W2 @ gbar)
    sar = float(n * (e2 @ Zt @ np.linalg.solve(Zt.T @ Zt, Zt.T @ e2)) / (e2 @ e2))
    return dict(J=J, p=float(stats.chi2.sf(J, L - 1)), df=L - 1, b_gmm=b,
                sargan=sar, p_sargan=float(stats.chi2.sf(sar, L - 1)))


def rotemberg(m, fe: FE, yvar, xvar="x"):
    Zg = np.column_stack([fe.r(m[f"zg_{k}"].values) for k in GRUPOS])
    xt, yt = fe.r(m[xvar].values), fe.r(m[yvar].values)
    num = Zg.T @ xt
    alpha = num / num.sum()
    bg = (Zg.T @ yt) / num
    out = pd.DataFrame({"grupo": GRUPOS, "alpha": alpha, "beta_g": bg, "cuota_media": [m[f"sh_{k}"].mean() for k in GRUPOS]})
    out["F_g"] = [primera_etapa(xt, Zg[:, [j]], fe)["F"] for j in range(len(GRUPOS))]
    return out


def bhj(m, fe: FE, yvar, xvar="x", fe_grupo=False, fe_anio=True):
    """IV a nivel de shock (BHJ): (g,t) con exposición e_igt = cuota_ig/pob_{i,t-1}; promedios ponderados
    por exposición de los residuos (sin FE provincia-año) de y y x; shock = variación nacional del stock."""
    yt, xt = fe.r(m[yvar].values), fe.r(m[xvar].values)
    rows = []
    for k in GRUPOS:
        e = 100 * m[f"sh_{k}"].values / m["pop_l"].values
        df = pd.DataFrame({"anio": m["anio"], "e": e, "ey": e * yt, "ex": e * xt})
        a = df.groupby("anio").sum()
        sh = m.groupby("anio")[f"shock_{k}"].first()
        rows.append(pd.DataFrame({"g": k, "anio": a.index, "w": a["e"].values, "y": (a["ey"] / a["e"]).values,
                                  "x": (a["ex"] / a["e"]).values, "s": sh.loc[a.index].values}))
    s = pd.concat(rows, ignore_index=True)
    s = s[s["w"] > 0]
    cols = [np.ones(len(s))]
    if fe_anio:
        cols = [pd.get_dummies(s["anio"], dtype=float).iloc[:, 1:].values, np.ones((len(s), 1))]
    if fe_grupo:
        cols.append(pd.get_dummies(s["g"], dtype=float).iloc[:, 1:].values)
    C = np.hstack([c.reshape(len(s), -1) for c in cols])
    sw = np.sqrt(s["w"].values)[:, None]
    Cw = C * sw
    Pc = np.eye(len(s)) - Cw @ np.linalg.pinv(Cw)
    yy, xx, ss = (Pc @ (s[c].values * sw[:, 0]) for c in ("y", "x", "s"))
    b = (ss @ yy) / (ss @ xx)
    e = yy - b * xx
    cl = pd.factorize(s["g"])[0]
    G = cl.max() + 1
    sc = np.bincount(cl, weights=ss * e, minlength=G)
    V = (G / (G - 1)) * (sc ** 2).sum() / (ss @ xx) ** 2
    return dict(b=float(b), se=float(np.sqrt(V)), p=float(tp(b / np.sqrt(V), G)), G=int(G), n=len(s))


def akm0(m, fe: FE, yvar, xvar="x"):
    """EE tipo AKM (exposure-robust, agrupando por grupo-shock a lo largo del tiempo): aproximación AKM0, sin la
    región de similitud de cuotas de AKM(2019) completo. V = sum_g (sum_it zg_it e_it)^2 / (z~'x)^2."""
    yt, xt, zt = fe.r(m[yvar].values), fe.r(m[xvar].values), fe.r(m["z"].values)
    r = iv(yt, xt, zt, fe)
    e = r["e"]
    sg = np.array([(fe.r(m[f"zg_{k}"].values) * e).sum() for k in GRUPOS])
    V = (sg ** 2).sum() / (zt @ xt) ** 2
    se = float(np.sqrt(V))
    G = len(GRUPOS)
    return dict(b=float(r["b"][0]), se=se, p_norm=float(2 * stats.norm.sf(abs(r["b"][0]) / se)),
                p_t=float(tp(r["b"][0] / se, G)), G=G)
