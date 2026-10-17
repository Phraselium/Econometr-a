"""V16 · fase 6 · grupo B: ensambla resultado.json, hechos.json, informe.md y registro.csv de Q3, Q4 y Q6 a partir de los parciales.

Ejecución (tras q3_shiftshare.py, q3_seccion.py, q4_oferta.py y q6_itp.py): python src/v16/qb_informe.py
Todo es C4 (asociación o descriptivo), pendiente de evaluación sellada; sin lenguaje causal.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
import qb_comun as C  # noqa: E402

O = C.RAIZ / "output" / "v16"
HOY = C.FECHA
FU_PAD = "INE, padrón continuo por nacionalidad (provincial/municipal/sección); MIVAU, SERPAVI"
CONSIGNA = "Asociación C4; pendiente de evaluación sellada. Sin lenguaje causal."


def cargar(p):
    return json.loads((O / p).read_text(encoding="utf-8"))


def f(x, d=4):
    return "n/d" if x is None else f"{x:.{d}f}".replace(".", ",")


def pct(x, d=2):
    return "n/d" if x is None else f"{100 * x:.{d}f} %".replace(".", ",")


def base(pregunta, datos, N, metodo, estimacion, diag, notas, p_valores, ic95=None):
    return {"rama": "r16/fase6-grupoB", "pregunta": pregunta, "capa": "C4", "datos": datos, "N": N, "metodo": metodo, "estimacion": estimacion,
            "ic95": ic95, "p_ajustado": None, "nivel_evidencia": "DESCRIPTIVO", "diagnosticos": diag,
            "fuera_muestra": {"modelo": None, "rmse": None, "dm_vs_ar4": None, "nota": "no es un diseño predictivo"},
            "pendiente_sellada": True, "p_valores_para_BY": p_valores, "notas": notas,
            "regla_hallazgo": {"a_q_le_0_10": "pendiente del control BY global (lo hace el orquestador)", "b_tipo_S_M": "no evaluable sin SE válido o sin magnitud de referencia",
                               "c_sellada": "pendiente", "resultado": "sin hallazgo; a lo sumo pista C4"}}


# ------------------------------------------------------------------ Q3
def q3():
    c = cargar("q3/q3c_resultado_parcial.json")
    b = cargar("q3/q3b_resultado_parcial.json")
    reg = pd.concat([pd.read_csv(O / "q3/registro_q3c.csv"), pd.read_csv(O / "q3/registro_q3b.csv")], ignore_index=True)
    reg.to_csv(O / "q3/registro.csv", index=False)
    pc1, pc2, bp = c["principal"]["Q3-c1"], c["principal"]["Q3-c2"], b["principal"]
    d1, d2, db = c["diagnosticos"]["Q3-c1"], c["diagnosticos"]["Q3-c2"], b["diagnosticos"]
    m1, m2, mb = c["multiverso"]["Q3-c1"], c["multiverso"]["Q3-c2"], b["multiverso"]
    g = b["blp_gates"]
    est = {"Q3-c1": {"beta_log_valor_tasado_por_punto_poblacion_extranjera_predicha": pc1["beta_por_punto"], "n": pc1["n"], "ic95": None, "p": None,
                      "inferencia": "AKM/AKM0 NO APTOS: solo puntual", "multiverso": m1},
           "Q3-c2": {"beta_log_compraventas_por_punto": pc2["beta_por_punto"], "n": pc2["n"], "ic95": None, "p": None, "inferencia": "AKM/AKM0 NO APTOS: solo puntual",
                      "multiverso": m2},
           "Q3-b": {"beta_dlog_serpavi_por_DT_cuota_extranjeros": bp["beta_por_DT"], "se_conley_2km": bp["se"], "ic95": bp["ic95"], "p": bp["p"], "n_secciones": bp["n"],
                    "n_municipios": bp["n_mun"], "multiverso": mb, "sensibilidad_rango_espacial": b["sensibilidad_rango_espacial"]},
           "BLP_GATES_Q3": g}
    diag = {"Q3-c1": d1, "Q3-c2": d2, "Q3-b": db, "Rotemberg_top5": c["diagnosticos"]["rotemberg_top5"],
            "pruebas": {
                "superadas": ["Q3-b: Conley 2 km APTO solo en el escenario principal", "Q3-b: sin grandes ciudades, mismo signo (%s por DT)" % f(db["sin_grandes_ciudades"]["beta_por_DT"]),
                              "Q3-b: Cinelli-Hazlett RV_q=1 = %s (≥ 0,05)" % f(db["cinelli_hazlett_RV_q1"]),
                              "Q3-c1/c2: sin grandes ciudades, mismo signo", "Q3-c1: pendiente previa 2003-2008 pequeña frente al efecto"],
                "fallidas": ["Q3-b: pretendencia placebo 2018-2021 = %s por DT (IC Conley %s a %s) excluye el 0" % (
                    f(db["pretendencia_placebo_2018_2021"]["beta_por_DT"]), f(db["pretendencia_placebo_2018_2021"]["ic95"][0]), f(db["pretendencia_placebo_2018_2021"]["ic95"][1])),
                    "Q3-b: no robusto a la sensibilidad del rango espacial (radios 0,5 y 1,5 km no pasan)",
                    "Q3-c: F efectivo no evaluable con herramienta APTA; en V9-D4 fue de 3,4 a 3,7 (< 10)",
                    "Q3-c1: estimación inestable al controlar por el instrumento retardado (de %s a %s)" % (f(pc1["beta_por_punto"]), f(d1["control_instrumento_retardado"]["beta_x"]))],
                "no_evaluables": ["AKM, AKM0 (NO APTOS)", "BLP/GATES (NO APTO): solo puntual", "TOST (sin magnitud en Q3-b; sin SE en Q3-c)", "desbordamientos a 15 km (no aplica a escala provincial, D2)",
                                  "Honest DiD / raíces unitarias con dependencia transversal (CIPS NO APTO): no aplican a una forma reducida con efectos fijos"]}}
    notas = [CONSIGNA, "Q3 municipal de alquiler retirado (es H4 con otra muestra, adenda punto 7).",
             "Q3-b es correlación transversal; Conley a 2 km no es robusto al rango espacial; las variantes son puntuales.",
             "Todas las desviaciones de operativización en docs/v16/desviaciones.md (D2).",
             "Valor tasado: F de 3,4 a 3,7 en V9-D4 (C4); no hay contradicción de dirección con V9-D4 (instrumento débil)."]
    pv = [{"id": "Q3-b|principal", "p": bp["p"], "rama": "diseños", "nota": "única prueba de Q3 con p-valor válido (Conley 2 km APTO, escenario principal)"},
          {"id": "Q3-c1|principal", "p": None, "rama": "diseños", "nota": "AKM NO APTO: sin p-valor"},
          {"id": "Q3-c2|principal", "p": None, "rama": "diseños", "nota": "AKM NO APTO: sin p-valor"},
          {"id": "Q3|BLP_GATES", "p": None, "rama": "diseños (prueba adicional, punto 13)", "nota": "NO APTO: sin p-valor"}]
    res = base("Q3: inmigración y precios/alquiler más allá de H4 (Q3-c1 valor tasado, Q3-c2 compraventas, Q3-b barrio) y BLP/GATES",
               "data/processed/v16/entrenamiento: padron_nacionalidad, base_poblacion, base_precio, base_alquiler (SERPAVI sección), tension_social; secciones.parquet (solo geometría)",
               {"Q3-c1": pc1["n"], "Q3-c2": pc2["n"], "Q3-b": bp["n"], "blp": g["n"]},
               "Shift-share de forma reducida (cuotas de 2003 × crecimiento nacional sin la provincia) con FE de provincia y año; correlación transversal por sección con FE de municipio y Conley 2 km; BLP lineal y GATES con validación cruzada",
               est, diag, notas, pv, ic95={"Q3-b": bp["ic95"], "Q3-c1": None, "Q3-c2": None})
    res["nivel_evidencia"] = "EXPLORATORIO (Q3-b, con pretendencia no nula); DESCRIPTIVO (Q3-c1, Q3-c2, BLP/GATES)"
    # hechos
    sec = "Padrón por nacionalidad, SERPAVI y valor tasado/compraventas de entrenamiento"
    lo1 = [e["beta"] for e in c["especificaciones"] if e["pregunta"] == "Q3-c1" and e["norm"] == "pts"]
    lo2 = [e["beta"] for e in c["especificaciones"] if e["pregunta"] == "Q3-c2" and e["norm"] == "pts"]
    H = [
        C.hecho("V16-Q3-c1-beta", "Q3-c1: asociación de log valor tasado con la población extranjera predicha (por punto), forma reducida", pc1["beta_por_punto"], min(lo1), max(lo1),
                "log por punto de población", "2011-2022", f"{pc1['n_provincias']} provincias" if "n_provincias" in pc1 else "38 provincias de entrenamiento", sec, "q3-c1", "q3", "2022"),
        C.hecho("V16-Q3-c2-beta", "Q3-c2: asociación de log compraventas con la población extranjera predicha (por punto), forma reducida", pc2["beta_por_punto"], min(lo2), max(lo2),
                "log por punto de población", "2011-2022", "41 provincias de entrenamiento", sec, "q3-c2", "q3", "2022"),
        C.hecho("V16-Q3-b-beta", "Q3-b: asociación transversal del Δlog SERPAVI 2021-2024 con la cuota de extranjeros 2022 (por DT)", bp["beta_por_DT"], mb["min"], mb["max"],
                "log por desviación típica", "2021-2024", f"{bp['n']} secciones en {bp['n_mun']} municipios", "MIVAU SERPAVI (VC); INE padrón por sección", "q3-b", "q3", "2024"),
        C.hecho("V16-Q3-b-pretendencia", "Q3-b: coeficiente placebo con el Δlog SERPAVI 2018-2021 (pretendencia)", db["pretendencia_placebo_2018_2021"]["beta_por_DT"],
                db["pretendencia_placebo_2018_2021"]["ic95"][0], db["pretendencia_placebo_2018_2021"]["ic95"][1], "log por desviación típica", "2018-2021",
                f"{db['pretendencia_placebo_2018_2021']['n']} secciones", "MIVAU SERPAVI (VC); INE padrón por sección", "q3-b", "q3", "2021"),
        C.hecho("V16-Q3-blp-gates", "Q3: diferencia GATES cuartil 4 menos cuartil 1 de la asociación de Q3-b (descriptivo)", g["gates_q4_menos_q1"], None, None,
                "log por desviación típica", "2021-2024", f"{g['n']} secciones", "MIVAU SERPAVI; INE; ADRH; Catastro", "q3-blp", "q3", "2024"),
        C.hecho("V16-Q3-rotemberg-1", "Q3-c: peso de Rotemberg del origen con mayor peso (Rumanía) en el shift-share", c["diagnosticos"]["rotemberg_top5"][0]["alfa_rotemberg"], None, None,
                "fracción del estimador", "2011-2022", "28 orígenes, 38 provincias", "INE padrón por nacionalidad", "q3-rotemberg", "q3", "2022"),
    ]
    inf = f"""# Q3 · Inmigración: valor tasado, compraventas y barrio (V16, fase 6)

