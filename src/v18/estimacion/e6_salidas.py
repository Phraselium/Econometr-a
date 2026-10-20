"""V18 · fase 4 · E6 · salidas: tabla.csv, mde.csv, resultado.json (formato de CLAUDE.md + clasificacion_v18), hechos.json (cifras V18-E6-*) e informe.md.

Análisis V18; capa C4; pre-registro interno plan-replicacion-v18. Sin lenguaje causal en las cifras (check_v18) ni en el informe.
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
import _e2e8_comun as K  # noqa: E402
import e6_obra_nueva as O  # noqa: E402

ALCANCE_TERRITORIAL = "sin lectura de datos"     # solo escribe salidas a partir de las tablas que recibe
FUENTES = ["Catastro (DGC), INSPIRE Buildings de la provincia de València (descarga de 2026-08-21, reutilización con reconocimiento)", "SERPAVI (MIVAU), alquiler mediano por sección, 2011-2024",
           "docs/v18/plan_replicacion.md + plan_replicacion_adenda.md (pre-registro interno plan-replicacion-v18)"]
I8 = "Sin estimación del resultado: no hay clasificación que contrastar con I8"
AEMET = ("la API de AEMET OpenData exige una clave personal (alta con correo electrónico del autor); la consulta sin clave, hecha el 2026-10-20 desde esta sesión, devuelve una respuesta vacía. "
         "Sin la lluvia de AEMET, E6-R2 es NO ESTIMABLE (plan 1.6, X1); no se sustituye por otra fuente (ERA5, Open-Meteo) sin orden expresa del autor")


def f(x, n=4):
    return "—" if x is None or (isinstance(x, (float, np.floating)) and not np.isfinite(x)) else f"{x:.{n}f}"


def md(df: pd.DataFrame) -> str:
    cols = list(df.columns)
    out = ["| " + " | ".join(str(c) for c in cols) + " |", "|" + "|".join("---" for _ in cols) + "|"]
    for r in df.itertuples(index=False):
        out.append("| " + " | ".join("—" if (isinstance(v, (float, np.floating)) and not np.isfinite(v)) or v is None else str(v) for v in r) + " |")
    return "\n".join(out)


def _resumen_cuentas(c: dict) -> tuple[int, int, str]:
    cs = c["conteos"]
    tr = sum(v.get("tratadas", 0) for v in cs.values())
    co = sum(v.get("controles", 0) for v in cs.values())
    return tr, co, "; ".join(f"{E}: {v.get('tratadas', 0)}/{v.get('controles', 0)}" for E, v in cs.items())


def escribir(OUT: Path, B: dict, secs: pd.DataFrame, c1: dict, d1: pd.DataFrame, cuentas: dict, dec: dict, est: dict | None, segundos: float) -> None:
    mde, mde10 = dec["mde"], dec["mde_10k"]
    umbral = dec["umbral"]
    n_sec, n_tot = secs.attrs["n_tras_sellado"], secs.attrs["n_total"]
    q = B["edif"]
    # ---------------------------------------------------------------- tabla.csv y mde.csv
    filas = []

    def fila(id_, rol, estado, resultado, **kw):
        base = {"id": id_, "rol": rol, "estado": estado, "resultado": resultado, "tratadas": np.nan, "controles": np.nan, "G": np.nan, "mde80": np.nan, "umbral": np.nan, "clase": "NO ESTIMABLE", "nota": ""}
        base.update(kw)
        filas.append(base)

    fila("E6-R1", "principal", dec["decision"], "ln SERPAVI (VC) de secciones contiguas a edificios de >= 20 viviendas terminados en 2015-2018", tratadas=dec["n_tr"], controles=dec["n_co"], G=mde["G"], mde80=mde["mde80"], umbral=umbral,
         nota=f"MDE80 con R = 10.000: {f(mde10['mde80'], 4)} (sensibilidad; la decisión previa es la de R = 2.000)")
    for suf, dim, desc, _ in O.VARIANTES_R1:
        tr, co, txt = _resumen_cuentas(cuentas[f"E6-R1-{suf}"])
        fila(f"E6-R1-{suf}", "variante", "no estimada (principal NO ESTIMABLE)", f"[{dim}] {desc}", tratadas=tr, controles=co, nota=f"recuento de pilas (tratadas/controles): {txt}")
    tr, co, txt = _resumen_cuentas(cuentas["E6-A1"])
    fila("E6-A1", "principal", f"NO ESTIMABLE por datos: {tr} secciones tratadas con edificios de >= 50 viviendas y anillo de 250 m (mínimo 30)", "E6-R1 con umbral de 50 viviendas y anillo de 250 m", tratadas=tr, controles=co,
         nota=f"recuento de pilas (tratadas/controles): {txt}")
    fila("E6-A2", "NO ESTIMABLE", "NO ESTIMABLE (datos): E6-R1 en el resto de España requiere la descarga masiva del Catastro (tareas_autor, punto 1)", "E6-R1 en el resto de España")
    fila("E6-R2", "principal", f"NO ESTIMABLE (X1): {AEMET}", "ln alquiler provincial (IPVA) por unidad terminada en el 4T, instrumentada con la lluvia de julio a septiembre", nota="datos disponibles: terminadas trimestrales provinciales 2008T1-2026T2, IPVA provincial 2011-2024")
    for suf, dim, desc in O.VARIANTES_R2:
        fila(f"E6-R2-{suf}", "variante", "no estimada (E6-R2 NO ESTIMABLE)", f"[{dim}] {desc}")
    fila("E6-A3", "principal", "NO ESTIMABLE (X1): sin la lluvia de AEMET", "E6-R2 con el IPC de alquiler 2002-2025")
    tab = pd.DataFrame(filas)
    tab.to_csv(OUT / "tabla.csv", index=False)
    pd.DataFrame([{"id": "E6-R1", "tratadas": dec["n_tr"], "controles": dec["n_co"], "minimo_datos": "≥ 30 tratadas y ≥ 30 de control", "cumple_minimo": dec["minimo"], "G": mde["G"], "mde80": mde["mde80"],
                   "mde80_nominal": mde["mde80_nominal"], "mde80_corregido_tamano": mde["mde80_corregido_tamano"], "mde80_R10000": mde10["mde80"], "umbral": umbral, "tamano_nominal_cr1": mde["tamano_nominal"],
                   "sigma_residual_previo": mde["sigma_residual_previo"], "R": mde["R"], "estimable": dec["ok"]}]).to_csv(OUT / "mde.csv", index=False)

    # ---------------------------------------------------------------- hechos
    H = []
    cob = f"{dec['n_tr']} secciones tratadas y {dec['n_co']} de control de la provincia de València no selladas (de {n_sec} de {n_tot} tras el sellado), {mde['G']} clusters (secciones de edificio), 2011-2024"
    H.append(K.hecho("V18-E6-R1", "MDE al 80 % de potencia de E6-R1: efecto medio (k = 0..3) de un edificio de 20 viviendas o más terminado en 2015-2018 sobre el log del alquiler SERPAVI de las secciones contiguas",
                     mde["mde80"], None, None, "log", "2011-2024", cob, FUENTES, "NO ESTIMABLE",
                     f"NO ESTIMABLE por variación: MDE80 {f(mde['mde80'], 4)} frente al umbral {f(umbral, 3)} (Asquith et al., «cerca frente a cerca», −0,062; ficha con año DISCREPANTE). La diferencia es de {f(mde['mde80'] - umbral, 4)} "
                     f"y se mantiene con R = 10.000 (MDE80 {f(mde10['mde80'], 4)}); se aplica la regla previa. No se estima el resultado ni entra en Holm. Lo haría estimable: más cohortes posteriores a 2018 "
                     "con SERPAVI de 2025-2027, la descarga masiva del Catastro (otras provincias) o el alquiler por anuncio georreferenciado."))
    tr1, co1, _ = _resumen_cuentas(cuentas["E6-A1"])
    H.append(K.hecho("V18-E6-A1", "Secciones tratadas de E6-A1 (edificios de 50 viviendas o más terminados en 2015-2018; anillo de 250 m), provincia de València", float(tr1), None, None, "secciones (mínimo 30)", "2015-2018", f"{tr1} secciones tratadas y {co1} de control en las pilas de E6-A1 (50 viviendas, anillo de 250 m), provincia de València no sellada", FUENTES,
                     "NO ESTIMABLE", f"NO ESTIMABLE por datos: {tr1} secciones tratadas (mínimo 30). Lo haría estimable: la descarga masiva del Catastro (tareas_autor, punto 1)."))
    H.append(K.hecho("V18-E6-A2", "E6-R1 en el resto de España", None, None, None, "sin cifra", "—", "sin datos", ["docs/v18/tareas_autor.md"], "NO ESTIMABLE",
                     "NO ESTIMABLE: requiere la descarga masiva del Catastro (tareas_autor, punto 1)."))
    H.append(K.hecho("V18-E6-R2", "Instrumento de Mense (2025): lluvia de julio a septiembre y alquiler provincial por unidad terminada en el cuarto trimestre", None, None, None, "sin cifra", "2011-2024", "sin lluvia de AEMET",
                     ["Mense (2025), JPE Macroeconomics 3(1): ficha de docs/v18/bib/obra_nueva", "MIVAU, terminadas trimestrales por provincia; IPVA provincial"], "NO ESTIMABLE",
                     f"NO ESTIMABLE (X1): {AEMET}. Lo haría estimable: la clave gratuita de AEMET OpenData o la autorización expresa del autor para sustituir la lluvia por una fuente alternativa (tarea del autor)."))
    H.append(K.hecho("V18-E6-A3", "E6-R2 con el IPC de alquiler 2002-2025", None, None, None, "sin cifra", "2002-2025", "sin lluvia de AEMET", ["INE, IPC de alquiler por provincia"], "NO ESTIMABLE",
                     "NO ESTIMABLE (X1): sin la lluvia de AEMET."))
    K.volcar_json(OUT / "hechos.json", H)

    # ---------------------------------------------------------------- resultado.json
    res = {
        "rama": "v18/estimacion/e6", "pregunta": "¿Se asocian los edificios nuevos de 20 viviendas o más terminados en 2015-2018 con el alquiler mediano de las secciones contiguas (piloto de la provincia de València), y las unidades terminadas con el alquiler provincial (instrumento de lluvia)?",
        "capa": "C4", "datos": "Catastro INSPIRE (edificios con año de construcción) de 92 municipios de la provincia de València; SERPAVI por sección 2011-2024; terminadas trimestrales y IPVA provinciales; sin unidades selladas (v6, V15, V16)",
        "N": {"E6-R1_tratadas": dec["n_tr"], "E6-R1_controles": dec["n_co"], "E6-R1_obs": int(len(d1)), "secciones_no_selladas": int(n_sec)},
        "metodo": "Diferencias en diferencias apiladas por cohorte (controles aún no expuestos), efectos fijos de unidad, año y municipio × año por pila, CR1 con t(G−1) por sección del edificio, MDE por Monte Carlo; IV con lluvia (AEMET) no disponible",
        "estimacion": {}, "ic95": {}, "p_ajustado": {}, "nivel_evidencia": "EXPLORATORIO", "clasificacion_v18": "NO ESTIMABLE",
        "clasificaciones": {"E6-R1": "NO ESTIMABLE", "E6-A1": "NO ESTIMABLE", "E6-A2": "NO ESTIMABLE", "E6-R2": "NO ESTIMABLE", "E6-A3": "NO ESTIMABLE"},
        "diagnosticos": {"estimabilidad": [{"id": "E6-R1", "tratadas": dec["n_tr"], "controles": dec["n_co"], "cumple_minimo": dec["minimo"], "G": mde["G"], "mde80": mde["mde80"], "mde80_R10000": mde10["mde80"], "umbral": umbral,
                                            "decision": dec["decision"], "sigma_residual_previo": mde["sigma_residual_previo"], "tamano_nominal_cr1": mde["tamano_nominal"]}],
                         "recuentos_pilas": {k: {"conteos": v["conteos"], "unidades_contaminadas_por_secciones_selladas": v["contaminadas"]} for k, v in cuentas.items()},
                         "nota_clasificacion_global": "clasificacion_v18 es la de la estimación propia designada para B5, E6-R2 (NO ESTIMABLE por falta de la lluvia de AEMET); E6-R1 está en otra unidad y también es NO ESTIMABLE"},
        "fuera_muestra": {"modelo": None, "rmse": None, "dm_vs_ar4": None, "nota": "no aplica: diseño de evaluación, no predictivo; E6-R2 es hipótesis de la evaluación sellada diferida (adenda 1.11) solo si llegara a IDENTIFICADO"},
        "notas": "Análisis V18; capa C4; pre-registro interno plan-replicacion-v18. " + I8 + ". Sin parada G.",
    }
    K.volcar_json(OUT / "resultado.json", res)

    # ---------------------------------------------------------------- informe.md
    pilas = pd.DataFrame([{"cohorte": E, "tratadas": v.get("tratadas"), "controles": v.get("controles"), "municipios tratadas": v.get("municipios_tratadas"), "municipios controles": v.get("municipios_controles"),
                           "València ciudad (tratadas)": v.get("valencia_ciudad_tratadas")} for E, v in c1["conteos"].items()])
    var = pd.DataFrame([{"id": k, "tratadas": _resumen_cuentas(v)[0], "controles": _resumen_cuentas(v)[1], "por pila (tratadas/controles)": _resumen_cuentas(v)[2]} for k, v in cuentas.items()])
    mde_t = pd.DataFrame([{"id": "E6-R1", "tratadas": dec["n_tr"], "controles": dec["n_co"], "clusters": mde["G"], "MDE80 (R = 2.000)": f(mde["mde80"], 4), "nominal": f(mde["mde80_nominal"], 4),
                           "corregido por tamaño": f(mde["mde80_corregido_tamano"], 4), "R = 10.000": f(mde10["mde80"], 4), "umbral": f(umbral, 3), "decisión": "estimable" if dec["ok"] else "NO ESTIMABLE"}])
    txt = f"""# V18 · E6 · Obra nueva y alquileres cercanos (piloto de la provincia de València)

