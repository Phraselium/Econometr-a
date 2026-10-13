#!/usr/bin/env python3
"""V8-F6: fichas V8 del verificador de afirmaciones -> output/v8/fichas_verificador_v8.json y output/v8/verificador_v8.md.

Cada ficha evalúa una AFIRMACIÓN frecuente sobre por qué ha subido la vivienda (nunca a quien la formula) con la evidencia de V8, su capa y las
cifras con id «V8-» (leídas de output/v8/F6/hechos.json, escrito por src/v8/f6_hechos.py; nunca tecleadas). Mismo formato que las fichas de v7.1
(output/v7_1/fichas/fichas_verificador.json). Regla: con capa C4 el veredicto es como máximo «ANALIZADA, NO CONCLUYENTE»; con C3s, los resultados
valen solo condicionados a las restricciones de signo y de cero de M2. Determinista y sin red.
Uso: python3 src/v8/f6_verificador.py
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import pandas as pd

RAIZ = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(RAIZ / "src" / "v8"))
import render_v8 as RV  # noqa: E402  (reutiliza el formato de src/v5/render.py)

OUT = RAIZ / "output" / "v8"
H = pd.DataFrame(json.loads((OUT / "F6" / "hechos.json").read_text(encoding="utf-8"))).set_index("id")
USADOS: list[str] = []
COND = "condicionado a las restricciones de signo y de cero de M2"
NC = "ANALIZADA, NO CONCLUYENTE"
REGLA_C4 = "Con capa C4 el veredicto es como máximo ANALIZADA, NO CONCLUYENTE."
REGLA_C3S = ("Con capa C3s los resultados valen solo " + COND + "; ninguna regla de V8 designa un factor (0 de 10 celdas), de modo que la afirmación no se "
             "puede ni respaldar ni descartar con este diseño.")
METODO_SVAR = ("Método: SVAR bayesiano con restricciones de signo y de cero (Rubio-Ramírez, Waggoner y Zha, 2010; Arias, Rubio-Ramírez y Waggoner, 2018). "
               "Referencias NO VERIFICADAS (DOI Crossref y cuartil Scimago pendientes).")


def c(i: str, campo: str | None = None) -> str:
    """Cifra formateada como en los entregables (src/v5/render.py) y registro del id usado."""
    USADOS.append(i)
    return RV.texto(H.loc[i].rename(i).astype(object), campo)


def incluye_cero(*ids: str) -> bool:
    return all(H.loc[i, "min"] <= 0 <= H.loc[i, "max"] for i in ids)


def ficha(i, tema, enun, magnitud, intervalo, limites, capa, veredicto, regla, evidencia, literatura="No aplica.") -> dict:
    ids = sorted(set(USADOS))
    USADOS.clear()
    return {"id": i, "tema": tema, "enunciado": enun, "magnitud": magnitud, "intervalo": intervalo, "literatura": literatura, "limites": limites,
            "evidencia": evidencia + ["output/v8/F6/hechos.json", "docs/v8/plantillas/README.md"], "ids_cifras": ids, "capa": capa, "cota": "—",
            "veredicto": veredicto, "regla": regla, "version": "V8"}


def fichas() -> list[dict]:
    f = []
    h = H.loc["V8-M9-shap-a-P5-demanda_externa"]
    FUERA_A_P5 = ("" if h["min"] <= h["valor"] <= h["max"] else
                  " (en el alquiler de P5 el punto queda fuera de su banda del 68 %: el punto SHAP no es el centro de la banda bootstrap)")
    R = [i for i in H.index if i.startswith("V8-REGLA-")]
    n_des = int(H.loc[R, "valor"].sum())
    for i in R:
        USADOS.append(i)
    m7 = json.loads((OUT / "M7" / "resultado.json").read_text(encoding="utf-8"))["estimacion"]["cumplen"]
    assert all("demografia" in x and x.startswith("alquiler") for x in m7), "texto de V8-V2 desfasado respecto a M7"

    # V8-V1 · tipos de interés
    assert incluye_cero(*[f"V8-SVAR-c-P{p}-credito_tipos-media" for p in range(1, 6)])
    f.append(ficha(
        "V8-V1", "Tipos de interés y crédito", "Los tipos de interés bajos y el crédito abundante explican la subida del precio de la vivienda de compra.",
        f"SVAR de 7 variables (C3s, {COND}): contribución de crédito y tipos a la variación del precio real de compra, media y banda del 68 %: "
        f"P2 {c('V8-SVAR-c-P2-credito_tipos-media')}; P4 {c('V8-SVAR-c-P4-credito_tipos-media')}; P5 {c('V8-SVAR-c-P5-credito_tipos-media')} (versión larga en P1: "
        f"{c('V8-SVAR-c-P1-credito_tipos-media')}). Las cinco bandas incluyen el 0. H8-2 (en P5, contribución negativa de crédito y tipos a la compra): p de Holm "
        f"{c('V8-H8-2-pholm')}, no respaldada. Instrumento externo (shocks monetarios del BCE, H8-5): F efectivo {c('V8-H8-5-F')} (umbral 10), instrumentos que cumplen "
        f"las condiciones de C3: {c('V8-M5-c3', 'num')} de 3; sin lectura causal (C4).",
        "Bandas del 68 % de la contribución (por periodo); intervalo al 95 % de H8-2: " + c("V8-H8-2-est", "rango"),
        "Las magnitudes del SVAR pueden estar atenuadas (solo restricciones de impacto en V3); el instrumento monetario es débil; el signo positivo del tipo real con el precio en el multiverso no se lee como efecto (la inflación entra en el tipo real y en el deflactor del precio, y no se descarta el sentido inverso); no se designa ningún factor "
        "como el más relevante en ningún periodo.", "C3s", NC, REGLA_C3S,
        ["output/v8/M2/resumen.md", "output/v8/M5/resumen.md", "output/v8/F5/fichas.md", "docs/v8/hipotesis.md"], METODO_SVAR))

    # V8-V2 · demografía e inmigración
    assert incluye_cero(*[f"V8-SVAR-a-P{p}-demografia-media" for p in (2, 3, 5)])
    f.append(ficha(
        "V8-V2", "Demografía e inmigración", "El crecimiento de la población y la inmigración explican sobre todo la subida del alquiler.",
        f"SVAR (C3s, {COND}): contribución de la demografía a la variación del alquiler real, media y banda del 68 %: P2 {c('V8-SVAR-a-P2-demografia-media')}; "
        f"P3 {c('V8-SVAR-a-P3-demografia-media')}; P5 {c('V8-SVAR-a-P5-demografia-media')}. H8-1 (en P5, contribución positiva de la demografía al alquiler): "
        f"p de Holm {c('V8-H8-1-pholm')}, no respaldada. Multiverso (C4, asociación): {c('V8-M7-cumplen', 'num')} de {c('V8-M7-combinaciones', 'num')} combinaciones "
        f"cumplen la regla por familias, ambas de demografía en el alquiler (periodo P2 y periodo completo, signo positivo); por variables, {c('V8-M7-var-cumplen', 'num')} de {c('V8-M7-var-total', 'num')}. La población total y la extranjera son casi colineales (correlación {c('V8-M6-colpob-completo-corr')} en la muestra completa), de modo que sus filas no son pruebas independientes. Instrumento de empuje migratorio (H8-7): F efectivo "
        f"{c('V8-H8-7-F')}, no cumple C3. Contabilidad hogares-viviendas (asociación): vota a favor de la demografía en {c('V8-M4-voto-demografia', 'num')} celdas (compra P3 y P5).",
        "Bandas del 68 % de la contribución (las tres citadas incluyen el 0)",
        "Demografía y oferta no se separan en la contabilidad; población total y extranjera colineales; el instrumento migratorio tiene 20 observaciones anuales y F muy bajo; la asociación del multiverso "
        "no distingue causa de comovimiento.", "C3s", NC, REGLA_C3S,
        ["output/v8/M2/resumen.md", "output/v8/M5/resumen.md", "output/v8/M7/resumen.md", "output/v8/M4/resumen.md"], METODO_SVAR))

    # V8-V3 · turismo
    f.append(ficha(
        "V8-V3", "Viviendas turísticas", "El turismo y las viviendas de uso turístico explican la subida del alquiler.",
        f"El factor de turismo no entra en el SVAR (M2). Solo hay datos utilizables en {c('V8-M9-turismo-ccaa', 'num')} de 17 CCAA y para P4 y P5. Sensibilidad no principal "
        "(valores ausentes nativos de LightGBM), media de las 6 CCAA con datos de turismo; no comparable con la variación nacional. Contraste del modelo de "
        f"aprendizaje automático (C4, no es un efecto): contribución SHAP media del turismo al alquiler, con banda del 68 %: P4 {c('V8-M9-shap-a-P4-turismo')}; "
        f"P5 {c('V8-M9-shap-a-P5-turismo')}; en la compra, P4 {c('V8-M9-shap-c-P4-turismo')} y P5 {c('V8-M9-shap-c-P5-turismo')}. Ninguna de estas cifras es la variante principal.",
        "Bandas del 68 % del bootstrap de bloques (el punto puede quedar fuera de la banda)",
        "Sin identificación, cobertura parcial y periodos P1-P3 sin datos de turismo; SHAP describe cómo el modelo usa la variable y no identifica efectos. "
        "Véanse las fichas anteriores sobre viviendas turísticas (v3, v6) para el análisis municipal.", "C4", NC, REGLA_C4,
        ["output/v8/M9/resumen.md", "output/v8/F5/fichas.md"]))

    # V8-V4 · compradores extranjeros
    f.append(ficha(
        "V8-V4", "Compradores extranjeros", "La demanda de compradores extranjeros es el principal motor de la subida del precio de la vivienda.",
        f"En V8 la demanda externa solo se contrasta con aprendizaje automático (C4, no es un efecto), en el panel de 17 CCAA: contribución SHAP media a la variación del "
        f"precio real de compra, con banda del 68 %: P3 {c('V8-M9-shap-c-P3-demanda_externa')}; P5 {c('V8-M9-shap-c-P5-demanda_externa')}; al alquiler en P5 "
        f"{c('V8-M9-shap-a-P5-demanda_externa')}{FUERA_A_P5}. No es un shock identificado en el SVAR. El peso de las compraventas con comprador extranjero (cifra de v4, "
        "C4, id compradores_extranjeros en cifras_clave) no mide su efecto sobre el precio.",
        "Bandas del 68 % del bootstrap de bloques", "Sin identificación; fuentes de compradores extranjeros no independientes entre sí; la demanda externa es colineal "
        "con tipos y actividad.", "C4", NC, REGLA_C4, ["output/v8/M9/resumen.md", "output/v8/F5/fichas.md"]))

    # V8-V5 · oferta
    f.append(ficha(
        "V8-V5", "Oferta de vivienda", "La falta de construcción (oferta insuficiente) explica la subida del precio de la vivienda.",
        f"SVAR (C3s, {COND}): contribución de la oferta a la variación del precio real de compra, media y banda del 68 %: P2 {c('V8-SVAR-c-P2-oferta-media')}; "
        f"P4 {c('V8-SVAR-c-P4-oferta-media')}; P5 {c('V8-SVAR-c-P5-oferta-media')}; al alquiler en P4 {c('V8-SVAR-a-P4-oferta-media')}. En el largo plazo (M4), el ARDL con cotas "
        f"rechaza la no cointegración en {c('V8-M4-ardl-rechaza', 'num')} de {c('V8-M4-ardl-total', 'num')} especificaciones (asociación, C4), y la que añade la oferta es inconcluyente.",
        "Bandas del 68 % de la contribución", "La oferta y la demanda específica de vivienda se identifican por signos opuestos en el precio y las compraventas; el "
        "signo estimado no distingue por sí mismo escasez de otros canales.", "C3s", NC, REGLA_C3S,
        ["output/v8/M2/resumen.md", "output/v8/M4/resumen.md"], METODO_SVAR))

    # V8-V6 · empleo y renta
    f.append(ficha(
        "V8-V6", "Empleo y renta", "La mejora del empleo y de la renta explica la subida del precio de la vivienda.",
        f"SVAR (C3s, {COND}): empleo y renta es el factor con mayor contribución media en compra P1 (versión larga): {c('V8-SVAR-c-P1-empleo_renta-media')}, con P(f*) = "
        f"{c('V8-PFSTAR-c-P1')} y {c('V8-VOTOS-c-P1', 'num')} de 4 votos; en P5 {c('V8-SVAR-c-P5-empleo_renta-media')}. H8-3 (en P3, contribución positiva de actividad y renta "
        f"a la compra): estimación {c('V8-H8-3-est')} y p de Holm {c('V8-H8-3-pholm')}, no respaldada. M0 (exploratorio): {c('V8-M0-cumplen', 'num')} de "
        f"{c('V8-M0-coef', 'num')} coeficientes cumplen la regla de §8 ({c('V8-M0-evaluables', 'num')} evaluables; la del alquiler es «no evaluable», no incumplida) y ninguno sobrevive a BH.",
        "Bandas del 68 % de la contribución; intervalo al 95 % de H8-3: " + c("V8-H8-3-est", "rango"),
        "Empleo y renta compite con demografía y crédito; P1 usa una versión de 4 variables desde 1995T2; no se designa factor en ningún periodo.", "C3s", NC,
        REGLA_C3S, ["output/v8/M2/resumen.md", "output/v8/M0/resumen.md", "output/v8/F5/fichas.md"], METODO_SVAR))

    # V8-V7 · factor europeo
    f.append(ficha(
        "V8-V7", "Factor europeo", "La subida en España forma parte de un movimiento común europeo del precio de la vivienda.",
        f"El factor común español covaría positivamente con el crecimiento del precio de la vivienda de la zona euro (EA19): correlación {c('V8-H8-9-est')} "
        f"(H8-9; p de Holm {c('V8-H8-9-pholm')}, rechazada la ausencia de relación; la zona euro incluye a España). En compra P2, la parte asociada al precio europeo "
        f"es {c('V8-M1-eur-c-P2')}. En cambio, H8-8 (el componente común de las 17 CCAA explica más del 50 % de la varianza en cada periodo) no se rechaza: cuota mínima "
        f"{c('V8-H8-8-est')}, p de Holm {c('V8-H8-8-pholm')}. Todo es asociación estadística (C4): un factor común resume comovimiento, no una causa.",
        "Intervalo al 95 % de la correlación: " + c("V8-H8-9-est", "rango") + "; bandas del 68 % de la parte europea",
        "La zona euro sin España no es construible con los pesos oficiales (se usa una aproximación de 5 países como sensibilidad); con 17 CCAA y pocos trimestres la cuota "
        "del primer componente está sesgada al alza.", "C4", NC, REGLA_C4, ["output/v8/M1/resumen.md", "output/v8/F5/fichas.md"]))

    # V8-V8 · factor único
    f.append(ficha(
        "V8-V8", "Un factor único", "Hay un único factor que explica la subida de la vivienda en cada periodo y se puede identificar.",
        f"Regla de §9 (tres de cuatro métodos, multiverso orientado ≥ 80 % y banda del 68 % del SVAR que excluya el 0), fijada antes de calcular: se designa un factor en "
        f"{n_des} de 10 celdas (mercado, periodo). Cuota no atribuida (parte determinista y no identificada del SVAR), compra P1: {c('V8-QNA-c-P1')} de la variación; "
        f"compra P5: {c('V8-QNA-c-P5')}. Ejemplo de ranking incierto: en compra P3, P(f*) del primero = {c('V8-PFSTAR-c-P3')}.",
        "Bandas del 68 % de la cuota no atribuida (fracción de la variación observada)",
        "No designar un factor no prueba que no exista uno dominante; indica que los métodos no coinciden con la incertidumbre actual. P4 (9 trimestres) y alquiler P1 "
        "(sin datos) no se designan por regla.", "C3s", NC, REGLA_C3S, ["output/v8/F5/resumen.md", "output/v8/F5/fichas.md", "docs/v8/desviaciones.md"], METODO_SVAR))

    # V8-V9 · predicción
    f.append(ficha(
        "V8-V9", "Capacidad predictiva", "Los modelos econométricos y de aprendizaje automático predicen el precio y el alquiler mejor que un modelo sencillo.",
        f"Tabla común fuera de muestra (2016T2-2026T1, misma muestra, embargo de 4 trimestres), RMSE del crecimiento trimestral real de compra: AR(4) {c('V8-OOS-c-ar4-rmse')}; "
        f"ECM v1 {c('V8-OOS-c-ecm_v1-rmse')}; BVAR de M2 {c('V8-OOS-c-bvar_m2-rmse')}. Alquiler: AR(4) {c('V8-OOS-a-ar4-rmse')}; ECM v1 {c('V8-OOS-a-ecm_v1-rmse')}; BVAR "
        f"{c('V8-OOS-a-bvar_m2-rmse')}. Ningún modelo supera a la base más exigente (el AR(4)); el ECM v1 es peor con p de Holm {c('V8-OOS-c-ecm_v1-pholm')} (compra). "
        f"M9 (nacional, compra): mejor modelo de aprendizaje automático {c('V8-M9-oos-c-nacional-ml')} frente a {c('V8-M9-oos-c-nacional-base')} del AR(4); modelos que superan "
        f"a la base tras BH: {c('V8-M9-oos-c-nacional-mejor', 'num')}.",
        "Contraste Diebold-Mariano con corrección de Harvey-Leybourne-Newbold; p ajustados por Holm", "El bloque de prueba es corto (40 trimestres); explicar y predecir son tareas distintas "
        "(un modelo puede ser útil para atribuir sin predecir mejor).", "C4", NC, REGLA_C4, ["output/v8/F5/fuera_muestra_comun.csv", "output/v8/M9/resumen.md"]))
    return f


MARC_INI, MARC_FIN = "<!-- V8:inicio (generado por src/v8/f6_verificador.py; no editar a mano) -->", "<!-- V8:fin -->"
NOTA_CAB = ("Nota V8 (2026-10-13): este historial incluye V8; las filas de V8 están en la adenda «Adenda V8» del final, con la columna «Estado en V8 y porqué». "
            "Las filas anteriores no se modifican.")


def historial() -> None:
    """Añade (o refresca) la adenda V8 de docs/v6_1/historial_conclusiones.md, con cifras leídas de hechos.json."""
    p = RAIZ / "docs" / "v6_1" / "historial_conclusiones.md"
    t = p.read_text(encoding="utf-8")
    if NOTA_CAB not in t:
        lineas = t.split("\n")
        lineas.insert(1, "")
        lineas.insert(2, NOTA_CAB)
        t = "\n".join(lineas)
    if MARC_INI in t:
        t = t[:t.index(MARC_INI)].rstrip("\n") + "\n"
    N = "nacional"
    F = [
        ("Demografía e inmigración", "Alquiler real", f"P5 (2022T3-2026T2): {c('V8-SVAR-a-P5-demografia-media')}; multiverso: {c('V8-M7-cumplen', 'num')} de {c('V8-M7-combinaciones', 'num')} combinaciones por familias y {c('V8-M7-var-cumplen', 'num')} de {c('V8-M7-var-total', 'num')} por variables",
         "SVAR (C3s); multiverso (C4); IV migratorio (C4)", "+ en el multiverso (alquiler P2 y completo); 0 en el SVAR", "C3s / C4",
         "**Se mantiene** (no concluyente): la banda del SVAR incluye el 0 y el instrumento migratorio no tiene primera etapa (F " + c("V8-H8-7-F") + "); solo la asociación del multiverso es estable en alquiler"),
        ("Tipos de interés y crédito", "Precio real de compra", f"P5: {c('V8-SVAR-c-P5-credito_tipos-media')}; P2: {c('V8-SVAR-c-P2-credito_tipos-media')}", "SVAR (C3s); IV monetario (C4)",
         "no distinguible de 0", "C3s / C4", "**Se mantiene** (no concluyente): H8-2 no respaldada (p de Holm " + c("V8-H8-2-pholm") + ") y el instrumento monetario es débil (F " + c("V8-H8-5-F") + ")"),
        ("Empleo y renta", "Precio real de compra", f"P1 (larga): {c('V8-SVAR-c-P1-empleo_renta-media')}; P5: {c('V8-SVAR-c-P5-empleo_renta-media')}", "SVAR (C3s); M0 (C4)", "+ en la media posterior, con banda que incluye el 0 salvo P1",
         "C3s / C4", "**Se mantiene** (no concluyente): es el factor con mayor media en compra P1 y P5, pero la regla del §9 no designa ninguno (" + c("V8-VOTOS-c-P1", "num") + " de 4 votos en P1)"),
        ("Oferta", "Precio real de compra", f"P5: {c('V8-SVAR-c-P5-oferta-media')}; P2: {c('V8-SVAR-c-P2-oferta-media')}", "SVAR (C3s); ARDL con cotas (C4)", "signo según periodo", "C3s / C4",
         "**Se mantiene** (no concluyente): bandas con el 0; cointegración solo en " + c("V8-M4-ardl-rechaza", "num") + " de " + c("V8-M4-ardl-total", "num") + " especificaciones"),
        ("Turismo y viviendas turísticas", "Alquiler real", f"SHAP P5: {c('V8-M9-shap-a-P5-turismo')}; CCAA con datos: {c('V8-M9-turismo-ccaa', 'num')} de 17", "ML interpretable (C4, contraste)", "no concluyente", "C4",
         "**Se mantiene** (no concluyente): cobertura de turismo parcial y solo P4-P5; el SVAR no lo incluye"),
        ("Demanda externa y compradores extranjeros", "Precio real de compra", f"SHAP P5: {c('V8-M9-shap-c-P5-demanda_externa')}", "ML interpretable (C4, contraste)", "+ pequeño en P5", "C4",
         "**Se mantiene** (no concluyente): contribución pequeña en el contraste de aprendizaje automático y sin identificación"),
        ("Factor europeo (nuevo en V8)", "Crecimiento del precio de compra", f"correlación con la zona euro {c('V8-H8-9-est')}; parte europea en P2: {c('V8-M1-eur-c-P2')}", "Factor común (PCA/DFM); bootstrap por bloques",
         "+", "C4", "**Nuevo**: asociación positiva (H8-9, p de Holm " + c("V8-H8-9-pholm") + "); el factor común no supera el 50 % de la varianza en todos los periodos (H8-8, p de Holm " + c("V8-H8-8-pholm") + "); sin lectura causal"),
        ("Un factor único (regla del §9)", "Precio real de compra y alquiler real", f"{n_des(c)} de 10 celdas designadas", "Regla de 4 votos, multiverso y banda del SVAR", "—", "C3s / C4",
         "**Nuevo**: ningún factor se designa como el más relevante en ningún periodo; se publican rankings con incertidumbre"),
        ("Predicción fuera de muestra", "Crecimiento trimestral real", f"RMSE compra: AR(4) {c('V8-OOS-c-ar4-rmse')}, ECM v1 {c('V8-OOS-c-ecm_v1-rmse')}, BVAR {c('V8-OOS-c-bvar_m2-rmse')}", "Diebold-Mariano con Holm",
         "—", "C4", "**Se mantiene** (K1): ningún modelo supera al AR(4) en la misma muestra"),
    ]
    L = [MARC_INI, "", "## Adenda V8 (por qué ha subido la vivienda: factores, periodos y factor común, 2026-10-13)", "",
         "Una fila por factor. Las cifras salen de `output/v5/cifras_clave.csv` (ids `V8-`); los resultados del SVAR (C3s) valen solo condicionados a las restricciones de signo y de "
         "cero de M2; el resto es asociación (C4). Sin lectura causal por debajo de C3/C3s.", "",
         "| Factor | Medida de resultado | Magnitud | Método | Signo | Capa | Estado en V8 y porqué | Fuente |", "|---|---|---|---|---|---|---|---|"]
    for fac, med, mag, met, sig, capa, est, *_ in F:
        L.append(f"| {fac} | {med} | {mag} | {met} | {sig} | {capa} | {est} | output/v8/F6/hechos.json; output/v8/F5/resumen.md |")
    L += ["", MARC_FIN]
    p.write_text(t.rstrip("\n") + "\n\n" + "\n".join(L) + "\n", encoding="utf-8")


def n_des(cf) -> str:
    return str(int(H.loc[[i for i in H.index if i.startswith("V8-REGLA-")], "valor"].sum()))


def main() -> None:
    f = fichas()
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "fichas_verificador_v8.json").write_text(json.dumps(f, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    ver = ["# Verificador V8 (por qué ha subido la vivienda: factores, periodos y factor común)", "",
           "Generado por `src/v8/f6_verificador.py`. Cada ficha evalúa una afirmación, nunca a quien la formula, y se aplican las mismas reglas a todas. Complementa el "
           "verificador principal (output/v5/verificador) y las fichas de V7 (output/v7_1/verificador_v7_1.md), cuyos recuentos no cambian. Capas: C3s = identificación por "
           "restricciones de signo y de cero explícitas, válida solo bajo ellas; C4 = exploratorio o asociación. Las cifras llevan el id de `cifras_clave` (campo «ids_cifras»).", ""]
    for x in f:
        ver += [f"## {x['id']} · {x['tema']}", "", f"**Afirmación evaluada:** {x['enunciado']}", "", f"**Veredicto:** {x['veredicto']} ({x['capa']})", "",
                f"**Magnitud:** {x['magnitud']}", "", f"**Intervalo:** {x['intervalo']}", "", f"**Límites:** {x['limites']}", "", f"**Regla:** {x['regla']}", "",
                f"**Literatura:** {x['literatura']}", "", "**Evidencia:** " + "; ".join(x["evidencia"]), "", "**Ids de cifras:** " + ", ".join(x["ids_cifras"]), ""]
    (OUT / "verificador_v8.md").write_text("\n".join(ver), encoding="utf-8")
    historial()
    print(f"f6_verificador: {len(f)} fichas V8 y adenda V8 del historial")


if __name__ == "__main__":
    main()
