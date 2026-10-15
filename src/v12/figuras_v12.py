"""V12-B8 · figuras de V12 con el estilo de V10. `make figuras` las llama desde src/v10/figuras.py (`FIGURAS`), que
pasa su propio módulo como `F` (helpers `guardar`, `mapa`, `peninsula`, constantes de estilo). Solo salidas versionadas
de output/v12 y geometrías de data/base/geo. Todas descriptivas (C4)."""
from __future__ import annotations

from pathlib import Path

import geopandas as gpd
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

RAIZ = Path(__file__).resolve().parents[2]
O = RAIZ / "output" / "v12"
GEO = RAIZ / "data" / "base" / "geo"


def f15_contabilidad(F):
    p = pd.read_csv(O / "b1/contabilidad_periodos_nacional.csv", dtype={"cod_territorio": str})
    p = p[p.nac == "TOTAL"].set_index("periodo")
    fig, ax = plt.subplots()
    x = np.arange(len(p))
    comp = [("vegetativo", "Saldo vegetativo"), ("saldo_exterior", "Saldo con el extranjero"), ("residuo", "Residuo (revisiones del padrón)")]
    pos, neg = np.zeros(len(p)), np.zeros(len(p))
    for (c, et), col in zip(comp, F.OKABE):
        v = p[c].to_numpy() / 1e3
        base = np.where(v >= 0, pos, neg)
        ax.bar(x, v, bottom=base, label=et, color=col, width=0.6)
        pos, neg = pos + np.clip(v, 0, None), neg + np.clip(v, None, 0)
    ax.plot(x, p.crecimiento / 1e3, "o", color="#000000", label="Crecimiento de la población")
    ax.set_xticks(x, p.index)
    ax.set_ylabel("miles de personas")
    ax.axhline(0, color="#666666", lw=0.8)
    ax.legend(fontsize=7, loc="upper right")
    ax.set_title("España: de dónde viene el crecimiento de la población")
    F.guardar(fig, "F15_contabilidad_demografica", "España: de dónde viene el crecimiento de la población",
              "INE: padrón y censo anual, MNP, EVR (hasta 2020) y EMCR (desde 2021); V12-B1", "2003-2024", "C4",
              "Identidad contable; el residuo recoge revisiones del padrón y bajas no registradas como flujo (grande con la EVR).",
              "Barras apiladas por periodo con los componentes y un punto con el crecimiento total; datos en output/v12/b1.")


def f16_mapa_exterior(F):
    p = pd.read_csv(O / "b1/contabilidad_periodos_provincia.csv", dtype={"cod_territorio": str})
    p = p[(p.nac == "TOTAL") & (p.periodo == "2022-2024")].rename(columns={"cod_territorio": "cod_provincia"})
    g = gpd.read_parquet(GEO / "provincias.parquet").merge(p, on="cod_provincia", how="left")
    F.mapa(F.peninsula(g), "tasa_saldo_exterior_por_mil_anual", "F16_mapa_saldo_exterior", "Saldo migratorio con el extranjero, 2022-2024",
           "INE, EMCR (microdatos); padrón y censo anual; V12-B1", "2022-2024", "C4",
           "Personas por 1.000 habitantes y año. Describe flujos; no atribuye efectos. Canarias recolocada.",
           "Mapa de provincias con el saldo exterior anual por 1.000 habitantes; datos en output/v12/b1.", etiqueta="‰ anual")


def f17_od(F):
    p = pd.read_csv(O / "b2/flujos_area_periodos.csv")
    t = p.groupby(["area", "periodo"]).saldo_capital_con_corona.sum().unstack("area")
    pob = {"valencia": "València", "madrid": "Madrid", "barcelona": "Barcelona", "alicante": "Alicante", "castellon": "Castelló"}
    fig, ax = plt.subplots()
    x = np.arange(len(t))
    w = 0.16
    for i, (a, col) in enumerate(zip(pob, F.OKABE)):
        ax.bar(x + (i - 2) * w, t[a] / 1e3, width=w, label=pob[a], color=col)
    ax.set_xticks(x, t.index)
    ax.set_ylabel("miles de personas (saldo de la capital)")
    ax.axhline(0, color="#666666", lw=0.8)
    ax.legend(fontsize=7)
    ax.set_title("Saldo de cada capital con su corona metropolitana")
    F.guardar(fig, "F17_saldo_capital_corona", "Saldo de cada capital con su corona metropolitana",
              "INE, EVR y EMCR (microdatos origen-destino); V12-B2", "2003-2024", "C4",
              "Negativo: salen más personas de la capital a la corona que al revés. Corona de composición fija (cota inferior).",
              "Barras agrupadas por periodo y capital; datos en output/v12/b2/flujos_area_periodos.csv.")


