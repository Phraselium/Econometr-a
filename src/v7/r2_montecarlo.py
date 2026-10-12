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
ESTS = ["MG", "PMG", "PMG_sandwich", "PMG_boot", "DFE", "CS-ARDL", "CS-DL", "MG_dm", "PMG_dm"]
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
    yrw = np.cumsum(rng.standard_normal((N, TT)) + (ky[:, None] * f[None, :] if factor else 0), 1)  # RW puro (tamano CIPS)
    sl = slice(BURN, None)
    return y[:, sl], x[:, sl, :], ys[:, sl], phi, th, yrw[:, sl]


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
    y, X, ys, phi, th, yrw = simulate(rng, coint, factor, hetero)
    out = {"scen": scen, "r": r}
    pm = pt.pmg(y, X)
    res = {"MG": pt.mg(y, X), "PMG": pm, "DFE": pt.dfe(y, X), "CS-ARDL": pt.cs_ardl(y, X), "CS-DL": pt.cs_dl(y, X),
           "PMG_sandwich": dict(pm, se_theta=np.sqrt(np.diag(pm["V_sandwich"])))}
    if coint and not factor and not hetero or scen.startswith("B"):
        if r < 100:
            res["PMG_boot"] = dict(pm, se_theta=pt.pmg_bootstrap(y, X, B=49, seed=SEED + r)["se_theta"])
    yd, Xd = pt.cs_demean(y, X)
    pmd = pt.pmg(yd, Xd)
    res["MG_dm"], res["PMG_dm"] = pt.mg(yd, Xd), pmd
    out["MG_jk_phi"] = pt.jackknife_phi(pt.mg, y, X)
    out["DFE_jk_phi"] = pt.jackknife_phi(pt.dfe, y, X)
    truth = th.mean(0)
    for m, o in res.items():
        for j in range(2):
            out[f"{m}_th{j}"] = o["theta"][j]
            out[f"{m}_se{j}"] = o["se_theta"][j]
        out[f"{m}_phi"] = o["phi"]
    out["phi_true"] = phi.mean()
    out["th_true0"], out["th_true1"] = truth
    out["haus_p"] = pt.hausman_mg_pmg(res["MG"], pm, "info", "difference")["p"]
    out["haus_sw_p"] = pt.hausman_mg_pmg(res["MG"], pm, "sandwich", "difference")["p"]
    out["haus_vmg_p"] = pt.hausman_mg_pmg(res["MG"], pm, "info", "mg")["p"]
    w = pt.westerlund(y, X, 1, B, seed=SEED + r)
    for k_, v in w["p"].items():
        out[f"WL_{k_}_p"] = v
    ped = pt.pedroni(y, X, 1, sim=sims[1])
    out["PED_panel_p"], out["PED_group_p"] = ped["p"]["panel_adf"], ped["p"]["group_adf"]
    out["CIPS_p"] = pt.sim_pvalue(pt.cips(y, 1), sims[0])
    out["CIPS_rw_p"] = pt.sim_pvalue(pt.cips(yrw, 1), sims[0])
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
        g0 = g
        for m in ESTS:
            if not coint or f"{m}_th0" not in g0 or g0[f"{m}_th0"].isna().all():
                continue
            g = g0.dropna(subset=[f"{m}_th0"])
            for j in range(2):
                est, se, tr = g[f"{m}_th{j}"], g[f"{m}_se{j}"], g[f"th_true{j}"]
                err = est - tr
                cov = ((est - 1.96 * se <= tr) & (tr <= est + 1.96 * se)).mean()
                recs.append(dict(scen=s, herramienta=m, metrica=f"theta{j + 1}", valor_verdadero=tr.mean(),
                                 sesgo=err.mean(), sesgo_rel=err.mean() / abs(tr.mean()), rmse=np.sqrt((err ** 2).mean()),
                                 cobertura=cov, tasa_rechazo=np.nan))
            e = g[f"{m}_phi"] - g["phi_true"]
            if m in ("MG", "DFE"):
                ej = g[f"{m}_jk_phi"] - g["phi_true"]
                recs.append(dict(scen=s, herramienta=m + "_jackknife", metrica="phi_media", valor_verdadero=g["phi_true"].mean(),
                                 sesgo=ej.mean(), sesgo_rel=ej.mean() / abs(g["phi_true"].mean()), rmse=np.sqrt((ej ** 2).mean())))
            recs.append(dict(scen=s, herramienta=m, metrica="phi_media", valor_verdadero=g["phi_true"].mean(),
                             sesgo=e.mean(), sesgo_rel=e.mean() / abs(g["phi_true"].mean()),
                             rmse=np.sqrt((e ** 2).mean()), cobertura=np.nan, tasa_rechazo=np.nan))
        g = g0
        tests = {"Westerlund_Gt": "WL_Gt_p", "Westerlund_Ga": "WL_Ga_p", "Westerlund_Pt": "WL_Pt_p",
                 "Westerlund_Pa": "WL_Pa_p", "Pedroni_panelADF": "PED_panel_p", "Pedroni_groupADF": "PED_group_p",
                 "Hausman_info": "haus_p", "Hausman_sandwich": "haus_sw_p",
                 "Hausman_VMG": "haus_vmg_p"}
        for nm, c in tests.items():
            recs.append(dict(scen=s, herramienta=nm, metrica="rechazo_5%", tasa_rechazo=(g[c] < 0.05).mean()))
        recs.append(dict(scen=s, herramienta="CIPS_RW_puro", metrica="rechazo_5%",
                         tasa_rechazo=(g["CIPS_rw_p"] < 0.05).mean()))
        recs.append(dict(scen=s, herramienta="CIPS_sobre_y_del_DGP", metrica="rechazo_5%",
                         tasa_rechazo=(g["CIPS_p"] < 0.05).mean()))
        recs.append(dict(scen=s, herramienta="CIPS_sobre_serie_estacionaria", metrica="rechazo_5%",
                         tasa_rechazo=(g["CIPS_stat_p"] < 0.05).mean()))
    return pd.DataFrame(recs)


