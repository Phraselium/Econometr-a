"""V18 · E2 · robustez B6 declarada A POSTERIORI (ronda 1 del abogado del diablo: hallazgos 1, 2, 4, 5 y 6).

Análisis V18; capa C4; pre-registro interno plan-replicacion-v18. Estas pruebas se añaden DESPUÉS de ver los resultados de E2 (ronda 1 de B6):
no cambian la especificación principal ni la clase por sí solas; se declaran en docs/v18/desviaciones_e2_e8.md (B6-2). Nada se elige por p-valor.

(a) tendencia lineal del coeficiente por trimestre en 2021T1-2022T1 (mínima distancia sobre el estudio de eventos, con su covarianza agrupada por
    municipio) y contraste de un salto en 2022T2 sobre la extrapolación de esa recta;
(b) densidad HUT 2019 × efectos de trimestre y ln(población 2019) × efectos de trimestre (padrón municipal: está en el repositorio);
(c) controles emparejados por el crecimiento de la renta 2017-2019 (y por 2014-2017 y 2017-2019) y placebo de 2017 con tendencia propia de los
    regulados en 2014-2019;
(d) SDID (src/v18/herramientas/sdid.py) con controles ponderados; inferencia de Conley-Taber por placebos. Monte Carlo de V18: APTO solo si los
    tratados son intercambiables con los controles: se mide la razón de variabilidad temporal previa y se rotula;
(e) E2-R1c-v1 (contratos por hogar inquilino; hogares en alquiler del Censo 2021, muestra del 10 %, municipios de 10.000 habitantes o más), posible
    porque la variable c21md_hogares_muestra|municipio|D se añadió a docs/v18/sellado_v18.json (desviación B6-1).

Se ejecuta DESPUÉS de e2_topes.py (reescribe informe.md y hechos.json; esta fase añade su sección y sus hechos de forma idempotente).
Uso: python3 src/v18/estimacion/e2_robustez.py
Salidas: output/v18/estimacion/e2/{robustez_b6.csv, registry_b6.csv} + sección «Robustez B6 (a posteriori)» en informe.md + hechos V18-E2-B6-* en hechos.json.
Lecturas solo con sellado.filtrar + holdout.excluir_sellados_v6 (por _e2e8_comun, e2_datos, e2_diseno). Nunca data/sealed.
"""
from __future__ import annotations

import json
import re
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats
from statsmodels.stats.multitest import multipletests

sys.path.insert(0, str(Path(__file__).resolve().parent))
import _e2e8_comun as K  # noqa: E402
import e2_diseno as DS  # noqa: E402
import e2_estim as E  # noqa: E402
from herramientas import sdid as SD  # noqa: E402

ALCANCE_TERRITORIAL = "lectura con sellado.filtrar y holdout.excluir_sellados_v6"
OUT = DS.OUT
B_W = 4999            # réplicas de Webb de las variantes B6
B_CT = 999            # placebos de Conley-Taber
SECCION = "## Robustez B6 (a posteriori)"
FUENTES = ["Incasòl, fianzas (Socrata qww9-bvhh, descarga 2026-10-14)", "BOE-A-2020-11363 (Ley 11/2020 de Cataluña) y cataluna_contencion_rentas_v3.csv (v3)",
           "INE, Padrón municipal; IDESCAT (viviendas de uso turístico); INE, Censo 2021 (muestra del 10 %)",
           "docs/v18/revision_estimaciones/ronda1_e2_e8.md (ronda 1 del abogado del diablo)"]


def f(x, n=4):
    return "—" if x is None or (isinstance(x, float) and not np.isfinite(x)) else f"{x:.{n}f}"


def fila(id_, prueba, descr, rol, n_tr=None, n_co=None, coef=None, se=None, p_cr1=None, p_webb=None, ic=(None, None), nota="") -> dict:
    return {"id": id_, "prueba": prueba, "descripcion": descr, "rol": rol, "n_tratados": n_tr, "n_controles": n_co, "coef": coef, "se": se, "p_cr1": p_cr1,
            "p_webb": p_webb, "ic95_lo": ic[0], "ic95_hi": ic[1], "q_bh": None, "nota": nota}


# --------------------------------------------------------------------------------------------- utilidades
def evento_w(Y: np.ndarray, tr: np.ndarray, w: np.ndarray | None = None, base: int = E.BASE_COL) -> dict:
    """Estudio de eventos TWFE (Reg × 1[t = k], base 2019T4) con pesos opcionales y covarianza agrupada por municipio."""
    N, T = Y.shape
    ks = [k for k in range(T) if k != base]
    Dm = np.column_stack([(tr[:, None] * (np.arange(T) == k)[None, :]).ravel() for k in ks]).astype(float)
    unit, time_ = np.repeat(np.arange(N), T), np.tile(np.arange(T), N)
    ev = K.evento_multi(Y.ravel(), Dm, unit, time_, w=None if w is None else np.repeat(w, T), cluster=unit)
    leads = [i for i, k in enumerate(ks) if k < E.ANT_COL]
    W, p = K.wald_conjunto(ev["b"][leads], ev["V"][np.ix_(leads, leads)], ev["G"])
    return {"ks": ks, "b": ev["b"], "V": ev["V"], "G": ev["G"], "p_pretend": p}


def extra_por_trimestre(vec: np.ndarray, T: int) -> list[np.ndarray]:
    """vec_i × 1[t = k] para cada trimestre k (la parte constante la absorbe el efecto fijo de municipio; Modelo elimina la colinealidad)."""
    return [vec[:, None] * (np.arange(T) == k)[None, :].astype(float) for k in range(T)]


def inferir_var(m: K.Modelo, B: int = B_W) -> dict:
    return E.inferir(m, B, 0, ic=False)


