#!/usr/bin/env python3
"""V8-F4 M7: multiverso estructurado (<= 50.000 especificaciones, TODAS en el Registry). Capa C4: sensibilidad, no causalidad.

Dimensiones: mercado/medida de precio (compra: valor tasado e IPV; alquiler: IPC de alquiler, sin alternativa trimestral nacional), deflactor (IPC /
deflactor del PIB), transformacion (interanual / trimestral), periodo (P1-P5, completo), factor focal y SU variable (2-3 alternativas por familia),
conjunto de controles (subconjuntos de familias: ninguno, macro, estructura, todas; cada control con su variable principal), retardos de los
regresores (0/1/4), errores (HAC Newey-West de 4 retardos / EWC) y ficticias COVID/EPA2021 (sin/con).
Para cada (mercado, periodo, factor, variable) y para el agregado de la familia (variable='TODAS', clave de cruce para M2/M5):
n_multiverso, % mismo signo, % significativo tras BH (q=0,10, por mercado y periodo, sobre TODAS las especificaciones) y cuantiles del coeficiente
tipificado. cumple_multiverso = signo estable >= 80 % Y significativo tras BH en >= 50 % (hipotesis.md §9). Nunca se elige una especificacion por su p.
Extension frente a herramientas/multiverso.correr_multiverso (que solo admite HAC, beta sin tipificar, una sola variable x por especificacion y sin
EWC ni ficticias): mismo OLS + HAC (statsmodels), mas EWC y beta tipificado; se valida en tests/v8/test_m7.py contra la herramienta.
Uso: python3 src/v8/m7_multiverso.py [--rapido] [--salida DIR]
"""
from __future__ import annotations

import os

for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS"):
    os.environ[_v] = "1"

import argparse  # noqa: E402
import itertools  # noqa: E402
import json  # noqa: E402
import sys  # noqa: E402
import time  # noqa: E402
import warnings  # noqa: E402
from pathlib import Path  # noqa: E402

import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402
import statsmodels.api as sm  # noqa: E402

RAIZ = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(RAIZ / "src"))
sys.path.insert(0, str(RAIZ / "src" / "v8"))
import m67_comun as C  # noqa: E402
from econ_utils import Registry  # noqa: E402

warnings.filterwarnings("ignore")
SEED = 20261010
SCRIPT = "src/v8/m7_multiverso.py"
MAX_SPECS = 50_000
Q_BH = 0.10
MAX_ALT = 3
CONJUNTOS = {"ninguno": [], "macro": ["empleo_renta", "credito_tipos"], "estructura": ["demografia", "oferta"], "todas": None}
ORIENTACION = {"tipo_hip_real": -1.0}   # J6: tipos x-1 (expansivo = positivo); el resto, «mas es mas presion»
TRUNCADO = {("alquiler", "P4"), ("compra", "P4"), ("compra", "P1")}   # J15: celdas con >= 37 % de fallidas
COLS = ["id", "mercado", "medida", "deflactor", "transformacion", "periodo", "factor", "variable", "interpolada", "retardo", "controles", "n_controles",
        "ficticias", "errores", "n", "beta", "beta_std", "se", "p", "r2_adj"]


def construir_celdas(d, mercados, deflactores, transfs, periodos):
    celdas = {}
    for merc, medidas in mercados.items():
        for med in medidas:
            for dfl in deflactores:
                for tr in transfs:
                    dep, X, ip, niv = C.preparar(d, merc, med, dfl, tr)
                    for per in periodos:
                        win = C.ventana(d.index, per)
                        focal = {}
                        ctrl = {}
                        for f in C.FAM_ORDEN:
                            v = C.candidatas_viables(f, dep, X, ip, win, permitir_interp=True)[:MAX_ALT]
                            if v:
                                focal[f] = v
                            v0 = C.candidatas_viables(f, dep, X, ip, win)
                            if v0:
                                ctrl[f] = v0[0][0]
                        celdas[(merc, med, dfl, tr, per)] = {"dep": dep, "X": X, "win": win, "focal": focal, "ctrl": ctrl, "tr": tr}
    return celdas


