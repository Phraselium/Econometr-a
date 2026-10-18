"""V16 fase 6 · salidas (resultado.json, hechos.json, informe.md) de Q1, Q2, Q7 y Q8 a partir de los *_detalle.json.

Todo es C4 (asociación o descriptivo), pendiente de evaluación sellada; sin lenguaje causal. Uso: python3 src/v16/q_salidas.py
"""
from __future__ import annotations

import json
import math
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from src.v16 import q_comun as Q

OUTD = ROOT / "output" / "v16"
FECHA = Q.CORTE
HERR = {  # veredictos de output/v16/montecarlo/veredictos.csv
    "sdid_conley_taber": "APTO solo en el escenario A (tamaño 0,0575, límite superior)",
    "cs_webb": "NO APTO (tamaño 0,0655; cobertura 0,9015) → solo descriptivo",
    "did_intensidad_webb": "NO APTO (Q2a: tamaño 0,142; Q2c: 0,0975) → solo descriptivo",
    "blp_gates": "NO APTO (tamaño 0,005; cobertura 0,9885) → solo descriptivo",
    "bh_jerarquico": "NO APTO; alternativa Benjamini-Yekutieli APTA (la aplica el orquestador)",
}


def f(x, d=3):
    if x is None:
        return "n/d"
    return f"{x:.{d}f}".replace(".", ",")


def pc(x, d=1):
    return f(100 * x, d) + " %"


def load(q):
    return json.loads((OUTD / q / f"{q}_detalle.json").read_text(encoding="utf-8"))


def hecho(i, q, indicador, valor, mn, mx, unidad, periodo, cobertura, fuentes, ancla, nota=""):
    return {"id": f"V16-{q.upper()}-{i}", "indicador": indicador, "valor": valor, "min": mn, "max": mx, "unidad": unidad, "periodo": periodo,
            "cobertura": cobertura, "fuentes": fuentes, "capa": "C4", "fecha_dato": nota or FECHA,
            "ficha": f"output/v16/{q}/informe.md#{ancla}"}


def resultado_base(q, pregunta, datos, N, metodo, estimacion, diag, herramientas, notas, extra=None):
    r = {"rama": f"v16/{q}", "pregunta": pregunta, "capa": "C4", "datos": datos, "N": N, "metodo": metodo, "estimacion": estimacion, "ic95": None,
         "p_ajustado": {"metodo": "sin p-valor: las herramientas de inferencia del diseño son NO APTAS o no estimables; el control Benjamini-Yekutieli lo aplica el orquestador", "valores": []},
         "p_valores": [], "nivel_evidencia": "DESCRIPTIVO", "diagnosticos": diag, "herramientas": herramientas,
         "fuera_muestra": {"modelo": "no aplica (no es predicción)", "rmse": None, "dm_vs_ar4": None},
         "pendiente_sellada": True,
         "regla_hallazgo": {"a_q_menor_0_10": "no evaluable (sin p-valor)", "b_error_S_M": "no evaluable (sin errores típicos)", "c_sellada": "pendiente",
                            "resultado": "ni hallazgo ni pista confirmada: estimación puntual descriptiva C4"},
         "notas": notas}
    if extra:
        r.update(extra)
    return r


def d(prueba, estado, detalle):
    return {"prueba": prueba, "estado": estado, "detalle": detalle}