**Análisis V18; capa C4; pre-registro interno plan-replicacion-v18.** Nivel de evidencia EXPLORATORIO. La clasificación V18 va en el campo `clasificacion_v18` y no cambia la capa. {I8}.
Código: `src/v18/estimacion/e6_obra_nueva.py` (+ `e6_datos.py`, `e6_diseno.py`, `e6_estim.py`, `e6_salidas.py`, `e1_nucleo.py`, `e1_datos.py`, `_e2e8_comun.py`); SEED 20261010; sin red; {segundos:.0f} s.

## 1. Resumen
- **Ninguna especificación de E6 supera la estimabilidad previa (adenda 1.3)**; no se estima ningún coeficiente y no hay cifra de efecto que difundir. Se publican los recuentos, el MDE y lo que falta.
- **E6-R1** (cohortes 2015-2018, secciones contiguas sin la propia, edificios de 20 viviendas o más): {dec['n_tr']} secciones tratadas y {dec['n_co']} de control (mínimo 30 y 30: se cumple), pero **MDE80 = {f(mde['mde80'], 4)}** frente al umbral 0,062 (|−0,062| de Asquith, Mast y Reed, «cerca frente a cerca», año de la ficha DISCREPANTE). Supera el umbral por {f(mde['mde80'] - umbral, 4)} (una diferencia de unas dos milésimas del umbral) y se mantiene con R = 10.000 (MDE80 {f(mde10['mde80'], 4)}); con el valor crítico nominal en lugar del corregido por tamaño sería {f(mde['mde80_nominal'], 4)}. La regla de la adenda es «MDE ≤ referencia» con R = 2.000 y el valor crítico corregido por tamaño cuando el tamaño se aparta del 5 %: aquí el tamaño nominal del CR1 es {f(mde['tamano_nominal'], 3)}. Se aplica la regla, no el matiz: NO ESTIMABLE por variación.
- **E6-A1** (50 viviendas, anillo de 250 m): {tr1} secciones tratadas (mínimo 30): NO ESTIMABLE por datos.
- **E6-R2 y E6-A3** (instrumento de lluvia de Mense): NO ESTIMABLES (X1) sin la lluvia de AEMET; E6-A2 sin la descarga masiva del Catastro.
- Consecuencia para B5: la estimación propia de E6 es E6-R2 (sin respaldo: E6-R1 está en otra unidad y no se combina). **E6 no tiene estimación propia**: la magnitud de E6 sale solo de la literatura en B5.
- Sin estimación del resultado no hay clase que pueda ser IDENTIFICADO ni contradicción con lo publicado (parada G no activada).