**Capa C4. {CONSIGNA}** Datos: solo entrenamiento. Desviaciones de operativización: docs/v16/desviaciones.md (D2). Registro: output/v16/q3/registro.csv.

## Resultado
| Diseño | Estimación | Inferencia | Lectura |
|---|---|---|---|
| Q3-c1 (log valor tasado, 38 prov., 2011-2022) | {f(pc1['beta_por_punto'])} log por punto (≈ {pct(pc1['beta_por_punto'])} por punto) | solo puntual (AKM/AKM0 NO APTOS) | {f(pc1['beta_por_punto'] / 0.01, 2)} veces la referencia de Saiz (0,01); descriptivo |
| Q3-c2 (log compraventas, 41 prov.) | {f(pc2['beta_por_punto'])} log por punto | solo puntual | signo negativo; sin referencia comparable |
| Q3-b (Δlog SERPAVI 2021-24, {bp['n']} secciones) | {f(bp['beta_por_DT'])} por DT (IC 95 % Conley 2 km {f(bp['ic95'][0])} a {f(bp['ic95'][1])}; p = {bp['p']:.1e}) | Conley 2 km, solo escenario principal | correlación; **pretendencia placebo no nula** |
| BLP/GATES (Q3-b) | GATES Q4-Q1 = {f(g['gates_q4_menos_q1'])}; ganancia de R² dentro = {f(g['ganancia_r2_within'])} | NO APTO: solo puntual | sin heterogeneidad apreciable |

