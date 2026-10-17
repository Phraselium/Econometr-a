"""V15-A · H1 y H2: escribe resultado.json, informe.md y hechos.json desde output/v15/p6/estimacion_bruta.json (sin teclear cifras)."""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
from pa_comun import FECHA, OUT, volcar  # noqa: E402

S = OUT / "p6"


def pc(x):
    """log-diferencia -> cambio porcentual."""
    return 100 * (np.exp(x) - 1)


def f1(x):
    return "n.d." if x is None or (isinstance(x, float) and not np.isfinite(x)) else f"{x:.1f}".replace(".", ",")


def rango(multi, est):
    v = [pc(s["att"]) for s in multi if s["estimador"] == est and s["fin"] == "2026T1" and s["att"] is not None and np.isfinite(s["att"])]
    return (min(v), max(v), len(v)) if v else (None, None, 0)


def main():
    r = json.loads((S / "estimacion_bruta.json").read_text(encoding="utf-8"))
    pr = r["principal"]
    out = {}
    hechos = []
    informe = ["# V15-A · H1 y H2: zonas tensionadas en Cataluña (renta y contratos nuevos de Incasòl)", "",
               f"Capa C4 (entrenamiento; asociación, sin lenguaje causal). Estimación **puntual descriptiva**: la inferencia de SDID (placebo literal no computable, Webb NO APTO), Honest DiD y control sintético es NO APTA (docs/v15/validacion_montecarlo.md, K13). Sin p-valor ni IC. `pendiente_sellada: true`: la evaluación sellada (hacia marzo de 2027) no se ha hecho. La ventana 2024T2-2026T1 ya la vio V9-D1 (ATT de CS −5,8 % en renta y −6,2 % en contratos, ambos C4): lo que sigue repite la ventana con otro diseño y es informativo, no confirmatorio.", "",
               "## Datos y diseño",
               f"- Medida: renta de los contratos nuevos de Incasòl (media ponderada por contratos de los tramos con renta publicada; stock excluido) y recuento de contratos. {r['N_muestra']} municipios catalanes del recuento de la adenda: {r['cohorte_2024T1']} de la cohorte 2024T1, {r['cohorte_2024T4']} de la 2024T4 y {r['nunca_tratados']} nunca tratados. Preperiodo limpio 2022T2-2023T4 (pesos de SDID en 2022T2-2023T2).",
               f"- Limitación de los datos: Incasòl suprime la renta con menos de 6 contratos; el panel de renta equilibrado en 16 trimestres solo conserva {r['N_tratados_renta_16q']} tratados y {r['N_donantes_renta_16q']} donantes (SDID de H1). CS usa los municipios con renta en cada celda. Las cotas de Lee acotan la selección.",
               f"- Balance previo (diferencia tipificada tratados menos donantes): log renta {f1(r['balance']['log_renta_pre']['dif_tipificada'])}; log contratos {f1(r['balance']['log_contratos_pre']['dif_tipificada'])}. Donantes en el soporte común de la renta previa: {r['balance']['donantes_en_soporte_comun_renta']} (la regla de la adenda exige ≥ 30 para C3; aquí sería suficiente, pero C3 es inalcanzable en entrenamiento).", ""]
    diag_comun = {
        "inferencia": "NO APTO (SDID placebo no computable; Webb tamaño 0,2155; Honest DiD NO APTO; control sintético NO APTO): estimación puntual",
        "honest_did_M_barra": "no evaluado (NO APTO)", "potencia_roth": "no calculable sin error típico válido"}

    for H, nombre, outc in (("H1", "renta media de los contratos nuevos (log)", "H1"), ("H2", "número de contratos nuevos", "H2")):
        p = pr[outc]
        multi = r["multiverso"][outc]
        cs, sd = p["CS_att"], p["SDID_att"]
        cs_lo, cs_hi, cs_n = rango(multi, "CS")
        sd_lo, sd_hi, sd_n = rango(multi, "SDID")
        ref = abs(cs) * 0.5
        pt = p["pretendencias"]
        plc = p["placebo_temporal_2023T2"]
        pe = r["placebo_espacial"][outc]
        ex = r["exclusiones"][outc]
        sc_txt = ""
        diag = dict(diag_comun)
        # pruebas con regla puntual (DV15-A, A1): máximo |coef| <= 0,5 |ATT|
        diag["pretendencias_CS"] = {"max_abs_coef_pre": pt["max_abs_pre"], "umbral_0.5ATT": ref, "compatible_puntualmente": bool(pt["max_abs_pre"] <= ref), "pendiente_lineal_por_anio": pt["pendiente_lineal_por_anio"]}
        diag["contraste_SDID_2023T3_T4"] = {"efecto": p["SDID_contraste_2023T3_T4"], "umbral_0.5ATT": 0.5 * abs(sd), "compatible_puntualmente": bool(abs(p["SDID_contraste_2023T3_T4"]) <= 0.5 * abs(sd))}
        diag["placebo_temporal_2023T2"] = {"CS": plc["CS"], "SDID": plc["SDID"], "compatible_CS": bool(abs(plc["CS"]) <= ref), "compatible_SDID": bool(abs(plc["SDID"]) <= 0.5 * abs(sd))}
        diag["placebo_espacial_1000"] = {"CS": pe["CS"], "SDID_200": pe["SDID"], "ATT_CS_fuera_de_p2.5_p97.5": bool(cs < pe["CS"]["p2_5"] or cs > pe["CS"]["p97_5"]), "nota": "escala de los ATT permutados, sin p-valor"}
        diag["exclusiones"] = {"sin_Barcelona_ni_decil_superior": ex["sin_Barcelona_ni_decil_superior"], "provincia_08_sin_capital": ex["provincia_08_sin_capital"],
                               "mantiene_signo_CS": bool(np.sign(ex["sin_Barcelona_ni_decil_superior"]["CS"]) == np.sign(cs) and np.sign(ex["provincia_08_sin_capital"]["CS"]) == np.sign(cs)),
                               "mantiene_signo_SDID": bool(np.sign(ex["sin_Barcelona_ni_decil_superior"]["SDID"]) == np.sign(sd) and np.sign(ex["provincia_08_sin_capital"]["SDID"]) == np.sign(sd))}
        diag["solapamiento_donantes_soporte_comun"] = {"n": r["balance"]["donantes_en_soporte_comun_renta"], "menos_de_30": r["balance"]["soporte_comun_menos_30"]}
        diag["balance"] = r["balance"]
        diag["exclusion_islas"] = "no aplica (no hay islas en Cataluña)"
        diag["oster_cinelli_evalue"] = "no calculados (diferencias en diferencias sin error típico válido)"
        diag["R_IPVA"] = "no estimada (adenda 2, B; S4 NO APTO)"
        if H == "H1":
            diag["control_sintetico_10_mayores"] = r["control_sintetico_10_mayores"]
            diag["cotas_Lee"] = r["lee_H1"]
            diag["moran_residuos"] = r["moran_residuos_H1"]
            diag["ruptura_preperiodo_largo_2022T2"] = r["ruptura_preperiodo_largo"]
            diag["CS_a1_cohorte4_control_solo_2024T2_T3"] = p["CS_a1_cohorte4_control_solo"]
        if H == "H2":
            pp = r["ppml"]["2026T1"]
            est_ppt = pp["att_pct"]
            diag["PPML_sin_Barcelona_ni_decil"] = ex["PPML_sin_Barcelona_ni_decil"]
        fallidas = [k for k, v in (("pretendencias_CS", diag["pretendencias_CS"]["compatible_puntualmente"]), ("contraste_SDID_2023T3_T4", diag["contraste_SDID_2023T3_T4"]["compatible_puntualmente"]),
                                   ("placebo_temporal_CS", diag["placebo_temporal_2023T2"]["compatible_CS"]), ("placebo_temporal_SDID", diag["placebo_temporal_2023T2"]["compatible_SDID"])) if not v]
        superadas = [k for k, v in (("pretendencias_CS", diag["pretendencias_CS"]["compatible_puntualmente"]), ("contraste_SDID_2023T3_T4", diag["contraste_SDID_2023T3_T4"]["compatible_puntualmente"]),
                                    ("placebo_temporal_CS", diag["placebo_temporal_2023T2"]["compatible_CS"]), ("placebo_temporal_SDID", diag["placebo_temporal_2023T2"]["compatible_SDID"])) if v]
        if diag["exclusiones"]["mantiene_signo_CS"]:
            superadas.append("exclusiones_signo_CS")
        else:
            fallidas.append("exclusiones_signo_CS")
        if diag["exclusiones"]["mantiene_signo_SDID"]:
            superadas.append("exclusiones_signo_SDID")
        else:
            fallidas.append("exclusiones_signo_SDID")
        diag["pruebas_superadas_puntualmente"] = superadas
        diag["pruebas_fallidas_puntualmente"] = fallidas
        diag["no_evaluadas_por_herramienta_NO_APTA"] = ["inferencia SDID (placebo)", "wild bootstrap Webb", "Honest DiD (M̄ ≥ 1)", "inferencia control sintético", "potencia de Roth", "inferencia por aleatorización (solo escala)"]

        est = {"CS_att_pct": pc(cs), "SDID_att_pct": pc(sd), "CS_por_cohorte_pct": {g: pc(v) for g, v in p["CS_att_por_cohorte"].items()},
               "SDID_por_cohorte_pct": {g: pc(v) for g, v in p["SDID_por_cohorte"].items()}, "rango_multiverso_CS_pct": [cs_lo, cs_hi], "rango_multiverso_SDID_pct": [sd_lo, sd_hi]}
        if H == "H2":
            est["PPML_principal_pct"] = r["ppml"]["2026T1"]["att_pct"]
            est["PPML_por_cohorte_pct"] = {"2024T1": r["ppml"]["2026T1"]["pct_g1"], "2024T4": r["ppml"]["2026T1"]["pct_g4"]}
        out[H] = {
            "rama": "v15/p6", "pregunta": f"{H}: asociación de la zona tensionada (Ley 12/2023, Cataluña) con {nombre}",
            "capa": "C4", "datos": "data/processed/v15/p6_zonas_tensionadas.parquet (Incasòl trimestral municipal 2022T2-2026T1; entrenamiento)",
            "N": {"municipios": r["N_muestra"], "tratados": r["tratados"], "nunca_tratados": r["nunca_tratados"], "renta_equilibrado_tratados": r["N_tratados_renta_16q"], "renta_equilibrado_donantes": r["N_donantes_renta_16q"]},
            "metodo": ("CS (2x2, control no tratado aún y nunca tratados) y SDID por cohortes, estimación puntual; " if H == "H1" else "PPML con efectos de municipio y trimestre (principal) más CS y SDID sobre log(1+n) (robustez); ") + "preperiodo 2022T2-2023T4; sin inferencia (herramientas NO APTAS)",
            "estimacion": est, "ic95": None, "p_ajustado": None, "nivel_evidencia": "DESCRIPTIVO",
            "diagnosticos": diag, "fuera_muestra": {"modelo": None, "rmse": None, "dm_vs_ar4": None},
            "pendiente_sellada": True,
            "p_valores_para_BY": [{"hipotesis": H, "p": None, "motivo": "inferencia NO APTA (SDID placebo no computable, Webb NO APTO); H1/H2 son de la familia Holm {H1,H2,H4} de la evaluación sellada, no de BY"}],
            "notas": "Asociación C4, sin lenguaje causal. Ventana 2024T2-2026T1 ya vista en V9-D1. Hechos candidatos: ver hechos.json. Desviaciones: docs/v15/desviaciones.md (DV15-A).",
            "multiverso_n": len(multi), "multiverso_registro": "output/v15/p6/registro.csv"}

        # --------- informe por hipótesis ---------
        informe += [f"## {H} · {nombre}",
                    f"- **CS (diseño a):** {f1(pc(cs))} % (cohorte 2024T1: {f1(pc(p['CS_att_por_cohorte']['2024T1']))} %; cohorte 2024T4: {f1(pc(p['CS_att_por_cohorte']['2024T4']))} %). Con solo la cohorte 2024T4 como control de 2024T2-2024T3: {f1(pc(p['CS_a1_cohorte4_control_solo']))} %.",
                    f"- **SDID (diseño b):** {f1(pc(sd))} % con {p['SDID_n_donantes']} donantes (cohorte 2024T1: {f1(pc(p['SDID_por_cohorte']['2024T1']))} %; 2024T4: {f1(pc(p['SDID_por_cohorte']['2024T4']))} %)."]
        if H == "H2":
            informe.append(f"- **PPML (principal de H2):** {f1(r['ppml']['2026T1']['att_pct'])} % (2024T1: {f1(r['ppml']['2026T1']['pct_g1'])} %; 2024T4: {f1(r['ppml']['2026T1']['pct_g4'])} %); TWFE simple de referencia {f1(r['ppml']['2026T1']['twfe_pct'])} %. Sin error típico válido.")
        informe += [f"- **Multiverso (36 especificaciones, BH no aplicable sin p):** CS entre {f1(cs_lo)} % y {f1(cs_hi)} % ({cs_n} estimables); SDID entre {f1(sd_lo)} % y {f1(sd_hi)} % ({sd_n} estimables). Las celdas con menos de 3 donantes no son estimables o son degeneradas (ver registro.csv).",
                    f"- **Pretendencias** (CS, 2022T2-2023T3): máximo |coef| {f1(100*pt['max_abs_pre'])} puntos log·100 frente al umbral declarado {f1(100*ref)}: {'compatible' if diag['pretendencias_CS']['compatible_puntualmente'] else 'NO compatible'}. Contraste SDID 2023T3-2023T4: {f1(100*p['SDID_contraste_2023T3_T4'])}: {'compatible' if diag['contraste_SDID_2023T3_T4']['compatible_puntualmente'] else 'NO compatible'}.",
                    f"- **Placebo temporal (2023T2):** CS {f1(100*plc['CS'])}, SDID {f1(100*plc['SDID'])} (log·100). **Placebo espacial** (1.000 permutaciones, CS): DT {f1(100*pe['CS']['dt'])}, rango p2,5-p97,5 [{f1(100*pe['CS']['p2_5'])}; {f1(100*pe['CS']['p97_5'])}]; el ATT de CS {'queda fuera' if diag['placebo_espacial_1000']['ATT_CS_fuera_de_p2.5_p97.5'] else 'queda dentro'} de ese rango (escala, no p-valor).",
                    f"- **Exclusiones:** sin Barcelona ni el decil superior de renta: CS {f1(pc(ex['sin_Barcelona_ni_decil_superior']['CS']))} %, SDID {f1(pc(ex['sin_Barcelona_ni_decil_superior']['SDID']))} %; provincia 08 sin la capital: CS {f1(pc(ex['provincia_08_sin_capital']['CS']))} %, SDID {f1(pc(ex['provincia_08_sin_capital']['SDID']))} %."]
        if H == "H1":
            lee = r["lee_H1"]
            sc = r["control_sintetico_10_mayores"]
            informe += [f"- **Cotas de Lee** (renta observada en todos los trimestres posteriores: {f1(100*lee['p_obs_tratados'])} % de tratados frente a {f1(100*lee['p_obs_controles'])} % de donantes): variación de la renta entre {f1(100*lee['lim_inf'])} y {f1(100*lee['lim_sup'])} puntos log·100.",
                        f"- **Control sintético** (10 mayores tratados, puntual): mediana {f1(sc['mediana_pct'])} %, media {f1(sc['media_pct'])} %. **Ruptura en 2022T2** (preperiodo largo): salto de nivel de la brecha {f1(100*r['ruptura_preperiodo_largo']['salto_nivel_2022T2'])} puntos log·100; ruptura única estimada en {r['ruptura_preperiodo_largo']['ruptura_unica_estimada']}. Moran de residuos: I = {f1(r['moran_residuos_H1']['I_moran']*100)}/100."]
        informe += [f"- **Pruebas superadas (regla puntual):** {', '.join(superadas) or 'ninguna'}. **Fallidas:** {', '.join(fallidas) or 'ninguna'}. **No evaluadas (herramienta NO APTA):** inferencia de SDID, Webb, Honest DiD, potencia de Roth.", ""]

        # --------- hechos candidatos ---------
        base = dict(unidad="%", periodo="2024T2-2026T1", cobertura="Cataluña, municipios con ≥ 5 contratos en 2022T2-2023T4", fuentes=["Incasòl"], capa="C4", fecha_dato=FECHA)
        hechos += [
            dict(id=f"V15-{H}-cs-att", indicador=f"{H}: asociación de la zona tensionada con {nombre}, CS puntual (rango = mínimo y máximo de las especificaciones CS del multiverso; no es IC)", valor=round(pc(cs), 2), min=round(cs_lo, 2), max=round(cs_hi, 2), ficha=f"output/v15/p6/informe.md#ficha-{H.lower()}-cs", **base),
            dict(id=f"V15-{H}-sdid-att", indicador=f"{H}: ídem, SDID puntual (rango = especificaciones SDID estimables; no es IC)", valor=round(pc(sd), 2), min=round(sd_lo, 2) if sd_lo is not None else None, max=round(sd_hi, 2) if sd_hi is not None else None, ficha=f"output/v15/p6/informe.md#ficha-{H.lower()}-sdid", **base),
            dict(id=f"V15-{H}-placebo-cs", indicador=f"{H}: placebo temporal 2023T2 (CS), puntual", valor=round(pc(plc["CS"]), 2), min=None, max=None, unidad="%", periodo="2023T2-2023T4", cobertura=base["cobertura"], fuentes=["Incasòl"], capa="C4", fecha_dato=FECHA, ficha=f"output/v15/p6/informe.md#ficha-{H.lower()}-placebo"),
        ]
        if H == "H2":
            hechos.append(dict(id="V15-H2-ppml", indicador="H2: asociación con el número de contratos nuevos, PPML con efectos de municipio y trimestre (puntual)", valor=round(r["ppml"]["2026T1"]["att_pct"], 2), min=round(min(r["ppml"]["2026T1"]["pct_g4"], r["ppml"]["2026T1"]["pct_g1"]), 2), max=round(max(r["ppml"]["2026T1"]["pct_g4"], r["ppml"]["2026T1"]["pct_g1"]), 2), ficha="output/v15/p6/informe.md#ficha-h2-ppml", **base))
        if H == "H1":
            hechos.append(dict(id="V15-H1-lee", indicador="H1: cotas de Lee de la variación de la renta (valor = sin recorte; min/max = cotas)", valor=round(100 * r["lee_H1"]["sin_recorte"], 2), min=round(100 * r["lee_H1"]["lim_inf"], 2), max=round(100 * r["lee_H1"]["lim_sup"], 2),
                               unidad="puntos log·100", periodo="2024T2-2026T1", cobertura=base["cobertura"], fuentes=["Incasòl"], capa="C4", fecha_dato=FECHA, ficha="output/v15/p6/informe.md#ficha-h1-lee"))

    informe += ["## Lectura frente a lo ya publicado",
                "- H1: el signo coincide con V9-D1a (−5,8 %), que no superó pretendencias ni placebo; aquí tampoco las supera la regla puntual declarada (ver arriba), así que el valor no se interpreta como magnitud de la intervención. No contradice con dirección ninguna conclusión de la 1.0.",
                "- H2: V9-D1a concluyó «sin diferencia detectable» con una estimación de −6,2 % (−13,2 a 0,7). Las estimaciones puntuales de aquí son negativas pero sin inferencia válida: no pueden contradecir ni confirmar un contraste de significación. No es una parada.",
                "- Cada estimación se lee junto a V9-D1 (multiplicidad entre versiones, preregistro_v15 §0).", "",
                "## Fichas reproducibles",
                "Todas: `python3 src/v15/p6_zonas.py && python3 src/v15/p6_informe.py` (SEED 20261010); cifras en output/v15/p6/estimacion_bruta.json.",
                "- <a id=\"ficha-h1-cs\"></a>**ficha-h1-cs / ficha-h2-cs:** clave `principal.<H>.CS_att` (log-diferencia media de las celdas ATT(g,t), g ∈ {2024T1, 2024T4}, t desde 2024T2 / 2024T4 hasta 2026T1, base g−1, ponderada por tratados), convertida a % con 100·(exp(x) − 1). Rango: `multiverso.<H>` con estimador CS y fin 2026T1.",
                "- <a id=\"ficha-h1-sdid\"></a>**ficha-h1-sdid / ficha-h2-sdid:** clave `principal.<H>.SDID_att`; SDID por cohorte con donantes nunca tratados, pesos en 2022T2-2023T2 (src/v15/pa_did.py:sdid).",
                "- <a id=\"ficha-h1-placebo\"></a>**ficha-h1-placebo / ficha-h2-placebo:** `principal.<H>.placebo_temporal_2023T2.CS` (adopción falsa en 2023T2, base 2023T1, controles nunca tratados).",
                "- <a id=\"ficha-h2-ppml\"></a>**ficha-h2-ppml:** `ppml.2026T1.att_pct` (Poisson pseudo-máxima verosimilitud, efectos de municipio y trimestre, cohorte × posterior).",
                "- <a id=\"ficha-h1-lee\"></a>**ficha-h1-lee:** `lee_H1` (selección = renta observada en todos los trimestres posteriores y previos).",
                "- <a id=\"ficha-h2-cs\"></a><a id=\"ficha-h2-sdid\"></a><a id=\"ficha-h2-placebo\"></a>"]

    volcar(S / "resultado_H1.json", out["H1"])
    volcar(S / "resultado_H2.json", out["H2"])
    volcar(S / "resultado.json", {"H1": out["H1"], "H2": out["H2"]})
    volcar(S / "hechos.json", hechos)
    (S / "informe.md").write_text("\n".join(informe) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
