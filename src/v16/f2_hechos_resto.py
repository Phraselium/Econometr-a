"""V16-F2.1 · Hechos 3 a 7: parque y vacías (Censo 2021), obra nueva frente a hogares (ampliación a 2025), vivienda pública (pendiente),
lanzamientos (CGPJ) y comparación internacional (OCDE, Eurostat). Las lecturas de la base filtran muestra_sellada_v6 (NOT coalesce(...)).

Parque: la tabla INE 59531 (vacías y uso esporádico por consumo eléctrico) ES una tabla del Censo 2021: comparte universo (26.623.708
viviendas) y publicación con la 59525. El Censo solo publica «vacías» a través de ella; por tanto «vacías del Censo» y «vacías por consumo»
son la misma cifra y NO son dos fuentes. Se comprueba la identidad de totales en el código. No se ha verificado en la metodología oficial del
INE (sin consulta en línea en esta sesión) qué parte de la clasificación usa el consumo; la conclusión de C4 no depende de ello.
Sin datos municipales: los de las ocho CCAA de la muestra sellada v6 solo se usan vía src/holdout.py (K8). Nivel nacional y CCAA.
"""
from __future__ import annotations

import duckdb
import numpy as np
import pandas as pd

from f2_hechos_base import RAIZ, SAL, TOL_PP, TOL_REL_RECUENTO, anotar, pct

RAW = RAIZ / "data" / "raw"
BASE = RAIZ / "data" / "base" / "hechos.parquet"
DI = RAIZ / "data" / "processed" / "v16" / "demanda_internacional.parquet"
CGPJ = RAW / "v16" / "tension_social" / "_terceros" / "cgpj_series_tsj_2T2026.xlsx"


def _n(s: pd.Series) -> pd.Series:
    return s.astype(str).str.replace(".", "", regex=False).astype(float)