def descriptores(celdas, retardos, errores, d=None):
    """Lista ligera de especificaciones (sin ajustar). Los conjuntos de controles duplicados tras la disponibilidad se eliminan."""
    out = []
    for key, c in celdas.items():
        dums = (0, 1)
        if d is not None:   # las ficticias solo se anaden como dimension si varian dentro de la ventana del periodo
            dums = (0, 1) if any(d.loc[c["win"], z].nunique() > 1 for z in ("covid", C.col_epa(key[3]))) else (0,)
        for f, alts in c["focal"].items():
            conj = {}
            for nom, fams in CONJUNTOS.items():
                fl = [g for g in C.FAM_ORDEN if g != f and g in c["ctrl"]] if fams is None else [g for g in fams if g != f and g in c["ctrl"]]
                conj.setdefault(tuple(fl), nom)
            for (v, ipo), (fl, nom), L, dum, err in itertools.product(alts, conj.items(), retardos, dums, errores):
                out.append((key, f, v, ipo, nom, fl, L, dum, err))
    return out


def ajustar(c, d, f, v, fl, L, dum, err):
    """Un ajuste OLS. Devuelve dict o ('FALLIDA', motivo, n)."""
    cols = [v] + [c["ctrl"][g] for g in fl]
    D = pd.concat([c["dep"]] + [c["X"][x].shift(L) for x in cols], axis=1).loc[c["win"]]
    D.columns = ["dep"] + cols
    nd = []
    if dum:
        dd = d.loc[D.index]
        if dd["covid"].std() > 0:
            nd.append("covid")
        ce = C.col_epa(c.get("tr", "interanual"))
        if any(x in C.EPA_VARS for x in cols) and dd[ce].std() > 0:
            nd.append(ce)
        if not nd:
            return ("OMITIDA", "las ficticias no varian en la muestra (duplica la especificacion sin ficticias)", 0)
        D = pd.concat([D, dd[nd]], axis=1)
    D = D.dropna()
    n = len(D)
    k = len(cols) + len(nd)
    if n - (k + 1) < C.GL_MIN:
        return ("FALLIDA", f"muestra insuficiente (n={n}, k={k}): GL < {C.GL_MIN}", n)
    y = D["dep"].values
    A = np.column_stack([np.ones(n), D[cols + nd].values])
    try:
        if err == "HAC4":
            r = sm.OLS(y, A).fit(cov_type="HAC", cov_kwds={"maxlags": 4})
            b, se, p = r.params[1], r.bse[1], r.pvalues[1]
            r2a, aic, bic = r.rsquared_adj, r.aic, r.bic
        else:
            ew = C.ewc_ols(y, A)
            b, se, p = ew["beta"][1], ew["se"][1], ew["p"][1]
            r = sm.OLS(y, A).fit()
            r2a, aic, bic = r.rsquared_adj, r.aic, r.bic
    except Exception as ex:  # noqa: BLE001
        return ("FALLIDA", f"error de ajuste ({type(ex).__name__}: {str(ex)[:60]})", n)
    sx, sy = A[:, 1].std(ddof=0), y.std(ddof=0)
    if not (np.isfinite(b) and np.isfinite(p) and sx > 0 and sy > 0):
        return ("FALLIDA", "estimacion no finita o varianza nula", n)
    return {"n": n, "beta": float(b), "beta_std": float(b * sx / sy), "se": float(se), "p": float(p), "r2_adj": float(r2a), "aic": float(aic), "bic": float(bic),
            "ini": D.index[0], "fin": D.index[-1], "nd": nd, "cols": cols}


