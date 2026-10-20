"""V18 · fase 4 · E1 · estimación de lo que supera la estimabilidad (R3, R4 y la coprincipal P-H3), sus variantes enumeradas, las pruebas B4, Holm y la clasificación I1-I8.

Análisis V18; capa C4; pre-registro interno plan-replicacion-v18. Lo que no supera la estimabilidad (R1, R2, A1) solo deja filas «NO ESTIMABLE» con su MDE.
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
import _e2e8_comun as K  # noqa: E402
import e1_estim as E  # noqa: E402
import e1_nucleo as N  # noqa: E402

B_PRINCIPAL, B_VAR = 9999, 1999
ANEXO_A = None     # se rellena desde e1_turismo (evita importación circular)


def _anexo():
    import e1_turismo as T
    return T.ANEXO_A


def robustez(coef: float, ic: tuple, variantes: list[dict], diag: list[dict]) -> dict:
    """I5: mismo signo en las pruebas B4 que aplican (diag) y en ≥ 80 % de las variantes enumeradas; IC95 de cada variante comparable solapa con el de la principal."""
    cambio = any(np.isfinite(d["coef"]) and d["coef"] * coef < 0 for d in diag)
    vs = [v for v in variantes if np.isfinite(v["coef"])]
    frac = float(np.mean([v["coef"] * coef > 0 for v in vs])) if vs else np.nan
    comp = [v for v in vs if v.get("comparable", True)]
    solape = all((v["ic95"][0] <= ic[1] and v["ic95"][1] >= ic[0]) for v in comp) if comp else None
    return {"cambio_signo": bool(cambio), "frac_mismo_signo": frac, "solape_ic": solape, "n_variantes": len(vs)}


def clasificar(info: dict) -> dict:
    return K.clasificar(info)


def _fila(id_, rol, estado, resultado="", **kw) -> dict:
    base = {"id": id_, "rol": rol, "estado": estado, "resultado": resultado, "n_obs": np.nan, "n_unidades": np.nan, "G": np.nan, "ventana": "", "coef": np.nan, "se": np.nan, "ic95_lo": np.nan,
            "ic95_hi": np.nan, "p_cr1": np.nan, "p_webb": np.nan, "p_i7": np.nan, "p_holm": np.nan, "q_by": np.nan, "mde80": np.nan, "umbral": np.nan, "inferencia": "", "banda": "", "clase": "",
            "razon_ref": np.nan, "coherente_ref": "", "nota": ""}
    base.update(kw)
    return base


def estimar_todo(B: pd.DataFrame, C: pd.DataFrame, gsf: pd.DataFrame, est: dict, ok: dict, rng, reg, pe: pd.DataFrame, forzar: bool = False) -> dict:
    """forzar = True solo en el ensayo de código con resultado sintético: ignora la decisión de estimabilidad para recorrer todo el código."""
    A = _anexo()
    if not forzar:
        if not (ok["E1-R3"] and ok["E1-R4"]):
            raise NotImplementedError("E1-R3 o E1-R4 no estimable: el informe de e1_salidas asume ambas estimadas; reescribir las salidas")
        if ok["E1-R1"] or ok["E1-R2"] or ok["E1-A1"]:
            raise NotImplementedError("E1-R1, R2 o A1 estimable: su estimación existe en e1_estim (r1, r2, a1) pero e1_resultados no la orquesta todavía")
    filas: list[dict] = []
    out: dict = {"est": est, "ok": ok}

    # ------------------------------------------------------------------ lo que no supera la estimabilidad
    for ident in ("E1-R1", "E1-R2", "E1-A1"):
        e = est[ident]
        filas.append(_fila(ident, "principal", e["decision"], "ln SERPAVI (VC)", n_obs=e.get("n_obs", np.nan), n_unidades=e.get("n_unidades", np.nan), G=e.get("G", np.nan),
                           mde80=e.get("mde80", np.nan), umbral=e["umbral"], clase="NO ESTIMABLE", nota=e["decision"]))
        for suf, dim, desc in A.get(ident, []):
            filas.append(_fila(f"{ident}-{suf}", "variante", "no estimada (principal NO ESTIMABLE)", f"[{dim}] {desc}", clase="NO ESTIMABLE"))
    filas.append(_fila("E1-A2", "principal", "NO ESTIMADA en esta pasada", "dCDH con dosis continua (registro de Andalucía)", clase="NO ESTIMABLE",
                       nota="el Monte Carlo de V18 valida dCDH solo con aleatorización del calendario entre 8 CCAA (K5): con dos ciudades la inferencia no está validada y la adenda la deja «solo descriptiva»; "
                            "no se estima ni entra en Holm (desviación D8)"))
    for suf, dim, desc in A["E1-A2"]:
        filas.append(_fila(f"E1-A2-{suf}", "variante", "no estimada (principal no estimada)", f"[{dim}] {desc}", clase="NO ESTIMABLE"))
    filas.append(_fila("E1-A3", "variante (robustez de A1)", "no estimada (A1 NO ESTIMABLE)", "registro reconstruido de la GVA", clase="NO ESTIMABLE", nota="clasificación máxima ASOCIACIÓN; solo robustez de A1"))
    for i, n in (("E1-A4", "regulaciones locales (PEUAT, moratorias): faltan la geometría del PEUAT y las fechas (tareas_autor, punto 13)"),
                 ("E1-A5", "InsideAirbnb como exposición: solo hay instantáneas desde 2025-12 (tareas_autor, punto 14)"),
                 ("E1-X1", "precio de compra por barrio: no hay dato en abierto (Open Data BCN no publica la serie de compraventa por barrio)")):
        filas.append(_fila(i, "NO ESTIMABLE", "NO ESTIMABLE (datos)", n, clase="NO ESTIMABLE", nota=n))

    # ------------------------------------------------------------------ R3
    r3 = E.r3(B, None, webb_B=B_PRINCIPAL, rng=rng)
    ev3 = E.r3_evento(B)
    sd3 = r3["_sd_dosis"]
    M3 = r3["_res"]["modelo"]
    ck = E.coords_km(r3["_d"])
    conley3 = {c: M3.conley(ck, c) for c in (1.0, 2.0)}
    var3 = {}
    for suf, dim, desc in A["E1-R3"]:
        rv = E.r3(B, suf)
        var3[suf] = rv
    med3 = {}
    for nombre, col in (("y_vu", "y_vu"), ("y_mes", "y_mes")):
        try:
            rr = E.r3(B.assign(y=B[col]), None)
            med3[nombre] = {"coef": rr["coef_por_pp"], "ic95": rr["ic95_por_pp"], "p": rr["p_principal"], "n": rr["n"]}
        except Exception as e:  # noqa: BLE001  (p. ej. sin observaciones suficientes de vivienda unifamiliar en las secciones céntricas)
            med3[nombre] = {"coef": np.nan, "ic95": (np.nan, np.nan), "p": np.nan, "n": 0, "error": str(e)[:60]}
    d0 = E.muestra(B, E.ANIOS_R3, ["y", "dosis0"])
    var_y = d0.groupby("cod_seccion").y.agg(lambda s: s.iloc[-1] - s.iloc[0]).abs()
    atip3 = E.sin_extremos(d0, "dosis0") | set(var_y[var_y > var_y.quantile(0.99)].index)
    ra3 = E.r3(B.assign(y=np.where(B.cod_seccion.isin(atip3), np.nan, B.y)), None)
    med3["sin_atipicos"] = {"coef": ra3["coef_por_pp"], "ic95": ra3["ic95_por_pp"], "p": ra3["p_principal"], "n": ra3["n"], "n_excluidas": len(atip3)}
    moran3 = K.moran_i(K.residuo_medio_por_unidad(M3), ck, k=5, B=999)
    # r3: la tendencia por distancia de 2011-2013 decide si v3 pasa a coprincipal (adenda R-15)
    v3_copr = bool(ev3["tendencia_distancia"]["p"] < 0.10)
    out["R3"] = {"r": r3, "ev": ev3, "conley": conley3, "var": var3, "medidas": med3, "moran": moran3, "v3_coprincipal": v3_copr, "sd": sd3}
    R3 = out["R3"]

    # ------------------------------------------------------------------ R4
    cnt = E.r4_conteos(gsf)
    r4 = E.r4(B, gsf, None, webb_B=B_PRINCIPAL, rng=rng)
    M4 = r4["_res"]["modelo"]
    ic4 = M4.webb_ic(B_VAR, np.random.default_rng(K.SEMILLA))
    ev4 = E.r4_eventos(r4["_d"])
    var4 = {}
    for suf in ("v1", "v2", "v3"):
        var4[suf] = E.r4(B, gsf, suf, webb_B=B_VAR if suf in ("v2", "v3") else 0, rng=np.random.default_rng(K.SEMILLA))
    # K8 bis: la variante con adelantos (E1-R4-v3, estudio de eventos) se publica al lado con su IC95 y su IC90 por inversión del contraste de Webb
    M4v3 = var4["v3"]["_res"]["modelo"]
    ic95_v3 = M4v3.webb_ic(B_VAR, np.random.default_rng(K.SEMILLA))
    ic90_v3 = M4v3.webb_ic(B_VAR, np.random.default_rng(K.SEMILLA), nivel=0.10)
    var4["v3"]["ic95"] = (float(ic95_v3[0]), float(ic95_v3[1]))
    med4 = {}
    for nombre, col in (("y_vu", "y_vu"), ("y_mes", "y_mes")):
        try:
            rr = E.r4(B.assign(y=B[col]), gsf, None, webb_B=0)
            med4[nombre] = {"coef": rr["coef"], "ic95": rr["ic95"], "p": rr["p_principal"], "n": rr["n"]}
        except Exception as e:  # noqa: BLE001
            med4[nombre] = {"coef": np.nan, "ic95": (np.nan, np.nan), "p": np.nan, "n": 0, "error": str(e)[:60]}
    moran4 = K.moran_i(K.residuo_medio_por_unidad(M4), E.coords_km(r4["_d"]), k=5, B=999)
    out["R4"] = {"r": r4, "ev": ev4, "var": var4, "medidas": med4, "moran": moran4, "ic_webb": ic4, "conteos": cnt, "v3_ic90": (float(ic90_v3[0]), float(ic90_v3[1])), "v3_ic95": var4["v3"]["ic95"]}
    R4 = out["R4"]

    # ------------------------------------------------------------------ P-H3
    ph = E.ph3()
    out["PH3"] = ph

    # ------------------------------------------------------------------ Holm (familia E1: contrastes estimados tras las comprobaciones previas)
    tam3 = est["E1-R3"]["tamano_nominal"]
    p3 = K.p_corr(r3["p_principal"], tam3)
    tam4 = est["E1-R4"].get("tamano_webb_5pct", np.nan)
    p4 = K.p_corr(r4["_res"]["p_webb"], tam4 if np.isfinite(tam4) else None)
    familia = {"E1-R3": p3, "E1-R4": p4, "E1-P-H3": K.p_corr(ph["p_principal"], None)}
    if v3_copr:
        familia["E1-R3-v3"] = K.p_corr(var3["v3"]["p_principal"], tam3)
    holm = K.holm_familia(familia)
    out["familia"], out["holm"] = familia, holm
    out["tam"] = {"R3": tam3, "R4": tam4}

    # ------------------------------------------------------------------ clasificación
    ref3_sd = E.REF["E1-R3"] * sd3
    d3_sd = E.DELTA["E1-R3"] * sd3
    tost3 = K.tost(r3["coef"], r3["se"], d3_sd, r3["G"] - 1)
    pre3 = ev3["pretend"]
    rob3 = robustez(r3["coef_por_pp"], r3["ic95_por_pp"],
                    [{"coef": v["coef_por_pp"] if np.isfinite(v["coef_por_pp"]) else v["coef"], "ic95": v["ic95_por_pp"] if np.isfinite(v["coef_por_pp"]) else v["ic95"],
                      "comparable": np.isfinite(v["coef_por_pp"])} for v in var3.values()],
                    [med3["y_vu"], med3["y_mes"], med3["sin_atipicos"]])
    info3 = {"estimable": True, "coprincipal": False, "p_holm": holm["E1-R3"], "coef": r3["coef"], "tost": tost3, "pretend_p": pre3["p"], "roth_ok": bool(pre3["sesgo_post"] < d3_sd) if np.isfinite(pre3["sesgo_post"]) else None,
             "placebo_fecha": {"p": ev3["placebo_fecha"]["p"], "coef": ev3["placebo_fecha"]["coef"], "mismo_signo": bool(ev3["placebo_fecha"]["coef"] * r3["coef"] > 0)},
             "placebo_resultado": "no aplica (2011-2019: la población de 65 años o más por sección existe solo desde 2021; adenda R-15)", "robustez": rob3,
             "inferencia_banda": K.banda_mc(tam3), "topes": ["tope de la especificación: SUGESTIVO (sin instrumento; la exogeneidad estricta no se contrasta)"],
             "debiles_extra": ["inferencia con valor crítico corregido por tamaño (tamaño del Monte Carlo de este diseño: %.3f)" % tam3] if not (0.04 <= tam3 <= 0.06) else []}
    cl3 = clasificar(info3)
    cl3["info"] = info3

    d4_ = E.DELTA["E1-R4"]
    r4_ic = ic4
    # TOST (adenda 1.1; K8): equivalencia con el IC90 por inversión del contraste de Webb (la inferencia principal), no con el IC de CR1 con 5 clusters
    ic90_4 = M4.webb_ic(B_VAR, np.random.default_rng(K.SEMILLA), nivel=0.10)
    tost4 = {"ic90": (float(ic90_4[0]), float(ic90_4[1])), "delta": d4_, "equivalente": bool(ic90_4[0] > -d4_ and ic90_4[1] < d4_), "metodo": "IC90 por inversión del contraste de Webb"}
    pre4 = ev4["pretend"]
    rob4 = robustez(r4["coef"], r4_ic, [{"coef": v["coef"], "ic95": v["ic95"], "comparable": True} for v in var4.values()], [med4["y_vu"], med4["y_mes"]])
    # variante con adelantos: misma clasificación aplicada a su coeficiente y a su IC90 de Webb (su p de Webb sin ajuste de Holm: no entra en la familia)
    pv3 = var4["v3"]["_res"]["p_webb"]
    tost_v3 = {"ic90": out["R4"]["v3_ic90"], "delta": d4_, "equivalente": bool(ic90_v3[0] > -d4_ and ic90_v3[1] < d4_), "metodo": "IC90 por inversión del contraste de Webb"}
    info4 = {"estimable": True, "coprincipal": False, "p_holm": holm["E1-R4"], "coef": r4["coef"], "tost": tost4, "pretend_p": pre4["p"], "roth_ok": bool(pre4["sesgo_post"] < d4_) if np.isfinite(pre4["sesgo_post"]) else None,
             "placebo_fecha": {"p": ev4["placebo_fecha"]["p"], "coef": ev4["placebo_fecha"]["coef"], "mismo_signo": bool(ev4["placebo_fecha"]["coef"] * r4["coef"] > 0)},
             "placebo_resultado": "no aplica (2011-2019: sin población de 65 años o más por sección)", "robustez": rob4, "inferencia_banda": "apta" if (np.isfinite(tam4) and 0.04 <= tam4 <= 0.06) else K.banda_mc(tam4) if np.isfinite(tam4) else "sin medida",
             "topes": ["tope de la especificación: SUGESTIVO (un solo grupo tratado: la Sagrada Família)"],
             "debiles_extra": []}      # Webb apto con la mitad de los clusters tratados (Monte Carlo de V18; tamaño propio del diseño %.3f)
    cl4 = clasificar(info4)
    cl4["info"] = info4
    info4v3 = {**info4, "coef": var4["v3"]["coef"], "tost": tost_v3, "p_holm": K.p_corr(pv3, tam4 if np.isfinite(tam4) else None)}
    cl4v3 = clasificar(info4v3)
    cl4v3["info"] = info4v3
    out["R4"]["v3_clase"] = cl4v3
    out["clases"] = {"E1-R3": cl3, "E1-R4": cl4, "E1-R4-v3": cl4v3}

    # ------------------------------------------------------------------ filas de la tabla
    r3d = r3
    filas.append(_fila("E1-R3", "principal", "estimada", "ln SERPAVI (VC) por pp de densidad HUT de 2018T2 (media de β_k 2014-2019)", n_obs=r3["n"], n_unidades=r3["n_unidades"], G=r3["G"], ventana=r3["ventana"],
                       coef=r3["coef_por_pp"], se=r3["se"] / sd3, ic95_lo=r3["ic95_por_pp"][0], ic95_hi=r3["ic95_por_pp"][1], p_cr1=r3["p_principal"], p_webb=r3["_res"]["p_webb"], p_i7=p3, p_holm=holm["E1-R3"],
                       mde80=est["E1-R3"]["mde80"], umbral=est["E1-R3"]["umbral"], inferencia="CR1 t(G−1) por barrio; Webb 9.999 al lado", banda=K.banda_mc(tam3), clase=cl3["clase"], razon_ref=r3["razon_ref"],
                       coherente_ref="coherente" if r3["coherente_ref"] else "no coherente", nota=f"coef por DT de la dosis {r3['coef']:.5f} (DT = {sd3:.3f} pp)"))
    for suf, dim, desc in A["E1-R3"]:
        v = var3[suf]
        cpp = v["coef_por_pp"] if np.isfinite(v["coef_por_pp"]) else v["coef"]
        lo, hi = (v["ic95_por_pp"] if np.isfinite(v["coef_por_pp"]) else v["ic95"])
        filas.append(_fila(f"E1-R3-{suf}", "variante" if not (suf == "v3" and v3_copr) else "coprincipal (tendencia por distancia con p < 0,10)", "estimada", f"[{dim}] {desc}", n_obs=v["n"],
                           n_unidades=v["n_unidades"], G=v["G"], ventana=v["ventana"], coef=cpp, se=v["se"] / (sd3 if np.isfinite(v["coef_por_pp"]) else 1), ic95_lo=lo, ic95_hi=hi, p_cr1=v["p_principal"], p_i7=K.p_corr(v["p_principal"], tam3),
                           p_holm=holm.get("E1-R3-v3", np.nan) if suf == "v3" else np.nan, inferencia="CR1 t(G−1) por barrio", clase="no se clasifica" if (suf == "v3" and v3_copr) else "",
                           nota="unidad: log por DT de la dosis binaria" if suf == "v2" else ""))
    qs = N.by([var3[s]["p_principal"] for s, _, _ in A["E1-R3"]])
    for (suf, _, _), q in zip(A["E1-R3"], qs):
        for f in filas:
            if f["id"] == f"E1-R3-{suf}":
                f["q_by"] = q

    filas.append(_fila("E1-R4", "principal", "estimada", "ln SERPAVI (VC): < 500 m de la Sagrada Família frente al anillo 500-1.000 m, 2014-2019 frente a 2013, sin los adelantos de 2011-2012 como regresores (K8 bis)", n_obs=r4["n"], n_unidades=r4["n_unidades"], G=r4["G"],
                       ventana=r4["ventana"], coef=r4["coef"], se=r4["se"], ic95_lo=ic4[0], ic95_hi=ic4[1], p_cr1=r4["p_principal"], p_webb=r4["_res"]["p_webb"], p_i7=p4, p_holm=holm["E1-R4"], mde80=est["E1-R4"]["mde80"],
                       umbral=est["E1-R4"]["umbral"], inferencia="wild cluster bootstrap de Webb (9.999) por barrio; IC por inversión (1.999)", banda=("apta" if (np.isfinite(tam4) and 0.04 <= tam4 <= 0.06) else K.banda_mc(tam4) if np.isfinite(tam4) else "sin medida"),
                       clase=cl4["clase"], nota=f"{r4['n_tratadas']} secciones tratadas en {r4['G_tratados']} barrios y {r4['n_control']} de control"))
    for suf, dim, desc in A["E1-R4"]:
        v = var4[suf]
        filas.append(_fila(f"E1-R4-{suf}", "variante", "estimada", f"[{dim}] {desc}", n_obs=v["n"], n_unidades=v["n_unidades"], G=v["G"], ventana=v["ventana"], coef=v["coef"], se=v["se"], ic95_lo=v["ic95"][0],
                           ic95_hi=v["ic95"][1], p_cr1=v["p_principal"], p_webb=v["_res"].get("p_webb", np.nan), p_i7=v["_res"].get("p_webb", v["p_principal"]), inferencia="Webb por barrio" if suf in ("v2", "v3") else "CR1 t(G−1) por barrio",
                           clase=cl4v3["clase"] if suf == "v3" else "",
                           nota=(f"{v['n_tratadas']} tratadas y {v['n_control']} de control" + (f"; IC95 e IC90 por inversión de Webb; IC90 ({out['R4']['v3_ic90'][0]:.4f}; {out['R4']['v3_ic90'][1]:.4f})" if suf == "v3" else ""))))
    qs = N.by([var4[s]["_res"].get("p_webb", var4[s]["p_principal"]) for s, _, _ in A["E1-R4"]])
    for (suf, _, _), q in zip(A["E1-R4"], qs):
        for f in filas:
            if f["id"] == f"E1-R4-{suf}":
                f["q_by"] = q

    filas.append(_fila("E1-P-H3", "coprincipal", "estimada", "ln SERPAVI (VC) por DT intra-sección del % de viviendas turísticas (INE), 2021-2024, muestra V18", n_obs=ph["n"], n_unidades=ph["n_secciones"], G=ph["G"], ventana=ph["ventana"],
                       coef=ph["coef"], se=ph["se"], ic95_lo=ph["ic95"][0], ic95_hi=ph["ic95"][1], p_cr1=ph["p_principal"], p_i7=ph["p_principal"], p_holm=holm["E1-P-H3"], inferencia=ph["inferencia"], clase="no se clasifica",
                       nota="repite H3 de V15 (0,0030 por DT, p = 0,931) en la muestra V18; no se clasifica (adenda 1.6)"))
    # ------------------------------------------------------------------ diagnósticos al Registry (no cuentan en el multiverso: adenda 1.8)
    def diag(ident, nombre, valor, pv, nota):
        reg.log("v18-E1-diagnostico", f"{ident}/{nombre}", nota, "", "", 0, np.nan, np.nan, np.nan, coef_interes=valor, p_interes=pv, notas="diagnóstico; no cuenta en el multiverso")
    diag("E1-R3", "pretendencias", np.nan, pre3["p"], "contraste conjunto de los adelantos 2011-2012")
    diag("E1-R3", "roth_pendiente_80", pre3["pendiente_detectable"], np.nan, "pendiente previa detectable al 80 %")
    diag("E1-R3", "placebo_fecha_2012", ev3["placebo_fecha"]["coef"], ev3["placebo_fecha"]["p"], "adopción falsa en 2012, ventana 2011-2013")
    diag("E1-R3", "tendencia_distancia_2011_2013", ev3["tendencia_distancia"]["coef"], ev3["tendencia_distancia"]["p"], "Δ ln y 2011-2013 sobre la distancia al centro")
    for c_, s_ in R3["conley"].items():
        diag("E1-R3", f"conley_{c_:g}km", s_, float(2 * __import__("scipy.stats", fromlist=["t"]).t.sf(abs(r3["_res"]["coef"] / s_), r3["G"] - 1)), "Conley (Bartlett) sobre la media posterior")
    diag("E1-R3", "moran_residuos", R3["moran"]["I"], R3["moran"]["p_unilateral"], "I de Moran de los residuos medios por sección")
    for h in ev3["honest"]:
        diag("E1-R3", f"honest_Mbar_{h['Mbar']:g}", float(np.mean(h["ic95"])), np.nan, f"IC95 ({h['ic95'][0]:.4f}; {h['ic95'][1]:.4f}); informativo")
    for nombre, v in med3.items():
        diag("E1-R3", f"medida_{nombre}", v["coef"], v["p"], "robustez de la medida o de la muestra (por pp)")
    diag("E1-R4", "pretendencias", np.nan, pre4["p"], "contraste conjunto de los adelantos 2011-2012")
    diag("E1-R4", "roth_pendiente_80", pre4["pendiente_detectable"], np.nan, "pendiente previa detectable al 80 %")
    diag("E1-R4", "placebo_fecha_2012", ev4["placebo_fecha"]["coef"], ev4["placebo_fecha"]["p"], "adopción falsa en 2012, ventana 2011-2013")
    diag("E1-R4", "moran_residuos", R4["moran"]["I"], R4["moran"]["p_unilateral"], "I de Moran de los residuos medios por sección")
    for h in ev4["honest"]:
        diag("E1-R4", f"honest_Mbar_{h['Mbar']:g}", float(np.mean(h["ic95"])), np.nan, f"IC95 ({h['ic95'][0]:.4f}; {h['ic95'][1]:.4f}); informativo")
    for nombre, v in med4.items():
        diag("E1-R4", f"medida_{nombre}", v["coef"], v["p"], "robustez de la medida")
    for _, row in pe.iterrows():
        reg.log("v18-E1-diagnostico", f"{row['id']}/primera_etapa", "F efectivo de la primera etapa sin el resultado", "", "", int(row["n"]), np.nan, np.nan, np.nan, coef_interes=row["F_efectivo"], p_interes=np.nan,
                notas="diagnóstico de diseño; no cuenta en el multiverso")
    for k_, e_ in est.items():
        diag(k_, "mde80", e_.get("mde80", np.nan), np.nan, f"MDE80 (umbral {e_['umbral']:.4f})")

    out["filas"] = filas
    for f in filas:
        if f["estado"] == "estimada":
            reg.log("v18-E1-estimada", f["id"], f["resultado"], "", "", int(f["n_obs"]) if f["n_obs"] == f["n_obs"] else 0, np.nan, np.nan, np.nan, coef_interes=f["coef"],
                    p_interes=f["p_i7"] if f["p_i7"] == f["p_i7"] else f["p_cr1"], notas=f"{f['rol']}; clase {f['clase']}")
        else:
            reg.log("v18-E1-no-estimada", f["id"], f["resultado"], "", "", 0, np.nan, np.nan, np.nan, notas=f["estado"])
    reg.flush()
    return out
