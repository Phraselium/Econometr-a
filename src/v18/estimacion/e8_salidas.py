"""V18 · E8 · salidas: resultado.json (formato de CLAUDE.md + clasificacion_v18), hechos.json (cifras V18-E8-*) e informe.md.

Análisis V18; capa C4; pre-registro interno plan-replicacion-v18. Sin lenguaje causal en cifras (check_v18) ni en el informe.
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
import _e2e8_comun as K  # noqa: E402
import e8_diseno as DS  # noqa: E402

ALCANCE_TERRITORIAL = "lectura con sellado.filtrar y holdout.excluir_sellados_v6"
I8 = "Clasificación provisional: falta I8 (réplica ciega, B6)"
FUENTES = ["intervenciones.csv de V16 (tipos generales del ITP, memorias del Ministerio de Hacienda: fuente secundaria, fechas sin contraste con el BOE)",
           "MIVAU, valor tasado de vivienda libre por provincia", "docs/v18/plan_replicacion.md + plan_replicacion_adenda.md (pre-registro interno plan-replicacion-v18)"]


def f(x, n=4):
    return "—" if x is None or (isinstance(x, float) and not np.isfinite(x)) else f"{x:.{n}f}"


def md(df: pd.DataFrame) -> str:
    cols = list(df.columns)
    out = ["| " + " | ".join(str(c) for c in cols) + " |", "|" + "|".join("---" for _ in cols) + "|"]
    for r in df.itertuples(index=False):
        out.append("| " + " | ".join("—" if (isinstance(v, float) and not np.isfinite(v)) or v is None else str(v) for v in r) + " |")
    return "\n".join(out)


def escribir(OUT: Path, est: pd.DataFrame, tab: pd.DataFrame, diag: dict, clasif: dict, cal: pd.DataFrame, segundos: float) -> None:
    t = tab.set_index("id")
    ne = est.set_index("id")
    di = diag["E8-R1"]
    r = di["r"]
    cl = clasif["E8-R1"]["clase"]
    info = clasif["E8-R1"]["info"]
    ref = DS.ESPEC["E8-R1"]["ref"]
    razon = r["coef"] / (-ref)
    v4 = t.loc["E8-R1-v4"]
    pq = diag["E8-P-Q6p"]["r"]

    # ---------------------------------------------------------------- hechos
    H = []
    cob = (f"{int(t.loc['E8-R1', 'n_provincias'])} provincias con valor tasado trimestral de {int(t.loc['E8-R1', 'n_comunidades'])} comunidades de régimen común no selladas "
           "(sin Cantabria: no hay serie provincial completa), 2007T1-2026T2")
    nota = (f"Wald-DID de dosis continua (dCDH, 4 trimestres) por punto de variación del tipo general; p de aleatorización de calendarios entre comunidades {f(r['p_aleat'], 4)} "
            f"(estudentizada, 9.999 permutaciones; tamaño de Monte Carlo 0,0455, banda apta); p tras Holm con la coprincipal V16-Q6-p {f(t.loc['E8-R1', 'p_holm'], 4)}. "
            f"Signo contrario al de la referencia (Dolls et al., −0,03 por pp): razón {f(razon, 2)}, etiqueta «no coherente». Sin 2012-2013 el signo cambia ({f(v4.coef)}): el calendario se "
            "concentra en la crisis. Fechas de la memoria de Hacienda sin contraste con el BOE y sin control de recaudación previa: tope SUGESTIVO. Lectura: asociación estimada. " + I8 + ".")
    H.append(K.hecho("V18-E8-R1", "Cambio del log del valor tasado provincial a 4 trimestres por punto de variación del tipo general del ITP (Wald-DID de dosis continua)", r["coef"],
                     r["ic_aleat"][0], r["ic_aleat"][1], "log por punto del tipo general", "2007T1-2026T2", cob, FUENTES, cl["clase"], nota))
    for ident, texto, cober in (("E8-R2", "MDE al 80 % de potencia del efecto del tipo general del ITP sobre las compraventas provinciales mensuales (por punto)",
                                 f"{int(ne.loc['E8-R2', 'n_unidades'])} provincias, 216 meses, {int(ne.loc['E8-R2', 'n_comunidades'])} comunidades"),
                                ("E8-A2", "MDE al 80 % de potencia del efecto del tipo general del ITP sobre las compraventas municipales (por punto)",
                                 f"{int(ne.loc['E8-A2', 'n_unidades'])} municipios grandes, 72 trimestres, {int(ne.loc['E8-A2', 'n_comunidades'])} comunidades")):
        e = ne.loc[ident]
        H.append(K.hecho(f"V18-{ident}", texto, e.mde80, None, None, "log por punto (MDE80)", "2007-2024", cober, FUENTES, "NO ESTIMABLE",
                         f"NO ESTIMABLE por variación: MDE80 {f(e.mde80)} por punto mayor que el umbral {f(e.umbral)} ({e.referencia}); no se estima. Lo haría estimable: más comunidades con cambios "
                         "de tipo, más años de calendario o compraventas con menor ruido (Notariado o AEAT por tramo, tareas_autor punto 7)."))
    H.append(K.hecho("V18-E8-A1", "Primera etapa fiscal: recaudación del ITP por comunidad frente al cambio del tipo", None, None, None, "sin cifra", "—", "sin datos",
                     ["docs/v18/tareas_autor.md, punto 7"], "NO ESTIMABLE",
                     "NO ESTIMABLE: la recaudación del ITP por comunidad (liquidación de tributos cedidos, Hacienda) no está en el repositorio. Lo haría estimable: descargar esa serie (fuente abierta)."))
    for ident, texto in (("E8-X1", "Bunching en los umbrales de los tipos reducidos"), ("E8-X2", "Tipos reducidos para jóvenes y familias")):
        H.append(K.hecho(f"V18-{ident}", texto, None, None, None, "sin cifra", "—", "sin datos", ["docs/v18/tareas_autor.md, punto 7"], "NO ESTIMABLE", f"NO ESTIMABLE: {t.loc[ident, 'nota']}."))
    K.volcar_json(OUT / "hechos.json", H)

    # ---------------------------------------------------------------- resultado.json
    res = {
        "rama": "v18/estimacion/e8", "pregunta": "¿Se asocian los cambios del tipo general del ITP por comunidad con el valor tasado y con las compraventas provinciales?",
        "capa": "C4", "datos": "valor tasado provincial trimestral 2007T1-2026T2 (30 provincias de 7 comunidades), tipos del ITP de la base de intervenciones de V16; sin unidades selladas (v6, V15, V16)",
        "N": {"E8-R1": int(r["n_obs"]), "provincias": int(t.loc["E8-R1", "n_provincias"]), "comunidades": int(t.loc["E8-R1", "n_comunidades"])},
        "metodo": "dCDH con dosis continua (ℓ = 4), aleatorización de calendarios entre comunidades (APTO), t con G − 1 gl, adelantos por aleatorización, Sun-Abraham en bajadas, Wald-DID anual de V16 como coprincipal",
        "estimacion": {"E8-R1": r["coef"], "E8-P-Q6p": pq["coef"],
                       "variantes": {i: float(c) for i, c in zip(tab[(tab.rol == "variante") & tab.coef.notna()].id, tab[(tab.rol == "variante") & tab.coef.notna()].coef)}},
        "ic95": {"E8-R1": [float(r["ic_aleat"][0]), float(r["ic_aleat"][1])]},
        "p_ajustado": {"E8-R1": float(t.loc["E8-R1", "p_holm"]), "E8-P-Q6p": float(t.loc["E8-P-Q6p", "p_holm"])},
        "nivel_evidencia": "EXPLORATORIO", "clasificacion_v18": K.clase_corta(cl["clase"]),
        "clasificaciones": {"E8-R1": cl["clase"], "E8-R2": "NO ESTIMABLE", "E8-A1": "NO ESTIMABLE", "E8-A2": "NO ESTIMABLE", "E8-X1": "NO ESTIMABLE", "E8-X2": "NO ESTIMABLE"},
        "diagnosticos": {
            "estimabilidad": est.to_dict("records"),
            "E8-R1": {"adelantos_g": dict(zip([f"-{k}" for k in di["adelantos"]["ks"]], di["adelantos"]["g"])), "pretendencias_p_conjunto": di["adelantos"]["p_conjunto"],
                      "pendiente_detectable": di["pendiente"], "placebo_fecha_adelanto_8": di["placebo_fecha"], "placebo_resultado_poblacion": di["placebo_resultado"],
                      "inferencia": {"p_aleatorizacion": r["p_aleat"], "p_t_7gl": r["p_t"], "p_webb_no_fiable": float(t.loc["E8-R1", "p_webb_no_fiable"]), "driscoll_kraay_twfe_no_fiable": di["dk"]},
                      "tost": info["tost"], "moran_residuos": di["moran"], "razon_con_referencia": razon, "clasificacion_razones": cl["razones"]},
            "E8-P-Q6p": pq,
        },
        "fuera_muestra": {"modelo": None, "rmse": None, "dm_vs_ar4": None, "nota": "no aplica: diseño de evaluación (dCDH), no predictivo; E8 es episodio histórico y no entra en la evaluación sellada diferida (adenda 1.11)"},
        "notas": "Análisis V18; capa C4; pre-registro interno plan-replicacion-v18. " + I8 + ". Ninguna estimación IDENTIFICADO: sin contradicción con lo publicado (parada G no activada).",
    }
    K.volcar_json(OUT / "resultado.json", res)

    # ---------------------------------------------------------------- informe.md
    e_tab = est[["id", "n_unidades", "n_comunidades", "mde80", "umbral", "estimable"]].copy()
    e_tab["mde80"] = e_tab.mde80.map(lambda x: f(x))
    e_tab["umbral"] = e_tab.umbral.map(lambda x: f(x))
    cal_t = cal[["cod_ine", "fecha_original", "dosis", "fecha_codificada_mes", "fecha_codificada_trimestre", "calidad_fecha"]].copy()
    cal_t["fecha_original"] = cal_t.fecha_original.dt.strftime("%Y-%m-%d")
    cal_t["dosis"] = cal_t.dosis.map(lambda x: f"{x:+.0f}")
    var = tab[(tab.rol == "variante") & tab.id.str.startswith("E8-R1-")][["id", "nota", "estado", "coef", "se", "p_t", "p_aleat", "q_by"]].copy()
    for c in ("coef", "se"):
        var[c] = var[c].map(lambda x: f(x))
    for c in ("p_t", "p_aleat", "q_by"):
        var[c] = var[c].map(lambda x: f(x, 3))
    var["nota"] = var.nota.str.slice(0, 100)
    ad = pd.DataFrame({"adelanto (trimestres antes)": [f"−{k}" for k in di["adelantos"]["ks"]], "gap": [f(x) for x in di["adelantos"]["g"]],
                       "p (aleatorización)": [f(di["adelantos"]["p_k"][k], 3) for k in di["adelantos"]["ks"]]})
    txt = f"""# V18 · E8 · Fiscalidad de la compra: ITP por comunidades