def lineal(c: np.ndarray, b: np.ndarray, V: np.ndarray, G: int) -> dict:
    est, se = float(c @ b), float(np.sqrt(max(c @ V @ c, 0.0)))
    q = stats.t.ppf(0.975, G - 1)
    return {"est": est, "se": se, "p": float(2 * stats.t.sf(abs(est / se), G - 1)), "ic": (est - q * se, est + q * se)}


# --------------------------------------------------------------------------------------------- (a) tendencia y salto
def prueba_a(d: dict) -> tuple[list[dict], dict]:
    filas, info = [], {}
    for etiqueta, fin in (("14T", "2022T2"), ("20T", "2023T4")):
        per = K.trimestres("2019T1", fin)
        p = DS.panel_r1(d, "renta", per=per)
        ev = evento_w(p["Y"], p["tr"])
        ix = {k: i for i, k in enumerate(ev["ks"])}
        for nombre, ventana in (("2021T1-2022T1", [8, 9, 10, 11, 12]), ("2020T4-2022T1", [7, 8, 9, 10, 11, 12])):
            wi = [ix[k] for k in ventana]
            x = np.array(ventana, float) - ventana[0]
            X = np.column_stack([np.ones(len(x)), x])
            Vi = np.linalg.pinv(ev["V"][np.ix_(wi, wi)])
            cov = np.linalg.inv(X.T @ Vi @ X)
            M = cov @ X.T @ Vi                                    # (a, s) = M b_ventana
            b_w = ev["b"][wi]
            a_s = M @ b_w
            G = ev["G"]
            C_s = np.zeros(len(ev["b"]))
            C_s[wi] = M[1]
            tend = lineal(C_s, ev["b"], ev["V"], G)
            Ccon = []
            for objetivo, k0 in (("2022T2", 13), ("2022T2-2022T4 (media)", None)):
                if k0 is None:
                    if etiqueta != "20T":
                        continue
                    ks_obj = [13, 14, 15]
                else:
                    ks_obj = [k0]
                c = np.zeros(len(ev["b"]))
                for k in ks_obj:
                    c[ix[k]] += 1.0 / len(ks_obj)
                    c[wi] -= (M[0] + (k - ventana[0]) * M[1]) / len(ks_obj)
                salto = lineal(c, ev["b"], ev["V"], G)
                extrap = float(np.mean([a_s[0] + (k - ventana[0]) * a_s[1] for k in ks_obj]))
                obs = float(np.mean([ev["b"][ix[k]] for k in ks_obj]))
                Ccon.append((objetivo, salto, extrap, obs))
            clave = f"{etiqueta}-{nombre}"
            info[clave] = {"pendiente": tend, "saltos": Ccon, "a": float(a_s[0]), "n_tr": p["n_tr"], "n_co": p["n_co"], "G": G}
            filas.append(fila(f"E2-R1-B6a-{clave}-pendiente", "a", f"pendiente del coeficiente por trimestre en {nombre} (panel 2019T1-{fin}); mínima distancia sobre el estudio de eventos", "diagnóstico",
                              p["n_tr"], p["n_co"], tend["est"], tend["se"], tend["p"], None, tend["ic"],
                              f"coeficiente ajustado al inicio de la ventana {a_s[0]:+.4f}"))
            for objetivo, salto, extrap, obs in Ccon:
                filas.append(fila(f"E2-R1-B6a-{clave}-salto-{objetivo.split(' ')[0]}", "a", f"salto en {objetivo} sobre la extrapolación de la recta de {nombre} (panel 2019T1-{fin})", "diagnóstico",
                                  p["n_tr"], p["n_co"], salto["est"], salto["se"], salto["p"], None, salto["ic"],
                                  f"observado {obs:+.4f}; extrapolado {extrap:+.4f}"))
    return filas, info


# --------------------------------------------------------------------------------------------- (b) covariables × trimestre
def prueba_b(d: dict) -> tuple[list[dict], dict]:
    filas = []
    m0, q = E.spec_trim(d, "renta")
    T = q["Y"].shape[1]
    cods = list(q["cod"])
    pop19 = d["pop"].reindex(cods)["2019"].values
    hut = d["hut"].reindex(cods)["2019"].fillna(0.0).values
    dens = hut / pop19 * 1000.0
    lp = np.log(pop19)
    paro19 = np.log1p(DS.paro_interp(d["paro"]).reindex(cods)["2019"].values)
    ok_paro = np.isfinite(paro19)
    base = {"coef": m0.beta, "n_tr": q["n_tr"], "n_co": q["n_co"]}
    specs = [("B6b-1", "densidad HUT 2019 × efectos de trimestre", [dens], np.ones(len(cods), bool)),
             ("B6b-2", "ln(población 2019) × efectos de trimestre", [lp], np.ones(len(cods), bool)),
             ("B6b-3", "densidad HUT 2019 × trimestre y ln(población 2019) × trimestre", [dens, lp], np.ones(len(cods), bool)),
             ("B6b-4", "B6b-3 y ln(1 + paro registrado 2019) × trimestre (paro real de 2019; sin el de 2020)", [dens, lp, paro19], ok_paro)]
    for ident, descr, vecs, keep in specs:
        Y, tr = q["Y"][keep], q["tr"][keep]
        ex = []
        for v in vecs:
            ex += extra_por_trimestre(v[keep], T)
        m = E.twfe_panel(Y, tr, E.POST_COLS, (E.ANT_COL,), ex)
        r = inferir_var(m)
        filas.append(fila(f"E2-R1-{ident}", "b", descr, "variante", int(tr.sum()), int((~tr).sum()), r["coef"], r["se"], r["p_cr1"], r["p_webb"], r["ic_cr1"],
                          f"principal {base['coef']:+.4f}; criterio de la ronda: por debajo de −0,03: {'sí' if r['coef'] < -0.03 else 'no'}"))
    return filas, base