def correr(d, celdas, desc, reg, max_specs=MAX_SPECS, seed=SEED):
    n_rej = len(desc)
    truncado = n_rej > max_specs
    if truncado:
        idx = np.sort(np.random.default_rng(seed).choice(n_rej, max_specs, replace=False))
        desc = [desc[i] for i in idx]
    filas, fallidas = [], []
    for i, (key, f, v, ipo, nom, fl, L, dum, err) in enumerate(desc):
        merc, med, dfl, tr, per = key
        mid = f"mv7_{i:05d}"
        r = ajustar(celdas[key], d, f, v, fl, L, dum, err)
        form = f"dep({merc},{med},{dfl},{tr}) ~ {v}(L{L}) + {'+'.join(celdas[key]['ctrl'][g] for g in fl) or '-'} [{'dummies' if dum else 'sin dummies'}]"
        if isinstance(r, tuple):
            estado, motivo, n = r
            fallidas.append({"id": mid, "mercado": merc, "periodo": per, "factor": f, "variable": v, "estado": estado, "motivo": motivo})
            reg.log("M7", mid, form, "", "", n, np.nan, np.nan, np.nan, notas=f"{estado}: {motivo};{merc};{med};{dfl};{tr};{per};{f};{err}")
            continue
        reg.log("M7", mid, form, r["ini"], r["fin"], r["n"], r["r2_adj"], r["aic"], r["bic"], coef_interes=r["beta"], p_interes=r["p"],
                notas=f"{merc};{med};{dfl};{tr};{per};{f};{v};L{L};{nom};{err};beta_std={r['beta_std']:.4f};interp={ipo}")
        filas.append({"id": mid, "mercado": merc, "medida": med, "deflactor": dfl, "transformacion": tr, "periodo": per, "factor": f, "variable": v,
                      "interpolada": bool(ipo), "retardo": L, "controles": nom, "n_controles": len(fl), "ficticias": int(bool(dum)), "errores": err,
                      "n": r["n"], "beta": r["beta"], "beta_std": r["beta_std"], "se": r["se"], "p": r["p"], "r2_adj": r["r2_adj"]})
    specs = pd.DataFrame(filas, columns=COLS)
    if len(specs):
        specs["p_bh"] = np.nan
        for _, g in specs.groupby(["mercado", "periodo"]):
            specs.loc[g.index, "p_bh"] = C.bh(g["p"].values, Q_BH)
    return specs, pd.DataFrame(fallidas, columns=["id", "mercado", "periodo", "factor", "variable", "estado", "motivo"]), truncado, n_rej


def _resumir(g, merc, per, f, var, n_rejilla=None):
    """Resumen de un grupo de especificaciones ajustadas. Signo ORIENTADO (J6): beta_std x orientacion de la variable (tipos x-1).
    n_rejilla = especificaciones de la rejilla completa del grupo (ajustadas + fallidas/omitidas); las fallidas cuentan como «no cumple» (J15)."""
    o = g["beta_std"] * g["variable"].map(ORIENTACION).fillna(1.0)
    med = o.median()
    sg = np.sign(med)
    mismo = np.sign(o) == sg
    sig = (g["p_bh"] < Q_BH) & mismo
    ps, pb = float(mismo.mean()), float(sig.mean())
    gi = g[~g["interpolada"]]
    if len(gi):
        oi = o.loc[gi.index]
        mi = np.sign(oi) == sg
        ps_i, pb_i = float(mi.mean()), float(((gi["p_bh"] < Q_BH) & mi).mean())
    else:
        ps_i = pb_i = np.nan
    nr = int(n_rejilla) if n_rejilla else len(g)
    ps_r, pb_r = float(mismo.sum() / nr), float(sig.sum() / nr)
    cum_r = bool(ps_r >= 0.80 and pb_r >= 0.50)
    return {"mercado": merc, "periodo": per, "factor": f, "variable": var, "n_multiverso": len(g), "pct_mismo_signo": ps,
            "signo_mayoritario": "positivo" if sg > 0 else ("negativo" if sg < 0 else "nulo"), "pct_sig_bh": pb,
            "beta_std_mediana": float(g["beta_std"].median()), "p05": float(g["beta_std"].quantile(0.05)), "p95": float(g["beta_std"].quantile(0.95)),
            "cumple_multiverso": bool(ps >= 0.80 and pb >= 0.50), "pct_interpoladas": float(g["interpolada"].mean()), "n_sin_interp": int(len(gi)),
            "pct_mismo_signo_sin_interp": ps_i, "pct_sig_bh_sin_interp": pb_i,
            "cumple_multiverso_sin_interp": (bool(ps_i >= 0.80 and pb_i >= 0.50) if len(gi) else np.nan),
            "pct_hac": float((g["errores"] == "HAC4").mean()), "capa": "C4",
            "orientacion": ("tipo x-1" if var in ORIENTACION else ("mixta" if var == "TODAS" and f == "credito_tipos" else "mas es mas presion")),
            "beta_orient_mediana": float(med), "n_rejilla": nr, "pct_mismo_signo_rejilla": ps_r, "pct_sig_bh_rejilla": pb_r,
            "cumple_multiverso_rejilla": cum_r,
            "multiverso_truncado": bool((merc, per) in TRUNCADO or (nr - len(g)) / nr >= 0.20)}