**Análisis V18; capa C4; pre-registro interno plan-replicacion-v18.** Nivel de evidencia EXPLORATORIO. La clasificación V18 va en `clasificacion_v18` y no cambia la capa. {I8}.
Código: `src/v18/estimacion/e8_itp.py` (+ `e8_datos.py`, `e8_diseno.py`, `e8_estim.py`, `e8_salidas.py`, `_e2e8_comun.py`); SEED 20261010; sin red; {segundos:.0f} s.
Rótulo del plan (1.8): no se conoce una evaluación española del ITP con diseño (ficha L4); esta sería la primera, con las reservas de la clasificación.

## 1. Resumen
- **E8-R1 (principal)**: Wald-DID de dosis continua sobre el log del valor tasado provincial a 4 trimestres = **{f(r['coef'])} por punto** del tipo general (IC95 por inversión de la aleatorización {f(r['ic_aleat'][0])}; {f(r['ic_aleat'][1])}); p de aleatorización {f(r['p_aleat'], 4)}; p tras Holm (familia E8, m = 2) {f(t.loc['E8-R1', 'p_holm'], 4)}. Clase V18: **{cl['clase']}**.
- El signo es **contrario** al de la referencia (Dolls et al.: −0,03 por pp; razón {f(razon, 2)}, etiqueta «no coherente»). Sin 2012-2013 el signo cambia ({f(v4.coef)}, p de aleatorización {f(v4.p_aleat, 3)}): el calendario de cambios se concentra en la crisis y el diseño no separa el tipo del ciclo.
- **Coprincipal V16-Q6-p** reproducida en la muestra V18: {f(pq['coef'], 6)} por punto (cifra publicada −0,0020); p de aleatorización {f(pq['p_aleat'], 3)}.
- **No estimables**: E8-R2 (compraventas: MDE {f(ne.loc['E8-R2', 'mde80'])} > 0,06 por punto), E8-A2 (municipal: MDE {f(ne.loc['E8-A2', 'mde80'])} > 0,06), E8-A1 (recaudación sin datos), E8-X1 y E8-X2 (sin compraventas por tramo ni calendario de tipos reducidos). E8-P-Q6v hereda la no estimabilidad de E8-R2.
- Ninguna estimación IDENTIFICADO: no hay contradicción con una conclusión publicada (parada G no activada). Lo publicado (Q6-p «no concluyente», Q6-v «descriptivo», ITP «no evaluable con los datos disponibles») no cambia.

