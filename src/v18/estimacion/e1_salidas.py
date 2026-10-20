"""V18 · fase 4 · E1 · salidas: tabla.csv, resultado.json (formato de CLAUDE.md + clasificacion_v18), hechos.json (cifras V18-E1-*) e informe.md.

Análisis V18; capa C4; pre-registro interno plan-replicacion-v18. Sin lenguaje causal en las cifras (check_v18) ni en el informe.
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
import _e2e8_comun as K  # noqa: E402
import e1_datos as D  # noqa: E402
import e1_estim as E  # noqa: E402

ALCANCE_TERRITORIAL = "sin lectura de datos"     # solo escribe salidas a partir de las tablas que recibe
FUENTES = ["SERPAVI (MIVAU), alquiler mediano por sección, 2011-2024", "Ajuntament de Barcelona, registro de viviendas de uso turístico (cortes trimestrales con coordenadas, data/manual/v11)",
           "INE, viviendas turísticas (INE-VUT) por sección; Censo 2021 (viviendas por sección)", "docs/v18/plan_replicacion.md + plan_replicacion_adenda.md (pre-registro interno plan-replicacion-v18)"]
I8 = "Clasificación provisional: falta I8 (réplica ciega, B6)"


def f(x, n=4):
    return "—" if x is None or (isinstance(x, (float, np.floating)) and not np.isfinite(x)) else f"{x:.{n}f}"


def md(df: pd.DataFrame) -> str:
    cols = list(df.columns)
    out = ["| " + " | ".join(str(c) for c in cols) + " |", "|" + "|".join("---" for _ in cols) + "|"]
    for r in df.itertuples(index=False):
        out.append("| " + " | ".join("—" if (isinstance(v, (float, np.floating)) and not np.isfinite(v)) or v is None else str(v) for v in r) + " |")
    return "\n".join(out)


def escribir(OUT: Path, B: pd.DataFrame, C: pd.DataFrame, gsf: pd.DataFrame, est: dict, ok: dict, pe: pd.DataFrame, out: dict, segundos: float, P: dict) -> None:
    tab = pd.DataFrame(out["filas"])
    tab.to_csv(OUT / "tabla.csv", index=False)
    R3, R4, PH = out["R3"], out["R4"], out["PH3"]
    r3, r4 = R3["r"], R4["r"]
    cl3, cl4 = out["clases"]["E1-R3"], out["clases"]["E1-R4"]
    holm = out["holm"]
    ev3, ev4 = R3["ev"], R4["ev"]
    sd3 = R3["sd"]
    aud = P["aud_hut"]
    n_att = P["n_atractivos"]
    cob = (f"769 de las 1.068 secciones de Barcelona (sin Gràcia, Sant Andreu y Nou Barris, sellados en V15 y V16), en 48 barrios; {B.cod_seccion.nunique()} con SERPAVI; "
           "viviendas del Censo 2021 como denominador")

    # ---------------------------------------------------------------- hechos
    H = []
    razon3 = r3["razon_ref"]
    nota3 = (f"Coeficiente de D_s × 1[t ≥ 2014] (dosis = HUT por 100 viviendas de 2018T2) con efectos fijos de sección y de año y los adelantos de 2011 y 2012 como control (base 2013); "
             f"media de β_k de 2014-2019; CR1 con t({r3['G'] - 1}) por barrio (p {f(r3['p_principal'], 4)}; Webb 9.999: {f(r3['_res']['p_webb'], 4)}); p corregido por el tamaño del Monte Carlo de este diseño "
             f"({f(out['tam']['R3'], 3)}) y tras Holm: {f(holm['E1-R3'], 4)}. Referencia de Segú (2018), 0,038 por pp (NO VERIFICADA): razón {f(razon3, 2)}, etiqueta "
             f"{'coherente' if r3['coherente_ref'] else 'no coherente'} (no interviene en la clase). Pretendencias (2011-2012): p = {f(ev3['pretend']['p'], 3)}. Tope SUGESTIVO de la especificación. "
             f"Lectura: asociación estimada; la clase describe el diseño, no el coeficiente. {I8}.")
    H.append(K.hecho("V18-E1-R3", "Coeficiente de la densidad de viviendas turísticas (HUT de 2018T2, por pp) × posterior (2014-2019) sobre el log del alquiler mediano SERPAVI por sección, Barcelona",
                     r3["coef_por_pp"], r3["ic95_por_pp"][0], r3["ic95_por_pp"][1], "log por pp de densidad HUT (por 100 viviendas)", "2011-2019", cob, FUENTES, cl3["clase"], nota3))
    nota4 = (f"Secciones a menos de 500 m de la Sagrada Família ({r4['n_tratadas']}) frente al anillo de 500-1.000 m ({r4['n_control']}), tratamiento desde 2014, base 2013, efectos fijos de sección y de año; "
             f"Webb por barrio con {r4['G']} clusters ({r4['G_tratados']} con tratadas), p = {f(r4['_res']['p_webb'], 4)}, p tras Holm {f(holm['E1-R4'], 4)}; IC95 por inversión del contraste de Webb. "
             f"Pretendencias (2011-2012): p = {f(ev4['pretend']['p'], 3)}. Sin referencia en la literatura (δ = 0,05): TOST: el IC90 de Webb ({f(cl4['info']['tost']['ic90'][0])}; {f(cl4['info']['tost']['ic90'][1])}) {'queda dentro de' if cl4['info']['tost']['equivalente'] else 'no queda dentro de'} ±0,05 (nulo {'acotado' if cl4['info']['tost']['equivalente'] else 'no acotado'}). Tope SUGESTIVO: un solo grupo tratado. Lectura: asociación estimada; "
             f"la clase describe el diseño, no el coeficiente. {I8}.")
    H.append(K.hecho("V18-E1-R4", "Coeficiente de estar a menos de 500 m de la Sagrada Família × posterior (2014-2019) sobre el log del alquiler mediano SERPAVI por sección, frente al anillo de 500-1.000 m",
                     r4["coef"], R4["ic_webb"][0], R4["ic_webb"][1], "log (diferencia entre radio y anillo, posterior frente a 2013)", "2011-2019",
                     f"{r4['n_tratadas']} secciones en el radio y {r4['n_control']} en el anillo, no selladas; el anillo conserva {R4['conteos']['anillo_no_sellado']} de {R4['conteos']['anillo_total']} secciones", FUENTES, cl4["clase"], nota4))
    H.append(K.hecho("V18-E1-P-H3", "Coeficiente del % de viviendas turísticas (INE-VUT, por desviación típica intra-sección) sobre el log del alquiler mediano SERPAVI por sección: especificación de H3 de V15 en la muestra V18",
                     PH["coef"], PH["ic95"][0], PH["ic95"][1], "log por DT intra-sección", PH["ventana"], f"{PH['n_secciones']} secciones de España no selladas, {PH['G']} municipios, 2021-2024", FUENTES, "SUGESTIVO",
                     f"Coprincipal P (adenda 1.6): repite la especificación de H3 de V15 (efectos de sección y de municipio × año, CR1 por municipio; DT intra-sección {f(PH['sd_intra'], 3)} pp) en la muestra V18; p = {f(PH['p_principal'], 4)}, "
                     f"p tras Holm {f(holm['E1-P-H3'], 4)}. Cifra publicada de V15: 0,0030 por DT, p = 0,931. No se clasifica (la clase mostrada es la del diseño de V15: asociación sin identificación; no cambia la de lo publicado)."))
    e1 = est["E1-R1"]
    H.append(K.hecho("V18-E1-R1", "Barrios de Barcelona cuyo stock de viviendas turísticas cambia al menos un 10 % entre el primer y el último valor anual (mínimo de datos de E1-R1)", float(e1["n_barrios_cambian"]), None, None,
                     "barrios (mínimo 20)", "2018-2024", "48 barrios no sellados; stock por barrio a partir de los puntos del registro", FUENTES, "NO ESTIMABLE",
                     f"NO ESTIMABLE por datos: {e1['minimo_datos']}. Con ese mínimo la especificación no se estima ni entra en Holm; su MDE80 sería {f(e1['mde80'], 4)} por pp (umbral 0,038). Lo haría estimable: "
                     "más variación del stock entre barrios (periodo posterior a 2024) o la serie reconstruida de licencias con bajas."))
    e2 = est["E1-R2"]
    pe2 = pe[pe.id == "E1-R2"].iloc[0]
    H.append(K.hecho("V18-E1-R2", "F efectivo de la primera etapa de la proximidad a atractivos × Google Trends sobre la densidad de viviendas turísticas (Barcelona, 2018-2024, con distancia al centro × año)",
                     float(pe2.F_efectivo), None, None, "F efectivo (MOP)", "2018-2024", cob, FUENTES + ["OpenStreetMap (ODbL)", "Google Trends (término «airbnb», ES-CT)"], "NO ESTIMABLE",
                     f"NO ESTIMABLE por variación: el contraste de Anderson-Rubin no alcanza el 80 % de potencia con ningún efecto (potencia máxima {f(e2.get('potencia_max'), 3)}); umbral 0,038. La primera etapa es nula: "
                     "el stock de licencias apenas varía en el tiempo (moratoria desde 2014 y PEUAT desde 2017) y el «cuándo» mueve los anuncios, no las licencias. "
                     f"La variante E1-R2-v5 (INE-VUT como endógena, 2022-2024) tiene F efectivo {f(float(pe[pe.id == 'E1-R2-v5'].F_efectivo.iloc[0]), 2)} con primera etapa de signo "
                     f"{'negativo' if float(pe[pe.id == 'E1-R2-v5'].pi.iloc[0]) < 0 else 'positivo'} y MDE80 {f(est['E1-R2-v5'].get('mde80'), 4)} (suplementaria: solo MDE, no se estima). Sin estimación del resultado."))
    a1 = est["E1-A1"]
    pa1 = pe[pe.id == "E1-A1"].iloc[0]
    H.append(K.hecho("V18-E1-A1", "MDE al 80 % de potencia (Anderson-Rubin) de la ampliación E1-A1: % de viviendas turísticas (INE-VUT) instrumentado con proximidad a atractivos × noches de la NUTS3, València, Sevilla, Málaga y Alicante",
                     a1["mde80"], None, None, "log por punto porcentual de viviendas turísticas", "2021-2024", f"{a1['n_unidades']} secciones, {a1['G']} distritos censales, 2021-2024", FUENTES + ["OpenStreetMap (ODbL)", "Eurostat tour_ce_oan3"],
                     "NO ESTIMABLE", f"NO ESTIMABLE por variación: MDE80 {f(a1['mde80'], 4)} frente al umbral 0,038 (Segú, 2018, NO VERIFICADA); F efectivo de la primera etapa {f(float(pa1.F_efectivo), 2)}. No se estima el resultado ni entra en Holm. "
                     "Lo haría estimable: una exposición con más variación dentro de la ciudad y el año (INE-VUT con más ediciones posteriores a 2024) o un instrumento más fuerte."))
    H.append(K.hecho("V18-E1-A2", "Registro de Andalucía con fecha de alta (Málaga y Sevilla), de Chaisemartin-D'Haultfœuille con dosis continua", None, None, None, "sin cifra", "2015-2024", "no estimada", FUENTES, "NO ESTIMABLE",
                     "NO ESTIMADA en esta pasada: el Monte Carlo de V18 valida dCDH solo con aleatorización del calendario entre 8 CCAA y la adenda deja «solo descriptivo» lo que ese Monte Carlo no valida. Lo haría estimable: un Monte Carlo de dCDH con dosis continua y dos ciudades, o más ciudades con registro con fecha de alta."))
    for i, t, n in (("E1-A4", "Regulaciones locales (PEUAT y moratorias) como diferencias en diferencias", "faltan la geometría del PEUAT y las fechas de las moratorias (docs/v18/tareas_autor.md, punto 13)"),
                    ("E1-A5", "InsideAirbnb como exposición", "solo hay instantáneas desde 2025-12; el histórico requiere la Archived Data Request (tareas_autor, punto 14)"),
                    ("E1-X1", "Precio de compra por barrio de Barcelona", "no hay serie de compraventa por barrio en abierto (Open Data BCN solo publica la oferta de segunda mano de 2007-2015)")):
        H.append(K.hecho(f"V18-{i}", t, None, None, None, "sin cifra", "—", "sin datos", ["docs/v18/tareas_autor.md"], "NO ESTIMABLE", f"NO ESTIMABLE: {n}."))
    K.volcar_json(OUT / "hechos.json", H)

    # ---------------------------------------------------------------- resultado.json
    t = tab.set_index("id")
    estim = {k: float(t.loc[k, "coef"]) for k in ("E1-R3", "E1-R4", "E1-P-H3")}
    res = {
        "rama": "v18/estimacion/e1", "pregunta": "¿Se asocian la densidad de viviendas turísticas (licencias HUT, % INE-VUT) y la proximidad al foco turístico con el alquiler mediano por sección (SERPAVI) en Barcelona y en otras cuatro ciudades no selladas?",
        "capa": "C4", "datos": "Registro HUT de Barcelona (puntos con coordenadas, 2018-2024), SERPAVI por sección 2011-2024, INE-VUT por sección 2021-2025, Censo 2021, OpenStreetMap (atractivos, ayuntamientos, hospitales, universidades), Google Trends, Eurostat; sin unidades selladas (v6, V15, V16)",
        "N": {"E1-R3": int(r3["n"]), "E1-R4": int(r4["n"]), "E1-P-H3": int(PH["n"]), "secciones_barcelona": int(B.cod_seccion.nunique()), "secciones_otras_ciudades": int(C.cod_seccion.nunique())},
        "metodo": "Estudio de eventos de dosis y diferencias en diferencias con efectos fijos de sección y de año, CR1 con t(G−1) y wild cluster bootstrap de Webb por barrio, Conley (1 y 2 km), Honest DiD (M̄ = 0 informativo), Roth, TOST, Moran; IV con F efectivo de MOP y Anderson-Rubin solo en la estimabilidad",
        "estimacion": estim,
        "ic95": {"E1-R3": [float(t.loc["E1-R3", "ic95_lo"]), float(t.loc["E1-R3", "ic95_hi"])], "E1-R4": [float(R4["ic_webb"][0]), float(R4["ic_webb"][1])], "E1-P-H3": [float(PH["ic95"][0]), float(PH["ic95"][1])]},
        "p_ajustado": {k: float(v) for k, v in holm.items()},
        "nivel_evidencia": "EXPLORATORIO", "clasificacion_v18": "NO ESTIMABLE",
        "clasificaciones": {"E1-R1": "NO ESTIMABLE", "E1-R2": "NO ESTIMABLE", "E1-R3": cl3["clase"], "E1-R4": cl4["clase"], "E1-A1": "NO ESTIMABLE", "E1-A2": "NO ESTIMABLE", "E1-A3": "NO ESTIMABLE", "E1-A4": "NO ESTIMABLE",
                            "E1-A5": "NO ESTIMABLE", "E1-X1": "NO ESTIMABLE", "E1-P-H3": "no se clasifica"},
        "diagnosticos": {
            "nota_clasificacion_global": "clasificacion_v18 es la de la estimación propia designada para B5, E1-A1 (NO ESTIMABLE); el respaldo E1-R2 también (NO ESTIMABLE por variación): E1 no tiene estimación propia estimable",
            "estimabilidad": [{k: v for k, v in e.items() if not isinstance(v, dict)} | {"estimable": bool(ok[i])} for i, e in est.items()],
            "primera_etapa_sin_resultado": pe.to_dict("records"),
            "E1-R3": {"pretendencias_p": ev3["pretend"]["p"], "pendiente_detectable_80": ev3["pretend"]["pendiente_detectable"], "sesgo_implicado_post": ev3["pretend"]["sesgo_post"], "placebo_fecha": ev3["placebo_fecha"],
                      "honest": ev3["honest"], "tendencia_distancia_2011_2013": ev3["tendencia_distancia"], "conley_se": R3["conley"], "moran_residuos": R3["moran"], "medidas_alternativas": R3["medidas"],
                      "razon_con_referencia": r3["razon_ref"], "tamano_mc_cr1": out["tam"]["R3"], "v3_coprincipal": R3["v3_coprincipal"], "clasificacion_razones": cl3["razones"]},
            "E1-R4": {"tost_delta_0_05": {"ic90_webb": list(cl4["info"]["tost"]["ic90"]), "delta": 0.05, "equivalente": cl4["info"]["tost"]["equivalente"]}, "pretendencias_p": ev4["pretend"]["p"], "pendiente_detectable_80": ev4["pretend"]["pendiente_detectable"], "sesgo_implicado_post": ev4["pretend"]["sesgo_post"], "placebo_fecha": ev4["placebo_fecha"],
                      "honest": ev4["honest"], "moran_residuos": R4["moran"], "medidas_alternativas": R4["medidas"], "conteos_geometria": R4["conteos"], "tamano_webb_mc": out["tam"]["R4"], "clasificacion_razones": cl4["razones"]},
            "E1-P-H3": {k: v for k, v in PH.items() if k != "ic95"},
        },
        "fuera_muestra": {"modelo": None, "rmse": None, "dm_vs_ar4": None, "nota": "no aplica: diseño de evaluación (efectos fijos y eventos), no predictivo; la evaluación sellada diferida de la adenda 1.11 solo incluye E1-A1, que no supera la estimabilidad"},
        "notas": "Análisis V18; capa C4; pre-registro interno plan-replicacion-v18. " + I8 + ". Ninguna estimación IDENTIFICADO: sin contradicción con lo publicado (parada G no activada).",
    }
    K.volcar_json(OUT / "resultado.json", res)

    # ---------------------------------------------------------------- informe.md
    e_tab = pd.DataFrame([{"id": i, "unidades": e.get("n_unidades"), "obs": e.get("n_obs"), "clusters": e.get("G"), "mínimo de datos": (e.get("minimo_datos") or "")[:95], "MDE80": f(e.get("mde80")), "umbral": f(e["umbral"]),
                           "decisión": ("estimable" if ok[i] else "NO ESTIMABLE")} for i, e in est.items()])
    pe_t = pe.copy()
    pe_t["F_efectivo"] = pe_t.F_efectivo.map(lambda x: f(x, 2))
    pe_t["pi"] = pe_t.pi.map(lambda x: f(x, 4))
    pe_t = pe_t[["id", "n", "G", "F_efectivo", "pi"]]
    prin = tab[tab.id.isin(["E1-R3", "E1-R4", "E1-P-H3"])][["id", "n_obs", "n_unidades", "G", "coef", "ic95_lo", "ic95_hi", "p_cr1", "p_webb", "p_i7", "p_holm", "clase"]].copy()
    for c in ("coef", "ic95_lo", "ic95_hi"):
        prin[c] = prin[c].map(lambda x: f(x, 4))
    for c in ("p_cr1", "p_webb", "p_i7", "p_holm"):
        prin[c] = prin[c].map(lambda x: f(x, 4))
    prin["n_obs"] = prin.n_obs.astype(int)
    prin["n_unidades"] = prin.n_unidades.astype(int)
    prin["G"] = prin.G.astype(int)
    var = tab[tab.rol.str.startswith(("variante", "coprincipal (tend")) & (tab.estado == "estimada")][["id", "resultado", "n_obs", "coef", "ic95_lo", "ic95_hi", "p_cr1", "p_webb", "q_by"]].copy()
    for c in ("coef", "ic95_lo", "ic95_hi"):
        var[c] = var[c].map(lambda x: f(x, 4))
    for c in ("p_cr1", "p_webb", "q_by"):
        var[c] = var[c].map(lambda x: f(x, 4))
    var["n_obs"] = var.n_obs.astype(int)
    evt = pd.DataFrame({"año": ev3["ev"]["anios"], "coef por DT de la dosis": [f(x) for x in ev3["ev"]["b"]], "ee": [f(x) for x in np.sqrt(np.diag(ev3["ev"]["V"]))]})
    evt4 = pd.DataFrame({"año": ev4["ev"]["anios"], "coef": [f(x) for x in ev4["ev"]["b"]], "ee": [f(x) for x in np.sqrt(np.diag(ev4["ev"]["V"]))]})
    hon3 = pd.DataFrame([{"M̄": h["Mbar"], "IC95": f"({f(h['ic95'][0])}; {f(h['ic95'][1])})", "excluye 0": h["excluye_cero"], "lectura": h["lectura"]} for h in ev3["honest"]])
    hon4 = pd.DataFrame([{"M̄": h["Mbar"], "IC95": f"({f(h['ic95'][0])}; {f(h['ic95'][1])})", "excluye 0": h["excluye_cero"], "lectura": h["lectura"]} for h in ev4["honest"]])
    aud_t = pd.DataFrame(aud).T.reset_index().rename(columns={"index": "corte"})
    ref_lit = "Segú (2018), IV lineal, por pp de densidad: 0,038 (0,012), ficha NO VERIFICADA (adenda, anexo B)"
    txt = f"""# V18 · E1 · Vivienda turística (Barcelona con registro HUT y SERPAVI; otras ciudades no selladas)

