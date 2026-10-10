"""Rama BM: orquestador (bloques 1-4; 5-6 documentados como no ejecutados). Ejecutar: python src/v2/bm_run.py [--smoke]

Objetivos (h=4, y = ln X_{t+4} - ln X_t): A nacional ln IPV real; B panel provincial IPC alquiler; C panel provincial
p_tasado real. Validación SOLO en bloques temporales (v2_common.block_splits, h=4, primer test 2012Q1, embargo 4).
Misma muestra que AR(4) y ECM v1 (v2_common.evaluar). Todo EXPLORATORIO hasta la evaluación sellada de H7.
"""
from __future__ import annotations

import json
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
import bm_lib as bl  # noqa: E402
import bm_modelos as bm  # noqa: E402
import v2_common as vc  # noqa: E402
from econ_utils import Registry  # noqa: E402

OUT = bl.OUT
SMOKE = "--smoke" in sys.argv
if SMOKE:
    OUT = OUT / "smoke"
OUT.mkdir(parents=True, exist_ok=True)
PRES = json.loads((bl.OUT / "presupuesto.json").read_text())
assert (bl.OUT / "regla_H7.md").exists(), "la regla H7 debe existir antes de ejecutar la comparación"
T0 = time.time()
TIEMPOS = {}


def bh(p):
    p = np.asarray(p, float)
    out = np.full(len(p), np.nan)
    ok = ~np.isnan(p)
    pv = p[ok]
    if len(pv) == 0:
        return out
    o = np.argsort(pv)
    adj = pv[o] * len(pv) / (np.arange(len(pv)) + 1)
    adj = np.minimum.accumulate(adj[::-1])[::-1]
    r = np.empty(len(pv))
    r[o] = np.minimum(adj, 1.0)
    out[ok] = r
    return out


# ------------------------------------------------------------------ elección (regla_H7.md)
def rmse_bloques(preds: dict, base_keys, split_of):
    """RMSE medio en bloques sobre la muestra común (ver regla_H7.md). preds: nombre -> df."""
    keyed = {}
    for n, df in preds.items():
        x = df.dropna(subset=["y_real", "y_pred"]).drop_duplicates(["unidad", "periodo"]).set_index(["unidad", "periodo"])
        keyed[n] = x
    elig, cob = {}, {}
    for n, x in keyed.items():
        cob[n] = len(x.index.intersection(base_keys)) / max(len(base_keys), 1)
        elig[n] = cob[n] >= 0.9
    common = base_keys
    for n, x in keyed.items():
        if elig[n]:
            common = common.intersection(x.index)
    res = {}
    for n, x in keyed.items():
        if not elig[n]:
            res[n] = np.nan
            continue
        e = (x.loc[common, "y_real"] - x.loc[common, "y_pred"])
        sp = split_of.loc[common]
        res[n] = float(np.mean([np.sqrt(np.mean(g ** 2)) for _, g in e.groupby(sp.values)]))
    return res, cob, elig, len(common)


def elegir(vals: dict, meta: dict):
    v = {k: x for k, x in vals.items() if not np.isnan(x)}
    mn = min(v.values())
    emp = [k for k, x in v.items() if x <= 1.01 * mn]
    return sorted(emp, key=lambda k: (meta[k]["rank"], meta[k]["orden"]))[0], sorted(emp)


