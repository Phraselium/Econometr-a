"""Validacion Monte Carlo de src/v7/panel_tools.py (V7-R2). Solo datos simulados. Determinista (SEED=20261010)."""
from __future__ import annotations

import sys
import time
from multiprocessing import Pool
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "src" / "v7"))
import panel_tools as pt  # noqa: E402

SEED = pt.SEED
N, T = 17, 78
TH = np.array([1.0, -0.5])
SCEN = {  # coint, factor, theta heterogeneo
    "A_coint_sin_factor": (True, False, False),
    "B_coint_con_factor": (True, True, False),
    "C_sin_coint_sin_factor": (False, False, False),
    "D_sin_coint_con_factor": (False, True, False),
    "E_coint_theta_heterogeneo": (True, False, True),
}
BURN = 50


def simulate(rng, coint=True, factor=False, hetero=False, N=N, T=T):
    """DGP: ECM por unidad con phi_i~U(-.4,-.1), corto plazo heterogeneo, FE en el nivel y factor comun AR(.5)."""
    TT = T + BURN
    f = np.zeros(TT)
    if factor:
        eta = rng.standard_normal(TT)
        for t in range(1, TT):
            f[t] = 0.5 * f[t - 1] + eta[t]
    phi = rng.uniform(-0.4, -0.1, N) if coint else np.zeros(N)
    ci = rng.normal(0, 2, N)
    dlt = rng.uniform(0, 0.6, (N, 2))
    lam = rng.uniform(0, 0.3, N)
    gx = rng.normal(1, 0.5, (N, 2)) if factor else np.zeros((N, 2))
    ky = rng.normal(1, 0.5, N) if factor else np.zeros(N)
    th = np.tile(TH, (N, 1)) + (rng.normal(0, 0.5, (N, 2)) if hetero else 0)
    dx = 0.05 + gx[:, None, :] * f[None, :, None] + rng.standard_normal((N, TT, 2))
    x = np.cumsum(dx, 1)
    y = np.zeros((N, TT))
    y[:, 0] = ci
    eps = rng.standard_normal((N, TT))
    dyp = np.zeros(N)
    for t in range(1, TT):
        ec = y[:, t - 1] - ci - (th * x[:, t - 1]).sum(1)
        dyt = phi * ec + (dlt * dx[:, t]).sum(1) + lam * dyp + ky * f[t] + eps[:, t]
        y[:, t] = y[:, t - 1] + dyt
        dyp = dyt
    ys = np.zeros((N, TT))  # serie estacionaria (potencia de CIPS)
    for t in range(1, TT):
        ys[:, t] = 0.7 * ys[:, t - 1] + (ky * f[t] if factor else 0) + rng.standard_normal(N)
    sl = slice(BURN, None)
    return y[:, sl], x[:, sl, :], ys[:, sl], phi, th


_SIM = {}


def null_tables(reps=500):
    key = reps
    if key not in _SIM:
        _SIM[key] = (pt.cips_critical_values(N, T, 1, reps, SEED)["sim"], pt.pedroni_null(N, T, 2, 1, reps, SEED))
    return _SIM[key]


def one_rep(args):
    scen, r, B, sims = args
    coint, factor, hetero = SCEN[scen]
    rng = np.random.default_rng([SEED, r, list(SCEN).index(scen)])
    y, X, ys, phi, th = simulate(rng, coint, factor, hetero)
    out = {"scen": scen, "r": r}
    res = {"MG": pt.mg(y, X), "PMG": pt.pmg(y, X), "DFE": pt.dfe(y, X), "CS-ARDL": pt.cs_ardl(y, X)}
    truth = th.mean(0)
    for m, o in res.items():
        for j in range(2):
            out[f"{m}_th{j}"] = o["theta"][j]
            out[f"{m}_se{j}"] = o["se_theta"][j]
        out[f"{m}_phi"] = o["phi"]
    out["phi_true"] = phi.mean()
    out["th_true0"], out["th_true1"] = truth
    h = pt.hausman_mg_pmg(res["MG"], res["PMG"])
    out["haus_p"] = h["p"]
    w = pt.westerlund(y, X, 1, B, seed=SEED + r)
    for k_, v in w["p"].items():
        out[f"WL_{k_}_p"] = v
    ped = pt.pedroni(y, X, 1, sim=sims[1])
    out["PED_panel_p"], out["PED_group_p"] = ped["p"]["panel_adf"], ped["p"]["group_adf"]
    out["CIPS_p"] = pt.sim_pvalue(pt.cips(y, 1), sims[0])
    out["CIPS_stat_p"] = pt.sim_pvalue(pt.cips(ys, 1), sims[0])  # potencia sobre serie estacionaria
    return out