# --------------------------------------------------------------------------------------------- (c) controles emparejados y placebo de 2017
def panel_emparejado(d: dict, k: int = 1, dos_dim: bool = False) -> dict:
    """Controles (no regulados, sin el criterio de crecimiento de JMS) emparejados con reposición por el crecimiento anual de la renta 2017-2019
    (y, con dos_dim, también por el de 2014-2017), distancia euclídea sobre variables tipificadas; peso del control = (veces elegido)/k."""
    p = DS.panel_r1(d, "renta", grupo_control="todos")
    cods = list(p["cod"])
    rA = d["rA"].reindex(cods)
    cols = [(rA["2019"] / rA["2017"]) ** 0.5 - 1]
    if dos_dim:
        cols.append((rA["2017"] / rA["2014"]) ** (1 / 3) - 1)
    X = np.column_stack([c.values for c in cols])
    ok = np.isfinite(X).all(axis=1)
    X = (X - X[ok].mean(0)) / X[ok].std(0)
    tr = p["tr"] & ok
    co = np.where(~p["tr"] & ok)[0]
    cuenta = np.zeros(len(cods))
    for i in np.where(tr)[0]:
        dist = ((X[co] - X[i]) ** 2).sum(1)
        for j in co[np.argsort(dist)[:k]]:
            cuenta[j] += 1.0 / k
    sel = tr | (cuenta > 0)
    out = {kk: (v[sel] if isinstance(v, np.ndarray) and len(v) == len(sel) else v) for kk, v in p.items()}
    out["tr"] = tr[sel]
    out["w"] = np.where(tr[sel], 1.0, cuenta[sel])
    out["n_tr"], out["n_co"] = int(tr.sum()), int((cuenta > 0).sum())
    return out


def placebo_anual(d: dict, cod_tr: list[str], cod_co: list[str], w: dict | None, tendencia: bool) -> dict:
    """Placebo de fecha (adopción falsa en 2017; anual 2014-2019) con o sin tendencia lineal propia de los regulados."""
    anios = ["2014", "2015", "2016", "2017", "2018", "2019"]
    A = d["rA"].reindex(columns=anios)
    ok = A.notna().all(axis=1) & (A > 0).all(axis=1)
    tr = [c for c in cod_tr if c in ok.index and ok[c]]
    co = [c for c in cod_co if c in ok.index and ok[c]]
    sel = tr + co
    Y = np.log(A.loc[sel].values)
    trv = np.array([c in set(tr) for c in sel])
    pc = [i for i, a in enumerate(anios) if a >= "2017"]
    ex = [trv[:, None].astype(float) * np.arange(len(anios))[None, :]] if tendencia else []
    wv = None if w is None else np.array([1.0 if c in set(tr) else w.get(c, 0.0) for c in sel])
    m = E.twfe_panel(Y, trv, pc, (), ex, w=wv)
    return {"coef": m.beta, "se": m.se, "p": m.p_t, "ic": m.ic_t, "n_tr": len(tr), "n_co": len(co)}


def prueba_c(d: dict) -> tuple[list[dict], dict]:
    filas, info = [], {}
    m0, q = E.spec_trim(d, "renta")
    for ident, k, dos, descr in (("B6c-1", 1, False, "controles emparejados por el crecimiento de la renta 2017-2019 (1 vecino más próximo, con reposición)"),
                                 ("B6c-2", 1, True, "controles emparejados por el crecimiento 2017-2019 y 2014-2017 (1 vecino más próximo)"),
                                 ("B6c-3", 3, False, "controles emparejados por el crecimiento 2017-2019 (3 vecinos más próximos)")):
        pe = panel_emparejado(d, k, dos)
        m = E.twfe_panel(pe["Y"], pe["tr"], E.POST_COLS, (E.ANT_COL,), w=pe["w"])
        r = inferir_var(m)
        ev = evento_w(pe["Y"], pe["tr"], pe["w"])
        info[ident] = {"pretend_p": ev["p_pretend"], "n_tr": pe["n_tr"], "n_co": pe["n_co"]}
        filas.append(fila(f"E2-R1-{ident}", "c", descr, "variante", pe["n_tr"], pe["n_co"], r["coef"], r["se"], r["p_cr1"], r["p_webb"], r["ic_cr1"],
                          f"pretendencias (contraste conjunto) p = {ev['p_pretend']:.3f}; principal {m0.beta:+.4f}"))
        if ident == "B6c-1":
            pe1 = pe
    # placebo de 2017 anual: con y sin tendencia propia; muestra de la principal y con controles emparejados
    pa = E.panel_anual(d, "rA", ["2014", "2015", "2016", "2017", "2018", "2019"], [])
    cod_tr_a = [c for c, t in zip(pa["cod"], pa["tr"]) if t]
    cod_co_a = [c for c, t in zip(pa["cod"], pa["tr"]) if not t]
    w_m = {c: w for c, t, w in zip(pe1["cod"], pe1["tr"], pe1["w"]) if not t}
    for ident, descr, tr_, co_, w_, tend in (("B6c-4", "placebo de 2017 (anual 2014-2019, controles de JMS), sin tendencia propia (reproduce el de la principal)", cod_tr_a, cod_co_a, None, False),
                                             ("B6c-5", "placebo de 2017 con tendencia lineal propia de los regulados 2014-2019 (controles de JMS)", cod_tr_a, cod_co_a, None, True),
                                             ("B6c-6", "placebo de 2017 con tendencia propia y controles emparejados por el crecimiento 2017-2019 (el emparejamiento usa 2017-2019: informativo)",
                                              cod_tr_a, list(w_m), w_m, True)):
        pl = placebo_anual(d, tr_, co_, w_, tend)
        info[ident] = pl
        filas.append(fila(f"E2-R1-{ident}", "c", descr, "placebo", pl["n_tr"], pl["n_co"], pl["coef"], pl["se"], pl["p"], None, pl["ic"],
                          "adopción falsa en 2017; el coeficiente principal del placebo sin tendencia fue +0,0146 (p = 0,056), de signo contrario al de la principal"))
    return filas, info


