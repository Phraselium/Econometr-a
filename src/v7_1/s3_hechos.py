"""V7.1-S3 · Cifras difundibles de V7 que faltaban en cifras_clave, más un DESCRIPTIVO del peso del componente común.

Sin modelos nuevos. Lee output/v7 versionado y data/processed/v7/panel_ccaa_q_v7.csv. Escribe output/v7_1/S3/hechos.json.
- Peso del componente común (W7): R² de la regresión de la variación interanual de cada CCAA sobre la media transversal de
  las 17 CCAA (2008T1-2026T2). Es contabilidad de varianza, no un modelo ni un contraste; C4 por fuente única (INE).
- Recuentos de V7: hipótesis confirmadas, CCAA con I(2) no descartado, CCAA donde el mejor modelo bate a la base más
  exigente, sesgo y cobertura del Monte Carlo (escenario F) y valor crítico simulado de φ̄.
"""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd

RAIZ = Path(__file__).resolve().parents[2]
V7 = RAIZ / "output" / "v7"
OUT = RAIZ / "output" / "v7_1" / "S3"
FECHA = "2026-10-12"
Y = {"alquiler": "ipc_alquiler", "compra": "ipv"}


def h(i, ind, val, mn, mx, uni, per, fue, capa="C4", sentido="rango", cob="17 CCAA"):
    return dict(id=i, indicador=ind, valor=val, min=mn, max=mx, unidad=uni, periodo=per, cobertura=cob, fuentes=fue, capa=capa,
                fecha_dato=FECHA, sentido_min_max=sentido)


def componente_comun() -> list[dict]:
    d = pd.read_csv(RAIZ / "data/processed/v7/panel_ccaa_q_v7.csv")
    out = []
    for m, col in Y.items():
        w = d.pivot(index="trimestre", columns="codigo_ine_ccaa", values=col)
        g = np.log(w).diff(4).dropna(how="any")
        g = g[g.index >= "2008Q1"]
        media = g.mean(axis=1)
        r2 = []
        for c in g.columns:
            x = np.c_[np.ones(len(g)), media.values]
            b, *_ = np.linalg.lstsq(x, g[c].values, rcond=None)
            e = g[c].values - x @ b
            r2.append(1 - e.var() / g[c].values.var())
        r2 = pd.Series(r2, index=g.columns)
        cor = g.corr().values[np.triu_indices(g.shape[1], 1)]
        per = f"{g.index.min()}-{g.index.max()}"
        out.append(h(f"V71-S3-comun-r2-{m}", f"Parte de la varianza de la variación interanual de {'IPC del alquiler' if m == 'alquiler' else 'IPV'} de cada CCAA "
                     "que acompaña a la media de las 17 CCAA (R², mediana entre CCAA; mín. y máx. entre CCAA; descriptivo, no causal)",
                     float(r2.median() * 100), float(r2.min() * 100), float(r2.max() * 100), "%", per, "INE (panel_ccaa_q_v7)",
                     sentido="mínimo y máximo entre las 17 CCAA"))
        out.append(h(f"V71-S3-comun-corr-{m}", f"Correlación media entre pares de CCAA de la variación interanual ({m}; mín. y máx. entre pares)",
                     float(cor.mean()), float(cor.min()), float(cor.max()), "proporción", per, "INE (panel_ccaa_q_v7)",
                     sentido="mínimo y máximo entre los 136 pares de CCAA"))
    return out