## 2. Datos y sellado
- **Secciones.** {n_tot} secciones INE de la provincia de València; quedan {n_sec} tras excluir los bloques sellados de V15 y V16 (166 de las 588 secciones de València ciudad y los 101 municipios sellados de la provincia). La provincia 46 no está sellada en v6.
- **Edificios.** Microdatos del Catastro (INSPIRE, 92 municipios de la provincia, descarga de 2026-08-21; microdatos no versionados, agregados en data/raw/v11/catastro_inspire): {len(q)} edificios residenciales con año de construcción en 2011-2024 y en secciones no selladas. Cada edificio se asigna a la sección INE 2025 que contiene su centro; el año es el fin de obra del Catastro y mide solo edificios que siguen en pie.
- **Sellado y exposición.** La exposición a edificios de secciones selladas no es observable: se excluyen las unidades con alguna sección contigua sellada ({c1['contaminadas']} de {n_sec}). Las pilas usan solo edificios de secciones no selladas.
- **SERPAVI** (VC, €/m²): {int(B['sp']['VC'].notna().any(axis=1).sum())} secciones de la provincia no selladas con algún año; todas las lecturas con `sellado.filtrar` (tope 2024).

## 3. Diseño (sin resultados)
Definiciones operativas fijadas antes de estimar (docs/v18/desviaciones_e1_e6.md, D-E6-1 a D-E6-4 y D-E6-8): edificio cualificado, unidad, «contigua», pila por cohorte, tratadas y controles, k = año − (T + 1), ventana T−4..T+4 (k = −5..3) y referencia k = −5. Controles: unidades cuyo primer edificio expuesto es de T+6 a 2024; ni unas ni otras tienen edificio propio cualificado en la ventana, y las tratadas no tienen otro edificio expuesto en la ventana.