def run(reps=200, B=99, sim_reps=500, procs=4, scens=None):
    sims = null_tables(sim_reps)
    scens = scens or list(SCEN)
    jobs = [(s, r, B, sims) for s in scens for r in range(reps)]
    with Pool(procs) as pool:
        rows = pool.map(one_rep, jobs, chunksize=10)
    return pd.DataFrame(rows)


def summarize(df):
    recs = []
    for s, g in df.groupby("scen"):
        coint, factor, hetero = SCEN[s]
        for m in ["MG", "PMG", "DFE", "CS-ARDL"]:
            if not coint:
                continue
            for j in range(2):
                est, se, tr = g[f"{m}_th{j}"], g[f"{m}_se{j}"], g[f"th_true{j}"]
                err = est - tr
                cov = ((est - 1.96 * se <= tr) & (tr <= est + 1.96 * se)).mean()
                recs.append(dict(scen=s, herramienta=m, metrica=f"theta{j + 1}", valor_verdadero=tr.mean(),
                                 sesgo=err.mean(), sesgo_rel=err.mean() / abs(tr.mean()), rmse=np.sqrt((err ** 2).mean()),
                                 cobertura=cov, tasa_rechazo=np.nan))
            e = g[f"{m}_phi"] - g["phi_true"]
            recs.append(dict(scen=s, herramienta=m, metrica="phi_media", valor_verdadero=g["phi_true"].mean(),
                             sesgo=e.mean(), sesgo_rel=e.mean() / abs(g["phi_true"].mean()),
                             rmse=np.sqrt((e ** 2).mean()), cobertura=np.nan, tasa_rechazo=np.nan))
        tests = {"Westerlund_Gt": "WL_Gt_p", "Westerlund_Ga": "WL_Ga_p", "Westerlund_Pt": "WL_Pt_p",
                 "Westerlund_Pa": "WL_Pa_p", "Pedroni_panelADF": "PED_panel_p", "Pedroni_groupADF": "PED_group_p",
                 "Hausman_MG_PMG": "haus_p"}
        for nm, c in tests.items():
            recs.append(dict(scen=s, herramienta=nm, metrica="rechazo_5%", tasa_rechazo=(g[c] < 0.05).mean()))
        recs.append(dict(scen=s, herramienta="CIPS_sobre_y_I(1)", metrica="rechazo_5%",
                         tasa_rechazo=(g["CIPS_p"] < 0.05).mean()))
        recs.append(dict(scen=s, herramienta="CIPS_sobre_serie_estacionaria", metrica="rechazo_5%",
                         tasa_rechazo=(g["CIPS_stat_p"] < 0.05).mean()))
    return pd.DataFrame(recs)


if __name__ == "__main__":
    t0 = time.time()
    reps = int(sys.argv[1]) if len(sys.argv) > 1 else 200
    df = run(reps)
    out = ROOT / "output" / "v7" / "R2"
    out.mkdir(parents=True, exist_ok=True)
    sm = summarize(df)
    sm.to_csv(out / "montecarlo.csv", index=False)
    df.to_csv(out / "montecarlo_replicas.csv.gz", index=False)
    print(f"{time.time() - t0:.0f}s")