Multiverso (resumen, sin IC): Q3-c1 {m1['n_especificaciones']} especificaciones, mediana {f(m1['mediana_beta_por_DT'])} por DT, {pct(m1['proporcion_mismo_signo_que_principal'], 0)} con el mismo signo; Q3-c2 {m2['n_especificaciones']}, mediana {f(m2['mediana_beta_por_DT'])}, {pct(m2['proporcion_mismo_signo_que_principal'], 0)}; Q3-b {mb['n_especificaciones']}, mediana {f(mb['mediana_beta_por_DT'])}, {pct(mb['proporcion_mismo_signo'], 0)} (variantes puntuales).

## Pruebas
- Superadas: {'; '.join(diag['pruebas']['superadas'])}.
- Fallidas: {'; '.join(diag['pruebas']['fallidas'])}.
- No evaluables: {'; '.join(diag['pruebas']['no_evaluables'])}.
- Sensibilidad: Q3-b Oster δ = {f(db['oster']['delta_beta0_rmax1_3'], 1)} (negativo: los efectos fijos acercan la estimación a un valor mayor, no frágil por la regla δ < 1); E-value del punto {f(db['e_value_punto'], 2)} (límite del IC {f(db['e_value_limite_ic'], 2)}). Q3-c1: δ = {f(d1['oster']['delta_beta0_rmax1_3'], 1)}, E-value {f(d1['e_value_punto'], 2)}.
- Balance Q3-b con FE de municipio (coeficiente estandarizado por DT de cuota): renta ADRH {f(db['balance_covariables_con_FE_municipio']['renta_adrh']['coef_std_por_DT'], 2)}, población {f(db['balance_covariables_con_FE_municipio']['poblacion']['coef_std_por_DT'], 2)}, % vivienda turística {f(db['balance_covariables_con_FE_municipio']['pct_vut']['coef_std_por_DT'], 2)}: desbalance notable en renta y vivienda turística (sin umbral pre-registrado).
- Rotemberg (Q3-c): Rumanía {f(c['diagnosticos']['rotemberg_top5'][0]['alfa_rotemberg'], 3)}, Reino Unido {f(c['diagnosticos']['rotemberg_top5'][1]['alfa_rotemberg'], 3)}; suma de pesos negativos {f(c['diagnosticos']['rotemberg_suma_alfa_negativos'], 3)}. Primera etapa descriptiva (coef. {f(d1['primera_etapa_descriptiva']['coef'], 2)}, R² dentro {f(d1['primera_etapa_descriptiva']['r2_within'], 2)}); F efectivo con herramienta APTA no disponible.
- Moran de residuos: provincial I = {f(d1['moran_residuos_prov']['I'], 3)}; secciones I = {f(db['moran_residuos_secciones']['I'], 3)} (efecto de la demedia por municipio).

