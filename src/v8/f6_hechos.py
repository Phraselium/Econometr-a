#!/usr/bin/env python3
"""V8-F6: hechos estándar de V8 (lista con el formato de output/v7_1/S3/hechos.json) -> output/v8/F6/hechos.json.

Todo se LEE de las salidas versionadas de output/v8/ (M0-M9, F5); nada se teclea salvo etiquetas (nombres de periodos y de factores).
Los ids llevan el prefijo «V8-». Lo recoge src/v5/cifras_clave.py (output/v8/*/hechos.json). Determinista (SEED = 20261010) y sin red.
Capas: svar_hd = C3s (condicionada a las restricciones de signo y de cero de M2); el resto, C4 (asociación o descriptivo).
Uso: python3 src/v8/f6_hechos.py
"""
from __future__ import annotations

import json
import math
import re
from pathlib import Path

import pandas as pd

RAIZ = Path(__file__).resolve().parents[2]
OUT = RAIZ / "output" / "v8"
SAL = OUT / "F6"
SEED = 20261010
PERS = ["P1", "P2", "P3", "P4", "P5"]
PER_ETQ = {"P1": "1995T1-2007T4", "P2": "2008T3-2013T4", "P3": "2014T1-2019T4", "P4": "2020T2-2022T2", "P5": "2022T3-2026T2"}   # docs/v8/hipotesis.md §3
MERC = {"compra": "precio real de compra", "alquiler": "alquiler real"}
FACTOR = {"empleo_renta": "empleo y renta", "demografia": "demografía", "credito_tipos": "crédito y tipos", "oferta": "oferta",
          "demanda_vivienda": "demanda específica de vivienda (shock de M2, no pre-registrado como factor)", "factor_europeo": "factor europeo",
          "demanda_externa": "demanda externa", "turismo": "turismo"}
AMB = {"cv_prov:03": "provincia de Alicante (03)", "cv_prov:12": "provincia de Castellón (12)", "cv_prov:46": "provincia de València (46)",
       "valencia_ciudad": "València ciudad"}
SVAR_FACTORES = ["empleo_renta", "demografia", "demanda_vivienda", "oferta", "credito_tipos"]
NOTA_C3S = "condicionado a las restricciones de signo y de cero de M2"
SENTIDO_SHAP = "min y max = banda del 68 % del bootstrap de bloques (el punto SHAP puede quedar fuera de la banda: no es rango del valor)"
HECHOS: list[dict] = []


def _fin(x):
    return x is not None and not (isinstance(x, float) and not math.isfinite(x)) and not pd.isna(x)


def _tr(q: str) -> str:
    return q.replace("Q", "T")


def _ultimo_trim() -> str:
    d = pd.read_csv(RAIZ / "data" / "processed" / "v8" / "nacional_q_v8.csv", usecols=["trimestre"])
    return _tr(str(d.trimestre.iloc[-1]))


def _fechas() -> dict[str, str]:
    """Último trimestre de dato usado por módulo, leído de sus salidas (rango «AAAAQn-AAAAQn» o ventana)."""
    base = _ultimo_trim()
    f = {k: base for k in ("M0", "M1", "M6", "M7", "M8", "M9")}

    def ult(txt: str) -> str | None:
        m = sorted(re.findall(r"(20\d\d)Q([1-4])", txt))
        return f"{m[-1][0]}T{m[-1][1]}" if m else None   # el último trimestre = el máximo de los citados
    j = json.loads((OUT / "M2" / "resultado.json").read_text(encoding="utf-8"))
    f["M2"] = ult(str(j["datos"])) or base
    c = pd.read_csv(OUT / "M4" / "cointegracion.csv")
    f["M4"] = ult(" ".join(c.ventana.astype(str))) or base
    f["M5"] = ult((OUT / "M5" / "resultado.json").read_text(encoding="utf-8")) or base
    f["F5"] = ult(json.dumps(json.loads((OUT / "F5" / "resultado.json").read_text(encoding="utf-8"))["N"])) or base
    return f


def add(i, ind, val, mn, mx, uni, per, cob, fue, capa, fecha, sentido="rango"):
    r = {"id": i, "indicador": ind, "valor": float(val) if _fin(val) else None, "min": float(mn) if _fin(mn) else None,
         "max": float(mx) if _fin(mx) else None, "unidad": uni, "periodo": per, "cobertura": cob, "fuentes": fue, "capa": capa,
         "fecha_dato": fecha, "sentido_min_max": sentido}
    if r["valor"] is None and r["min"] is None and r["max"] is None:
        return
    assert i not in {h["id"] for h in HECHOS}, f"id duplicado {i}"
    if sentido == "rango" and r["valor"] is not None and r["min"] is not None and r["max"] is not None:
        assert r["min"] - 1e-9 <= r["valor"] <= r["max"] + 1e-9, f"{i}: valor fuera de [min, max]"
    HECHOS.append(r)


