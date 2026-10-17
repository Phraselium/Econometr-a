"""V16 fase 6 · Q7a · Bono Alquiler Joven como diferencia en discontinuidades por edad (35 años) en la ECV. Descriptiva, C4.

Antes 2018-2021 (Plan Estatal 2018-2021) y después 2023-2025 (Bono Alquiler Joven); 2022 queda fuera (transición).
Corte entre 35 y 36 años de la edad del sustentador principal. Sin intervalo: no se usa Kolesár-Rothe (adenda, punto 3).
Precisiones: docs/v16/desviaciones.md, D3. Uso: python3 src/v16/q7_bono.py
"""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

import numpy as np
import pandas as pd

from src.v16 import q_comun as Q

OUT = ROOT / "output" / "v16" / "q7"
ANTES, DESPUES = list(range(2018, 2022)), [2023, 2024, 2025]
ANCHOS = (3, 5, 7)


def extraer() -> pd.DataFrame:
    from src.v16 import f2_esfuerzo_datos as D, f2_esfuerzo_nucleo as N
    d = D.cargar(anios=ANTES + DESPUES)
    x = N.preparar(d)
    x = x[x.edad_sust.between(28, 42)]
    keep = ["anio", "hid", "ccaa", "edad_sust", "ten", "HH060", "HY020", "DB090", "n_pers", "nac_g"]
    return x[keep].reset_index(drop=True)


def datos() -> pd.DataFrame:
    # Microdatos de hogar de la ECV: se extraen en memoria en cada ejecución y no se guardan en output/ (nunca datos crudos en salidas).
    return extraer()


def wls(y, X, w):
    sw = np.sqrt(w)
    b, *_ = np.linalg.lstsq(X * sw[:, None], y * sw, rcond=None)
    return b


def did_disc(df: pd.DataFrame, y: str, h: int, corte: int = 35):
    """Diferencia en discontinuidades: coeficiente de T×post. Lineal local, pendientes por lado y periodo, pesos DB090."""
    s = df[df.edad_sust.between(corte - h, corte + h) & df.anio.isin(ANTES + DESPUES)].dropna(subset=[y, "DB090"]).copy()
    s["T"] = (s.edad_sust <= corte).astype(float)
    s["e"] = s.edad_sust - (corte + 0.5)
    s["post"] = s.anio.isin(DESPUES).astype(float)
    X = np.column_stack([np.ones(len(s)), s["T"], s.e, s.e * s["T"], s.post, s.post * s["T"], s.post * s.e, s.post * s.e * s["T"]])
    b = wls(s[y].to_numpy(float), X, s.DB090.to_numpy(float))
    # saltos por periodo
    out = {"salto_antes": float(b[1]), "salto_despues": float(b[1] + b[5]), "diferencia_en_discontinuidades": float(b[5]), "n": int(len(s)),
           "n_antes_T": int(((s.post == 0) & (s["T"] == 1)).sum()), "n_antes_noT": int(((s.post == 0) & (s["T"] == 0)).sum()),
           "n_despues_T": int(((s.post == 1) & (s["T"] == 1)).sum()), "n_despues_noT": int(((s.post == 1) & (s["T"] == 0)).sum())}
    return out