## Regla de hallazgo
(a) q ≤ 0,10: pendiente del control BY global (único p-valor propio: Q3-b). (b) Q3-b no tiene magnitud de referencia; Q3-c carece de SE válido: errores S y M no evaluables. (c) sellada: pendiente. **Sin hallazgo.** TOST: «no concluyente».
Frente a la conclusión publicada V9-D4 (instrumento débil, C4): ninguna contradicción de dirección; no hay parada D.

## Fichas reproducibles
Comando: `python src/v16/q3_shiftshare.py && python src/v16/q3_seccion.py && python src/v16/qb_informe.py` (SEED 20261010).
- <a id="q3-c1"></a>**q3-c1.** x_pt = 100·Σ_o F_{{po,2003}}·(N_{{o,t,-p}}/N_{{o,2003,-p}})/Pob_{{p,2003}} (28 orígenes; padron_pob_nacionalidad provincial); log valor tasado anual (base_precio) ~ x + FE provincia + FE año, 2011-2022, N = {pc1['n']}. Rango = 8 especificaciones con x en puntos (orígenes, año base 2003/2004, efectos temporales).
- <a id="q3-c2"></a>**q3-c2.** Igual con log compraventas provinciales anuales (INE ETDP 6150, total de vivienda), N = {pc2['n']}.
- <a id="q3-b"></a>**q3-b.** Δlog de la mediana €/m² SERPAVI (tipología VC) 2021→2024 ~ cuota de extranjeros 2022 estandarizada + FE municipio; Conley 2 km (núcleo de Bartlett), secciones de entrenamiento (`unidad_sellada_v16`), municipios con ≥ 2 secciones. Rango = 6 variantes puntuales.
- <a id="q3-blp"></a>**q3-blp.** Interacciones exposición × {{renta ADRH 2019, población 2022, cuota extranjeros, % VUT 2021-02, obra per cápita 2018-21}}; GATES por cuartiles con 2 mitades por municipio.
- <a id="q3-rotemberg"></a>**q3-rotemberg.** α_o = Σ c̃_o·B̃ / Σ B̃², c̃ residualizado en FE (output/v16/q3/q3c_rotemberg.csv).
- <a id="q3-pretendencia"></a>Pretendencia: igual que q3-b con Δlog 2018→2021.
"""
    C.volcar(O / "q3/resultado.json", res)
    C.volcar(O / "q3/hechos.json", H)
    (O / "q3/informe.md").write_text(inf, encoding="utf-8")
    return res


# ------------------------------------------------------------------ Q4
def q4():
    r = cargar("q4/q4_resultado_parcial.json")
    a, b = r["Q4a"], r["Q4b"]
    pa, pb = a["principal"], b["principal"]
    da, db = a["diagnosticos"], b["diagnosticos"]
    est = {"Q4a": {"beta_log_obra_neta_por_DT_red_natura": pa["beta_por_DT_RN"], "n": pa["n"], "n_municipios": pa["n_municipios"], "ic95": None, "p": None, "multiverso": a["multiverso"]},
           "Q4b": {"beta_interaccion_choque_x_RN": pb["beta_interaccion_por_DT_RN_y_punto_de_choque"], "n": pb["n"], "n_municipios": pb["n_municipios"], "ic95": None, "p": None,
                   "multiverso": b["multiverso"]}}
    diag = {"Q4a": da, "Q4b": db, "pruebas": {
        "superadas": ["Q4a: sin grandes ciudades, mismo resultado (%s)" % f(da["sin_grandes_ciudades"]["beta"]), "Q4a: periodo 2012-2016 de signo igual (%s; no es placebo)" % f(da["periodo_regularizacion_2012_2016"]["beta"]),
                      "Q4b: sin grandes ciudades, mismo signo (%s)" % f(db["sin_grandes_ciudades"]["beta_interaccion"])],
        "fallidas": ["Q4a: dependencia espacial de residuos (Moran I = %s, p de permutación %s)" % (f(da["moran_residuos_municipios"]["I"], 3), f(da["moran_residuos_municipios"]["p_perm_bilateral"], 3)),
                     "Q4b: placebo de choque adelantado de igual signo y mayor tamaño que el efecto (%s frente a %s)" % (f(db["placebo_choque_adelantado"]["beta_interaccion"]), f(pb["beta_interaccion_por_DT_RN_y_punto_de_choque"])),
                     "Q4a y Q4b: la Red Natura no es exógena (restricción de uso del suelo correlacionada con rural y despoblación)"],
        "no_evaluables": ["inferencia con agrupación provincial (rejilla TWFE provincia NO APTA): sin p-valor ni IC", "Cinelli-Hazlett (requiere t válido)",
                          "costa, pendiente, agua y planeamiento: no están en disco (tareas del autor)"]}}
    pv = [{"id": "Q4a|principal", "p": None, "rama": "diseños", "nota": "agrupación provincial NO APTA"}, {"id": "Q4b|principal", "p": None, "rama": "diseños", "nota": "agrupación provincial NO APTA"}]
    res = base("Q4: oferta municipal y restricción física (% Red Natura): Q4a obra nueva neta, Q4b interacción con el choque de demanda de Q3",
               "data/processed/v16/entrenamiento: base_oferta (obra neta Catastro, SERPAVI municipal), oferta_suelo_terceros (Red Natura 2000), padron_nacionalidad",
               {"Q4a": pa["n"], "Q4b": pb["n"]},
               "Q4a: MCO con FE de provincia y año, 2018-2025; Q4b: primeras diferencias con FE de año, interacción choque × RN, 2018-2022. Solo puntual.", est, diag,
               [CONSIGNA, "La Red Natura no se presenta como exógena. Sin magnitud de referencia: (b) no se cumple.", "Q4b: ventana 2018-2022 porque el padrón por nacionalidad termina en 2022 (D2)."], pv)
    H = [C.hecho("V16-Q4a-beta", "Q4a: asociación de log obra nueva neta (obra > 0) con el porcentaje de Red Natura municipal (por DT = " + f(pa["sd_rn_entre_municipios_pp"], 1) + " pp)", pa["beta_por_DT_RN"],
                 a["multiverso"]["min"], a["multiverso"]["max"], "log por desviación típica", "2018-2025", f"{pa['n_municipios']} municipios", "Catastro (obra neta); MITECO (Red Natura 2000)", "q4a", "q4", "2025"),
         C.hecho("V16-Q4b-beta", "Q4b: interacción del choque de demanda (Δ población extranjera predicha) con el % de Red Natura sobre el Δlog SERPAVI", pb["beta_interaccion_por_DT_RN_y_punto_de_choque"],
                 b["multiverso"]["min"], b["multiverso"]["max"], "log por punto de choque y DT de RN", "2018-2022", f"{pb['n_municipios']} municipios", "MIVAU SERPAVI; INE padrón; MITECO", "q4b", "q4", "2022")]
    inf = f"""# Q4 · Oferta municipal y restricción física (V16, fase 6)