# ------------------------------------------------------------------ objetivos
def preparar(nac, pan):
    obj = {}
    # A
    dA = bl.preparar_nacional(nac)
    famA = bl.familias_con_ar(bl.FAM_NAC)
    longA, perA, uA, colsA = bl.construir_long(dA, "A", famA)
    a = vc.ar4_nacional(nac, "ln_ipv", 4, real=True, desde="2012Q1", min_train=8)
    e = vc.ecm_v1_nacional(nac, 4, desde="2012Q1", min_train=8)
    obj["A"] = dict(long=longA, per=perA, units=["ES"], cols=colsA, fam=famA, base={vc.BASE: a, vc.ECM: e}, d=dA,
                    unit_col=None)
    for o, var, real in (("B", "ipc_alquiler", False), ("C", "p_tasado", True)):
        d = bl.preparar_panel(pan, nac, o)
        fam = bl.familias_con_ar(bl.FAM_PANEL)
        long, per, units, cols = bl.construir_long(d, o, fam, nac)
        a = vc.panel_ar4(pan, var, "cod_prov", 4, real=real, nac=nac, desde="2012Q1", min_train=8)
        e = vc.panel_ecm_v1(pan, var, "cod_prov", 4, real=real, nac=nac, desde="2012Q1", min_train=8)
        obj[o] = dict(long=long, per=per, units=units, cols=cols, fam=fam, base={vc.BASE: a, vc.ECM: e}, d=d,
                      unit_col="unidad")
    for o, v in obj.items():
        sp = v["base"][vc.BASE].attrs["splits"]
        v["splits"] = [(np.array(x), np.array(y)) for x, y in sp]
        assert v["per"] == sorted(v["per"])
    return obj


def candidatos(o, v, nac):
    """Devuelve dict nombre -> (Spec-meta, df predicciones). Cada configuración se registra en Presupuesto."""
    out = {}
    long, per, sp, units, cols = v["long"], v["per"], v["splits"], v["units"], v["cols"]
    specs = bl.specs_enet() + [bl.SPEC_PL]
    if o in ("B", "C"):
        specs += bl.specs_rf() + bl.specs_lgbm()
    if SMOKE:
        specs = specs[:2] + [bl.SPEC_PL]
    for s in specs:
        out[s.nombre] = (dict(clase=s.clase, rank=s.rank, orden=s.orden, spec=s, config=dict(s.params)),
                         bl.correr_bloques(long, per, sp, cols, s, units))
    if o == "A":
        lg, pr, _ = bm._long_ecm(nac)
        assert pr == per
        out["ARDL"] = (dict(clase="ardl", rank=1, orden=0, config={"p": 4, "dx_lags": [0, 1]}), bm.ardl(lg, pr, sp))
        for i, var in enumerate(("asim", "credito")):
            out[f"TAR_ECM_{var}"] = (dict(clase="tar_ecm", rank=3, orden=i, config={"umbral": var}),
                                     bm.tar_ecm(lg, pr, sp, var))
        cols_v = ["dY", "dOcup", "dTipoR", "dCred"]
        for i, lam in enumerate(bm.LAMBDAS):
            df = bm.var_modelos(lg, pr, sp, cols_v, "bvar", lam, f"BVAR_lam{lam}")
            out[f"BVAR_lam{lam}"] = (dict(clase="bvar", rank=3, orden=10 + i, config={"lambda": lam}), df)
            out[f"BVAR_lam{lam}"][0]["logml"] = df.attrs["logml"]
        for i, k in enumerate((0.99, 0.95)):
            out[f"TVPVAR_k{k}"] = (dict(clase="tvpvar", rank=4, orden=i, config={"kappa": k}),
                                   bm.var_modelos(lg, pr, sp, cols_v, "tvp", k, f"TVPVAR_k{k}"))
    return out