def _retro(fin: str, n: int) -> str:
    """Trimestre inicial de una ventana de n trimestres que termina en `fin` (AAAATq)."""
    a, q = int(fin[:4]), int(fin[-1])
    k = a * 4 + (q - 1) - (n - 1)
    return f"{k // 4}T{k % 4 + 1}"


def _n_per(p: str) -> int:
    ini, fin = PER_ETQ[p].split("-")
    return (int(fin[:4]) * 4 + int(fin[-1])) - (int(ini[:4]) * 4 + int(ini[-1])) + 1


def per_txt(p: str, m: str | None = None) -> str:
    t = f"{p} ({PER_ETQ[p]})"
    if p == "P1" and m == "alquiler":
        t = f"{p} (sin datos de alquiler)"
    if p == "P5":
        t = f"{p} (2022T3-último dato)"
    return t


def f5_reglas(F: dict) -> None:
    R = pd.read_csv(OUT / "F5" / "regla_s9.csv")
    fue = "F5 (regla del §9 sobre M2, M6, M5, M4, M7); nacional_q_v8"
    for r in R.itertuples():
        m, p = r.mercado, r.periodo
        k, pt = f"{'c' if m == 'compra' else 'a'}-{p}", per_txt(p, m)
        cob = f"España (nacional); {m}"
        add(f"V8-OBS-{k}", f"Variación observada de {MERC[m]} en {p} (pp, log×100; unidad común R0)", r.delta_y_pp, None, None, "pp", pt, cob,
            "nacional_q_v8 (valor tasado del Ministerio; IPC de alquiler del INE)", "C4", F["F5"])
        if _fin(r.cuota_no_atribuida):
            add(f"V8-QNA-{k}", f"Cuota no atribuida de la variación de {MERC[m]} en {p} (parte determinista y no identificada del SVAR, banda del 68 %; "
                f"{NOTA_C3S}; fracción de la variación observada, puede superar 1 o ser negativa si la variación es pequeña)", r.cuota_no_atribuida, r.cuota_b68_lo,
                r.cuota_b68_hi, "proporción", pt, cob, fue, "C3s", F["F5"])
            add(f"V8-QNA-pp-{k}", f"Cuota no atribuida de {MERC[m]} en {p} en puntos (banda del 68 %; {NOTA_C3S})", r.cuota_no_atribuida_pp,
                r.cuota_b68_lo_pp, r.cuota_b68_hi_pp, "pp", pt, cob, fue, "C3s", F["F5"])
        if _fin(r.p_fstar):
            add(f"V8-PFSTAR-{k}", f"Probabilidad posterior de que {FACTOR[r.voto_svar_hd]} sea el factor de mayor contribución en {MERC[m]} en {p} "
                f"(P(f*); {NOTA_C3S})", 100 * r.p_fstar, None, None, "%", pt, cob, fue, "C3s", F["F5"])
        if _fin(r.n_votos) and isinstance(r.factor_evaluado, str):
            add(f"V8-VOTOS-{k}", f"Votos máximos (de 4 métodos) a un mismo factor en {MERC[m]} en {p}: {FACTOR[r.factor_evaluado]}", r.n_votos, None, None,
                "votos", pt, cob, fue, "C4", F["F5"])
        capa = str(r.capa).split()[0]
        ev = FACTOR.get(r.factor_evaluado, "ninguno") if isinstance(r.factor_evaluado, str) else "ninguno"
        add(f"V8-REGLA-{k}", f"Resultado de la regla del §9 en {MERC[m]} en {p}: {r.resultado} (factor evaluado: {ev}); 1 = designado, 0 = no designado",
            1.0 if r.resultado == "designado" else 0.0, None, None, "designado (0/1)", pt, cob, fue, capa, F["F5"])


