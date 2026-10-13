"""V8-F3 grupo B: validacion por Monte Carlo (SOLO datos simulados) de src/v8/herramientas/{regimenes,dfm,lp,dominancia,
permutacion,shap_grupos,multiverso}. SEED=20261010, un hilo, determinista.

Uso:  python3 src/v8/f3_montecarlo_otros.py --bloque {ms12,ms23,msbic,resto}   (escribe output/v8/F3/otros/_parcial_<bloque>.csv)
      python3 src/v8/f3_montecarlo_otros.py --merge   (une parciales, escribe montecarlo.csv, validacion.md y resultado.json)
"""
from __future__ import annotations

import argparse
import itertools
import json
import os
import sys
import time
import warnings
from pathlib import Path

for v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS"):
    os.environ[v] = "1"
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "src"))
from src.v8.herramientas import dfm, dominancia, lp, permutacion, regimenes, shap_grupos  # noqa: E402

warnings.filterwarnings("ignore")
SEED = 20261010
OUT = ROOT / "output" / "v8" / "F3" / "otros"
FILAS: list = []


def reg(herr, esc, metrica, valor, objetivo, cumple, reps, B="", n="", nota=""):
    FILAS.append({"herramienta": herr, "escenario": esc, "metrica": metrica, "valor": float(valor), "objetivo": objetivo,
                  "cumple": cumple, "reps": reps, "B": B, "n": n, "nota": nota})


def en(v, lo, hi):
    return bool(lo <= v <= hi)


def rng_(*k):
    return np.random.default_rng([SEED, *k])


# ----------------------------------------------------------------------------- umbral
def mc_umbral(R=300, B=299, n=120):
    for esc in ("H0_iid", "H0_heterocedastico", "H1_salto_pendiente"):
        rej, cov, gam = [], [], []
        for r in range(R):
            g = rng_(1, r)
            x, q = g.normal(size=n), g.normal(size=n)
            e = g.normal(size=n) * (np.sqrt(0.4 + x ** 2) if esc == "H0_heterocedastico" else 1.0)
            b = np.where(q > 0.0, 1.2, 0.4) if esc.startswith("H1") else 0.4
            y = 1 + b * x + e
            res = regimenes.umbral_hansen(y, np.column_stack([np.ones(n), x]), q, B=B, seed=SEED + r)
            rej.append(res["p_linealidad"] < 0.05)
            if esc.startswith("H1"):
                cov.append(res["ic_gamma"][0] <= 0.0 <= res["ic_gamma"][1])
                gam.append(res["gamma"])
        if esc.startswith("H0"):
            v = np.mean(rej)
            reg("umbral_hansen", esc, "tamaño (rechazo al 5%)", v, "[0,02;0,10]", en(v, .02, .10), R, B, n)
        else:
            v = np.mean(rej)
            reg("umbral_hansen", esc, "potencia (rechazo al 5%)", v, ">=0,80", v >= .8, R, B, n)
            reg("umbral_hansen", esc, "cobertura IC95 del umbral por inversión de LR", np.mean(cov), "[0,90;0,98]",
                en(np.mean(cov), .90, .98), R, B, n, nota="gamma verdadero = 0")
            reg("umbral_hansen", esc, "sesgo mediano del umbral", np.median(gam), "|.|<0,15", abs(np.median(gam)) < .15, R, B, n)