**Análisis V18; capa C4; pre-registro interno plan-replicacion-v18.** Nivel de evidencia EXPLORATORIO. La clasificación V18 va en el campo `clasificacion_v18` y no cambia la capa. {I8}.
Código: `src/v18/estimacion/e1_turismo.py` (+ `e1_adquisicion.py`, `e1_datos.py`, `e1_diseno.py`, `e1_estim.py`, `e1_mde.py`, `e1_nucleo.py`, `e1_resultados.py`, `e1_salidas.py`); SEED 20261010; sin red en la estimación; {segundos:.0f} s.

## 1. Resumen
- **Lo que supera la estimabilidad (adenda 1.3)**: E1-R3 (estudio de eventos de dosis, 2011-2019) y E1-R4 (Sagrada Família), más la coprincipal E1-P-H3 (H3 de V15 en la muestra V18).
- **E1-R3**: coeficiente por pp de densidad HUT de 2018T2 = **{f(r3['coef_por_pp'])}** (IC95 {f(r3['ic95_por_pp'][0])}; {f(r3['ic95_por_pp'][1])}; p corregido tras Holm {f(holm['E1-R3'], 4)}). Clase V18: **{cl3['clase']}**. Razón con la referencia (0,038): {f(razon3, 2)}, etiqueta {'coherente' if r3['coherente_ref'] else 'no coherente'}.
- **E1-R4**: {f(r4['coef'])} (IC95 de Webb {f(R4['ic_webb'][0])}; {f(R4['ic_webb'][1])}; p de Webb {f(r4['_res']['p_webb'], 4)}, tras Holm {f(holm['E1-R4'], 4)}). Clase V18: **{cl4['clase']}**.
- **E1-P-H3**: {f(PH['coef'])} por DT intra-sección (IC95 {f(PH['ic95'][0])}; {f(PH['ic95'][1])}; p {f(PH['p_principal'], 4)}). Cifra de V15: 0,0030, p = 0,931. No se clasifica.
- **NO ESTIMABLES por la regla previa** (se publica el MDE, no el coeficiente): **E1-R1** (solo {e1['n_barrios_cambian']} barrios con un cambio del stock HUT de al menos el 10 %, mínimo 20; MDE80 {f(e1['mde80'], 4)}), **E1-R2** (primera etapa nula: F efectivo {f(float(pe2.F_efectivo), 3)}) y **E1-A1** (MDE80 {f(a1['mde80'], 3)} frente a 0,038; F efectivo {f(float(pa1.F_efectivo), 2)}).
- Consecuencia para B5: la estimación propia designada de E1 es E1-A1 y su respaldo E1-R2; las dos son NO ESTIMABLES por variación, de modo que **E1 no tiene estimación propia estimable** (la adenda 1.9 solo prevé el respaldo cuando la propia es NO ESTIMABLE, y también lo es). Lo dice el informe; no se sustituye por E1-R3 ni E1-R4.
- Ninguna estimación IDENTIFICADO: no hay contradicción con una conclusión publicada (parada G no activada).