## 2. Qué se ha leído y qué queda fuera (sellado)
- Toda serie pasa por `sellado.filtrar` y `holdout.excluir_sellados_v6`. No se lee `data/sealed` ni se ejecuta ningún `evaluate_*`.
- Las 8 comunidades de régimen común no selladas en v6 (Andalucía, Cantabria, Castilla y León, Castilla-La Mancha, Cataluña, Comunitat Valenciana, Extremadura y Galicia) suman 36 provincias (la adenda corrige las 30 del plan). El valor tasado provincial completo 2007T1-2026T2 existe para 30 de ellas (7 comunidades: falta Cantabria y seis provincias con huecos). Las compraventas mensuales (INE) cubren las 36.
- Los territorios forales y Ceuta y Melilla no entran. Los bloques de V15 y V16 no contienen provincias, solo municipios y distritos: no afectan al diseño provincial.

## 3. Calendario de cambios del tipo general y reglas de codificación (adenda R-18)
Reglas: fecha de entrada en vigor; mes de entrada si es día 15 o anterior y, si no, el siguiente (trimestral: el trimestre de ese mes); dosis = variación del tipo general en puntos (en las escalas, el tipo mínimo, que es el «tipo general» de la base); dos cambios de una comunidad a menos de 12 meses se fusionan con la dosis acumulada en la primera fecha. Antes de 2010 no hay datos de tipos: se supone sin cambios en 2007-2009.

