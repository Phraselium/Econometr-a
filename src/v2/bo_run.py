"""Rama BO (oferta y suelo): H4 (confirmatoria), déficit, suelo, panel UE y fuera de muestra.

Uso:  python3 src/v2/bo_run.py [--smoke]
Salidas en output/v2/BO/ (smoke en output/v2/BO/smoke/). Determinista, sin red, SEED=20261010.
NO usa la muestra sellada: solo v2_common.load (= holdout.load_train).
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import bo_lib as bl  # noqa: E402  (fija 1 hilo BLAS antes de numpy)

import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402
from scipy import stats  # noqa: E402

import v2_common as vc  # noqa: E402

SMOKE = "--smoke" in sys.argv
OUT = bl.OUT / ("smoke" if SMOKE else "")
OUT.mkdir(parents=True, exist_ok=True)
B_MAIN = 199 if SMOKE else 9999
B_SUB = 199 if SMOKE else 1999
A0, A1 = (2009, 2015) if SMOKE else (2005, 2023)
LOG = bl.Log(OUT / "registro.csv")
RES: dict = {}


def guardar(nombre, df, idx=False):
    df = df.copy()
    for c in df.columns:
        if pd.api.types.is_float_dtype(df[c]):
            df[c] = df[c].round(10)
    df.to_csv(OUT / nombre, index=idx)


def cargar():
    pa = vc.load("panel_prov_a")
    pq = vc.load("panel_prov_q")
    nq = vc.load("nacional_q_v2")
    pa["cod_prov"] = pa["cod_prov"].astype(str)
    pq["cod_prov"] = pq["cod_prov"].astype(str)
    if SMOKE:
        provs = sorted(pa["cod_prov"].unique())
        rng = np.random.default_rng(vc.SEED)
        sel = sorted(rng.choice(provs, 14, replace=False).tolist())
        pa, pq = (x[x["cod_prov"].isin(sel)].copy() for x in (pa, pq))
        pa, pq = pa[pa["anio"] <= 2015].copy(), pq[pq["trimestre"].astype(str) <= "2015Q4"].copy()
        nq = nq[nq["trimestre"].astype(str) <= "2015Q4"].copy()
        print("SMOKE provincias:", sel)
    return pa, pq, nq


# ======================================================================= 1. H4
Y = "d_ln_ini"
XP = ["d_ln_pr_l1", "inter"]


def spec(fase, sid, d, y, xs, interes, boot=(), B=0, notas="", fe=("cod_prov", "anio")):
    r = bl.fe_ols(d, y, xs, fe=fe, cluster="cod_prov", boot_vars=boot, B=B)
    LOG.spec(fase, sid, f"{y} ~ " + " + ".join(xs) + " | FE(" + ",".join(fe) + ") cl=cod_prov", r, interes, notas)
    return r


def iut(r, v1="d_ln_pr_l1", v2="inter"):
    p1, p2 = bl.p_unilateral(r, v1, +1), bl.p_unilateral(r, v2, -1)
    return p1, p2, max(p1, p2)


def fila_h4(sid, r, extra=None, v1="d_ln_pr_l1", v2="inter"):
    i1, i2 = r["names"].index(v1), r["names"].index(v2)
    p1, p2, pi = iut(r, v1, v2)
    row = dict(spec=sid, n=r["n"], G=r["G"], muestra=f"{r['muestra'][0]}-{r['muestra'][1]}",
               b_precio=r["beta"][i1], se_precio=r["se"][i1], lo_precio=r["lo"][i1], hi_precio=r["hi"][i1],
               p_uni_precio=p1, b_inter=r["beta"][i2], se_inter=r["se"][i2], lo_inter=r["lo"][i2],
               hi_inter=r["hi"][i2], p_uni_inter=p2, p_IUT=pi, signos_ok=bool(r["beta"][i1] > 0 and r["beta"][i2] < 0))
    if extra:
        row.update(extra)
    return row


def tarea_h4(pa, nq):
    d = bl.preparar_h4(pa, nq)
    d["d_ln_pr_f1"] = d.groupby("cod_prov", sort=False)["d_ln_pr"].shift(-1)
    d["inter_f1"] = d["d_ln_pr_f1"] * d["suelo_c"]
    m = d[d["anio"].between(A0, A1)]
    info = dict(n_prov_suelo=d.attrs["n_prov_suelo"], media_ln_suelo=d.attrs["media_ln_suelo"], fuente_iniciadas="MIVAU 32200500 anual",
                provincias_sin_suelo=sorted(set(d["cod_prov"]) - set(d.loc[d["suelo_c"].notna(), "cod_prov"])),
                iniciadas_desde=int(d.loc[d["iniciadas_libres_anual"].notna(), "anio"].min()), muestra=[A0, A1])
    filas = []
    r = spec("H4", "H4_principal", m, Y, XP, "d_ln_pr_l1", boot=XP, B=B_MAIN,
             notas=f"PRE-REGISTRADA (muestra 2005-2023, iniciadas_libres_anual). WCR Webb B={B_MAIN}; precio real = p_tasado/deflactor medio anual")
    filas.append(fila_h4("H4_principal", r))
    tabs = [bl.tabla_res(r, "H4_principal")]
    # robustez / submuestras (B_SUB)
    sub = [("R1_precio_nominal", m, Y, ["d_ln_pn_l1", "inter_n"], "d_ln_pn_l1", "d_ln_pn_l1", "inter_n"),
           ("R2_precio_lag2", m[m["anio"] >= A0 + 1], Y, ["d_ln_pr_l2", "inter_l2"], "d_ln_pr_l2", "d_ln_pr_l2", "inter_l2"),
           ("S1_sin_Madrid_Barcelona", m[~m["cod_prov"].isin(["28", "08"])], Y, XP, "d_ln_pr_l1", "d_ln_pr_l1", "inter"),
           ("S2_2005-2013", m[m["anio"] <= min(2013, A1)], Y, XP, "d_ln_pr_l1", "d_ln_pr_l1", "inter"),
           ("S3_2014-2023", m[m["anio"] >= 2014], Y, XP, "d_ln_pr_l1", "d_ln_pr_l1", "inter"),
           ("S4_pre-COVID_2005-2019", m[m["anio"] <= min(2019, A1)], Y, XP, "d_ln_pr_l1", "d_ln_pr_l1", "inter"),
           ("S5_sin_COVID_2020-2021", m[~m["anio"].isin([2020, 2021])], Y, XP, "d_ln_pr_l1", "d_ln_pr_l1", "inter")]
    sub_filas = []
    for sid, dd, y, xs, it, v1, v2 in sub:
        if len(dd) < 30:
            continue
        rr = spec("H4", sid, dd, y, xs, it, boot=xs, B=B_SUB, notas=f"robustez/submuestra; WCR Webb B={B_SUB}")
        f = fila_h4(sid, rr, v1=v1, v2=v2)
        filas.append(f)
        sub_filas.append(f)
        tabs.append(bl.tabla_res(rr, sid))
    # R0: estimación previa (2009-2023, suma mensual, vista ANTES de la principal): robustez registrada
    d0 = bl.preparar_h4(pa, nq, ini_col="iniciadas_libres")
    m0 = d0[d0["anio"].between(2009, A1)]
    r0 = spec("H4", "R0_vista_antes_2009-2023_mensual", m0, Y, XP, "d_ln_pr_l1", boot=XP, B=B_SUB,
              notas=f"ROBUSTEZ; estimación previa vista antes (suma mensual, sin 2016-2018); WCR Webb B={B_SUB}")
    filas.append(fila_h4("R0_vista_antes_2009-2023_mensual", r0))
    tabs.append(bl.tabla_res(r0, "R0_vista_antes_2009-2023_mensual"))
    # placebo: precio futuro (t+1) añadido -> si el timing es exógeno, su coeficiente no debería ser significativo
    mp = m[m["anio"] <= A1 - 1]
    rp = spec("H4", "D1_placebo_lead_precio", mp, Y, XP + ["d_ln_pr_f1", "inter_f1"], "d_ln_pr_f1",
              notas="diagnóstico: precio real FUTURO (t+1) como placebo; coeficiente ~0 si no hay anticipación/endogeneidad")
    tabs.append(bl.tabla_res(rp, "D1_placebo_lead_precio"))
    # IV (robustez; endogeneidad del precio)
    iv_filas = []
    ivs = [("IV1_ocup_y_pob2034", ["d_ln_ocup_l1", "d_ln_pob2034_l1", "d_ln_ocup_l1_x", "d_ln_pob2034_l1_x"]),
           ("IV2_solo_ocup", ["d_ln_ocup_l1", "d_ln_ocup_l1_x"]),
           ("IV3_solo_pob2034", ["d_ln_pob2034_l1", "d_ln_pob2034_l1_x"])]
    for sid, inst in ivs:
        ri = bl.fe_2sls(m, Y, XP, [], inst)
        i1, i2 = 0, 1
        pu1 = float(stats.t.sf(ri["t"][i1], ri["df"]))
        pu2 = float(stats.t.cdf(ri["t"][i2], ri["df"]))
        LOG.libre("H4", sid, f"2SLS {Y} ~ {XP} | inst={inst} | FE(prov,anio) cl=prov", ri["muestra"][0],
                  ri["muestra"][1], ri["n"], coef=ri["beta"][0], p=ri["p"][0],
                  notas=f"ROBUSTEZ (no confirmatoria). F1={ri['F']}; J={ri['J']}; G={ri['G']}")
        iv_filas.append(dict(spec=sid, n=ri["n"], G=ri["G"], b_precio=ri["beta"][0], se_precio=ri["se"][0],
                             p_uni_precio=pu1, b_inter=ri["beta"][1], se_inter=ri["se"][1], p_uni_inter=pu2,
                             p_IUT=max(pu1, pu2), F_precio=ri["F"]["d_ln_pr_l1"], F_inter=ri["F"]["inter"],
                             J=ri["J"]["J"], J_gl=ri["J"]["df"], J_p=ri["J"]["p"]))
    guardar("h4_principal.csv", pd.DataFrame([filas[0]]))
    guardar("h4_robustez_submuestras.csv", pd.DataFrame(filas[1:]))
    guardar("h4_coeficientes.csv", pd.concat(tabs, ignore_index=True))
    guardar("h4_iv.csv", pd.DataFrame(iv_filas))
    # regla de submuestras (declarada en desviaciones.md): signos ok en TODAS las submuestras S1-S5
    sf = [f for f in sub_filas if f["spec"].startswith("S")]
    RES["h4"] = dict(info=info, principal=filas[0], p_IUT=filas[0]["p_IUT"], signos_ok=filas[0]["signos_ok"],
                     subm_signos_ok=all(f["signos_ok"] for f in sf), subm_n=len(sf),
                     subm_IUT_p=[(f["spec"], f["p_IUT"]) for f in sf], iv=iv_filas,
                     placebo_lead_p=float(rp["p"][rp["names"].index("d_ln_pr_f1")]),
                     placebo_lead_b=float(rp["beta"][rp["names"].index("d_ln_pr_f1")]))
    return d


# ======================================================================= 2. déficit
def tarea_deficit(pa, pq, nq):
    n = nq.copy()
    n["trimestre"] = n["trimestre"].astype(str)
    n = n[n["trimestre"] <= "2024Q2"].sort_values("trimestre").reset_index(drop=True)
    n["d_epa"] = n["hogares_epa"].diff() * 1000
    base = n[n["trimestre"].isin(["2020Q2", "2020Q3", "2020Q4", "2021Q2"])]["d_epa"].mean()
    n["d_epa_c"] = n["d_epa"]
    n.loc[n["trimestre"] == "2021Q1", "d_epa_c"] = base
    w = n[n["trimestre"] >= "2021Q1"].copy()
    # protegida: suma de las provincias de entrenamiento (49) y reescalado por cobertura de terminadas libres
    q = pq.copy()
    q["trimestre"] = q["trimestre"].astype(str)
    prot = q.groupby("trimestre")["protegida"].sum(min_count=1)
    tl = q.groupby("trimestre")["terminadas_libres"].sum(min_count=1)
    w["prot_49"] = w["trimestre"].map(prot).values
    w["term_libres_49"] = w["trimestre"].map(tl).values
    w["cobertura"] = w["term_libres_49"] / w["terminadas"]
    w["prot_escalada"] = w["prot_49"] / w["cobertura"]
    w["d_ecp"] = n["hogares_ecp"].diff().reindex(w.index)
    ok = w["prot_49"].notna()
    rows = []

    def add(etq, per, dh, term, prot_, ref):
        rows.append(dict(variante=etq, periodo=per, delta_hogares=dh, terminadas_libres=term, protegida=prot_,
                         deficit=dh - term - prot_, ref=ref))
    per = f"{w['trimestre'].iloc[0]}-{w['trimestre'].iloc[-1]}"
    dh_epa, term = w["d_epa_c"].sum(), w["terminadas"].sum()
    for etq, p_ in (("EPA corregida, sin protegida", 0.0),
                    ("EPA corregida, con protegida (49 prov. + reescalado)", w["prot_escalada"].sum()),
                    ("EPA corregida, con protegida (solo 49 prov., cota inferior)", w["prot_49"].sum())):
        add(etq, per, dh_epa, term, p_, "EPA")
    # ECP: stock a día 1 del trimestre -> H(2024Q2) - H(2021Q1) cubre 2021Q1-2024Q1
    wi = w[w["trimestre"] <= "2024Q1"]
    h1, h0 = n.loc[n["trimestre"] == "2024Q2", "hogares_ecp"].iloc[0], n.loc[n["trimestre"] == "2021Q1", "hogares_ecp"].iloc[0]
    termi = wi["terminadas"].sum()
    for etq, p_ in (("ECP, sin protegida", 0.0), ("ECP, con protegida (49 prov. + reescalado)", wi["prot_escalada"].sum()),
                    ("ECP, con protegida (solo 49 prov., cota inferior)", wi["prot_49"].sum())):
        add(etq, f"2021Q1-2024Q1", h1 - h0, termi, p_, "ECP")
    t = pd.DataFrame(rows)
    # por año
    w["anio"] = w["trimestre"].str[:4].astype(int)
    ya = w.groupby("anio").agg(delta_hogares_epa_c=("d_epa_c", "sum"), terminadas_libres=("terminadas", "sum"),
                               protegida_49=("prot_49", "sum"), protegida_escalada=("prot_escalada", "sum"),
                               cobertura_media=("cobertura", "mean"), n_trim=("trimestre", "count")).reset_index()
    guardar("deficit_nacional.csv", t)
    guardar("deficit_nacional_anual.csv", ya)
    prot_trim = float(w["prot_escalada"].mean())
    BDE = 750000
    v1_epa_res, v1_ecp_res = 866100 - BDE, 810936 - BDE
    RES["deficit"] = dict(tabla=t.to_dict("records"), prot_escalada_total=float(w["prot_escalada"].sum()),
                          prot_49_total=float(w["prot_49"].sum()), prot_trim_medio=prot_trim,
                          cobertura_media=float(w["cobertura"].mean()), n_trim=int(len(w)),
                          v1_residuo_epa=v1_epa_res, v1_residuo_ecp=v1_ecp_res,
                          ilustracion_2021_2025=float(w["prot_escalada"].sum() + prot_trim * 6),
                          protegida_observada_2021Q1_2024Q2=float(w["prot_escalada"].sum()), protegida_SUPUESTA_2024Q3_2025Q4=float(prot_trim * 6))
    LOG.libre("DEFICIT", "D_nacional", "Σ(Δhogares − terminadas [− protegida]) 2021Q1-2024Q2", "2021Q1", "2024Q2",
              int(len(w)), notas="DESCRIPTIVO; protegida = calificaciones definitivas VPO (MIVAU) como aprox. de terminadas")
    # proxy provincial (anual; flujo durante el año t = stock 1-ene t+1 - stock 1-ene t; años 2020-2022)
    a = pa.sort_values(["cod_prov", "anio"]).copy()
    a["anio"] = a["anio"].astype(int)
    hh = n.copy()
    hh["anio"] = hh["trimestre"].str[:4].astype(int)
    tam = (nq["pob_total"] / (nq["hogares_epa"] * 1000)).mean() if False else None
    q1 = nq[nq["trimestre"].astype(str).str.endswith("Q1")].copy()
    q1["anio"] = q1["trimestre"].astype(str).str[:4].astype(int)
    q1 = q1[q1["anio"].between(2021, 2024)]
    tam_hog = float((q1["pob_total"] / (q1["hogares_ecp"])).mean()) if len(q1) else np.nan
    a["d_pob"] = a.groupby("cod_prov")["pob_total"].shift(-1) - a["pob_total"]
    a["d_pob2034"] = a.groupby("cod_prov")["pob_20_34"].shift(-1) - a["pob_20_34"]
    p_ = a[a["anio"].between(2020, 2022)] if not SMOKE else a[a["anio"].between(2012, 2014)]
    g = p_.groupby("cod_prov").agg(d_pob=("d_pob", "sum"), d_pob2034=("d_pob2034", "sum"),
                                   term=("terminadas_libres", "sum"), prot=("protegida", "sum"),
                                   pob=("pob_total", "first"), n=("anio", "count")).reset_index()
    g["hogares_proxy"] = g["d_pob"] / tam_hog
    g["deficit_proxy"] = g["hogares_proxy"] - g["term"] - g["prot"]
    g["deficit_proxy_por_1000hab"] = g["deficit_proxy"] / g["pob"] * 1000
    g["term_por_joven_adicional"] = np.where(g["d_pob2034"] > 0, (g["term"] + g["prot"]) / g["d_pob2034"], np.nan)
    g = g.sort_values("deficit_proxy_por_1000hab", ascending=False)
    guardar("deficit_provincial_proxy.csv", g)
    RES["deficit"]["tam_hogar_ecp"] = tam_hog
    RES["deficit"]["prov_top5"] = g.head(5)[["cod_prov", "deficit_proxy_por_1000hab"]].values.tolist()
    LOG.libre("DEFICIT", "D_provincial_proxy", "Δpob_total/tamaño hogar nacional − terminadas − protegida (2020-2022)",
              "2020", "2022", int(len(g)), notas="DESCRIPTIVO; sin hogares provinciales; población 1-ene (padrón)")


# ======================================================================= 3. suelo
PER = {"P1": ("2008Q1", "2013Q4"), "P2": ("2014Q1", "2019Q4"), "P3": ("2020Q1", "2021Q4"), "P4": ("2022Q1", "2024Q2")}


def tarea_suelo(pq):
    q0 = pq.sort_values(["cod_prov", "trimestre"]).reset_index(drop=True).copy()
    q0["trimestre"] = q0["trimestre"].astype(str)
    H = range(1, 9) if not SMOKE else range(1, 5)
    periodos = dict(PER)
    periodos["TODO"] = ("2008Q1", "2024Q2")
    if SMOKE:
        periodos = {"P1": PER["P1"], "P2": ("2014Q1", "2015Q4"), "TODO": ("2008Q1", "2015Q4")}
    filas = []
    # variante "crudo": ln p_suelo trimestral (muy ruidoso: DE de Δ4 = 0,28 frente a 0,07 del precio);
    # variante "media4T": media móvil de 4 trimestres de ln p_suelo (reduce error de medida). Ambas EXPLORATORIAS.
    for var in ("crudo", "media4T"):
        q = q0.copy()
        q["ln_p"] = np.log(q["p_tasado"])
        ls = np.log(q["p_suelo"].where(q["p_suelo"] > 0))
        q["ln_s"] = ls if var == "crudo" else ls.groupby(q["cod_prov"]).transform(lambda x: x.rolling(4).mean())
        g = q.groupby("cod_prov", sort=False)
        q["d4_p"] = q["ln_p"] - g["ln_p"].shift(4)
        q["d4_s"] = q["ln_s"] - g["ln_s"].shift(4)
        for h in H:
            q[f"fp{h}"] = g["ln_p"].shift(-h) - q["ln_p"]
            q[f"fs{h}"] = g["ln_s"].shift(-h) - q["ln_s"]
        for pk, (a, b) in periodos.items():
            m = q[(q["trimestre"] >= a) & (q["trimestre"] <= b)]
            for h in H:
                for dirc, y, x, ctrl in (("suelo->precio", f"fp{h}", "d4_s", "d4_p"),
                                         ("precio->suelo", f"fs{h}", "d4_p", "d4_s")):
                    sid = f"L_{var}_{pk}_{dirc}_h{h}"
                    mm = m.dropna(subset=[y, x, ctrl])
                    if mm["cod_prov"].nunique() < 10 or len(mm) < 60:
                        continue
                    r = bl.fe_ols(mm, y, [x, ctrl], fe=("cod_prov", "trimestre"), cluster="cod_prov")
                    LOG.spec("SUELO", sid, f"{y} ~ {x} + {ctrl} | FE(prov,trim) cl=prov", r, x,
                             notas=f"EXPLORATORIO; proyección local; origen t en el periodo; suelo={var}")
                    filas.append(dict(variante=var, periodo=pk, direccion=dirc, h=h, coef=r["beta"][0], se=r["se"][0],
                                      t=r["t"][0], p=r["p"][0], ic95_lo=r["lo"][0], ic95_hi=r["hi"][0], n=r["n"], G=r["G"]))
    t = pd.DataFrame(filas)
    t["q_BH"] = np.nan
    t["p_Holm"] = np.nan
    ix = t.index
    t.loc[ix, "q_BH"] = pd.Series(bl.bh({i: t.loc[i, "p"] for i in ix}))      # familia = TODOS los contrastes (160)
    t.loc[ix, "p_Holm"] = pd.Series(bl.holm({i: t.loc[i, "p"] for i in ix}))
    guardar("suelo_proyecciones_locales.csv", t)
    res = {}
    for var in t["variante"].unique():
        for pk in periodos:
            s_ = t[(t["variante"] == var) & (t["periodo"] == pk)]
            sp, ps = s_[s_["direccion"] == "suelo->precio"], s_[s_["direccion"] == "precio->suelo"]
            res[f"{var}_{pk}"] = dict(
                suelo_antic_pos_p05=int(((sp["p"] < 0.05) & (sp["coef"] > 0)).sum()),
                precio_antic_pos_p05=int(((ps["p"] < 0.05) & (ps["coef"] > 0)).sum()),
                suelo_antic_pos_BH05=int(((sp["q_BH"] < 0.05) & (sp["coef"] > 0)).sum()),
                precio_antic_pos_BH05=int(((ps["q_BH"] < 0.05) & (ps["coef"] > 0)).sum()),
                n_h=int(len(sp)), min_p_suelo=float(sp["p"].min()), min_p_precio=float(ps["p"].min()),
                coef_suelo_h4=float(sp[sp["h"] == 4]["coef"].iloc[0]) if (sp["h"] == 4).any() else np.nan,
                coef_precio_h4=float(ps[ps["h"] == 4]["coef"].iloc[0]) if (ps["h"] == 4).any() else np.nan)
    RES["suelo"] = res


# ======================================================================= 4. panel UE
def _prep_ue(u, per_col, lagk, step):
    u = u.sort_values(["geo", per_col]).copy()
    g = u.groupby("geo", sort=False)
    u["lp"] = np.log(u["permisos"].where(u["permisos"] > 0))
    u["lh"] = np.log(u["hpi"] / u["hicp_general"])
    u["la"] = np.log(u["alquiler_hicp"] / u["hicp_general"])
    for v in ("lp", "lh", "la"):
        u["d_" + v] = u[v] - g[v].shift(step)
    u["d_lh_l"] = u.groupby("geo", sort=False)["d_lh"].shift(lagk)
    u["d_la_l"] = u.groupby("geo", sort=False)["d_la"].shift(lagk)
    return u


def tarea_ue():
    ua = _prep_ue(vc.load("panel_ue_a"), "anio", 1, 1)
    ua = ua[ua["anio"] <= 2023]
    filas = []
    for geo, d in ua.groupby("geo"):
        for nm, x in (("precio", "d_lh_l"), ("alquiler", "d_la_l")):
            dd = d.dropna(subset=["d_lp", x])
            if len(dd) < 10:
                continue
            X = np.c_[np.ones(len(dd)), dd[x].values]
            b, *_ = np.linalg.lstsq(X, dd["d_lp"].values, rcond=None)
            e = dd["d_lp"].values - X @ b
            XtXi = np.linalg.inv(X.T @ X)
            L = 1
            S = (X * e[:, None]).T @ (X * e[:, None])
            for l_ in range(1, L + 1):
                w = 1 - l_ / (L + 1)
                G_ = (X[l_:] * e[l_:, None]).T @ (X[:-l_] * e[:-l_, None])
                S += w * (G_ + G_.T)
            V = XtXi @ S @ XtXi * len(dd) / (len(dd) - 2)
            se = float(np.sqrt(V[1, 1]))
            p = float(2 * stats.t.sf(abs(b[1] / se), len(dd) - 2))
            filas.append(dict(geo=geo, regresor=nm, elasticidad=float(b[1]), se=se, p=p, n=len(dd),
                              desde=int(dd["anio"].min()), hasta=int(dd["anio"].max())))
            LOG.libre("UE", f"UE_{geo}_{nm}", f"d_ln_permisos_t ~ d_ln_{nm}_real_(t-1) HAC(1) [anual]",
                      int(dd["anio"].min()), int(dd["anio"].max()), len(dd), coef=float(b[1]), p=p,
                      notas="EXPLORATORIO; serie corta")
    pais = pd.DataFrame(filas)
    guardar("ue_elasticidades_pais.csv", pais)
    out = {}
    for nm in ("precio", "alquiler"):
        s = pais[(pais["regresor"] == nm)]
        es, ot = s[s["geo"] == "ES"], s[(s["geo"] != "ES") & (s["geo"] != "UK")]
        if len(es) == 0:
            continue
        mg = float(ot["elasticidad"].mean())
        se_mg = float(ot["elasticidad"].std(ddof=1) / np.sqrt(len(ot)))
        out[nm] = dict(ES=float(es["elasticidad"].iloc[0]), ES_se=float(es["se"].iloc[0]), UE_media=mg, UE_mediana=float(ot["elasticidad"].median()),
                       UE_se_media=se_mg, n_paises=int(len(ot)),
                       rango_ES=int((ot["elasticidad"] < es["elasticidad"].iloc[0]).sum()) + 1)
        LOG.libre("UE", f"UE_MG_{nm}", "media entre países (mean-group)", "", "", int(len(ot)), coef=mg, notas="EXPLORATORIO")
    # panel agrupado con FE país y año, interacción España
    pan = []
    for nm, x in (("precio", "d_lh_l"), ("alquiler", "d_la_l")):
        d = ua.dropna(subset=["d_lp", x]).copy()
        d["es"] = (d["geo"] == "ES").astype(float)
        d["x_es"] = d[x] * d["es"]
        d["x_noes"] = d[x] * (1 - d["es"])
        r = bl.fe_ols(d, "d_lp", ["x_noes", "x_es"], fe=("geo", "anio"), cluster="geo")
        LOG.spec("UE", f"UE_panel_{nm}", f"d_ln_permisos ~ {x}×(no ES, ES) | FE(geo,anio) cl=geo", r, "x_es",
                 notas="EXPLORATORIO; anual; p/EE de x_es NO válidos (España = un solo clúster): no interpretar")
        # diferencia ES - resto
        V = r["V"]
        dif = r["beta"][1] - r["beta"][0]
        sed = float(np.sqrt(V[0, 0] + V[1, 1] - 2 * V[0, 1]))
        pan.append(dict(regresor=nm, b_resto=r["beta"][0], se_resto=r["se"][0], b_ES=r["beta"][1],
                        dif_ES_menos_resto=dif,
                        n=r["n"], G=r["G"]))
    guardar("ue_panel_ES_vs_resto.csv", pd.DataFrame(pan))
    # trimestral (robustez): Δ4 ln permisos_t sobre Δ4 ln precio real_{t-4}
    uq = _prep_ue(vc.load("panel_ue_q"), "trimestre", 4, 4)
    uq["trimestre"] = uq["trimestre"].astype(str)
    uq = uq[uq["trimestre"] <= "2024Q2"]
    d = uq.dropna(subset=["d_lp", "d_lh_l"]).copy()
    d["x_es"] = d["d_lh_l"] * (d["geo"] == "ES")
    d["x_noes"] = d["d_lh_l"] * (d["geo"] != "ES")
    pq_ = []
    if len(d) > 100:
        r = bl.fe_ols(d, "d_lp", ["x_noes", "x_es"], fe=("geo", "trimestre"), cluster="geo")
        LOG.spec("UE", "UE_panel_q_precio", "Δ4 ln permisos ~ Δ4 ln precio real (t-4) ×(no ES, ES) | FE(geo,trim) cl=geo", r,
                 "x_es", notas="EXPLORATORIO; trimestral (permisos índice; hicp_general anual_asignado); p/EE de x_es NO válidos (un clúster)")
        V = r["V"]
        dif = r["beta"][1] - r["beta"][0]
        sed = float(np.sqrt(V[0, 0] + V[1, 1] - 2 * V[0, 1]))
        pq_.append(dict(regresor="precio_trimestral", b_resto=r["beta"][0], se_resto=r["se"][0], b_ES=r["beta"][1],
                        dif_ES_menos_resto=dif, n=r["n"], G=r["G"]))
        guardar("ue_panel_trimestral.csv", pd.DataFrame(pq_))
    RES["ue"] = dict(mg=out, panel=pan, panel_q=pq_)


# ======================================================================= 5. fuera de muestra
def _roll4(long, v):
    return long.groupby("unidad")[v].transform(lambda s: s.rolling(4).sum())


def _dl4(long, s):
    return s - vc._g(long, s, 4)


def feat_factory(ini=False, suelo=False, term=False, precio=False, base_ar=True):
    def f(long):
        cols = []
        for k in range(4):
            long[f"dY_l{k}"] = vc._g(long, long["dY"], k) if k else long["dY"]
            cols.append(f"dY_l{k}")
        if ini:
            r = _roll4(long, "iniciadas_libres")
            long["x_ini"] = _dl4(long, np.log(r.where(r > 0)))
            cols.append("x_ini")
        if suelo:
            long["x_suelo"] = _dl4(long, np.log(long["p_suelo"].where(long["p_suelo"] > 0)))
            cols.append("x_suelo")
        if term:
            r = _roll4(long, "terminadas_libres")
            long["x_term"] = _dl4(long, np.log(r.where(r > 0)))
            cols.append("x_term")
        if precio:
            lp = np.log(long["p_tasado"])
            long["x_pr"] = _dl4(long, lp)
            cols.append("x_pr")
        return cols
    return f


def tarea_oos(pq, nq):
    q = pq.copy()
    q["trimestre"] = q["trimestre"].astype(str)
    h = 4
    desde = "2011Q1" if SMOKE else "2014Q1"
    mt = 28 if SMOKE else 40
    pres = vc.Presupuesto(LOG.reg, "OOS", 6, "4 de precio real (AR4+oferta/suelo) y 2 de iniciadas; primario: P3")
    base_a = vc.panel_ar4(q, "p_tasado", "cod_prov", h, real=True, nac=nq, desde=desde, min_train=mt)
    base_e = vc.panel_ecm_v1(q, "p_tasado", "cod_prov", h, real=True, nac=nq, desde=desde, min_train=mt)
    cfgs = {"P1_ini": dict(ini=True), "P2_suelo": dict(suelo=True), "P3_ini_suelo": dict(ini=True, suelo=True),
            "P4_ini_suelo_term": dict(ini=True, suelo=True, term=True)}
    lvl_p = vc._lvl_fn("p_tasado", True, nq)
    preds = {}
    for nm, cfg in cfgs.items():
        pres.usar(nm, cfg, f"y_(t+4)=Δln precio real ~ AR(4)+{list(cfg)}", "", "", 0, notas="objetivo precio real, h=4")
        preds[nm] = vc._run(q, "cod_prov", h, None, desde, mt, 4, 4, lvl_p, feat_factory(**cfg), nm)
    # muestra común (precio): intersección de modelos y bases
    idx = None
    for p_ in list(preds.values()) + [base_a, base_e]:
        k = p_.dropna(subset=["y_real", "y_pred"]).drop_duplicates(["unidad", "periodo"]).set_index(["unidad", "periodo"]).index
        idx = k if idx is None else idx.intersection(k)

    def cut(p_):
        x = p_.dropna(subset=["y_real", "y_pred"]).drop_duplicates(["unidad", "periodo"]).set_index(["unidad", "periodo"])
        return x.loc[idx].reset_index()
    ba, be = cut(base_a), cut(base_e)
    filas = []
    for nm, p_ in preds.items():
        ev = vc.evaluar(cut(p_), {"AR4": ba, "ECM_v1": be}, h)
        ev.insert(0, "objetivo", "precio real")
        filas.append(ev)
    # iniciadas: ln(suma 4T) ; AR4 vs AR4 + precio (+ suelo). ECM v1 no definido para iniciadas.
    q2 = q.copy()
    q2["ini4"] = q2.groupby("cod_prov")["iniciadas_libres"].transform(lambda s: s.rolling(4).sum())
    q2 = q2.sort_values(["cod_prov", "trimestre"])
    mt_i = 10 if not SMOKE else 6
    d_i = "2014Q1" if not SMOKE else "2012Q1"
    lvl_i = vc._lvl_fn("ini4", False, None)
    bi = vc._run(q2, "cod_prov", h, None, d_i, mt_i, 4, 4, lvl_i, feat_factory(), vc.BASE)
    cfi = {"I1_precio": dict(precio=True), "I2_precio_suelo": dict(precio=True, suelo=True)}
    pi_ = {}
    for nm, cfg in cfi.items():
        pres.usar(nm, cfg, f"y_(t+4)=Δln iniciadas(4T) ~ AR(4)+{list(cfg)}", "", "", 0, notas="objetivo iniciadas, h=4; sin ECM v1")
        pi_[nm] = vc._run(q2, "cod_prov", h, None, d_i, mt_i, 4, 4, lvl_i, feat_factory(**cfg), nm)
    idx2 = bi.dropna(subset=["y_real", "y_pred"]).set_index(["unidad", "periodo"]).index
    for p_ in pi_.values():
        idx2 = idx2.intersection(p_.dropna(subset=["y_real", "y_pred"]).drop_duplicates(["unidad", "periodo"]).set_index(["unidad", "periodo"]).index)

    def cut2(p_):
        x = p_.dropna(subset=["y_real", "y_pred"]).drop_duplicates(["unidad", "periodo"]).set_index(["unidad", "periodo"])
        return x.loc[idx2].reset_index()
    for nm, p_ in pi_.items():
        ev = vc.evaluar(cut2(p_), {"AR4": cut2(bi)}, h)
        ev.insert(0, "objetivo", "iniciadas (4T)")
        filas.append(ev)
    t = pd.concat(filas, ignore_index=True)
    # p bilateral de DM-HLN (DM>0: el modelo mejora a la base)
    t["p_BH"] = np.nan
    pdict = {r["modelo"]: r["p_vs_AR4"] for _, r in t.iterrows() if np.isfinite(r["p_vs_AR4"])}
    for k, v in bl.bh(pdict).items():
        t.loc[t["modelo"] == k, "p_BH"] = v
    guardar("oos_h4.csv", t)
    for _, r in t.iterrows():
        LOG.libre("OOS", f"OOS_{r['modelo']}", f"h=4 {r['objetivo']} vs AR4 (y ECM v1 si precio)", desde, "2024Q2", int(r["n"]),
                  rmse_oos=r["rmse"], p=r["p_vs_AR4"], notas=f"DM-HLN vs AR4={r['dm_vs_AR4']:.3f}; rmse AR4={r['rmse_AR4']:.5f}")
    RES["oos"] = dict(tabla=t.to_dict("records"), primario="P3_ini_suelo", n_pres=pres.usadas)


def escribir_resultado():
    h = RES["h4"]
    pr = h["principal"]
    oos = {r["modelo"]: r for r in RES["oos"]["tabla"]}
    prim = oos[RES["oos"]["primario"]]
    dstr = RES["deficit"]
    nivel = "EXPLORATORIO"      # H4: ver criterio uniforme; no pasa submuestras ni IV -> no ASOCIACIÓN ROBUSTA
    vc.resultado_json(
        OUT / "resultado.json", rama="BO",
        pregunta="H4 (confirmatoria): elasticidad de las viviendas iniciadas libres al precio real (+) y mayor con suelo más barato "
                 "(interacción −); déficit de vivienda; suelo vs precio; elasticidad de permisos UE; fuera de muestra",
        datos="panel_prov_a 2005-2023 (47 provincias de entrenamiento con iniciadas y suelo; iniciadas libres anuales MIVAU 32200500); "
              "panel_prov_q, nacional_q_v2 (hasta 2024Q2), panel_ue_a/q; sin muestra sellada",
        N=int(pr["n"]),
        metodo="MCO con FE provincia y año, EE cluster provincia + wild cluster bootstrap restringido (Webb, B=9999); "
               "contraste conjunto por intersección-unión; robustez 2SLS (ocupados, población 20-34); proyecciones locales; "
               "panel UE; fuera de muestra en bloques con embargo (DM-HLN)",
        estimacion={"beta_precio": pr["b_precio"], "beta_interaccion": pr["b_inter"],
                    "p_uni_precio_boot": pr["p_uni_precio"], "p_uni_interaccion_boot": pr["p_uni_inter"],
                    "p_IUT_sin_ajustar": pr["p_IUT"], "signos_ok": pr["signos_ok"]},
        ic95={"beta_precio": [pr["lo_precio"], pr["hi_precio"]], "beta_interaccion": [pr["lo_inter"], pr["hi_inter"]]},
        p_ajustado={"p_IUT_sin_ajustar": pr["p_IUT"], "Holm_7": "lo aplica el orquestador (BS); p_IUT mínimo requerido "
                    "para sobrevivir si es la menor de las 7: 0,05/7=0,0071", "submuestras_signos_ok": h["subm_signos_ok"]},
        nivel_evidencia=nivel,
        diagnosticos={"IV": h["iv"], "placebo_precio_futuro": {"coef": h["placebo_lead_b"], "p": h["placebo_lead_p"]},
                      "submuestras_p_IUT": h["subm_IUT_p"],
                      "advertencia": "precio endógeno; IV con desplazadores de demanda débil y J rechaza; asociación, no causal"},
        fuera_muestra={"modelo": RES["oos"]["primario"], "rmse": prim["rmse"], "dm_vs_ar4": prim["dm_vs_AR4"],
                       "rmse_AR4": prim["rmse_AR4"], "p_vs_AR4": prim["p_vs_AR4"], "rmse_ECM_v1": prim["rmse_ECM_v1"],
                       "dm_vs_ecm_v1": prim["dm_vs_ECM_v1"], "p_vs_ecm_v1": prim["p_vs_ECM_v1"],
                       "nota": "precio real h=4; no mejora al AR(4). En iniciadas, AR4+precio mejora al AR4 (ver oos_h4.csv)"},
        notas="H4 re-estimada UNA vez con la muestra pre-registrada 2005-2023 (iniciadas_libres_anual MIVAU 32200500). Protegida: OBSERVADA "
              f"{dstr['protegida_observada_2021Q1_2024Q2']:.0f} (2021Q1-2024Q2) y SUPUESTA {dstr['protegida_SUPUESTA_2024Q3_2025Q4']:.0f} (2024Q3-2025Q4, 6 trim. a la media observada). "
              "Resultados secundarios (déficit, suelo, UE, OOS) EXPLORATORIOS/DESCRIPTIVOS; ver resumen.md y desviaciones.md. "
              f"Protegida 2021Q1-2024Q2 ≈ {dstr['prot_escalada_total']:.0f} viviendas (reescalada).")


# ======================================================================= main
def main():
    pa, pq, nq = cargar()
    tarea_h4(pa, nq)
    if SMOKE:
        tarea_deficit(vc.load('panel_prov_a'), vc.load('panel_prov_q'), vc.load('nacional_q_v2'))
    else:
        tarea_deficit(pa, pq, nq)
    tarea_suelo(pq)
    tarea_ue()
    tarea_oos(pq, nq)
    LOG.flush()
    escribir_resultado()
    (OUT / "resultados_internos.json").write_text(json.dumps(RES, indent=1, ensure_ascii=False, default=float))
    print("registro:", LOG.n, "filas;", "smoke" if SMOKE else "completo")
    print(json.dumps({k: v for k, v in RES.items() if k in ("h4",)}, indent=1, default=float)[:3000])


if __name__ == "__main__":
    main()