def f18_jefatura(F):
    j = pd.read_csv(O / "b3/jefatura_nacional.csv")
    j = j[j.grupo_edad != "0-14"]
    fig, ax = plt.subplots()
    for anio, col in zip((2011, 2021), F.OKABE):
        s = j[j.anio == anio]
        ax.plot(s.grupo_edad, 100 * s.jefatura, "-o", ms=3, label=str(anio), color=col)
    ax.set_ylabel("% de personas que encabezan un hogar")
    ax.tick_params(axis="x", rotation=60)
    ax.legend()
    ax.set_title("Tasa de jefatura por edad, Censos 2011 y 2021")
    F.guardar(fig, "F18_jefatura_edad", "Tasa de jefatura por edad, Censos 2011 y 2021", "INE, Censos 2011 y 2021 (microdatos); V12-B3",
              "2011 y 2021", "C4", "Persona de referencia = la de mayor edad del hogar (regla común a los dos censos).",
              "Dos líneas por grupo de edad; datos en output/v12/b3/jefatura_nacional.csv.")


def f19_mapa_presion(F):
    p = pd.read_csv(O / "b4/presion_hogares_obra_municipio.csv", dtype={"cod_municipio": str})
    p = p[p.periodo == "2021-2025"]
    g = gpd.read_parquet(GEO / "municipios.parquet")
    g = g[g.cod_ccaa == "10"].merge(p, on="cod_municipio", how="left")
    orden = ["obra ≥ hogares", "obra 50-100 %", "obra < 50 %", "hogares no crecen"]
    colores = dict(zip(orden, ["#009E73", "#F0E442", "#D55E00", "#56B4E9"]))
    fig, ax = plt.subplots()
    g[g.categoria.isna()].plot(ax=ax, color="#eeeeee", linewidth=0.1, edgecolor="#ffffff")
    for c in orden:
        s = g[g.categoria == c]
        if len(s):
            s.plot(ax=ax, color=colores[c], linewidth=0.1, edgecolor="#ffffff", label=c)
    from matplotlib.patches import Patch
    ax.legend(handles=[Patch(color=colores[c], label=c) for c in orden] + [Patch(color="#eeeeee", label="< 10.000 hab. o sin dato")], fontsize=7, loc="lower right")
    ax.set_axis_off()
    ax.set_title("Comunitat Valenciana: obra nueva frente a hogares nuevos, 2021-2025")
    F.guardar(fig, "F19_mapa_cv_obra_hogares", "Comunitat Valenciana: obra nueva frente a hogares nuevos, 2021-2025",
              "Catastro (URBANA); INE, censo anual y Censo 2021; V12-B4", "2021-2025", "C4",
              "Hogares nuevos estimados con el tamaño de hogar de 2021; obra nueva neta del Catastro. No mide necesidad ni déficit.",
              "Mapa de municipios de 10.000 habitantes o más coloreados por categoría; datos en output/v12/b4.")


def f20_catastro_mivau(F):
    c = pd.read_csv(O / "b4/contraste_catastro_mivau_provincia.csv", dtype={"cpro": str})
    n = c.groupby("anio")[["obra_neta_catastro", "terminadas_mivau_total"]].sum(min_count=1).loc[2012:]
    fig, ax = plt.subplots()
    ax.plot(n.index, n.obra_neta_catastro / 1e3, "-o", ms=3, label="Catastro: unidades residenciales netas", color=F.OKABE[0])
    ax.plot(n.index, n.terminadas_mivau_total / 1e3, "-o", ms=3, label="MIVAU: libres terminadas + protegidas", color=F.OKABE[1])
    ax.axvspan(2012.5, 2017.5, color="#eeeeee", label="regularización catastral")
    ax.set_ylabel("miles de viviendas")
    ax.legend(fontsize=7)
    ax.set_title("Obra nueva según dos fuentes")
    F.guardar(fig, "F20_obra_nueva_dos_fuentes", "Obra nueva según dos fuentes", "Catastro (URBANA); MIVAU; V12-B4", "2012-2025", "C4",
              "Sin País Vasco ni Navarra (catastros forales). En 2013-2017 el Catastro incluye altas por regularización.",
              "Dos líneas anuales; datos en output/v12/b4/contraste_catastro_mivau_provincia.csv.")