# ---------------------------------------------------------------- Q1
def salidas_q1():
    j = load("q1")
    a, b, c = j["q1a"], j["q1b"], j["q1c"]
    s = c["sensibilidad_corte"]
    diag = [
        d("Q1b · periodo posterior al tratamiento en el entrenamiento", "fallida", f"primera entrada en vigor fuera de Cataluña {b['primer_efecto_fuera_cataluna']}; último año de SERPAVI {b['ultimo_anio_serpavi_entrenamiento']}; zonas vigentes fuera de Cataluña antes de 2025: {b['zt_vigente_fuera_cataluna_antes_2025']}"),
        d("Q1b · potencia", "fallida", "MDE 7,1 % frente a −0,75 % de referencia (SERPAVI es stock): sin potencia"),
        d("Q1b · balance tratados/donantes", "informativa (sin umbral pre-registrado)", "renta ADRH 36.639 frente a 25.974 €; población 160.845 frente a 12.133 (tratados 8, donantes 1.201); exposición al tipo variable no está en disco"),
        d("Q1c · pretendencias (coeficientes previos del estudio de eventos)", "informativa (sin umbral pre-registrado)", f"media de los coeficientes e∈[−8,−2] = {f(c['pretendencia']['media_coef_pre_evento'])}; |media| de las ATT(g,t) previas = {f(c['pretendencia']['media_abs_pre'])}"),
        d("Q1c · Honest DiD", "no evaluable", "no validado en la fase 5 (no figura en veredictos.csv)"),
        d("Q1c · placebo de fecha (cohortes 8 trimestres antes)", "informativa (sin umbral pre-registrado)", f"estimación placebo {f(c['att_placebo_fecha'], 4)} frente a {f(c['att_global'])} del principal"),
        d("Q1c · exclusión de grandes ciudades", "informativa", f"sin Barcelona, València, Sevilla y Málaga: {f(c['att_global_sin_grandes_ciudades'])} (mismo signo)"),
        d("Q1c · balance tratadas/no tratadas", "informativa (sin umbral pre-registrado)", "diferencias estandarizadas: " + "; ".join(f"{x['variable']} {f(x['dif_estandarizada'], 2)}" for x in c["balance"])),
        d("Q1c · Oster (δ, β=0, Rmax = 1,3 R²)", "fallida" if (s["oster"]["delta"] is not None and s["oster"]["delta"] < 1) else "superada", f"δ = {f(s['oster']['delta'])} (δ < 1 = frágil)"),
        d("Q1c · Cinelli-Hazlett RV_q=1", "superada" if not s["cinelli_hazlett_frágil_si_RV_menor_0_05"] else "fallida", f"RV = {f(s['cinelli_hazlett_RV_q1'])} (frágil si < 0,05)"),
        d("Q1c · E-value (puntual)", "informativa (sin umbral)", f"{f(s['e_value_puntual'], 2)}"),
        d("Q1c · Moran de los residuos (cruce provincial)", "informativa", f"I = {f(c['moran_residuos']['I'])}, p de permutación (diagnóstico) = {f(c['moran_residuos']['p_permutacion_diagnostico'])}"),
        d("Q1c · heterocedasticidad (Breusch-Pagan)", "informativa", f"LM = {f(c['breusch_pagan']['LM'])}, p = {f(c['breusch_pagan']['p_diagnostico'])}"),
        d("Q1c · ruptura (Bai-Perron) en la brecha tratadas − no tratadas", "informativa", f"{c['bai_perron_brecha'].get('n_bkps')} rupturas, trimestres {c['bai_perron_brecha'].get('fechas')}: la brecha cambia de régimen antes del primer tratamiento (2024T1)"),
        d("Controles negativos (población 65+, IPC general provincial)", "no evaluable", "no están en el entrenamiento"),
        d("Raíces unitarias / cointegración con dependencia transversal", "no aplica", "diseños en diferencias sobre ventana corta"),
        d("BLP/GATES de Q1", "no evaluable", "Q1b sin periodo posterior; Q1c tiene 8 tratadas frente a 5 moderadores; herramienta NO APTA"),
    ]
    est = {"Q1a_tasa_declaracion_elegibles": a["tasa_declaracion_elegibles"], "Q1a_tasa_declaracion_no_elegibles": a["tasa_declaracion_no_elegibles"],
           "Q1b": "no estimable en el entrenamiento; pendiente de la evaluación sellada",
           "Q1c_estimador_CS_global_dlog": c["att_global"], "Q1c_sin_grandes_ciudades": c["att_global_sin_grandes_ciudades"], "Q1c_placebo_fecha": c["att_placebo_fecha"]}
    notas = ("Q1c incluye Cataluña (solapa con H1/H2 de V15, declarado). Cohortes 2024T1 (Cataluña) y 2025T2-T4 (Euskadi, Galicia): las de 2025 tienen entre 1 y 4 trimestres posteriores. "
             "La cohorte de Álava/Gipuzkoa/Bizkaia/A Coruña se fecha con base_regulacion (zt_vigente); intervenciones.csv recoge una fecha de 2025-01-31 para un municipio de Gipuzkoa que base_regulacion no lleva. "
             "Magnitud de referencia de Q1c: ninguna comparable → condición (b) no se cumple. Q1a no tiene resultado en entrenamiento. Multiverso de Q1c: solo la principal y la exclusión del punto 14 (D3).")
    res = resultado_base("q1", "¿Qué diferencia hay, en el entrenamiento, entre los mercados con y sin zonas tensionadas declaradas (Q1a diagnóstico, Q1b SDID, Q1c compraventas provinciales)?",
                         "data/processed/v16/entrenamiento (base_alquiler SERPAVI, base_precio compraventas, base_regulacion BOE); sin muestra sellada",
                         {"Q1a_municipios": a["n_municipios"], "Q1b_tratados_fuera_Cataluna": b["tratados_fuera_cataluna_en_panel_serpavi"], "Q1c_provincias": c["n_provincias"], "Q1c_tratadas": c["n_tratadas"]},
                         "Q1a recuento de elegibilidad (art. 18); Q1b SDID con Conley-Taber (no estimable); Q1c Callaway-Sant'Anna sin regresores, puntual",
                         est, diag, {k: HERR[k] for k in ("sdid_conley_taber", "cs_webb", "blp_gates", "bh_jerarquico")}, notas,
                         extra={"q1b_veredicto": b["veredicto"], "multiverso_declarado": {"Q1a": "sin resultado", "Q1b": "no estimable", "Q1c": "2 especificaciones (principal + punto 14)"}})
    Q.jdump(res, OUTD / "q1" / "resultado.json")
    cob = f"{c['n_provincias']} provincias de entrenamiento ({c['n_tratadas']} con zona vigente)"
    H = [
        hecho(1, "q1", "Municipios tratados fuera de Cataluña con panel SERPAVI en el entrenamiento", b["tratados_fuera_cataluna_en_panel_serpavi"], None, None, "municipios", "2011-2024", "entrenamiento (CCAA no selladas)", "BOE zonas tensionadas; SERPAVI (MIVAU)", "v16-q1-1"),
        hecho(2, "q1", "Primer inicio de zona vigente fuera de Cataluña (Q1b sin periodo posterior: último año SERPAVI 2024)", 2025.0, None, None, "año", "2025-2026", "entrenamiento", "BOE; intervenciones.csv V16", "v16-q1-1"),
        hecho(3, "q1", "Diferencia media de compraventas, provincias con zona vigente frente a nunca tratadas (estimador CS, descriptivo)", c["att_global"], min(c["att_global"], c["att_global_sin_grandes_ciudades"]), max(c["att_global"], c["att_global_sin_grandes_ciudades"]), "Δlog", "2019T1-2026T2", cob, "MIVAU transacciones; BOE", "v16-q1-3"),
        hecho(4, "q1", "Misma comparación en un placebo de fecha (8 trimestres antes)", c["att_placebo_fecha"], None, None, "Δlog", "2019T1-2023T4", cob, "MIVAU transacciones; BOE", "v16-q1-4"),
        hecho(5, "q1", "Diferencia de la cohorte de Cataluña (2024T1)", c["att_por_cohorte"]["2024Q1"], None, None, "Δlog", "2024T1-2026T2", "4 provincias catalanas frente a 33 nunca tratadas", "MIVAU transacciones; BOE", "v16-q1-5"),
        hecho(6, "q1", "Tasa de declaración de zona entre municipios que superan el criterio de precio del art. 18", a["tasa_declaracion_elegibles"], a["tasa_declaracion_no_elegibles"], a["tasa_declaracion_elegibles"], "proporción", "SERPAVI 2018-2023", f"{a['n_municipios']} municipios de entrenamiento", "SERPAVI VC; IPC (INE); BOE", "v16-q1-6"),
        hecho(7, "q1", "Municipios de entrenamiento que superan IPC + 3 p.p. en 2018-2023 (SERPAVI)", a["n_elegibles"], None, None, "municipios", "2018-2023", f"{a['n_municipios']} municipios", "SERPAVI VC; IPC (INE)", "v16-q1-6"),
    ]
    Q.jdump(H, OUTD / "q1" / "hechos.json")
    inf = f"""# V16 · Q1 · Zonas tensionadas (grupo A, entrenamiento)

**Capa C4, pendiente de evaluación sellada.** Todo es asociación o descriptivo; sin lenguaje causal. Datos: {res['datos']}. Fecha de corte {FECHA}.

## Qué se ha hecho
- **Q1a (diagnóstico descriptivo).** Sin RD ni efecto: su resultado solo existe en la muestra sellada. Se cuenta la elegibilidad por el criterio de precio del art. 18.
- **Q1b (SDID).** Se comprueba si hay periodo posterior al tratamiento en el entrenamiento.
- **Q1c (Callaway-Sant'Anna).** Herramienta: {HERR['cs_webb']}. Estimación puntual, sin p-valor ni IC.
- **BLP/GATES.** No estimable para Q1.

## Resultados
<a id="v16-q1-1"></a>
**Q1b: no estimable en el entrenamiento; pendiente de la evaluación sellada.**
- Tratados fuera de Cataluña con panel SERPAVI: {b['tratados_fuera_cataluna_en_panel_serpavi']} ({b['tratados_en_panel_completo_2019_2024']} con panel completo 2019-2022 y 2024).
- Primer inicio de zona: {b['primer_efecto_fuera_cataluna']}. Último año de SERPAVI en el entrenamiento: {b['ultimo_anio_serpavi_entrenamiento']}. Ninguna otra ventana (no se inventa).
- La inferencia de Conley-Taber solo es APTA en el escenario A, con un tamaño de 0,0575 (límite superior de [0,04; 0,06]). Potencia: MDE 7,1 % frente a −0,75 %.

<a id="v16-q1-3"></a>
**Q1c.** Cohortes: {', '.join(f'{p} {g}' for p, g in sorted(c['cohortes'].items()))}.
- Estimador CS global (Δlog de compraventas, tratadas frente a nunca tratadas, base g−1): **{f(c['att_global'])}** (≈ {pc(math.exp(c['att_global']) - 1)}); sin grandes ciudades: {f(c['att_global_sin_grandes_ciudades'])}.
- Por cohorte: {', '.join(f'{g} {f(v)}' for g, v in c['att_por_cohorte'].items())}. Las cohortes de 2025 tienen pocos trimestres posteriores.
- Estudio de eventos (e = −8…+6): {', '.join(f'{k}: {f(v)}' for k, v in c['evento'].items())}. Los coeficientes previos (e = −8, −7, −2) tienen el mismo orden de magnitud que los posteriores: no hay separación nítida entre la diferencia posterior y el ruido previo.
- Magnitud de referencia: ninguna comparable, así que la condición (b) no se cumple. Sin errores típicos no hay tipo S ni M.

<a id="v16-q1-4"></a>
**Placebo de fecha:** {f(c['att_placebo_fecha'], 4)} (cohortes adelantadas 8 trimestres; datos hasta el tratamiento real).

<a id="v16-q1-5"></a>
**Cataluña (2024T1):** {f(c['att_por_cohorte']['2024Q1'])}. Solapa con H1/H2 de V15 (declarado); no se contrasta con ellas.

<a id="v16-q1-6"></a>
**Q1a:** IPC acumulado 2018-2023 {pc(a['ipc_acumulado_2018_2023'])}; umbral = ln(1+IPC+0,03) = {f(a['umbral_log'])}.
- De {a['n_municipios']} municipios con SERPAVI VC en 2018 y 2023, {a['n_elegibles']} lo superan y {a['n_en_banda_10pts']} están a ±10 puntos logarítmicos.
- Tasa de declaración: {pc(a['tasa_declaracion_elegibles'])} entre elegibles y {pc(a['tasa_declaracion_no_elegibles'])} entre no elegibles ({a['declarados_elegibles']} y {a['declarados_no_elegibles']} declarados).

## Diagnósticos (superados y fallidos)
| Prueba | Estado | Detalle |
|---|---|---|
""" + "\n".join(f"| {x['prueba']} | {x['estado']} | {x['detalle']} |" for x in diag) + f"""

## Límites
{notas}
Resumen para el control de falsos descubrimientos: lista de p-valores vacía (ninguna prueba con inferencia apta). Ficha reproducible: `python3 src/v16/q1_zonas.py` (SEED=20261010); entradas en data/processed/v16/entrenamiento (base_precio, base_alquiler, base_regulacion, base_macro, renta_parque, base_poblacion, alquiler_turismo); salidas en output/v16/q1/ (q1c_att_gt.csv, q1c_evento.csv, q1a_elegibilidad.csv, q1b_balance.csv, registro.csv).
"""
    (OUTD / "q1" / "informe.md").write_text(inf, encoding="utf-8")