def resumen_multiverso(specs, fall=None):
    """Una fila por (mercado, periodo, factor, variable) y por familia (variable = TODAS). La rejilla de cada grupo = ajustadas + FALLIDAS
    (las omitidas por duplicar la especificacion sin ficticias no cuentan). R3: cumple_R3 = familia (TODAS) Y variable principal (primera
    candidata de la familia presente, orden de m67_comun) cumplen con signos orientados."""
    filas = []
    nf = {}
    if fall is not None and len(fall):
        for r in fall[fall["estado"] == "FALLIDA"].itertuples():
            nf[(r.mercado, r.periodo, r.factor, r.variable)] = nf.get((r.mercado, r.periodo, r.factor, r.variable), 0) + 1
    for (merc, per, f), g in specs.groupby(["mercado", "periodo", "factor"]):
        fam_f = sum(v for (m_, p_, f_, _), v in nf.items() if (m_, p_, f_) == (merc, per, f))
        filas.append(_resumir(g, merc, per, f, "TODAS", len(g) + fam_f))
        for var, gv in g.groupby("variable"):
            filas.append(_resumir(gv, merc, per, f, var, len(gv) + nf.get((merc, per, f, var), 0)))
    res = pd.DataFrame(filas)
    if res.empty:
        return res
    res["variable_principal"] = ""
    for c_ in ("cumple_R3", "cumple_multiverso_familia", "cumple_R3_rejilla"):
        res[c_] = pd.Series([None] * len(res), dtype=object)
    for (merc, per, f), g in res.groupby(["mercado", "periodo", "factor"]):
        vars_ = [v for v in g["variable"] if v != "TODAS"]
        orden = [c.clave for c in C.POR_FAMILIA[f]]
        noint = set(specs[(specs["mercado"] == merc) & (specs["periodo"] == per) & (specs["factor"] == f) & (~specs["interpolada"])]["variable"])
        cand = [v for v in orden if v in noint] or [v for v in orden if v in vars_]
        if not cand:
            continue
        pr = cand[0]
        rp = g[g["variable"] == pr].iloc[0]
        it = g[g["variable"] == "TODAS"].index[0]
        res.loc[it, "variable_principal"] = pr
        res.loc[it, "cumple_multiverso_familia"] = bool(g.loc[it, "cumple_multiverso"])
        res.loc[it, "cumple_R3"] = bool(g.loc[it, "cumple_multiverso"] and rp["cumple_multiverso"])
        res.loc[it, "cumple_multiverso"] = res.loc[it, "cumple_R3"]   # §9 / R3: familia Y variable principal
        res.loc[it, "cumple_R3_rejilla"] = bool(g.loc[it, "cumple_multiverso_rejilla"] and rp["cumple_multiverso_rejilla"])
        res.loc[g.index[g["variable"] == pr], "variable_principal"] = "principal"
    return res


