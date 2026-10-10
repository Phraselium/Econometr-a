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
    cc, dg, cr = h3["contraste_conjunto"], h3["diagnosticos"], h3["criterios_causal"]
    comp = cr["componentes"]
    an = {r["modelo"]: r for r in oos["anual"]}
    m1 = an["AR4+flujo_t (observado)"]
    m2 = [v for k, v in an.items() if k.startswith("AR4+flujo_t+1")][0]
    ecm = oos["ecm_v1_trimestral_Q4"]
    rob = pd.DataFrame(h3["robustez"])
    dml = {f"{d['modelo']}_{d['learner']}": d for d in het["dml"]}
    cf = het["causal_forest"]

    vc.resultado_json(
        OUT / "resultado.json", rama="BI",
        pregunta="H3 (confirmatoria): la inmigración (flujo/población t-1, instrumentada con shift-share por agrupación de países, cuotas 2002) eleva más el alquiler que el precio de compra (beta_alq>0 y beta_alq>beta_compra).",
        datos="panel_prov_a (holdout.load_train, vía v2_common.load), 49 provincias de entrenamiento, 2009-2021; flujos INE EM 2009-2021; stock por nacionalidad ECP 2002-2021; IPC alquiler (media anual); valor tasado real.",
        N=int(h3["N"]),
        metodo="2SLS, FE provincia y año, EE cluster provincia (49), wild cluster bootstrap restringido (WRE, Webb, B=9999); instrumento shift-share con cuotas 2002 fijas y shock nacional leave-one-out; contraste conjunto por unión-intersección con covarianza entre ecuaciones.",
        estimacion={"beta_alquiler": a["b_2sls"], "beta_compra_real": p["b_2sls"], "beta_alq_menos_compra": dif["b_2sls"],
                    "se_cluster": {"alq": a["se"], "compra": p["se"], "dif": dif["se"]},
                    "p_wcb_una_cola": {"alq": a["p_wcb_1c"], "dif": dif["p_wcb_1c"]},
                    "p_wcb_dos_colas": {"alq": a["p_wcb_2c"], "compra": p["p_wcb_2c"], "dif": dif["p_wcb_2c"]},
                    "unidades": "puntos % de variación anual por cada 1 p.p. de población (flujo/pob t-1)"},
        ic95={"alq": [a["ic95_lo"], a["ic95_hi"]], "compra": [p["ic95_lo"], p["ic95_hi"]], "dif": [dif["ic95_lo"], dif["ic95_hi"]],
              "AR_alq": [a["ar_lo"], a["ar_hi"]]},
        p_ajustado={"IUT_wcb": cc["p_IUT_wcb"], "holm_2_componentes": cc["holm_2_componentes"],
                    "cota_Holm_familia7_beta_alq": comp["beta_alq_gt0"]["p_holm7_cota"],
                    "cota_Holm_familia7_contraste": comp["contraste_alq_menos_compra_gt0"]["p_holm7_cota"]},
        nivel_evidencia=h3["nivel_evidencia"],
        diagnosticos={"F_cluster": dg["F_cluster"], "criterios": cr, "rotemberg_alq": dg["rotemberg_alq"], "pretendencias": dg["pretendencias"],
                      "overid": dg["overid"], "BHJ": dg["BHJ"], "AKM0": dg["AKM0"], "corr_zmedio_caract02": dg["corr_zmedio_caract02"],
                      "sistema": h3["sistema"], "robustez_timing": h3["robustez"],
                      "heterogeneidad_EXPLORATORIO": {"dml": het["dml"], "causal_forest": {k: cf[k] for k in ("ate", "ate_ic95", "importancias")},
                                                      "interacciones_iv": het["interacciones_iv"]}},
        fuera_muestra={"modelo": "AR4 panel anual + flujo de inmigración observado en t (orígenes 2013-2020, bloques con embargo)",
                       "rmse": m1["rmse"], "rmse_AR4": m1["rmse_AR4"], "dm_vs_ar4": m1["dm_vs_AR4"], "p_dm_hln": m1["p_vs_AR4"],
                       "contemporaneo_no_pronostico": {"rmse": m2["rmse"], "dm_vs_ar4": m2["dm_vs_AR4"], "p": m2["p_vs_AR4"]},
                       "ecm_v1_trimestral_Q4": ecm, "nota": oos["nota"]},
        notas="Hipótesis H3: sin muestra sellada (flujos terminan en 2022). Grupo Europa = UE+resto de Europa (suma coherente en el tiempo, por la ruptura UE28/UE27 de 2021); cuotas sobre las 49 provincias de entrenamiento; 8 grupos de origen. Heterogeneidad (DML, causal forest) EXPLORATORIA.")

    L = []
    w = L.append
    w("# BI · inmigración y vivienda (H3) · resumen\n")
    w(f"Muestra: {h3['N']} observaciones provincia-año (49 provincias, 2009-2021), idéntica para alquiler, compra y contraste. SEED 20261010. Todas las especificaciones están en `registro.csv` (la ejecución de humo 2009-2015 en `smoke_*`).\n")
    w("## H3 (confirmatoria, especificación pre-registrada)\n")
    w("| | beta (2SLS) | EE cluster | IC95 t(48) | p WCB 2 colas | p WCB 1 cola | MCO |")
    w("|---|---|---|---|---|---|---|")
    for k, nm in (("alq", "Δln IPC alquiler"), ("pre", "Δln valor tasado real"), ("dif", "alquiler − compra")):
        r = T[k]
        w(f"| {nm} | {f(r['b_2sls'])} | {f(r['se'])} | [{f(r['ic95_lo'])}; {f(r['ic95_hi'])}] | {f(r['p_wcb_2c'],3)} | {f(r['p_wcb_1c'],3)} | {f(r['b_ols'])} ({f(r['se_ols'])}) |")
    w(f"\nUnidades: % de variación anual por cada 1 p.p. de población (flujo/pob t-1). Conjunto de AR de beta_alq: [{f(a['ar_lo'],1)}; {f(a['ar_hi'],1)}]. Correlación entre ecuaciones (cluster) {f(h3['sistema']['corr_ecuaciones'])}; el SE del contraste del sistema apilado ({f(h3['sistema']['se_contraste'],3)}) coincide con el de la regresión de la diferencia.")
    w(f"\nContraste conjunto (unión-intersección, p WCB una cola): beta_alq>0 p={f(cc['p_wcb_beta_alq_gt0'],4)}; beta_alq−beta_compra>0 p={f(cc['p_wcb_contraste_gt0'],4)}; p_IUT={f(cc['p_IUT_wcb'],4)}. Holm sobre 7 confirmatorias: el p ajustado nunca es menor que (8−rango)·p; cota pesimista Bonferroni-7: beta_alq {f(comp['beta_alq_gt0']['p_holm7_cota'],3)} (sobrevive), contraste {f(comp['contraste_alq_menos_compra_gt0']['p_holm7_cota'],3)} (no sobrevive salvo que las otras seis hipótesis rechacen todas). La corrección final de la familia la aplica el orquestador.")
    w(f"\n**Nivel de evidencia de H3 tal como se registró (conjunción): {h3['nivel_evidencia']}.** Por componentes: beta_alq>0 → {comp['beta_alq_gt0']['nivel']} (regla mecánica); contraste alquiler>compra → {comp['contraste_alq_menos_compra_gt0']['nivel']}.\n")
    w("## Diagnósticos de shift-share\n")
    w(f"- Primera etapa: F cluster = {f(dg['F_cluster'],1)} (≥10; con un instrumento y un regresor el F efectivo de Montiel Olea-Pflueger coincide con el F robusto; no se contrasta con valores críticos). Es un F moderado: con tendencias provinciales baja a {f(rob[(rob.spec=='tendencias_prov')].F.iloc[0],1)}.")
    ro = dg["rotemberg_alq"]
    w(f"- Pesos de Rotemberg (8 grupos): sin pesos negativos; Sudamérica pesa {f(ro['top'][0]['alpha'],2)} (F del grupo {f(ro['top'][0]['F_g'],0)}), los dos mayores suman {f(ro['suma_top2'],2)}. La identificación descansa sobre pocas cuotas (sobre todo Sudamérica); África y Europa tienen F por grupo < 2.")
    zc = dg["corr_zmedio_caract02"]
    w(f"- Cuotas 2002 vs. características 2002 (instrumento medio): extranjeros 2002 r={f(zc['extr02']['corr'])} (p={f(zc['extr02']['p'],3)}), paro 2002 r={f(zc['paro02']['corr'])} (p={f(zc['paro02']['p'],3)}), ln población r={f(zc['ln_pob02']['corr'])} (p={f(zc['ln_pob02']['p'],3)}), ln precio r={f(zc['ln_p02']['corr'])} (p={f(zc['ln_p02']['p'],2)}). **Las cuotas no son independientes de las condiciones iniciales** (amenaza a la exogeneidad de cuotas de GPSS 2020).")
    pt = dg["pretendencias"]
    w(f"- Pretendencias (Δ resultados 2003-2007 sobre el instrumento medio posterior, FE año): alquiler p={f(pt['alq']['p'],2)}, precio p={f(pt['pre']['p'],2)} (no significativas; con 5 años y 49 clusters la potencia es limitada).")
    ov = dg["overid"]
    w(f"- Sobreidentificación (5 grupos de origen): J de Hansen cluster alquiler p={f(ov['alq']['p_hansen'],2)}, precio p={f(ov['pre']['p_hansen'],2)} (no rechaza), pero Sargan homocedástico: alquiler p={f(ov['alq']['p_sargan'],3)}, precio p={ov['pre']['p_sargan']:.1e} (rechaza en precio). Con 5 instrumentos y 49 clusters el J robusto tiene poca potencia. beta_alq con 5 instrumentos: {f(ov['alq']['b_2sls_5inst'])} (EE {f(ov['alq']['se'])}).")
    bh, ak = dg["BHJ"], dg["AKM0"]
    w(f"- BHJ a nivel de shock (8 grupos × 13 años, EE cluster por grupo, t(7)): alquiler {f(bh['alq_anioFE']['b'])} (p={f(bh['alq_anioFE']['p'],3)}); precio {f(bh['pre_anioFE']['b'])} (p={f(bh['pre_anioFE']['p'],2)}). **Con 8 grupos la potencia y la inferencia son pobres**; es una comprobación de coherencia, no una prueba.")
    w(f"- EE tipo AKM0 (agrupando por grupo-shock, sin región de similitud de cuotas; aproximación a AKM 2019): alquiler EE {f(ak['alq']['se'])} (p t(7) = {f(ak['alq']['p_t'],3)}) frente a {f(a['se'])} cluster-provincia; precio p={f(ak['pre']['p_t'],2)}. No es AKM completo.\n")
    w("## Stock vs flujo y timing (EXPLORATORIO)\n")
    w("| spec | resultado | regresor | b | EE | p cluster | F |\n|---|---|---|---|---|---|---|")
    for _, r in rob.iterrows():
        w(f"| {r['spec']} | {r['resultado']} | {r['regresor']} | {f(r['b'])} | {f(r['se'])} | {f(r['p_cluster'],3)} | {f(r['F'],1)} |")
    w("\nEl efecto sobre el alquiler es positivo en todas las variantes (stock: +1,2 por p.p. de variación de la cuota extranjera; sin COVID y con instrumento alineado ΔS_{t+1}: 2,4), pero con flujo t−1 solo y con x_t y x_{t−1} conjuntos pierde precisión (F 7-10). El efecto sobre el precio de compra cambia de signo entre variantes: no es estable.\n")
    w("## Heterogeneidad (EXPLORATORIO)\n")
    w(f"- DML (cross-fitting {5} bloques de provincias × 3 repeticiones, EE cluster): PLR lasso {f(dml['PLR_lasso']['theta'])} (p={f(dml['PLR_lasso']['p'],3)}), PLR RF {f(dml['PLR_rf']['theta'])} (p={f(dml['PLR_rf']['p'],4)}); PLIV lasso {f(dml['PLIV_lasso']['theta'])} (p={f(dml['PLIV_lasso']['p'],2)}), PLIV RF {f(dml['PLIV_rf']['theta'])} (p={f(dml['PLIV_rf']['p'],3)}). PLR sin FE de provincia, con características 2002 y dummies de año.")
    w(f"- Causal forest (sin instrumento): efecto medio {f(cf['ate'])} [{f(cf['ate_ic95'][0])}; {f(cf['ate_ic95'][1])}]; mayor efecto estimado donde la cuota extranjera 2002 y el precio inicial son altos y el paro 2002 bajo (importancia mayor: cuota extranjera 2002 {f(cf['importancias']['extr02'],2)}). La IC del bosque no agrupa por provincia y subestima la incertidumbre.")
    ii = {i["caracteristica"]: i for i in het["interacciones_iv"]}
    w(f"- Interacciones IV paramétricas (5 características): ninguna significativa (p mínimo {f(min(i['p_inter'] for i in ii.values()),2)}, Holm 1,00). La heterogeneidad del bosque no se confirma con instrumento.")
    w("- Presupuesto declarado: 14 configuraciones, 10 usadas (4 DML + 1 bosque + 5 interacciones); hiperparámetros fijos, sin búsqueda.\n")
    w("## Comparación de magnitudes\n")
    w(f"- Saiz (2007, EE. UU.): entrada del 1 % de la población ≈ +1 % en alquileres. Aquí: 1 p.p. de población ⇒ +{f(a['b_2sls'])} % de alquiler [IC {f(a['ic95_lo'],1)}; {f(a['ic95_hi'],1)}], unas 3 veces mayor; solo el extremo inferior del IC se acerca al valor de Saiz; MCO da {f(a['b_ols'])}. Unidades y mercado no son estrictamente comparables.")
    w("- v1 (F3, 17 CCAA): 2SLS IPC alquiler 0,44 (p cluster 0,16, WCB 0,12); valor tasado −0,88 (p 0,37). Con 49 provincias (más variación y cuotas más finas) el efecto sobre el alquiler es más grande y significativo; la compra sigue sin efecto detectable.\n")
    w("## Fuera de muestra\n")
    w(f"Anual, 2013-2020 (8 orígenes × 49 provincias, bloques expansivos con embargo 1 año). RMSE AR(4) panel {f(m1['rmse_AR4'],4)}; AR(4)+flujo observado en t {f(m1['rmse'],4)} (DM-HLN {f(m1['dm_vs_AR4'])}, p={f(m1['p_vs_AR4'],2)}: mejora no significativa); con flujo contemporáneo t+1 (NO es pronóstico) {f(m2['rmse'],4)} (DM {f(m2['dm_vs_AR4'])}, p={f(m2['p_vs_AR4'],2)}). ECM v1 solo existe en trimestres: panel_ecm_v1 vs panel_ar4 (h=4, orígenes T4, mismo número de observaciones) RMSE {f(ecm['rmse'],4)} vs {f(ecm['rmse_AR4'],4)}, DM {f(ecm['dm_vs_AR4'])} (p={f(ecm['p_vs_AR4'],2)}). No es posible añadir la tasa de inmigración (observada o instrumentada) al panel_ar4 trimestral: los flujos terminan en 2021-22 y sin muestra posterior. El instrumento no sirve para predecir (usa información posterior).\n")
    w("## Lo que NO se puede afirmar\n")
    for t in (
        "Que el contraste alquiler > compra sea robusto: p WCB una cola 0,03, bilateral 0,05, IC95 del contraste incluye 0 y no sobrevive a Holm sobre 7 (cota 0,21). Es EXPLORATORIO.",
        "Que la inmigración no afecte al precio de compra: el IC de beta_compra es muy ancho; solo se puede decir que no hay evidencia de efecto con este diseño, y que la estimación cambia de signo entre variantes de timing.",
        "Que beta_alq sea un efecto causal nítido: pasa la regla mecánica, pero F=14 moderado, identificación concentrada en Sudamérica, cuotas 2002 correlacionadas con extranjeros/paro/población iniciales, Sargan rechaza en precio, 8 grupos limitan BHJ/AKM, y el timing (stock a 1 enero vs flujo anual) no coincide exactamente. Debe leerse como efecto local (LATE) de la variación inducida por enclaves 2002.",
        "Que el efecto se mantenga tras 2021, en las provincias selladas (11, 16, 45) o en el periodo posterior (sin muestra sellada para H3).",
        "Que haya heterogeneidad por costa, turismo, tamaño o precio inicial: solo se observa con métodos sin instrumento y no se confirma con interacciones IV.",
        "Efectos de equilibrio general (salida de nativos, oferta, composición de la demanda) ni efectos sobre cantidades: el diseño estima el efecto reducido-forma sobre precios en la provincia.",
        "Capacidad predictiva fuera de muestra con inmigración (no hay mejora significativa frente a AR(4); ECM v1 no mejora a AR(4) en alquiler)."):
        w(f"- {t}")
    (OUT / "resumen.md").write_text("\n".join(L) + "\n")