def svar(F: dict) -> None:
    c = pd.read_csv(OUT / "F5" / "atribucion_combinada.csv")
    s = c[(c.metodo == "svar_hd") & c.factor.isin(SVAR_FACTORES)]
    for r in s.itertuples():
        m, p, f = r.mercado, r.periodo, r.factor
        k = f"{'c' if m == 'compra' else 'a'}-{p}-{f}"
        ver = "versión larga de 4 variables" if r.variante == "larga" else "SVAR de 7 variables, variante principal V3"
        cob = f"España (nacional); {m}; {ver}"
        fue = "M2 SVAR bayesiano con restricciones de signo y de cero (descomposición histórica); nacional_q_v8"
        add(f"V8-SVAR-{k}-media", f"Contribución de {FACTOR[f]} a la variación de {MERC[m]} en {p} (media posterior; banda del 68 %; pp log×100; {NOTA_C3S})",
            r.media, r.b68_lo, r.b68_hi, "pp", per_txt(p, m), cob, fue, "C3s", F["M2"] if r.variante != "larga" else F["F5"])
        add(f"V8-SVAR-{k}-mediana", f"Contribución de {FACTOR[f]} a la variación de {MERC[m]} en {p} (mediana posterior; banda del 68 %; pp log×100; {NOTA_C3S})",
            r.mediana, r.b68_lo, r.b68_hi, "pp", per_txt(p, m), cob, fue, "C3s", F["M2"] if r.variante != "larga" else F["F5"])


def hipotesis(F: dict) -> None:
    h = pd.read_csv(OUT / "M2" / "hipotesis_m2.csv")
    for r in h.itertuples():
        i = r.id
        cob = f"España (nacional); {r.mercado}"
        add(f"V8-{i}-est", f"{i}: {r.hipotesis} (contribución acumulada del periodo, intervalo al 95 %; {NOTA_C3S})", r.contribucion_pp, r.ic95_lo, r.ic95_hi,
            "pp", per_txt(r.periodo), cob, "M2 SVAR con restricciones de signo y de cero", "C3s", F["M2"])
        add(f"V8-{i}-pholm", f"{i}: p ajustado por Holm (Prob. posterior unilateral; {r.estado})", r.p_holm, None, None, "p-valor", per_txt(r.periodo), cob,
            "M2 SVAR con restricciones de signo y de cero", "C3s", F["M2"])
    h5 = pd.read_csv(OUT / "M5" / "hipotesis_m5.csv")
    for r in h5.itertuples():
        i = r.id
        cob = f"España (nacional); {r.mercado}"
        fue = "M5 proyecciones locales con variable instrumental (IV1/IV2)"
        add(f"V8-{i}-F", f"{i}: F efectivo de la primera etapa ({r.hipotesis}; umbral C3: F ≥ 10)", r.F_efectivo, None, None, "estadístico F", "ver hipótesis", cob, fue, "C4", F["M5"])
        add(f"V8-{i}-tFR", f"{i}: t de la forma reducida (signo esperado {int(r.signo_esperado_forma_reducida):+d})", r.t_forma_reducida, None, None, "estadístico t",
            "ver hipótesis", cob, fue, "C4", F["M5"])
        add(f"V8-{i}-pholm", f"{i}: p ajustado por Holm ({r.lectura})", r.p_holm, None, None, "p-valor", "ver hipótesis", cob, fue, "C4", F["M5"])
    n_c3 = int(h5.cumple_c3.astype(str).str.lower().eq("true").sum())
    add("V8-M5-c3", "Instrumentos de M5 (hipótesis H8-5 a H8-7) que cumplen las condiciones de C3", n_c3, None, None, "instrumentos", "ver hipótesis", "España (nacional)",
        "M5 proyecciones locales con variable instrumental", "C4", F["M5"])
    h1 = pd.read_csv(OUT / "M1" / "hipotesis_m1.csv").set_index("id")
    cuotas = json.loads(h1.loc["H8-8", "estimacion"])
    add("V8-H8-8-est", "H8-8: cuota mínima del componente común de las 17 CCAA en la varianza del crecimiento interanual del precio real de compra (mínimo de los 5 periodos; "
        "prueba de unión-intersección)", 100 * min(cuotas.values()), None, None, "%", "P1-P5", "17 CCAA", "M1 factor común (PCA, bootstrap por bloques)", "C4", F["M1"])
    add("V8-H8-8-pholm", "H8-8: p ajustado por Holm", h1.loc["H8-8", "p_holm"], None, None, "p-valor", "P1-P5", "17 CCAA", "M1 factor común", "C4", F["M1"])
    cr = pd.read_csv(OUT / "M1" / "correlaciones_h89.csv").set_index("variante").loc["principal_ea19_nominal"]
    add("V8-H8-9-est", "H8-9: correlación del factor común español con el crecimiento interanual del precio de la vivienda de la zona euro (EA19; intervalo al 95 %)",
        cr.correlacion, cr.ic95_lo, cr.ic95_hi, "proporción", "1999-último dato", "España y zona euro", "M1 factor común; Eurostat (prc_hpi_q)", "C4", F["M1"])
    add("V8-H8-9-pholm", "H8-9: p ajustado por Holm", h1.loc["H8-9", "p_holm"], None, None, "p-valor", "1999-último dato", "España y zona euro", "M1 factor común; Eurostat",
        "C4", F["M1"])