# ---------------------------------------------------------------- Q2
def salidas_q2():
    j = load("q2")
    a, b, c = j["q2a"], j["q2b"], j["q2c"]
    sa, sc = a["sensibilidad"], c["sensibilidad"]
    ev = a["evento_base_2019"]
    diag = [
        d("Q2a · pretendencias (estudio de eventos, base 2019)", "informativa (sin umbral pre-registrado)", "coeficientes 2012-2018: " + ", ".join(f"{k} {f(v, 4)}" for k, v in ev.items() if int(k) < 2019) + f"; pendiente lineal previa {f(a['pendiente_coef_pre'], 5)}/año"),
        d("Q2a · Honest DiD", "no evaluable", "no validado en la fase 5"),
        d("Q2a · placebo de fecha (post falso 2016-2019 frente a 2012-2015)", "informativa", f"{f(a['placebo_fecha'], 4)} por DT frente a {f(a['beta_por_DT'], 4)} del principal"),
        d("Q2a · exclusión de grandes ciudades", "informativa", f"{f(a['beta_sin_grandes_ciudades'], 4)} (mismo signo)"),
        d("Q2a · Oster", "superada" if sa["oster"]["delta"] is not None and sa["oster"]["delta"] >= 1 else "fallida", f"δ = {f(sa['oster']['delta'], 2)}"),
        d("Q2a · Cinelli-Hazlett", "superada" if not sa["cinelli_hazlett_frágil_si_RV_menor_0_05"] else "fallida", f"RV_q=1 = {f(sa['cinelli_hazlett_RV_q1'])}"),
        d("Q2a · E-value (puntual)", "informativa", f"{f(sa['e_value_puntual'], 2)}"),
        d("Q2a · Moran de residuos", "informativa", f"I = {f(a['moran_residuos']['I'])}, p diagnóstico = {f(a['moran_residuos']['p_permutacion_diagnostico'])}"),
        d("Q2a · Breusch-Pagan", "informativa", f"p = {f(a['breusch_pagan']['p_diagnostico'])}"),
        d("Q2a · ruptura (Bai-Perron) brecha tercil alto − bajo", "informativa", f"{a['bai_perron_brecha_tercil'].get('n_bkps')} rupturas: {a['bai_perron_brecha_tercil'].get('fechas')}"),
        d("Q2a · balance (terciles de exposición)", "informativa", "; ".join(f"{x['variable']} {f(x['dif_estandarizada'], 2)}" for x in a["balance_terciles"])),
        d("Q2a · F efectivo de Montiel Olea-Pflueger / AKM / Rotemberg", "no aplica", "shift-share retirado (no hay pernoctaciones por país en disco): forma reducida"),
        d("Q2c · Oster", "superada" if sc["oster"]["delta"] is not None and sc["oster"]["delta"] >= 1 else "fallida", f"δ = {f(sc['oster']['delta'], 2)}"),
        d("Q2c · Cinelli-Hazlett", "superada" if not sc["cinelli_hazlett_frágil_si_RV_menor_0_05"] else "fallida", f"RV_q=1 = {f(sc['cinelli_hazlett_RV_q1'])}"),
        d("Q2c · exposición adelantada (placebo temporal)", "informativa", f"{f(c['placebo_exposicion_adelantada'], 4)} por DT"),
        d("Q2c · Moran (por provincia, aproximado)", "informativa", f"I = {f(c['moran_residuos_por_provincia']['I'])}, p diagnóstico = {f(c['moran_residuos_por_provincia']['p_permutacion_diagnostico'])}"),
        d("Q2c · Breusch-Pagan", "fallida (heterocedasticidad)", f"p = {c['breusch_pagan']['p_diagnostico']:.1e}"),
        d("Q2c · exclusión de grandes ciudades", "informativa", f"{f(c['beta_sin_grandes_ciudades'], 4)}"),
        d("Controles negativos (población 65+, IPC general provincial)", "no evaluable", "no están en el entrenamiento"),
        d("Raíces unitarias / cointegración con dependencia transversal", "no aplica", "diferencias sobre ventanas cortas"),
        d("BLP/GATES (adenda, punto 13)", "no evaluable como prueba", "herramienta NO APTA: solo puntuales, descriptivos (ver detalle)"),
    ]
    est = {"Q2a_beta_por_DT_log_exposicion": a["beta_por_DT"], "Q2a_elasticidad": a["elasticidad"], "Q2a_referencia_por_DT": a["referencia_b_por_DT"],
           "Q2c_beta_por_DT": c["beta_por_DT"], "Q2c_referencia_por_DT": c["referencia_b_por_DT"], "Q2b_mediana_robustez": b["mediana"]}
    notas = ("Todo es asociación en forma reducida (C4). Solapes declarados: V9-D2 y H3. La conclusión publicada sobre vivienda turística es «no concluyente»: este resultado no la cambia. "
             "Q2c se lee como robustez de H3. Q2b es solo robustez, con dosis reconstruida (sesgo de supervivencia). El multiverso de 32 especificaciones de Q2a era del shift-share retirado y no se ejecuta (D3). "
             "Sin errores típicos no se calculan tipo S ni M: la condición (b) no es evaluable. Pernoctaciones por país y municipio: tarea del autor.")
    res = resultado_base("q2", "¿Qué asociación hay, en el entrenamiento, entre la exposición a vivienda turística y la evolución del alquiler (Q2a provincial, Q2b Andalucía solo robustez, Q2c IPVA municipal)?",
                         "data/processed/v16/entrenamiento (alquiler_turismo INE-VUT, base_alquiler IPC y IPVA-TAM, alquiler_turismo_terceros OpenRTA solo robustez); sin muestra sellada",
                         {"Q2a_provincias": 41, "Q2a_obs": a["n_obs"], "Q2c_municipios": c["n_municipios"], "Q2c_obs": c["n_obs"]},
                         "Q2a DiD de intensidad en forma reducida (puntual); Q2b robustez; Q2c efectos fijos de municipio y año (puntual); BLP/GATES descriptivo",
                         est, diag, {k: HERR[k] for k in ("did_intensidad_webb", "blp_gates", "bh_jerarquico")}, notas,
                         extra={"blp_gates_descriptivo": {"Q2a": a["blp_gates"], "Q2c": c["blp_gates"]}, "multiverso_Q2c": c["multiverso"], "multiverso_Q2b": {"n": b["n_especificaciones"], "mediana": b["mediana"], "mismo_signo": b["proporcion_mismo_signo_que_la_primera"]}})
    Q.jdump(res, OUTD / "q2" / "resultado.json")
    cobA = "41 provincias de entrenamiento (Ceuta y Melilla incluidas)"
    ests = list(b["estimaciones"].values())
    H = [
        hecho(1, "q2", "Q2a · coeficiente DiD de intensidad (log IPC alquiler por DT del log de la exposición INE-VUT 2020-08)", a["beta_por_DT"], min(a["beta_por_DT"], a["beta_sin_grandes_ciudades"], a["beta_con_controles"]), max(a["beta_por_DT"], a["beta_sin_grandes_ciudades"], a["beta_con_controles"]), "Δlog por DT", "2017-2019 frente a 2022-2025", cobA, "INE IPC alquiler; INE viviendas turísticas", "v16-q2-1"),
        hecho(2, "q2", "Q2a · magnitud de referencia (0,04 × DT del log de la exposición)", a["referencia_b_por_DT"], None, None, "Δlog por DT", "2017-2025", cobA, "literatura L2/P5 (docs/v16/literatura.md)", "v16-q2-1"),
        hecho(3, "q2", "Q2a · placebo de fecha", a["placebo_fecha"], None, None, "Δlog por DT", "2012-2019", cobA, "INE IPC alquiler; INE viviendas turísticas", "v16-q2-2"),
        hecho(4, "q2", "Q2c · coeficiente (Δlog IPVA-TAM municipal por DT del % de vivienda turística)", c["beta_por_DT"], c["multiverso"]["min"], c["multiverso"]["max"], "Δlog por DT", "2021-2024", f"{c['n_municipios']} municipios de entrenamiento", "IPVA-TAM (MIVAU/INE); INE viviendas turísticas", "v16-q2-3"),
        hecho(5, "q2", "Q2c · magnitud de referencia (0,04 × DT del log de la exposición)", c["referencia_b_por_DT"], None, None, "Δlog por DT", "2021-2024", f"{c['n_municipios']} municipios", "literatura L2/P5", "v16-q2-3"),
        hecho(6, "q2", "Q2b · mediana de 8 especificaciones de robustez (Andalucía, dosis reconstruida)", b["mediana"], min(ests), max(ests), "Δlog por unidad de dosis", "2016-2024", "177 municipios (SERPAVI), 90 (IPVA)", "OpenRTA (terceros, agregado propio); SERPAVI; IPVA-TAM", "v16-q2-4"),
        hecho(7, "q2", "Q2a · GATES: pendiente del cuartil superior menos el inferior del CATE proxy (descriptivo)", a["blp_gates"]["GATES_cuartil4_menos_cuartil1"], None, None, "Δlog por DT", "2017-2025", "37 provincias con moderadores", "ADRH; padrón; Catastro/MIVAU", "v16-q2-5"),
    ]
    Q.jdump(H, OUTD / "q2" / "hechos.json")
    inf = f"""# V16 · Q2 · Vivienda turística (grupo A, entrenamiento)

**Capa C4, pendiente de evaluación sellada.** Asociaciones en forma reducida, sin lenguaje causal. Fecha de corte {FECHA}. Herramientas: {HERR['did_intensidad_webb']}; BLP/GATES {HERR['blp_gates']}. **Sin p-valor ni IC.**

<a id="v16-q2-1"></a>
## Q2a · DiD de intensidad (principal)
log IPC de alquiler provincial (media anual) ~ exposición × posterior + efectos fijos de provincia y año. Exposición: log del % de viviendas turísticas INE de 2020-08, estandarizado (DT del log = {f(a['dt_log_exposicion'])}). Pre 2017-2019, post 2022-2025, sin 2020-2021; N = {a['n_obs']}.
- Coeficiente: **{f(a['beta_por_DT'], 4)} por DT** (elasticidad {f(a['elasticidad'], 4)}). Referencia pre-registrada: {f(a['referencia_b_por_DT'], 4)} por DT (0,04 × DT del log). La estimación puntual es {f(a['beta_por_DT'] / a['referencia_b_por_DT'], 2)} veces la referencia.
- Sin grandes ciudades: {f(a['beta_sin_grandes_ciudades'], 4)}. Con controles (renta, población, extranjeros × posterior): {f(a['beta_con_controles'], 4)}; misma muestra sin controles: {f(a['beta_corto_misma_muestra'], 4)}.
- Estudio de eventos (base 2019): {', '.join(f'{k}: {f(v, 4)}' for k, v in ev.items())}.

<a id="v16-q2-2"></a>
**Placebo de fecha** (post falso 2016-2019): {f(a['placebo_fecha'], 4)} por DT.

<a id="v16-q2-3"></a>
## Q2c · exposición INE-VUT municipal frente al IPVA-TAM
Δlog IPVA-TAM ~ z(% VUT en nivel) + efectos fijos de municipio y año, 2021-2024 (especificación de la adenda, punto 3; corregida en K17); {c['n_municipios']} municipios, N = {c['n_obs']}.
- Coeficiente: **{f(c['beta_por_DT'], 4)} por DT** (referencia {f(c['referencia_b_por_DT'], 4)}). Variantes (log del nivel del IPVA; exposición en log; versión inicial con ambos en log; sin grandes ciudades; controles): {f(c['beta_variante_nivel'], 4)}; {f(c['beta_variante_dlog'], 4)}; {f(c['beta_variante_dlog_nivel'], 4)}; {f(c['beta_sin_grandes_ciudades'], 4)}; {f(c['beta_con_controles'], 4)}.
- Multiverso (6 especificaciones): mediana {f(c['multiverso']['mediana'], 4)}, rango [{f(c['multiverso']['min'], 4)}; {f(c['multiverso']['max'], 4)}], mismo signo que la principal en {pc(c['multiverso']['proporcion_mismo_signo_que_principal'], 0)}. Se lee como robustez de H3.

<a id="v16-q2-4"></a>
## Q2b · solo robustez (Andalucía)
Dosis = altas acumuladas de viviendas completas (OpenRTA, reconstruida con sesgo de supervivencia). {b['n_especificaciones']} especificaciones: mediana {f(b['mediana'], 5)}; mismo signo que la primera en {pc(b['proporcion_mismo_signo_que_la_primera'], 0)}. Sin inferencia.

<a id="v16-q2-5"></a>
## BLP/GATES (descriptivo, NO APTO)
- Q2a (n = {a['blp_gates']['n']}): pendiente media {f(a['blp_gates']['ATE_beta1_mediana'], 4)}; GATES por cuartil {[round(x, 4) if x is not None else None for x in a['blp_gates']['GATES_pendiente_por_cuartil_mediana']]}.
- Q2c (n = {c['blp_gates']['n']}): pendiente media {f(c['blp_gates']['ATE_beta1_mediana'], 4)}; GATES por cuartil {[round(x, 4) if x is not None else None for x in c['blp_gates']['GATES_pendiente_por_cuartil_mediana']]}.
- Moderadores: renta ADRH, población, cuota de extranjeros, obra nueva per cápita (y % VUT 2021 en Q2c; en Q2a coincide con la exposición). Subgrupos descriptivos C4.

## Diagnósticos (superados y fallidos)
| Prueba | Estado | Detalle |
|---|---|---|
""" + "\n".join(f"| {x['prueba']} | {x['estado']} | {x['detalle']} |" for x in diag) + f"""

## Límites
{notas}
Lista de p-valores para el control BY: vacía. Ficha reproducible: `python3 src/v16/q2_turismo.py` (SEED=20261010); entradas en data/processed/v16/entrenamiento; salidas en output/v16/q2/ (q2_detalle.json, registro.csv).
"""
    (OUTD / "q2" / "informe.md").write_text(inf, encoding="utf-8")