def parque() -> list[str]:
    avisos = []
    c = RAW / "v11" / "ine_censo2021"
    t = pd.read_csv(c / "censo2021_tpx59531.csv", sep=";", encoding="utf-8-sig")
    nac = t[t["Total Nacional"] == "Total Nacional"].copy()
    nac = nac[nac["Comunidades y Ciudades Autónomas"].isna()].set_index("Consumo eléctrico").Total
    nac = _n(nac)
    p = pd.read_csv(c / "censo2021_tpx59525.csv", sep=";", encoding="utf-8-sig")
    tipo = p.columns[2]
    fil = p[(p.iloc[:, 1].isna()) & (p["Total Nacional"] == "Total Nacional")].set_index(tipo).Total
    fil = _n(fil)
    tot, prin, nopr = fil["Total"], fil["Vivienda principal"], fil["Vivienda no principal"]
    if abs(tot - nac["Viviendas totales"]) > 0:
        avisos.append("59531 y 59525 no comparten total de viviendas")
    vac, esp = nac["Viviendas vacías"], nac["Viviendas de uso esporádico"]
    mot_c = "Una sola fuente (Censo 2021, INE): estadística oficial de fuente única."
    base = "f2_hechos_resto.py:parque; INE Censo 2021 tabla 59525 (tipo de vivienda, total nacional)"
    anotar("V16-HEC-PARQUE-TOTAL-2021", "Viviendas familiares, Censo 2021", tot, None, None, "viviendas", "1-11-2021", "España",
           ["Censo 2021"], "C4", "2021", base, motivo_capa=mot_c)
    anotar("V16-HEC-PARQUE-PRINCIPALES-2021", "Viviendas principales, Censo 2021", prin, None, None, "viviendas", "1-11-2021", "España",
           ["Censo 2021"], "C4", "2021", base, motivo_capa=mot_c)
    anotar("V16-HEC-PARQUE-NOPRINCIPALES-2021", "Viviendas no principales (secundarias y vacías), Censo 2021", nopr, None, None, "viviendas",
           "1-11-2021", "España", ["Censo 2021"], "C4", "2021", base, motivo_capa=mot_c)
    mot_v = ("Las «vacías del Censo» solo se publican en la tabla 59531 (consumo eléctrico), que es una tabla del propio Censo 2021 con el mismo "
             "universo (26.623.708 viviendas, comprobado). Las vacías del Censo y las vacías por consumo eléctrico son la misma cifra: no son "
             "independientes. Fuente única: C4. Las vacías por consumo y el uso esporádico son subconjuntos de las no principales "
             f"({(vac + esp) / nopr:.0%} de ellas).")
    anotar("V16-HEC-VACIAS-CONSUMO-2021", "Viviendas vacías por consumo eléctrico (Censo 2021, tabla 59531)", vac, None, None, "viviendas",
           "2021", "España", ["Censo 2021 consumo eléctrico", "Censo 2021"], "C4", "2021",
           "f2_hechos_resto.py:parque; tabla 59531, fila «Viviendas vacías», total nacional. Definición INE: sin contrato o consumo inferior al "
           "de una vivienda media ocupada 15 días al año (docs/v16/fuentes/renta_parque.md, ficha 3).", motivo_capa=mot_v)
    anotar("V16-HEC-VACIAS-PCT-2021", "Vacías por consumo eléctrico sobre viviendas familiares, Censo 2021", pct(vac / tot), None, None, "%", "2021",
           "España", ["Censo 2021 consumo eléctrico", "Censo 2021"], "C4", "2021", "vacías / total de viviendas, ambas del Censo 2021.",
           motivo_capa=mot_v)
    anotar("V16-HEC-ESPORADICO-2021", "Viviendas de uso esporádico por consumo eléctrico, Censo 2021", esp, None, None, "viviendas", "2021",
           "España", ["Censo 2021 consumo eléctrico", "Censo 2021"], "C4", "2021", "tabla 59531, fila «Viviendas de uso esporádico».",
           motivo_capa=mot_v)
    # CCAA
    d = t[t["Comunidades y Ciudades Autónomas"].notna() & t["Provincias"].isna()].copy()
    d["Total"] = _n(d["Total"])
    w = d.pivot_table(index="Comunidades y Ciudades Autónomas", columns="Consumo eléctrico", values="Total")[
        ["Viviendas totales", "Viviendas vacías", "Viviendas de uso esporádico"]]
    t20 = pd.read_csv(c / "censo2021_tpx59520.csv", sep=";", encoding="utf-8-sig")
    t20 = t20[t20.iloc[:, 2] == "Total (tamaño de municipio)"]
    t20 = t20[t20.iloc[:, 1].isin(w.index)].copy()
    t20["Total"] = _n(t20["Total"])
    pr = t20.pivot_table(index=t20.columns[1], columns=t20.columns[0], values="Total")
    out = w.join(pr[["Vivienda principal", "Vivienda no principal"]])
    out["pct_vacias"] = (100 * out["Viviendas vacías"] / out["Viviendas totales"]).round(2)
    out["pct_no_principales"] = (100 * out["Vivienda no principal"] / out["Viviendas totales"]).round(2)
    out.reset_index().rename(columns={"Comunidades y Ciudades Autónomas": "ccaa"}).to_csv(SAL / "parque_ccaa.csv", index=False)
    # Catastro frente a Censo (territorio común: sin País Vasco ni Navarra)
    cat = pd.read_csv(RAW / "catastro_urbana_municipios.csv")
    cat = cat[cat.serie.str.startswith("catastro_uu_res") & (cat.periodo == 2022)]
    cat_c = cat[~cat.provincia_codigo.isin([1, 20, 48, 31])].valor.sum()
    cen_c = tot - out.loc["16 País Vasco", "Viviendas totales"] - out.loc["15 Navarra, Comunidad Foral de", "Viviendas totales"]
    rel = cat_c / cen_c - 1
    within = abs(rel) <= TOL_REL_RECUENTO
    anotar("V16-HEC-PARQUE-CATASTRO-CENSO-2021", "Unidades urbanas residenciales del Catastro (1-1-2022) frente a viviendas del Censo 2021, territorio común",
           pct(rel), None, None, "% de diferencia", "2021-2022", "Territorio común (sin País Vasco ni Navarra)", ["Catastro", "Censo 2021"], "C4", "2022",
           f"f2_hechos_resto.py:parque; Catastro {cat_c:,.0f} frente a Censo {cen_c:,.0f}.",
           tolerancia=f"±{TOL_REL_RECUENTO:.0%} en recuentos (capas.md)",
           motivo_capa=(f"Las dos cifras {'coinciden' if within else 'no coinciden'} dentro de la tolerancia, pero NO se declara C1: la independencia no está "
                        "demostrada en el repositorio (el directorio de viviendas del Censo puede apoyarse en el Catastro; no verificado en la "
                        "metodología oficial) y la misma vara bajó a C4 las parejas que comparten origen (V9-D7-c1-dif, V10-ATL-A1). C4."))
    return avisos