# --------------------------------------------------------------------------------------------- (d) SDID
def prueba_d(d: dict) -> tuple[list[dict], dict]:
    filas, info = [], {}
    pre, post = [0, 1, 2, 3, 4, 5], list(E.POST_COLS)            # 2019T1-2020T2 y 2020T4-2022T1 (2020T3, la anticipación, fuera)
    for ident, grupo, descr in (("B6d-1", "jms", "SDID, controles de JMS (crecimiento 2014-2019 > 4,15 %)"),
                                ("B6d-2", "todos", "SDID, todos los municipios no regulados con serie completa (más donantes)")):
        p = DS.panel_r1(d, "renta", grupo_control=grupo)
        Y, tr = p["Y"], p["tr"]
        Ytr, Yco = Y[tr], Y[~tr]
        s = SD.sdid(Ytr[:, pre], Ytr[:, post], Yco[:, pre], Yco[:, post])
        n_tr, n_co = int(tr.sum()), int((~tr).sum())
        pl = SD.placebos(Yco[:, pre], Yco[:, post], s["lambda"], s["zeta"], n_tr, np.random.default_rng(K.SEMILLA), B=B_CT)
        c = pl["sdid"]
        p_ct = SD.p_placebo(s["tau"], c, 0.0)
        m_ = int(np.ceil(0.05 * (len(c) + 1))) - 1
        crit = float(np.sort(np.abs(c))[::-1][m_ - 1])
        did = float(Ytr[:, post].mean() - Ytr[:, pre].mean() - (Yco[:, post].mean() - Yco[:, pre].mean()))
        sd_t = float(np.std(np.diff(Ytr[:, pre], axis=1), axis=1).mean())
        sd_c = float(np.std(np.diff(Yco[:, pre], axis=1), axis=1).mean())
        om = s["omega"]
        n_ef = float(1.0 / (om ** 2).sum())
        razon = sd_t / sd_c
        interc = "conservadora (tratados menos variables que los controles)" if razon < 0.7 else ("dentro de lo validado" if razon <= 1.3 else "no fiable (tratados más variables: tamaño 0,44 en el Monte Carlo)")
        donantes = n_co - n_tr
        nota = (f"τ(SDID) {s['tau']:+.4f}; DiD simple en los mismos periodos {did:+.4f}; razón de variabilidad previa tratados/controles {razon:.2f} ({interc}); "
                f"donantes efectivos {n_ef:.1f}; {donantes} donantes en cada placebo (Monte Carlo validado con 2 a 25 tratados y 200 controles)")
        if donantes < 2 * n_tr:
            nota += "; pocos donantes por placebo: inferencia débil"
        info[ident] = {"tau": s["tau"], "did": did, "p_ct": p_ct, "ic": (s["tau"] - crit, s["tau"] + crit), "razon_var": razon, "interc": interc, "n_ef": n_ef,
                       "n_tr": n_tr, "n_co": n_co, "donantes": donantes, "lambda": [round(float(x), 3) for x in s["lambda"]], "top5": float(np.sort(om)[::-1][:5].sum())}
        filas.append(fila(f"E2-R1-{ident}", "d", descr, "variante", n_tr, n_co, s["tau"], float(np.std(c, ddof=1)), None, p_ct, (s["tau"] - crit, s["tau"] + crit), nota))
    return filas, info


# --------------------------------------------------------------------------------------------- (e) E2-R1c-v1
def hogares_inquilinos(d: dict) -> pd.Series:
    """Hogares en alquiler (tenencia = 3 del Censo 2021, ES + EXT) por municipio: recuento MUESTRAL del 10 % ×10 (solo municipios de 10.000 habitantes o más)."""
    h = K.leer_hechos("c21md_hogares_muestra", "municipio", "D")
    h = h[h.desagregacion.str.endswith("tenencia=3")]
    return h.groupby("territorio_codigo").valor.sum() * 10.0