**Capa C4, descriptiva. {CONSIGNA}** Datos de entrenamiento; desviaciones D2 en docs/v16/desviaciones.md. Registro: output/v16/q4/registro.csv.

## Resultado
| Diseño | Estimación puntual | Inferencia |
|---|---|---|
| Q4a: log obra neta (obra > 0), 2018-2025, {pa['n_municipios']} municipios, N = {pa['n']} | {f(pa['beta_por_DT_RN'])} por DT de Red Natura ({f(pa['sd_rn_entre_municipios_pp'], 1)} pp), con FE de provincia y año | ninguna (agrupación provincial NO APTA) |
| Q4b: Δlog SERPAVI (VC), 2018-2022, {pb['n_municipios']} municipios, N = {pb['n']} | interacción {f(pb['beta_interaccion_por_DT_RN_y_punto_de_choque'])} (choque principal {f(pb['beta_choque_main'])}) | ninguna |

Multiverso (sin IC): Q4a {a['multiverso']['n']} especificaciones, mediana {f(a['multiverso']['mediana'])}, {pct(a['multiverso']['proporcion_mismo_signo'], 0)} con el mismo signo (las variantes asinh tienen otra escala); Q4b {b['multiverso']['n']}, mediana {f(b['multiverso']['mediana'])}, {pct(b['multiverso']['proporcion_mismo_signo'], 0)}.

