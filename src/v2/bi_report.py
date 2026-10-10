"""BI · resultado.json y resumen.md a partir de los resultados (determinista, sin marcas de tiempo)."""
from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import v2_common as vc  # noqa: E402


def f(x, n=2):
    return f"{x:.{n}f}"


def escribir(h3, het, oos, OUT):
    T = {r["resultado"]: r for r in h3["tabla_principal"]}
    a, p, dif = T["alq"], T["pre"], T["dif"]
    cc, dg, cr = h3["contraste_conjunto"], h3["diagnosticos"], h3["criterios_identificacion"]
    comp = cr["componentes"]
    cA, cB = list(comp.values())
    an = {r["modelo"]: r for r in oos["anual"]}
    m1 = an["AR4+flujo_t (observado)"]
    m2 = [v for k, v in an.items() if k.startswith("AR4+flujo_t+1")][0]
    rob = pd.DataFrame(h3["robustez"])
    idf = pd.DataFrame(h3["identificacion"])
    dml = {f"{d['modelo']}_{d['learner']}": d for d in het["dml"]}
    cf = het["causal_forest"]
    DESV = ("Elecciones NO fijadas en el pre-registro (desviación/interpretación declarada): (i) 'flujo/población t-1' se lee como flujo del año t (INE EM) "
            "dividido por la población a 1 de enero del año t−1; la lectura alternativa flujo_{t-1}/pob_{t-2} se muestra aparte; "
            "(ii) momento del shock: el principal usa ΔS_t = S(1-ene t) − S(1-ene t-1), que cubre el año t-1 (desalineado con el flujo del año t); "
            "la versión alineada ΔS_{t+1} se muestra aparte y cambia el signo del contraste; (iii) el valor tasado se deflacta con el deflactor nacional "
            "(inocuo con FE de año); (iv) Europa = UE+resto de Europa (ruptura UE28/UE27 de 2021); cuotas y shock sobre las 49 provincias de entrenamiento.")
    pid = lambda n, k: idf[(idf.spec == n) & (idf.res == k)].iloc[0]

    vc.resultado_json(
        OUT / "resultado.json", rama="BI",
        pregunta="H3 (confirmatoria): ¿se asocia la inmigración (flujo/población, instrumentada con shift-share por agrupación de países, cuotas 2002) más con el alquiler que con el precio de compra (β_alq>0 y β_alq>β_compra)?",
        datos="panel_prov_a (v2_common.load), 49 provincias de entrenamiento, 2009-2021; flujos INE EM; stock por nacionalidad ECP; IPC alquiler (media anual); valor tasado real.",
        N=int(h3["N"]),
        metodo="2SLS, FE provincia y año, EE cluster provincia (49), wild cluster bootstrap restringido (WRE, Webb, B=9999); shift-share con cuotas 2002 fijas y shock nacional leave-one-out; contraste conjunto por unión-intersección (p_IUT). Diagnósticos GPSS/placebo/subperiodos EXPLORATORIOS.",
        estimacion={"coef_alquiler": a["b_2sls"], "coef_compra_real": p["b_2sls"], "coef_alq_menos_compra": dif["b_2sls"],
                    "se_cluster": {"alq": a["se"], "compra": p["se"], "dif": dif["se"]},
                    "p_wcb_una_cola": {"alq": a["p_wcb_1c"], "dif": dif["p_wcb_1c"]},
                    "p_wcb_dos_colas": {"alq": a["p_wcb_2c"], "compra": p["p_wcb_2c"], "dif": dif["p_wcb_2c"]},
                    "contraste_con_instrumento_alineado": {"b": float(pid("z_alineado_t+1", "dif")["b"]), "p_wcb_1c": float(pid("z_alineado_t+1", "dif")["p_wcb_1c"])},
                    "magnitud": "NO identificada (rango razonable 0,8-5 entre variantes)",
                    "unidades": "puntos % de variación anual por cada 1 p.p. de población"},
        ic95={"alq": [a["ic95_lo"], a["ic95_hi"]], "compra": [p["ic95_lo"], p["ic95_hi"]], "dif": [dif["ic95_lo"], dif["ic95_hi"]],
              "AR_alq": [a["ar_lo"], a["ar_hi"]]},
        p_ajustado={"p_IUT_H3_sin_ajustar_wcb": cc["p_IUT_wcb"], "cota_Holm7_H3": cc["cota_bonferroni_familia7"],
                    "nota": "la unidad de la familia de 7 es H3 (p_IUT); el ajuste final lo aplica el orquestador; las cotas por componente son informativas"},
        nivel_evidencia=h3["nivel_evidencia"],
        diagnosticos={"nivel_beta_alq_signo": h3["nivel_beta_alq_signo"], "F_cluster": dg["F_cluster"], "criterios": cr, "identificacion_exploratoria": h3["identificacion"],
                      "balance_cuotas_Sudamerica": h3["balance_cuotas_Sudamerica"], "pretendencias_Sudamerica": h3["pretendencias_Sudamerica"],
                      "rotemberg_alq": dg["rotemberg_alq"], "pretendencias_NO_informativas": dg["pretendencias"], "overid": dg["overid"], "BHJ": dg["BHJ"], "AKM0": dg["AKM0"],
                      "corr_zmedio_caract02": dg["corr_zmedio_caract02"], "sistema": h3["sistema"], "robustez_timing": h3["robustez"],
                      "heterogeneidad_EXPLORATORIO": {"dml": het["dml"], "causal_forest": {k: cf[k] for k in ("ate", "ate_ic95", "importancias")},
                                                      "interacciones_iv": het["interacciones_iv"]}},
        fuera_muestra={"modelo": "AR4 panel anual + flujo de inmigración observado en t (orígenes 2013-2020, bloques con embargo)",
                       "rmse": m1["rmse"], "rmse_AR4": m1["rmse_AR4"], "dm_vs_ar4": m1["dm_vs_AR4"], "p_dm_hln": m1["p_vs_AR4"],
                       "contemporaneo_no_pronostico": {"rmse": m2["rmse"], "dm_vs_ar4": m2["dm_vs_AR4"], "p": m2["p_vs_AR4"]},
                       "ecm_v1": oos["ecm_v1"], "nota": oos["nota"]},
        notas=DESV + " H3 sin muestra sellada. Heterogeneidad (DML, causal forest) EXPLORATORIA. CAUSAL descartado.")

    L = []
    w = L.append
    w("# BI · inmigración y vivienda (H3) · resumen\n")
    w(f"Muestra: {h3['N']} observaciones provincia-año (49 provincias, 2009-2021), idéntica para alquiler, compra y contraste. SEED 20261010. Todas las especificaciones en `registro.csv` (humo 2009-2015 en `smoke_*`).\n")
    w("**Lectura general: H3 queda EXPLORATORIO. Hay una asociación positiva y estable en el signo entre el instrumento de inmigración y el alquiler, de magnitud no identificada; el contraste alquiler>compra no es robusto.**\n")
    w("## Desviaciones/interpretaciones no fijadas en el pre-registro\n")
    w(DESV + " Si la versión desalineada se eligió antes o después de ver resultados no es auditable: se declara como grado de libertad.\n")
    w("## H3 (especificación pre-registrada)\n")
    w("| | coef. (2SLS) | EE cluster | IC95 t(48) | p WCB 2 colas | p WCB 1 cola | MCO |")
    w("|---|---|---|---|---|---|---|")
    for k, nm in (("alq", "Δln IPC alquiler"), ("pre", "Δln valor tasado real"), ("dif", "alquiler − compra")):
        r = T[k]
        w(f"| {nm} | {f(r['b_2sls'])} | {f(r['se'])} | [{f(r['ic95_lo'])}; {f(r['ic95_hi'])}] | {f(r['p_wcb_2c'],3)} | {f(r['p_wcb_1c'],3)} | {f(r['b_ols'])} ({f(r['se_ols'])}) |")
    w(f"\nUnidades: % de variación anual por cada 1 p.p. de población. Conjunto AR del coef. de alquiler: [{f(a['ar_lo'],1)}; {f(a['ar_hi'],1)}]. Correlación entre ecuaciones {f(h3['sistema']['corr_ecuaciones'])}; el EE del contraste del sistema apilado ({f(h3['sistema']['se_contraste'],3)}) coincide con el de la regresión de la diferencia.")
    w(f"\nIntersección-unión (p WCB una cola): coef. alquiler>0 p={f(cc['p_wcb_beta_alq_gt0'],4)}; contraste>0 p={f(cc['p_wcb_contraste_gt0'],4)}; **p_IUT de H3 = {f(cc['p_IUT_wcb'],4)}**, cota Holm-7 {f(cc['cota_bonferroni_familia7'],3)} (la corrección final de la familia la aplica el orquestador).")
    w(f"\n**Nivel de evidencia de H3: {h3['nivel_evidencia']}.** Componente alquiler>0 (no pre-registrado por separado, informativo): {h3['nivel_beta_alq_signo']}; cota Holm-7 {f(cA['p_cota_Holm7'],3)}. Compra: no informativa (IC [{f(p['ic95_lo'],1)}; {f(p['ic95_hi'],1)}], signo inestable). **CAUSAL descartado.**\n")
    w("## Diagnósticos de identificación (EXPLORATORIOS, con p WCB una cola; con F<10 el bootstrap no es fiable)\n")
    w("| especificación | resultado | coef. | EE | p cluster | p WCB 1c | F |\n|---|---|---|---|---|---|---|")
    for _, r in idf.iterrows():
        w(f"| {r['spec']} | {r['res']} | {f(r['b'])} | {f(r['se'])} | {f(r['p_cluster'],3)} | {f(r['p_wcb_1c'],3)} | {f(r['F'],1)} |")
    g1, gt, so, al = pid("gpss_extr02", "alq"), pid("gpss_todas", "alq"), pid("solo_Sudamerica", "dif"), pid("z_alineado_t+1", "dif")
    pl1, pl2 = pid("placebo_resultado_t-1", "alq"), pid("placebo_resultado_t-2", "alq")
    w(f"""
Lectura:
- **Controles GPSS (características 2002 × año).** Al controlar por la cuota de extranjeros 2002 el coeficiente de alquiler baja a {f(g1['b'])} (p cluster {f(g1['p_cluster'],3)}) y el contraste cambia de signo ({f(pid('gpss_extr02','dif')['b'])}); con las cinco características el F cae a {f(gt['F'],1)} y el coeficiente es {f(gt['b'])} (p {f(gt['p_cluster'],2)}). Las cuotas 2002 no están balanceadas: la cuota de Sudamérica correlaciona con ln población 2002 (r={f(h3['balance_cuotas_Sudamerica']['ln_pob02']['corr'])}), ln precio 2002 (r={f(h3['balance_cuotas_Sudamerica']['ln_p02']['corr'])}) y extranjeros 2002 (r={f(h3['balance_cuotas_Sudamerica']['extr02']['corr'])}).
- **Placebo de alquiler pasado sobre x_t instrumentado**: coef. {f(pl1['b'])} (t−1, p {f(pl1['p_cluster'],3)}) y {f(pl2['b'])} (t−2, p {f(pl2['p_cluster'],3)}), del mismo tamaño que el principal: **el placebo rechaza**. El diseño no separa el flujo de t de dinámicas provinciales previas o de flujos pasados (shocks persistentes); el coeficiente no puede leerse como efecto del flujo del año t.
- **Solo Sudamérica** (68 % del peso de Rotemberg; F {f(so['F'],0)}): alquiler {f(pid('solo_Sudamerica','alq')['b'])}, compra {f(pid('solo_Sudamerica','pre')['b'])} (positivo y significativo) y contraste {f(so['b'])}. **Sin Sudamérica** el instrumento es débil (F {f(pid('sin_Sudamerica','alq')['F'],1)}).
- **Contraste con instrumento alineado ΔS_{{t+1}}** (F {f(al['F'],0)}): {f(al['b'])} (p WCB 1c {f(al['p_wcb_1c'],2)}): **el signo del contraste se invierte**; con 'flujo t−1' el contraste es {f(pid('flujo_t-1','dif')['b'])}. El contraste depende de elecciones de timing y de instrumento.
- **Subperiodos**: 2009-2014 el instrumento no tiene primera etapa (F {f(pid('sub_2009-2014','alq')['F'],1)}, sin información); 2015-2021 coef. alquiler {f(pid('sub_2015-2021','alq')['b'])} (p cluster {f(pid('sub_2015-2021','alq')['p_cluster'],3)}).
""")
    w("## Diagnósticos de shift-share previos\n")
    w(f"- Primera etapa: F cluster = {f(dg['F_cluster'],1)} (moderado; F efectivo de Montiel Olea-Pflueger no implementado: con un instrumento y un regresor se reporta el F robusto, sin valores críticos). Con tendencias provinciales baja a {f(rob[(rob.spec=='tendencias_prov')].F.iloc[0],1)}.")
    ro = dg["rotemberg_alq"]
    w(f"- Pesos de Rotemberg (8 grupos): sin pesos negativos; Sudamérica {f(ro['top'][0]['alpha'],2)} (F del grupo {f(ro['top'][0]['F_g'],0)}); los dos mayores suman {f(ro['suma_top2'],2)}. África y Europa: F por grupo < 2.")
    zc = dg["corr_zmedio_caract02"]
    w(f"- Instrumento medio vs. características 2002: extranjeros r={f(zc['extr02']['corr'])} (p={f(zc['extr02']['p'],3)}), paro r={f(zc['paro02']['corr'])} (p={f(zc['paro02']['p'],3)}), ln población r={f(zc['ln_pob02']['corr'])} (p={f(zc['ln_pob02']['p'],3)}).")
    pt = dg["pretendencias"]
    w(f"- **Pretendencias: NO informativas.** La ventana 2003-2007 (resultados sobre el instrumento medio posterior: alquiler p={f(pt['alq']['p'],2)}, precio p={f(pt['pre']['p'],2)}) coincide con el boom de llegadas a los mismos enclaves: no es un periodo pre-tratamiento. Con el instrumento de Sudamérica: alquiler p={f(h3['pretendencias_Sudamerica']['alq']['p'],2)}.")
    ov = dg["overid"]
    w(f"- Sobreidentificación (5 grupos): Hansen cluster alquiler p={f(ov['alq']['p_hansen'],2)}, precio p={f(ov['pre']['p_hansen'],2)}; Sargan homocedástico alquiler p={f(ov['alq']['p_sargan'],3)}, precio p={ov['pre']['p_sargan']:.1e} (rechaza). El J robusto con 49 clusters tiene poca potencia.")
    bh, ak = dg["BHJ"], dg["AKM0"]
    w(f"- BHJ a nivel de shock (8 grupos × 13 años, t(7)): alquiler {f(bh['alq_anioFE']['b'])} (p={f(bh['alq_anioFE']['p'],3)}); precio {f(bh['pre_anioFE']['b'])} (p={f(bh['pre_anioFE']['p'],2)}). Con 8 shocks la potencia y la inferencia son pobres: no aporta evidencia de exogeneidad de los shocks.")
    w(f"- EE tipo AKM0 (aproximación, sin región de similitud de cuotas): alquiler EE {f(ak['alq']['se'])} (p t(7) = {f(ak['alq']['p_t'],3)}) frente a {f(a['se'])}.")
    w("- **Naturaleza del shock**: ΔS es la variación del stock de nacionales del grupo (incluye nacionalizaciones, p. ej. sudamericanos en 2010-2015), mientras que x es el flujo bruto de entradas: el shock no mide entradas.\n")
    w("## Stock vs flujo y timing (EXPLORATORIO)\n")
    w("| spec | resultado | regresor | coef. | EE | p cluster | F |\n|---|---|---|---|---|---|---|")
    for _, r in rob.iterrows():
        w(f"| {r['spec']} | {r['resultado']} | {r['regresor']} | {f(r['b'])} | {f(r['se'])} | {f(r['p_cluster'],3)} | {f(r['F'],1)} |")
    w("\nEl coeficiente de alquiler es positivo en las variantes con el instrumento completo; con flujo t−1 y con x_t y x_{t−1} conjuntos pierde precisión. El coeficiente de compra cambia de signo entre variantes.\n")
    w("## Heterogeneidad (EXPLORATORIO)\n")
    w(f"- DML (cross-fitting 5 bloques de provincias × 3 repeticiones, EE cluster): PLR lasso {f(dml['PLR_lasso']['theta'])} (p={f(dml['PLR_lasso']['p'],3)}), PLR RF {f(dml['PLR_rf']['theta'])} (p={f(dml['PLR_rf']['p'],4)}); PLIV lasso {f(dml['PLIV_lasso']['theta'])} (p={f(dml['PLIV_lasso']['p'],2)}), PLIV RF {f(dml['PLIV_rf']['theta'])} (p={f(dml['PLIV_rf']['p'],3)}). PLR sin FE de provincia.")
    w(f"- Causal forest (sin instrumento): coeficiente medio {f(cf['ate'])} [{f(cf['ate_ic95'][0])}; {f(cf['ate_ic95'][1])}]; los coeficientes estimados son mayores con cuota extranjera 2002 y precio inicial altos y paro 2002 bajo (importancia mayor: cuota extranjera 2002 {f(cf['importancias']['extr02'],2)}). La IC del bosque no agrupa por provincia y subestima la incertidumbre.")
    ii = {i["caracteristica"]: i for i in het["interacciones_iv"]}
    w(f"- Interacciones IV paramétricas: ninguna significativa (p mínimo {f(min(i['p_inter'] for i in ii.values()),2)}, Holm 1,00): el patrón del bosque no se confirma con instrumento.")
    w("- Presupuesto declarado 14 configuraciones, 10 usadas; hiperparámetros fijos.\n")
    w("## Magnitudes\n")
    w(f"- Coeficiente de alquiler {f(a['b_2sls'])} [{f(a['ic95_lo'],1)}; {f(a['ic95_hi'],1)}] vs MCO {f(a['b_ols'])}, Saiz (2007, EE. UU.) ≈ 1 (aumento neto de población inmigrante, no flujo bruto) y v1 (F3, 17 CCAA) 0,44 (n.s.). Es unas 3 veces el MCO y Saiz y 7 veces v1, con F moderado y cuotas no balanceadas; la diferencia no está explicada. Entre variantes el coeficiente va de 0,8 a 5: **la magnitud no está identificada**; solo el signo positivo es estable.\n")
    w("## Fuera de muestra\n")
    w(f"Anual, orígenes 2013-2020 (8 × 49 provincias, bloques expansivos con embargo 1 año, misma muestra). RMSE AR(4) panel {f(m1['rmse_AR4'],4)}; AR(4)+flujo observado en t {f(m1['rmse'],4)} (DM-HLN {f(m1['dm_vs_AR4'])}, p={f(m1['p_vs_AR4'],2)}: sin mejora significativa); con flujo contemporáneo t+1 (NO es pronóstico) {f(m2['rmse'],4)} (p={f(m2['p_vs_AR4'],2)}). El flujo del año t se publica a mitad de t+1: es un pseudo-pronóstico con pequeña anticipación. **ECM v1: no comparable** (solo existe trimestral, sin análogo anual en la misma muestra); se retira la comparación. No es posible añadir la inmigración al panel_ar4 trimestral (flujos hasta 2021-22).\n")
    w("## Lo que NO se puede afirmar\n")
    for t in (
        "Que la inmigración se asocie más con el alquiler que con la compra: p_IUT 0,029, cota Holm-7 0,21, IC95 del contraste incluye 0 y el signo se invierte con el instrumento alineado, con Sudamérica sola y con los controles GPSS.",
        "Que exista un efecto causal o un efecto local (LATE) del flujo: el placebo de alquiler pasado rechaza, las cuotas 2002 no están balanceadas, el F cae a 4,6 con controles GPSS y la ventana de pretendencias no es pre-tratamiento.",
        "Ninguna magnitud concreta (rango 0,8-5); ni comparación cuantitativa con Saiz (2007): unidades y definición (flujo bruto vs neto) distintas.",
        "Nada sobre el precio de compra (IC muy ancho, signo inestable).",
        "Nada sobre 2022 en adelante ni sobre las provincias selladas (H3 sin evaluación sellada).",
        "Heterogeneidad por costa, turismo, tamaño o precio inicial: solo aparece en métodos sin instrumento.",
        "Equilibrio general (salida de nativos, oferta) ni cantidades.",
        "Mejora predictiva con inmigración fuera de muestra (sin mejora significativa frente a AR(4))."):
        w(f"- {t}")
    (OUT / "resumen.md").write_text("\n".join(L) + "\n")
