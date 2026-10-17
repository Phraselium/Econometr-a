"""V15-A · E4 (P5-CV): exposición turística con periodo previo. Cataluña (IDESCAT frente a Incasòl) y Comunitat Valenciana (registro GVA reconstruido frente a SERPAVI).

Estudio de eventos de dosis continua (DV15-A, A6): dosis estandarizada = log(1 + HUT) en 2017 (o fechado alternativo), año de referencia 2017,
coeficientes dosis × año; efectos fijos de municipio y de año. Honest DiD NO APTO y sin inferencia APTA para el diseño: SOLO coeficientes puntuales.
Ejecución: python3 src/v15/p5cv_exposicion.py   (SEED 20261010). Solo entrenamiento; la exposición GVA reconstruida nunca es principal.
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
from pa_comun import FECHA, OUT, PROC, registrar, volcar  # noqa: E402
import pa_panel as PN  # noqa: E402
from econ_utils import Registry  # noqa: E402

SALIDA = OUT / "p5cv"
REF = 2017
GRANDES = {"08019", "46250"}
VENT = {"2015-2024": list(range(2015, 2025)), "2015-2019": list(range(2015, 2020))}


def incasol_anual(d) -> pd.DataFrame:
    t = d[(d.frecuencia == "A") & d.variable.isin(["incasol_contratos", "incasol_renta_media"])]
    w = t.pivot_table(index=["territorio_codigo", "periodo", "desagregacion"], columns="variable", values="valor", aggfunc="first").reset_index()
    w["imp"] = w.incasol_contratos * w.incasol_renta_media
    w["cr"] = np.where(w.incasol_renta_media.notna(), w.incasol_contratos, 0.0)
    g = w.groupby(["territorio_codigo", "periodo"]).agg(imp=("imp", "sum"), cr=("cr", "sum")).reset_index()
    g["y"] = np.log(g.imp / g.cr.where(g.cr > 0))
    g["anio"] = g.periodo.astype(int)
    return g.rename(columns={"territorio_codigo": "mun"})[["mun", "anio", "y"]]


def serpavi(d, tip, prov) -> pd.DataFrame:
    s = d[(d.variable == "serpavi_alquiler_m2_mediana") & (d.nivel == "municipio") & (d.desagregacion == f"tipologia={tip}") & d.territorio_codigo.str[:2].isin(prov)]
    return pd.DataFrame({"mun": s.territorio_codigo.values, "anio": s.periodo.astype(int).values, "y": np.log(s.valor.values)})


def evento(Y: pd.DataFrame, dosis: pd.Series, anios: list, sin_top1=False, sin_grandes=False):
    """Estudio de eventos de dosis continua. Panel equilibrado en `anios`. Devuelve coeficientes dosis × año (%)."""
    P = Y[Y.anio.isin(anios)].dropna(subset=["y"])
    n = P.groupby("mun").anio.transform("nunique")
    P = P[n == len(anios)]
    P = P[P.mun.isin(dosis.index)]
    if sin_grandes:
        P = P[~P.mun.isin(GRANDES)]
    ds = dosis.reindex(P.mun.unique())
    if sin_top1:
        ds = ds[ds <= ds.quantile(0.99)]
        P = P[P.mun.isin(ds.index)]
    sd = float(ds.std(ddof=0))
    if len(ds) < 20 or sd == 0:
        return None
    z = (ds - ds.mean()) / sd
    P = P.assign(z=P.mun.map(z))
    cols = [a for a in anios if a != REF]
    X = np.column_stack([P.z.values * (P.anio.values == a) for a in cols])
    mun = pd.factorize(P.mun)[0]
    yr = pd.factorize(P.anio)[0]
    r = PN.ols_fe(P.y.values, X, mun, yr, mun)
    coef = {a: float(100 * b) for a, b in zip(cols, r["b"])}
    pre = [coef[a] for a in cols if a < REF]
    post = [coef[a] for a in cols if a > REF]
    return {"coef_pct_por_DT": coef, "n_municipios": int(mun.max() + 1), "n_obs": int(len(P)), "dt_dosis": sd,
            "max_abs_pre": float(np.max(np.abs(pre))), "media_post": float(np.mean(post)), "ultimo_post": float(post[-1]),
            "compatible_puntualmente": bool(np.max(np.abs(pre)) <= 0.5 * abs(np.mean(post)))}


def main():
    SALIDA.mkdir(parents=True, exist_ok=True)
    reg = Registry(SALIDA / "registro.csv")
    d = pd.read_parquet(PROC / "p5_cv_cataluna.parquet")
    res = {"cataluna": [], "valenciana": []}
    # ---- Cataluña ----
    inc = incasol_anual(d)
    for medida, var in (("hut_n", "idescat_hut_n"), ("hut_plazas", "idescat_hut_plazas")):
        h = d[(d.variable == var) & (d.periodo == str(REF))].set_index("territorio_codigo").valor
        dosis = np.log1p(h)
        for vn, anios in VENT.items():
            r = evento(inc, dosis, anios)
            r2 = evento(inc, dosis, anios, sin_top1=True)
            r3 = evento(inc, dosis, anios, sin_grandes=True)
            if r is None:
                continue
            fila = {"region": "Cataluña", "medida": medida, "fechado": "n/a", "ventana": vn, **r, "sin_1pct_superior": r2, "sin_grandes_ciudades": r3}
            res["cataluna"].append(fila)
            registrar(reg, "V15-A", f"E4-CAT-{medida}-{vn}", f"log renta Incasòl anual ~ dosis({medida} {REF}) x año + FE municipio + FE año", vn[:4], vn[5:], r["n_obs"], coef=r["media_post"] / 100, notas=f"media post (% por DT); max|pre|={r['max_abs_pre']:.3f}; puntual, sin inferencia")
    # ---- Comunitat Valenciana (exposición reconstruida: nunca principal) ----
    g = d[d.variable == "vut_registro_gva_reconstruido"]
    prov = ["03", "12", "46"]
    esc = {"base_dic2017": "2017-12", "alta_12m_antes_dic2018": "2018-12", "alta_12m_despues_dic2016": "2016-12"}
    for tip in ("VC", "VU"):
        S = serpavi(d, tip, prov)
        for en, per in esc.items():
            h = g[g.periodo == per].set_index("territorio_codigo").valor
            munis = S.mun.unique()
            dosis = np.log1p(h.reindex(munis).fillna(0.0))  # municipio sin VUT inscrita hoy = 0 (supuesto, DV15-A A6)
            for vn, anios in VENT.items():
                r = evento(S, dosis, anios)
                r2 = evento(S, dosis, anios, sin_top1=True)
                r3 = evento(S, dosis, anios, sin_grandes=True)
                if r is None:
                    continue
                res["valenciana"].append({"region": "Comunitat Valenciana", "medida": f"SERPAVI {tip}", "fechado": en, "ventana": vn, **r, "sin_1pct_superior": r2, "sin_grandes_ciudades": r3})
                registrar(reg, "V15-A", f"E4-CV-{tip}-{en}-{vn}", f"log SERPAVI {tip} ~ dosis(GVA reconstruida {per}) x año + FE municipio + FE año", vn[:4], vn[5:], r["n_obs"], coef=r["media_post"] / 100, notas=f"media post (% por DT); max|pre|={r['max_abs_pre']:.3f}; exposición reconstruida: solo C4 y robustez")
    todas = res["cataluna"] + res["valenciana"]
    res["n_especificaciones"] = len(todas)
    res["resumen"] = {"compatibles_puntualmente": int(sum(x["compatible_puntualmente"] for x in todas)), "no_compatibles": int(sum(not x["compatible_puntualmente"] for x in todas)),
                      "media_post_rango": [float(min(x["media_post"] for x in todas)), float(max(x["media_post"] for x in todas))],
                      "signo_positivo_media_post": int(sum(x["media_post"] > 0 for x in todas))}
    volcar(SALIDA / "estimacion_bruta.json", res)
    reg.flush()
    escribir(res)
    return res


def escribir(res):
    f = lambda x, d=2: "n.d." if x is None else f"{x:.{d}f}".replace(".", ",")
    todas = res["cataluna"] + res["valenciana"]
    princ = next(x for x in res["cataluna"] if x["medida"] == "hut_n" and x["ventana"] == "2015-2024")
    cv_b = next(x for x in res["valenciana"] if x["medida"] == "SERPAVI VC" and x["fechado"] == "base_dic2017" and x["ventana"] == "2015-2024")
    sm = res["resumen"]
    lineas = ["# V15-A · E4: exposición turística con periodo previo (Cataluña y Comunitat Valenciana)", "",
              "Capa C4 (exploratoria, entrenamiento; asociación, sin lenguaje causal). Estudio de eventos de dosis continua con coeficientes **puntuales**: no hay inferencia APTA para el diseño y Honest DiD es NO APTO (docs/v15/validacion_montecarlo.md). `pendiente_sellada`: no aplica a E4 (exploratoria, sin evaluación sellada pre-registrada), se deja `true` por la regla común. BY lo aplica el orquestador (p = null).", "",
              "## Diseño (DV15-A, A6)",
              f"- Dosis: log(1 + viviendas de uso turístico) en {REF}, estandarizada (IDESCAT n y plazas en Cataluña; registro GVA reconstruido en la Comunitat Valenciana, fechados base/−12/+12 meses). Resultado: log de la renta anual de Incasòl (media ponderada por contratos) en Cataluña; log de la mediana SERPAVI (stock de contratos) VC o VU en la Comunitat Valenciana. Efectos fijos de municipio y de año; referencia {REF}; paneles equilibrados en la ventana. Ventanas 2015-2024 y 2015-2019.",
              "- La exposición del registro GVA es reconstruida a partir de las altas y bajas fechadas del registro actual: no recoge las viviendas ya dadas de baja, y los municipios sin vivienda inscrita hoy se tratan como dosis 0. Se reporta como C4 y nunca como principal.",
              f"- {res['n_especificaciones']} especificaciones registradas (≤ 24 declaradas). Pretendencias: coeficientes de 2015 y 2016; lectura puntual declarada «compatible» si max|coef previo| ≤ 0,5 × |media de los coeficientes posteriores| (no es un test).", "",
              "## Resultados",
              f"- **Cataluña, IDESCAT n, 2015-2024** ({princ['n_municipios']} municipios): coeficientes previos {f(princ['coef_pct_por_DT'][2015])} % (2015) y {f(princ['coef_pct_por_DT'][2016])} % (2016) por DT de dosis; media posterior (2018-2024) {f(princ['media_post'])} %; 2024: {f(princ['ultimo_post'])} %. Lectura puntual: {'compatible' if princ['compatible_puntualmente'] else 'NO compatible'}.",
              f"- **Comunitat Valenciana, SERPAVI VC, fechado base, 2015-2024** ({cv_b['n_municipios']} municipios): previos {f(cv_b['coef_pct_por_DT'][2015])} % y {f(cv_b['coef_pct_por_DT'][2016])} %; media posterior {f(cv_b['media_post'])} %. Lectura: {'compatible' if cv_b['compatible_puntualmente'] else 'NO compatible'}.",
              f"- **Conjunto de {res['n_especificaciones']}:** media posterior entre {f(sm['media_post_rango'][0])} % y {f(sm['media_post_rango'][1])} % por DT; positiva en {sm['signo_positivo_media_post']}; compatibles puntualmente con la regla declarada: {sm['compatibles_puntualmente']}; no compatibles: {sm['no_compatibles']}.", "",
              "| región | medida | fechado | ventana | N mun. | previos 2015 / 2016 (%) | media post (%) | compatible | sin 1 % sup. (media post) | sin grandes ciudades (media post) |", "|---|---|---|---|---|---|---|---|---|---|"]
    for x in todas:
        lineas.append(f"| {x['region']} | {x['medida']} | {x['fechado']} | {x['ventana']} | {x['n_municipios']} | {f(x['coef_pct_por_DT'][2015])} / {f(x['coef_pct_por_DT'][2016])} | {f(x['media_post'])} | {'sí' if x['compatible_puntualmente'] else 'no'} | {f(x['sin_1pct_superior']['media_post']) if x['sin_1pct_superior'] else 'n.d.'} | {f(x['sin_grandes_ciudades']['media_post']) if x['sin_grandes_ciudades'] else 'n.d.'} |")
    lineas += ["", "## Lectura frente a lo ya publicado",
               "- V9 estimó una dosis-respuesta en Cataluña con pretendencias rechazadas (V9-D2, C4). Aquí se repite con IDESCAT y otra referencia temporal; ninguna cifra es confirmatoria y ninguna contradice con dirección una conclusión de la 1.0 («turísticos: no concluyente»).",
               "- Pruebas no evaluadas por herramienta NO APTA: inferencia del estudio de eventos, Honest DiD, potencia de Roth. Oster, Cinelli-Hazlett y E-values no se calculan sin error típico válido. Raíces unitarias y cointegración no aplican (T ≤ 10 por municipio, estudio de eventos).", "",
               "## Fichas reproducibles",
               "Todas: `python3 src/v15/p5cv_exposicion.py` (SEED 20261010; no hay aleatoriedad); cifras en output/v15/p5cv/estimacion_bruta.json y registro.csv.",
               "- <a id=\"ficha-e4-cat\"></a>**ficha-e4-cat:** `cataluna[medida=hut_n, ventana=2015-2024].media_post` = media de los coeficientes dosis × año de 2018 a 2024 (×100) del modelo log(renta Incasòl) ~ z·1[año] + FE de municipio y de año.",
               "- <a id=\"ficha-e4-pre\"></a>**ficha-e4-pre:** `cataluna[...].coef_pct_por_DT[2015, 2016]`.",
               "- <a id=\"ficha-e4-cv\"></a>**ficha-e4-cv:** `valenciana[medida=SERPAVI VC, fechado=base_dic2017, ventana=2015-2024].media_post`.",
               "- <a id=\"ficha-e4-resumen\"></a>**ficha-e4-resumen:** `resumen`."]
    (SALIDA / "informe.md").write_text("\n".join(lineas) + "\n", encoding="utf-8")
    diag = {"inferencia": "NO APTA para el estudio de eventos de dosis; Honest DiD NO APTO: solo coeficientes puntuales",
            "pretendencias": {"regla_puntual": "max|coef 2015,2016| <= 0,5 x |media post|", "compatibles": sm["compatibles_puntualmente"], "no_compatibles": sm["no_compatibles"]},
            "exclusion_1pct_superior_y_grandes_ciudades": "en la tabla del informe (media posterior sin el 1 % superior de dosis y sin Barcelona y València)",
            "honest_did": "no evaluado (NO APTO)", "potencia_roth": "no calculable sin error típico válido", "oster_cinelli_evalue": "no calculados (sin error típico válido)",
            "exposicion_GVA": "reconstruida (supuesto de fechado); solo robustez, nunca principal", "raices_unitarias_cointegracion": "no aplica (T <= 10, estudio de eventos)",
            "pruebas_superadas_puntualmente": [f"{x['region']}|{x['medida']}|{x['fechado']}|{x['ventana']}" for x in todas if x["compatible_puntualmente"]],
            "pruebas_fallidas_puntualmente": [f"{x['region']}|{x['medida']}|{x['fechado']}|{x['ventana']}" for x in todas if not x["compatible_puntualmente"]]}
    out = {"rama": "v15/p5cv", "pregunta": "E4: asociación entre la exposición turística con periodo previo (IDESCAT; registro GVA reconstruido) y el alquiler, en estudio de eventos de dosis continua",
           "capa": "C4", "datos": "data/processed/v15/p5_cv_cataluna.parquet (IDESCAT 2015-2024, Incasòl anual, registro GVA reconstruido, SERPAVI municipal; entrenamiento)",
           "N": {"municipios_cataluna": princ["n_municipios"], "municipios_valenciana": cv_b["n_municipios"], "especificaciones": res["n_especificaciones"]},
           "metodo": "estudio de eventos de dosis continua, efectos fijos de municipio y año, referencia 2017; coeficientes puntuales",
           "estimacion": {"cataluna_hut_n_2015_2024": {"previos_2015_2016_pct_por_DT": [princ["coef_pct_por_DT"][2015], princ["coef_pct_por_DT"][2016]], "media_post_pct_por_DT": princ["media_post"]},
                          "valenciana_VC_base_2015_2024": {"previos_2015_2016_pct_por_DT": [cv_b["coef_pct_por_DT"][2015], cv_b["coef_pct_por_DT"][2016]], "media_post_pct_por_DT": cv_b["media_post"]}, "resumen": sm},
           "ic95": None, "p_ajustado": None, "nivel_evidencia": "EXPLORATORIO", "diagnosticos": diag, "fuera_muestra": {"modelo": None, "rmse": None, "dm_vs_ar4": None},
           "pendiente_sellada": True, "p_valores_para_BY": [{"hipotesis": "E4", "p": None, "motivo": "inferencia NO APTA para el estudio de eventos de dosis; Honest DiD NO APTO"}],
           "notas": "Asociación C4 exploratoria, sin lenguaje causal. Exposición GVA reconstruida: solo robustez. Desviaciones: DV15-A, A6.", "multiverso_registro": "output/v15/p5cv/registro.csv"}
    volcar(SALIDA / "resultado.json", out)
    base = dict(unidad="% por DT de dosis", cobertura="municipios con panel equilibrado 2015-2024", fuentes=["IDESCAT turall", "Incasòl"], capa="C4", fecha_dato=FECHA)
    mm = [x["media_post"] for x in res["cataluna"] if x["ventana"] == "2015-2024"]
    mc = [x["media_post"] for x in res["valenciana"] if x["ventana"] == "2015-2024"]
    hechos = [
        dict(id="V15-E4-cat-post", indicador="E4: media de los coeficientes dosis × año 2018-2024, renta Incasòl y HUT IDESCAT (min/max = IDESCAT n y plazas; puntual)", valor=round(princ["media_post"], 3), min=round(min(mm), 3), max=round(max(mm), 3), periodo="2018-2024", ficha="output/v15/p5cv/informe.md#ficha-e4-cat", **base),
        dict(id="V15-E4-cat-pre", indicador="E4: mayor |coeficiente previo| (2015, 2016) en Cataluña, IDESCAT n", valor=round(princ["max_abs_pre"], 3), min=None, max=None, periodo="2015-2016", ficha="output/v15/p5cv/informe.md#ficha-e4-pre", **base),
        dict(id="V15-E4-cv-post", indicador="E4: media de los coeficientes dosis × año 2018-2024, SERPAVI VC y registro GVA reconstruido, fechado base (C4; min/max = VC y VU en los 3 fechados)", valor=round(cv_b["media_post"], 3), min=round(min(mc), 3), max=round(max(mc), 3), periodo="2018-2024", ficha="output/v15/p5cv/informe.md#ficha-e4-cv", **{**base, "fuentes": ["GVA registro de turismo (reconstruido)", "MIVAU SERPAVI"], "cobertura": "municipios de Alicante, Castellón y València con panel equilibrado"}),
        dict(id="V15-E4-compat", indicador="E4: especificaciones compatibles con la regla puntual de pretendencias, sobre el total", valor=sm["compatibles_puntualmente"], min=0, max=res["n_especificaciones"], unidad="especificaciones", periodo="2015-2024", ficha="output/v15/p5cv/informe.md#ficha-e4-resumen", **{k: v for k, v in base.items() if k != "unidad"}),
    ]
    volcar(SALIDA / "hechos.json", hechos)


if __name__ == "__main__":
    main()