def correr_objetivo(o, v, nac, reg, pres):
    cands = candidatos(o, v, nac)
    bases = v["base"]
    for n, (m, df) in cands.items():
        df["modelo"] = n
    ref = None
    for b in bases.values():
        x = b.dropna(subset=["y_real", "y_pred"]).drop_duplicates(["unidad", "periodo"]).set_index(["unidad", "periodo"])
        ref = x.index if ref is None else ref.intersection(x.index)
    a_df = bases[vc.BASE].drop_duplicates(["unidad", "periodo"]).set_index(["unidad", "periodo"])
    split_of = a_df["split"]
    vals, cob, elig, ncom = rmse_bloques({n: df for n, (m, df) in cands.items()}, ref, split_of)
    filas = []
    for n, (m, df) in cands.items():
        if len(df.dropna(subset=["y_real", "y_pred"])) < 8:
            filas.append(dict(modelo=n, objetivo=o, clase=m["clase"], N=0, nota="sin muestra suficiente"))
            pres.usar(f"{o}_{n}", m["config"], formula=f"objetivo {o}", n=0, notas="sin muestra suficiente")
            continue
        r = vc.evaluar(df, bases, 4).iloc[0].to_dict()
        fila = dict(modelo=n, objetivo=o, clase=m["clase"], N=int(r["n"]), n_periodos=int(r["n_periodos"]),
                    RMSE=r["rmse"], MAE=r["mae"], RMSE_AR4=r["rmse_AR4"], RMSE_ECM_v1=r["rmse_ECM_v1"],
                    DM_vs_AR4=r["dm_vs_AR4"], p_vs_AR4=r["p_vs_AR4"], DM_vs_ECM_v1=r["dm_vs_ECM_v1"],
                    p_vs_ECM_v1=r["p_vs_ECM_v1"], cobertura=cob[n], elegible=bool(elig[n]),
                    rmse_bloques_medio=vals[n], n_comun_ranking=ncom)
        filas.append(fila)
        pres.usar(f"{o}_{n}", m["config"], formula=f"y_{{t+4}} ~ familias ({m['clase']})", muestra_ini="2012Q1",
                  muestra_fin=Q_FIN, n=int(r["n"]), rmse_oos=float(r["rmse"]),
                  notas=f"objetivo {o}; DM vs AR4 {r['dm_vs_AR4']:.3f}")
    tab = pd.DataFrame(filas)
    ok = tab["N"] > 0
    tab.loc[ok, "p_BH_AR4"] = bh(tab.loc[ok, "p_vs_AR4"])
    tab.loc[ok, "p_BH_ECM_v1"] = bh(tab.loc[ok, "p_vs_ECM_v1"])
    tab["mejora_ambas_nominal"] = (tab["RMSE"] < tab["RMSE_AR4"]) & (tab["RMSE"] < tab["RMSE_ECM_v1"]) & \
        (tab["p_vs_AR4"] < 0.05) & (tab["p_vs_ECM_v1"] < 0.05)
    meta = {n: m for n, (m, _) in cands.items()}
    sel, emp = elegir({n: vals[n] for n in cands}, meta)
    # filas de las líneas base (misma muestra AR4 ∩ ECM v1)
    base_rows = []
    for bn, bdf in bases.items():
        x = bdf.set_index(["unidad", "periodo"]).loc[ref]
        e = x["y_real"] - x["y_pred"]
        base_rows.append(dict(modelo=bn, objetivo=o, clase="linea_base", N=int(len(x)), RMSE=float(np.sqrt(np.mean(e ** 2))),
                              MAE=float(np.mean(np.abs(e))), elegible=False))
    return tab, base_rows, cands, dict(seleccionado=sel, empatados=emp, vals=vals, cobertura=cob,
                                        n_comun=ncom, meta={k: {kk: vv for kk, vv in m.items() if kk in ("clase", "rank", "orden", "config")}
                                                            for k, m in meta.items()})


Q_FIN = vc.Q_TRAIN_FIN


def tiempo(k):
    TIEMPOS[k] = round(time.time() - T0, 1)


