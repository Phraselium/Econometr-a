"""R2 ronda 3: Monte Carlo ampliado (escenarios F, G, J, K, L; pT; jackknife; bootstrap PMG con demeaning; CIPS;
SBC; valor critico de phi-bar). Solo datos simulados, SEED=20261010, determinista."""
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
import r2_montecarlo as m1  # noqa: E402

SEED, N, T, TH, BURN = pt.SEED, m1.N, m1.T, m1.TH, m1.BURN
# nombre: (tipo, replicas, componentes)
SC = {
    "A": ("old", 500, {"est", "wl", "cips", "sbc", "boot"}),
    "B": ("old", 200, {"est", "cips", "boot"}),
    "C": ("old", 500, {"est", "wl", "cips"}),
    "D": ("old", 500, {"est", "wl", "cips"}),
    "E": ("old", 200, {"est", "cips", "boot"}),
    "F": ("het", 500, {"est", "wl", "boot"}),
    "G": ("hom", 200, {"est"}),
    "J": ("slow", 200, {"est", "wl"}),
    "K": ("feed", 200, {"est"}),
    "L": ("brk", 200, {"est"}),
}
DESC = {"A": "coint., sin factor", "B": "coint., factor I(0)", "C": "sin coint., sin factor", "D": "sin coint., factor I(0)",
        "E": "theta_i heterogeneo", "F": "factor I(1) en el residuo, cargas heterogeneas correlacionadas con las de x",
        "G": "factor I(1), cargas homogeneas", "J": "phi_i~U(-0,1;-0,02) (ajuste lento)",
        "K": "retroalimentacion: dx con -0,1*ec", "L": "rotura en c_i hacia T/3"}
BOOT_B, BOOT_R = 199, 200


