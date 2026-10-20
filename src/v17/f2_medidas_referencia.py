"""V17 · Fase 2 · B5: medidas de referencia del Banco de España (análisis a posteriori).

Lee la Síntesis de indicadores del mercado de la vivienda del Banco de España (data/raw/v17/credito/bde_si_1_5.csv) y las
hipotecas (INE H) y compraventas (INE ETDP) del repositorio. Para cada indicador da el último valor, el de 2007 (máximo del
ciclo anterior), el de 2019 y la media histórica, y la desviación respecto a esa media. Es la forma en que el Banco de España lee
la sobrevaloración «frente a su media». Aproxima además la proporción de compras sin hipoteca.

Salidas: output/v17/lectura_bde/medidas_referencia/{medidas.csv, informe.md, hechos.json}. Determinista; sin red; no lee
data/sealed ni la base (solo series nacionales).
"""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd

ALCANCE_TERRITORIAL = "nacional"   # guarda de fuga v6 (check_v17): solo series nacionales: Síntesis del BdE, hipotecas (nivel nacional) y compraventas (Total Nacional)
RAIZ = Path(__file__).resolve().parents[2]
SI = RAIZ / "data" / "raw" / "v17" / "credito" / "bde_si_1_5.csv"
OUT = RAIZ / "output" / "v17" / "lectura_bde" / "medidas_referencia"
FECHA = "2026-10-19"
MESES = {"ENE": 1, "FEB": 2, "MAR": 3, "ABR": 4, "MAY": 5, "JUN": 6, "JUL": 7, "AGO": 8, "SEP": 9, "OCT": 10, "NOV": 11, "DIC": 12}

# alias -> (id V17, nombre, para qué se usa en B5)
SERIES = {
    "SI_1_5.43": ("V17-B5-PRECIO-RENTA", "Precio de la vivienda / renta bruta por hogar (años)", "sobrevaloración y acceso"),
    "SI_1_5.44": ("V17-B5-ESFUERZO-TEORICO", "Esfuerzo teórico anual sin deducciones (% de la renta)", "acceso"),
    "SI_1_5.63": ("V17-B5-RENTABILIDAD-ALQUILER", "Rentabilidad bruta por alquiler, doce meses (%)", "sobrevaloración (inversa del precio/alquiler)"),
    "SI_1_5.38": ("V17-B5-LTV", "Relación préstamo-valor (RPV o LTV) de transacción (%)", "crédito"),
    "SI_1_5.39": ("V17-B5-LTV80", "Préstamos con RPV mayor que 80 % (% del total)", "crédito"),
    "SI_1_5.56": ("V17-B5-CREDITO-PIB", "Saldo del crédito a hogares para vivienda (% del PIB)", "crédito"),
    "SI_1_5.55": ("V17-B5-CREDITO-TASA", "Crédito a hogares para adquisición de vivienda, tasa interanual (%)", "crédito"),
    "SI_1_5.59": ("V17-B5-DUDOSIDAD", "Ratio de dudosidad del crédito a hogares para vivienda (%)", "crédito"),
}


def leer_si() -> pd.DataFrame:
    d = pd.read_csv(SI, encoding="latin-1", header=None, dtype=str)
    alias = d.iloc[2].tolist()
    filas = d.iloc[6:].copy()
    filas = filas[filas[0].str.match(r"^[A-Z]{3} \d{4}$", na=False)]
    fecha = filas[0].map(lambda s: pd.Timestamp(int(s[4:]), MESES[s[:3]], 1))
    largo = []
    for j, a in enumerate(alias):
        if a not in SERIES:
            continue
        v = pd.to_numeric(filas[j].str.replace(",", "."), errors="coerce")
        largo.append(pd.DataFrame({"alias": a, "fecha": fecha.values, "valor": v.values}).dropna())
    return pd.concat(largo, ignore_index=True)