MCSE = float(np.sqrt(0.05 * 0.95 / 200))  # error MC de una tasa en torno a 0,05 con 200 replicas
EST_OK = ["A_coint_sin_factor", "B_coint_con_factor"]  # DGP bajo el que se juzgan los estimadores (theta comun)


def veredictos(sm):
    """Aplica los criterios declarados. Estimadores (escenarios A y B, theta1 y theta2): |sesgo rel| <= 10 % Y
    cobertura en [0,90; 0,98]. Punto apto pero cobertura fuera -> 'apta con reservas'; sesgo fuera -> 'no apta'.
    Tests: tamano en [0,02; 0,10] en TODOS los escenarios con H0 verdadera (para Hausman: A y B). Tamano mayor
    que 0,10 pero <= 0,10 + 1 EE-MC (0,015) o menor que 0,02 con potencia >= 0,90 -> 'apta con reservas'; mas
    alejado -> 'no apta'."""
    v = {}
    for m in ESTS:
        g = sm[(sm.herramienta == m) & sm.scen.isin(EST_OK) & sm.metrica.str.startswith("theta")]
        if g.empty:
            continue
        bias = g.sesgo_rel.abs().max()
        cov = g.cobertura
        e = sm[(sm.herramienta == m) & (sm.scen == "E_coint_theta_heterogeneo") & (sm.metrica == "theta1")]
        ph = sm[(sm.herramienta == m) & sm.scen.isin(EST_OK) & (sm.metrica == "phi_media")].sesgo_rel.abs().max()
        txt = (f"max|sesgo rel| theta={bias:.3f}, cobertura {cov.min():.3f}-{cov.max():.3f}, "
               f"max|sesgo rel| media phi={ph:.3f}")
        if len(e):
            txt += f"; con theta_i heterogeneo (E): sesgo rel theta1={e.iloc[0].sesgo_rel:.3f}, cobertura={e.iloc[0].cobertura:.3f}"
        if bias > 0.10:
            v[m] = f"no apta: sesgo relativo de theta fuera de +-10 % ({txt})"
        elif ((cov < 0.90) | (cov > 0.98)).any():
            v[m] = f"apta con reservas: punto apto pero IC95 infra/sobre-cubre ({txt})"
        else:
            v[m] = f"apta ({txt})"
        if m in ("MG", "DFE") and ph > 0.10:
            j = sm[(sm.herramienta == m + "_jackknife") & sm.scen.isin(EST_OK)].sesgo_rel.abs().max()
            v[m] += (f". Sesgo de muestra finita CONOCIDO de phi (Hurwicz-Nickell, T=78): {ph:.3f}; "
                     f"con jackknife por mitades temporales {j:.3f}")
    def power(h, scs):
        return sm[(sm.herramienta == h) & sm.scen.isin(scs) & (sm.metrica == "rechazo_5%")].tasa_rechazo
    h0 = ["C_sin_coint_sin_factor", "D_sin_coint_con_factor"]
    h1 = ["A_coint_sin_factor", "B_coint_con_factor", "E_coint_theta_heterogeneo"]
    for h in sorted(set(sm.herramienta) - set(ESTS) - {"MG_jackknife", "DFE_jackknife"}):
        if h.startswith("Hausman"):
            siz, pw = power(h, EST_OK), power(h, ["E_coint_theta_heterogeneo"])
        elif h in ("CIPS_sobre_serie_estacionaria", "CIPS_sobre_y_del_DGP"):
            continue
        elif h.startswith("CIPS"):
            siz, pw = power(h, list(SCEN)), power("CIPS_sobre_serie_estacionaria", list(SCEN))
        else:
            siz, pw = power(h, h0), power(h, h1)
        lo, hi = siz.min(), siz.max()
        txt = f"tamano {lo:.3f}-{hi:.3f}; potencia {pw.min():.3f}-{pw.max():.3f}"
        if 0.02 <= lo and hi <= 0.10:
            v[h] = f"apta ({txt})"
        elif hi <= 0.10 + MCSE and lo >= 0.02 - 1e-9 or (hi <= 0.10 and pw.min() >= 0.90):
            v[h] = f"apta con reservas: {'conservador' if hi <= 0.10 else 'tamano algo > 0,10'} ({txt})"
        else:
            v[h] = (f"solo diagnostico (tamano fuera de [0,02; 0,10]; {txt})" if h.startswith("Hausman")
                    else f"no apta: tamano fuera de [0,02; 0,10] ({txt})")
    return v