def grafico(res, out):
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
    except Exception:  # noqa: BLE001
        return False
    t = res[(res["variable"] == "TODAS") & (res["periodo"] == "completo")]
    if t.empty:
        return False
    fig, axs = plt.subplots(1, t["mercado"].nunique(), figsize=(7, 2.8), sharex=True, squeeze=False)
    for ax, (m, g) in zip(axs[0], t.groupby("mercado")):
        g = g.set_index("factor").reindex([f for f in C.FAM_ORDEN if f in set(g["factor"])])
        yy = np.arange(len(g))
        ax.hlines(yy, g["p05"], g["p95"], color="#555")
        ax.plot(g["beta_std_mediana"], yy, "o", color="#1f4e79")
        ax.axvline(0, color="k", lw=0.6)
        ax.set_yticks(yy)
        ax.set_yticklabels(g.index, fontsize=6)
        ax.set_title(f"{m}, completo: beta tipificado (p05-p95)", fontsize=7)
        ax.tick_params(axis="x", labelsize=6)
    fig.tight_layout()
    fig.savefig(out / "especificaciones.png", dpi=80)
    plt.close(fig)
    return True


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--rapido", action="store_true")
    ap.add_argument("--salida", default=str(RAIZ / "output" / "v8" / "M7"))
    a = ap.parse_args(argv)
    t0 = time.perf_counter()
    out = Path(a.salida)
    out.mkdir(parents=True, exist_ok=True)
    reg = Registry(out / "registro.csv")
    d = C.cargar()
    if a.rapido:
        mercados, defl, trs, pers, ret = {"compra": ["tasado"], "alquiler": ["ipc_alquiler"]}, ["ipc"], ["interanual"], ["P3", "completo"], (0, 1)
    else:
        mercados, defl, trs, pers, ret = C.MEDIDAS, ["ipc", "pib"], ["interanual", "trimestral"], list(C.PERIODOS), (0, 1, 4)
    celdas = construir_celdas(d, mercados, defl, trs, pers)
    desc = descriptores(celdas, ret, ("HAC4", "EWC"), d)
    print(f"[M7] rejilla = {len(desc)} especificaciones (tope {MAX_SPECS})", flush=True)
    specs, fall, truncado, n_rej = correr(d, celdas, desc, reg)
    res = resumen_multiverso(specs, fall)
    specs.drop(columns=[]).to_csv(out / "especificaciones.csv", index=False)
    fall.to_csv(out / "fallidas.csv", index=False)
    res.to_csv(out / "resumen_multiverso.csv", index=False)
    reg.flush()
    graf = grafico(res, out)
    escribir_resultado(out, a, specs, fall, res, truncado, n_rej, len(reg.rows), time.perf_counter() - t0, graf, celdas)
    print(f"[M7] fin: {len(specs)} ajustadas, {len(fall)} fallidas/omitidas, registro={len(reg.rows)} ({(time.perf_counter() - t0) / 60:.1f} min)", flush=True)
    return out