def resumen(s: pd.DataFrame) -> dict:
    s = s.sort_values("fecha")
    anual = s.groupby(s.fecha.dt.year).valor.mean()
    ult = s.iloc[-1]
    media = float(anual.loc[: ult.fecha.year - 1].mean())   # media histórica de años completos
    return {"ultimo": float(ult.valor), "fecha_ultimo": ult.fecha.strftime("%Y-%m"),
            "media_2007": float(anual.get(2007, np.nan)), "media_2019": float(anual.get(2019, np.nan)),
            "media_historica": media, "inicio": int(anual.index.min()), "fin_media": int(ult.fecha.year - 1),
            "desv_media_pct": 100 * (float(ult.valor) / media - 1) if media else np.nan,
            "max": float(anual.max()), "anio_max": int(anual.idxmax())}


def compras_sin_hipoteca() -> pd.DataFrame:
    h = pd.read_csv(RAIZ / "data" / "raw" / "ine_v2_hipotecas_prov.csv")
    h = h[(h.nivel == "nacional") & (h.medida == "hipotecas_viviendas_numero")]
    h = h.assign(anio=h.periodo.str[:4].astype(int)).groupby("anio").agg(hip=("valor", "sum"), n=("valor", "size"))
    e = pd.read_csv(RAIZ / "data" / "raw" / "ine_etdp_compraventas.csv")
    e = e[e.nombre == "Total Nacional. General. Compraventa. Número."]
    e = e.assign(anio=e.periodo.str[:4].astype(int)).groupby("anio").agg(cv=("valor", "sum"), m=("valor", "size"))
    x = h.join(e, how="inner")
    x = x[(x.n == 12) & (x.m == 12)]
    x["pct_con_hipoteca_max"] = 100 * x.hip / x.cv
    x["pct_sin_hipoteca_min"] = 100 - x.pct_con_hipoteca_max
    x["informativa"] = x.pct_sin_hipoteca_min >= 0   # con más hipotecas que compraventas la aproximación no dice nada
    return x.reset_index()


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    largo = leer_si()
    filas, hechos = [], []
    for a, (i, nombre, uso) in SERIES.items():
        r = resumen(largo[largo.alias == a])
        filas.append({"id": i, "alias_bde": a, "indicador": nombre, "uso_b5": uso, **r})
        hechos.append({"id": i, "indicador": f"{nombre}, último dato", "valor": round(r["ultimo"], 3),
                       "min": round(r["media_historica"], 3), "max": round(r["max"], 3), "unidad": nombre.split("(")[-1].rstrip(")"),
                       "periodo": r["fecha_ultimo"], "cobertura": "España",
                       "fuentes": ["Banco de España, Síntesis de indicadores del mercado de la vivienda (SI_1_5)"],
                       "capa": "C4", "lectura_v17": "OF", "tipo_rango": "referencias", "fecha_dato": r["fecha_ultimo"],
                       "ficha": "output/v17/lectura_bde/medidas_referencia/informe.md",
                       "nota": f"a posteriori; min = media histórica {r['inicio']}-{r['fin_media']}; max = máximo anual ({r['anio_max']})"})
    m = pd.DataFrame(filas)
    m.to_csv(OUT / "medidas.csv", index=False, float_format="%.4f")
    sh = compras_sin_hipoteca()
    sh.to_csv(OUT / "compras_sin_hipoteca.csv", index=False, float_format="%.3f")
    ult = sh.iloc[-1]
    shi = sh[sh.informativa]
    hechos.append({"id": "V17-B5-SIN-HIPOTECA-MIN", "indicador": "Compras de vivienda sin hipoteca, cota inferior (1 - hipotecas sobre "
                   "viviendas / compraventas de viviendas)", "valor": round(float(ult.pct_sin_hipoteca_min), 2),
                   "min": round(float(shi.pct_sin_hipoteca_min.min()), 2), "max": round(float(shi.pct_sin_hipoteca_min.max()), 2),
                   "unidad": "% de las compraventas", "periodo": str(int(ult.anio)), "cobertura": "España",
                   "fuentes": ["INE, Estadística de Hipotecas", "INE, Estadística de Transmisiones de Derechos de la Propiedad"],
                   "capa": "C4", "lectura_v17": "cota", "tipo_rango": "referencias", "fecha_dato": str(int(ult.anio)),
                   "ficha": "output/v17/lectura_bde/medidas_referencia/informe.md",
                   "nota": "a posteriori; cota inferior: las hipotecas sobre viviendas incluyen las no ligadas a una compra; "
                           f"min y max = rango anual de los años informativos {int(shi.anio.min())}-{int(shi.anio.max())}"})
    (OUT / "hechos.json").write_text(json.dumps(hechos, ensure_ascii=False, indent=1), encoding="utf-8")

    def f(x, d=1):
        return "n/d" if pd.isna(x) else f"{x:,.{d}f}".replace(",", "X").replace(".", ",").replace("X", ".")
    L = ["# V17 · B5 · Medidas de referencia del Banco de España", "",
         "Análisis a posteriori (V17). Generado por src/v17/f2_medidas_referencia.py. Las cifras son estadísticas oficiales de fuente "
         "única (lectura «OF»); en la capa del proyecto son C4. No cambian ninguna cifra publicada.", "",
         "## Indicadores del Banco de España", "",
         "La lectura del Banco de España compara el último dato con su media histórica y con el máximo del ciclo anterior (2007). "
         "Una desviación positiva del precio/renta o del esfuerzo indica menor accesibilidad; una rentabilidad por alquiler menor que "
         "su media indica precios altos frente al alquiler.", "",
         "| Indicador | Último | Fecha | 2007 | 2019 | Media histórica (años) | Desviación frente a la media | Uso |",
         "|---|---|---|---|---|---|---|---|"]
    for r in filas:
        L.append(f"| {r['indicador']} | {f(r['ultimo'], 2)} | {r['fecha_ultimo']} | {f(r['media_2007'], 2)} | {f(r['media_2019'], 2)} | "
                 f"{f(r['media_historica'], 2)} ({r['inicio']}-{r['fin_media']}) | {f(r['desv_media_pct'])} % | {r['uso_b5']} |")
    L += ["", "## Compras sin hipoteca (aproximación)", "",
          "Proporción de compraventas de viviendas que no tienen una hipoteca sobre vivienda constituida el mismo año. Es una COTA "
          "INFERIOR: la estadística de hipotecas incluye préstamos no ligados a una compra (refinanciaciones, autopromoción), así que "
          "1 - hipotecas/compraventas subestima las compras al contado. La serie del Notariado, que las mide directamente, queda como "
          "tarea del autor (docs/v18/tareas_autor.md). Hasta 2011 se constituían más hipotecas sobre viviendas que compraventas "
          "(refinanciaciones, autopromoción y el desfase entre escritura e inscripción), así que en esos años la aproximación no es "
          "informativa y no se usa.", "",
          "| Año | Hipotecas sobre viviendas | Compraventas de viviendas | Sin hipoteca (cota inferior) |", "|---|---|---|---|"]
    for r in sh.itertuples():
        v = f"{f(r.pct_sin_hipoteca_min)} %" if r.informativa else "no informativa"
        L.append(f"| {r.anio} | {f(r.hip, 0)} | {f(r.cv, 0)} | {v} |")
    L += ["", "## Otras medidas de B5 ya publicadas en el repositorio", "",
          "- **Precio ajustado por calidad (IPV del INE) como medida principal.** La variación real 2019-2025 es la cifra "
          "V16-HEC-INTL-RHP-ES-2019-2025, y la del precio medio por m² tasado está en el informe integral (Parte I). El sesgo de "
          "composición de los precios medios se analiza en la fase 3 (fila «Precio»).",
          "- **Precio deflactado por renta.** Precio/renta disponible de Eurostat: V16-HEC-INTL-HPI_YDH-ES-2019-2025 y 2007-2025.",
          "- **Sobrevaloración.** GSADF corregido (V7.2, B-4: R1B-G-*) y factor común de V16 (Q9-g, pista no confirmada). El "
          "Banco de España estima la sobrevaloración con sus propios modelos (docs/v17/referencias/bde_bce_documentos.md).", ""]
    (OUT / "informe.md").write_text("\n".join(L), encoding="utf-8")
    print(f"f2_medidas_referencia V17: {len(filas)} indicadores BdE; compras sin hipoteca {int(sh.anio.min())}-{int(sh.anio.max())}; "
          f"{len(hechos)} cifras V17-B5")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