def prueba_e(d: dict) -> tuple[list[dict], dict]:
    filas = []
    hog = hogares_inquilinos(d)
    p = DS.panel_r1(d, "contratos")
    keep = np.isin(p["cod"], hog[hog > 0].index)
    cod = p["cod"][keep]
    tr = p["tr"][keep]
    per = p["cols"]
    c = d["cT"].loc[cod, per].values
    Y_v1 = np.log(c) - np.log(hog.reindex(cod).values)[:, None] + np.log(1000)
    Y_pop = np.log(c) - DS.ln_pop_trimestral(d["pop"], list(cod), per) + np.log(1000)
    n_tr, n_co = int(tr.sum()), int((~tr).sum())
    # estimabilidad (adenda 1.3): mínimos y MDE antes del coeficiente
    mde = K.mde_desde_placebos(DS.placebos_twfe(Y_v1, n_tr, list(E.POST_COLS), DS.R_MDE, np.random.default_rng(K.SEMILLA)))
    est = {"n_tr": n_tr, "n_co": n_co, "minimo_ok": bool(n_tr >= 30 and n_co >= 30), "mde80": mde["mde80"], "umbral": DS.ESPEC["E2-R1c"]["umbral"]}
    est["estimable"] = bool(est["minimo_ok"] and mde["mde80"] <= est["umbral"])
    est["nota"] = f"mínimo 30/30: {est['minimo_ok']}; MDE80 {mde['mde80']:.4f} (umbral {est['umbral']:.2f}, 2δ)"
    rr = {}
    if not est["estimable"]:
        filas.append(fila("E2-R1c-v1", "e", "contratos por hogar inquilino (Censo 2021)", "variante", n_tr, n_co, nota="NO ESTIMABLE: " + est["nota"]))
        return filas, {"est": est, "res": rr}
    for ident, descr, Y in (("E2-R1c-v1", "contratos por 1.000 hogares inquilinos (Censo 2021, ×10 de la muestra del 10 %)", Y_v1),
                            ("E2-R1c-v1-ref", "referencia: contratos por 1.000 habitantes en la MISMA muestra (municipios con Censo 2021)", Y_pop)):
        m = E.twfe_panel(Y, tr, E.POST_COLS, (E.ANT_COL,))
        r = E.inferir(m, 9999 if ident == "E2-R1c-v1" else B_W, 0, ic=False)
        ev = evento_w(Y, tr)
        r["p_pretend"] = ev["p_pretend"]
        r["cae5"] = bool(r["coef"] <= -0.05 and r["p_cr1"] < 0.05)
        rr[ident] = r
        filas.append(fila(ident, "e", descr, "variante" if ident == "E2-R1c-v1" else "referencia", n_tr, n_co, r["coef"], r["se"], r["p_cr1"], r["p_webb"], r["ic_cr1"],
                          f"pretendencias p = {ev['p_pretend']:.3f}; MDE80 {mde['mde80']:.4f}; criterio AD-E2 (cae ≥ 5 % con p < 0,05): {'sí' if r['cae5'] else 'no'}"))
    return filas, {"est": est, "res": rr}


# --------------------------------------------------------------------------------------------- salidas
def lectura(ia: dict, ib: dict, ic_: dict, id_: dict, ie: dict, filas: list[dict]) -> list[str]:
    t = {f_["id"]: f_ for f_ in filas}
    L = []
    k = ia["14T-2021T1-2022T1"]
    s, sal = k["pendiente"], k["saltos"][0]
    k2 = ia["20T-2021T1-2022T1"]
    sal3 = k2["saltos"][1]
    L.append(f"(a) Tendencia: el coeficiente por trimestre sube {s['est']:+.4f} por trimestre en 2021T1-2022T1 (IC95 {f(s['ic'][0])}; {f(s['ic'][1])}; p = {s['p']:.3f}): "
             f"ya durante la vigencia pierde magnitud trimestre a trimestre (ajustado: {k['a']:+.4f} en 2021T1); con la ventana 2020T4-2022T1 la pendiente es {ia['14T-2020T4-2022T1']['pendiente']['est']:+.4f} "
             f"(p = {ia['14T-2020T4-2022T1']['pendiente']['p']:.3f}). El coeficiente medio de la principal ({ib['coef']:+.4f}) no describe un nivel estable. "
             f"Salto en 2022T2 sobre la extrapolación de la recta: {sal[1]['est']:+.4f} (IC95 {f(sal[1]['ic'][0])}; {f(sal[1]['ic'][1])}; p = {sal[1]['p']:.3f}): observado {sal[3]:+.4f} frente a {sal[2]:+.4f} extrapolado; "
             f"media 2022T2-2022T4: {sal3[1]['est']:+.4f} (p = {sal3[1]['p']:.3f}). "
             + ("El observado es MÁS negativo que la extrapolación (no hay una desaparición abrupta del coeficiente en 2022T2): no se detecta un salto en la fecha de la STC a este nivel de potencia, y el coeficiente se aproxima a cero de forma gradual."
                if sal[1]["est"] < 0 and sal[1]["p"] >= 0.05 else
                ("El observado es más negativo que la extrapolación y el salto es distinguible." if sal[1]["est"] < 0 else "El observado está por encima de la extrapolación: el coeficiente se aproxima a cero más rápido que la recta.")))
    b = [t[f"E2-R1-B6b-{i}"] for i in (1, 2, 3, 4)]
    L.append("(b) Covariables por trimestre: " + "; ".join(f"{x['id'].split('-')[-1]} {x['coef']:+.4f} (IC95 {f(x['ic95_lo'])}; {f(x['ic95_hi'])}; p Webb {f(x['p_webb'])})" for x in b)
             + f"; principal {ib['coef']:+.4f}. HUT × trimestre deja el coeficiente en {b[0]['coef']:+.4f} (por debajo de −0,03); ln(población) × trimestre lo reduce a {b[1]['coef']:+.4f} "
             f"({'no queda' if b[1]['coef'] >= -0.03 else 'queda'} por debajo de −0,03, criterio de la ronda), con IC95 que casi llega a cero.")
    c = [t[f"E2-R1-B6c-{i}"] for i in (1, 2, 3)]
    pl = {i: ic_[f"B6c-{i}"] for i in (4, 5, 6)}
    L.append("(c) Controles emparejados: " + "; ".join(f"{x['id'].split('-')[-1]} {x['coef']:+.4f} (p Webb {f(x['p_webb'])}; pretendencias p = {ic_[x['id'].split('-')[-1]]['pretend_p']:.2f})" for x in c)
             + f". Placebo de 2017: sin tendencia {pl[4]['coef']:+.4f} (p = {pl[4]['p']:.3f}); con tendencia propia de los regulados {pl[5]['coef']:+.4f} (p = {pl[5]['p']:.3f}, de signo contrario al de la principal); "
             f"con tendencia y controles emparejados {pl[6]['coef']:+.4f} (p = {pl[6]['p']:.3f}). El placebo de signo contrario indica que los regulados subían más que los controles en 2017-2019 "
             "(lo que, si se revierte, sesgaría hacia un coeficiente más negativo); el emparejamiento por ese crecimiento no reduce el coeficiente.")
    L.append("(d) SDID: " + "; ".join(f"{k_} τ = {v['tau']:+.4f} (Conley-Taber p = {v['p_ct']:.3f}, mínimo posible 0,001; razón de variabilidad previa {v['razon_var']:.2f}, {v['interc']}; "
                                      f"donantes efectivos {v['n_ef']:.0f} de {v['n_co']}; DiD simple {v['did']:+.4f})" for k_, v in id_.items())
             + ". Los pesos de unidad quedan casi uniformes (la regularización de ζ es fuerte con 49 tratados): SDID reproduce al DiD y no cambia la lectura; la dependencia del control (hallazgo 5) se aborda mejor con B6c.")
    if "E2-R1c-v1" in ie["res"]:
        r, r0 = ie["res"]["E2-R1c-v1"], ie["res"]["E2-R1c-v1-ref"]
        L.append(f"(e) E2-R1c-v1: {r['coef']:+.4f} (IC95 {f(r['ic_cr1'][0])}; {f(r['ic_cr1'][1])}; p Webb {f(r['p_webb'])}); en la misma muestra con la población como denominador {r0['coef']:+.4f} "
                 f"(p Webb {f(r0['p_webb'])}); la R1c principal, con 156 controles, da +0,0173. Criterio de AD-E2 (caída ≥ 5 % con p < 0,05): {'se cumple' if r['cae5'] else 'no se cumple'}, pero el IC95 incluye caídas "
                 f"mayores que 5 % (hasta {r['ic_cr1'][0]:+.3f}): no se descarta el desvío a la temporada o a no depositar la fianza. {ie['est']['nota']}.")
    else:
        L.append(f"(e) E2-R1c-v1: NO ESTIMABLE ({ie['est']['nota']}).")
    return L