def escribir_doc(sm, tiempo=None):
    v = veredictos(sm)
    L = ["# Validacion Monte Carlo de las herramientas de panel (V7-R2)", "",
         "Capa C4 (metodologica). Datos SOLO simulados; sin datos reales. SEED=20261010; 200 replicas por escenario; "
         f"N={N}, T={T}; Westerlund con 99 remuestras por bloques; CIPS y Pedroni con valores nulos simulados "
         "(500 replicas, paseos aleatorios independientes; medias/varianzas tabuladas de Pedroni NO VERIFICADAS y no usadas). "
         "Script: src/v7/r2_montecarlo.py; datos: output/v7/R2/montecarlo.csv.", "",
         "## DGP", "ECM por unidad con phi_i~U(-0,4;-0,1); theta=(1,0; -0,5) comun; efectos fijos en el nivel (c_i~N(0,4)); "
         "corto plazo heterogeneo (delta_ik~U(0;0,6), lambda_i~U(0;0,3)); x_k con deriva 0,05. Factor comun AR(0,5) en dx e y "
         "(cargas N(1;0,25)) en los escenarios con factor. Estimacion: ARDL(2,1) en forma ECM.",
         "- A: cointegrado, sin factor. B: cointegrado, con factor (dependencia transversal).",
         "- C: sin cointegracion (phi=0), sin factor. D: sin cointegracion, con factor (tamano de los tests).",
         "- E: cointegrado con theta_i heterogeneo (sd 0,5), sin factor (potencia del Hausman; PMG mal especificado).", "",
         "## Criterios declarados",
         "- |sesgo relativo| <= 10 %; cobertura IC95 de theta en [0,90; 0,98]; tamano nominal 5 % en [0,02; 0,10].",
         f"- Tolerancia: 1 error estandar MC de una tasa en 5 % con 200 replicas = {MCSE:.3f}. Reglas de veredicto en "
         "`veredictos()`: estimadores juzgados en A y B (theta1 y theta2); tests en todos los escenarios con H0 verdadera "
         "(Hausman: A y B; CIPS: y es I(1) en los cinco escenarios).", ""]
    for s in SCEN:
        g = sm[sm.scen == s]
        L += [f"## Escenario {s}", ""]
        e = g[g.metrica.str.startswith(("theta", "phi"))]
        if len(e):
            e = e.drop(columns=["scen", "tasa_rechazo"]).round(3)
            L += ["| herramienta | metrica | verdadero | sesgo | sesgo rel | RMSE | cobertura |", "|---|---|---|---|---|---|---|"]
            L += [f"| {r.herramienta} | {r.metrica} | {r.valor_verdadero} | {r.sesgo} | {r.sesgo_rel} | {r.rmse} | {r.cobertura} |"
                  for r in e.itertuples()]
            L.append("")
        t = g[g.metrica == "rechazo_5%"].round(3)
        L += ["| test | tasa de rechazo al 5 % |", "|---|---|"] + [f"| {r.herramienta} | {r.tasa_rechazo} |" for r in t.itertuples()]
        L.append("")
    L += ["## Juicio de aptitud por herramienta", "", "| herramienta | veredicto |", "|---|---|"]
    L += [f"| {k} | {x} |" for k, x in v.items()]
    L += ["", "## Lectura y limites (revision tras correcciones)",
          "- Rechazo en C/D = tamano; en A/B/E = potencia. CIPS: tamano sobre un paseo aleatorio puro (N=17, T=78; con y sin factor) = 0,055-0,080 "
          "(apta). Sobre la y del DGP (I(1) mas un componente estacionario grande) rechaza 0,11-0,56: no es un problema de CIPS sino de ese DGP, "
          "y se informa como `CIPS_sobre_y_del_DGP` solo a titulo informativo. Potencia: serie AR(0,7). No se probaron truncacion K1/K2 ni tendencia.",
          "- PMG: EE por informacion cubre 0,86-0,885; el sandwich Huber-White cubre peor (0,79-0,84); el bootstrap por unidades (B=49, solo 100 replicas "
          "en A y B) cubre 0,87-0,92: el mas cercano a [0,90; 0,98] pero sin cumplirlo en B. Para inferencia con datos reales: `pmg_bootstrap` con B>=199 "
          "y tratar el IC como aproximado (reserva). Con theta_i heterogeneo (E) el PMG sesga 16-43 % y cubre 0,17-0,39: usar MG si el Hausman rechaza.",
          "- CS-ARDL y CS-DL: la revision de la implementacion (p_T=floor(T^(1/3))=4, theta_i=-b_x/phi, media MG) no halla error; ambas sesgan theta2 un 17-22 % "
          "(coste de grados de libertad con T=78 y ~20 regresores) y cubren 0,72-0,84: NO APTAS. No usar. La dependencia transversal se trata con "
          "demeaning transversal (`cs_demean`): MG_dm tiene sesgo <=7 % y cobertura 0,87-0,94 (apta con reservas); PMG_dm cubre 0,83-0,87. "
          "En este DGP el factor es estacionario y MG/PMG sin ajuste ya tienen sesgo <=6 %.",
          "- Hausman: la version V_MG - V_PMG (info o sandwich) sobre-rechaza (0,065-0,135): SOLO DIAGNOSTICO. La version con la varianza no parametrica de MG "
          "(`var_diff='mg'`, defecto) tiene tamano 0,03-0,06 pero potencia moderada (0,61 con theta_i sd 0,5): apta, conservadora. No se implemento el bootstrap de la diferencia.",
          "- Sesgo de phi en MG y DFE: sesgo de muestra finita conocido (Hurwicz-Nickell; ~-19 % MG, +4 % a +19 % DFE). El jackknife por mitades "
          "temporales (`jackknife_phi`) no lo corrige de forma fiable (MG: +7 % en A, +13 % en B; DFE empeora): NO se aplica; se reporta el sesgo.",
          "- Westerlund y Pedroni: p por bootstrap/simulacion, no por momentos tabulados. Westerlund es una variante (pooled ponderado 1/sigma_i^2, sin leads de dx), conservadora aqui.",
          "- Resultados de simulacion con 200 replicas por escenario; no extrapolar a otros DGP. Ninguna cifra procede de datos reales.", ""]
    (ROOT / "docs" / "v7" / "validacion_herramientas.md").write_text("\n".join(L), encoding="utf-8")
    return v