def preparar_resultados(x: pd.DataFrame):
    r = x[x.ten == "alquiler_mercado"].copy()
    r = r[r.HH060 > 0]
    r["log_alquiler"] = np.log(r.HH060)
    r["alq_renta"] = np.where(r.HY020 > 0, np.minimum(12 * r.HH060 / r.HY020, 1.0), np.nan)
    r["ln_renta_hogar"] = np.where(r.HY020 > 0, np.log(r.HY020.where(r.HY020 > 0)), np.nan)
    r["extranjero"] = (r.nac_g != "Espana").astype(float)
    x = x.copy()
    x["inquilino_mercado"] = (x.ten == "alquiler_mercado").astype(float)
    return r, x


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    x = datos()
    r, xt = preparar_resultados(x)
    reg, res = [], {}
    for y, nom in (("log_alquiler", "log del alquiler mensual (HH060)"), ("alq_renta", "alquiler anual / renta del hogar (tope 1)")):
        for h in ANCHOS:
            o = did_disc(r, y, h)
            res[f"{y}|{h}"] = o
            reg.append({"id": f"Q7a-{y}-h{h}", "pregunta": "Q7a", "rol": "principal" if (y, h) == ("log_alquiler", 5) else "multiverso declarado",
                        "especificacion": f"diff-in-disc, {nom}, ancho ±{h} años", "muestra": "inquilinos de mercado, sustentador 35±h, 2018-21 vs 2023-25", "n": o["n"],
                        "estimacion": o["diferencia_en_discontinuidades"], "unidad": "Δlog" if y == "log_alquiler" else "proporción de la renta",
                        "inferencia": "ninguna (sin intervalo; no se usa Kolesár-Rothe)", "nota": ""})
    # umbrales placebo (ancho 3, sin tocar el corte real)
    pl = {}
    for c in (31, 39):
        pl[c] = did_disc(r, "log_alquiler", 3, corte=c)
        reg.append({"id": f"Q7a-PL-{c}", "pregunta": "Q7a", "rol": "placebo de umbral", "especificacion": f"diff-in-disc log alquiler, corte falso {c}|{c + 1}, ±3", "muestra": "ídem", "n": pl[c]["n"],
                    "estimacion": pl[c]["diferencia_en_discontinuidades"], "unidad": "Δlog", "inferencia": "ninguna", "nota": "debería estar cerca de 0"})
    # balance de covariables y proporción de inquilinos en el umbral
    bal = {}
    for v in ("ln_renta_hogar", "n_pers", "extranjero"):
        bal[v] = did_disc(r, v, 5)["diferencia_en_discontinuidades"]
    prop = did_disc(xt, "inquilino_mercado", 5)
    reg.append({"id": "Q7a-PROP", "pregunta": "Q7a", "rol": "diagnóstico (proporción de inquilinos)", "especificacion": "diff-in-disc de la proporción de inquilinos de mercado, ±5", "muestra": "todos los hogares 30-40", "n": prop["n"],
                "estimacion": prop["diferencia_en_discontinuidades"], "unidad": "proporción", "inferencia": "ninguna", "nota": ""})
    # densidad por edad (discreta) del corte
    dens = {}
    for per, ys in (("antes", ANTES), ("despues", DESPUES)):
        s = r[r.anio.isin(ys)]
        c = s.groupby("edad_sust").DB090.sum()
        dens[per] = {"hogares_ponderados_edad_35": float(c.get(35, 0)), "hogares_ponderados_edad_36": float(c.get(36, 0)), "razon_35_36": float(c.get(35, np.nan) / c.get(36, np.nan))}
    # robustez: pendiente constante (cuadrática no) -> sin 2 CCAA grandes no aplica (ECV sin provincia); se omite
    pp = res["log_alquiler|5"]
    vals = [v["diferencia_en_discontinuidades"] for k, v in res.items() if k.startswith("log_alquiler")]
    resumen = {"principal_log_alquiler_h5": pp, "porcentaje_equivalente_principal": float(np.expm1(pp["diferencia_en_discontinuidades"]) * 100),
               "multiverso_log_alquiler": {k: v["diferencia_en_discontinuidades"] for k, v in res.items() if k.startswith("log_alquiler")},
               "multiverso_alq_renta": {k: v["diferencia_en_discontinuidades"] for k, v in res.items() if k.startswith("alq_renta")},
               "mediana_log_alquiler": float(np.median(vals)), "mismo_signo_que_principal": float(np.mean([np.sign(v) == np.sign(vals[1]) for v in vals])),
               "placebos_umbral": {str(k): v["diferencia_en_discontinuidades"] for k, v in pl.items()}, "balance_diff_in_disc": bal,
               "proporcion_inquilinos": prop, "densidad_edad": dens,
               "cota_incidencia_con_cobertura_plena_pct": 13.9,
               "plan_2018_2021": {"fuente": "BOE-A-2018-3358 (RD 106/2018), capítulo IX, programa de ayuda a los jóvenes", "consultado": Q.CORTE,
                                  "existia_programa_para_menores_de_35": True,
                                  "requisito": "ayuda al alquiler para quien tiene «menos de treinta y cinco años» en el momento de solicitar, con ingresos limitados",
                                  "lectura": "la diferencia en discontinuidades mide un CAMBIO de generosidad entre el Plan 2018-2021 y el Bono Alquiler Joven (hasta 35 años inclusive), no el efecto de un programa nuevo; el corte legal difiere en un año (34|35 frente a 35|36) y la edad de la ECV es la diferencia de años de nacimiento"},
               "n_hogares_total": int(len(r))}
    Q.registro(reg, OUT / "registro.csv")
    Q.jdump(resumen, OUT / "q7_detalle.json")
    print(pp, resumen["porcentaje_equivalente_principal"], resumen["placebos_umbral"])


if __name__ == "__main__":
    main()