# ---------------------------------------------------------------- Q7
def salidas_q7():
    j = load("q7")
    pp = j["principal_log_alquiler_h5"]
    diag = [
        d("Q7a · umbrales placebo (31|32 y 39|40, ±3)", "informativa (sin umbral pre-registrado)", f"{f(j['placebos_umbral']['31'], 3)} y {f(j['placebos_umbral']['39'], 3)} frente a {f(pp['diferencia_en_discontinuidades'], 3)} del principal: del mismo orden"),
        d("Q7a · balance de covariables en el umbral (diferencia en discontinuidades)", "informativa", "; ".join(f"{k} {f(v, 3)}" for k, v in j["balance_diff_in_disc"].items())),
        d("Q7a · proporción de inquilinos en el umbral", "informativa", f"salto antes {f(j['proporcion_inquilinos']['salto_antes'])}, después {f(j['proporcion_inquilinos']['salto_despues'])}, diferencia {f(j['proporcion_inquilinos']['diferencia_en_discontinuidades'])}"),
        d("Q7a · densidad por edad (edad discreta)", "informativa", f"razón de hogares de edad 35/36: antes {f(j['densidad_edad']['antes']['razon_35_36'], 2)}, después {f(j['densidad_edad']['despues']['razon_35_36'], 2)}; McCrary no aplica con edad entera"),
        d("Q7a · Plan Estatal 2018-2021 con programa para menores de 35", "informativa (cambio de generosidad)", "sí: RD 106/2018, programa de ayuda a los jóvenes («menos de treinta y cinco años»); la diferencia en discontinuidades mide un cambio de generosidad, no un programa nuevo"),
        d("Q7a · anchos 0,5× y 2× del óptimo; rdrobust", "no aplica", "edad discreta de 11 valores: anchos de 3, 5 y 7 años declarados; sin rdrobust (en RD difuso/dif-en-disc no validado)"),
        d("Q7a · intervalo de Kolesár-Rothe", "no mostrado", "no se muestra ningún intervalo"),
        d("Q7a · sensibilidad a confusores (Oster, Cinelli-Hazlett, E-value)", "no evaluable", "sin errores típicos ni controles en el diseño de corte"),
        d("Q7a · exclusión de grandes ciudades e islas", "no aplica", "la ECV no lleva provincia (solo NUTS2)"),
    ]
    res = resultado_base("q7", "¿Cambió en el corte de 35 años la diferencia de alquiler pagado entre inquilinos de mercado, de 2018-2021 a 2023-2025 (Q7a, diferencia en discontinuidades)?",
                         "ECV transversal 2018-2021 y 2023-2025 (microdatos INE, data/raw; extracto en output/v16/q7); sin muestra sellada v6",
                         {"hogares_inquilinos_mercado": j["n_hogares_total"], "n_principal": pp["n"]},
                         "diferencia en discontinuidades lineal local, pesos DB090, anchos 3/5/7 años; sin intervalo",
                         {"principal_log_alquiler_h5": pp["diferencia_en_discontinuidades"], "equivalente_pct": j["porcentaje_equivalente_principal"], "cota_incidencia_pct": j["cota_incidencia_con_cobertura_plena_pct"]},
                         diag, {"kolesar_rothe": "no se muestra intervalo"}, "Descriptiva. La edad no asigna el bono por sí sola (renta, contrato, límites de precio). Potencia en el límite (MDE 13,2 % frente a cota de 13,9 %). El corte legal del Plan 2018-2021 (<35) difiere en un año del Bono (≤35). Sin magnitud de referencia numérica creíble → (b) no se cumple.",
                         extra={"plan_2018_2021": j["plan_2018_2021"], "multiverso": {"log_alquiler": j["multiverso_log_alquiler"], "alq_renta": j["multiverso_alq_renta"]}})
    Q.jdump(res, OUTD / "q7" / "resultado.json")
    H = [
        hecho(1, "q7", "Q7a · diferencia en discontinuidades del log del alquiler mensual en el corte de 35 años (2023-2025 frente a 2018-2021, ±5 años)", pp["diferencia_en_discontinuidades"], min(j["multiverso_log_alquiler"].values()), max(j["multiverso_log_alquiler"].values()), "Δlog", "2018-2021 / 2023-2025", f"{pp['n']} hogares inquilinos de mercado, sustentador 30-40 años", "INE ECV (microdatos)", "v16-q7-1"),
        hecho(2, "q7", "Q7a · salto del log del alquiler en el corte, antes (2018-2021)", pp["salto_antes"], None, None, "Δlog", "2018-2021", f"{pp['n_antes_T'] + pp['n_antes_noT']} hogares", "INE ECV", "v16-q7-1"),
        hecho(3, "q7", "Q7a · salto del log del alquiler en el corte, después (2023-2025)", pp["salto_despues"], None, None, "Δlog", "2023-2025", f"{pp['n_despues_T'] + pp['n_despues_noT']} hogares", "INE ECV", "v16-q7-1"),
        hecho(4, "q7", "Q7a · diferencia en discontinuidades en umbrales placebo (31|32 y 39|40)", j["placebos_umbral"]["31"], min(j["placebos_umbral"].values()), max(j["placebos_umbral"].values()), "Δlog", "2018-2025", "inquilinos de mercado, ±3 años", "INE ECV", "v16-q7-2"),
        hecho(5, "q7", "Q7a · diferencia en discontinuidades de la proporción de inquilinos de mercado en el corte", j["proporcion_inquilinos"]["diferencia_en_discontinuidades"], None, None, "proporción", "2018-2021 / 2023-2025", f"{j['proporcion_inquilinos']['n']} hogares 30-40 años", "INE ECV", "v16-q7-3"),
    ]
    Q.jdump(H, OUTD / "q7" / "hechos.json")
    inf = f"""# V16 · Q7a · Bono Alquiler Joven, diferencia en discontinuidades (grupo A, entrenamiento)

**Capa C4, descriptiva, pendiente de evaluación sellada.** Sin lenguaje causal ni intervalo (no se usa Kolesár-Rothe porque no se muestra ninguno). Fecha de corte {FECHA}.

## Diseño
Inquilinos de mercado (ECV), edad del sustentador principal entre 35−h y 35+h; corte entre 35 y 36 años; antes = 2018-2021, después = 2023-2025 (2022 fuera). Lineal local con pendientes por lado y periodo, pesos DB090. Anchos 3, 5 (principal) y 7; resultados: log del alquiler mensual (HH060) y alquiler anual / renta del hogar.

<a id="v16-q7-1"></a>
## Resultado
- Principal (±5, log alquiler): **{f(pp['diferencia_en_discontinuidades'])}** (≈ {f(j['porcentaje_equivalente_principal'], 1)} %). Salto antes {f(pp['salto_antes'])}, después {f(pp['salto_despues'])}. Hogares: antes {pp['n_antes_T'] + pp['n_antes_noT']}, después {pp['n_despues_T'] + pp['n_despues_noT']}.
- Anchos 3/5/7: {', '.join(f'{k.split("|")[1]}: {f(v)}' for k, v in j['multiverso_log_alquiler'].items())}. Alquiler / renta: {', '.join(f'{k.split("|")[1]}: {f(v)}' for k, v in j['multiverso_alq_renta'].items())} (proporción de la renta).
- Cota de incidencia con cobertura plena: {j['cota_incidencia_con_cobertura_plena_pct']} %; la potencia está en el límite (MDE 13,2 %).

<a id="v16-q7-2"></a>
**Umbrales placebo:** {', '.join(f'{k}|{int(k) + 1}: {f(v)}' for k, v in j['placebos_umbral'].items())}. Son del mismo orden que el principal: no hay separación entre señal y ruido.

<a id="v16-q7-3"></a>
**Proporción de inquilinos en el corte:** diferencia en discontinuidades {f(j['proporcion_inquilinos']['diferencia_en_discontinuidades'])}.

## Plan Estatal 2018-2021 (punto 8 de la adenda)
{j['plan_2018_2021']['fuente']} ({j['plan_2018_2021']['consultado']}): {j['plan_2018_2021']['requisito']}. **Sí tenía un programa para menores de 35 años**, así que {j['plan_2018_2021']['lectura']}.

## Diagnósticos (superados y fallidos)
| Prueba | Estado | Detalle |
|---|---|---|
""" + "\n".join(f"| {x['prueba']} | {x['estado']} | {x['detalle']} |" for x in diag) + f"""

## Límites
{res['notas']} Lista de p-valores: vacía. Ficha reproducible: `python3 src/v16/q7_bono.py` (ECV 2018-2025 en data/raw/v9/ine_microdatos/ecv y v16/renta_parque/ecv; extracto output/v16/q7/hogares_edad_28_42.parquet).
"""
    (OUTD / "q7" / "informe.md").write_text(inf, encoding="utf-8")