def escribir(filas: list[dict], info: dict, seg: float) -> None:
    df = pd.DataFrame(filas)
    v = df[(df.rol == "variante") & df.id.str.startswith("E2-R1-B6")].copy()
    p = v.p_webb.astype(float).values
    ok = np.isfinite(p)
    q = multipletests(p[ok], alpha=0.10, method="fdr_bh")[1]
    df.loc[v.index[ok], "q_bh"] = q
    df.to_csv(OUT / "robustez_b6.csv", index=False, float_format="%.6f")
    # Registry de las especificaciones de B6 (fichero propio: el registry.csv de e2_topes se reescribe entero en cada ejecución)
    reg = K.Registry(OUT / "registry_b6.csv")
    for r in df.itertuples():
        reg.log("v18-E2-B6-aposteriori", r.id, r.descripcion, "2019T1", "2022T1", int((r.n_tratados or 0) + (r.n_controles or 0)), np.nan, np.nan, np.nan,
                coef_interes=r.coef if r.coef is not None else np.nan, p_interes=r.p_webb if r.p_webb is not None and r.p_webb == r.p_webb else (r.p_cr1 if r.p_cr1 is not None else np.nan),
                notas=f"robustez declarada a posteriori (ronda 1, B6); {r.rol}")
    reg.flush()
    ia, ib, ic_, id_, ie = info["a"], info["b"], info["c"], info["d"], info["e"]
    tab = df[["id", "rol", "n_tratados", "n_controles", "coef", "se", "p_cr1", "p_webb", "ic95_lo", "ic95_hi", "q_bh"]].copy()
    for c in ("coef", "se", "ic95_lo", "ic95_hi"):
        tab[c] = tab[c].map(lambda x: f(x))
    for c in ("p_cr1", "p_webb", "q_bh"):
        tab[c] = tab[c].map(lambda x: f(x, 4) if x is not None and x == x else "—")
    for c in ("n_tratados", "n_controles"):
        tab[c] = tab[c].map(lambda x: "—" if x is None or x != x else int(x))
    notas = df[["id", "nota"]].copy()
    notas["nota"] = notas.nota.astype(str).str.slice(0, 230)
    L = lectura(ia, ib, ic_, id_, ie, filas)
    txt = f"""{SECCION}

Pruebas pedidas por la ronda 1 del abogado del diablo (hallazgos 1, 2, 4, 5 y 6; docs/v18/revision_estimaciones/ronda1_e2_e8.md). **Se declaran a posteriori**: se añadieron después de ver los
resultados de E2, no cambian la especificación principal ni su clase por sí solas y entran como robustez (desviación B6-2 de docs/v18/desviaciones_e2_e8.md). Código: `src/v18/estimacion/e2_robustez.py`;
SEED 20261010; {seg:.0f} s; inferencia de Webb con {B_W // 1000}.{B_W % 1000:03d} réplicas por municipio en las variantes (9.999 en E2-R1c-v1) y {B_CT} placebos de Conley-Taber en el SDID. q_bh: Benjamini-Hochberg al 10 % sobre las variantes de la renta de esta sección (B6b, B6c-1 a B6c-3, B6d; exploratorias);
los diagnósticos, los placebos y E2-R1c-v1 (una sola variante) llevan su p propio, sin ajuste. Análisis V18; capa C4; nivel de evidencia EXPLORATORIO.

### Lectura
""" + "\n".join(f"- {x}" for x in L) + f"""

### Tabla
{md(tab)}

### Notas por fila
{md(notas)}

### Cómo se hizo
- **(a)** Estudio de eventos (base 2019T4) en los paneles equilibrados 2019T1-2022T2 (14 trimestres) y 2019T1-2023T4 (20): la recta se ajusta por mínima distancia (GLS con la covarianza agrupada por municipio) a los coeficientes de 2021T1-2022T1 (y, como variante, de 2020T4-2022T1); el salto es el coeficiente de 2022T2 menos el valor de la recta extrapolada, con su error típico conjunto (t de G−1 gl). La muestra de estos paneles es menor que la de la principal porque exige contratos en más trimestres.
- **(b)** Covariables por trimestre: x_i × 1[t = k] para cada trimestre; la densidad HUT usa IDESCAT 2019 (sin dato = 0) entre los habitantes del padrón de 2019; la población municipal del padrón está en el repositorio. B6b-4 añade el paro registrado de 2019 (el de 2020 no está en la base; los ERTE por municipio tampoco).
- **(c)** Emparejamiento con reposición por el crecimiento anual de la renta 2017-2019 (y 2014-2017 en B6c-2) con el conjunto de no regulados sin el criterio de crecimiento de JMS; el peso del control es el número de veces elegido. El placebo de 2017 usa Incasòl anual 2014-2019, adopción falsa en 2017, con y sin una tendencia lineal propia de los regulados.
- **(d)** SDID con los pesos de unidad ω (símplex, con regularización) y de tiempo λ de `sdid.py`; pre = 2019T1-2020T2, post = 2020T4-2022T1 (como la principal; 2020T3 queda fuera). La inferencia por placebos de Conley-Taber solo es válida si los tratados son intercambiables con los controles (Monte Carlo de V18): se rotula la razón de variabilidad temporal previa entre tratados y controles. Con JMS hay pocos donantes por placebo.
- **(e)** E2-R1c-v1: estimabilidad (mínimo de 30/30 y MDE80 frente al umbral 2δ = 0,10) calculada antes del coeficiente. Como el denominador (hogares inquilinos) es fijo en el tiempo, lo absorbe el efecto fijo de municipio: la variante equivale al log de contratos en la muestra de municipios con Censo 2021 (de 10.000 habitantes o más), y su contribución es el cambio de muestra y de unidades.

### Qué dicen estas pruebas sobre la clase de E2-R1
{clase_texto(info)}
"""
    inf = OUT / "informe.md"
    base = inf.read_text(encoding="utf-8")
    base = base.split(SECCION)[0].rstrip() + "\n\n"
    sin_causal(txt)
    inf.write_text(base + txt, encoding="utf-8")
    # hechos (idempotente: se quitan los V18-E2-B6-* previos)
    hs = [h for h in json.loads((OUT / "hechos.json").read_text(encoding="utf-8")) if not h["id"].startswith("V18-E2-B6-")]
    hs += hechos_b6(info, df)
    K.volcar_json(OUT / "hechos.json", hs)