## 2. Datos y sellado
- **Barcelona.** {cob}. Las 299 secciones selladas no se usan (ni sus puntos del registro): de los puntos del registro en 2018T4 se asignan a secciones no selladas {aud['2018T4']['en_secciones_no_selladas']} de {aud['2018T4']['filas_fichero']} ({100 * aud['2018T4']['en_secciones_no_selladas'] / aud['2018T4']['filas_fichero']:.1f} %). Quedan los distritos de Ciutat Vella y l'Eixample, que concentran las licencias.
- **HUT.** El registro del Ajuntament trae coordenadas por licencia; cada punto se asigna a la sección INE que lo contiene (data/manual/v11/bcn_hut_trimestral; cortes de 2018T2 y de 4T de 2018 a 2024). El valor anual es el corte más cercano al 31 de diciembre (regla 1.3): en esos años es el de 4T. La densidad es HUT por 100 viviendas del Censo 2021 por sección. La asignación por punto sustituye a la agregación por barrio de la base (la base solo tiene series por barrio desde 2023): desviación D2.
- **SERPAVI** (VC, €/m²): {int(B[B.anio == 2011].y.notna().sum())} secciones en 2011 y {int(B[B.anio == 2024].y.notna().sum())} en 2024; todas las lecturas con `sellado.filtrar` (tope 2024).
- **Otras ciudades.** València (422 de 588 secciones tras el sellado), Sevilla (416 de 522), Málaga (356 de 435) y Alicante (196 de 246). INE-VUT por sección (media anual 2021-2024).
- **Atractivos, ayuntamientos, hospitales y universidades** de OpenStreetMap (extractos regionales de 2026-10-19; atractivos: Barcelona {n_att.get('08019', 136)}, València {n_att['46250']}, Sevilla {n_att['41091']}, Málaga {n_att['29067']}, Alicante {n_att['03014']}); **Google Trends** «airbnb» (término) en ES-CT, una descarga; **noches** de Eurostat por NUTS3; correspondencia sección-barrio de Open Data BCN. Todas con la marca `posterior_prereg` y manifiesto en data/raw/v18/_manifest_e1e6.csv.