# ---------------------------------------------------------------- Q8
def salidas_q8():
    j = load("q8")
    c = j["cambio"]
    an = {r["anio"]: r for r in j["anual"]}
    diag = [
        d("Q8 · distinción UE / fuera de la UE", "no disponible", "la fuente MIVAU no la trae (adenda, R23); solo no residentes totales, extranjeros y españoles"),
        d("Q8 · muestra", "informativa", "agregado de 9 CCAA de entrenamiento + Ceuta y Melilla; el total nacional se descarta porque incluye las 8 CCAA de v6"),
        d("Q8 · comparación con el año anterior", "informativa", f"variación de la cuota un año antes: {f(c['dif_cuota_pp_referencia_ano_anterior'], 2)} pp frente a {f(c['dif_cuota_pp'], 2)} pp"),
        d("Q8 · pruebas de diseño (pretendencias, placebos, sensibilidad)", "no aplica", "descriptiva: sin estimador de efecto"),
    ]
    res = resultado_base("q8", "¿Cómo ha evolucionado la cuota de compras de no residentes (MIVAU) en el agregado de entrenamiento, antes y después de abril de 2025?",
                         "data/raw/mivau_transacciones_residencia.csv (nivel CCAA y ciudad autónoma, 9 CCAA de entrenamiento + Ceuta y Melilla); sin muestra sellada",
                         {"trimestres": 78, "periodo": f"{j['primer_trimestre']}-{j['ultimo_trimestre']}"},
                         "descriptivo: cuotas y niveles por trimestre y año, comparación de ventanas de 4 trimestres",
                         {"cuota_no_res_antes": c["cuota_no_res_antes"], "cuota_no_res_despues": c["cuota_no_res_despues"], "dif_pp": c["dif_cuota_pp"], "dif_pp_ano_anterior": c["dif_cuota_pp_referencia_ano_anterior"]},
                         diag, {}, "Descriptiva. Sin distinción UE/extra-UE: la cuota total de no residentes no identifica los visados de oro. No hay autorizaciones del OPI. Ninguna lectura causal sobre el fin de la golden visa.")
    Q.jdump(res, OUTD / "q8" / "resultado.json")
    H = [
        hecho(1, "q8", "Cuota de compras de no residentes sobre el total de transacciones (agregado de entrenamiento), 2025T2-2026T1", c["cuota_no_res_despues"], None, None, "% de las transacciones", "2025T2-2026T1", "9 CCAA de entrenamiento + Ceuta y Melilla", "MIVAU, Boletín Online (tabla 340101d0)", "v16-q8-1"),
        hecho(2, "q8", "Cuota de compras de no residentes, 2024T2-2025T1", c["cuota_no_res_antes"], None, None, "% de las transacciones", "2024T2-2025T1", "9 CCAA de entrenamiento + Ceuta y Melilla", "MIVAU, Boletín Online (tabla 340101d0)", "v16-q8-1"),
        hecho(3, "q8", "Variación de la cuota entre ambas ventanas", c["dif_cuota_pp"], c["dif_cuota_pp"], c["dif_cuota_pp_referencia_ano_anterior"], "puntos porcentuales", "2024T2-2026T1", "ídem (mínimo y máximo: este año y el anterior)", "MIVAU, Boletín Online", "v16-q8-2"),
        hecho(4, "q8", "Compras de no residentes (número), 2025", an[2025]["no_residentes_total"], an[2024]["no_residentes_total"], an[2022]["no_residentes_total"], "transacciones", "2025", "ídem (mínimo y máximo: 2024 y 2022)", "MIVAU, Boletín Online", "v16-q8-3"),
        hecho(5, "q8", "Cuota anual de compras de no residentes, 2025", an[2025]["cuota_no_res"], an[2025]["cuota_no_res"], an[2022]["cuota_no_res"], "% de las transacciones", "2025", "ídem (máximo: 2022)", "MIVAU, Boletín Online", "v16-q8-3"),
    ]
    Q.jdump(H, OUTD / "q8" / "hechos.json")
    inf = f"""# V16 · Q8 · Compras de no residentes (grupo A, entrenamiento)

**Capa C4, descriptiva, pendiente de evaluación sellada.** Sin estimador de efecto, sin p-valor y sin lectura causal. Fecha de corte {FECHA}. Fuente: {res['datos']}.

<a id="v16-q8-1"></a>
## Cuota de no residentes
- Ventana 2024T2-2025T1: **{f(c['cuota_no_res_antes'], 2)} %** ({int(c['compras_no_res_antes'])} de {int(c['compras_total_antes'])} transacciones).
- Ventana 2025T2-2026T1: **{f(c['cuota_no_res_despues'], 2)} %** ({int(c['compras_no_res_despues'])} de {int(c['compras_total_despues'])}).
- No residentes extranjeros: {f(c['cuota_no_res_extranjeros_antes'], 2)} % → {f(c['cuota_no_res_extranjeros_despues'], 2)} %.

<a id="v16-q8-2"></a>
## Variación
{f(c['dif_cuota_pp'], 2)} pp entre ventanas. La misma comparación un año antes (2023T2-2024T1 frente a 2024T2-2025T1) dio {f(c['dif_cuota_pp_referencia_ano_anterior'], 2)} pp: la cuota ya bajaba antes de abril de 2025. La descripción no separa los visados de oro (no hay distinción UE/extra-UE ni autorizaciones del OPI).

<a id="v16-q8-3"></a>
## Serie anual (agregado de entrenamiento)
| Año | No residentes | Total | Cuota (%) |
|---|---|---|---|
""" + "\n".join(f"| {y} | {int(an[y]['no_residentes_total'])} | {int(an[y]['total'])} | {f(an[y]['cuota_no_res'], 2)} |" for y in sorted(an) if y >= 2018) + f"""

2026 recoge solo dos trimestres. Provincias con más cuota en 2025: {', '.join(f"{p['territorio']} {f(p['2025'], 1)} %" for p in j['provincias_top5_cuota_2025'])} (output/v16/q8/q8_provincias.csv).

## Diagnósticos
| Prueba | Estado | Detalle |
|---|---|---|
""" + "\n".join(f"| {x['prueba']} | {x['estado']} | {x['detalle']} |" for x in diag) + f"""

## Límites
{res['notas']} Lista de p-valores: vacía. Ficha reproducible: `python3 src/v16/q8_no_residentes.py` sobre data/raw/mivau_transacciones_residencia.csv; salidas en output/v16/q8/.
"""
    (OUTD / "q8" / "informe.md").write_text(inf, encoding="utf-8")


def main():
    salidas_q1()
    salidas_q2()
    salidas_q7()
    salidas_q8()


if __name__ == "__main__":
    main()