def obra_hogares() -> list[str]:
    avisos = []
    q = lambda s: duckdb.sql(s).df()  # noqa: E731
    base = "NOT coalesce(muestra_sellada_v6, false)"
    ter = q(f"SELECT periodo, valor FROM read_parquet('{BASE}') WHERE variable='terminadas' AND nivel='nacional' AND {base}")
    ter["y"] = ter.periodo.str[:4].astype(int)
    g = ter.groupby("y").valor.agg(["sum", "count"])
    anual = g[g["count"] == 4]["sum"]
    ecp = q(f"SELECT periodo, valor FROM read_parquet('{BASE}') WHERE variable='hogares_ecp' AND nivel='nacional' AND {base}").set_index("periodo").valor
    dh = 1000 * (ecp["2025T1"] - ecp["2021T1"])
    ck = pd.read_csv(RAIZ / "output/v5/cifras_clave.csv", dtype=str).set_index("id")
    if abs(dh - float(ck.at["dh_2125", "min"])) > 1:
        avisos.append(f"ECP 2021T1-2025T1 = {dh:,.0f} frente al mínimo publicado de dh_2125 {ck.at['dh_2125', 'min']}")
    suma = float(anual.loc[2021:2025].sum())
    anotar("V16-HEC-OBRA-TERMINADAS-2125", "Viviendas libres terminadas (MIVAU, certificados de fin de obra; sin protegidas), acumulado 2021-2025", suma, None, None, "viviendas",
           "2021-2025", "España", ["MIVAU fin de obra"], "C4", "2026T2",
           "f2_hechos_resto.py:obra_hogares; suma de trimestres de la variable terminadas (nacional) de la base, años completos.",
           motivo_capa="Una sola fuente (MIVAU, fin de obra): la misma razón que E-T7-prod en bajadas_capa.csv. Amplía a 2025 la cifra de la 1.0 (terminadas_1924, "
           "otro periodo y otro id).")
    anotar("V16-HEC-OBRA-TERMINADAS-2025", "Viviendas libres terminadas (MIVAU) en 2025", float(anual.loc[2025]), None, None, "viviendas", "2025", "España",
           ["MIVAU fin de obra"], "C4", "2026T2", "suma de los cuatro trimestres de 2025.", motivo_capa="Fuente única (MIVAU).")
    anotar("V16-HEC-HOGARES-ECP-2125", "Aumento del número de hogares (ECP, 1-1-2021 a 1-1-2025)", dh, None, None, "hogares", "2021-2025", "España",
           ["INE ECP"], "C4", "2025T1",
           f"ECP 2025T1 - 2021T1 de la base. Reproduce el extremo inferior publicado de dh_2125 ({ck.at['dh_2125', 'min']}); la cifra publicada "
           "dh_2125 (C1, con EPA) no se recalcula ni se sustituye.", motivo_capa="Aquí solo ECP (un extremo): C4; la cifra C1 con ECP y EPA sigue siendo dh_2125.")
    anotar("V16-HEC-OBRA-SOBRE-HOGARES-2125", "Libres terminadas 2021-2025 por hogar nuevo (ECP 2021-2025)", suma / dh, None, None, "viviendas por hogar",
           "2021-2025", "España", ["MIVAU fin de obra", "INE ECP"], "C4", "2026T2",
           "terminadas 2021-2025 / aumento de hogares ECP. Cociente de dos fuentes distintas con ventanas distintas (año natural frente a 1 de enero): "
           "descriptivo, sin lectura causal ni déficit (el déficit con bajas es L3-DEF-2125).", motivo_capa="Cociente de dos cifras de capa C4: la capa es la menor de las componentes.")
    return avisos