def sim_new(rng, kind):
    TT = T + BURN
    fac = kind in ("het", "hom")
    eta = rng.standard_normal(TT)
    f = np.cumsum(eta) if fac else np.zeros(TT)
    gx = rng.normal(1, 0.5, N) if kind == "het" else np.ones(N)
    ky = (0.7 * gx + rng.normal(0.3, 0.3, N)) if kind == "het" else np.ones(N)
    if not fac:
        gx, ky = np.zeros(N), np.zeros(N)
    phi = rng.uniform(-0.1, -0.02, N) if kind == "slow" else rng.uniform(-0.4, -0.1, N)
    ci, dlt, lam = rng.normal(0, 2, N), rng.uniform(0, 0.6, (N, 2)), rng.uniform(0, 0.3, N)
    ex, ez = rng.standard_normal((N, TT, 2)), rng.standard_normal((N, TT))
    x, z, dzp = np.zeros((N, TT, 2)), np.zeros((N, TT)), np.zeros(N)
    for t in range(1, TT):
        dx = 0.05 + gx[:, None] * eta[t] + ex[:, t]
        if kind == "feed":
            dx = dx - 0.1 * z[:, t - 1][:, None]
        x[:, t] = x[:, t - 1] + dx
        dz = phi * z[:, t - 1] + (dlt * dx).sum(1) + lam * dzp + ez[:, t]
        z[:, t] = z[:, t - 1] + dz
        dzp = dz
    c = np.tile(ci[:, None], (1, TT))
    if kind == "brk":
        c[:, BURN + T // 3:] += 3.0
    y = c + (x * TH).sum(2) + ky[:, None] * f[None, :] + z
    sl = slice(BURN, None)
    return y[:, sl], x[:, sl], phi


def gen(name, rng):
    kind = SC[name][0]
    if kind == "old":
        c, fct, h = m1.SCEN[{"A": "A_coint_sin_factor", "B": "B_coint_con_factor", "C": "C_sin_coint_sin_factor",
                             "D": "D_sin_coint_con_factor", "E": "E_coint_theta_heterogeneo"}[name]]
        y, X, _, phi, th, yrw = m1.simulate(rng, c, fct, h)
        return y, X, phi, yrw, th.mean(0)
    y, X, phi = sim_new(rng, kind)
    return y, X, phi, np.cumsum(rng.standard_normal((N, T)), 1), TH


_NULL = {}
VAR = {"base": {}, "sbc": dict(sbc=True), "trunc": dict(trunc=True), "trend": dict(trend=True),
       "sbc_trunc": dict(sbc=True, trunc=True)}


def null_cips(reps=500):
    if reps not in _NULL:
        _NULL[reps] = {k: pt.cips_critical_values(N, T, 1, reps, SEED, **kw)["sim"] for k, kw in VAR.items()}
    return _NULL[reps]


def estimators(y, X):
    out = {}
    pm = pt.pmg(y, X)
    yd, Xd = pt.cs_demean(y, X)
    mgd = pt.mg_dm_jackknife(y, X)
    allr = {"MG": pt.mg(y, X), "PMG": pm, "PMG_dm": pt.pmg(yd, Xd),
            "MG_dm": dict(theta=mgd["theta"], se_theta=mgd["se_theta"], phi=pt.mg(yd, Xd)["phi"],
                          se_phi=pt.mg(yd, Xd)["se_phi"])}
    for pT in (1, 2, 4):
        allr[f"CS-ARDL_pT{pT}"] = pt.cs_ardl(y, X, pT=pT)
        allr[f"CS-DL_pT{pT}"] = pt.cs_dl(y, X, pT=pT)
        for nm, fn in (("CS-ARDL", pt.cs_ardl), ("CS-DL", pt.cs_dl)):
            base = allr[f"{nm}_pT{pT}"]
            allr[f"{nm}_pT{pT}_jk"] = dict(base, theta=pt.jackknife_theta(fn, y, X, pT=pT))
    for k, o in allr.items():
        for j in range(2):
            out[f"{k}|th{j}"], out[f"{k}|se{j}"] = o["theta"][j], o["se_theta"][j]
        out[f"{k}|phi"] = o.get("phi", np.nan)
    return out, allr


def one_rep(args):
    name, r, B, nulls = args
    kind, _, comps = SC[name]
    rng = np.random.default_rng([SEED, r, 1000 + list(SC).index(name)])
    y, X, phi, yrw, thm = gen(name, rng)
    o = {"scen": name, "r": r, "phi_true": phi.mean(), "tt0": thm[0], "tt1": thm[1]}
    if "est" in comps:
        e, allr = estimators(y, X)
        o.update(e)
        o["MG_t_phi"] = allr["MG"]["phi"] / allr["MG"]["se_phi"]
        o["MG_dm_t_phi"] = allr["MG_dm"]["phi"] / allr["MG_dm"]["se_phi"]
    if "boot" in comps and r < BOOT_R:
        bt = pt.pmg_bootstrap(y, X, B=BOOT_B, seed=SEED + r, demean=True)["se_theta"]
        yd, Xd = pt.cs_demean(y, X)
        th = pt.pmg(yd, Xd)["theta"]
        for j in range(2):
            o[f"PMG_dm_boot|th{j}"], o[f"PMG_dm_boot|se{j}"] = th[j], bt[j]
    if "wl" in comps:
        w = pt.westerlund(y, X, 1, B, seed=SEED + r)["p"]
        for k_, v in w.items():
            o[f"WL_{k_}"] = v
    if "cips" in comps:
        for k, kw in VAR.items():
            o[f"CIPS_RW|{k}"] = pt.sim_pvalue(pt.cips(yrw, 1, **kw), nulls[k])
            o[f"CIPS_Y|{k}"] = pt.sim_pvalue(pt.cips(y, 1, **kw), nulls[k])
    if "sbc" in comps and r < 200:
        p, q = pt.select_lags_sbc(y, X)
        o["sbc_p"], o["sbc_q"] = p, q
        mgs = pt.mg(y, X, p, q)
        o["MG_sbc|th0"], o["MG_sbc|th1"] = mgs["theta"]
        o["MG_sbc|se0"], o["MG_sbc|se1"] = mgs["se_theta"]
    return o


def run(reps=None, B=99, nsim=500, procs=4, scens=None, boot_r=None):
    global BOOT_R
    if boot_r is not None:
        BOOT_R = boot_r
    nulls = null_cips(nsim)
    jobs = [(s, r, B, nulls) for s in (scens or SC) for r in range(reps or SC[s][1])]
    with Pool(procs) as pool:
        return pd.DataFrame(pool.map(one_rep, jobs, chunksize=4))


def summarize(df):
    rec = []
    for s, g in df.groupby("scen"):
        coint = SC[s][0] != "old" or s in ("A", "B", "E")
        names = sorted({c.split("|")[0] for c in df.columns if c.endswith("|th0")})
        for m in names:
            gm = g.dropna(subset=[f"{m}|th0"])
            if not coint or gm.empty:
                continue
            for j in range(2):
                est, se, tr = gm[f"{m}|th{j}"], gm[f"{m}|se{j}"], gm[f"tt{j}"]
                err = est - tr
                cov = ((est - 1.96 * se <= tr) & (tr <= est + 1.96 * se)).mean()
                rec.append(dict(scen=s, herramienta=m, metrica=f"theta{j + 1}", n=len(gm), sesgo_rel=float(err.mean() / abs(TH[j])),
                                rmse=float(np.sqrt((err ** 2).mean())), cobertura=float(cov),
                                ee_mc_cob=float(np.sqrt(cov * (1 - cov) / len(gm)))))
        for c in [c for c in g.columns if c.startswith(("WL_", "CIPS_"))]:
            x = g[c].dropna()
            if len(x):
                rec.append(dict(scen=s, herramienta=c, metrica="rechazo_5%", n=len(x), tasa=float((x < .05).mean()),
                                ee_mc_cob=float(np.sqrt((x < .05).mean() * (1 - (x < .05).mean()) / len(x)))))
        for c in ("MG_t_phi", "MG_dm_t_phi"):
            if c in g:
                rec.append(dict(scen=s, herramienta=c, metrica="cuantil5%", n=len(g), tasa=float(g[c].quantile(.05)),
                                ee_mc_cob=float(g[c].quantile(.01))))
        if "sbc_p" in g:
            x = g.dropna(subset=["sbc_p"])
            rec.append(dict(scen=s, herramienta="SBC_elige_(2,1)", metrica="frecuencia", n=len(x),
                            tasa=float(((x.sbc_p == 2) & (x.sbc_q == 1)).mean())))
    return pd.DataFrame(rec)


def aptitud(sm, escenarios=("A", "B", "F", "G", "E", "J", "K", "L")):
    """Matriz estimador x escenario: apta / apta con reservas (sesgo ok, cobertura fuera de [0,90;0,98]) / no apta
    (|sesgo rel| > 10 % en theta1 o theta2). Incluye cobertura min-max y su EE-MC."""
    e = sm[sm.metrica.str.startswith("theta")]
    rows = []
    for m in sorted(e.herramienta.unique()):
        row = {"estimador": m}
        for s in escenarios:
            g = e[(e.herramienta == m) & (e.scen == s)]
            if g.empty:
                row[s] = "-"
                continue
            b, cv = g.sesgo_rel.abs().max(), g.cobertura
            lab = "no apta" if b > .10 else ("apta" if ((cv >= .90) & (cv <= .98)).all() else "reservas")
            row[s] = f"{lab} (b={b:.2f}; cob {cv.min():.2f}-{cv.max():.2f}±{g.ee_mc_cob.max():.2f})"
        rows.append(row)
    return pd.DataFrame(rows)


def _md(df):
    cols = list(df.columns)
    return "\n".join(["| " + " | ".join(cols) + " |", "|" + "---|" * len(cols)] +
                     ["| " + " | ".join(str(v) for v in r) + " |" for r in df.itertuples(index=False)])


def escribir_doc(sm):
    r2 = pd.read_csv(ROOT / "output" / "v7" / "R2" / "montecarlo.csv")
    ap = aptitud(sm)
    L = ["# Validacion Monte Carlo de las herramientas de panel (V7-R2, ronda 3)", "",
         "Capa C4 (metodologica). Solo datos simulados, SEED=20261010, N=17, T=78. Replicas: 500 en A, C, D, F; 200 en B, E, G, J, K, L; "
         "PMG bootstrap: B=199, 200 replicas en A, B, E, F; Westerlund-tipo: 99 remuestras. `±` = EE-MC de la cobertura/tasa. "
         "Codigo: src/v7/r2_mc3.py (+ r2_montecarlo.py, ronda 2: output/v7/R2/montecarlo.csv). Datos: output/v7/R2/montecarlo_r3.csv.", "",
         "## Escenarios", ""] + [f"- {k}: {v}" for k, v in DESC.items()] + [
         "", "Criterios declarados (sin cambios respecto a la ronda 1): |sesgo rel| <= 10 %; cobertura IC95 en [0,90; 0,98]; tamano en [0,02; 0,10]. "
         "Etiqueta: `apta` (ambos), `reservas` (sesgo ok, cobertura fuera), `no apta` (sesgo > 10 % en theta1 o theta2). b = max |sesgo rel|.", "",
         "## Tabla final de aptitud de estimadores de theta, por escenario", "", _md(ap), ""]
    t = sm[sm.metrica == "rechazo_5%"]
    for pref, tit in (("WL_", "Test tipo Westerlund (variante; no el estadistico original): tasa de rechazo 5 %"),
                      ("CIPS_RW", "CIPS sobre paseo aleatorio puro (objetivo 1: tamano)"),
                      ("CIPS_Y", "CIPS sobre la y del DGP, I(1) + I(0) grande (objetivo 2: tamano; en A, B, E, y tambien C, D)")):
        g = t[t.herramienta.str.startswith(pref)]
        if len(g):
            pv = g.assign(v=g.tasa.round(3).astype(str) + "±" + g.ee_mc_cob.round(3).astype(str)).pivot(index="herramienta", columns="scen", values="v")
            L += [f"## {tit}", "", _md(pv.reset_index()), ""]
    q = sm[sm.metrica == "cuantil5%"]
    L += ["## Valor critico al 5 % del t de MG para phi-bar bajo H0 (sin cointegracion; escenarios C y D)", "",
          _md(q[["scen", "herramienta", "n", "tasa"]].rename(columns={"tasa": "cuantil_5%"}).round(3)), "",
          f"Valor critico al 5 % para H7-E2 (cuantil 5 % del t de MG para phi-bar bajo H0, el menor de C y D): "
          f"**{q[q.scen.isin(['C', 'D']) & (q.herramienta == 'MG_t_phi')].tasa.min():.2f}** (no -1,645: la distribucion es de tipo Dickey-Fuller y esta muy desplazada). "
          "Aplicable solo a este DGP (N=17, T=78, ARDL(2,1)); el t de MG con demeaning da -8,58 (C) y -8,22 (D).", ""]
    sb = sm[(sm.metrica == "frecuencia") & (sm.n > 0)]
    L += ["## Seleccion de retardos por SBC (p, q <= 4; verdadero ARDL(2,1))", "", _md(sb[["scen", "herramienta", "n", "tasa"]].round(3)), ""]
    ho = r2[r2.herramienta.str.startswith(("Pedroni", "Hausman"))]
    L += ["## Pedroni y Hausman (ronda 2, 200 replicas; sin cambios)", "",
          _md(ho.pivot(index="herramienta", columns="scen", values="tasa_rechazo").round(3).reset_index()), ""]
    L += ["## Observaciones y limites (ronda 3)", "",
          "- Tiempo de ejecucion del Monte Carlo completo de la ronda 3: ~1.600 s con 4 procesos (supera los 10 min del encargo original); "
          "la ronda 2 (r2_montecarlo.py) tarda ~6 min. Los tests usan versiones reducidas (<60 s).",
          "- Con factor I(1) y cargas heterogeneas (F) ningun estimador cumple ambos criterios: MG y PMG sin ajuste fallan (sesgo >40 %); "
          "MG_dm sesga 20 %; CS-DL con p_T=4 es el mas cercano (sesgo <=11 %, cobertura 0,86-0,90); PMG_dm con bootstrap (demeaning re-aplicado) cubre 0,90-0,94 con sesgo 16 %. "
          "Con cargas homogeneas (G) MG_dm es apto. El jackknife de mitades sobre theta de CS reduce el sesgo en algunos casos pero hunde la cobertura (EE sin corregir).",
          "- PMG_dm con bootstrap B=199 (ver tabla): cobertura 0,95-0,97 en A y B (apta), 0,90-0,94 en F, 0,91-0,92 en E; sobrecubre algo en A/B (dentro de lo conservador).",
          "- CIPS: tamano correcto sobre paseo aleatorio puro (base y SBC 0,034-0,076; con tendencia 0,064-0,095) pero sobrerrechaza sobre una I(1)+I(0) grande "
          "(base 0,35-0,62; SBC 0,14-0,60); la truncacion CIPS* (K1=6,19, K2=2,61, NO VERIFICADOS) no cambia nada. Ambos objetivos se reportan con el mismo criterio de tamano.",
          "- Test tipo Westerlund: tamano 0,002-0,016 (conservador, por debajo de 0,02); potencia con phi_i en [-0,1; -0,02] (J): Gt 0,10, Ga 0,06, Pt 0,18, Pa 0,29: baja. "
          "En F rechaza 0,86-0,93: en F y, x y el factor cointegran conjuntamente, de modo que la lectura 'H0 verdadera' no es estricta.",
          "- SBC con p, q <= 4 elige el orden verdadero ARDL(2,1) el 52 % de las veces (A); MG con SBC: ver fila MG_sbc (A).",
          "- PMG con retroalimentacion (K) o rotura (L) o phi lento (J): no apto (inestable). MG_dm es apto con rotura (L) pero no con retroalimentacion (K).",
          "- (H10a) No hay Stata/R ni red en esta sesion para comparar con xtpmg o un resultado publicado: queda anotado como pendiente.",
          "- Referencias NO VERIFICADAS (sin acceso a Crossref).", ""]
    (ROOT / "docs" / "v7" / "validacion_herramientas.md").write_text("\n".join(L), encoding="utf-8")


def escribir_json(sm):
    import json

    from econ_utils import Registry
    out = ROOT / "output" / "v7" / "R2"
    reg = Registry(out / "registro.csv")
    for r in sm.itertuples():
        reg.log("R2_MC3", f"{r.scen}|{r.herramienta}|{r.metrica}", "simulacion N=17 T=78", "sim", "sim", int(r.n), np.nan, np.nan, np.nan,
                coef_interes=getattr(r, "sesgo_rel", np.nan) if str(r.metrica).startswith("theta") else getattr(r, "tasa", np.nan),
                notas="sin contraste de hipotesis; FDR no aplica")
    reg.flush()
    ap = aptitud(sm)
    res = dict(rama="R2", pregunta="Aptitud de herramientas de panel (MG, MG_dm, PMG, PMG_dm, CS-ARDL, CS-DL, tipo Westerlund, CIPS) con factor I(1)",
               capa="C4", datos="simulados (SEED=20261010)", N=dict(unidades=N, T=T), metodo="Monte Carlo, escenarios A-G, J, K, L",
               estimacion=None, ic95=None, p_ajustado=None, nivel_evidencia="DESCRIPTIVO (validacion por simulacion)",
               diagnosticos={r["estimador"]: {k: v for k, v in r.items() if k != "estimador"} for r in ap.to_dict("records")},
               fuera_muestra=dict(modelo=None, rmse=None, dm_vs_ar4=None),
               notas="Ver docs/v7/validacion_herramientas.md. Referencias NO VERIFICADAS.")
    (out / "resultado.json").write_text(json.dumps(res, ensure_ascii=False, indent=1), encoding="utf-8")


if __name__ == "__main__":
    t0 = time.time()
    out = ROOT / "output" / "v7" / "R2"
    if len(sys.argv) > 1 and sys.argv[1] == "doc":
        sm = pd.read_csv(out / "montecarlo_r3.csv")
    else:
        df = run()
        sm = summarize(df)
        sm.to_csv(out / "montecarlo_r3.csv", index=False)
        df.to_csv(out / "montecarlo_r3_replicas.csv.gz", index=False, compression={"method": "gzip", "mtime": 0})  # determinista
    escribir_doc(sm)
    escribir_json(sm)
    print(f"{time.time() - t0:.0f}s")