def escribir_resto(sm, v):
    import json
    from econ_utils import Registry
    out = ROOT / "output" / "v7" / "R2"
    reg = Registry(out / "registro.csv")
    for r in sm.itertuples():
        reg.log("R2_MC", f"{r.scen}|{r.herramienta}|{r.metrica}", "simulacion N=17 T=78 200 rep", "sim", "sim", 200,
                np.nan, np.nan, np.nan, coef_interes=r.sesgo if r.metrica.startswith(("theta", "phi")) else r.tasa_rechazo,
                p_interes=np.nan, notas="sesgo (estimadores) o tasa de rechazo (tests); sin contraste de hipotesis -> FDR no aplica")
    reg.flush()
    res = dict(rama="R2", pregunta="Son aptas las herramientas de panel (MG, PMG, DFE, CS-ARDL, Hausman, CIPS, Westerlund, Pedroni) "
               "en N=17, T=78 con dependencia transversal?", capa="C4", datos="simulados (SEED=20261010); sin datos reales",
               N=dict(unidades=N, T=T, replicas_por_escenario=200), metodo="Monte Carlo, 5 escenarios (ver docs/v7/validacion_herramientas.md)",
               estimacion=None, ic95=None, p_ajustado=None, nivel_evidencia="DESCRIPTIVO (validacion metodologica por simulacion)",
               diagnosticos=v, fuera_muestra=dict(modelo=None, rmse=None, dm_vs_ar4=None),
               notas="Medias/varianzas tabuladas de Pedroni no verificadas ni usadas (p simulados). Referencias NO VERIFICADAS.")
    (out / "resultado.json").write_text(json.dumps(res, ensure_ascii=False, indent=1), encoding="utf-8")


if __name__ == "__main__":
    t0 = time.time()
    out = ROOT / "output" / "v7" / "R2"
    out.mkdir(parents=True, exist_ok=True)
    if len(sys.argv) > 1 and sys.argv[1] == "doc":
        sm = pd.read_csv(out / "montecarlo.csv")
    else:
        df = run(200)
        sm = summarize(df)
        sm.to_csv(out / "montecarlo.csv", index=False)
        df.to_csv(out / "montecarlo_replicas.csv.gz", index=False, compression={"method": "gzip", "mtime": 0})  # determinista
    escribir_resto(sm, escribir_doc(sm))
    print(f"{time.time() - t0:.0f}s")
