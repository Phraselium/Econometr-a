"""E-2 (v5): cifras extra para artículos (E3), artículo del Colegio (E4) y ponencia (E5).

Todo se LEE de salidas de módulos (output/v5, output/v4, output/v3); nada tecleado. Ids con prefijo E-.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
from e_hechos import h  # noqa: E402

R = Path(__file__).resolve().parents[2]
O5, O4, O3 = R / "output" / "v5", R / "output" / "v4", R / "output" / "v3"


def _j(p: Path) -> dict:
    return json.loads(p.read_text())


def _b1() -> list[dict]:
    out = []
    nac = pd.read_csv(O5 / "B1/tablas/B1_nacional.csv").set_index("componente")
    fu = "INE Proyección de Hogares; INE mortalidad; Censo 2021; MIVAU; Catastro"
    per = "2026-2035"
    g = lambda c, k: float(nac.loc[c, k])  # noqa: E731
    for c, ind, capa in [("N10", "Necesidad de vivienda acumulada en 10 años (A+R+V+F-M-K), suma de 52 provincias", "C4"),
                         ("A1", "Atraso: déficit 2021-2025 (componente A1)", "C4"),
                         ("A2", "Atraso: emancipación retrasada (componente A2)", "C4"),
                         ("F", "Crecimiento de hogares proyectado (componente F, 10 años)", "C2"),
                         ("M", "Vacías movilizables en zonas con presión (componente M, 10 años)", "C4"),
                         ("K", "Cartera en construcción (componente K)", "C4"),
                         ("L", "Viviendas liberadas por envejecimiento (componente L, 10 años; no se resta)", "C4"),
                         ("R", "Reposición del parque (componente R, 10 años; límite inferior)", "C4")]:
        out.append(h(f"E-B1-{c}", ind, g(c, "central"), g(c, "min"), g(c, "max"), "viviendas", per, "España (52 provincias)", fu, capa, "2026"))
    out.append(h("E-B1-anual", "Necesidad de vivienda por año (N10/10), suma de 52 provincias", g("N10", "central") / 10,
                 g("N10", "min") / 10, g("N10", "max") / 10, "viviendas/año", per, "España (52 provincias)", fu, "C4", "2026"))
    for c, ind in [("N10_formula_literal_menos_L", "Variante literal: necesidad 10 años restando además L (duplica disoluciones)"),
                   ("N10_solo_presion_central", "Necesidad 10 años solo en provincias con presión"),
                   ("L_en_presion_central", "Viviendas liberadas por envejecimiento en provincias con presión (10 años)")]:
        out.append(h(f"E-B1-{c}", ind, g(c, "central"), None, None, "viviendas", per, "España", fu, "C4", "2026"))
    out.append(h("E-B1-npresion", "Provincias con presión (clase A4 1-3)", g("n_prov_presion", "central"), None, None,
                 "provincias", per, "52 provincias", "A4; B1", "C4", "2025"))
    d = _j(O5 / "B1/resultado.json")["diagnosticos"]
    out.append(h("E-B1-Rnopos", "Provincias con tasas brutas de baja no positivas en los dos métodos de reposición",
                 d["R_prov_con_ambas_tasas_no_positivas"], None, None, "provincias", "2011-2025", "52 provincias",
                 "Censo 2011-2021; Catastro; MIVAU", "C4", "2025"))
    pv = pd.read_csv(O5 / "B1/tablas/B1_provincias.csv", dtype={"cod_prov": str})
    for cod, nom in [("46", "Valencia"), ("03", "Alicante"), ("12", "Castellon"), ("28", "Madrid"), ("08", "Barcelona")]:
        r = pv[pv.cod_prov.str.zfill(2) == cod].iloc[0]
        out.append(h(f"E-B1-anual-{nom}", f"Necesidad de vivienda por año, provincia de {r.provincia}", r.N_anual_central,
                     r.N_anual_min, r.N_anual_max, "viviendas/año", per, r.provincia, fu, "C4", "2026"))
    return out


def _b2() -> list[dict]:
    out = []
    b = pd.read_csv(O5 / "B2/tablas/B2_provincias_completo.csv")
    vc = b.signo.value_counts()
    for s in ("empeora", "mejora", "indeterminado"):
        out.append(h(f"E-B2-{s}", f"Provincias cuyo déficit 2025-2030 {s} en todo el rango (ritmo actual)", int(vc.get(s, 0)),
                     None, None, "provincias", "2025 a 2030", "52 provincias", "B2 (INE hogares; MIVAU)", "C4", "2025"))
    e = pd.read_csv(O5 / "B2/tablas/B2_escenarios_nacional.csv").set_index("escenario")
    out.append(h("E-B2-D2030-b", "Déficit acumulado a fin de 2030, escenario b (cartera con retardo)", e.loc["b", "D2030_central"],
                 None, None, "viviendas", "2026-2030", "España", "B2 (INE hogares; MIVAU)", "C4", "2025"))
    out.append(h("E-B2-Tb", "Terminadas 2026-2030, escenario b (cartera con retardo)", e.loc["b", "T_central"],
                 None, None, "viviendas", "2026-2030", "España", "MIVAU", "C4", "2025"))
    return out


def _b3() -> list[dict]:
    out = []
    d = _j(O5 / "B3/resultado.json")
    fu, per = "MIVAU valor tasado; Registradores; EPA; Padrón; CRE", "2015-2025"
    for hip in ("H-B3-1", "H-B3-2", "H-B3-6"):
        lo, hi = d["ic95"][hip]
        out.append(h(f"E-B3-{hip}-ic", f"{hip}: coeficiente por DT del regresor con IC95 (HC3/Conley, mayor EE)",
                     d["estimacion"][hip]["b_por_DT_logpuntos"] * 100, lo * 100, hi * 100, "puntos log. por DT", per,
                     "50 provincias", fu, "C4", "2025"))
        p = d["p_ajustado"][hip]
        out.append(h(f"E-B3-{hip}-p3", f"{hip}: p Holm sobre las 3 confirmatorias", p["holm_3_confirmatorias"] * 100, None, None,
                     "% (valor p)", per, "50 provincias", fu, "C4", "2025"))
        out.append(h(f"E-B3-{hip}-pri", f"{hip}: p por aleatorización Freedman-Lane", p["p_aleatorizacion"] * 100, None, None,
                     "% (valor p)", per, "50 provincias", fu, "C4", "2025"))
    out.append(h("E-B3-H-B3-6-p8", "H-B3-6: p Holm sobre 8 familias", d["p_ajustado"]["H-B3-6"]["holm_8_familias"] * 100, None,
                 None, "% (valor p)", per, "50 provincias", fu, "C4", "2025"))
    s = d["diagnosticos"]["shapley"]
    out.append(h("E-B3-R2reg", "R² del modelo de 8 familias con precio de Registradores", s["R2_registradores"], None, None,
                 "proporción", per, "50 provincias", fu, "C4", "2025"))
    out.append(h("E-B3-kendall", "Tau de Kendall de los Shapley entre fuentes de precio", s["kendall"], None, None,
                 "coeficiente", per, "50 provincias", fu, "C4", "2025"))
    fm = d["fuera_muestra"]
    out.append(h("E-B3-rmse", "RMSE dejando una fuera, modelo de 8 familias (máx = modelo de solo media)", fm["rmse"], None,
                 fm["rmse_media"], "log-puntos", per, "50 provincias", fu, "C4", "2025"))
    out.append(h("E-B3-N", "Provincias en la muestra principal de B3", d["N"]["principal_Y1_P1"], None, None, "provincias",
                 per, "España sin Ceuta y Melilla", fu, "C4", "2025"))
    pe = pd.read_csv(O5 / "B3/tablas/potencia_emd.csv")
    ref = pe[(pe.K == 12) & (pe.R2 == 0.5) & (pe.VIF == 2.0) & (pe.m_Holm == 8)].EMD_DT.iloc[0]
    g8 = pe[(pe.K == 12) & (pe.m_Holm == 8)].EMD_DT
    out.append(h("E-B3-EMD", "Efecto mínimo detectable con Holm m=8 (R² 0,5, VIF 2; rango de la rejilla)", ref, g8.min(), g8.max(),
                 "DT", "pre-registro 2026-10-10", "50 provincias", "B3 potencia (analítica y simulación)", "C4", "2026"))
    return out


def _replicacion() -> list[dict]:
    out = []
    m0 = _j(O4 / "M0/resultado.json")["diagnosticos"]["gl"]
    gl = _j(O3 / "GL/resultado.json")
    lo, hi = gl["ic95"]
    fu = "SERPAVI; INE VUT; Ayuntamiento de Barcelona"
    out.append(h("E-GL-coef", "Réplica García-López: coeficiente propio (FE sección y año, sin IV), Barcelona",
                 gl["estimacion"] * 1000, lo * 1000, hi * 1000, "milésimas de log-punto por punto de VUT/parque", "2021-2024", "Barcelona (secciones)", fu, "C4", "2024"))
    out.append(h("E-GL-pholm", "Réplica García-López: p ajustado Holm", gl["p_ajustado"] * 100, None, None, "% (valor p)",
                 "2021-2024", "Barcelona", fu, "C4", "2024"))
    out.append(h("E-GL-esperado", "Coeficiente esperado en un stock si el efecto de GL sobre el flujo se atenuase", m0["coef_esperado_stock"] * 1000,
                 None, None, "milésimas de log-punto por punto de VUT/parque", "2012-2024", "Barcelona", "Incasòl; SERPAVI", "C4", "2024"))
    out.append(h("E-GL-lambda", "Parte de la variación del flujo (Incasòl) que recoge el stock (SERPAVI)", m0["lambda_2022_2024"] * 100,
                 m0["lambda_2022_2024"] * 100, m0["lambda_2015_2020"] * 100, "%", "2022-2024 (máx: 2015-2020)", "Barcelona",
                 "Incasòl; SERPAVI", "C4", "2024"))
    c3 = _j(O3 / "C3/resultado.json")["estimacion"]
    for hip, ind in (("H3-3a", "renta"), ("H3-3b", "contratos")):
        cs = c3[hip]["CS"]
        out.append(h(f"E-v3-{hip}-CS", f"Topes v3 ({ind}), DiD Callaway-Sant'Anna en entrenamiento; reportado como C4",
                     cs["pct"], cs["pct_ic95"][0], cs["pct_ic95"][1], "%", "2018-2022", "Municipios sujetos de Cataluña",
                     "SERPAVI; Incasòl", "C4", "2022"))
        se = c3[hip]["sellado"]
        out.append(h(f"E-v3-{hip}-sell", f"Topes v3 ({ind}), DiD anual en la muestra sellada; validación contaminada, C4",
                     se["pct"], se["pct_ic95"][0], se["pct_ic95"][1], "%", "2018-2022", "Municipios sujetos de Cataluña",
                     "SERPAVI; Incasòl", "C4", "2022"))
    c1 = _j(O3 / "C1/resultado.json")
    out.append(h("E-v3-H3-1", "VUT por 100 viviendas y alquiler SERPAVI (FE sección, nacional), coeficiente v3",
                 c1["estimacion"] * 1000, c1["ic95"][0] * 1000, c1["ic95"][1] * 1000, "milésimas de log-punto por VUT/100 viv.", "2021-2024", "Secciones censales",
                 "INE VUT; SERPAVI", "C4", "2024"))
    out.append(h("E-v3-H3-1-p", "p Holm de H3-1 (v3)", c1["p_ajustado"]["H3-1"] * 100, None, None, "% (valor p)", "2021-2024",
                 "Secciones censales", "INE VUT; SERPAVI", "C4", "2024"))
    pb = _j(O3 / "PB/resultado.json")["estimacion"]
    out.append(h("E-v3-vut-precio-cota", "Cota de precio atribuible a VUT con la elasticidad mínima de la rejilla (v3)",
                 pb["B1_precio_eps_min_pct"], None, None, "%", "2020M08-2024M08", "España", "INE VUT; supuestos de Manski",
                 "C4", "2024"))
    return out


def filas() -> list[dict]:
    return _b1() + _b2() + _b3() + _replicacion()