def lanzamientos() -> list[str]:
    hojas = {"total": "Lanzamientos practic. total TSJ", "hipotecaria": "Lanzamientos E.hipotecaria TSJ", "lau": "Lanzamientos L.A.U  TSJ",
             "otros": "Lanzamientos. Otros TSJ"}
    tab = {}
    for k, h in hojas.items():
        x = pd.read_excel(CGPJ, sheet_name=h, header=None)
        hr = next(i for i in range(10) if any(isinstance(a, str) and "".join(a.split()) == "Total2025" for a in x.iloc[i, 1:]))
        fin = next(i for i in range(hr + 1, len(x)) if x.iloc[i, 1] == "TOTAL")
        d = x.iloc[hr + 1:fin + 1, 1:].copy()
        d.columns = ["tsj"] + ["".join(str(c).split()) for c in x.iloc[hr, 2:]]
        d = d[d.tsj.notna()].set_index("tsj")
        tab[k] = d.apply(pd.to_numeric, errors="coerce")
    tot = tab["total"]
    anual = tot.loc["TOTAL", [c for c in tot.columns if str(c).startswith("Total")]]
    anual.index = [int(str(c)[-4:]) for c in anual.index]
    ult4 = float(tot.loc["TOTAL", ["25-T3", "25-T4", "26-T1", "26-T2"]].sum())
    fu = "CGPJ"
    mot = ("Una sola fuente (CGPJ, estadística de los órganos judiciales): C4. Redistribuible «no»; se publica como agregado propio "
           "(terceros_1_0: agregados). Es el total de los 17 TSJ (nacional); los partidos judiciales de 2025 están excluidos (K6).")
    ficha = "f2_hechos_resto.py:lanzamientos; hoja «Lanzamientos practic. total TSJ» de cgpj_series_tsj_2T2026.xlsx, fila TOTAL; columnas «Total AAAA»."
    anotar("V16-HEC-LANZ-2013", "Lanzamientos practicados en 2013, España (total)", anual.loc[2013], None, None, "lanzamientos", "2013", "España", [fu], "C4", "2013", ficha, motivo_capa=mot)
    pico = int(anual.idxmax())
    anotar("V16-HEC-LANZ-PICO", f"Año con más lanzamientos practicados 2013-2025 ({pico}), España", anual.loc[pico], None, None, "lanzamientos", f"{pico}", "España", [fu], "C4", f"{pico}", ficha, motivo_capa=mot)
    anotar("V16-HEC-LANZ-2025", "Lanzamientos practicados en 2025, España (total)", anual.loc[2025], None, None, "lanzamientos", "2025", "España", [fu], "C4", "2025", ficha, motivo_capa=mot)
    anotar("V16-HEC-LANZ-UM4T", "Lanzamientos practicados en los últimos cuatro trimestres (2025T3-2026T2), España", ult4, None, None, "lanzamientos", "2025T3-2026T2", "España", [fu], "C4", "2026T2", ficha, motivo_capa=mot)
    for k in ("hipotecaria", "lau", "otros"):
        s = float(tab[k].loc["TOTAL", "Total2025"])
        anotar(f"V16-HEC-LANZ-TIPO-{k.upper()}-2025", f"Cuota de los lanzamientos por tipo «{k}» en 2025, España", pct(s / anual.loc[2025]), None, None, "%", "2025", "España", [fu], "C4", "2025",
               ficha + f" Tipo: hoja «{hojas[k]}». Los tres tipos suman {sum(float(tab[c].loc['TOTAL', 'Total2025']) for c in ('hipotecaria', 'lau', 'otros')):,.0f} frente al total {anual.loc[2025]:,.0f}.", motivo_capa=mot)
    ccaa = pd.DataFrame({f"{k}_2025": tab[k]["Total2025"] for k in hojas}).join(
        pd.DataFrame({"total_2013": tot["Total2013"], "total_ultimos_4T": tot[["25-T3", "25-T4", "26-T1", "26-T2"]].sum(axis=1)}))
    ccaa.reset_index().rename(columns={"index": "tsj"}).to_csv(SAL / "lanzamientos_ccaa.csv", index=False)
    return []