def m1(F: dict) -> None:
    q = pd.read_csv(OUT / "M1" / "cuota_varianza.csv")
    q = q[(q.k == 1) & (q.metodo == "pca") & q.serie.isin(["compra_tasado", "alquiler_ipc"]) & q.periodo.isin(PERS)]
    for r in q.itertuples():
        m = r.mercado
        add(f"V8-M1-cuota-{'c' if m == 'compra' else 'a'}-{r.periodo}", f"Cuota del primer componente común de las 17 CCAA en la varianza del crecimiento interanual de {MERC[m]} en "
            f"{r.periodo} (banda del 68 %; resumen de comovimiento, sin lectura causal)", 100 * r.cuota, 100 * r.b68_lo, 100 * r.b68_hi, "%", per_txt(r.periodo, m),
            "17 CCAA", "M1 factor común (PCA); panel_ccaa_q_v8 (cruce por código INE)", "C4", F["M1"])
    a = pd.read_csv(OUT / "M1" / "atribucion.csv")
    a = a[(a.factor == "factor_europeo") & (a.principal == "si")]
    for r in a.itertuples():
        mn = re.search(r"n=(\d+)", str(r.notas))
        n = int(mn.group(1)) if mn else None
        pt = per_txt(r.periodo, r.mercado)
        ind = (f"Parte de la variación de {MERC[r.mercado]} en {r.periodo} asociada al precio de la vivienda de la zona euro "
               f"(regresión con retardos 0-1; banda del 68 %; asociación, no causal; la zona euro incluye a España)")
        if n is not None:
            fin = PER_ETQ[r.periodo].split("-")[1]
            ini = _retro(fin, n)
            pt = f"{r.periodo} (ventana efectiva {ini}-{fin}, n = {n})" if n < _n_per(r.periodo) else pt
            ind += f"; n = {n} trimestres"
        add(f"V8-M1-eur-{'c' if r.mercado == 'compra' else 'a'}-{r.periodo}", ind, r.contribucion_pp, r.b68_lo, r.b68_hi, "pp",
            pt, "España (nacional)", "M1 factor común; Eurostat (prc_hpi_q)", "C4", F["M1"])


def m7(F: dict) -> None:
    j = json.loads((OUT / "M7" / "resultado.json").read_text(encoding="utf-8"))
    e, n = j["estimacion"], j["N"]
    fue, cob = "M7 multiverso estructurado", "España (nacional)"
    add("V8-M7-rejilla", "Especificaciones de la rejilla del multiverso (tope 50.000; sin truncar)", n["rejilla"], None, None, "especificaciones", "P1-P5 y completo", cob, fue, "C4", F["M7"])
    add("V8-M7-ajustadas", "Especificaciones del multiverso ajustadas con éxito (las fallidas están en registro.csv)", n["especificaciones_ajustadas"], None, None,
        "especificaciones", "P1-P5 y completo", cob, fue, "C4", F["M7"])
    add("V8-M7-combinaciones", "Combinaciones (mercado, periodo, factor) evaluadas en el multiverso", e["n_factor_periodo_mercado"], None, None, "combinaciones",
        "P1-P5 y completo", cob, fue, "C4", F["M7"])
    add("V8-M7-cumplen", "Combinaciones que cumplen la regla del multiverso (signo orientado estable en ≥ 80 % y significativo tras BH en ≥ 50 %)", e["n_cumplen_multiverso"],
        None, None, "combinaciones", "P1-P5 y completo", cob, fue, "C4", F["M7"])

VAR_ETQ = {"credito_nuevo_real": "crédito nuevo real", "credito_stock_real": "saldo de crédito real", "tipo_hip_real": "tipo hipotecario real", "hogares_epa": "hogares (EPA)",
           "pob_extranj_ine": "población extranjera (INE)", "pob_total": "población total", "ocupados": "ocupados (EPA)", "pib_vol": "PIB en volumen",
           "bis_hpi_xm_real": "precio real de la vivienda de otros países (BIS)", "terminadas": "viviendas terminadas", "visados": "visados de obra nueva"}


