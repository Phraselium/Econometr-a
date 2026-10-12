"""V7: fichas nuevas del verificador y cuenta acumulada de especificaciones entre versiones. Sin red; lee output/v7.

Escribe output/v7/fichas/fichas_verificador.json y output/v7/cuenta_especificaciones.{csv,md}.
"""
from __future__ import annotations

import glob
import json
import re
from collections import Counter
from pathlib import Path

import pandas as pd

RAIZ = Path(__file__).resolve().parents[2]
V7 = RAIZ / "output" / "v7"


def es(x, d=1):
    return f"{x:.{d}f}".replace(".", ",")


def fichas() -> list[dict]:
    h4 = {x["id"]: x for x in json.loads((V7 / "R4" / "hechos.json").read_text())}
    im = pd.read_csv(V7 / "R6" / "impactos.csv", dtype={"cc": str})
    x = im[(im.horizonte == 10) & (im.fuente_es == "rejilla") & (im.instrumento == "e_ayuda_demanda") & (im.mercado == "precio")]
    lp = pd.read_csv(V7 / "R4b" / "lp_compra.csv")
    sig = int((lp.filter(regex="q_bh|p_bh|bh").min(axis=1) < 0.10).sum()) if lp.filter(regex="q_bh|p_bh|bh").shape[1] else 0
    c1, a1 = h4["V7-R4-H7-C1"], h4["V7-R4-H7-A1"]
    base = dict(capa="C4", cota="—", veredicto="ANALIZADA, NO CONCLUYENTE",
                regla="Con capa C4 el veredicto es como máximo ANALIZADA, NO CONCLUYENTE. Muestra regional ya vista en v1; la validación limpia es diferida (make evaluate_v7).")
    return [
        dict(id="V7-V1", tema="Determinantes regionales de largo plazo",
             enunciado="En cada comunidad autónoma, el precio y el alquiler dependen a largo plazo sobre todo del empleo y de la población.",
             magnitud=(f"Paneles de 17 CCAA, 2007T1-2026T2 (MG con demeaning, PMG y CS-DL). Ninguna de las 7 hipótesis de largo plazo se confirma tras "
                       f"Holm y triangulación. Rango del coeficiente del empleo en alquiler: {es(a1['min'],3)} a {es(a1['max'],3)}; en compra: "
                       f"{es(c1['min'],2)} a {es(c1['max'],2)}. La velocidad de ajuste no es significativa frente al valor crítico simulado."),
             intervalo="rango entre estimadores (output/v7/R4/*/hipotesis.csv)", literatura="Pesaran, Shin y Smith (1999); Chudik y Pesaran (2015).",
             limites="Con un factor común I(1) de cargas heterogéneas ningún estimador es apto en el Monte Carlo (R2); I(2) no descartado en 8 de 17 CCAA.",
             evidencia=["output/v7/R4/alquiler/resumen.md", "output/v7/R4/compra/resumen.md", "docs/v7/validacion_herramientas.md"], **base),
        dict(id="V7-V2", tema="Ayudas a la compra",
             enunciado="Las ayudas directas a la compra abaratan la vivienda.",
             magnitud=(f"Simulación de traslado (rejilla de elasticidades de v5, C4), a 10 años, mediana entre CCAA: el esfuerzo neto del beneficiario varía "
                       f"{es(x.esfuerzo_med.median())} %, pero el precio de mercado sube {es(x.dprecio_med.median())} % (afecta a quien no recibe la ayuda)."),
             intervalo=f"p5-p95 del esfuerzo: {es(x.esfuerzo_p5.median())} a {es(x.esfuerzo_p95.median())} %",
             literatura="Incidencia según elasticidades de oferta y demanda (rejilla de v5; ver docs/literatura.md).",
             limites="Elasticidad de oferta regional no utilizable (DOLS fuera de [0; 5]); parámetros supuestos.",
             evidencia=["output/v7/R6/impactos.csv", "output/v7/R6/metodo.md"], **base),
        dict(id="V7-V3", tema="Tipos de interés y regiones",
             enunciado="Las subidas de los tipos de interés abaratan la vivienda más en las regiones con más hipotecas.",
             magnitud=(f"Proyecciones locales de panel (17 CCAA) con exposición hipotecaria 2015-2019: en compra, {sig} horizontes con q de BH < 0,10 "
                       f"que no resisten a Driscoll-Kraay; en alquiler, ninguno. El signo depende de cómo se construye el shock."),
             intervalo="output/v7/R4b/lp_*.csv", literatura="Jordà (2005), proyecciones locales.",
             limites="Shock = residuo AR(2) del tipo nacional (desviación declarada); 17 unidades.",
             evidencia=["output/v7/R4b/lp_compra.csv", "output/v7/R4b/resumen.md"], **base),
    ]


def cuenta() -> pd.DataFrame:
    tot = Counter()
    for f in glob.glob(str(RAIZ / "output" / "**" / "registro*.csv"), recursive=True) + glob.glob(str(RAIZ / "output" / "registro_busqueda*.csv")):
        rel = str(Path(f).relative_to(RAIZ))
        if "_smoke" in rel:
            continue
        m = re.match(r"output/(v[0-9_]+|f[2-6])", rel)
        v = m.group(1) if m else "v1"
        v = "v1" if v.startswith("f") else v
        with open(f, encoding="utf-8", errors="ignore") as fh:
            tot[v] += max(sum(1 for _ in fh) - 1, 0)
    df = pd.DataFrame(sorted(tot.items()), columns=["version", "especificaciones_registradas"])
    df["acumulado"] = df.especificaciones_registradas.cumsum()
    return df


def main():
    (V7 / "fichas").mkdir(parents=True, exist_ok=True)
    f = fichas()
    (V7 / "fichas" / "fichas_verificador.json").write_text(json.dumps(f, ensure_ascii=False, indent=1))
    ver = ["# Verificador V7 (fichas nuevas)", "",
           "Fichas añadidas en V7. Se publican aparte para no alterar los recuentos del verificador de v6.2 (versión de referencia congelada).", ""]
    for x in f:
        ver += [f"## {x['id']} · {x['tema']}", "", f"**Afirmación evaluada:** {x['enunciado']}", "", f"**Veredicto:** {x['veredicto']} ({x['capa']})", "",
                f"**Magnitud:** {x['magnitud']}", "", f"**Intervalo:** {x['intervalo']}", "", f"**Límites:** {x['limites']}", "",
                f"**Regla:** {x['regla']}", "", "**Evidencia:** " + "; ".join(x["evidencia"]), ""]
    (V7 / "verificador_v7.md").write_text("\n".join(ver), encoding="utf-8")
    c = cuenta()
    c.to_csv(V7 / "cuenta_especificaciones.csv", index=False)
    md = ["# Especificaciones registradas por versión (registro*.csv)", "",
          "Recuento de filas de los registros de especificaciones (econ_utils.Registry y registros de búsqueda). Es una cota inferior del "
          "número de contrastes mirados: algunas exploraciones de v1-v3 no se registraron. Sirve para dimensionar el riesgo de "
          "comparaciones múltiples entre versiones (objeción A-04 del árbitro simulado).", "",
          "| Versión | Especificaciones | Acumulado |", "|---|---|---|"]
    md += [f"| {r.version} | {r.especificaciones_registradas:,} | {r.acumulado:,} |".replace(",", ".") for r in c.itertuples()]
    (V7 / "cuenta_especificaciones.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    print(f"r7_fichas: {len(f)} fichas; especificaciones acumuladas {int(c.acumulado.iloc[-1])}")


if __name__ == "__main__":
    main()
