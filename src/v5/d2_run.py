"""D2 · Política por territorio: cruza necesidad (B1), clase (A4) y matriz (D1). Cruce C4 (las clases son C4). Sin red."""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd

RAIZ = Path(__file__).resolve().parents[2]
OUT = RAIZ / "output" / "v5" / "D2"
SEED = 20261010
FECHA = "2026-10-10"
PD_LO, PD_HI = 25_000, 100_000   # construcción adicional de P-D v3 (viviendas/año, nacional)

COMBI = {
    1: dict(estable="P1 más construcción donde falta (signo estable C2); I10/I27/N7 movilización de vacías (signo estable C2)",
            verificada="N2 edificabilidad (Büchler-Lutz 2024, Greenaway-McGrevy-Phillips 2023; VERIFICADAS, otros países, magnitud de resumen secundario); N1/I13 licencias (Ball 2011, solo asociación)",
            plazo="vacías: corto-medio; construcción y N2: medio-largo", no_rec="Ayudas generales a la demanda (I06-I09, N9) sin más oferta: con εs de A4 en esta clase (central 0,55) se traslada al precio el 28-82 % (método A) o el 15-46 % (método B) de una ayuda general; I02/N8 solo si no desplaza a la construcción privada (signo ≤ 0, posiblemente nulo)"),
    2: dict(estable="P1 más construcción (signo estable C2) y I10/I27/N7 (signo estable C2); la clase se define por oferta sin respuesta, de modo que el cuello de botella es de suelo o regulatorio",
            verificada="N2 edificabilidad y N1/I13 licencias actúan sobre ese cuello de botella (mismas referencias que en clase 1; sin evaluación en España)",
            plazo="vacías: corto-medio; N2/N1: medio; construcción: medio-largo", no_rec="Ayudas generales a la demanda (I06-I09, N9): con εs ≈ 0 (A4) se traslada al precio el 88-100 % de una ayuda general (Eriksen-Ross 2015: subidas donde la oferta es rígida; Hilber-Turner 2014: efecto adverso en mercados restrictivos); I29 y N4 (la rebaja o el crédito se capitaliza en el suelo, literatura NO VERIFICADA)"),
    3: dict(estable="P1 con financiación pública y I02/N8 (signo ≤ 0, posiblemente nulo: C2 débil); I10/I27/N7 no aplican porque B1 no asigna movilización a clases sin presión",
            verificada="Sin literatura verificada con magnitud aplicable: I04/I20 y N4 NO VERIFICADAS (solo robustez)",
            plazo="largo (5-10 años) para parque público", no_rec="Ayudas generales a la demanda: con εs de A4 en esta clase (central 0,23) se traslada al precio el 50-90 % (método A) o el 40-77 % (método B); N2 No evaluable: construir no es rentable al coste oficial, no hay una restricción de edificabilidad identificada (C4)"),
    9: dict(estable="No evaluable: clase 9 (sin dato de clase en A4)", verificada="No evaluable: sin dato", plazo="No evaluable",
            no_rec="No evaluable: sin dato"),
}