def m7_variables(F: dict) -> None:
    """Lectura a nivel de VARIABLE del multiverso (regla §9: signo orientado >= 80 % y significativo tras BH >= 50 %). Complementa la lectura por familias."""
    d = pd.read_csv(OUT / "M7" / "resumen_multiverso.csv")
    v = d[d.variable != "TODAS"]
    ok = v[v.cumple_multiverso.astype(str).str.lower() == "true"]
    fue, cob = "M7 multiverso estructurado (lectura por variable)", "España (nacional)"
    add("V8-M7-var-total", "Combinaciones (mercado, periodo, variable) evaluadas a nivel de variable en el multiverso", len(v), None, None, "combinaciones", "P1-P5 y completo", cob, fue,
        "C4", F["M7"])
    add("V8-M7-var-cumplen", "Combinaciones (mercado, periodo, variable) que cumplen la regla del multiverso a nivel de variable (signo orientado estable en >= 80 % y "
        "significativo tras BH en >= 50 %)", len(ok), None, None, "combinaciones", "P1-P5 y completo", cob, fue, "C4", F["M7"])
    rej = ok[ok.cumple_multiverso_rejilla.astype(str).str.lower() == "true"]
    add("V8-M7-var-cumplen-rejilla", "De ellas, las que siguen cumpliendo si las especificaciones fallidas u omitidas cuentan como «no cumple» (P4 y compra P1: multiverso truncado)",
        len(rej), None, None, "combinaciones", "P1-P5 y completo", cob, fue, "C4", F["M7"])
    for r in ok.itertuples():
        m, per = r.mercado, r.periodo
        k = f"{m[0]}-{per}-{r.variable}"
        pt = "muestra completa" if per == "completo" else per_txt(per, m)
        ori = ("signo orientado " + r.signo_mayoritario + (" (un tipo más bajo cuenta como presión al alza)" if r.variable == "tipo_hip_real" else " (más de la variable, más presión al alza)"))
        base = f"{VAR_ETQ.get(r.variable, r.variable)} ({FACTOR[r.factor]}), {MERC[m]}, {pt}"
        add(f"V8-M7-var-{k}-signo", f"Multiverso por variable: % de especificaciones con el mismo signo, {base}; {ori}; asociación, sin lectura causal",
            100 * r.pct_mismo_signo, None, None, "%", pt, cob, fue, "C4", F["M7"])
        add(f"V8-M7-var-{k}-bh", f"Multiverso por variable: % de especificaciones significativas tras BH (q = 0,10), {base}; {ori}; asociación, sin lectura causal",
            100 * r.pct_sig_bh, None, None, "%", pt, cob, fue, "C4", F["M7"])


def m6_colinealidad(F: dict) -> None:
    """Colinealidad entre población total y población extranjera: VIF/Belsley de M6 (una variable por familia) y correlación directa de los crecimientos interanuales."""
    c = pd.read_csv(OUT / "M6" / "colinealidad.csv")
    fue, cob = "M6 colinealidad (VIF y Belsley); nacional_q_v8", "España (nacional)"
    add("V8-M6-vif-max", "VIF máximo de las ecuaciones de M6 (una variable por familia; ninguna ecuación incluye a la vez la población total y la extranjera)", c.vif.max(), None, None,
        "cociente", "P1-P5", cob, fue, "C4", F["M6"])
    pt = c[c.variable == "pob_total"].sort_values("vif").iloc[-1]
    add("V8-M6-vif-pob_total-max", f"VIF máximo de la población total en las ecuaciones de M6 ({pt.periodo}, {pt.transformacion})", pt.vif, None, None, "cociente", per_txt(pt.periodo),
        cob, fue, "C4", F["M6"])
    n = pd.read_csv(RAIZ / "data" / "processed" / "v8" / "nacional_q_v8.csv", usecols=["trimestre", "d4_ln_pob_total", "d4_ln_pob_extranj_ine"])
    n["trimestre"] = n.trimestre.astype(str).str.replace("Q", "T")
    n = n.dropna()
    ventanas = {"completo": (n.trimestre.iloc[0], n.trimestre.iloc[-1], "muestra completa")}
    for p in ("P2", "P5"):
        a, b = PER_ETQ[p].split("-")
        ventanas[p] = (a, b, per_txt(p))
    for k, (a, b, etq) in ventanas.items():
        w = n[(n.trimestre >= a) & (n.trimestre <= b)]
        r = float(w.d4_ln_pob_total.corr(w.d4_ln_pob_extranj_ine))
        add(f"V8-M6-colpob-{k}-corr", f"Correlación entre el crecimiento interanual de la población total y el de la población extranjera (INE), {etq} (n = {len(w)} trimestres; diagnóstico descriptivo)",
            r, None, None, "proporción", etq, cob, "nacional_q_v8 (d4_ln_pob_total, d4_ln_pob_extranj_ine)", "C4", F["M7"])
        add(f"V8-M6-colpob-{k}-vif", f"VIF del par población total y población extranjera, {etq} (1 / (1 - r²) con dos variables; diagnóstico descriptivo)", 1 / (1 - r * r), None, None,
            "cociente", etq, cob, "nacional_q_v8 (d4_ln_pob_total, d4_ln_pob_extranj_ine)", "C4", F["M7"])