Auditoría del geocodificado del registro HUT (puntos del fichero, con coordenadas y asignados a secciones no selladas):

{md(aud_t)}

## 3. Estimabilidad (adenda 1.3), calculada antes de mirar ningún coeficiente
MDE80: R = 2.000 réplicas, SEED 20261010; el ruido se remuestrea por barrio de los residuos del periodo previo de cada diseño («ya visto»: V15 y V16 no publican la σ residual de ln SERPAVI por sección) con la variación real del tratamiento; el valor crítico es el mayor entre el nominal t(G−1) y el empírico del propio Monte Carlo (corrección por tamaño). En los diseños con IV, el MDE es el del contraste de Anderson-Rubin por cluster.

{md(e_tab)}

Primera etapa de las especificaciones con instrumento y de sus variantes, **sin el resultado** (ln SERPAVI sustituido por 0): F efectivo de Montiel Olea-Pflueger y coeficiente.

{md(pe_t)}

- **E1-R1 no alcanza el mínimo de datos** ({e1['n_barrios_cambian']} barrios frente a 20): el stock HUT de los barrios no sellados casi no cambia entre 2018 y 2024 (moratoria desde 2014 y PEUAT desde 2017). Es una regla de la adenda, no una decisión sobre el coeficiente; de haberse contado 20 barrios, el MDE80 ({f(e1['mde80'], 4)}) sí habría estado por debajo del umbral. Sus 10 variantes no se estiman.
- **E1-R2-v5 (suplementaria, solo diseño)**: la variante con el % INE-VUT como endógena (2022-2024) tiene F efectivo {f(float(pe[pe.id == 'E1-R2-v5'].F_efectivo.iloc[0]), 2)}, coeficiente de la primera etapa {f(float(pe[pe.id == 'E1-R2-v5'].pi.iloc[0]), 3)} y MDE80 {f(est['E1-R2-v5'].get('mde80'), 4)} frente a 0,038. Una variante solo se estima si su principal es estimable (anexo A); el dato queda para la revisión.
- **Placebos del instrumento (solo primera etapa)**: con la proximidad a hospitales y a universidades × el mismo «cuándo», el F efectivo es {f(float(pe[pe.id == 'E1-R2 [placebo hospitales]'].F_efectivo.iloc[0]), 2)} y {f(float(pe[pe.id == 'E1-R2 [placebo universidades]'].F_efectivo.iloc[0]), 2)} en E1-R2 (instrumento real: {f(float(pe2.F_efectivo), 2)}) y {f(float(pe[pe.id == 'E1-A1 [placebo hospitales]'].F_efectivo.iloc[0]), 2)} y {f(float(pe[pe.id == 'E1-A1 [placebo universidades]'].F_efectivo.iloc[0]), 2)} en E1-A1 (real: {f(float(pa1.F_efectivo), 2)}). La forma reducida sobre el resultado no se calcula (no se estima el resultado).
- **E1-R2 y E1-A1**: la proximidad × Trends (o × noches), con efectos de sección y de año (o de municipio × año) y la distancia al centro × año, casi no predice la exposición; el AR no alcanza el 80 % de potencia con efectos de magnitud razonable. Sus variantes se documentan solo en la primera etapa.