def main() -> dict:
    np.random.seed(SEED)
    OUT.mkdir(parents=True, exist_ok=True)
    a = pd.read_csv(RAIZ / "output" / "v5" / "A4" / "clasificacion_provincias.csv", dtype={"cod_prov": int})
    b = pd.read_csv(RAIZ / "output" / "v5" / "B1" / "tablas" / "B1_tabla_provincial.csv")
    b2 = pd.read_csv(RAIZ / "output" / "v5" / "B2" / "tablas" / "B2_deficit_2030_provincial.csv")
    nac = pd.read_csv(RAIZ / "output" / "v5" / "B1" / "tablas" / "B1_nacional.csv").set_index("componente")
    ic = pd.read_csv(RAIZ / "output" / "v5" / "D1" / "incidencia_ayudas_por_clase.csv")
    d = b[["cod_prov", "provincia", "clase_A4", "N_anual_min", "N_anual_central", "N_anual_max", "M_min", "M_central", "M_max", "V_central"]].merge(
        a[["cod_prov", "robusta_diagnostico"]], on="cod_prov").merge(b2[["cod_prov", "D2025", "D2030_min", "D2030_central", "D2030_max"]], on="cod_prov")
    tot = d.N_anual_central.sum()
    d["cuota_necesidad"] = d.N_anual_central / tot
    # construcción adicional de P-D asignada por cuota de necesidad (supuesto de reparto proporcional, C4)
    d["pd_construccion_adicional_min"] = PD_LO * d.cuota_necesidad
    d["pd_construccion_adicional_max"] = PD_HI * d.cuota_necesidad
    d["cobertura_pd_min_pct"] = 100 * d.pd_construccion_adicional_min / d.N_anual_central.where(d.N_anual_central > 0)
    d["cobertura_pd_max_pct"] = 100 * d.pd_construccion_adicional_max / d.N_anual_central.where(d.N_anual_central > 0)
    # movilización de vacías por año: B1 da el stock movilizable a 10 años (10-30 % de vacías en provincias con presión)
    for s in ("min", "central", "max"):
        d[f"vacias_movilizables_anual_{s}"] = d[f"M_{s}"] / 10
    d["cobertura_vacias_central_pct"] = 100 * d.vacias_movilizables_anual_central / d.N_anual_central.where(d.N_anual_central > 0)
    d["clase"] = d.clase_A4
    for k in ("estable", "verificada", "plazo", "no_rec"):
        d[{"estable": "instrumentos_signo_estable_C2", "verificada": "instrumentos_evidencia_verificada_aplicable", "plazo": "plazo", "no_rec": "instrumentos_no_recomendados_por_evidencia"}[k]] = d.clase.map(lambda c, k=k: COMBI[c][k])
    d["capa"] = "C4"
    d["lectura"] = ("Con la evidencia disponible, en provincias de clase " + d.clase.astype(str) + " los instrumentos con signo estable son los indicados; "
                    "la cobertura es un orden de magnitud (reparto proporcional a la necesidad, C4), no una predicción.")
    cols = ["cod_prov", "provincia", "clase", "robusta_diagnostico", "N_anual_min", "N_anual_central", "N_anual_max", "D2025", "D2030_min", "D2030_central", "D2030_max",
            "pd_construccion_adicional_min", "pd_construccion_adicional_max", "cobertura_pd_min_pct", "cobertura_pd_max_pct", "vacias_movilizables_anual_min",
            "vacias_movilizables_anual_central", "vacias_movilizables_anual_max", "cobertura_vacias_central_pct", "plazo", "instrumentos_signo_estable_C2",
            "instrumentos_evidencia_verificada_aplicable", "instrumentos_no_recomendados_por_evidencia", "capa"]
    d[cols].round(2).to_csv(OUT / "politica_territorio.csv", index=False)
    # resumen por clase
    g = d.groupby("clase").agg(n=("cod_prov", "size"), robustas=("robusta_diagnostico", "sum"), N_min=("N_anual_min", "sum"), N_central=("N_anual_central", "sum"),
                              N_max=("N_anual_max", "sum"), vac_central=("vacias_movilizables_anual_central", "sum"), vac_min=("vacias_movilizables_anual_min", "sum"),
                              vac_max=("vacias_movilizables_anual_max", "sum"), D2030=("D2030_central", "sum")).reset_index()
    g["cuota_N_pct"] = 100 * g.N_central / g.N_central.sum()
    g["pd_min"] = PD_LO * g.cuota_N_pct / 100
    g["pd_max"] = PD_HI * g.cuota_N_pct / 100
    g["cob_pd_min_pct"] = 100 * g.pd_min / g.N_central
    g["cob_pd_max_pct"] = 100 * g.pd_max / g.N_central
    g["cob_vac_pct"] = 100 * g.vac_central / g.N_central
    g.round(2).to_csv(OUT / "resumen_por_clase.csv", index=False)
    # controles de suma
    nac_n = float(nac.loc["N10", "central"]) / 10
    ctrl = [dict(tabla="N_anual_central_provincias_vs_N10_nacional_div10", suma_provincial=float(tot), nacional=nac_n, tolerancia_rel=1e-3, ok=bool(abs(tot - nac_n) / nac_n < 1e-3)),
            dict(tabla="N_anual_central_suma_clases", suma_provincial=float(g.N_central.sum()), nacional=float(tot), tolerancia_rel=1e-9, ok=bool(abs(g.N_central.sum() - tot) < 1e-6)),
            dict(tabla="M_central_provincias_vs_B1_nacional", suma_provincial=float(d.M_central.sum()), nacional=float(nac.loc["M", "central"]), tolerancia_rel=1e-3,
                 ok=bool(abs(d.M_central.sum() - nac.loc["M", "central"]) / nac.loc["M", "central"] < 1e-3)),
            dict(tabla="pd_construccion_adicional_max_vs_nacional", suma_provincial=float(d.pd_construccion_adicional_max.sum()), nacional=float(PD_HI), tolerancia_rel=1e-9,
                 ok=bool(abs(d.pd_construccion_adicional_max.sum() - PD_HI) < 1e-3)),
            dict(tabla="provincias", suma_provincial=float(len(d)), nacional=52.0, tolerancia_rel=0.0, ok=bool(len(d) == 52))]
    (OUT / "control_sumas.json").write_text(json.dumps(ctrl, ensure_ascii=False, indent=1))
    assert all(c["ok"] for c in ctrl), ctrl

    def f0(x):
        return f"{x:,.0f}".replace(",", ".")
    nac_pd = (PD_LO, PD_HI)
    md = ["# Política por territorio (D2, v5)\n",
          f"Fecha: {FECHA}. Cruce de la necesidad anual de B1 (central y rango), la clase de A4 y la matriz de D1. **Capa C4**: las clases de A4 son C4, de modo que ningún resultado "
          "por clase se promueve. El lenguaje es condicional y sin causalidad: lo que se describe son instrumentos con signo estable en la rejilla de P-D v3 (C2, nacional) o con "
          "literatura verificada de otros países; no hay efecto estimado por clase en España. Se evalúan instrumentos, no actores.\n",
          f"Referencia nacional (B1, {FECHA}): necesidad total {f0(nac_n)} viviendas/año (rango {f0(d.N_anual_min.sum())}-{f0(d.N_anual_max.sum())}), suma de 52 provincias; "
          f"construcción adicional de P-D v3: +{f0(PD_LO)} a +{f0(PD_HI)} viviendas/año (C2 en signo; reparto por provincia proporcional a la necesidad, supuesto C4); "
          "vacías movilizables: 10-30 % de las vacías en provincias con presión (clases 1-2), repartidas en 10 años. Contexto: B2 proyecta 1.296.672 viviendas de déficit a fin de 2030 "
          "(escenario a, C4) con el ritmo actual de terminadas (≈94.650/año, 2023-2025).\n",
          "## Resumen por clase\n",
          "| clase | provincias (robustas) | necesidad anual (rango) | cuota | P-D adicional por año | cobertura P-D | vacías movilizables por año (rango) | cobertura vacías (central) |", "|---|---|---|---|---|---|---|---|"]
    for r in g.itertuples():
        if r.clase == 9:
            md.append(f"| 9 | {r.n} ({r.robustas}) | {f0(r.N_central)} ({f0(r.N_min)}-{f0(r.N_max)}) | {r.cuota_N_pct:.1f} % | No evaluable: sin clase | No evaluable | No evaluable | No evaluable |")
        else:
            md.append(f"| {r.clase} | {r.n} ({r.robustas}) | {f0(r.N_central)} ({f0(r.N_min)}-{f0(r.N_max)}) | {r.cuota_N_pct:.1f} % | {f0(r.pd_min)}-{f0(r.pd_max)} | "
                      f"{r.cob_pd_min_pct:.0f}-{r.cob_pd_max_pct:.0f} % | {f0(r.vac_central)} ({f0(r.vac_min)}-{f0(r.vac_max)}) | {r.cob_vac_pct:.0f} % |")
    md.append("")
    for c in (1, 2, 3, 9):
        r = g[g.clase == c].iloc[0]
        x = COMBI[c]
        md += [f"## Clase {c} ({int(r.n)} provincias, {int(r.robustas)} con clase robusta en el diagnóstico)\n",
               f"- Con la evidencia disponible, en provincias de clase {c} los instrumentos con signo estable son: {x['estable']}.",
               f"- Evidencia verificada aplicable: {x['verificada']}.",
               f"- Plazo: {x['plazo']}.",
               ("- Necesidad cubierta (orden de magnitud): No evaluable: sin dato de clase." if c == 9 else
                f"- Necesidad cubierta (orden de magnitud, C4): necesidad {f0(r.N_central)} viviendas/año; la construcción adicional de P-D (+{f0(PD_LO)} a +{f0(PD_HI)} nacional, repartida por cuota) "
                f"aportaría {f0(r.pd_min)}-{f0(r.pd_max)} viviendas/año ({r.cob_pd_min_pct:.0f}-{r.cob_pd_max_pct:.0f} % de la necesidad de la clase) y la movilización de vacías "
                f"{f0(r.vac_central)} viviendas/año en el central ({r.cob_vac_pct:.0f} %)."),
               f"- No recomendados por la evidencia en esta clase: {x['no_rec']}.\n"]
    md += ["## Lectura transversal (C4)\n",
           f"- Con la construcción adicional de P-D (+{f0(PD_LO)} a +{f0(PD_HI)}/año) el porcentaje de cobertura es igual en todas las clases por construcción del reparto proporcional (supuesto): solo la cifra absoluta distingue las clases. Cubre una fracción de la necesidad central nacional ({f0(nac_n)}/año), no su totalidad.",
           "- La movilización de vacías sí difiere por clase, porque depende de las vacías de cada provincia con presión: en el central cubre un 30 % de la necesidad en la clase 1 y un 74 % en la clase 2 (con 10-30 % de movilización; rango en la tabla). En las clases 3 y 9 B1 no asigna movilización (sin presión).",
           "- La necesidad se concentra en la clase 1 (88 % del total), donde la respuesta de oferta de A4 es mayor; en la clase 2 la combinación de signo estable es la misma, pero con una oferta sin respuesta el cuello de botella es de suelo o regulatorio, sobre el que solo hay literatura verificada de otros países.",
           "- Limitaciones: B1 en C4; la clase y la respuesta de oferta de A4 son C4; el reparto proporcional de P-D es un supuesto; las vacías de B1 no se asignan a clases sin presión; la literatura es de otros países y su magnitud proviene de resúmenes secundarios.\n",
           "Tabla por provincia: `output/v5/D2/politica_territorio.csv`; suma provincial = nacional comprobada en `control_sumas.json`."]
    (OUT / "politica_territorio.md").write_text("\n".join(md), encoding="utf-8")
    hechos = []
    for r in g.itertuples():
        hechos.append(dict(id=f"D2-H0{r.clase}", indicador=f"Necesidad anual de vivienda, provincias de clase A4 {r.clase} (B1)", valor=round(r.N_central), min=round(r.N_min), max=round(r.N_max),
                           unidad="viviendas/año", periodo="2026-2035", cobertura=f"{r.n} provincias", fuentes="output/v5/B1; output/v5/A4", capa="C4", fecha_dato=FECHA))
        if r.clase != 9:
            hechos.append(dict(id=f"D2-H1{r.clase}", indicador=f"Cobertura de la necesidad por la construcción adicional de P-D (+25-100 mil/año repartidas por cuota), clase {r.clase}",
                               valor=round((r.cob_pd_min_pct + r.cob_pd_max_pct) / 2, 1), min=round(r.cob_pd_min_pct, 1), max=round(r.cob_pd_max_pct, 1), unidad="%", periodo="2026-2035",
                               cobertura=f"{r.n} provincias", fuentes="output/v3/PD; output/v5/B1; output/v5/A4", capa="C4", fecha_dato=FECHA))
    (OUT / "hechos.json").write_text(json.dumps(hechos, ensure_ascii=False, indent=1))
    res = {"rama": "D2", "pregunta": "¿Qué combinación de instrumentos tiene signo estable o evidencia verificada aplicable en cada clase de provincia, y qué parte de la necesidad cubre?",
           "capa": "C4", "datos": ["output/v5/B1", "output/v5/B2", "output/v5/A4", "output/v5/D1", "output/v3/PD"], "N": {"provincias": int(len(d))},
           "metodo": "cruce de tablas; reparto de P-D por cuota de necesidad (supuesto); vacías de B1 a 10 años", "estimacion": {"necesidad_anual_nacional": nac_n,
           "por_clase": {int(r.clase): dict(necesidad=r.N_central, cobertura_pd_pct=[r.cob_pd_min_pct, r.cob_pd_max_pct], cobertura_vacias_pct=r.cob_vac_pct) for r in g.itertuples()}},
           "ic95": None, "p_ajustado": None, "nivel_evidencia": "EXPLORATORIO (C4)", "diagnosticos": {"control_sumas": "output/v5/D2/control_sumas.json", "todos_ok": True},
           "fuera_muestra": {"modelo": None, "rmse": None, "dm_vs_ar4": None}, "notas": "Lenguaje condicional; sin efectos por clase; sin especificaciones nuevas."}
    (OUT / "resultado.json").write_text(json.dumps(res, ensure_ascii=False, indent=1, default=float))
    return res


if __name__ == "__main__":
    main()
    print((OUT / "resumen_por_clase.csv").read_text())