# ----------------------------------------------------------------------------- Bai-Perron
def mc_bp(R=250, B=199, n=120):
    for esc, rho, boot, het, shift in [("H0_iid_wild", 0, "wild", 0, 0), ("H0_heterocedastico_wild", 0, "wild", 1, 0),
                                       ("H0_AR0.5_wild", .5, "wild", 0, 0), ("H0_AR0.5_bloque", .5, "block", 0, 0),
                                       ("H1_salto1.0_wild", 0, "wild", 0, 1.0), ("H1_salto0.6_wild", 0, "wild", 0, 0.6)]:
        rej, rej1, fecha, mbic = [], [], [], []
        for r in range(R):
            g = rng_(2, r)
            e = g.normal(size=n)
            if rho:
                u = np.zeros(n)
                for t in range(n):
                    u[t] = (rho * u[t - 1] if t else 0) + e[t]
                e = u * np.sqrt(1 - rho ** 2)
            if het:
                e = e * np.r_[np.ones(n // 2) * .6, np.ones(n - n // 2) * 1.4]
            y = e + shift * (np.arange(n) >= n // 2)
            res = regimenes.bai_perron(y, max_cortes=3, B=B, seed=SEED + r, boot=boot)
            rej.append(res["p_UDmax"] < .05)
            rej1.append(res["p_supF"][0] < .05)
            mbic.append(res["m_bic"])
            if shift:
                fecha.append(abs(res["cortes"][1][0] - n // 2) if res["cortes"][1] else np.nan)
        if shift == 0:
            v = np.mean(rej)
            reg("bai_perron_boot", esc, "tamaño UDmax (5%)", v, "[0,02;0,10]", en(v, .02, .10), R, B, n)
            v1 = np.mean(rej1)
            reg("bai_perron_boot", esc, "tamaño supF(1) (5%)", v1, "[0,02;0,10]", en(v1, .02, .10), R, B, n)
            reg("bai_perron_boot", esc, "P(BIC elige >=1 corte | nula)", np.mean(np.array(mbic) > 0), "informativo", "", R, B, n)
        else:
            v = np.mean(rej)
            reg("bai_perron_boot", esc, "potencia UDmax (5%)", v, ">=0,80" if shift >= 1 else "informativo", (v >= .8) if shift >= 1 else "", R, B, n)
            reg("bai_perron_boot", esc, "error absoluto mediano de la fecha (obs.)", np.nanmedian(fecha), "informativo", "", R, B, n)


# ----------------------------------------------------------------------------- Markov switching
def sim_ms(n, mu, s2, P, g):
    k = len(mu)
    s = np.zeros(n, int)
    for t in range(1, n):
        s[t] = g.choice(k, p=P[:, s[t - 1]])
    return np.asarray(mu)[s] + np.sqrt(np.asarray(s2)[s]) * g.normal(size=n)


DGP_MS = {
    "1reg": dict(mu=[0.], s2=[1.], P=np.ones((1, 1))),
    "2reg": dict(mu=[0., 1.5], s2=[1., 2.5], P=np.array([[.95, .05], [.05, .95]])),
    "3reg": dict(mu=[-2., 0., 2.], s2=[1., 1., 1.], P=np.array([[.92, .04, .04], [.04, .92, .04], [.04, .04, .92]])),
}


def mc_ms_bic(R=30, n=250):
    for nm, d in DGP_MS.items():
        ks = []
        for r in range(R):
            y = sim_ms(n, d["mu"], d["s2"], d["P"], rng_(3, r))
            bic = {1: -2 * np.sum(-0.5 * np.log(2 * np.pi * y.var()) - 0.5) + 2 * np.log(n)}
            for k in (2, 3):
                try:
                    bic[k] = regimenes.ms_fit(y, k, search_reps=3, seed=SEED + r)["bic"]
                except Exception:
                    bic[k] = np.inf
            ks.append(min(bic, key=bic.get))
        kt = len(d["mu"])
        v = np.mean(np.array(ks) == kt)
        reg("markov_switching", f"verdadero_{nm}", "% BIC elige k verdadero", v, ">=0,70", v >= .7, R, "", n)


def mc_ms12(R=20, B=39, n=200):
    for nm in ("1reg", "2reg"):
        d = DGP_MS[nm]
        rej = []
        for r in range(R):
            y = sim_ms(n, d["mu"], d["s2"], d["P"], rng_(4, r))
            t = regimenes.ms_contraste_regimenes(y, 1, 2, B=B, search_reps=3, seed=SEED + r)
            rej.append(t["p"] < .05)
        v = np.mean(rej)
        if nm == "1reg":
            reg("markov_switching", "H0_1reg_test_1v2", "tamaño del bootstrap LR 1 vs 2 (5%)", v, "[0,02;0,10] (R pequeño: IC amplio)",
                en(v, .02, .10), R, B, n, nota=f"IC binomial 95% ~ ±{1.96 * np.sqrt(.05 * .95 / R):.2f}")
        else:
            reg("markov_switching", "H1_2reg_test_1v2", "potencia del bootstrap LR 1 vs 2 (5%)", v, ">=0,80", v >= .8, R, B, n)


def mc_ms23(R=6, B=19, n=250):
    for nm, k0 in (("2reg", 2), ("3reg", 2)):
        d = DGP_MS[nm]
        ps = []
        for r in range(R):
            y = sim_ms(n, d["mu"], d["s2"], d["P"], rng_(5, r))
            ps.append(regimenes.ms_contraste_regimenes(y, 2, 3, B=B, search_reps=2, seed=SEED + r)["p"])
        v = np.mean(np.array(ps) < .05)
        reg("markov_switching", f"{nm}_test_2v3", "rechazo bootstrap LR 2 vs 3 (5%)", v,
            "tamaño ≤0,10 (2reg) / potencia ≥0,80 (3reg)", (v <= .10) if nm == "2reg" else (v >= .8), R, B, n,
            nota="R muy pequeño: resultado INDICATIVO, no validación")


# ----------------------------------------------------------------------------- LP y LP-IV
def mc_lp(R=400, n=200):
    cob = {h: [] for h in (0, 1, 4, 8)}
    wid = {h: [] for h in cob}
    for r in range(R):
        g = rng_(6, r)
        x, e = g.normal(size=n + 50), g.normal(size=n + 50)
        y = np.zeros(n + 50)
        for t in range(1, n + 50):
            y[t] = .6 * y[t - 1] + x[t] + e[t]
        res = lp.lp(y[50:], x[50:], H=8, rezagos=2)
        for h in cob:
            row = res.iloc[h]
            cob[h].append(row.lo <= .6 ** h <= row.hi)
            wid[h].append(row.hi - row.lo)
    for h in cob:
        v = np.mean(cob[h])
        reg("lp_ols_NW", f"h={h}", "cobertura IC95", v, "[0,90;0,98]", en(v, .90, .98), R, "", n)


def mc_lpiv(R=400, n=200):
    for esc, pi in (("instrumento_fuerte", 1.0), ("instrumento_debil", 0.12)):
        cov_n = {0: [], 2: []}
        cov_ar = {0: [], 2: []}
        F = []
        acot = []
        for r in range(R):
            g = rng_(7, r, int(pi * 100))
            z = g.normal(size=n + 50)
            v = g.normal(size=n + 50)
            u = 0.7 * v + np.sqrt(1 - .49) * g.normal(size=n + 50)
            x = pi * z + v
            y = np.zeros(n + 50)
            for t in range(1, n + 50):
                y[t] = .5 * y[t - 1] + 1.0 * x[t] + u[t]
            res = lp.lp_iv(y[50:], x[50:], z[50:], H=2, rezagos=2, grid_n=1201)
            F.append(res.F_robusto.iloc[0])
            for h in (0, 2):
                row = res.iloc[h]
                tr = .5 ** h
                cov_n[h].append(row.lo <= tr <= row.hi)
                cov_ar[h].append(row.ar_lo <= tr <= row.ar_hi)
                acot.append(row.ar_acotado)
        for h in (0, 2):
            reg("lp_iv_AR", f"{esc}_h={h}", "cobertura IC normal 2SLS", np.mean(cov_n[h]), "[0,90;0,98] (referencia)", en(np.mean(cov_n[h]), .90, .98), R, "", n,
                nota=f"F robusto mediano {np.median(F):.1f}")
            reg("lp_iv_AR", f"{esc}_h={h}", "cobertura IC Anderson-Rubin", np.mean(cov_ar[h]), "[0,90;0,98]", en(np.mean(cov_ar[h]), .90, .98), R, "", n,
                nota=f"F robusto mediano {np.median(F):.1f}; % AR no acotado {100 * (1 - np.mean(acot)):.0f}")


# ----------------------------------------------------------------------------- dominancia
def mc_dominancia(R=60, n=300, B=100):
    p = 5
    S = np.eye(p)
    S[0, 1] = S[1, 0] = .8
    S[2, 3] = S[3, 2] = .6
    S[1, 2] = S[2, 1] = .3
    beta = np.array([1., .5, .8, 0., .3])
    c = S @ beta
    vy = beta @ S @ beta + 1.0
    cache = {frozenset(): 0.0}
    for r in range(1, p + 1):
        for T in itertools.combinations(range(p), r):
            cs = c[list(T)]
            cache[frozenset(T)] = float(cs @ np.linalg.solve(S[np.ix_(T, T)], cs)) / vy
    phi0 = dominancia._shapley_from_cache(cache, p)
    vif0 = np.diag(np.linalg.inv(S))
    err, cov, top, vif_err = [], [], [], []
    for r in range(R):
        g = rng_(8, r)
        X = g.multivariate_normal(np.zeros(p), S, n)
        y = X @ beta + g.normal(size=n)
        o = dominancia.shapley_r2(X, y, B=B, seed=SEED + r)
        err.append(np.abs(o.phi.values - phi0))
        cov.append((o.lo.values <= phi0) & (phi0 <= o.hi.values))
        top.append(np.argsort(-o.phi.values)[:2].tolist() == np.argsort(-phi0)[:2].tolist())
        vif_err.append(np.max(np.abs(dominancia.colinealidad(X)["vif"].values / vif0 - 1)))
        if r == 0:
            jr = dominancia.johnson_rw(X, y)
            reg("dominancia", "p=5 colineal", "|Johnson - LMG| máx (en R2)", np.max(np.abs(jr.peso.values - o.phi.values)), "<0,05", np.max(np.abs(jr.peso.values - o.phi.values)) < .05, 1, "", n)
    reg("dominancia", "p=5 colineal", "error absoluto medio de phi (R2)", np.mean(err), "<0,03", np.mean(err) < .03, R, B, n, nota=f"phi verdadero={np.round(phi0, 3).tolist()}")
    cv = np.mean(cov)
    reg("dominancia", "p=5 colineal", "cobertura IC95 bootstrap de phi", cv, "[0,90;0,98]", en(cv, .90, .98), R, B, n)
    reg("dominancia", "p=5 colineal", "% acierto en las 2 variables dominantes (orden)", np.mean(top), ">=0,80", np.mean(top) >= .8, R, B, n)
    reg("dominancia", "p=5 colineal", "error relativo máx del VIF", np.mean(vif_err), "<0,20", np.mean(vif_err) < .2, R, "", n)


# ----------------------------------------------------------------------------- permutacion de fechas
def mc_perm(R=250, n=100, n_perm=2000):
    for esc, rho, shift in (("H0_iid", 0, 0.0), ("H0_AR0.5", .5, 0.0), ("H1_ruptura_pendiente", 0, .8)):
        rej_raw, rej_t = [], []
        for r in range(R):
            g = rng_(9, r)
            x = g.normal(size=n)
            e = g.normal(size=n)
            if rho:
                u = np.zeros(n)
                for t in range(1, n):
                    u[t] = rho * u[t - 1] + e[t]
                e = u * np.sqrt(1 - rho ** 2)
            b = np.where(np.arange(n) >= n // 2, .5 + shift, .5)
            y = 1 + b * x + e
            X = np.column_stack([np.ones(n), x])
            for fabrica, lst in ((permutacion.stat_dif_coef, rej_raw), (permutacion.stat_t_dif_coef, rej_t)):
                lst.append(permutacion.permutacion_cortes(fabrica(y, X, 1), n, (n // 2,), 15, n_perm=n_perm, seed=SEED + r)["p"] < .05)
        for nm, lst in (("estadístico sin studentizar", rej_raw), ("estadístico studentizado", rej_t)):
            v = np.mean(lst)
            if esc.startswith("H0"):
                reg("permutacion_fechas", f"{esc} | {nm}", "tamaño (5%)", v, "≈0,05 ([0,02;0,10])", en(v, .02, .10), R, n_perm, n)
            else:
                reg("permutacion_fechas", f"{esc} | {nm}", "potencia (5%)", v, ">=0,80", v >= .8, R, n_perm, n)


# ----------------------------------------------------------------------------- SHAP agrupado, DFM
GR = {"F1": ["a", "b"], "F2": ["c"], "F3": ["d", "e"], "F4": ["f"]}


def dgp_shap(g, n, duro=False):
    X = pd.DataFrame(g.normal(size=(n, 6)), columns=list("abcdef"))
    if duro:  # F1 y F2 casi iguales en importancia
        y = 1.0 * X.a + 0.2 * X.b + 0.95 * X.c + 0.3 * X.d * X.e + g.normal(size=n) * .5
    else:
        y = 2 * X.a + 1.5 * X.b + np.sin(2 * X.c) + 0.7 * X.d * X.e + g.normal(size=n) * .5
    return X, y


def mc_shap(R=30, n=400, Rest=10, B=20):
    ok = []
    for r in range(R):
        X, y = dgp_shap(rng_(10, r), n)
        m = shap_grupos.modelo_lgbm(seed=SEED + r).fit(X.values, y)
        ok.append(list(shap_grupos.shap_grupos(m, X, GR)[0].index) == ["F1", "F2", "F3", "F4"])
    v = np.mean(ok)
    reg("shap_grupos", "DGP aditivo+interacción (orden verdadero F1>F2>F3>F4)", "% ranking correcto de familias", v, ">=0,90", v >= .9, R, "", n)
    for duro in (False, True):
        pc, pt, pb = [], [], []
        for r in range(Rest):
            X, y = dgp_shap(rng_(11, r), n, duro)
            e = shap_grupos.estabilidad_ranking(X, y, GR, B=B, seed=SEED + r)
            pb.append(e["pct_ranking_completo_bootstrap"])
            pt.append(e["pct_ranking_completo_pliegues"])
            pc.append(e["pct_misma_pos_bootstrap"].min())
        esc = "DGP duro (F1≈F2)" if duro else "DGP claro"
        reg("shap_grupos", esc, "% réplicas bootstrap con ranking completo igual (media)", np.mean(pb), ">=0,80 si claro; informativo si duro",
            (np.mean(pb) >= .8) if not duro else "", Rest, B, n)
        reg("shap_grupos", esc, "% pliegues temporales con ranking completo igual (media)", np.mean(pt), "informativo", "", Rest, 4, n)
    # fidelidad del sustituto y ALE vs verdad (c: sin(2c))
    X, y = dgp_shap(rng_(12, 0), n)
    m = shap_grupos.modelo_lgbm().fit(X.values, y)
    reg("shap_grupos", "arbol sustituto prof.3", "fidelidad R2", shap_grupos.sustituto(m, X)["fidelidad_r2"], "informativo", "", 1, "", n)
    ale = shap_grupos.ale_1d(m.predict, X, "c")
    reg("shap_grupos", "ALE de c vs sin(2c) centrado", "correlación", np.corrcoef(ale.ale, np.sin(2 * ale.x))[0, 1], ">=0,90",
        np.corrcoef(ale.ale, np.sin(2 * ale.x))[0, 1] >= .9, 1, "", n)


def mc_dfm(R=200):
    ok = []
    for r in range(R):
        g = rng_(13, r)
        T, N = 120, 40
        F = g.normal(size=(T, 2))
        X = F @ g.normal(size=(2, N)) + g.normal(size=(T, N))
        ok.append(dfm.bai_ng(X, 8)["k_ic2"] == 2)
    reg("dfm_baing", "T=120,N=40,r=2", "% IC_p2 elige r verdadero", np.mean(ok), ">=0,90", np.mean(ok) >= .9, R, "", 120)
    ok = []
    for r in range(R):
        g = rng_(13, r, 1)
        T, N = 120, 10
        F = g.normal(size=(T, 2))
        X = F @ g.normal(size=(2, N)) + g.normal(size=(T, N))
        ok.append(dfm.bai_ng(X, 8)["k_ic2"] == 2)
    reg("dfm_baing", "T=120,N=10,r=2", "% IC_p2 elige r verdadero", np.mean(ok), ">=0,90", np.mean(ok) >= .9, R, "", 120,
        nota="con N pequeño el criterio tiende a elegir kmax")
    # DFM-ML: R2 de la parte comun recuperado (AR(1) factor)
    err = []
    Rm = 15
    for r in range(Rm):
        g = rng_(14, r)
        T, N = 100, 8
        f = np.zeros(T)
        for t in range(1, T):
            f[t] = .7 * f[t - 1] + g.normal()
        lam = g.uniform(.5, 1.5, N)
        X = np.outer(f, lam) + g.normal(size=(T, N))
        r2_true = lam ** 2 * f.var() / (lam ** 2 * f.var() + 1)
        o = dfm.dfm_ml(X, 1)
        err.append(np.mean(np.abs(o["r2"].values[:, 0] - r2_true)))
    reg("dfm_ml", "T=100,N=8,r=1", "error absoluto medio del R2 por variable", np.mean(err), "<0,10", np.mean(err) < .10, Rm, "", 100)


def bloque_resto():
    for f in (mc_umbral, mc_bp, mc_lp, mc_lpiv, mc_dominancia, mc_perm, mc_shap, mc_dfm):
        t0 = time.time()
        f()
        print(f.__name__, round(time.time() - t0, 1), "s", flush=True)


BLOQUES = {"ms12": [mc_ms12], "ms23": [mc_ms23], "msbic": [mc_ms_bic], "resto": [bloque_resto]}


def merge():
    parc = sorted(OUT.glob("_parcial_*.csv"))
    df = pd.concat([pd.read_csv(p) for p in parc], ignore_index=True)
    df.to_csv(OUT / "montecarlo.csv", index=False)
    tiempos = {p.stem.replace("_parcial_", ""): json.loads((OUT / f"_tiempo_{p.stem.replace('_parcial_', '')}.json").read_text()) for p in parc}
    print(df.to_string())
    return df, tiempos


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--bloque", choices=list(BLOQUES))
    ap.add_argument("--merge", action="store_true")
    a = ap.parse_args()
    if a.merge:
        merge()
    else:
        t0 = time.time()
        for f in BLOQUES[a.bloque]:
            f()
        pd.DataFrame(FILAS).to_csv(OUT / f"_parcial_{a.bloque}.csv", index=False)
        (OUT / f"_tiempo_{a.bloque}.json").write_text(json.dumps({"segundos": round(time.time() - t0, 1)}))
        print(a.bloque, "ok", round(time.time() - t0, 1), "s")
