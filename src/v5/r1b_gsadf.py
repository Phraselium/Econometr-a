"""R1b-3 (BK-023): GSADF con tamaño corregido y contraste frente a fundamentales. Capa C4.

Un contraste de exuberancia detecta comportamiento explosivo de una serie (o de un cociente), no una burbuja:
no identifica por qué se separa el precio de un valor de referencia ni predice un colapso.

Corrección de tamaño: valores críticos por bootstrap recursivo de residuos bajo la nula de raíz unitaria con la
dinámica de Δy ESTIMADA (AR(p) por BIC, p<=4, intercepto), en lugar del paseo aleatorio iid de M7 (que sobre-rechazaba
con Δy autocorrelacionada: 12,7 % con phi=0,5). El tamaño del procedimiento corregido se comprueba por Monte Carlo.
Sin red. SEED=20261010.
"""
import os

for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS"):
    os.environ.setdefault(_v, "1")
import json  # noqa: E402
import math  # noqa: E402
import sys  # noqa: E402
from pathlib import Path  # noqa: E402

import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402

RAIZ = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(RAIZ / "src"))
import econ_utils  # noqa: E402
import holdout  # noqa: E402

import warnings  # noqa: E402

warnings.filterwarnings("ignore", category=RuntimeWarning)
SEED = 20261010
SMOKE = "--smoke" in sys.argv
NBOOT = 49 if SMOKE else 499
OUT = RAIZ / "output/v5/R1B" / ("smoke" if SMOKE else "")
(OUT / "tablas").mkdir(parents=True, exist_ok=True)
REG = econ_utils.Registry(OUT / "registro_gsadf.csv")


# --------------------------------------------------------- núcleo GSADF (misma implementación que output/v4/M7)
def _prefijos(y):
    dy = np.diff(y)
    m = np.column_stack([np.ones_like(y[1:-1]), y[1:-1], dy[:-1], dy[1:]])
    p = np.zeros((len(m) + 1, 4, 4))
    p[1:] = np.cumsum(m[:, :, None] * m[:, None, :], axis=0)
    return p, len(m)


def _ventanas(n, w0):
    return np.triu_indices(n, k=w0 - 1)


def bsadf_path(y, w0, ab=None):
    p, n = _prefijos(y)
    a, b = ab if ab is not None else _ventanas(n, w0)
    s = p[b + 1] - p[a]
    xtx, xty = s[:, :3, :3], s[:, :3, 3]
    inv = np.linalg.inv(xtx + 1e-12 * np.eye(3))
    beta = np.einsum("nij,nj->ni", inv, xty)
    ssr = s[:, 3, 3] - np.einsum("ni,ni->n", beta, xty)
    s2 = np.maximum(ssr, 1e-300) / ((b - a + 1) - 3)
    t = beta[:, 1] / np.sqrt(s2 * inv[:, 1, 1])
    m = np.full((n, n), -np.inf)
    m[b, a] = t
    return m.max(axis=1)


def parametros(T):
    r0 = 0.01 + 1.8 / math.sqrt(T)
    w0 = max(int(math.floor(r0 * T)), 8)
    return r0, w0, T - 2, math.ceil(math.log(T))


def ar_fit(dy, pmax=4):
    """AR(p) con intercepto para Δy; p por BIC. Devuelve (const, phi, residuos centrados, p)."""
    best = None
    for p in range(0, pmax + 1):
        yy = dy[p:]
        X = np.column_stack([np.ones(len(yy))] + [dy[p - j - 1: len(dy) - j - 1] for j in range(p)])
        b = np.linalg.lstsq(X, yy, rcond=None)[0]
        e = yy - X @ b
        bic = len(yy) * math.log((e ** 2).mean()) + (p + 1) * math.log(len(yy))
        if best is None or bic < best[0]:
            best = (bic, p, b, e)
    _, p, b, e = best
    return b[0], b[1:], e - e.mean(), p


def sim_nula(y0, dy_ini, c, phi, e_pool, T, rng):
    p = len(phi)
    dy = np.empty(T - 1)
    dy[:p] = dy_ini[:p]
    ee = rng.choice(e_pool, size=T - 1)
    for t in range(p, T - 1):
        dy[t] = c + (phi @ dy[t - p:t][::-1] if p else 0.0) + ee[t]
    return np.concatenate([[y0], y0 + np.cumsum(dy)])


def episodios(sobre, L, off=2):
    eps, i, n = [], 0, len(sobre)
    while i < n:
        if sobre[i]:
            j = i
            while j + 1 < n and sobre[j + 1]:
                j += 1
            if j - i + 1 >= L:
                eps.append((i + off, j + off))
            i = j + 1
        else:
            i += 1
    return eps


