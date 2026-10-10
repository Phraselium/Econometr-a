"""Rama BA (alquiler): H1 confirmatoria (parte de entrenamiento), periodos, contribuciones, turismo, OOS.

Uso:  python3 src/v2/ba_run.py [--smoke]
Salidas en output/v2/BA/ (smoke en output/v2/BA/smoke/). Determinista, sin red, SEED=20261010.
NO usa la muestra sellada: solo v2_common.load (= holdout.load_train).
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import ba_lib as bl  # noqa: E402  (fija 1 hilo BLAS antes de numpy)

import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402
from scipy import stats  # noqa: E402

import econ_utils as eu  # noqa: E402
import v2_common as vc  # noqa: E402

SMOKE = "--smoke" in sys.argv
OUT = bl.OUT / ("smoke" if SMOKE else "")
OUT.mkdir(parents=True, exist_ok=True)
B_BOOT = 199 if SMOKE else 9999
Q0, Q1 = ("2010Q1", "2019Q4") if SMOKE else ("2008Q1", "2024Q2")
CLAVE = ["d4_ln_pob_20_34", "d4_ln_pob_extranj"]            # coeficientes de interés de H1 (signo +)
FAMILIAS = {"demografia": ["d4_ln_pob_20_34", "d4_ln_pob_extranj"], "empleo_renta": ["d4_ln_ocupados"],
            "oferta": ["x_oferta_l4"], "coste_uso": ["x_cu"], "turismo_VUT": ["d4_ln_vut_viviendas"]}
FAM_A = {"demografia": ["d_ln_pob_20_34", "d_ln_pob_extranj"], "empleo_renta": ["d_ln_ocupados", "d_ln_pib_pc"],
         "oferta": ["x_oferta_l1"], "coste_uso": ["x_cu"]}

LOG = bl.Log(OUT / "registro.csv")
TABLAS: dict = {}


def guardar(nombre, df, idx=False):
    df = df.copy()
    for c in df.columns:
        if pd.api.types.is_float_dtype(df[c]):
            df[c] = df[c].round(10)
    df.to_csv(OUT / nombre, index=idx)


def cargar():
    pq = bl.preparar_prov_q(vc.load("panel_prov_q"))
    pq["cod_prov"] = pq["cod_prov"].astype(str)
    pa = bl.preparar_prov_a(vc.load("panel_prov_a"), pq)
    pm = vc.load("panel_muni_a")
    pm["cod_prov"] = pm["cod_prov"].astype(str)
    if SMOKE:
        provs = sorted(pq["cod_prov"].unique())
        rng = np.random.default_rng(vc.SEED)
        sel = sorted(rng.choice(provs, 10, replace=False).tolist())
        pq, pa, pm = (x[x["cod_prov"].isin(sel)].copy() for x in (pq, pa, pm))
        print("SMOKE provincias:", sel)
    return pq, pa, pm


def muestra_h1(pq):
    return pq[(pq["trimestre"] >= Q0) & (pq["trimestre"] <= Q1)]


def spec(fase, sid, d, y, xs, fe=("cod_prov", "trimestre"), cluster="cod_prov", interes=None, boot=(), B=0,
         notas="", extra=None):
    r = bl.fe_ols(d, y, xs, fe=fe, cluster=cluster, boot_vars=boot, B=B)
    LOG.spec(fase, sid, f"{y} ~ " + " + ".join(xs) + " | FE(" + ",".join(fe) + ") cl=" + cluster, r,
             interes or xs[0], notas)
    return r, bl.tabla_res(r, sid, extra)


# ======================================================================= 1. H1
def tarea_h1(pq, pa):
    d = muestra_h1(pq)
    r, t = spec("H1", "H1_principal", d, bl.H1_Y, bl.H1_X, interes="d4_ln_pob_20_34", boot=bl.H1_X, B=B_BOOT,
                notas=f"PRE-REGISTRADA. WCR Webb B={B_BOOT}. Población interpolada intra-anual (MARCADA: "
                      "pob_*_metodo=interpolado_loglineal en T2-T4)")
    tabs = [t]
    # Holm sobre los dos contrastes de interés (bootstrap, bilateral)
    pb = {v: r["p_boot"][v] for v in CLAVE}
    holm = eu.holm(pb)
    t["p_holm_H1"] = t["var"].map(holm)
    TABLAS["h1_principal"] = r
    # --- robustez (submuestras) : mismas variables, EE cluster
    rob, filas = {}, []

    def corre(sid, dd, **kw):
        rr, tt = spec("H1_rob", sid, dd, bl.H1_Y, bl.H1_X, interes="d4_ln_pob_20_34", notas="robustez H1", **kw)
        tt["submuestra"] = sid
        filas.append(tt)
        rob[sid] = rr
    pre = d["trimestre"]
    corre("excl_COVID_2020-21", d[(pre < "2020Q1") | (pre > "2021Q4")])
    corre("pre_COVID_2008-2019", d[pre <= "2019Q4"])
    corre("desde_2014", d[pre >= "2014Q1"])
    corre("excl_Madrid_Barcelona", d[~d["cod_prov"].isin(["28", "08"])])
    corre("excl_5_grandes", d[~d["cod_prov"].isin(["28", "08", "46", "41", "03"])])
    corre("solo_T1_pob_observada", d[d["trimestre"].str.endswith("Q1")])
    if not SMOKE:
        for cc in sorted(d["ccaa"].unique()):
            corre(f"sin_CCAA_{cc}", d[d["ccaa"] != cc])
    dq = d.copy()
    dq["qa"] = dq["trimestre"].str[-1]
    rq, tq_ = spec("H1_rob", "H1_sin_FE_tiempo(FE_prov+trim_del_año)", dq, bl.H1_Y, bl.H1_X, fe=("cod_prov", "qa"),
                   interes="d4_ln_pob_20_34", notas="variante SIN efectos de tiempo (identifica también con la "
                   "serie temporal común); NO entra en el criterio de signos pre-fijado")
    tq_["submuestra"] = "variante_sin_FE_tiempo"
    filas.append(tq_)
    # --- anual (panel_prov_a): población observada, sin interpolación
    da = pa[(pa["anio"] >= max(2008, int(Q0[:4]))) & (pa["anio"] <= min(2023, int(Q1[:4])))]
    ra, ta = spec("H1_rob", "H1_anual_ipc", da, "d_ln_ipc_alquiler",
                  ["d_ln_pob_20_34", "d_ln_pob_extranj", "d_ln_ocupados"], fe=("cod_prov", "anio"),
                  interes="d_ln_pob_20_34", boot=["d_ln_pob_20_34", "d_ln_pob_extranj", "d_ln_ocupados"],
                  B=B_BOOT, notas="robustez anual, Δ ln anual, pob 1 enero observada; WCR")
    ta["submuestra"] = "anual_ipc"
    filas.append(ta)
    rob["anual_ipc"] = ra
    ds = da[da["anio"] >= 2012]
    rs, ts = spec("H1_rob", "H1_anual_serpavi", ds, "d_ln_serpavi_mediana_vc",
                  ["d_ln_pob_20_34", "d_ln_pob_extranj", "d_ln_ocupados"], fe=("cod_prov", "anio"),
                  interes="d_ln_pob_20_34", notas="robustez: SERPAVI mediana alquiler vivienda colectiva (AEAT)")
    ts["submuestra"] = "anual_serpavi"
    filas.append(ts)
    robdf = pd.concat(filas, ignore_index=True)
    # criterio de robustez fijado ANTES de mirar resultados: signo + en las dos variables clave en
    # TODAS las submuestras trimestrales y en el panel anual (ipc)
    k1 = robdf[robdf["var"].isin(["d4_ln_pob_20_34", "d_ln_pob_20_34", "d4_ln_pob_extranj",
                                  "d_ln_pob_extranj"]) & (robdf["submuestra"] != "anual_serpavi")]
    k1 = k1[k1["submuestra"] != "variante_sin_FE_tiempo"]
    signos = k1.groupby("var")["coef"].agg(lambda s: bool((s > 0).all()))
    TABLAS["h1_robustez"] = robdf
    guardar("h1_principal.csv", pd.concat(tabs))
    guardar("h1_robustez.csv", robdf)
    return d, r, holm, signos, robdf, k1


# ======================================================================= 2. periodos y contribuciones
def interacciones(d, xs, periodos=None):
    d = d.copy()
    per = periodos or [p for p in bl.PERIODOS if (d["periodo"] == p).sum() >= 30]
    cols = []
    for x in xs:
        for p in per:
            c = f"{x}__{p}"
            d[c] = d[x] * (d["periodo"] == p)
            cols.append(c)
    return d, cols, per


def wald_igualdad(res, x, per):
    """Wald H0: coeficientes de x iguales en todos los periodos (F(q, G-1))."""
    nm = res["names"]
    idx = [nm.index(f"{x}__{p}") for p in per]
    if len(idx) < 2:
        return np.nan, np.nan
    R = np.zeros((len(idx) - 1, len(nm)))
    for i in range(len(idx) - 1):
        R[i, idx[i]], R[i, idx[i + 1]] = 1, -1
    b = R @ res["beta"]
    W = float(b @ np.linalg.solve(R @ res["V"] @ R.T, b))
    q = len(idx) - 1
    return W / q, float(stats.f.sf(W / q, q, res["G"] - 1))


def tarea_periodos(d):
    xs = bl.H1_X
    dd, cols, per = interacciones(d, xs)
    r, t = spec("periodos", "P_coef_por_periodo_FEprov_trim", dd, bl.H1_Y, cols,
                interes=f"{CLAVE[0]}__{per[0]}", notas="EXPLORATORIO: H1 con coeficientes por periodo; BH sobre la familia")
    t["x"] = t["var"].str.split("__").str[0]
    t["periodo"] = t["var"].str.split("__").str[1]
    qv = bl.bh(dict(zip(t["var"], t["p"])))
    t["q_BH"] = t["var"].map(qv)
    t["p_Holm"] = t["var"].map(eu.holm(dict(zip(t["var"], t["p"]))))
    w = [dict(x=x, F=wald_igualdad(r, x, per)[0], p_F=wald_igualdad(r, x, per)[1]) for x in xs]
    guardar("periodos_coef.csv", t)
    guardar("periodos_wald_igualdad.csv", pd.DataFrame(w))
    return r, t, pd.DataFrame(w), per


def contribuciones(d, y, xs_fam, fam, fe, fase, sid, cluster="cod_prov", per_list=None, nota="", x_extra=()):
    """Modelo SIN efectos de tiempo (FE provincia [+ trimestre del año]) con coeficientes por periodo;
    contribución_{f,P} = β_{x,P} × media_P(x). IC95: t(G-1), EE cluster (los shocks comunes no
    se recogen: los IC de variables nacionales como coste de uso están subestimados)."""
    todas = [x for v in xs_fam.values() for x in v]
    dd, cols, per = interacciones(d.dropna(subset=[y] + todas), todas, per_list)
    r, t = spec(fase, sid, dd, y, cols, fe=fe, cluster=cluster, interes=cols[0], notas=nota)
    nm = r["names"]
    sam = r["data"]
    filas = []
    tq = stats.t.ppf(0.975, r["G"] - 1)
    ybar = float(sam[y].mean())
    for ref in ("cero", "media_muestra"):
        for p in per:
            sp = sam[sam["periodo"] == p]
            ym = float(sp[y].mean()) - (ybar if ref == "media_muestra" else 0.0)
            tot = {}
            for f, xl in xs_fam.items():
                c = np.zeros(len(nm))
                for x in xl:
                    c[nm.index(f"{x}__{p}")] = _media(dd, sam, p, x) - (float(sam[x].mean()) if ref == "media_muestra" else 0.0)
                val = float(c @ r["beta"])
                se = float(np.sqrt(c @ r["V"] @ c))
                filas.append(dict(spec=sid, referencia=ref, periodo=p, familia=f, contrib=val, se=se,
                                  lo=val - tq * se, hi=val + tq * se, y_medio=ym, n_periodo=len(sp)))
                tot[f] = val
            filas.append(dict(spec=sid, referencia=ref, periodo=p, familia="NO_EXPLICADO(const FE+residuo)",
                              contrib=ym - sum(tot.values()), se=np.nan, lo=np.nan, hi=np.nan, y_medio=ym,
                              n_periodo=len(sp)))
    return r, t, pd.DataFrame(filas)


def _media(dd, sam, p, x):
    """Media de x (original, no interactuada) en el periodo p dentro de la muestra de estimación."""
    s = sam[sam["periodo"] == p]
    return float(s[x].mean())


def tarea_contribuciones(pq, pa):
    d = muestra_h1(pq).copy()
    d["qa"] = d["trimestre"].str[-1]
    fam_h1 = {k: v for k, v in FAMILIAS.items() if k in ("demografia", "empleo_renta")}
    fam_ext = {k: v for k, v in FAMILIAS.items() if k in ("demografia", "empleo_renta", "oferta", "coste_uso")}
    out, tabs = [], {}
    r1, t1, c1 = contribuciones(d, bl.H1_Y, fam_h1, "contrib", ("cod_prov", "qa"), "contrib", "C1_Q_H1vars_sinFEt",
                                nota="EXPLORATORIO: variables H1, FE prov + trimestre del año, coef. por periodo")
    r2, t2, c2 = contribuciones(d, bl.H1_Y, fam_ext, "contrib", ("cod_prov", "qa"), "contrib", "C2_Q_extendido",
                                nota="EXPLORATORIO: + oferta (terminadas/1000 hab. 4T, Δ4 ln, retardo 4T) y coste de uso "
                                     "(Δ4 pp, nacional); muestra desde 2010Q4")
    for t_, nm in ((t1, "C1"), (t2, "C2")):
        t_["x"] = t_["var"].str.split("__").str[0]
        t_["periodo"] = t_["var"].str.split("__").str[1]
    # VUT trimestral (2021Q3-2024Q1: solo P3/P4)
    dv = d[d["d4_ln_vut_viviendas"].notna()].copy()
    fam_v = {"demografia": FAMILIAS["demografia"], "empleo_renta": FAMILIAS["empleo_renta"],
             "turismo_VUT": FAMILIAS["turismo_VUT"]}
    cv = None
    if len(dv) > 50:
        dv["periodo"] = dv["periodo"].fillna("P4")
        cvr, cvt, cv = contribuciones(dv, bl.H1_Y, fam_v, "contrib", ("cod_prov", "qa"), "contrib", "C3_Q_VUT",
                                      nota="EXPLORATORIO: VUT INE (observada, semestral irregular) 2021Q3-2024Q1; "
                                           "coef. por periodo con N muy corto", per_list=["P3", "P4"])
        cvt["x"] = cvt["var"].str.split("__").str[0]
        cvt["periodo"] = cvt["var"].str.split("__").str[1]
        guardar("contrib_coef_C3_VUT.csv", cvt)
    # Anual con PIB pc (sí hay PIB provincial solo anual)
    da = pa[(pa["anio"] >= max(2008, int(Q0[:4]))) & (pa["anio"] <= min(2023, int(Q1[:4])))].copy()
    r4, t4, c4 = contribuciones(da, "d_ln_ipc_alquiler", FAM_A, "contrib", ("cod_prov",), "contrib", "C4_A_extendido",
                                nota="EXPLORATORIO anual: + Δ ln PIB pc nominal (CRE), oferta (retardo 1 año), coste de uso "
                                     "(media anual); sin efectos de año")
    t4["x"] = t4["var"].str.split("__").str[0]
    t4["periodo"] = t4["var"].str.split("__").str[1]
    cont = pd.concat([c1, c2, c4] + ([cv] if cv is not None else []), ignore_index=True)
    guardar("contribuciones_por_periodo.csv", cont)
    guardar("contrib_coef_C1.csv", t1)
    guardar("contrib_coef_C2.csv", t2)
    guardar("contrib_coef_C4_anual.csv", t4)
    return cont, t2, t4


# ======================================================================= 3. turismo
def tarea_turismo(pq, pm):
    filas = []
    m = pm.copy()
    wide = m.pivot_table(index=["cod_muni", "cod_prov"], columns="anio",
                         values=["serpavi_mediana_vc", "serpavi_n_vc", "vut_viviendas", "uu_residenciales"])
    w = pd.DataFrame({
        "cod_prov": [i[1] for i in wide.index],
        "s17": wide[("serpavi_mediana_vc", 2017)].values if ("serpavi_mediana_vc", 2017) in wide else np.nan,
    }, index=wide.index)
    for nm, (v, a) in dict(s20=("serpavi_mediana_vc", 2020), s23=("serpavi_mediana_vc", 2023),
                            n20=("serpavi_n_vc", 2020), n23=("serpavi_n_vc", 2023),
                            v20=("vut_viviendas", 2020), v23=("vut_viviendas", 2023),
                            u20=("uu_residenciales", 2020)).items():
        w[nm] = wide[(v, a)].values if (v, a) in wide else np.nan
    w = w.reset_index(drop=True)
    w["dlny"] = np.log(w["s23"] / w["s20"])
    w["dlny_pre"] = np.log(w["s20"] / w["s17"])
    w["dvut"] = (w["v23"] - w["v20"]) / w["u20"] * 1000
    w["vut20"] = w["v20"] / w["u20"] * 1000
    w["ln_u20"] = np.log(w["u20"])
    w["ln_s20"] = np.log(w["s20"])
    base = w[(w["u20"] > 0) & np.isfinite(w["dlny"]) & w["dvut"].notna()].copy()
    lo, hi = base["dvut"].quantile([0.01, 0.99])
    base["dvut_w"] = base["dvut"].clip(lo, hi)
    base["uno"] = 1
    casos = [
        ("T_muni_base", base, "dlny", ["dvut"], "Δ ln SERPAVI vc 2020→2023 ~ Δ VUT por 1.000 uu residenciales; FE provincia"),
        ("T_muni_controles", base, "dlny", ["dvut", "ln_u20", "ln_s20"], "+ ln tamaño (uu) y ln alquiler inicial"),
        ("T_muni_winsor", base, "dlny", ["dvut_w"], "ΔVUT winsorizada p1-p99"),
        ("T_muni_u20_5000", base[base["u20"] >= 5000], "dlny", ["dvut"], "municipios con >=5.000 uu residenciales"),
        ("T_muni_n_ge_30", base[(base["n20"] >= 30) & (base["n23"] >= 30)], "dlny", ["dvut"],
         "SERPAVI con >=30 contratos en 2020 y 2023"),
        ("T_muni_PLACEBO_pretend", base[np.isfinite(base["dlny_pre"])], "dlny_pre", ["dvut"],
         "PLACEBO: Δ ln SERPAVI 2017→2020 (anterior) ~ ΔVUT 2020→2023; detecta selección/causalidad inversa"),
    ]
    for sid, dd, y, xs, nota in casos:
        if len(dd) < 30:
            continue
        r, t = spec("turismo", sid, dd, y, xs, fe=("cod_prov",), interes="dvut" if "dvut" in xs else xs[0],
                    notas="EXPLORATORIO. " + nota + ". Sin identificación: causalidad inversa/selección posibles; N temporal=2")
        t["nota"] = nota
        filas.append(t)
    # provincial trimestral: VUT observada 2020Q3-2024Q1 (Δ4 con ambos extremos observados)
    d = muestra_h1(pq).copy()
    d["vut_pc"] = d["vut_viviendas"] / d["pob_total"] * 1000
    d["d4_vut_pc"] = d["vut_pc"] - d.groupby("cod_prov", sort=False)["vut_pc"].shift(4)
    dv = d[d["d4_ln_vut_viviendas"].notna()]
    if len(dv) > 60:
        for sid, xs in (("T_prov_dlnVUT", ["d4_ln_vut_viviendas"]),
                        ("T_prov_dlnVUT_H1", ["d4_ln_vut_viviendas"] + bl.H1_X),
                        ("T_prov_dVUTpc", ["d4_vut_pc"])):
            r, t = spec("turismo", sid, dv, bl.H1_Y, xs, interes=xs[0],
                        notas="EXPLORATORIO. VUT INE provincial observada (Δ4 solo donde ambos extremos observados: "
                              "2021Q3,2022Q1,2022Q3,2023Q1,2023Q3,2024Q1); N temporal=6")
            t["nota"] = "provincial trimestral"
            filas.append(t)
    tab = pd.concat(filas, ignore_index=True)
    guardar("turismo.csv", tab)
    return tab


# ======================================================================= 4. fuera de muestra
def tarea_oos(pq):
    d = pq[pq["trimestre"] <= (Q1 if SMOKE else "2024Q2")].copy()
    desde = "2015Q1" if SMOKE else "2012Q1"
    kw = dict(desde=desde, min_train=36)
    nac = vc.load("nacional_q_v2")
    ar4 = vc.panel_ar4(d, "ipc_alquiler", "cod_prov", 4, real=False, nac=nac, **kw)
    ecm = vc.panel_ecm_v1(d, "ipc_alquiler", "cod_prov", 4, real=False, nac=nac, **kw)
    cfgs = {bl.PRIMARIO: bl.CONFIGS[bl.PRIMARIO]} if SMOKE else bl.CONFIGS
    pres = vc.Presupuesto(LOG.reg, "OOS", 6, "BA: modelos con variables de H1 (4 configuraciones declaradas; "
                                           "primario B_AR4_mas_H1 fijado antes de ver resultados)")
    preds = {}
    for nm, cfg in cfgs.items():
        preds[nm] = bl.predecir_modelo(d, nm, cfg, **kw)
    com = bl.muestra_comun({**preds, vc.BASE: ar4, vc.ECM: ecm})
    filas = []
    for nm in cfgs:
        r = vc.evaluar(com[nm], {vc.BASE: com[vc.BASE], vc.ECM: com[vc.ECM]}, 4)
        r["primario"] = nm == bl.PRIMARIO
        filas.append(r)
        pres.usar(nm, cfgs[nm], formula=f"y(t+4)=ln IPCalq(t+4)-ln IPCalq(t) ~ {cfgs[nm]}", muestra_ini=desde,
                  muestra_fin="2024Q2", n=int(r["n"].iloc[0]), rmse_oos=float(r["rmse"].iloc[0]),
                  notas="h=4, embargo 4, ventana expansiva; DM-HLN panel")
    # líneas base evaluadas contra sí mismas (muestra común)
    rb = {}
    for etq in (vc.BASE, vc.ECM):
        e = com[etq]
        rb[etq] = float(np.sqrt(np.mean((e["y_real"] - e["y_pred"]) ** 2)))
        vc.registrar(LOG.reg, "OOS_base", etq, "línea base panel", desde, "2024Q2", int(len(e)), rb[etq])
    tab = pd.concat(filas, ignore_index=True)
    ref = rb[vc.BASE]
    tab["razon_rmse_vs_AR4"] = tab["rmse"] / ref
    tab["razon_rmse_vs_ECM"] = tab["rmse"] / rb[vc.ECM]
    ps = {r["modelo"]: r["p_vs_AR4"] for _, r in tab.iterrows() if np.isfinite(r["p_vs_AR4"])}
    ph = eu.holm(ps) if ps else {}
    tab["p_vs_AR4_holm"] = tab["modelo"].map(ph)
    tab["rmse_ECM_v1_baseline"] = rb[vc.ECM]
    guardar("oos_h4.csv", tab)
    # RMSE por periodo de test (descriptivo) del modelo primario y AR(4)
    c = com[bl.PRIMARIO].copy()
    c["e2_mod"] = (c["y_real"] - c["y_pred"]) ** 2
    c["e2_ar4"] = (com[vc.BASE]["y_real"].values - com[vc.BASE]["y_pred"].values) ** 2
    c["e2_ecm"] = (com[vc.ECM]["y_real"].values - com[vc.ECM]["y_pred"].values) ** 2
    c["anio"] = c["periodo"].str[:4]
    pa = c.groupby("anio")[["e2_mod", "e2_ar4", "e2_ecm"]].mean().pow(0.5).add_prefix("rmse_")
    pa["n"] = c.groupby("anio").size()
    guardar("oos_h4_por_anio.csv", pa.reset_index())
    return tab, rb


# ======================================================================= main
def main():
    pq, pa, pm = cargar()
    d, r_h1, holm, signos, robdf, k1 = tarea_h1(pq, pa)
    per_r, per_t, per_w, per = tarea_periodos(d)
    if SMOKE:
        tab, rb = tarea_oos(pq)
        LOG.flush()
        print(TABLAS["h1_principal"]["beta"], TABLAS["h1_principal"]["p_boot"])
        print(per_t[["var", "coef", "se", "p"]])
        print(tab.T)
        return
    cont, c2, c4 = tarea_contribuciones(pq, pa)
    tur = tarea_turismo(pq, pm)
    tab, rb = tarea_oos(pq)
    LOG.flush()
    import ba_informe as bi
    bi.escribir(OUT, r_h1, holm, signos, robdf, k1, per_t, per_w, cont, c2, c4, tur, tab, rb, LOG)


if __name__ == "__main__":
    main()