# ------------------------------------------------------------------ importancias (EXPLORATORIO)
def importancias(o, v, cands, tab, reg):
    """Permutación agrupada por familia, SHAP (LightGBM) y ALE para el mejor RF y el mejor LGBM (B y C)."""
    perm_rows, shap_rows, ale_rows = [], [], []
    fam = v["fam"]
    for clase in ("rf", "lgbm"):
        t = tab[(tab["clase"] == clase) & (tab["N"] > 0)]
        if t.empty:
            continue
        best = t.sort_values("rmse_bloques_medio").iloc[0]
        nombre = best["modelo"]
        spec = cands[nombre][0]["spec"]
        mejora = bool(best["RMSE"] < best["RMSE_AR4"] and best["RMSE"] < best["RMSE_ECM_v1"]
                      and best["p_vs_AR4"] < 0.05)
        acc_p, acc_s, tops = [], [], {}
        last = {}

        def guardar(sid, f, sub, raw, fe):
            pg = bl.perm_grupos(f, sub, raw, fe, fam, reps=3)
            pg["periodo_origen"] = sub.loc[pg.index, "trimestre"].map(bl.periodo_de)
            pg["base_mse"] = ((sub.loc[pg.index, "yh"].values - (raw + fe)[sub.index.get_indexer(pg.index)]) ** 2)
            acc_p.append(pg)
            if f.spec.clase == "lgbm":
                sg, cg = bl.shap_grupos(f, sub, fam)
                ok = sub["yh"].notna().values
                sg = sg[ok]
                sg["periodo_origen"] = sub.loc[sg.index, "trimestre"].map(bl.periodo_de)
                acc_s.append(sg)
                for c in cg.columns:
                    tops[c] = tops.get(c, 0.0) + float(cg[c].abs().sum())
            last.update(f=f, sub=sub)
        bl.correr_bloques(v["long"], v["per"], v["splits"], v["cols"], spec, v["units"], guardar=guardar)
        P = pd.concat(acc_p)
        for per_, g in P.groupby("periodo_origen"):
            base = g["base_mse"].mean()
            for fn in fam:
                if fn in g.columns:
                    perm_rows.append(dict(objetivo=o, modelo=nombre, periodo=per_, familia=fn, n=int(len(g)),
                                          delta_mse=float(g[fn].mean()), delta_mse_rel=float(g[fn].mean() / base),
                                          mejora_fuera_muestra=mejora))
        if acc_s:
            S = pd.concat(acc_s)
            for per_, g in S.groupby("periodo_origen"):
                for fn in fam:
                    if fn in g.columns:
                        shap_rows.append(dict(objetivo=o, modelo=nombre, periodo=per_, familia=fn, n=int(len(g)),
                                              abs_shap_medio=float(g[fn].abs().mean()), shap_medio=float(g[fn].mean()),
                                              mejora_fuera_muestra=mejora))
            f, sub = last["f"], last["sub"]
            top3 = [c for c, _ in sorted(tops.items(), key=lambda kv: -kv[1]) if c not in bl.Q_COLS][:3]
            posL = int(v["splits"][-1][0][-1])
            trn = v["long"][(v["long"]["pos"] + 4 <= posL) & v["long"]["yh"].notna()]
            for c in top3:
                al = bl.ale_1d(lambda X, f=f: f.predict_raw(X), trn[f.cols + []].copy(), c)
                al["objetivo"], al["modelo"], al["variable"] = o, nombre, c
                ale_rows.append(al)
    return perm_rows, shap_rows, ale_rows


def colinealidad(o, v):
    d = v["long"]
    d = d[d["yh"].notna()]
    cols = [c for c in v["cols"] if d[c].notna().sum() > 30]
    C = d[cols].corr()
    rows = []
    fam_of = {c: k for k, vs in v["fam"].items() for c in vs}
    for i, a in enumerate(cols):
        for b in cols[i + 1:]:
            r = C.loc[a, b]
            if abs(r) >= 0.7:
                rows.append(dict(objetivo=o, var1=a, fam1=fam_of[a], var2=b, fam2=fam_of[b], rho=float(r)))
    return rows


# ------------------------------------------------------------------ inferencia por periodo (EXPLORATORIO)
PERIODOS_PDS = {"Todo": ("1990Q1", "2024Q2"), "P0_boom": ("2002Q1", "2007Q4"), **bl.PERIODOS}
LP_REGS_PANEL = ["g_pob_20_34", "g_pob_extranj", "d4_ln_ocupados", "d4_ln_hipotecas_importe", "tipo_hip_real",
                 "d4_ln_iniciadas_libres", "d4_ln_vut_viviendas", "n_eventos"]