def gsadf_corr(y, nboot, seed):
    T = len(y)
    r0, w0, n, L = parametros(T)
    ab = _ventanas(n, w0)
    bs = bsadf_path(y, w0, ab)
    gs = float(bs[w0 - 1:].max())
    dy = np.diff(y)
    c, phi, e, p = ar_fit(dy)
    rng = np.random.default_rng(seed)
    paths = np.empty((nboot, n))
    for i in range(nboot):
        paths[i] = bsadf_path(sim_nula(y[0], dy, c, phi, e, T, rng), w0, ab)
    bmax = paths[:, w0 - 1:].max(axis=1)
    cv_path = np.quantile(paths, 0.95, axis=0)
    sobre = np.zeros(n, bool)
    sobre[w0 - 1:] = bs[w0 - 1:] > cv_path[w0 - 1:]
    return dict(T=T, gsadf=gs, cv95=float(np.quantile(bmax, .95)), p=float((1 + (bmax >= gs).sum()) / (nboot + 1)),
                ar_p=p, phi1=float(phi[0]) if p else 0.0, eps=episodios(sobre, L), bsadf=bs, cv_path=cv_path, L=L)


def bh(p):
    m = len(p)
    o = np.argsort(p)
    adj = np.minimum.accumulate((p[o] * m / np.arange(1, m + 1))[::-1])[::-1]
    out = np.empty(m)
    out[o] = np.minimum(adj, 1.0)
    return out


# --------------------------------------------------------- tamaño (Monte Carlo)
def tamano(R, nb_in, T=78):
    rng = np.random.default_rng(SEED + 9)
    r0, w0, n, _ = parametros(T)
    ab = _ventanas(n, w0)
    stat = lambda y: float(bsadf_path(y, w0, ab)[w0 - 1:].max())  # noqa: E731
    nul = np.array([stat(np.cumsum(rng.standard_normal(T))) for _ in range(1000)])
    cv_iid = float(np.quantile(nul, .95))
    out = {"T": T, "R": R, "nboot_interno": nb_in, "cv95_iid": cv_iid}
    for phi in (0.0, 0.3, 0.5):
        rej_iid = rej_c = 0
        for r in range(R):
            e = rng.standard_normal(T)
            d = np.zeros(T)
            for t in range(1, T):
                d[t] = phi * d[t - 1] + e[t]
            y = np.cumsum(d)
            rej_iid += stat(y) > cv_iid
            g = gsadf_corr(y, nb_in, SEED + 1000 + r)
            rej_c += g["p"] <= 0.05
        out[f"phi{phi}"] = {"rechazo_vc_iid": rej_iid / R, "rechazo_bootstrap_AR": rej_c / R}
        REG.log("verif", f"tamano_phi{phi}", "tamaño GSADF T=78: vc iid frente a bootstrap AR(p) estimado", "", "", R, np.nan, np.nan, np.nan,
                coef_interes=rej_c / R, notas=json.dumps(out[f"phi{phi}"]))
    return out


# --------------------------------------------------------- series
def tramo_continuo(p):
    per = pd.PeriodIndex([f"{t[:4]}Q{t[-1]}" for t in p.index], freq="Q")
    pos = np.array([q.ordinal for q in per])
    tramos = np.split(np.arange(len(p)), np.where(np.diff(pos) != 1)[0] + 1)
    return p.iloc[max(tramos, key=len)]


def factor_anualidad(i_pct, anios=25):
    i = i_pct / 100 / 12
    n = anios * 12
    return i / (1 - (1 + i) ** (-n))


def construir_series(nq, pan):
    n = nq.set_index("trimestre")[["ipv", "p_tasado", "ipc_alquiler", "renta_hog", "tipo_hip", "tipo_hip_interp"]].dropna(
        subset=["ipv", "p_tasado", "ipc_alquiler", "renta_hog", "tipo_hip"])
    interp = bool(n.tipo_hip_interp.astype(bool).any())
    rb = n.loc["2015Q1":"2015Q4", ["ipv", "p_tasado", "ipc_alquiler", "renta_hog"]].mean()
    nb = n[["ipv", "p_tasado", "ipc_alquiler", "renta_hog"]] / rb * 100
    S = []   # (territorio, familia, medida, serie)
    for pn, P in (("IPV", nb.ipv), ("valor tasado", nb.p_tasado)):
        S.append(("Nacional", "fundamentales", f"precio/renta: {pn} / renta del hogar", np.log(P / nb.renta_hog)))
        S.append(("Nacional", "fundamentales", f"precio/alquiler: {pn} / IPC alquiler", np.log(P / nb.ipc_alquiler)))
        # capitalización del alquiler: P* = R / (tipo hipotecario - g + prima); g=2 %, prima=3 pp (principal)
        c = (n.tipo_hip - 2.0 + 3.0) / 100
        S.append(("Nacional", "fundamentales", f"precio frente a valor de descuento del alquiler (tipo, g=2 %, prima 3 pp): {pn}",
                  np.log(P / nb.ipc_alquiler) + np.log(c)))
        # asequibilidad: P* proporcional a renta / factor de anualidad hipotecaria (25 años) al tipo hipotecario
        S.append(("Nacional", "fundamentales", f"precio frente a valor de cuota hipotecaria constante sobre renta: {pn}",
                  np.log(P / nb.renta_hog) + np.log(factor_anualidad(n.tipo_hip))))
        S.append(("Nacional", "referencia", f"nivel: {pn}", np.log(P)))
    for prima in (2.0, 4.0):
        for pn, P in (("IPV", nb.ipv), ("valor tasado", nb.p_tasado)):
            c = (n.tipo_hip - 2.0 + prima) / 100
            S.append(("Nacional", "sensibilidad", f"precio frente a valor de descuento del alquiler (prima {prima:.0f} pp): {pn}",
                      np.log(P / nb.ipc_alquiler) + np.log(c)))
    for c_ in sorted(pan.ccaa.unique()):
        p = pan[pan.ccaa == c_].set_index("trimestre")[["ipv", "p_tasado", "ipc_alquiler"]].dropna()
        p = tramo_continuo(p)
        pb = p / p.mean() * 100
        S.append((c_, "ccaa", "precio/alquiler: IPV / IPC alquiler", np.log(pb.ipv / pb.ipc_alquiler)))
        S.append((c_, "ccaa", "precio/alquiler: valor tasado / IPC alquiler", np.log(pb.p_tasado / pb.ipc_alquiler)))
    return S, interp