## Pruebas
- Superadas: {'; '.join(diag['pruebas']['superadas'])}.
- Fallidas: {'; '.join(diag['pruebas']['fallidas'])}.
- No evaluables: {'; '.join(diag['pruebas']['no_evaluables'])}.
- Sensibilidad Q4a: Oster δ = {f(da['oster']['delta_beta0_rmax1_3'], 1)} (no frágil por la regla δ < 1); E-value del punto {f(da['e_value_punto'], 2)}. Q4b: E-value del punto {f(db['e_value_punto'], 2)}.
- Heterocedasticidad Q4a (BP LM) {f(da['het_autocorr']['breusch_pagan_LM'], 1)}; autocorrelación (Wooldridge) {f(da['het_autocorr']['wooldridge_pendiente'], 2)} frente a -0,5.

## Regla de hallazgo
Sin p-valor propio (NO APTO) y sin magnitud de referencia: (a) pendiente, (b) no se cumple, (c) pendiente. **Sin hallazgo.** No hay conclusión publicada sobre elasticidad municipal: sin contradicción.

## Fichas reproducibles
Comando: `python src/v16/q4_oferta.py && python src/v16/qb_informe.py`.
- <a id="q4a"></a>**q4a.** log(obra neta > 0) del Catastro ~ % Red Natura estandarizado + FE provincia + FE año, 2018-2025. Rango = 8 variantes (log/asinh, control log unidades 2017, 2018-2025/2018-2021).
- <a id="q4b"></a>**q4b.** Δlog mediana €/m² SERPAVI municipal (VC) ~ (Δx_mt × RN_std) + Δx_mt + FE año; Δx = cambio anual del shift-share municipal (cuotas del padrón de 2003, 28 orígenes, sin la provincia). Rango = 8 variantes (VC/VU, 2018-2022/2018-2020, FE año/provincia×año).
"""
    C.volcar(O / "q4/resultado.json", res)
    C.volcar(O / "q4/hechos.json", H)
    (O / "q4/informe.md").write_text(inf, encoding="utf-8")
    return res


# ------------------------------------------------------------------ Q6
def q6():
    r = cargar("q6/q6_resultado_parcial.json")
    v, p = r["Q6-v"], r["Q6-p"]
    est, diag = {}, {}
    for q, x in (("Q6-v", v), ("Q6-p", p)):
        est[q] = {"beta_por_punto_de_tipo": x["principal"]["beta_por_punto"], "n": x["principal"]["n"], "ic95": None, "p": None, "magnitud_referencia": x["diagnosticos"]["magnitud_referencia"],
                  "multiverso": x["multiverso"]}
        diag[q] = x["diagnosticos"]
    dv, dp = v["diagnosticos"], p["diagnosticos"]
    diag["pruebas"] = {
        "superadas": ["Q6-p: placebo con ΔY retardado pequeño (%s)" % f(dp["placebo_dy_retardado"]["beta"]), "Q6-p: sin grandes ciudades, mismo signo (%s)" % f(dp["sin_grandes_ciudades"]["beta"]),
                      "Q6-v y Q6-p: control negativo (log población) cercano a 0 (%s)" % f(dv["control_negativo_log_poblacion"]["beta"])],
        "fallidas": ["Q6-v: placebo con ΔY retardado de signo opuesto y mayor tamaño que el efecto (%s frente a %s)" % (f(dv["placebo_dy_retardado"]["beta"]), f(v["principal"]["beta_por_punto"])),
                     "Q6-v: la estimación principal tiene signo opuesto a la referencia (-0,07 por punto); las bajadas (%s) tienen el signo de la referencia y las subidas son casi nulas (%s): lectura no unívoca" % (f(dv["bajadas"]["beta"]), f(dv["subidas"]["beta"])),
                     "Q6-v/Q6-p: el diseño tiene 14 cambios en 8 CCAA, concentrados en 2012-2013: en 2012 no hay estables que cumplan la exclusión de anticipación"],
        "no_evaluables": ["inferencia por aleatorización del calendario (dCDH NO APTO): sin p-valor ni IC", "Honest DiD (no validado)", "Cinelli-Hazlett (requiere t válido)",
                          "Oster (no aplica al Wald-DID)", "TOST (sin SE)"]}
    pv = [{"id": "Q6-v|principal", "p": None, "rama": "diseños", "nota": "dCDH con aleatorización NO APTO"}, {"id": "Q6-p|principal", "p": None, "rama": "diseños", "nota": "dCDH con aleatorización NO APTO"}]
    res = base("Q6: fiscalidad de la compra (tipo general del ITP): Q6-v compraventas, Q6-p valor tasado",
               "data/processed/v16/entrenamiento: base_precio (compraventas y valor tasado provinciales anuales), base_poblacion; output/v16/f1/intervenciones.csv (calendario ITP)",
               {"Q6-v": v["principal"]["n"], "Q6-p": p["principal"]["n"]},
               "Wald-DID de de Chaisemartin-D'Haultfœuille (dosis continua, no absorbente) sobre panel anual provincial 2011-2024; referencia TWFE. Solo puntual.", est, diag,
               [CONSIGNA, "Compraventas = total de vivienda (sin desglose usada/nueva en el panel provincial); ver D2.", "Calendario: 14 cambios del tipo general en 8 CCAA no selladas (2012-2024).",
                "La variante «fecha adelantada un año» coincide con el placebo de ΔY retardado por construcción."], pv)
    cal = r["calendario_cambios"]
    H = [C.hecho("V16-Q6-v-beta", "Q6-v: asociación del Δlog compraventas con el cambio del tipo general del ITP (Wald-DID dCDH, por punto)", v["principal"]["beta_por_punto"], v["multiverso"]["min"], v["multiverso"]["max"],
                 "log por punto de tipo", "2011-2024", "34 provincias con cambio en 8 CCAA", "Ministerio de Hacienda (tipos); INE ETDP", "q6-v", "q6", "2024"),
         C.hecho("V16-Q6-p-beta", "Q6-p: asociación del Δlog valor tasado con el cambio del tipo general del ITP (Wald-DID dCDH, por punto)", p["principal"]["beta_por_punto"], p["multiverso"]["min"], p["multiverso"]["max"],
                 "log por punto de tipo", "2011-2024", "33 provincias con cambio en 7-8 CCAA", "Ministerio de Hacienda (tipos); MIVAU valor tasado", "q6-p", "q6", "2024"),
         C.hecho("V16-Q6-v-placebo", "Q6-v: placebo con ΔY retardado un año", dv["placebo_dy_retardado"]["beta"], None, None, "log por punto de tipo", "2011-2024", "34 provincias", "idem", "q6-v", "q6", "2024"),
         C.hecho("V16-Q6-cambios", "Q6: número de cambios del tipo general del ITP en el calendario de entrenamiento", len(cal), None, None, "cambios", "2011-2024", "8 CCAA no selladas", "Ministerio de Hacienda, Tributación Autonómica (secundaria)", "q6-calendario", "q6", "2024")]
    inf = f"""# Q6 · Fiscalidad de la compra: tipo general del ITP (V16, fase 6)