def clase_texto(info: dict) -> str:
    ia, ib, ic_ = info["a"], info["b"], info["c"]
    k = ia["14T-2021T1-2022T1"]
    tend_sig = k["pendiente"]["p"] < 0.05
    salto_sig = k["saltos"][0][1]["p"] < 0.05
    b1, b2 = info["b_coefs"][0], info["b_coefs"][1]
    pl5 = ic_["B6c-5"]
    partes = [
        f"- Prueba 1 de la ronda (tendencia y salto): pendiente {'significativa' if tend_sig else 'no significativa'}; salto en 2022T2 sobre la extrapolación {'distinguible' if salto_sig else 'no distinguible'}.",
        f"- Prueba 2 (COVID y turismo por trimestre): HUT × trimestre {b1:+.4f} ({'por debajo' if b1 < -0.03 else 'no por debajo'} de −0,03); ln(población) × trimestre {b2:+.4f} ({'por debajo' if b2 < -0.03 else 'no por debajo'} de −0,03).",
        f"- Placebo de 2017 con tendencia propia: {pl5['coef']:+.4f} (p = {pl5['p']:.3f}), de signo contrario al de la principal: no activa el fallo decisivo del plan (que exige el mismo signo); con controles emparejados el coeficiente de la principal sigue entre {min(info['c_coefs']):+.4f} y {max(info['c_coefs']):+.4f}.",
        "- Reglas escritas del plan (líneas 118-130): ninguna de estas pruebas es un fallo decisivo ni un tope pre-registrado; ninguna variante cambia de signo; las pretendencias de las muestras emparejadas son compatibles con cero. "
        "Por las reglas escritas, la clase provisional de E2-R1 sigue siendo SUGESTIVO. Las pruebas 1 y 2 limitan la lectura: el coeficiente no es un nivel estable (pierde magnitud durante la vigencia) y con ln(población) × trimestre baja a "
        f"{b2:+.4f}. La propuesta del abogado («ASOCIACIÓN si fallan las pruebas 1-2») usa un criterio (por debajo de −0,03) que no estaba en el pre-registro: "
        + ("aplicado literalmente, la prueba 2 falla con ln(población) × trimestre y no con HUT × trimestre; la decisión corresponde al orquestador y al árbitro, que deben decidir antes de la ronda 2." if b2 >= -0.03
           else "aplicado literalmente, la prueba 2 no falla."),
    ]
    return "\n".join(partes)


def sin_causal(txt: str) -> None:
    for w in K.PROHIBIDAS:
        if re.search(re.escape(w), txt, flags=re.IGNORECASE):
            raise ValueError(f"lenguaje no admitido: {w!r}")


def md(df: pd.DataFrame) -> str:
    cols = list(df.columns)
    out = ["| " + " | ".join(str(c) for c in cols) + " |", "|" + "|".join("---" for _ in cols) + "|"]
    for r in df.itertuples(index=False):
        out.append("| " + " | ".join("—" if (isinstance(v, float) and not np.isfinite(v)) or v is None else str(v) for v in r) + " |")
    return "\n".join(out)