def escribir_resultado(out, a, specs, fall, res, truncado, n_rej, nreg, seg, graf, celdas):
    fac = res[res["variable"] == "TODAS"]
    cumple = fac[fac["cumple_multiverso"].astype(bool)]
    cum_rej = fac[fac["cumple_R3_rejilla"].astype(bool)]
    trunc = fac[fac["multiverso_truncado"].astype(bool)]
    est = {"n_factor_periodo_mercado": int(len(fac)), "n_cumplen_multiverso": int(len(cumple)),
           "n_cumplen_solo_familia_orientada": int(fac["cumple_multiverso_familia"].astype(bool).sum()),
           "n_cumplen_R3_rejilla_completa": int(len(cum_rej)), "n_celdas_multiverso_truncado": int(len(trunc)),
           "celdas_truncadas": sorted({f"{m}|{p}" for m, p in zip(trunc["mercado"], trunc["periodo"])}),
           "cumplen": [f"{r.mercado}|{r.periodo}|{r.factor} ({r.signo_mayoritario}, signo {r.pct_mismo_signo:.0%}, BH {r.pct_sig_bh:.0%})" for r in cumple.itertuples()],
           "signo_estable_80": int((fac["pct_mismo_signo"] >= 0.80).sum()), "sig_bh_50": int((fac["pct_sig_bh"] >= 0.50).sum())}
    j = {"rama": "M7", "pregunta": "¿Es estable el signo y la significacion del coeficiente de cada factor ante decisiones razonables del analista "
         "(medida, deflactor, transformacion, periodo, variable, controles, retardos, errores, ficticias)?",
         "capa": "C4", "datos": "data/processed/v8/nacional_q_v8.csv", "N": {"especificaciones_ajustadas": int(len(specs)), "rejilla": int(n_rej),
                                                                       "fallidas_u_omitidas": int(len(fall)), "tope": MAX_SPECS, "truncado": bool(truncado)},
         "metodo": "OLS con errores HAC (Newey-West 4) o EWC; beta tipificado; BH q=0,10 por mercado y periodo sobre todas las especificaciones; "
                   "cumple_multiverso (R3) = signo ORIENTADO (tipos x-1) estable >=80 % y significativo tras BH >=50 % en la familia (TODAS) Y en su variable principal; "
                   "pct_*_rejilla cuentan las fallidas como «no cumple»; P4 y compra P1 marcados «multiverso truncado»",
         "estimacion": est, "ic95": "cuantiles p05-p95 del beta tipificado por (mercado, periodo, factor, variable) en resumen_multiverso.csv",
         "p_ajustado": {"metodo": "BH (q=0,10)", "familia": "todas las especificaciones de cada (mercado, periodo)"},
         "nivel_evidencia": "EXPLORATORIO (C4): sensibilidad de asociaciones; sin lenguaje causal",
         "diagnosticos": {"filas_registro": nreg, "celdas": len(celdas), "graf": bool(graf), "nota_P4": "P4 (9 trimestres) casi no admite especificaciones (GL<5): fallidas registradas"},
         "fuera_muestra": {"modelo": "no aplica (multiverso de sensibilidad, no predictivo)", "rmse": None, "dm_vs_ar4": None},
         "notas": ["Clave de cruce para M2/M5: (mercado, periodo, factor) con variable == 'TODAS'; las filas por variable muestran el detalle.",
                   "Las especificaciones con variables interpoladas se marcan (interpolada) y se resumen aparte (columnas *_sin_interp).",
                   "Alquiler: sin medida alternativa trimestral nacional (SERPAVI es anual; fianzas son regionales): una sola medida.",
                   "El BH usa todas las especificaciones (muy correlacionadas): es un criterio de sensibilidad, no una inferencia independiente.",
                   "Los controles usan siempre la variable principal no interpolada de cada familia; la variable alternativa varia solo en el factor focal."],
         }
    (out / "tiempos.json").write_text(json.dumps({"segundos": round(seg, 1)}))
    (out / "resultado.json").write_text(json.dumps(j, ensure_ascii=False, indent=2, default=str))
    L = ["# M7 - multiverso estructurado (capa C4: sensibilidad)", "",
         f"Rejilla {n_rej} especificaciones (tope {MAX_SPECS}); ajustadas {len(specs)}; fallidas u omitidas {len(fall)} (todas en registro.csv). "
         f"{'TRUNCADO por muestreo determinista.' if truncado else 'Sin truncar.'}", "",
         "Regla del multiverso (§9, R3): signo ORIENTADO (tipos x-1) estable en >=80 % y significativo tras BH (q=0,10) en >=50 % de las especificaciones, "
         "en la familia y en su variable principal. Las fallidas cuentan como «no cumple» en las columnas *_rejilla; P4 y compra P1: multiverso truncado. "
         f"Cumplen {len(cumple)} de {len(fac)} combinaciones (mercado, periodo, factor).", "",
         "| mercado | periodo | factor | n | % signo | signo | % sig BH | beta_std mediana [p05, p95] |", "|---|---|---|---|---|---|---|---|"]
    for r in cumple.sort_values(["mercado", "periodo", "factor"]).itertuples():
        L.append(f"| {r.mercado} | {r.periodo} | {r.factor} | {r.n_multiverso} | {r.pct_mismo_signo:.0%} | {r.signo_mayoritario} | {r.pct_sig_bh:.0%} | "
                 f"{r.beta_std_mediana:.2f} [{r.p05:.2f}, {r.p95:.2f}] |")
    if cumple.empty:
        L.append("| (ninguna combinacion cumple la regla) | | | | | | | |")
    L += ["", "Clave de cruce para M2/M5: `resumen_multiverso.csv`, filas con variable = TODAS, por (mercado, periodo, factor).",
          "Sin lenguaje causal: estas son asociaciones; el multiverso mide la sensibilidad a decisiones del analista, no identifica efectos.",
          "Alquiler sin medida alternativa trimestral nacional; P4 (9 trimestres) casi sin especificaciones viables (GL<5)."]
    (out / "resumen.md").write_text("\n".join(L) + "\n")


if __name__ == "__main__":
    main()
