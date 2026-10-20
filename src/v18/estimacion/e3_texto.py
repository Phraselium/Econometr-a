"""V18 · E3 · redacción de salidas: resultado.json, hechos.json e informe.md.

Análisis V18; capa C4; pre-registro interno plan-replicacion-v18. Sin lenguaje causal en las cifras (check_v18): «asociación condicionada al diseño», «estimación».
"""
from __future__ import annotations

import numpy as np
import pandas as pd

import _e359_comun as K
from e3_salidas import DATOS_QUE_FALTAN, ficha

ROT = K.ROTULO
FUENTES = ["Eurostat cens_01rsctz (Censo 2001, INE)", "Eurostat migr_imm1ctz (INE)", "MIVAU valor tasado e iniciadas", "base del proyecto: pob_extranj, pob_total",
           "Eurostat demo_r_pjanaggr3 y nama_10r_3empers (INE)"]


def tabla_md(df: pd.DataFrame, cols: list[str], fmt: dict | None = None) -> str:
    fmt = fmt or {}
    def f(c, v):
        if v is None or (isinstance(v, float) and not np.isfinite(v)):
            return "—"
        if c in fmt:
            return fmt[c](v)
        if isinstance(v, float):
            return f"{v:.4g}"
        return str(v)
    h = "| " + " | ".join(cols) + " |\n|" + "|".join("---" for _ in cols) + "|\n"
    for _, r in df.iterrows():
        h += "| " + " | ".join(f(c, r.get(c)) for c in cols) + " |\n"
    return h


def g4(x):
    if x is None or (isinstance(x, float) and np.isnan(x)):
        return "—"
    if isinstance(x, (float, np.floating)) and np.isinf(x):
        return "no acotado"
    return f"{x:.4g}"