## 4. Resultados de las especificaciones estimadas
{md(prin)}

p_cr1 = CR1 con t(G−1) por barrio (E1-R3) o por municipio (E1-P-H3); en E1-R4 la inferencia principal es Webb. p_i7 = p con el valor crítico corregido por el tamaño del Monte Carlo de cada diseño (E1-R3: {f(out['tam']['R3'], 3)} con CR1; E1-R4: {f(out['tam']['R4'], 3)} con Webb). Holm sobre la familia E1 estimada (m = {len(out['familia'])}: {', '.join(out['familia'])}); E1-R1, R2 y A1 salen antes de ajustar; P-D2 y P-Q2b no se han estimado (desviación D7). Las coprincipales P no se clasifican.

Coeficiente de E1-R3 por desviación típica de la dosis ({f(sd3, 3)} pp): {f(r3['coef'])} (EE {f(r3['se'])}); por pp: {f(r3['coef_por_pp'])}. Inferencias alternativas: Webb 9.999 p = {f(r3['_res']['p_webb'], 4)}; EE de Conley a 1 km {f(R3['conley'][1.0], 5)} y a 2 km {f(R3['conley'][2.0], 5)} (CR1: {f(r3['se'], 5)}; el Monte Carlo de V18 mide para Conley en secciones a 1 km un tamaño de 0,070, «con valor crítico corregido», apto solo si el alcance de la dependencia no supera el corte); Driscoll-Kraay no se usa («no fiable» en su Monte Carlo).