**Capa C4, descriptiva. {CONSIGNA}** Datos de entrenamiento; desviaciones D2. Registro: output/v16/q6/registro.csv.

## Resultado (dCDH, dosis continua, por punto de tipo; sin p-valor ni IC: aleatorización NO APTA)
| Resultado | Estimación | Referencia de la adenda | Rango del multiverso (8) | Con el mismo signo |
|---|---|---|---|---|
| Q6-v log compraventas (N = {v['principal']['n']}) | {f(v['principal']['beta_por_punto'])} | -0,07 | {f(v['multiverso']['min'])} a {f(v['multiverso']['max'])} | {pct(v['multiverso']['proporcion_mismo_signo'], 0)} |
| Q6-p log valor tasado (N = {p['principal']['n']}) | {f(p['principal']['beta_por_punto'])} | -0,01 | {f(p['multiverso']['min'])} a {f(p['multiverso']['max'])} | {pct(p['multiverso']['proporcion_mismo_signo'], 0)} |

TWFE de referencia: Q6-v {f(dv['twfe_referencia']['beta'])}; Q6-p {f(dp['twfe_referencia']['beta'])}. Subidas/bajadas por separado: Q6-v {f(dv['subidas']['beta'])} / {f(dv['bajadas']['beta'])}; Q6-p {f(dp['subidas']['beta'])} / {f(dp['bajadas']['beta'])}.