def oos(F: dict) -> None:
    o = pd.read_csv(OUT / "F5" / "fuera_muestra_comun.csv")
    fue, cob = "F5 tabla común fuera de muestra (5 bloques con embargo de 4 trimestres)", "España (nacional)"
    for r in o.itertuples():
        m = r.mercado
        add(f"V8-OOS-{m[0]}-{r.modelo}-rmse", f"RMSE fuera de muestra de {r.modelo} para el crecimiento trimestral real de {MERC[m]} (pp; misma muestra para todos los modelos)",
            r.rmse_pp, None, None, "pp", "2016T2-2026T1", cob, fue, "C4", F["F5"])
        if _fin(r.p_holm_vs_ar4):
            add(f"V8-OOS-{m[0]}-{r.modelo}-pholm", f"p ajustado por Holm del contraste Diebold-Mariano de {r.modelo} frente al AR(4) ({MERC[m]})", r.p_holm_vs_ar4, None, None,
                "p-valor", "2016T2-2026T1", cob, fue, "C4", F["F5"])


def m0_m4(F: dict) -> None:
    j = json.loads((OUT / "M0" / "resultado.json").read_text(encoding="utf-8"))
    e = j["estimacion"]
    cob, fue = "España (nacional)", "M0 coeficientes por periodo (OLS con EE HAC; confirmaciones Bai-Perron, Markov y umbral)"
    add("V8-M0-coef", "Coeficientes por periodo y variable estimados en M0", e["n_coeficientes"], None, None, "coeficientes", "P1-P5", cob, fue, "C4", F["M0"])
    add("V8-M0-cumplen", "Efectos por periodo que cumplen la regla de §8 de M0 (ninguno sobrevive a BH; exploratorio)", e["n_efectos_cumplen_regla"], None, None, "efectos",
        "P1-P5", cob, fue, "C4", F["M0"])
    add("V8-M0-bh", "Coeficientes de M0 significativos tras BH (q = 0,10)", j["p_ajustado"]["n_coef_sig_bh"], None, None, "coeficientes", "P1-P5", cob, fue, "C4", F["M0"])
    k0 = pd.read_csv(OUT / "M0" / "coeficientes.csv", low_memory=False)
    ne = k0[k0.cumple_regla_m0 == "no_evaluable"]
    add("V8-M0-no-evaluable", "Coeficientes de M0 cuya regla de periodo es «no evaluable» (falta la medida alternativa de precio o de periodo; no es un incumplimiento)", len(ne), None, None,
        "coeficientes", "P1-P5", cob, fue, "C4", F["M0"])
    add("V8-M0-no-evaluable-alquiler", "De ellos, los del alquiler (no hay medida alternativa trimestral nacional del alquiler: la regla es «no evaluable», no «incumplida»)",
        int((ne.mercado == "alquiler").sum()), None, None, "coeficientes", "P1-P5", cob, fue, "C4", F["M0"])
    add("V8-M0-evaluables", "Coeficientes de M0 con la regla de periodo evaluable (cumple o no cumple)", len(k0) - len(ne), None, None, "coeficientes", "P1-P5", cob, fue, "C4", F["M0"])
    c = pd.read_csv(OUT / "M4" / "cointegracion.csv")
    fue4 = "M4 largo plazo (DOLS, FMOLS, ARDL con cotas de Pesaran-Shin-Smith, Gregory-Hansen)"
    add("V8-M4-ardl-rechaza", "Especificaciones de largo plazo (compra y alquiler) en que el ARDL con cotas rechaza la no cointegración (sin rupturas)", int(c.ARDL_rechaza_sin.sum()), None, None,
        "especificaciones", "1998T1-último dato", cob, fue4, "C4", F["M4"])
    add("V8-M4-ardl-total", "Especificaciones de largo plazo probadas con el ARDL con cotas (compra y alquiler)", len(c), None, None, "especificaciones", "1998T1-último dato", cob, fue4,
        "C4", F["M4"])
    v = pd.read_csv(OUT / "M4" / "voto_contabilidad.csv")
    add("V8-M4-voto-demografia", "Celdas (mercado, periodo) en que la contabilidad hogares-viviendas vota a favor de la demografía", int((v.vota_demografia == "si").sum()), None, None,
        "celdas", "P1-P5", cob, "M4 contabilidad hogares-viviendas (asociación; no resta viviendas liberadas)", "C4", F["M4"])