def escribir_texto(E3, dat, specs, mspecs, mde_tab, res, ne, pd4, pq3, diag, clas, ph, qby, var_por_padre, tabla, B, t0):
    REF = E3.REF
    SAL = E3.SALIDA
    todas = {s["id"]: s for s in specs + mspecs}
    # ---- titular
    tit = "E3-R1" if "E3-R1" in res else next((i for i in clas if i in res and clas[i]["clase"] not in ("NO ESTIMABLE",)), None)
    ft = ficha(res[tit]) if tit else None
    # ---- resultado.json
    esp = {}
    for sid, s in todas.items():
        if sid in ne:
            m = mde_tab.get(sid, {})
            esp[sid] = {"rol": s["rol"], "clasificacion_v18": "NO ESTIMABLE", "motivo": ne[sid], "mde80": m.get("mde80"), "referencia": REF[s["ref"]]["v"] if s["ref"] in REF else None,
                        "datos_que_lo_harian_estimable": DATOS_QUE_FALTAN, "capa": "C4", "nivel_evidencia": "EXPLORATORIO"}
            continue
        if sid not in res:
            continue
        f = ficha(res[sid])
        d = {"rol": s["rol"], "padre": s.get("padre"), "estimacion": f["beta"], "se": f["se"], "ic95": [f["ic_lo"], f["ic_hi"]], "ic95_t": list(f["ic95_t"]), "ar": {"tipo": f["ar_tipo"], "lo": f["ar_lo"], "hi": f["ar_hi"]},
             "F_efectivo": f["F_eff"], "p_webb_ar": f["p_webb_ar"], "p_ar_exacto": f["p_ar"], "p_final": f["p_final"], "p_ajustado": ph.get(sid), "q_BY": qby.get(sid), "N": f["n"],
             "clusters": f["G"], "capa": "C4", "nivel_evidencia": "EXPLORATORIO", "nota": s["nota"], "mco": f["mco"]}
        if sid in clas:
            c = clas[sid]
            d["clasificacion_v18"] = c["clase"]
            d["razones"] = c["razones"]
            d["i6"] = c.get("i6")
            d["tost"] = c.get("tost")
            d["robustez"] = c.get("robustez")
        if sid in mde_tab:
            d["mde"] = {k: v for k, v in mde_tab[sid].items() if k != "curva"}
        if sid in diag:
            d["diagnosticos"] = diag[sid]
        esp[sid] = d
    esp["E3-P-D4"] = {"rol": "coprincipal", "clasificacion_v18": "no se clasifica", "estimacion": pd4["valor tasado"]["beta"], "se": pd4["valor tasado"]["se"],
                      "ic95": [pd4["valor tasado"]["ic_webb_ar"]["lo"], pd4["valor tasado"]["ic_webb_ar"]["hi"]], "F_efectivo": pd4["valor tasado"]["F_eff"], "p_ajustado": ph["E3-P-D4"],
                      "detalle": pd4, "capa": "C4", "nivel_evidencia": "EXPLORATORIO"}
    esp["E3-P-Q3c1"] = {"rol": "coprincipal", "clasificacion_v18": "no se clasifica", "estimacion": pq3["beta"], "se": pq3["se"], "ic95": list(pq3["ic_webb"]), "p_ajustado": ph["E3-P-Q3c1"], "detalle": pq3,
                        "capa": "C4", "nivel_evidencia": "EXPLORATORIO"}
    b5 = {"propia_E3-R2": esp.get("E3-R2", {}).get("clasificacion_v18"), "respaldo_E3-A1": esp.get("E3-A1", {}).get("clasificacion_v18"),
          "lectura": "la estimación propia de E3 para B5 (E3-R2) y su respaldo (E3-A1) son NO ESTIMABLES por variación (adenda 1.3 y 1.9): E3 no aporta magnitud propia a B5; entra solo la literatura"}
    out = {
        "rama": "v18/estimacion/e3", "pregunta": "¿Qué asociación hay entre la entrada de inmigrantes y el precio de la vivienda (y el alquiler) por provincia y municipio, identificada con el asentamiento histórico por origen?",
        "capa": "C4", "datos": "Panel de 39 provincias de entrenamiento (sin las 11 de v6): valor tasado MIVAU, iniciadas MIVAU, padrón (extranjeros y población), entradas por nacionalidad (Eurostat/INE), Censo de 2001 por nacionalidad (Eurostat/INE); municipal: padrón por nacionalidad 2003-2022 y SERPAVI",
        "N": ft["n"] if ft else None, "metodo": "IV de asentamiento histórico (shift-share) en primeras diferencias con efectos región-año y controles; inferencia por provincia: bootstrap de Webb con nulo impuesto sobre la forma reducida (Webb-AR, 9.999) y Anderson-Rubin exacto agrupado; F efectivo de Montiel Olea-Pflueger; MDE al 80 %",
        "estimacion": ft["beta"] if ft else None, "ic95": [ft["ic_lo"], ft["ic_hi"]] if ft else None, "p_ajustado": ph.get(tit) if tit else None, "nivel_evidencia": "EXPLORATORIO",
        "clasificacion_v18": clas[tit]["clase"] if tit in clas else None, "especificacion_titular": tit, "unidad_titular": REF["R1"]["unidad"] if tit == "E3-R1" else None,
        "diagnosticos": {"b5": b5, "familia_holm": {"m": len(ph), "p_ajustados": ph}, "inv_hhi_E3-R1": mde_tab.get("E3-R1", {}).get("inv_hhi_origen"), "estado_I8": "pendiente (replicador-ciego, B6)",
                         "mde": {k: {"mde80": v["mde80"], "ref": v["ref"], "estimable": v["estimable"]} for k, v in mde_tab.items()}},
        "fuera_muestra": {"modelo": None, "rmse": None, "dm_vs_ar4": None, "nota": "diseño de efectos con muestra de entrenamiento; la evaluación sellada (evaluate_v18) es posterior y no se ejecuta en V18"},
        "notas": ["análisis V18; capa C4; pre-registro interno plan-replicacion-v18", "clasificación provisional: pendiente de I8 (réplica ciega, B6)",
                  "sellado: sin las 11 provincias de v6, sin los municipios de V15 y V16; ningún acceso a data/sealed", "desviaciones: docs/v18/desviaciones_e3_e5_e9.md"],
        "especificaciones": esp,
    }
    K.volcar_json(SAL / "resultado.json", out)
    # ---- hechos.json
    H = []
    per = "2002, 2004-2008"
    for sid in ("E3-R1",):
        if sid in res:
            f = ficha(res[sid])
            c = clas[sid]["clase"]
            H.append(K.hecho("V18-E3-R1-beta", "E3-R1: asociación entre la entrada de extranjeros y la variación anual del valor tasado, estimación IV de asentamiento histórico", f["beta"], f["ic_lo"], f["ic_hi"],
                             "€/m² por punto de población (IC95 Webb-AR)", per, "39 provincias de entrenamiento; N = %d; sin las 11 provincias de v6" % f["n"], FUENTES, c,
                             f"Referencia IZA 2009: 44,72 €/m² por punto. Clase provisional, pendiente de I8. {clas[sid]['i6']['texto']}"))
            H.append(K.hecho("V18-E3-R1-F", "E3-R1: F efectivo de Montiel Olea-Pflueger de la primera etapa", f["F_eff"], None, None, "estadístico F", per, "39 provincias", FUENTES, c,
                             "El F efectivo no basta como criterio de potencia (Monte Carlo de V18)."))
    for sid, m in mde_tab.items():
        s = todas[sid]
        cl = clas[sid]["clase"] if sid in clas else "NO ESTIMABLE"
        if s["rol"] == "coprincipal":
            continue
        extra = "" if np.isfinite(m["mde80"]) else f" El MDE supera {g4(m['curva'][-1][0])} (seis errores típicos de referencia): no se alcanza el 80 % de potencia."
        H.append(K.hecho(f"V18-E3-{sid[3:]}-MDE80", f"{sid}: efecto mínimo detectable al 80 % de potencia con la variación real del diseño", m["mde80"], None, None, REF[s["ref"]]["unidad"],
                         str(s["cfg"]["ventana"] if "cfg" in s else s["cfgm"]["ventana"]), "comprobación previa por MDE (adenda 1.3), R = %d" % m["R"], FUENTES, cl,
                         f"Referencia única {REF[s['ref']]['v']} {REF[s['ref']]['unidad']}; estimable si el MDE no la supera. σ del preperiodo declarada (no vista en V15 o V16).{extra}"))
    if "E3-R1" in mde_tab:
        H.append(K.hecho("V18-E3-1HHI", "E3: número efectivo de choques (1/HHI de los pesos por origen)", mde_tab["E3-R1"]["inv_hhi_origen"]["por_origen"], None, None, "choques efectivos", per,
                         "8 grupos de origen", FUENTES, clas["E3-R1"]["clase"] if "E3-R1" in clas else "NO ESTIMABLE", "Menos de 20: inferencia principal por provincia con Webb más AR (adenda 1.13)."))
    for sid in ("E3-A3",):
        if sid in res:
            f = ficha(res[sid])
            H.append(K.hecho("V18-E3-A3-beta", "E3-A3: asociación entre la entrada de extranjeros y la variación anual del alquiler SERPAVI municipal, estimación IV", f["beta"], f["ic_lo"], f["ic_hi"],
                             "% por punto de población (IC95 Webb-AR)", "2014-2022", "%d municipios; N = %d" % (res[sid]["n_municipios"], f["n"]), FUENTES, clas[sid]["clase"],
                             f"Referencia 0,947 % por punto (Sanchis-Guarner). Clase provisional, pendiente de I8. {clas[sid]['i6']['texto']}"))
    K.volcar_json(SAL / "hechos.json", H)
    # ---- informe.md
    L = []
    L.append("# V18 · E3 Inmigración: réplica y ampliaciones de González y Ortega (2013)")
    L.append(f"\n*{ROT}.* Generado por `python3 src/v18/estimacion/e3_inmigracion.py` (SEED 20261010, sin red; B = {B} réplicas de Webb). Clasificaciones **provisionales: pendientes de I8** (réplica ciega, B6). "
             "Toda cifra es C4 (nivel_evidencia EXPLORATORIO). Sin lenguaje causal: se habla de asociación condicionada al diseño.\n")
    L.append("## 1. Resumen")
    prin = [i for i, s in todas.items() if s["rol"] == "principal"]
    n_est = sum(1 for i in prin if i in res)
    L.append(f"- De las {len(prin)} especificaciones principales ({', '.join(i[3:] for i in prin)}), la comprobación previa de variación (MDE al 80 %, adenda 1.3) deja **estimables {n_est}** "
             f"({', '.join(i[3:] for i in prin if i in res) or 'ninguna'}) y **NO ESTIMABLES {len(prin) - n_est}** (por variación: {', '.join(i[3:] for i in prin if i in ne and 'variación' in ne[i])}; por datos: {', '.join(i[3:] for i in prin if i in ne and 'variación' not in ne[i])}). "
             "Además se estiman las coprincipales P (V9-D4, V16-Q3c1 y V16-H4) en la muestra V18.")
    if tit:
        c = clas[tit]
        L.append(f"- **{tit}** (ventana {todas[tit]['cfg']['ventana'][0]}-{todas[tit]['cfg']['ventana'][1]}; sin 2003): {g4(ft['beta'])} {REF['R1']['unidad']}; IC95 Webb-AR [{g4(ft['ic_lo'])}; {g4(ft['ic_hi'])}]; "
                 f"AR exacto [{g4(ft['ar_lo'])}; {g4(ft['ar_hi'])}]; F efectivo {g4(ft['F_eff'])}; p (Webb-AR) {g4(ft['p_webb_ar'])}, p (AR) {g4(ft['p_ar'])}, p tras Holm {g4(ph[tit])}. "
                 f"Clase: **{c['clase']}**. {c['i6']['texto']}.")
    L.append("- Lectura: " + ("la estimación no es distinguible de cero ni de la referencia; el diseño no decide." if tit and ph[tit] >= 0.10 else "ver tabla."))
    L.append(f"- B5: E3-R2 (la estimación propia de E3) y su respaldo E3-A1 son NO ESTIMABLES por variación; E3 no aporta magnitud propia a la magnitud preferida (adenda 1.9).\n")
    L.append("## 2. Diseño y traslado")
    L.append("- **Original.** González y Ortega (2013, J. Regional Science) y su versión IZA de 2009: 50 provincias, primeras diferencias ponderadas, efectos región-año, instrumento de redes étnicas con el Censo de 1991; "
             "IZA: 44,72 €/m² por punto de población (EE 18,58); Chicago Fed 2011: elasticidad 0,959 (0,984) solo con redes, 2001-2010.")
    L.append("- **Aquí.** 39 provincias no selladas; x = 100·ΔF/P (F: extranjeros del padrón a 1 de enero; entre t y t+1 entran los del año t); z = 100·Σ_c s_pc·M_ct/P(t), con s_pc la distribución del grupo c entre provincias en el "
             "Censo de 2001 y M_ct las entradas nacionales del grupo (Eurostat/INE). Controles: región-año (5 NUTS 1 sin sellar), cuota de empleo en construcción de 2001 × año y costa × año (17 provincias). "
             "Pesos: población de 1 de enero de 1998 (R1) o 2000 (R2).")
    L.append("- **Desviaciones** (docs/v18/desviaciones_e3_e5_e9.md): Censo de 2001 vía Eurostat porque el INE no lo sirve (D-E359-1); 8 grupos de origen en lugar de 16 (D-E359-3); 2003 sin detalle por nacionalidad fuera de la principal "
             "(D-E359-4); balance a nivel de choque (D-E359-16); etiqueta NO CONCLUYENTE para las estimaciones no significativas con pruebas débiles (D-E359-17).\n")
    L.append("## 3. Comprobación previa de variación (adenda 1.3)\n")
    mt = []
    for sid, m in mde_tab.items():
        mt.append({"id": sid, "n": m["n"], "G": m["G"], "F efectivo": m["F_eff"], "σ preperiodo": m["sigma"], "ρ": m["rho"], "MDE80": m["mde80"], "|referencia|": m["ref"],
                   "estimable": "sí" if m["estimable"] else "NO", "1/HHI origen": m["inv_hhi_origen"]["por_origen"]})
    L.append(tabla_md(pd.DataFrame(mt), ["id", "n", "G", "F efectivo", "σ preperiodo", "ρ", "MDE80", "|referencia|", "estimable", "1/HHI origen"]))
    L.append("\nMDE por Monte Carlo (R = %d, SEED 20261010) con el contraste de Anderson-Rubin agrupado por provincia y la variación real del regresor y del instrumento; σ y ρ del preperiodo (1996-2001 en R; 2009-2013 en A1 y A5; "
             "2012-2013 en A2 y A3), declaradas como «no vistas» en V15/V16 para estas unidades. Se calculó **antes** de estimar (incidencia D-E359-15: una lectura de desarrollo de R1 antes del MDE, sin efecto en ninguna decisión).\n" % E3.R_MDE)
    L.append("## 4. Resultados\n")
    ft_rows = tabla[tabla["estado"] == "estimada"].copy()
    cols = ["id", "rol", "ventana", "n", "G", "beta", "se", "ic95_webb_ar_lo", "ic95_webb_ar_hi", "F_eff", "p_webb_ar", "p_ar", "p_holm", "q_BY", "clase"]
    L.append(tabla_md(ft_rows, [c for c in cols if c in ft_rows.columns], {"n": lambda v: str(int(v)), "G": lambda v: str(int(v))}))
    L.append(f"\nUnidades: R1 en €/m² por punto de población; A1, A3 y A5 en % por punto; R2 en elasticidad (ln valor tasado frente a ln población de 15 a 64). IC95 Webb-AR: inversión del contraste de "
             f"Anderson-Rubin con bootstrap de Webb (nulo impuesto, {B} réplicas); si no está acotado se dice. «p_holm»: Holm dentro de la familia E3 (principales y coprincipales estimables; m = {len(ph)}). «q_BY»: "
             "Benjamini-Yekutieli entre las variantes de su principal.\n")
    L.append("### NO ESTIMABLES\n")
    for sid in ne:
        L.append(f"- **{sid}**: {ne[sid]}.")
    L.append(f"\nQué datos las harían estimables: {DATOS_QUE_FALTAN}.\n")
    # B4
    L.append("## 5. Pruebas B4 de las principales estimables\n")
    for sid, d in diag.items():
        L.append(f"### {sid}")
        pr = d["pretendencia"]
        L.append(f"- Pretendencia del instrumento (corte transversal, efectos de macrorregión): pendiente {g4(pr['pendiente'])} (EE {g4(pr['se'])}), p Webb {g4(pr['p_webb'])}; pendiente detectable al 80 %: {g4(pr['pendiente_detectable80'])}; "
                 f"sesgo implicado en β: {g4(pr['sesgo_detectable_beta'])} frente a ½|referencia| = {g4(0.5 * REF[todas[sid]['ref']]['v'])} → potencia {'suficiente' if pr['roth_ok'] else 'insuficiente (prueba débil)'}.")
        pf = d.get("placebo_fecha")
        if pf:
            L.append(f"- Placebo de fecha (instrumento de t+6 en el preperiodo): coef. {g4(pf['coef'])}, p Webb {g4(pf['p_webb'])} (N = {pf['n']}).")
        po = d.get("placebo_resultado")
        L.append("- Placebo de resultado (población de 65 años o más, total): " + (f"coef. {g4(po['coef'])}, p Webb-AR {g4(po['p_webb_ar'])}, p AR exacto {g4(po['p_ar_exacto'])}." if po else "sin dato municipal en el repositorio."))
        bl = d["balance"]
        L.append("- Balance a nivel de choque (BHJ; 8 choques; Holm entre características): " + "; ".join(f"{k}: pendiente {g4(v['pendiente'])}, p {g4(v['p'])}" for k, v in bl["por_caracteristica"].items()) +
                 f". p de Holm mínimo {g4(bl['p_holm_min'])}.")
        if "balance_provincial_info" in d:
            bp = d["balance_provincial_info"]
            L.append(f"- Información: el balance del instrumento medio frente a las características de 2001 a nivel de provincia da p = {bp['p']:.2g} (esperable: el instrumento es proporcional a la exposición de 2001); no entra en la clasificación (D-E359-16).")
        ro = d["rotemberg"]
        L.append("- Pesos de Rotemberg: " + ", ".join(f"{k} {v:.2f}" for k, v in ro["alpha"].items()) if "alpha" in ro else "- Pesos de Rotemberg (mayores): " + ", ".join(f"{k} {v:.2f}" for k, v in ro["alpha_top"].items()))
        L.append(f"  Sin los orígenes de más peso ({', '.join(ro['excluidos'])}): β = {g4(ro['beta_sin_top'])} (F efectivo {g4(ro['F_eff'])}); mismo signo: {ro['mismo_signo']}; dentro del IC95 principal: {ro['dentro_ic']}.")
        j = d.get("jrs", {})
        if "beta" in j:
            L.append(f"- Jaeger-Ruist-Stuhler (instrumento de t-4 como control): β = {g4(j['beta'])} (EE {g4(j['se'])}); dentro del IC95 principal: {j['dentro_ic']}.")
        sa = d.get("sin_atipicos")
        if sa:
            L.append(f"- Sin atípicos: β = {g4(sa['beta'])} (EE {g4(sa['se'])}); mismo signo: {sa['mismo_signo']}.")
        cs = d.get("con_suma_exposicion")
        if cs:
            L.append(f"- Información (no preinscrita): con el control de la suma de cuotas × año, β = {g4(cs['beta'])} (EE {g4(cs['se'])}), F efectivo {g4(cs['F_eff'])}.")
        bh = d.get("bhj_alternativa")
        if bh and "beta" in bh:
            L.append(f"- BHJ a nivel de choque (alternativa, **{bh['etiqueta']}**): β = {g4(bh['beta'])} (EE {g4(bh['se'])}; {bh['n_choques']} choques, {bh['G']} orígenes).")
        if "particion" in d:
            L.append("- Partición de A5: " + "; ".join(f"{k}: β = {g4(v['beta'])} (EE {g4(v['se'])}, F {g4(v['F_eff'])}, p Webb-AR {g4(v['p_webb_ar'])})" for k, v in d["particion"].items()) + ".")
        L.append("")
    L.append("## 6. Clasificación (I1-I8 revisados; adenda 1.1 y 1.2)\n")
    for sid, c in clas.items():
        if c["clase"] in ("NO ESTIMABLE", "no se clasifica"):
            continue
        L.append(f"- **{sid}: {c['clase']}** (provisional, pendiente de I8). Razones y pruebas débiles: {'; '.join(c['razones']) if c['razones'] else 'ninguna'}. TOST con δ = {c['tost']['delta']}: "
                 f"{'equivalencia demostrada' if c['tost']['equivalente'] else 'sin equivalencia'}. {c['i6']['texto']}.")
    L.append("\nLa adenda reserva SUGESTIVO a diseños creíbles con alguna prueba débil; una estimación sin significación (p de Holm ≥ 0,10) y sin equivalencia no tiene un efecto que sugerir, por lo que se rotula NO CONCLUYENTE (sin potencia) "
             "con las pruebas débiles listadas (D-E359-17). Tope de la tabla consolidada para E3-R1: SUGESTIVO (año base 2001 tras el F de 3,4-4,6 de V9-D4, adenda 1.6).\n")
    L.append("## 7. Coprincipales P (adenda 1.6; no se clasifican)\n")
    v = pd4["valor tasado"]
    L.append(f"- **E3-P-D4** (V9-D4, 2003-2012, valor tasado, muestra V18): β = {g4(v['beta'])} (EE {g4(v['se'])}); IC95 Webb-AR [{g4(v['ic_webb_ar']['lo'])}; {g4(v['ic_webb_ar']['hi'])}]; F efectivo {g4(v['F_eff'])}; "
             f"p Webb-AR {g4(v['p_webb_ar'])}, p AR {g4(v['p_ar'])}; n = {v['n']}. Publicado en V9: −0,0029 (valor tasado) y 0,0072 (IPC de alquiler), F de 3,4 a 4,6. IPC de alquiler aquí: β = {g4(pd4['IPC de alquiler']['beta'])}.")
    L.append(f"- **E3-P-Q3c1** (V16, TWFE, ln valor tasado 2011-2022): β = {g4(pq3['beta'])} (EE {g4(pq3['se'])}); IC95 Webb [{g4(pq3['ic_webb'][0])}; {g4(pq3['ic_webb'][1])}]; p Webb {g4(pq3['p_webb'])}; {pq3['G']} provincias × {pq3['T']} años. Publicado en V16: 0,0119 (solo puntual).")
    if "E3-P-H4" in res:
        f = ficha(res["E3-P-H4"])
        L.append(f"- **E3-P-H4** (V16 réplica ciega H4, municipal SERPAVI): β = {g4(f['beta'])} % por punto (EE {g4(f['se'])}); IC95 Webb-AR [{g4(f['ic_lo'])}; {g4(f['ic_hi'])}]; F efectivo {g4(f['F_eff'])}; N = {f['n']} (réplica de V16: 2SLS 0,309 con N = 13.395; H4 publicado: 0,29 con N = 13.442; la muestra V18 excluye además los municipios de V16).")
    L.append("")
    L.append("## 8. Familia de Holm y multiverso\n")
    L.append(f"- Familia E3: m = {len(ph)} contrastes (principales estimables y coprincipales P tras las comprobaciones previas); p ajustados: " + ", ".join(f"{k} {v:.3f}" for k, v in ph.items()) + ".")
    L.append(f"- Variantes enumeradas estimadas: {sum(len(v) for v in var_por_padre.values())}; las de datos ausentes quedan «no estimable» sin sustituir (D-E359-11). R1-v11 (2003 interpolado) es holgura nº 1: no cuenta en I5 ni en B5.\n")
    L.append("## 9. Limitaciones\n")
    L.append("- Ocho grupos de origen en lugar de 16: el número efectivo de choques es bajo y el instrumento es menos fino que el original.\n- La σ del preperiodo es la del residuo con los mismos efectos; el Webb-AR de la estimación no tiene Monte Carlo propio (sus piezas, Webb en TWFE y AR de una endógena, son APTAS).\n"
             "- El F efectivo alto de R1 no garantiza potencia (el Monte Carlo deja NO APTA la regla F ≥ 10).\n- Sin las 11 provincias selladas de v6 (entre ellas Madrid, Baleares y Canarias) el panel no cubre las de más inmigración reciente.\n- I8 (réplica ciega) y la ronda del abogado del diablo (B6) están pendientes.\n")
    (SAL / "informe.md").write_text("\n".join(L) + "\n", encoding="utf-8")
    print("informe escrito", flush=True)
