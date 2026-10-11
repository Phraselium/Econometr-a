"""E-T7 (v5.1): cifras extra para la actualización de entregables con T1-T4 de v5.1.

Todo se LEE de output/v5_1 (nada tecleado). Ids con prefijo E-T7-.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
from e_hechos import h  # noqa: E402

R = Path(__file__).resolve().parents[2]
O51 = R / "output" / "v5_1"


def _j(p: Path) -> dict:
    return json.loads(p.read_text())


def filas() -> list[dict]:
    out = []
    # T1: demoliciones con licencia en 2024, en % del parque (estrecha y amplia)
    d = pd.read_csv(O51 / "T1/tablas/licencias_demolicion_nacional.csv").set_index("anio").loc[2024]
    out.append(h("E-T7-demol-2024", "Viviendas con licencia de demolición en 2024 en % del parque (definición estrecha y amplia)",
                 None, 100 * float(d["tasa_D_estrecha"]), 100 * float(d["tasa_D_amplia"]), "% del parque", "2024",
                 "España", "MIVAU licencias municipales de obra; MIVAU parque", "C4", "2024-12-31"))
    t3 = _j(O51 / "T3/resultado.json")["estimacion"]
    # T3: producción con la misma cobertura que la necesidad (nacional con País Vasco y Navarra)
    p = t3["producciones_serie"]["nacional_con_PV_NA_2019_2024"]
    out.append(h("E-T7-prod", "Viviendas terminadas al año, España con País Vasco y Navarra (mín. y máx. anual)",
                 None, float(p[0]), float(p[1]), "viviendas/año", "2019-2024", "España (52 provincias)",
                 "MIVAU terminadas libres y protegidas", "C1", "2024-12-31"))
    # T3: peso de cada supuesto en la amplitud de la necesidad anual
    for k, i in [("movilizables (M)", "M"), ("flujo futuro (F)", "F"), ("atraso (A1+A2)", "A"),
                 ("liberadas que no llegan al mercado (X)", "X"), ("reposición (R)", "R"),
                 ("vacancia friccional (V)", "V"), ("cartera (K)", "K")]:
        v = t3["descomposicion_amplitud_anual"][k]
        out.append(h(f"E-T7-peso-{i}", f"Peso en la amplitud de la necesidad anual 2026-2035: {k}",
                     float(v["peso_pct"]), None, None, "%", "2026-2035", "España (52 provincias)", "T3 (v5.1)", "C4", "2026-10-11"))
    # T2: liberadas 2026-2035 por tipo de municipio (central)
    t2 = _j(O51 / "T2/resultado.json")["estimacion"]["por_tipo_municipio_central_2026_2035"]
    for k, i, ind in [("capital", "capital", "capitales de provincia"), ("entorno_grande", "entorno", "entorno de las grandes ciudades"),
                      ("resto", "resto", "resto de municipios")]:
        out.append(h(f"E-T7-lib-{i}", f"Viviendas liberadas por envejecimiento en {ind} (central)", float(t2[k]), None, None,
                     "viviendas", "2026-2035", "52 provincias", "T2 (v5.1); INE 54562; INE 36726; INE Censo 2021", "C4", "2026-06-17"))
    return out