LP_REGS_NAC = ["g_pob_extranj", "d4_ln_ocupados", "d4_ln_credito_nuevo", "tipo_hip_real", "d4_ln_permisos", "n_eventos"]


def inferencia(o, v):
    long = v["long"]
    long = long[long["yh"].notna()]
    unit = v["unit_col"]
    pds_rows, lp_rows = [], []
    fam = v["fam"]
    for pn, (a, b) in PERIODOS_PDS.items():
        d = long[(long["trimestre"] >= a) & (long["trimestre"] <= b)]
        if len(d) < 25:
            continue
        for fn in fam:
            if fn in ("autorregresivo", "estacional"):
                continue
            r = bl.pds_familia(d, fam, fn, unit)
            pds_rows.append(dict(objetivo=o, periodo=pn, familia=fn, **{k: x for k, x in r.items() if k != "coef"},
                                 coef=json.dumps({c: round(z, 5) for c, z in r.get("coef", {}).items()})))
        lp = bl.lp_periodo(d, LP_REGS_NAC if o == "A" else LP_REGS_PANEL, unit)
        for row in lp or []:
            lp_rows.append(dict(objetivo=o, periodo=pn, **row))
    return pds_rows, lp_rows


def markov_switching(nac):
    """Descriptivo, EN MUESTRA (no se usa fuera de muestra): ECM con intercepto y coeficiente del ECT con cambio de
    régimen markoviano de 2 estados (statsmodels MarkovRegression) sobre Δ ln IPV real."""
    import statsmodels.api as sm
    long, per, units = bm._long_ecm(nac)
    L = int(long["pos"].max())
    r = vc._dols(long, L, "lvl", bm.ECM_X, ["ES"])
    if r is None:
        return {"estado": "DOLS no estimable"}
    ect, _ = r
    lg = long.copy()
    lg["ect_l1"] = ect(lg).shift(1)
    d = lg.dropna(subset=["dY", "ect_l1", "dOcup"])
    try:
        m = sm.tsa.MarkovRegression(d["dY"].values, k_regimes=2, exog=d[["ect_l1"]].values, switching_variance=True,
                                    switching_exog=True)
        f = m.fit(disp=False, maxiter=300, search_reps=0)
        pr = pd.DataFrame(f.smoothed_marginal_probabilities, columns=["p_reg0", "p_reg1"])
        pr.insert(0, "trimestre", d["trimestre"].values)
        pr.to_csv(OUT / "markov_probabilidades.csv", index=False)
        return {"estado": "ok", "n": int(len(d)), "loglik": float(f.llf),
                "params": {k: float(x) for k, x in zip(f.model.param_names, f.params)},
                "duraciones_esperadas": [float(x) for x in np.ravel(f.expected_durations)],
                "nota": "descriptivo en muestra con N pequeño; NO se usa como predictor"}
    except Exception as ex:  # noqa: BLE001
        return {"estado": f"fallo: {type(ex).__name__}: {ex}"}