def m8(F: dict) -> None:
    q = pd.read_csv(OUT / "M8" / "cuota_cv.csv")
    for r in q.itertuples():
        a = AMB[r.ambito]
        k = r.ambito.replace("cv_prov:", "p").replace("valencia_ciudad", "vlc")
        fue = "M8 regional (provincias de la Comunitat Valenciana y València ciudad; cruce por código INE)"
        add(f"V8-M8-cv-{k}-{r.periodo}-total", f"Variación observada del precio real de compra en {a} en {r.periodo} (pp, log×100; media interanual × T/4: aproximación, "
            "no es el acumulado observado)", r.total_pp, None, None, "pp", per_txt(r.periodo), a, fue, "C4", F["M8"])
        add(f"V8-M8-cv-{k}-{r.periodo}-cuota", f"R² del crecimiento interanual de {a} en {r.periodo} sobre el factor común nacional (cuota de varianza; no es parte de la "
            "variación acumulada; resumen de comovimiento, sin lectura causal)", 100 * r.cuota_factor_nacional, None, None, "%", per_txt(r.periodo), a, fue, "C4", F["M8"])
    at = pd.read_csv(OUT / "M8" / "atribucion.csv")
    at = at[(at.mercado == "compra") & (at.periodo == "P5") & (at.factor == "factor_comun") & (at.principal == "si") & at.ambito.isin(AMB)]
    ds = pd.read_csv(OUT / "M8" / "descriptivo_cv.csv")
    ds = ds[ds.periodo == "P5"].set_index("ambito")
    fue = "M8 regional (provincias de la Comunitat Valenciana y València ciudad; cruce por código INE)"
    for r in at.itertuples():
        a = AMB[r.ambito]
        k = r.ambito.replace("cv_prov:", "p").replace("valencia_ciudad", "vlc")
        add(f"V8-M8-cv-{k}-P5-fcpp", f"Parte de la variación del precio real de compra de {a} en P5 asociada al factor común nacional (pp; regresión sobre el factor; banda del 68 %; "
            "asociación, no causal)", r.contribucion_pp, r.b68_lo, r.b68_hi, "pp", per_txt("P5"), a, fue, "C4", F["M8"])
        d = ds.loc[r.ambito]
        add(f"V8-M8-cv-{k}-P5-acum-mivau", f"Variación acumulada observada del valor tasado real de compra en {a} en P5 ({d.fuente1}; pp log)", d.valor1, None, None, "pp",
            per_txt("P5"), a, "M8 descriptivo; " + str(d.fuente1), str(d.capa), F["M8"])
        if _fin(d.valor2):
            add(f"V8-M8-cv-{k}-P5-acum-alt", f"Variación acumulada observada del precio real de compra en {a} en P5 con la segunda fuente ({d.fuente2}; pp log)", d.valor2, None, None,
                "pp", per_txt("P5"), a, "M8 descriptivo; " + str(d.fuente2), str(d.capa), F["M8"])
    j = json.loads((OUT / "M8" / "resultado.json").read_text(encoding="utf-8"))
    for m, d in j["estimacion"]["cuota_comun_mediana_ccaa"].items():
        for p, v in d.items():
            if _fin(v):
                add(f"V8-M8-comun-{m[0]}-{p}", f"Cuota del componente común en la varianza de {MERC[m]} (mediana entre las 17 CCAA) en {p}", 100 * v, None, None, "%", per_txt(p, m), "17 CCAA",
                    "M8 regional (panel de CCAA; cruce por código INE)", "C4", F["M8"])


