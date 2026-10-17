"""V16 fase 6 · Q8 · compras de no residentes (MIVAU, mivau_transacciones_residencia). Descriptiva, C4.

Sin distinción UE / fuera de la UE (adenda, R23): la fuente no la trae. Agregado propio de las 9 CCAA de entrenamiento más Ceuta y Melilla
(excluye las 8 CCAA de v6). Sin estimación de efecto, sin p-valor. Uso: python3 src/v16/q8_no_residentes.py
"""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

import numpy as np
import pandas as pd

from src.v16 import q_comun as Q

OUT = ROOT / "output" / "v16" / "q8"
RAW = ROOT / "data" / "raw" / "mivau_transacciones_residencia.csv"
CCAA = ["Andalucía", "Cantabria", "Castilla-La Mancha", "Castilla y León", "Cataluña", "Comunitat Valenciana", "Extremadura", "Galicia", "País Vasco"]
SELLADAS_PROV = ["Huesca", "Teruel", "Zaragoza", "Palmas (Las)", "Santa Cruz de Tenerife"]
VARS = {"no_residentes_total": "tx_residencia_no_residentes_total", "no_res_extranjeros": "tx_residencia_no_residentes_extranjeros",
        "no_res_espanoles": "tx_residencia_no_residentes_espanoles", "total": "tx_residencia_total"}


def cargar():
    d = pd.read_csv(RAW)
    d["base"] = d.serie.str.replace(r"_(ccaa|provincia|ciudad_autonoma|nacional).*$", "", regex=True)
    aut = d[((d.nivel == "ccaa") & d.territorio.isin(CCAA)) | ((d.nivel == "ciudad_autonoma") & d.territorio.isin(["Ceuta", "Melilla"]))]
    prov = d[(d.nivel == "provincia") & ~d.territorio.isin(SELLADAS_PROV)]
    return aut, prov


def agregado(aut):
    w = aut[aut.base.isin(VARS.values())].pivot_table(index="periodo", columns="base", values="valor", aggfunc="sum")
    w = w.rename(columns={v: k for k, v in VARS.items()})
    w["cuota_no_res"] = w.no_residentes_total / w.total * 100
    w["cuota_no_res_extranjeros"] = w.no_res_extranjeros / w.total * 100
    w.index = pd.PeriodIndex([f"{p[:4]}Q{p[-1]}" for p in w.index], freq="Q")
    return w.sort_index()


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    aut, prov = cargar()
    w = agregado(aut)
    w.to_csv(OUT / "q8_trimestral.csv")
    w["anio"] = w.index.year
    anual = w.groupby("anio")[["no_residentes_total", "no_res_extranjeros", "no_res_espanoles", "total"]].sum()
    anual["cuota_no_res"] = anual.no_residentes_total / anual.total * 100
    anual["cuota_no_res_extranjeros"] = anual.no_res_extranjeros / anual.total * 100
    anual.to_csv(OUT / "q8_anual.csv")
    a0, a1 = pd.Period("2024Q2", "Q"), pd.Period("2025Q1", "Q")
    b0, b1 = pd.Period("2025Q2", "Q"), pd.Period("2026Q1", "Q")
    antes, desp = w.loc[a0:a1], w.loc[b0:b1]
    cuota = lambda s, c: float(s[c].sum() / s.total.sum() * 100)
    cambio = {"ventana_antes": f"{a0}-{a1}", "ventana_despues": f"{b0}-{b1}",
              "cuota_no_res_antes": cuota(antes, "no_residentes_total"), "cuota_no_res_despues": cuota(desp, "no_residentes_total"),
              "cuota_no_res_extranjeros_antes": cuota(antes, "no_res_extranjeros"), "cuota_no_res_extranjeros_despues": cuota(desp, "no_res_extranjeros"),
              "compras_no_res_antes": float(antes.no_residentes_total.sum()), "compras_no_res_despues": float(desp.no_residentes_total.sum()),
              "compras_total_antes": float(antes.total.sum()), "compras_total_despues": float(desp.total.sum())}
    cambio["dif_cuota_pp"] = cambio["cuota_no_res_despues"] - cambio["cuota_no_res_antes"]
    cambio["dif_cuota_extranj_pp"] = cambio["cuota_no_res_extranjeros_despues"] - cambio["cuota_no_res_extranjeros_antes"]
    # misma comparación un año antes (referencia de variación interanual habitual)
    c0, c1, d0, d1 = (pd.Period(x, "Q") for x in ("2023Q2", "2024Q1", "2024Q2", "2025Q1"))
    ref = w.loc[d0:d1], w.loc[c0:c1]
    cambio["dif_cuota_pp_referencia_ano_anterior"] = cuota(ref[0], "no_residentes_total") - cuota(ref[1], "no_residentes_total")
    # por provincia (entrenamiento): cuota de no residentes 2025 y variación 2024-2025
    p = prov[prov.base.isin([VARS["no_residentes_total"], VARS["total"]])].copy()
    p["anio"] = p.periodo.str[:4].astype(int)
    pp = p[p.anio.isin([2024, 2025])].pivot_table(index=["territorio", "anio"], columns="base", values="valor", aggfunc="sum")
    pp["cuota"] = pp[VARS["no_residentes_total"]] / pp[VARS["total"]] * 100
    cu = pp.cuota.unstack()
    cu["dif_pp"] = cu[2025] - cu[2024]
    cu.sort_values(2025, ascending=False).to_csv(OUT / "q8_provincias.csv")
    top = cu.sort_values(2025, ascending=False).head(5)
    # serie nacional de control con el agregado completo NO se usa (incluye CCAA selladas)
    reg = [{"id": "Q8-D1", "pregunta": "Q8", "rol": "descriptivo", "especificacion": "cuota de no residentes sobre el total de transacciones, agregado de entrenamiento, 4 trimestres tras 2025Q2 frente a los 4 previos",
            "muestra": "9 CCAA + Ceuta y Melilla", "n": int(len(antes) + len(desp)), "estimacion": cambio["dif_cuota_pp"], "unidad": "puntos porcentuales", "inferencia": "ninguna (descriptiva)", "nota": "sin distinción UE/extra-UE"},
           {"id": "Q8-D2", "pregunta": "Q8", "rol": "descriptivo", "especificacion": "misma comparación un año antes (referencia)", "muestra": "ídem", "n": int(len(ref[0]) + len(ref[1])),
            "estimacion": cambio["dif_cuota_pp_referencia_ano_anterior"], "unidad": "puntos porcentuales", "inferencia": "ninguna", "nota": ""}]
    Q.registro(reg, OUT / "registro.csv")
    res = {"cambio": cambio, "anual": anual.reset_index().to_dict("records"), "provincias_top5_cuota_2025": top.reset_index().to_dict("records"),
           "primer_trimestre": str(w.index.min()), "ultimo_trimestre": str(w.index.max()), "n_provincias": int(cu.shape[0])}
    Q.jdump(res, OUT / "q8_detalle.json")
    print(cambio)


if __name__ == "__main__":
    main()