def recuentos() -> list[dict]:
    out = []
    n_conf = 0
    for m in ("alquiler", "compra"):
        hp = pd.read_csv(V7 / "R4" / m / "hipotesis.csv")
        col = next(c for c in hp.columns if "veredicto" in c)
        n_conf += int(hp[col].astype(str).str.startswith("CONFIRMADA").sum())
    out.append(h("V71-S3-largo-confirmadas", "Hipótesis de largo plazo regional confirmadas (de 7 pre-registradas; Holm y triangulación MG_dm, PMG_dm y CS-DL)",
                 n_conf, None, None, "hipótesis", "2007T1-2026T2", "R4 v7 (panel_ccaa_q_v7)", sentido="sin min/max"))
    for m, y in (("alquiler", "ln_ipc_alquiler"), ("compra", "ln_ipv")):
        it = pd.read_csv(V7 / "R4" / m / "integracion.csv")
        n2 = int(it[it.variable == y].i2_no_descartado.sum())
        out.append(h(f"V71-S3-i2-{m}", f"CCAA en las que no se descarta I(2) en {y} (ADF en diferencias con constante y tendencia)", n2, None, None,
                     "CCAA de 17", "2007T1-2026T2", "R4 v7", sentido="sin min/max"))
    b = pd.read_csv(V7 / "R5" / "mejor_por_region.csv")
    for m, g in b.groupby("mercado"):
        out.append(h(f"V71-S3-R5-exigente-{m}", f"CCAA en las que el mejor modelo regional bate a la base más exigente ({m}; h=1-4; selección en muestra, informativo)",
                     int(g.bate_base_exigente.sum()), None, None, "CCAA de 17", "2016T1-2026T1 (orígenes)", "R5 v7", sentido="sin min/max"))
    mc = pd.read_csv(V7 / "R2" / "montecarlo_r3.csv")
    f = mc[(mc.scen == "F") & mc.metrica.isin(["theta1", "theta2"])]
    for est, nom in (("MG_dm", "MG con demeaning"), ("PMG_dm_boot", "PMG con demeaning y bootstrap"), ("CS-DL_pT4", "CS-DL (p_T=4)"),
                     ("MG", "MG sin ajuste"), ("PMG", "PMG sin ajuste"), ("CS-ARDL_pT4", "CS-ARDL (p_T=4)")):
        g = f[f.herramienta == est]
        out.append(h(f"V71-S3-MC-F-sesgo-{est}", f"Sesgo relativo máximo |θ| de {nom} con factor común I(1) de cargas heterogéneas (Monte Carlo R2, N=17, T=78)",
                     float(g.sesgo_rel.abs().max() * 100), None, None, "%", "simulación", "R2 v7 (montecarlo_r3.csv)", sentido="sin min/max",
                     cob="simulación"))
        out.append(h(f"V71-S3-MC-F-cobertura-{est}", f"Cobertura del IC95 de {nom} en el mismo escenario (mín. y máx. entre θ1 y θ2)",
                     float(g.cobertura.mean()), float(g.cobertura.min()), float(g.cobertura.max()), "proporción", "simulación", "R2 v7 (montecarlo_r3.csv)",
                     cob="simulación"))
    cv = mc[mc.scen.isin(["C", "D"]) & (mc.herramienta == "MG_t_phi")]
    out.append(h("V71-S3-MC-phi-critico", "Valor crítico al 5 % del t de MG de la velocidad de ajuste media bajo no cointegración (simulado; menor de C y D)",
                 round(float(cv.tasa.min() if cv.tasa.notna().any() else cv.sesgo_rel.min()), 2), None, None, "estadístico t", "simulación",
                 "R2 v7 (validacion_herramientas.md)", sentido="sin min/max", cob="simulación"))
    wl = mc[(mc.scen == "J") & mc.herramienta.str.startswith("WL_")]
    out.append(h("V71-S3-MC-WL-potencia-J", "Potencia del contraste tipo Westerlund con ajuste lento (φ entre −0,1 y −0,02; mín. y máx. de Ga, Gt, Pa y Pt)",
                 float(wl.tasa.median()), float(wl.tasa.min()), float(wl.tasa.max()), "proporción", "simulación", "R2 v7", cob="simulación"))
    r2 = pd.read_csv(V7 / "R2" / "montecarlo.csv")   # ronda 2: DFE (escenarios A, B y E; sin F)
    for sc, lab in (("A_coint_sin_factor", "A"), ("B_coint_con_factor", "B"), ("E_coint_theta_heterogeneo", "E")):
        g = r2[(r2.scen == sc) & (r2.herramienta == "DFE") & r2.metrica.isin(["theta1", "theta2"])]
        out.append(h(f"V71-S3-MC-DFE-{lab}-sesgo", f"Sesgo relativo máximo |θ| de DFE en el escenario {lab} (Monte Carlo R2, ronda 2, N=17, T=78)",
                     float(g.sesgo_rel.abs().max() * 100), None, None, "%", "simulación", "R2 v7 (montecarlo.csv)", sentido="sin min/max", cob="simulación"))
        out.append(h(f"V71-S3-MC-DFE-{lab}-cobertura", f"Cobertura del IC95 de DFE en el escenario {lab} (media; mín. y máx. entre θ1 y θ2)",
                     float(g.cobertura.mean()), float(g.cobertura.min()), float(g.cobertura.max()), "proporción", "simulación", "R2 v7 (montecarlo.csv)", cob="simulación"))
    return out


NOM = {"a_construccion": "construcción adicional", "b_vacias": "movilización de vacías", "c_vivienda_publica": "vivienda pública o asequible",
       "d_turisticos": "regulación local de turísticos", "e_ayuda_demanda": "ayudas a la demanda",
       "f1_rebaja_ITP_IVA_vivienda_nueva": "rebaja de ITP/IVA (vivienda nueva)", "f2_impuestos_construccion": "rebaja de impuestos y costes de construcción"}


def propuestas() -> list[dict]:
    im = pd.read_csv(V7 / "R6" / "impactos.csv", dtype={"cc": str})
    im = im[(im.fuente_es == "rejilla") & (im.horizonte == 10)]
    out = []
    for (inst, mer), g in im.groupby(["instrumento", "mercado"]):
        ml = "compra" if mer == "precio" else "alquiler"
        out.append(h(f"V71-S3-R6-{inst}-{ml}-precio10a", f"Variación del {'precio de compra' if mer == 'precio' else 'alquiler'} de mercado a 10 años si se aplicase "
                     f"«{NOM[inst]}» (escenario condicional; mediana entre CCAA; mín. y máx. de las medianas regionales)",
                     float(g.dprecio_med.median()), float(g.dprecio_med.min()), float(g.dprecio_med.max()), "%", "2026-2036 (escenario)",
                     "R6 v7 (rejilla A4 v5; T3 v5.1; R4 v7)", sentido="mínimo y máximo de las medianas de las 17 CCAA"))
        out.append(h(f"V71-S3-R6-{inst}-{ml}-robustas", f"CCAA en las que «{NOM[inst]}» es robusta en {ml} (esfuerzo baja en todas las extracciones y el precio de mercado no sube)",
                     int(g.robusto.sum()), None, None, "CCAA de 17", "2026-2036 (escenario)", "R6 v7", sentido="sin min/max"))
    return out


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    hs = componente_comun() + recuentos() + propuestas()
    (OUT / "hechos.json").write_text(json.dumps(hs, ensure_ascii=False, indent=1), encoding="utf-8")
    for x in hs:
        print(x["id"], x["valor"], x["min"], x["max"])


if __name__ == "__main__":
    main()