{md(pilas)}

## 4. Estimabilidad (adenda 1.3), calculada antes de mirar ningún coeficiente
MDE80 de la media de k = 0..3, con CR1 t(G−1) por sección del edificio. El ruido se remuestrea por cluster de los residuos de 2011-2014 (ln SERPAVI tras efectos de sección y de municipio × año; «σ ya vista»: V15 y V16 no publican la σ residual de este resultado) con la variación real de las pilas; la ventana temporal se recicla de forma circular (4 años previos para 9 de ventana). Valor crítico: el mayor entre el nominal t(G−1) y el empírico del propio Monte Carlo (tamaño nominal del CR1: {f(mde['tamano_nominal'], 3)}).

{md(mde_t)}

Recuentos de las variantes y de E6-A1 (diseño, sin resultado):

{md(var)}

- Las variantes de E6-R1 no se estiman (principal NO ESTIMABLE). Los recuentos muestran además que la regla de «un solo evento en la ventana» deja pocas tratadas al bajar el umbral a 10 viviendas (más edificios por sección contigua) y que sin València ciudad no quedan controles suficientes.

## 5. E6-R2 (Mense, 2025): NO ESTIMABLE
- {AEMET}.
- Disponible: terminadas trimestrales por provincia (MIVAU, 2008T1-2026T2), IPVA provincial (2011-2024) e IPC de alquiler provincial. Con 39 provincias no selladas (las 11 de v6 fuera) el diseño tendría cluster por provincia con Webb (G < 40), según el plan.
- Los placebos de la adenda (lluvia de enero a marzo sobre T^Q4; lluvia sobre la renta ADRH y el empleo; lluvia de julio a septiembre de t−1 sobre las pernoctaciones de t) y la primera etapa no se pueden calcular sin la lluvia.