def internacional() -> list[str]:
    EU = ["AT", "BE", "CZ", "DE", "DK", "EE", "ES", "FI", "FR", "GR", "HU", "IE", "IT", "LT", "LU", "LV", "NL", "PL", "PT", "SE", "SI", "SK"]
    d = duckdb.sql(f"SELECT variable, territorio_codigo AS pais, periodo, valor FROM read_parquet('{DI}') WHERE NOT coalesce(muestra_sellada_v6, false) "
                   "AND variable IN ('oecd_rhp','oecd_hpi_rpi','oecd_hpi_ydh') AND nivel='pais'").df()
    d["y"] = d.periodo.str[:4].astype(int)
    avisos = []
    ficha = ("f2_hechos_resto.py:internacional; OCDE (Analytical house price indicators): media anual de cuatro trimestres (índice 2015=100); "
             "mediana de la variación entre los países con dato completo en las dos fechas. UE = {} países de la lista UE presentes; OCDE = todos los de la serie.")
    mot = ("Comparación internacional: C4. El índice de precios español de la OCDE, el de Eurostat y el de la BIS salen del IPV del INE (correlación "
           "0,9999; K6), y el de ratios usa la renta y el alquiler de las cuentas nacionales; no hay segunda fuente independiente para España.")
    for var, nom, uni in (("oecd_rhp", "precio real de la vivienda", "cambio acumulado"), ("oecd_hpi_rpi", "ratio precio/alquiler", "cambio acumulado del índice"),
                          ("oecd_hpi_ydh", "ratio precio/renta disponible", "cambio acumulado del índice")):
        x = d[d.variable == var]
        a = x.groupby(["pais", "y"]).valor.agg(["mean", "count"]).reset_index()
        a = a[a["count"] == 4].pivot(index="y", columns="pais", values="mean")
        if 2025 not in a.index or "ES" not in a.columns:
            avisos.append(f"{var}: sin 2025 completo para España")
            continue
        for b in (2007, 2019):
            ch = (a.loc[2025] / a.loc[b] - 1).dropna()
            es = float(ch["ES"])
            m_eu = float(ch[[p for p in ch.index if p in EU]].median())
            m_oecd = float(ch.median())
            anotar(f"V16-HEC-INTL-{var.split('_', 1)[1].upper()}-ES-{b}-2025", f"{nom.capitalize()}, {uni} {b}-2025: España", pct(es), None, None, "%", f"{b}-2025", "España",
                   ["OCDE"], "C4", "2025", ficha.format(len([p for p in ch.index if p in EU])), motivo_capa=mot)
            anotar(f"V16-HEC-INTL-{var.split('_', 1)[1].upper()}-MED-{b}-2025", f"{nom.capitalize()}, {uni} {b}-2025: mediana UE (mínimo/máximo: mediana UE y OCDE)",
                   pct(m_eu), pct(min(m_eu, m_oecd)), pct(max(m_eu, m_oecd)), "%", f"{b}-2025", f"UE ({len([p for p in ch.index if p in EU])} países) y OCDE ({len(ch)} países)",
                   ["OCDE"], "C4", "2025", ficha.format(len([p for p in ch.index if p in EU])), motivo_capa=mot)
    s = duckdb.sql(f"SELECT territorio_codigo AS t, periodo, valor FROM read_parquet('{DI}') WHERE NOT coalesce(muestra_sellada_v6, false) "
                   "AND variable='eurostat_sobrecarga_coste_vivienda_pct' AND desagregacion='edad=TOTAL;sexo=T;pobreza=TOTAL' AND t IN ('ES','EU27_2020')").df()
    p = s.pivot(index="periodo", columns="t", values="valor").dropna().sort_index()
    ult = p.index[-1]
    anotar(f"V16-HEC-INTL-SOBRECARGA-ES-{ult}", f"Tasa de sobrecarga del coste de la vivienda, España frente a la UE ({ult}); mínimo y máximo: España y UE", float(p.loc[ult, "ES"]),
           float(min(p.loc[ult])), float(max(p.loc[ult])), "% de la población", ult, "España y UE-27", ["Eurostat ECV"], "C4", ult,
           f"Eurostat ilc_lvho07a, total; España {p.loc[ult, 'ES']:.1f} % y UE-27 {p.loc[ult, 'EU27_2020']:.1f} %. Valor = España.",
           motivo_capa="Eurostat y el INE publican la misma ECV: no hay segunda fuente (V10-ATL-A1 bajó a C4 por esta razón).")
    return avisos


def publica_pendiente() -> None:
    ruta = RAIZ / "data" / "raw" / "v16" / "demanda_internacional"
    hay = any("PH4" in str(f) or "affordable" in str(f).lower() for f in ruta.rglob("*"))
    if hay:
        raise RuntimeError("Hay datos OCDE Affordable Housing: implementar la cifra de vivienda pública por habitante")