def solapa(a, b):
    return any(not (e1 < s2 or e2 < s1) for s1, e1 in a for s2, e2 in b)


def main():
    nq = holdout.load_full("nacional_q_v2", "R1b-BK023")
    pan = pd.read_csv(RAIZ / "data/processed/panel_ccaa_q.csv")
    S, interp = construir_series(nq, pan)
    old = pd.read_csv(RAIZ / "output/v4/M7/tablas/gsadf_resultados.csv")
    filas = []
    for k, (terr, fam, med, s) in enumerate(S):
        r = gsadf_corr(s.to_numpy(), NBOOT, SEED + 500 + k)
        fe = list(s.index)
        eps = [f"{fe[a]}-{fe[b]}" for a, b in r["eps"]]
        o = old[(old.territorio == terr) & (old.medida == med)]
        eps_old = [] if o.empty or not isinstance(o.episodios_bsadf.iloc[0], str) else o.episodios_bsadf.iloc[0].split(";")
        eps_old_idx = [(fe.index(x.split("-")[0]), fe.index(x.split("-")[1])) for x in eps_old if x.split("-")[0] in fe and x.split("-")[1] in fe]
        surv = [f"{fe[a]}-{fe[b]}" for (a, b) in eps_old_idx if solapa([(a, b)], r["eps"])]
        filas.append(dict(territorio=terr, familia=fam, medida=med, T=r["T"], ini=fe[0], fin=fe[-1], gsadf=r["gsadf"], cv95_corr=r["cv95"],
                          p_corr=r["p"], ar_p=r["ar_p"], phi1=r["phi1"], gsadf_M7=float(o.gsadf.iloc[0]) if len(o) else np.nan,
                          cv95_M7_iid=float(o.cv95_mc.iloc[0]) if len(o) else np.nan, p_M7=float(o.p_mc.iloc[0]) if len(o) else np.nan,
                          episodios_corregidos=";".join(eps), episodios_M7_iid=";".join(eps_old), episodios_M7_que_sobreviven=";".join(surv),
                          capa="C4", tipo_hip_interpolada=interp if fam != "ccaa" else False))
    df = pd.DataFrame(filas)
    df["p_holm"] = np.nan
    df["p_bh"] = np.nan
    for f in df.familia.unique():
        m = df.familia == f
        h = econ_utils.holm({str(i): p for i, p in zip(df.index[m], df.p_corr[m])})
        df.loc[m, "p_holm"] = [h[str(i)] for i in df.index[m]]
        df.loc[m, "p_bh"] = bh(df.p_corr[m].to_numpy())
    df["exuberancia_bh05"] = df.p_bh < 0.05
    df.to_csv(OUT / "tablas/gsadf_corregido.csv", index=False)
    for _, f in df.iterrows():
        REG.log("gsadf-corr", f"gsadf_{f.territorio}_{f.medida}", "GSADF ADF(1); vc bootstrap AR(p) estimado", f.ini, f.fin, int(f["T"]),
                np.nan, np.nan, np.nan, coef_interes=f.gsadf, p_interes=f.p_corr, notas=f"cv95={f.cv95_corr:.2f}; BH={f.p_bh:.3f}; Holm={f.p_holm:.3f}; episodios={f.episodios_corregidos or 'ninguno'}")
    tam = tamano(40 if SMOKE else 200, 49 if SMOKE else 99)
    (OUT / "tablas/gsadf_tamano.json").write_text(json.dumps(tam, ensure_ascii=False, indent=1))
    REG.flush()
    print(df[["territorio", "medida", "gsadf", "cv95_corr", "cv95_M7_iid", "p_corr", "p_bh", "episodios_corregidos", "episodios_M7_que_sobreviven"]].to_string())
    print(json.dumps(tam, indent=1))


if __name__ == "__main__":
    main()