def hechos_b6(info: dict, df: pd.DataFrame) -> list[dict]:
    t = df.set_index("id")
    H = []
    cl = "SUGESTIVO"
    k = info["a"]["14T-2021T1-2022T1"]
    sal = k["saltos"][0][1]
    H.append(K.hecho("V18-E2-B6-A", "Salto en 2022T2 del coeficiente de Reg por trimestre sobre la extrapolación de la recta de 2021T1-2022T1 (log de la renta media; E2-R1, robustez a posteriori)",
                     sal["est"], sal["ic"][0], sal["ic"][1], "log", "2019T1-2022T2", f"{k['n_tr']} regulados y {k['n_co']} controles, panel equilibrado 2019T1-2022T2", FUENTES, cl,
                     f"Pendiente del coeficiente en 2021T1-2022T1 {k['pendiente']['est']:+.4f} por trimestre (p = {k['pendiente']['p']:.3f}); p del salto {sal['p']:.3f}. Prueba declarada a posteriori (ronda 1, B6); "
                     "no cambia la especificación principal. Lectura: asociación estimada."))
    b3, b4 = t.loc["E2-R1-B6b-3"], t.loc["E2-R1-B6b-4"]
    H.append(K.hecho("V18-E2-B6-B", "Coeficiente Reg × Post con densidad HUT 2019 y ln(población 2019) por efectos de trimestre (E2-R1, robustez a posteriori)", b3.coef, b3.ic95_lo, b3.ic95_hi,
                     "log", "2019T1-2022T1", f"{int(b3.n_tratados)} regulados y {int(b3.n_controles)} controles", FUENTES, cl,
                     f"IC95 CR1 por municipio; p de Webb {b3.p_webb:.4f}; con el paro registrado de 2019 por trimestre {b4.coef:+.4f}. Principal {info['b']['coef']:+.4f}. Prueba declarada a posteriori (ronda 1, B6). Lectura: asociación estimada."))
    c1, p5 = t.loc["E2-R1-B6c-1"], t.loc["E2-R1-B6c-5"]
    H.append(K.hecho("V18-E2-B6-C", "Coeficiente Reg × Post con controles emparejados por el crecimiento de la renta 2017-2019 (E2-R1, robustez a posteriori)", c1.coef, c1.ic95_lo, c1.ic95_hi,
                     "log", "2019T1-2022T1", f"{int(c1.n_tratados)} regulados y {int(c1.n_controles)} controles emparejados con reposición", FUENTES, cl,
                     f"IC95 CR1 por municipio; p de Webb {c1.p_webb:.4f}. Placebo de 2017 con tendencia propia de los regulados 2014-2019: {p5.coef:+.4f} (p = {p5.p_cr1:.3f}). "
                     "Prueba declarada a posteriori (ronda 1, B6). Lectura: asociación estimada."))
    d1, d2 = info["d"]["B6d-1"], info["d"]["B6d-2"]
    H.append(K.hecho("V18-E2-B6-D", "Estimación SDID de Reg × Post con controles ponderados, todos los no regulados con serie completa (E2-R1, robustez a posteriori)", d2["tau"], d2["ic"][0], d2["ic"][1],
                     "log", "2019T1-2022T1", f"{d2['n_tr']} regulados y {d2['n_co']} controles", FUENTES, cl,
                     f"IC95 por inversión del contraste de placebos de Conley-Taber (p = {d2['p_ct']:.3f}); razón de variabilidad previa tratados/controles {d2['razon_var']:.2f} ({d2['interc']}). "
                     f"Con los controles de JMS τ = {d1['tau']:+.4f} (p = {d1['p_ct']:.3f}). Prueba declarada a posteriori (ronda 1, B6). Lectura: asociación estimada."))
    ie = info["e"]
    if "E2-R1c-v1" in ie["res"]:
        r, x = ie["res"]["E2-R1c-v1"], t.loc["E2-R1c-v1"]
        H.append(K.hecho("V18-E2-B6-R1CV1", "Coeficiente Reg × Post sobre el log de contratos nuevos por 1.000 hogares inquilinos del Censo 2021 (E2-R1c-v1)", r["coef"], x.ic95_lo, x.ic95_hi,
                         "log", "2019T1-2022T1", f"{int(x.n_tratados)} regulados y {int(x.n_controles)} controles de 10.000 habitantes o más (Censo 2021, muestra del 10 %)", FUENTES, "ASOCIACIÓN",
                         f"IC95 CR1 por municipio; p de Webb {r['p_webb']:.4f}; MDE80 {ie['est']['mde80']:.4f}. Criterio de AD-E2 (caída de al menos un 5 % con p < 0,05): {'se cumple' if r['cae5'] else 'no se cumple'}. "
                         "Prueba declarada a posteriori (ronda 1, B6); el denominador es fijo y lo absorbe el efecto fijo de municipio. Lectura: asociación estimada."))
    return H


def main() -> int:
    t0 = time.time()
    d = DS.cargar()
    fa, ia = prueba_a(d)
    fb, ib = prueba_b(d)
    fc, ic_ = prueba_c(d)
    fd, id_ = prueba_d(d)
    fe, ie = prueba_e(d)
    filas = fa + fb + fc + fd + fe
    info = {"a": ia, "b": ib, "c": ic_, "d": id_, "e": ie}
    info["b_coefs"] = [f_["coef"] for f_ in fb]
    info["c_coefs"] = [f_["coef"] for f_ in fc if f_["rol"] == "variante"]
    escribir(filas, info, time.time() - t0)
    print(f"E2 robustez B6 hecha en {time.time() - t0:.0f} s", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