**Calidad de las fechas.** La base de intervenciones recoge las memorias de Hacienda (fuente secundaria): las fechas de 1 de enero son aproximadas y las demás constan en la memoria, pero ninguna está contrastada con el BOE ni con el diario autonómico (la fuente `itp_fechas_entrada_en_vigor` es posterior a la etiqueta y no está descargada). Por eso: tope SUGESTIVO (plan 1.8 f), y la variante de fechas del 1 de enero y las de ±3 meses se publican.

{md(cal_t)}

## 4. Estimabilidad (adenda 1.3), calculada antes de mirar los coeficientes
Mínimo de datos: al menos 8 cambios efectivos en 4 comunidades (E8-R1: {ne.loc['E8-R1', 'minimo_datos']}). MDE80 por Monte Carlo (R = 2.000 reasignaciones de los calendarios entre comunidades, con el estimador principal; valor crítico = cuantil 95 % de |β̂| entre las reasignaciones; σ «ya vista»).

{md(e_tab)}

## 5. Resultado de E8-R1 y pruebas B4
- Inferencia principal: aleatorización estudentizada de los calendarios entre {int(t.loc['E8-R1', 'n_comunidades'])} comunidades (Monte Carlo de V18: tamaño 0,0455, APTO); p = {f(r['p_aleat'], 4)}. Alternativas: t con G − 1 = {r['G'] - 1} gl, p = {f(r['p_t'], 4)} (tamaño 0,0655: con valor crítico corregido, p corregido {f(r['p_t_i7'], 4)}); Webb p = {f(t.loc['E8-R1', 'p_webb_no_fiable'], 4)} (rótulo «no fiable»: tamaño 0,12-0,15 con 8 clusters); TWFE de nivel con Driscoll-Kraay {f(di['dk']['coef'])} (p {f(di['dk']['p'], 4)}; «no fiable»).
- Honest DiD: no se usa (con 7-8 clusters la covarianza tiene rango ≤ 7 y el tamaño con M̄ = 0 es 0,17 en el Monte Carlo de V18).
- TOST con δ = 0,015 por pp: intervalo al 90 % ({f(info['tost']['ic90'][0])}; {f(info['tost']['ic90'][1])}), {'dentro' if info['tost']['equivalente'] else 'no dentro'} de ±δ.

**Adelantos** (diferencia del resultado retardado entre unidades que cambian y estables, normalizada por la dosis; contraste conjunto por aleatorización de calendarios, p = {f(di['adelantos']['p_conjunto'], 3)}):

{md(ad)}

- Potencia previa (aproximación de Roth por aleatorización): pendiente detectable al 80 % = {f(di['pendiente']['pendiente_por_trimestre'], 4)} por trimestre; sesgo implicado en la ventana posterior = {f(di['pendiente']['sesgo_post'], 4)}, mayor que la mitad de |referencia| (0,015): prueba débil.
- I de Moran de los residuos medios por provincia del TWFE de la dosis (5 vecinos): I = {f(di['moran']['I'], 3)} (E[I] = {f(di['moran']['E_I'], 3)}), p unilateral = {f(di['moran']['p_unilateral'], 3)}.
- Placebo de fecha (resultado de 8 trimestres antes): {f(di['placebo_fecha']['coef'])}, p = {f(di['placebo_fecha']['p'], 3)}.
- Placebo de resultado (log de la población provincial, anual): {f(di['placebo_resultado']['coef'])}, p = {f(di['placebo_resultado']['p'], 3)}.
- No hay estimación sin 2012-2013 con el mismo signo: v4 = {f(v4.coef)}.