def m9(F: dict) -> None:
    o = pd.read_csv(OUT / "M9" / "oos.csv")
    fue = "M9 aprendizaje automático interpretable (LightGBM, GAM); contraste, no causal"
    for (m, amb), g in o.groupby(["mercado", "ambito"], sort=True):
        base = g[g.modelo == g.base_mas_exigente.iloc[0]].iloc[0]
        ml = g[g.modelo.str.startswith(("lgbm", "gam"))].sort_values("rmse").iloc[0]
        k = f"{m[0]}-{amb.replace('ccaa_panel', 'panel')}"
        cob = "España (nacional)" if amb == "nacional" else "17 CCAA (panel)"
        add(f"V8-M9-oos-{k}-base", f"RMSE fuera de muestra de la base más exigente ({base.modelo}) para {MERC[m]} (crecimiento trimestral real, pp)", base.rmse, None, None, "pp",
            "bloque de prueba de M9", cob, fue, "C4", F["M9"])
        add(f"V8-M9-oos-{k}-ml", f"RMSE fuera de muestra del mejor modelo de aprendizaje automático en esa tabla ({ml.modelo}) para {MERC[m]} (pp; no se elige por p)", ml.rmse, None, None, "pp",
            "bloque de prueba de M9", cob, fue, "C4", F["M9"])
        add(f"V8-M9-oos-{k}-mejor", f"Modelos de M9 que superan a la base más exigente tras BH en {MERC[m]}", int(g.predice_mejor_bh.astype(str).str.lower().eq("true").sum()), None, None,
            "modelos", "bloque de prueba de M9", cob, fue, "C4", F["M9"])
    a = pd.read_csv(OUT / "M9" / "atribucion.csv")
    a = a[a.metodo.isin(["shap", "shap_sens_turismo"]) & (a.ambito == "ccaa_panel") & a.factor.isin(["demanda_externa", "turismo", "factor_europeo"]) & a.periodo.isin(PERS)]
    for r in a.itertuples():
        tur = r.factor == "turismo" or r.metodo == "shap_sens_turismo"
        ind = (f"Contribución SHAP media de {FACTOR[r.factor]} a la variación de {MERC[r.mercado]} en {r.periodo} en el panel de CCAA "
               "(banda del 68 % por bootstrap de bloques; contraste del modelo de aprendizaje automático, no es un efecto)")
        cob = "17 CCAA (panel)"
        if tur:
            ind = ("Sensibilidad no principal (NaN nativos), media de las 6 CCAA con datos de turismo; no comparable con la variación nacional: " + ind)
            cob = "Sensibilidad no principal (NaN nativos), media de las 6 CCAA con datos de turismo; no comparable con la variación nacional"
        add(f"V8-M9-shap-{r.mercado[0]}-{r.periodo}-{r.factor}", ind, r.contribucion_pp, r.b68_lo, r.b68_hi, "pp",
            per_txt(r.periodo, r.mercado), cob, fue, "C4", F["M9"], sentido=SENTIDO_SHAP)
    j = json.loads((OUT / "M9" / "resultado.json").read_text(encoding="utf-8"))
    tu = j["diagnosticos"]["turismo_cobertura"]["compra"]
    add("V8-M9-turismo-ccaa", "CCAA con datos de turismo (viviendas de uso turístico y turistas) utilizables en M9", tu["ccaa_con_turismo"], None, None, "CCAA",
        "P4-P5", "17 CCAA (panel)", fue, "C4", F["M9"])
    for k, d in j["estimacion"]["dml_theta_completo"].items():
        m, v = k.split("/")
        if v == "tipo_hip_real":
            add(f"V8-M9-dml-{m[0]}-tipo", f"Coeficiente DML (sin identificación; asociación) del tipo hipotecario real sobre el crecimiento de {MERC[m]} (p ajustado BH {d['p_BH']:.3f})", d["beta"],
                None, None, "coeficiente", "panel de CCAA", "17 CCAA (panel)", fue, "C4", F["M9"])


def main() -> None:
    F = _fechas()
    f5_reglas(F)
    svar(F)
    hipotesis(F)
    m1(F)
    m7(F)
    m7_variables(F)
    m6_colinealidad(F)
    oos(F)
    m0_m4(F)
    m8(F)
    m9(F)
    SAL.mkdir(parents=True, exist_ok=True)
    (SAL / "hechos.json").write_text(json.dumps(HECHOS, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(f"f6_hechos: {len(HECHOS)} hechos V8 en output/v8/F6/hechos.json")


if __name__ == "__main__":
    main()