## 5. Pruebas B4
**E1-R3 (estudio de eventos de dosis; base 2013; coeficientes por DT de la dosis):**

{md(evt)}

- Adelantos (2011 y 2012, contraste conjunto): p = {f(ev3['pretend']['p'], 3)}. Pendiente lineal previa detectable al 80 % (Roth, 2022): {f(ev3['pretend']['pendiente_detectable'], 4)} por año; sesgo que implicaría en la ventana posterior: {f(ev3['pretend']['sesgo_post'], 4)}, frente a la mitad de |referencia| por DT ({f(E.DELTA['E1-R3'] * sd3, 4)}): {'superado' if (np.isfinite(ev3['pretend']['sesgo_post']) and ev3['pretend']['sesgo_post'] < E.DELTA['E1-R3'] * sd3) else 'no superado (prueba débil)'}. El preperiodo es de solo dos años.
- Placebo de fecha (adopción falsa en 2012, ventana 2011-2013): {f(ev3['placebo_fecha']['coef'])}, p = {f(ev3['placebo_fecha']['p'], 3)}.
- Tendencia por distancia al centro de 2011-2013 (diagnóstico de la adenda R-15): coeficiente {f(ev3['tendencia_distancia']['coef'])}, p = {f(ev3['tendencia_distancia']['p'], 3)}; {'la variante con distancia × año (v3) pasa a coprincipal' if R3['v3_coprincipal'] else 'no es significativa al 10 %: v3 sigue como variante'}.
- Honest DiD (Rambachan-Roth, magnitudes relativas). Según el Monte Carlo de V18 solo M̄ = 0 es apto; con M̄ = 0,5 y 1 es válido pero conservador y no decide (desviación D5):