# ------------------------------------------------------------------ main
def main():
    nac, pan = vc.load("nacional_q_v2"), vc.load("panel_prov_q")
    reg = Registry(OUT / "registro.csv")
    pres = vc.Presupuesto(reg, "BM", PRES["n_max_total"], "presupuesto BM declarado en presupuesto.json antes de ejecutar")
    obj = preparar(nac, pan)
    tiempo("preparar")
    tablas, bases_rows, sels, perm, shp, ale, col, pds, lps = [], [], {}, [], [], [], [], [], []
    for o in ("A", "B", "C"):
        tab, br, cands, sel = correr_objetivo(o, obj[o], nac, reg, pres)
        tablas.append(tab)
        bases_rows += br
        sels[o] = sel
        tiempo(f"modelos_{o}")
        if o in ("B", "C"):
            p_, s_, a_ = importancias(o, obj[o], cands, tab, reg)
            perm += p_
            shp += s_
            ale += a_
            tiempo(f"importancias_{o}")
        col += colinealidad(o, obj[o])
        a_, b_ = inferencia(o, obj[o])
        pds += a_
        lps += b_
        tiempo(f"inferencia_{o}")
        if o == "A":
            ml = {n: m.get("logml") for n, (m, _) in cands.items() if m["clase"] == "bvar"}
            sels["A"]["bvar_logml_medio"] = {n: {str(l): float(np.mean([s[l] for s in d.values()])) for l in bm.LAMBDAS}
                                              for n, d in ml.items() if d}
        # guarda las predicciones de los seleccionados y de las bases
        keep = [cands[sel["seleccionado"]][1]] + [obj[o]["base"][k] for k in obj[o]["base"]]
        pd.concat(keep).assign(objetivo=o).to_csv(OUT / f"predicciones_seleccion_{o}.csv.gz", index=False)
    T = pd.concat(tablas + [pd.DataFrame(bases_rows)], ignore_index=True)
    T.to_csv(OUT / "tabla_fuera_muestra.csv", index=False, float_format="%.6g")
    pd.DataFrame(perm).to_csv(OUT / "importancia_permutacion_familias.csv", index=False, float_format="%.6g")
    pd.DataFrame(shp).to_csv(OUT / "importancia_shap_familias.csv", index=False, float_format="%.6g")
    if ale:
        pd.concat(ale).to_csv(OUT / "ale_top3.csv", index=False, float_format="%.6g")
    pd.DataFrame(col).to_csv(OUT / "colinealidad_pares_0.7.csv", index=False, float_format="%.4g")
    P = pd.DataFrame(pds)
    for o, g in P.groupby("objetivo"):
        P.loc[g.index, "p_BH"] = bh(g["p"].values)
    P.to_csv(OUT / "pds_familias_periodos.csv", index=False, float_format="%.6g")
    pd.DataFrame(lps).to_csv(OUT / "proyecciones_locales_periodos.csv", index=False, float_format="%.6g")
    ms = markov_switching(nac)
    (OUT / "markov_switching_descriptivo.json").write_text(json.dumps(ms, indent=1, ensure_ascii=False))
    sel_json = {o: dict(modelo=s["seleccionado"], empatados=s["empatados"], clase=s["meta"][s["seleccionado"]]["clase"],
                        config=s["meta"][s["seleccionado"]]["config"], rmse_bloques=s["vals"][s["seleccionado"]],
                        n_comun_ranking=s["n_comun"], cobertura=s["cobertura"], rmse_bloques_todos=s["vals"],
                        meta=s["meta"]) for o, s in sels.items()}
    (OUT / "seleccion_H7.json").write_text(json.dumps(sel_json, indent=1, ensure_ascii=False, default=str))
    reg.flush()
    usadas = pres.usadas
    (OUT / "presupuesto_usado.json").write_text(json.dumps(
        {"n_max_declarado": pres.n_max, "configuraciones_usadas": usadas,
         "bloque5_factor_dinamico": "no ejecutado", "bloque6_deep_learning": "no ejecutado (torch no instalado)"}, indent=1))
    informe(T, sel_json, P, pd.DataFrame(perm), pd.DataFrame(shp), pd.DataFrame(lps), ms, usadas)
    tiempo("fin")
    (OUT.parent / "BM_tiempos.json").write_text(json.dumps(TIEMPOS, indent=1)) if not SMOKE else None


def informe(T, sel, P, perm, shp, lps, ms, usadas):
    from bm_informe import escribir
    escribir(OUT, T, sel, P, perm, shp, lps, ms, usadas)


if __name__ == "__main__":
    main()