## 6. Desviaciones (detalle y fechas en docs/v18/desviaciones_e1_e6.md)
D-E6-1 definición operativa de edificio, unidad y exposición; D-E6-2 unidades con vecina sellada excluidas; D-E6-3 pilas con controles aún no expuestos y referencia k = −5 en lugar de Sun-Abraham con nunca tratadas; D-E6-4 regla de evento único en la ventana; D-E6-5 caché de edificios fuera del repositorio; D-E6-6 E6-R2 NO ESTIMABLE sin AEMET (tarea del autor); D-E6-7 E6-R1 NO ESTIMABLE por 0,0003 sobre el umbral; D-E6-8 ventana temporal circular del ruido.

## 7. Limitaciones y datos que lo resolverían
- Con {dec['n_tr']} tratadas en {int(d1[d1.tr == 1].cl.nunique())} clusters de edificio, casi todas en València ciudad y municipios metropolitanos, el diseño tiene poca variación: el MDE80 queda en el límite de la referencia.
- SERPAVI mide contratos vigentes declarados (stock): diluye el efecto de una obra nueva sobre los alquileres de las secciones contiguas.
- El Catastro solo recoge edificios que siguen en pie: la obra nueva de 2015-2018 está subestimada si hubo demoliciones, y la fecha de inicio de obra no existe (v2 aproxima la terminación − 2).
- Datos: SERPAVI de 2025-2027 (más cohortes y periodo posterior), descarga masiva del Catastro (otras provincias; tareas_autor, punto 1), alquiler por anuncio georreferenciado (puntos 2 y 4) y la clave de AEMET OpenData o la autorización de una fuente alternativa de lluvia (tarea del autor).
"""
    (OUT / "informe.md").write_text(txt, encoding="utf-8")