{md(hon3)}

- I de Moran de los residuos medios por sección (5 vecinos): I = {f(R3['moran']['I'], 3)} (E[I] = {f(R3['moran']['E_I'], 3)}), p unilateral {f(R3['moran']['p_unilateral'], 3)}.
- Medida alternativa del resultado (por pp): €/mes de vivienda colectiva {f(R3['medidas']['y_mes']['coef'])} (IC95 {f(R3['medidas']['y_mes']['ic95'][0])}; {f(R3['medidas']['y_mes']['ic95'][1])}); vivienda unifamiliar {f(R3['medidas']['y_vu']['coef'])}; sin atípicos (1 % superior de dosis y 1 % extremo de la variación del resultado; {R3['medidas']['sin_atipicos']['n_excluidas']} secciones) {f(R3['medidas']['sin_atipicos']['coef'])}. Fianzas por barrio: no existen en abierto (desviación D6).
- Placebo de resultado (población de 65 años o más por sección): no aplicable a 2011-2019 (existe solo desde 2021; adenda R-15).

**E1-R4 (Sagrada Família; coeficientes del radio de 500 m frente al anillo; base 2013):**

{md(evt4)}

- Equivalencia (TOST, δ = 0,05): el IC90 por inversión del contraste de Webb ({f(cl4['info']['tost']['ic90'][0])}; {f(cl4['info']['tost']['ic90'][1])}) {'queda dentro de' if cl4['info']['tost']['equivalente'] else 'no queda dentro de'} ±0,05: el nulo {'queda acotado' if cl4['info']['tost']['equivalente'] else 'no queda acotado y la clase es NO CONCLUYENTE (sin potencia) si el diseño es válido'}. Con {r4['G']} clusters, {r4['G_tratados']} con tratadas (la mitad), el Monte Carlo de V18 da el Webb por barrio como apto (tamaño propio del diseño {f(out['tam']['R4'], 3)}).
- Adelantos (2011 y 2012): p = {f(ev4['pretend']['p'], 3)}; pendiente detectable {f(ev4['pretend']['pendiente_detectable'], 4)}; sesgo implicado {f(ev4['pretend']['sesgo_post'], 4)} (umbral δ = 0,05). Placebo de fecha (adopción falsa en 2012): {f(ev4['placebo_fecha']['coef'])}, p = {f(ev4['placebo_fecha']['p'], 3)}.
- Honest DiD:

{md(hon4)}