## 6. Variantes enumeradas (anexo A)
Aleatorización con 4.999 permutaciones; q_by = Benjamini-Yekutieli al 10 % dentro de E8-R1.

{md(var)}

## 7. Coprincipal V16-Q6-p
Wald-DID anual 2011-2024 de V16 (año de efecto, ΔY de años consecutivos, año previo al cambio fuera por anticipación) sobre las provincias de las 8 comunidades con valor tasado anual: **{f(pq['coef'], 6)}** por punto (V16: −0,002037; coincide). V16 no daba inferencia (dCDH con aleatorización NO APTO); aquí se añade la aleatorización de calendarios con el coeficiente como estadístico (p = {f(pq['p_aleat'], 3)}, {diag['E8-P-Q6p']['n_prov']} provincias). No se clasifica; entra en la familia de Holm.

## 8. Clasificación (I1-I8 revisados)
- **E8-R1: {cl['clase']}.** Razones: {'; '.join(cl['razones'])}.
- I6: razón con la referencia {f(razon, 2)} (signo contrario): etiqueta «no coherente»; no interviene en la clase ni en B5.
- Tope SUGESTIVO por: fechas sin contraste con el BOE, ausencia del control de recaudación previa, corrección de un fallo conocido de Q6 y cambio de signo sin 2012-2013 (adenda R-18).
- Lectura: asociación estimada con diseño de dosis continua; no se interpreta como respuesta del mercado al impuesto.

## 9. Desviaciones y lecturas de las reglas (se recogen en docs/v18/desviaciones.md)
- **D1. Fechas.** La fuente de fechas exactas (`itp_fechas_entrada_en_vigor`) no está descargada (sin red): se usan las de la base de intervenciones (Hacienda, fuente secundaria) con las reglas de codificación de la adenda; toda la especificación principal es «con fechas no contrastadas» (tope SUGESTIVO).
- **D2. Recaudación previa.** `itp_recaudacion_ccaa` no está descargada: la principal va sin ese control (tope SUGESTIVO) y E8-A1 es NO ESTIMABLE; E8-R1-v9 coincide con la principal.
- **D3. Valor tasado.** El panel completo 2007T1-2026T2 solo existe para 30 provincias de 7 comunidades (el plan decía 30; la adenda, 36 por recuento de provincias): se declara y se calcula el mínimo de datos con las comunidades presentes.
- **D4. Compraventas.** E8-R2 usa vivienda usada (el ITP grava la usada, plan 1.8 b); la coprincipal V16-Q6-v usaba el total.
- **D5. Códigos INE de MIVAU.** E8-A2: código por nombre dentro de su comunidad con el diccionario oficial del INE (3 de 205 sin resolver).
- **D6. Sun-Abraham.** E8-R1-v5 (subidas) no tiene comunidades nunca tratadas: NO ESTIMABLE. E8-R1-v6 (bajadas) tiene pocas comunidades tratadas (3, una de ellas con la bajada en 2026T2, sin periodo posterior): estimación puntual con p de Webb sin banda de Monte Carlo propia.
- **D7. Adelantos y Roth.** Los adelantos y la pendiente detectable se obtienen por aleatorización de calendarios (sin covarianza analítica de los adelantos): son diagnósticos sin Monte Carlo propio.
- **D8. Lectura de la regla de clasificación.** Aplicada literalmente (véase E2, D8); el p tras Holm entre 0,05 y 0,10 es una prueba débil.
- **D9. Coprincipal E8-P-Q6v** no se estima (hereda E8-R2).

## 10. Limitaciones y datos que las resolverían
- Calendario concentrado en 2012-2013 (crisis): el diseño no separa el tipo del ciclo; sin ese tramo el signo cambia.
- 7 comunidades como unidad de tratamiento: la inferencia de aleatorización tiene 5.040 calendarios posibles.
- Fechas exactas de entrada en vigor (BOE y diarios autonómicos), recaudación del ITP por comunidad, compraventas por tramo de precio (Notariado o AEAT, modelo 600) y tipos reducidos (tareas_autor, punto 7).
"""
    (OUT / "informe.md").write_text(txt, encoding="utf-8")