## Pruebas
- Superadas: {'; '.join(diag['pruebas']['superadas'])}.
- Fallidas: {'; '.join(diag['pruebas']['fallidas'])}.
- No evaluables: {'; '.join(diag['pruebas']['no_evaluables'])}.
- E-value del punto: Q6-v {f(dv['e_value_punto'], 2)}; Q6-p {f(dp['e_value_punto'], 2)}. Moran de residuos TWFE: {f(dv['moran_residuos_twfe_prov']['I'], 3)} / {f(dp['moran_residuos_twfe_prov']['I'], 3)}.

## Regla de hallazgo
(a) sin p-valor propio; (b) magnitud numérica disponible, pero sin SE válido los errores S y M no son evaluables; (c) pendiente. **Sin hallazgo.** Q6-v: signo opuesto a la referencia, con un placebo mayor que el efecto: no se interpreta. Q6-p: signo y orden de magnitud cercanos a la referencia (razón {f(dp['razon_estimacion_sobre_referencia'], 2)}), solo puntual. No hay conclusión publicada de la 1.0 sobre el ITP: sin contradicción.

## Fichas reproducibles
Comando: `python src/v16/q6_itp.py && python src/v16/qb_informe.py`.
- <a id="q6-v"></a>**q6-v.** Wald-DID = Σ_t Σ_{{switchers}}(Δlog compraventas_ut − media de estables) / Σ Δtipo; switchers = provincias de CCAA con cambio del tipo general en el año de efecto; estables = sin cambio en t ni t+1; CCAA 01, 06, 07, 08, 09, 10, 11, 12; 2012-2024 en diferencias.
- <a id="q6-p"></a>**q6-p.** Igual con log valor tasado provincial (38 provincias, sin Cantabria).
- <a id="q6-calendario"></a>**q6-calendario.** {len(cal)} cambios del tipo general (mínimo de la escala cuando hay escala) 2011-2024 en output/v16/f1/intervenciones.csv; fechas en su mayoría aproximadas al 1 de enero; año de efecto.
"""
    C.volcar(O / "q6/resultado.json", res)
    C.volcar(O / "q6/hechos.json", H)
    (O / "q6/informe.md").write_text(inf, encoding="utf-8")
    return res


if __name__ == "__main__":
    for fn in (q3, q4, q6):
        fn()
    print("ok")