- Geometría: radio {R4['conteos']['radio_no_sellado']} de {R4['conteos']['radio_total']} secciones no selladas ({f(R4['conteos']['cuota_radio'], 2)}) y anillo {R4['conteos']['anillo_no_sellado']} de {R4['conteos']['anillo_total']} ({f(R4['conteos']['cuota_anillo'], 2)}): se cumple el 75 % de la adenda 1.5. {r4['G']} barrios, {r4['G_tratados']} con tratadas.
- Medida alternativa: €/mes {f(R4['medidas']['y_mes']['coef'])}; vivienda unifamiliar {f(R4['medidas']['y_vu']['coef'])}. Moran de los residuos: I = {f(R4['moran']['I'], 3)}, p unilateral {f(R4['moran']['p_unilateral'], 3)}.

## 6. Variantes enumeradas (anexo A)
Benjamini-Yekutieli al 10 % dentro de cada identificador. E1-R3 y E1-R4 con CR1 (E1-R4-v2, con 1.999 réplicas de Webb). Las variantes de E1-R1, E1-R2 y E1-A1 no se estiman (principal NO ESTIMABLE). E1-R3-v3 figura además como coprincipal en la familia de Holm cuando la tendencia por distancia de 2011-2013 es significativa al 10 % (adenda R-15); el q de cada variante es el de Benjamini-Yekutieli con su p de CR1 (E1-R4-v2: con su p de Webb).

{md(var)}

## 7. Clasificación (I1-I8 revisados)
- **E1-R3: {cl3['clase']}.** Fallos decisivos: {'; '.join(cl3['decisivos']) if cl3['decisivos'] else '—'}. Pruebas débiles: {'; '.join(cl3['debiles']) if cl3['debiles'] else '—'}. Topes: {'; '.join(cl3['topes']) if cl3['topes'] else '—'}.
- **E1-R4: {cl4['clase']}.** Fallos decisivos: {'; '.join(cl4['decisivos']) if cl4['decisivos'] else '—'}. Pruebas débiles: {'; '.join(cl4['debiles']) if cl4['debiles'] else '—'}. Topes: {'; '.join(cl4['topes']) if cl4['topes'] else '—'}.
- E1-P-H3, coprincipal: no se clasifica; su cifra publicada (V15) se muestra al lado.
- I6 como etiqueta: {ref_lit}. E1-R3: razón {f(razon3, 2)}, {'coherente' if r3['coherente_ref'] else 'no coherente'}. La magnitud difiere de la referencia por la medida (licencias HUT, no anuncios activos), por SERPAVI (contratos vigentes declarados: stock, que diluye el cambio) y por el periodo (2014-2019, con la dosis medida en 2018T2). No interviene en la clase ni en B5.
- I8 pendiente en todas (replicador-ciego). En las dos especificaciones estimadas la clase describe el diseño; el lenguaje es el de una asociación estimada.

## 8. Comparación con lo ya visto en el proyecto
- H3 (V15): 0,0030 por DT intra-sección, p = 0,931 (2021-2024, toda España en entrenamiento). E1-P-H3 lo repite en la muestra V18: {f(PH['coef'])} (p {f(PH['p_principal'], 3)}).
- Q2a/Q2c (V16), V9-D2 (Cataluña) y V9-D3 (València): asociaciones no concluyentes o con pretendencias rechazadas; E1-R3 y E1-R4 no sustituyen a ninguna de esas lecturas (periodos y unidades distintos) y no promueven de capa.
- V17 B4 y el informe integral (III.4): «turísticos: no concluyente». Una estimación NO CONCLUYENTE o SUGESTIVO no contradice esa conclusión; ninguna es IDENTIFICADO ni NO CONCLUYENTE con equivalencia (parada G3 no activada).

## 9. Desviaciones (detalle y fechas en docs/v18/desviaciones_e1_e6.md)
D1 Overpass no accesible: OSM por extractos regionales. D2 HUT por punto en lugar de por barrio. D3 Censo 2021 sin clave en sellado_v18.json. D4 INE-VUT porcentaje y plazas heredan el tope de viviendas turísticas. D5 Honest DiD solo informativo. D6 fianzas por barrio inexistentes. D7 coprincipales P-D2 y P-Q2b no estimadas. D8 E1-A2 no estimada. D9 definición operativa del instrumento y del «primer/último valor anual».

## 10. Limitaciones y datos que lo resolverían
- El stock de licencias HUT casi no varía tras 2018: el diseño de E1 con licencias no tiene primera etapa. La exposición con variación es el anuncio activo (InsideAirbnb, histórico por la Archived Data Request; tareas_autor, punto 14), no la licencia.
- SERPAVI mide contratos vigentes declarados (stock), no anuncios; no se contrasta la composición a escala de sección (el recuento de contratos por sección tiene el tope sellado entero).
- El preperiodo de E1-R3 y E1-R4 es de dos años (2011-2012): la potencia para detectar tendencias previas es baja.
- Precio de compra por barrio (X1): serie de compraventa de Open Data BCN o microdatos de portales (tareas_autor, punto 2).
"""
    (OUT / "informe.md").write_text(txt, encoding="utf-8")
