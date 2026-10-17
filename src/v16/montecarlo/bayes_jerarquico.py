"""Modelo jerárquico normal-normal sección ⊂ municipio ⊂ provincia (adenda punto 12), muestreador Gibbs propio.

Implementación declarada: Gibbs con la varianza de sección marginalizada para μ, u_p, v_m y rejilla (griddy Gibbs)
para las tres desviaciones típicas con prior semi-normal(0, s); μ ~ normal(0, s). PyMC no se usa.
Solo se lee la ESTRUCTURA (códigos de sección) de base_alquiler (entrenamiento); los efectos se simulan.
Uso: python bayes_jerarquico.py [R_nulo] [R_resto]
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from src.v16.montecarlo import _comun_series as C  # noqa: E402

S0 = 0.07            # familia Q1 (log del alquiler)
NPROV, CAP_MUN, CAP_SEC = 8, 25, 12
GRID = np.exp(np.linspace(np.log(1e-4), np.log(0.5), 90))
ITER, BURN = 1200, 300


def estructura():
    d = pd.read_parquet(C.RAIZ / "data" / "processed" / "v16" / "entrenamiento" / "base_alquiler.parquet",
                        columns=["territorio_codigo", "nivel", "variable"])
    d = d[(d.nivel == "seccion") & (d.variable == "serpavi_alquiler_m2_mediana")]
    cod = pd.Series(d.territorio_codigo.astype(str).unique())
    g = cod.groupby([cod.str[:2], cod.str[:5]]).size().reset_index(name="n")
    g.columns = ["prov", "mun", "n"]
    rng = C.rng(7, 0)
    provs = rng.choice(g.prov.unique(), NPROV, replace=False)
    mun_p, sec_m = [], []
    for ip, p in enumerate(provs):
        gm = g[g.prov == p]
        gm = gm.iloc[rng.permutation(len(gm))[:CAP_MUN]]
        for n in gm.n.values:
            sec_m.append(min(int(n), CAP_SEC)); mun_p.append(ip)
    mun_p = np.array(mun_p); sec_m = np.array(sec_m)
    sec_mun = np.repeat(np.arange(len(sec_m)), sec_m)
    return mun_p, sec_mun


def semi(rng, s, n):
    return np.abs(rng.normal(0, s, n))


def gibbs(rng, y, se, mun_p, sec_mun, s):
    S, M, P = len(y), len(mun_p), mun_p.max() + 1
    sec_p = mun_p[sec_mun]
    mu, u, v = 0.0, np.zeros(P), np.zeros(M)
    tu, tv, tw = 0.02, 0.02, 0.02
    se2 = se ** 2
    mus, thetas, mun_eff, prov_eff = [], [], [], []
    lg = np.log(GRID)
    for it in range(ITER):
        d = se2 + tw ** 2
        # mu
        # mu | v, tu con u_p marginalizado (mejora la mezcla entre mu y los efectos de provincia)
        Pp = np.bincount(sec_p, 1 / d, P)
        ybar = np.bincount(sec_p, (y - v[sec_mun]) / d, P) / Pp
        wp = 1 / (1 / Pp + tu ** 2)
        prec = 1 / s ** 2 + wp.sum()
        mu = rng.normal((wp * ybar).sum() / prec, prec ** -0.5)
        # u_p
        r = y - mu - v[sec_mun]
        pu = 1 / tu ** 2 + np.bincount(sec_p, 1 / d, P)
        u = rng.normal(np.bincount(sec_p, r / d, P) / pu, pu ** -0.5)
        # v_m
        r = y - mu - u[sec_p]
        pv = 1 / tv ** 2 + np.bincount(sec_mun, 1 / d, M)
        v = rng.normal(np.bincount(sec_mun, r / d, M) / pv, pv ** -0.5)
        # desviaciones (rejilla con jacobiano de log-escala): prior semi-normal(0, s)
        def muestra(ll):
            w = np.exp(ll - ll.max()); w /= w.sum()
            return GRID[rng.choice(len(GRID), p=w)]
        tu = muestra(-P * lg - (u ** 2).sum() / (2 * GRID ** 2) - GRID ** 2 / (2 * s ** 2) + lg)
        tv = muestra(-M * lg - (v ** 2).sum() / (2 * GRID ** 2) - GRID ** 2 / (2 * s ** 2) + lg)
        e = y - mu - u[sec_p] - v[sec_mun]
        dg = se2[:, None] + GRID[None, :] ** 2
        ll = -0.5 * (np.log(dg) + e[:, None] ** 2 / dg).sum(0) - GRID ** 2 / (2 * s ** 2) + lg
        tw = muestra(ll)
        # w_s | resto
        d = se2 + tw ** 2
        pw = 1 / se2 + 1 / tw ** 2
        w = rng.normal((e / se2) / pw, pw ** -0.5)
        if it >= BURN:
            mus.append(mu)
            thetas.append(mu + u[sec_p] + v[sec_mun] + w)
            mun_eff.append(mu + u[mun_p] + v)
            prov_eff.append(mu + u)
    return np.array(mus), np.array(thetas), np.array(mun_eff), np.array(prov_eff)


def una(k, esc, escala_prior, mun_p, sec_mun):
    rng = C.rng(7, 1000 + k)
    s_true = S0
    M, S = len(mun_p), len(sec_mun)
    P = mun_p.max() + 1
    if esc == "prior":
        mu0 = rng.normal(0, S0); tu0, tv0, tw0 = semi(rng, S0, 3)
    elif esc == "no_nulo":
        mu0, tu0, tv0, tw0 = -0.05, 0.02, 0.03, 0.04
    elif esc == "nulo":
        mu0, tu0, tv0, tw0 = 0.0, 0.02, 0.03, 0.04
    elif esc == "homogeneo":
        mu0, tu0, tv0, tw0 = -0.05, 0.005, 0.005, 0.005
    u0 = rng.normal(0, tu0, P); v0 = rng.normal(0, tv0, M); w0 = rng.normal(0, tw0, S)
    sec_p = mun_p[sec_mun]
    th = mu0 + u0[sec_p] + v0[sec_mun] + w0
    se = 0.06 * np.exp(rng.normal(0, 0.5, S))
    y = th + se * rng.standard_normal(S)
    mus, thetas, meff, peff = gibbs(rng, y, se, mun_p, sec_mun, S0 * escala_prior)
    lo, hi = np.quantile(mus, [0.025, 0.975])
    cm = lo <= mu0 <= hi
    tl, tu_ = np.quantile(thetas, [0.025, 0.975], axis=0)
    cs = ((tl <= th) & (th <= tu_)).mean()
    ml, mh = np.quantile(meff, [0.025, 0.975], axis=0)
    mtrue = mu0 + u0[mun_p] + v0
    cmu = ((ml <= mtrue) & (mtrue <= mh)).mean()
    pl, ph = np.quantile(peff, [0.025, 0.975], axis=0)
    ptrue = mu0 + u0
    cp = ((pl <= ptrue) & (ptrue <= ph)).mean()
    return cm, cs, cmu, cp, mus.mean() - mu0, (mus.mean() - mu0) ** 2, (lo > 0) | (hi < 0)


def main(Rn=2000, Rr=1000):
    mun_p, sec_mun = estructura()
    plan = [("prior", 1.0, Rr), ("no_nulo", 1.0, Rr), ("nulo", 1.0, Rn), ("homogeneo", 1.0, Rr),
            ("no_nulo", 0.5, Rr // 2), ("no_nulo", 2.0, Rr // 2)]
    filas = []
    for i, (esc, ep, R) in enumerate(plan):
        a = np.array(C.paralelo(una, [(i * 10 ** 5 + k, esc, ep, mun_p, sec_mun) for k in range(R)]), dtype=float)
        filas.append({"escenario": esc, "escala_prior": ep, "R": R, "cob_mu": a[:, 0].mean(), "cob_seccion": a[:, 1].mean(),
                      "cob_municipio": a[:, 2].mean(), "cob_provincia": a[:, 3].mean(), "sesgo_mu": a[:, 4].mean(),
                      "rmse_mu": np.sqrt(a[:, 5].mean()), "P(0 fuera IC95 mu)": a[:, 6].mean()})
    t = pd.DataFrame(filas)
    prin = t[t.escala_prior == 1.0]
    cols = ["cob_mu", "cob_seccion", "cob_municipio", "cob_provincia"]
    mal = [f"{r.escenario} {c}={r[c]:.3f}" for _, r in prin.iterrows() for c in cols if not (C.COB_MIN <= r[c] <= 0.97)]
    glob = {"veredicto": "APTO" if not mal else "NO APTO", "fallos": mal}
    r = C.resultado_base("bayes_jerarquico", "Modelo jerárquico (adenda punto 12)",
                         {"provincias": int(mun_p.max() + 1), "municipios": len(mun_p), "secciones": len(sec_mun)},
                         "normal-normal 3 niveles, Gibbs propio (griddy para desviaciones)")
    r["estimacion"] = {"cobertura_mu_min": float(prin.cob_mu.min()), "cobertura_seccion_min": float(prin.cob_seccion.min()),
                       "cobertura_municipio_min": float(prin.cob_municipio.min()), "cobertura_provincia_min": float(prin.cob_provincia.min()),
                       "sesgo_mu_no_nulo": float(prin[prin.escenario == "no_nulo"].sesgo_mu.iloc[0]),
                       "rmse_mu_no_nulo": float(prin[prin.escenario == "no_nulo"].rmse_mu.iloc[0]),
                       "P_0_fuera_IC_bajo_nulo": float(prin[prin.escenario == "nulo"]["P(0 fuera IC95 mu)"].iloc[0]),
                       "potencia_mu_no_nulo": float(prin[prin.escenario == "no_nulo"]["P(0 fuera IC95 mu)"].iloc[0])}
    r["ic95"] = C.ic_binomial(float(prin.cob_mu.mean()), int(prin.R.min()))
    r["diagnosticos"] = {"veredicto": glob, "R_nulo": Rn, "R_resto": Rr, "criterio": "cobertura de IC creíble 95 % en [0,92; 0,97] (encargo, punto 6)",
                         "iter": ITER, "burn": BURN, "implementacion": "Gibbs propio; PyMC no usado"}
    r["notas"] = ["En el escenario «prior» la cobertura es una calibración bayesiana exacta si el muestreador es correcto.",
                  "Sensibilidad s×0,5 y s×2 informada con verdad fija (no se usa para el veredicto)."]
    md = (f"## Resultados\n\n" + t.round(4).to_markdown(index=False) + f"\n\n**Veredicto: {glob['veredicto']}** {'; '.join(glob['fallos'])}\n")
    C.escribir_salidas("bayes_jerarquico", r, t, md)
    print(t.round(3).to_string(), glob)


if __name__ == "__main__":
    main(*[int(x) for x in sys.argv[1:]])
