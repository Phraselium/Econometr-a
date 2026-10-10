"""E (v5), redactor E-1 (informe técnico E1 y working paper E2): cifras adicionales LEÍDAS de las salidas
de los módulos (nada tecleado ni reestimado). Ids «E-E1-...». Lo carga src/v5/e_hechos.py.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
from e_hechos import h  # noqa: E402

RAIZ = Path(__file__).resolve().parents[2]
O5 = RAIZ / "output" / "v5"
O4 = RAIZ / "output" / "v4"
FECHA = "2026-10-10"


def _csv(p: str) -> pd.DataFrame:
    return pd.read_csv(O5 / p)


def filas() -> list[dict]:
    f: list[dict] = []
    # --- B2: recuentos de provincias y escenarios -----------------------------------------------
    b2 = _csv("B2/tablas/B2_deficit_2030_provincial.csv")
    n_prov = len(b2)
    f.append(h("E-E1-nprov", "Provincias (y ciudades autónomas) de la contabilidad provincial B1/B2", n_prov, None, None,
               "provincias", "2026-2035", "España", "B2", "C4", FECHA))
    for s in ("empeora", "mejora", "indeterminado"):
        f.append(h(f"E-E1-B2-{s}", f"Provincias cuyo déficit {s} 2025-2030 en todo el rango", int((b2.signo == s).sum()),
                   None, None, "provincias", "2025 a 2030", "52 provincias", "B2 (rango completo)", "C4", FECHA))
    f.append(h("E-E1-B2-estable3", "Provincias con el mismo signo central en los 3 escenarios de terminadas",
               int(b2.signo_estable_3esc.sum()), None, None, "provincias", "2025 a 2030", "52 provincias", "B2", "C4", FECHA))
    esc = _csv("B2/tablas/B2_escenarios_nacional.csv").set_index("escenario")
    for e in ("a", "b", "c"):
        f.append(h(f"E-E1-B2-D2030-{e}", f"Déficit nacional a fin de 2030, escenario ({e}) de terminadas (central)",
                   float(esc.loc[e, "D2030_central"]), None, None, "viviendas", "1-ene-2026 a 31-dic-2030", "España",
                   "B2", "C4", FECHA))
        f.append(h(f"E-E1-B2-empeora-{e}", f"Provincias que empeoran, escenario ({e}) central",
                   int(esc.loc[e, "n_prov_empeora"]), None, None, "provincias", "2025 a 2030", "52 provincias", "B2",
                   "C4", FECHA))
    # --- B3: tamaño, multiverso y sensibilidad ------------------------------------------------------
    b3 = json.loads((O5 / "B3/resultado.json").read_text())
    f.append(h("E-E1-B3-N", "Provincias del corte transversal principal de B3 (sin Ceuta ni Melilla)",
               b3["N"]["principal_Y1_P1"], None, None, "provincias", "2015-2025", "España", "B3", "C4", FECHA))
    mv = {m["hipotesis"]: m for m in b3["diagnosticos"]["multiverso"]}
    f.append(h("E-E1-B3-nesp", "Especificaciones del multiverso por hipótesis confirmatoria (B3)",
               mv["H-B3-1"]["n_especificaciones"], None, None, "especificaciones", "2015-2025 / 2021-2025", "50 provincias",
               "B3", "C4", FECHA))
    for k in ("H-B3-1", "H-B3-2", "H-B3-6"):
        f.append(h(f"E-E1-B3-mvp-{k}", f"Multiverso {k}: % de especificaciones con p<0,05",
                   mv[k]["pct_p_menor_005"], None, None, "%", "2015-2025 / 2021-2025", "50 provincias", "B3", "C4", FECHA))
    for k, s in b3["diagnosticos"]["sensibilidad"].items():
        f.append(h(f"E-E1-B3-oster-{k}", f"Oster δ (Rmax acotado a 1) de {k}", s["delta_oster"], None, None, "razón δ",
                   "2015-2025", "50 provincias", "B3", "C4", FECHA))
        f.append(h(f"E-E1-B3-RV-{k}", f"Cinelli-Hazlett RV (q=1) de {k}", s["RV"], s["RV_alpha"], s["RV_gl_n"],
                   "R² parcial", "2015-2025", "50 provincias", "B3", "C4", FECHA))
    # --- D1: incidencia por clase, método B ---------------------------------------------------------
    inc = _csv("D1/incidencia_ayudas_por_clase.csv")
    for r in inc[inc.metodo == "B"].itertuples():
        f.append(h(f"E-E1-D1-incB-{r.clase}", f"Parte de una ayuda general que se traslada al precio, clase A4 {r.clase} (método B, rejilla P-D)",
                   100 * r.parte_precio_central, 100 * r.parte_precio_min, 100 * r.parte_precio_max, "%",
                   "rejilla εd 0,3-1,5", "clase A4", "D1", "C4", FECHA))
    # --- D2: vacías movilizables y P-D por clase ----------------------------------------------------
    d2 = _csv("D2/resumen_por_clase.csv")
    for r in d2[d2.clase.isin([1, 2])].itertuples():
        f.append(h(f"E-E1-D2-vac-{r.clase}", f"Vacías movilizables por año, clase A4 {r.clase} (central y rango)",
                   r.vac_central, r.vac_min, r.vac_max, "viviendas/año", "2026-2035", "clase A4", "D2 (B1)", "C4", FECHA))
        f.append(h(f"E-E1-D2-covvac-{r.clase}", f"Cobertura de la necesidad por vacías movilizables, clase A4 {r.clase} (central)",
                   r.cob_vac_pct, None, None, "%", "2026-2035", "clase A4", "D2", "C4", FECHA))
        f.append(h(f"E-E1-D2-cobpd-{r.clase}", f"Cobertura de la necesidad por la construcción adicional de P-D, clase A4 {r.clase}",
                   (r.cob_pd_min_pct + r.cob_pd_max_pct) / 2, r.cob_pd_min_pct, r.cob_pd_max_pct, "%", "2026-2035",
                   "clase A4", "D2 (P-D v3, reparto por cuota)", "C4", FECHA))
        f.append(h(f"E-E1-D2-nprov-{r.clase}", f"Provincias de clase A4 {r.clase} (2021-2025)", r.n, None, None,
                   "provincias", "2021-2025", "52 provincias", "D2 (A4)", "C4", FECHA))
        f.append(h(f"E-E1-D2-nrob-{r.clase}", f"Provincias de clase A4 {r.clase} con clase robusta (2021-2025)", r.robustas,
                   None, None, "provincias", "2021-2025", "52 provincias", "D2 (A4)", "C4", FECHA))
    # --- Verificador -------------------------------------------------------------------------------
    ver = _csv("verificador/resumen.csv")
    f.append(h("E-E1-ver-n", "Afirmaciones del debate evaluadas en el verificador v5", len(ver), None, None, "afirmaciones",
               "2026-10", "España", "verificador v5", "C4", FECHA))
    for v, n in ver.veredicto.value_counts().items():
        slug = {"ANALIZADA, NO CONCLUYENTE": "anc", "NO ANALIZADA: FALTAN DATOS": "nafd", "PARCIALMENTE": "parc",
                "CONTRADICHA": "contr", "RESPALDADA": "resp", "NO RESPALDADA": "nresp"}.get(v, v[:4].lower())
        f.append(h(f"E-E1-ver-{slug}", f"Afirmaciones con veredicto «{v}»", int(n), None, None, "afirmaciones", "2026-10",
                   "España", "verificador v5", "C4", FECHA))
    # --- València: SERPAVI por distritos (R1T) -----------------------------------------------------
    sd = _csv("R1T/serpavi_distritos_valencia_nombres.csv")
    f.append(h("E-E1-VLC-ndist", "Distritos de València ciudad con SERPAVI y nombre", len(sd), None, None, "distritos",
               "2015-2024", "València ciudad", "SERPAVI (MIVAU); Ajuntament de València (nombres)", "C4", FECHA))
    f.append(h("E-E1-VLC-contratos", "Contratos SERPAVI con renta declarada en los distritos de València, 2024",
               float(sd.n_contratos_2024.sum()), float(sd.n_contratos_2024.min()), float(sd.n_contratos_2024.max()),
               "contratos (min-max por distrito)", "2024", "València ciudad", "SERPAVI (MIVAU)", "C4", FECHA))
    s24 = sd.sort_values("mediana_VC_2024")
    for et, r in (("max", s24.iloc[-1]), ("min", s24.iloc[0])):
        f.append(h(f"E-E1-VLC-serpavi-{et}", f"Renta mediana SERPAVI 2024, distrito {r.distrito.title()}",
                   r.mediana_VC_2024, None, None, "€/m²/mes", "2024", f"distrito {r.distrito.title()}", "SERPAVI (MIVAU)",
                   "C4", FECHA))
    f.append(h("E-E1-VLC-serpavi-med", "Mediana entre distritos de la renta mediana SERPAVI 2024",
               float(sd.mediana_VC_2024.median()), float(sd.mediana_VC_2024.min()), float(sd.mediana_VC_2024.max()),
               "€/m²/mes", "2024", "19 distritos de València", "SERPAVI (MIVAU)", "C4", FECHA))
    c = sd.sort_values("crec_2015_2024_%")
    for et, r in (("max", c.iloc[-1]), ("min", c.iloc[0])):
        f.append(h(f"E-E1-VLC-crec-{et}", f"Crecimiento de la renta mediana SERPAVI 2015-2024, distrito {r.distrito.title()}",
                   r["crec_2015_2024_%"], None, None, "%", "2015-2024", f"distrito {r.distrito.title()}", "SERPAVI (MIVAU)",
                   "C4", FECHA))
    f.append(h("E-E1-VLC-crec-med", "Crecimiento de la renta mediana SERPAVI 2015-2024, mediana entre distritos",
               float(sd["crec_2015_2024_%"].median()), float(sd["crec_2015_2024_%"].min()),
               float(sd["crec_2015_2024_%"].max()), "%", "2015-2024", "19 distritos de València", "SERPAVI (MIVAU)", "C4", FECHA))
    # --- València: fianzas GVA (A23) ---------------------------------------------------------------
    g = _csv("A23/tablas/gva_fianzas_resumen.csv").set_index("anio")
    for a in (2020, 2025):
        f.append(h(f"E-E1-VLC-fianza-{a}", f"Mediana de la fianza depositada en la GVA, {a}", g.loc[a, "mediana_eur"], None,
                   None, "€", str(a), "Comunitat Valenciana", "GVA (registro de fianzas)", "C4", FECHA))
    f.append(h("E-E1-VLC-fianza-n2025", "Fianzas depositadas en la GVA, 2025", g.loc[2025, "n_fianzas"], None, None,
               "contratos", "2025", "Comunitat Valenciana", "GVA (registro de fianzas)", "C4", FECHA))
    # --- València: provincia y ciudad en A4/B1/B2 (v5) y clase v4 ---------------------------------
    ap = _csv("A4/clasificacion_provincias.csv").set_index("cod_prov").loc[46]
    f.append(h("E-E1-VLC-def2125", "Déficit contable 2021-2025, provincia de València (mediana y rango)",
               ap.deficit_2021_2025_mediana, ap.deficit_2021_2025_min, ap.deficit_2021_2025_max, "viviendas", "2021-2025",
               "provincia de València", "A4 (INE, Ministerio, Catastro)", "C4", FECHA))
    f.append(h("E-E1-VLC-claseprov", "Clase A4 de la provincia de València (2021-2025)", ap.clase_2021_2025, None, None,
               "clase", "2021-2025", "provincia de València", "A4", "C4", FECHA))
    am = _csv("A4/clasificacion_municipios.csv").set_index("cod_mun").loc[46250]
    f.append(h("E-E1-VLC-defciu", "Déficit contable 2021-2025, València ciudad (fuente única)", am.deficit_2021_2025, None,
               None, "viviendas", "2021-2025", "València ciudad", "A4 (padrón y Catastro)", "C4", FECHA))
    f.append(h("E-E1-VLC-precio", "Valor tasado de la vivienda libre, València ciudad", am.precio_eur_m2, None, None, "€/m²",
               "2025", "València ciudad", "MIVAU (valor tasado)", "C4", FECHA))
    f.append(h("E-E1-VLC-claseciu-v5", "Clase A4 v5 de València ciudad (rango oficial de coste)", am.clase_2021_2025, None,
               None, "clase", "2021-2025", "València ciudad", "A4", "C4", FECHA))
    f.append(h("E-E1-VLC-claseciu-v4", "Clase M3 v4 de València ciudad (coste supuesto)", am.clase_v4_modal, None, None,
               "clase", "2021-2025", "València ciudad", "v4 M3", "C4", FECHA))
    b1 = _csv("B1/tablas/B1_tabla_provincial.csv").set_index("cod_prov").loc[46]
    f.append(h("E-E1-VLC-B1", "Necesidad anual de vivienda, provincia de València", b1.N_anual_central, b1.N_anual_min,
               b1.N_anual_max, "viviendas/año", "2026-2035", "provincia de València", "B1", "C4", FECHA))
    b2v = b2.set_index("cod_prov").loc[46]
    f.append(h("E-E1-VLC-B2", "Déficit acumulado a fin de 2030, provincia de València", b2v.D2030_central, b2v.D2030_min,
               b2v.D2030_max, "viviendas", "1-ene-2026 a 31-dic-2030", "provincia de València", "B2", "C4", FECHA))
    m3 = pd.read_csv(O4 / "M3/clasificacion_municipios.csv").set_index("cod_mun").loc[46250]
    f.append(h("E-E1-VLC-estab-v4", "Estabilidad de la clase M3 v4 de València ciudad en el multiverso", m3.estabilidad_pct,
               None, None, "%", "2021-2025", "València ciudad", "v4 M3", "C4", FECHA))
    return f