def f21_mapa_titularidad(F):
    t = pd.read_csv(O / "b5/titularidad_cuotas.csv", dtype={"cod_territorio": str})
    u = int(t.anio.max())
    t = t[(t.nivel == "provincia") & (t.anio == u)].rename(columns={"cod_territorio": "cod_provincia"})
    g = gpd.read_parquet(GEO / "provincias.parquet").merge(t, on="cod_provincia", how="left")
    F.mapa(F.peninsula(g), "pct_PJ", "F21_mapa_personas_juridicas", f"Viviendas de personas jurídicas privadas, {u}",
           "Catastro, titularidad por tipo de persona (uso residencial); V12-B5", str(u), "C4",
           "Porcentaje de viviendas cuyo sujeto pasivo del IBI es una persona jurídica privada. País Vasco y Navarra sin dato.",
           "Mapa de provincias; datos en output/v12/b5/titularidad_cuotas.csv.", etiqueta="% de las viviendas")


def f22_brecha(F):
    b = pd.read_csv(O / "b6/ecv_brecha_misma_edad_renta.csv")
    nombres = {"propiedad": "Propiedad", "tenencia_3": "Alquiler de mercado", "sobrecarga_30": "Sobrecarga > 30 %",
               "sobrecarga_40": "Sobrecarga > 40 %", "esfuerzo_alquiler_30": "Alquiler > 30 % renta (inquilinos)",
               "esfuerzo_alquiler_40": "Alquiler > 40 % renta (inquilinos)", "hacinamiento": "Hacinamiento"}
    b["et"] = b.indicador.map(nombres)
    fig, ax = plt.subplots()
    y = np.arange(len(b))
    ax.errorbar(b.diferencia_estandarizada, y, xerr=[b.diferencia_estandarizada - b.ic95_inf, b.ic95_sup - b.diferencia_estandarizada],
                fmt="o", color=F.OKABE[0], capsize=2)
    ax.axvline(0, color="#666666", lw=0.8)
    ax.set_yticks(y, b.et)
    ax.set_xlabel("puntos porcentuales (adultos de nacionalidad extranjera − española, igual edad y renta)")
    ax.set_title(f"Condiciones de vivienda a igual edad y renta, {b.periodo.iloc[0]}")
    F.guardar(fig, "F22_brecha_misma_edad_renta", f"Condiciones de vivienda a igual edad y renta, {b.periodo.iloc[0]}",
              "INE, ECV (microdatos); V12-B6", b.periodo.iloc[0], "C4",
              "Estandarización directa por edad y quintil de renta; IC95 bootstrap por hogar. Descriptivo: no atribuye la diferencia a la nacionalidad.",
              "Puntos con intervalo por indicador; datos en output/v12/b6/ecv_brecha_misma_edad_renta.csv.")


def f23_mapa_vlc_vut(F):
    b = pd.read_csv(O / "b7/valencia_barrios_vut_serie.csv", dtype={"cod_barrio": str})
    u = b.periodo.max()
    b = b[b.periodo == u]
    g = gpd.read_parquet(GEO / "barrios_valencia.parquet").merge(b.drop(columns=["nombre"]), on="cod_barrio", how="left")
    F.mapa(g, "pct_vut", "F23_mapa_valencia_vut_barrio", f"València: viviendas turísticas por barrio, {u}",
           "INE, medición experimental de viviendas turísticas (secciones → barrios); V12-B7", u, "C4",
           "Porcentaje del parque; sección → barrio por área cuando la sección cruza barrios.",
           "Mapa de barrios de València; datos en output/v12/b7/valencia_barrios_vut_serie.csv.", etiqueta="% del parque")


FIGURAS = [f15_contabilidad, f16_mapa_exterior, f17_od, f18_jefatura, f19_mapa_presion, f20_catastro_mivau, f21_mapa_titularidad,
           f22_brecha, f23_mapa_vlc_vut]
