"""V10-B3 · `make figuras`: figuras y mapas de publicación con un estilo único, desde la base (data/base) y el atlas
(output/v10/atlas, derivado de la base y de los microdatos). Sin red y determinista.

Estilo: paleta Okabe-Ito (apta para daltonismo), tipografía DejaVu Sans, rejilla ligera; cada figura se guarda en
tres formatos:
  figuras/paper/<id>.png (16 × 10 cm, 300 ppp) y figuras/paper/<id>.pdf
  figuras/web/<id>.svg
  figuras/redes/<id>.png (1200 × 675 px)
y lleva su ficha en figuras/fichas.json y figuras/README.md (título, fuente, fecha del dato, capa y nota).
"""
from __future__ import annotations

import json
from pathlib import Path

import duckdb
import geopandas as gpd
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402

RAIZ = Path(__file__).resolve().parents[2]
BASE = RAIZ / "data" / "base"
ATLAS = RAIZ / "output" / "v10" / "atlas"
FIG = RAIZ / "figuras"
OKABE = ["#0072B2", "#E69F00", "#009E73", "#D55E00", "#CC79A7", "#56B4E9", "#F0E442", "#000000"]
SECUENCIAL = "cividis"   # perceptualmente uniforme y legible con daltonismo
DIVERGENTE = "PuOr"
FICHAS: list[dict] = []

plt.rcParams.update({
    "font.family": "DejaVu Sans", "font.size": 9, "axes.titlesize": 10, "axes.titleweight": "bold",
    "axes.labelsize": 9, "axes.spines.top": False, "axes.spines.right": False, "axes.grid": True,
    "grid.color": "#dddddd", "grid.linewidth": 0.6, "axes.prop_cycle": matplotlib.cycler(color=OKABE),
    "legend.frameon": False, "figure.dpi": 100, "savefig.bbox": "tight", "svg.hashsalt": "vivienda-v10",
    "pdf.compression": 9,
})


def q(sql: str) -> pd.DataFrame:
    con = duckdb.connect()
    con.execute(f"CREATE VIEW h AS SELECT * FROM read_parquet('{BASE / 'publica' / 'hechos.parquet'}') WHERE NOT posterior_prereg")
    con.execute(f"CREATE VIEW t AS SELECT * FROM read_parquet('{BASE / 'publica' / 'territorios.parquet'}')")
    con.execute(f"CREATE VIEW atr AS SELECT * FROM read_parquet('{BASE / 'publica' / 'v8_atribucion.parquet'}')")
    con.execute(f"CREATE VIEW cif AS SELECT * FROM read_parquet('{BASE / 'publica' / 'cifras_clave.parquet'}')")
    d = con.execute(sql).df()
    con.close()
    return d


def guardar(fig, ident: str, titulo: str, fuente: str, fecha: str, capa: str, nota: str, alt: str) -> None:
    pie = f"Fuente: {fuente}. Dato: {fecha}. Capa {capa}."
    fig.text(0.0, -0.02, pie, fontsize=7, color="#444444", ha="left", va="top", wrap=True)
    for sub in ("paper", "web", "redes"):
        (FIG / sub).mkdir(parents=True, exist_ok=True)
    fig.set_size_inches(16 / 2.54, 10 / 2.54)
    meta = {"Title": titulo, "Creator": "vivienda-espana-evidencia (V10)"}
    fig.savefig(FIG / "paper" / f"{ident}.png", dpi=300, metadata={**meta, "Software": None})
    fig.savefig(FIG / "paper" / f"{ident}.pdf", metadata={**meta, "CreationDate": None, "ModDate": None, "Producer": None})
    fig.savefig(FIG / "web" / f"{ident}.svg", metadata={"Title": titulo, "Date": None, "Creator": None})
    fig.set_size_inches(12, 6.75)
    fig.savefig(FIG / "redes" / f"{ident}.png", dpi=100, metadata={**meta, "Software": None})
    plt.close(fig)
    FICHAS.append({"id": ident, "titulo": titulo, "fuente": fuente, "fecha_dato": fecha, "capa": capa, "nota": nota,
                   "texto_alternativo": alt, "ficheros": [f"paper/{ident}.png", f"paper/{ident}.pdf", f"web/{ident}.svg",
                                                          f"redes/{ident}.png"]})


# ------------------------------------------------------------------------------------------------ figuras del atlas
def f01_sobrecarga_tenencia():
    t = pd.read_csv(ATLAS / "a_quien_ecv.csv")
    d = t[(t.grupo == "tenencia") & (t.indicador == "sobrecarga_40")]
    fig, ax = plt.subplots()
    for i, (cat, x) in enumerate(d.groupby("categoria")):
        x = x.sort_values("anio")
        ax.plot(x.anio, x.valor, marker="o", ms=3, label=cat, color=OKABE[i])
        ax.fill_between(x.anio, x.ic95_inf, x.ic95_sup, alpha=0.15, color=OKABE[i], lw=0)
    ax.set_ylabel("% de personas con gasto en vivienda > 40 % de la renta")
    ax.set_title("Sobrecarga del gasto en vivienda por régimen de tenencia, España")
    ax.legend(fontsize=7, ncol=2)
    capa = "C1 en propiedad y alquiler de mercado (coinciden con Eurostat ≤0,5 p. todos los años); C4 en alquiler inferior al de mercado y cesión"
    guardar(fig, "F01_sobrecarga_tenencia", "Sobrecarga del gasto en vivienda (>40 %) por tenencia, 2018-2025",
            "INE, ECV (microdatos), cálculo propio; contraste con Eurostat ilc_lvho07c", "ECV 2018-2025 (renta del año anterior)",
            capa, "Bandas: IC 95 % por linealización (sin estratos públicos).",
            "Líneas con bandas de confianza, una por régimen de tenencia, 2018-2025.")


def f02_esfuerzo_grupos():
    t = pd.read_csv(ATLAS / "a_quien_ecv.csv")
    ult = t.anio.max()
    d = t[(t.anio == ult) & (t.indicador == "esfuerzo_alquiler_mediana") & t.grupo.isin(["edad", "nacionalidad", "decil_renta"])]
    d = d.assign(etq=d.grupo.map({"edad": "Edad", "nacionalidad": "Nacionalidad", "decil_renta": "Decil"}) + ": " + d.categoria.astype(str))
    d = d.sort_values(["grupo", "categoria"])
    fig, ax = plt.subplots()
    y = np.arange(len(d))
    ax.errorbar(d.valor, y, xerr=[d.valor - d.ic95_inf, d.ic95_sup - d.valor], fmt="o", ms=3, color=OKABE[0], ecolor="#888888")
    ax.set_yticks(y, d.etq, fontsize=6)
    ax.axvline(30, color=OKABE[3], lw=0.8, ls="--")
    ax.set_xlabel("Alquiler anual / renta disponible del hogar (mediana, %)")
    ax.set_title(f"Esfuerzo de los hogares que alquilan a precio de mercado, {ult}")
    guardar(fig, "F02_esfuerzo_alquiler_grupos", f"Esfuerzo mediano de alquiler por edad, nacionalidad y decil, {ult}",
            "INE, ECV (microdatos), cálculo propio", f"ECV {ult}", "C4",
            "Mediana ponderada; IC 95 % de Woodruff. Personas que viven en hogares de alquiler a precio de mercado. Línea: 30 %.",
            "Puntos con intervalos de confianza por grupo de edad, nacionalidad y decil de renta.")


def f03_ipva_brecha_ccaa():
    t = pd.read_csv(ATLAS / "b_ipva_nuevo_existente.csv", dtype={"territorio_codigo": str})
    d = t[(t.periodo == t.periodo.max()) & (t.nivel.isin(["ccaa", "nacional"]))].sort_values("brecha_nuevo_menos_existente")
    fig, ax = plt.subplots()
    col = [OKABE[3] if n == "nacional" else OKABE[0] for n in d.nivel]
    ax.barh(d.nombre, d.brecha_nuevo_menos_existente, color=col)
    ax.set_xlabel("Índice de contratos nuevos − índice de contratos existentes (2015 = 100)")
    ax.set_title(f"Entrar frente a quedarse: brecha de renta acumulada desde 2015, {d.periodo.max()}")
    ax.tick_params(axis="y", labelsize=6)
    guardar(fig, "F03_ipva_brecha_ccaa", "Brecha entre contratos nuevos y existentes (IPVA) por CCAA",
            "INE, Índice de Precios de Vivienda en Alquiler (59004)", str(d.periodo.max()), "C4",
            "Índices encadenados: comparan crecimientos desde 2015, no niveles.",
            "Barras horizontales por comunidad; España en otro color.")


def f04_contratos_nuevos_existentes():
    t = pd.read_csv(ATLAS / "b_ipva_nuevo_existente.csv", dtype={"territorio_codigo": str})
    d = t[t.nivel == "nacional"].sort_values("periodo")
    fig, ax = plt.subplots()
    ax.plot(d.periodo, d.nuevo, marker="o", ms=3, label="Contratos nuevos")
    ax.plot(d.periodo, d.existente, marker="s", ms=3, label="Contratos existentes")
    ax.set_ylabel("Índice 2015 = 100")
    ax.set_title("Renta de los contratos nuevos frente a los existentes, España")
    ax.legend()
    guardar(fig, "F04_contratos_nuevos_existentes", "IPVA: contratos nuevos frente a existentes, España 2015-2024",
            "INE, IPVA (59004)", "2015-2024", "C4", "Figura clave de V5 (contratos nuevos frente a vigentes), regenerada desde la base.",
            "Dos líneas de índice 2015=100, contratos nuevos y existentes, 2015-2024.")


def mapa(gdf, col, ident, titulo, fuente, fecha, capa, nota, alt, cmap=SECUENCIAL, etiqueta="", centro=None):
    fig, ax = plt.subplots()
    kw = {}
    if centro is not None:
        import matplotlib.colors as mcolors
        lim = np.nanmax(np.abs(gdf[col] - centro))
        kw["norm"] = mcolors.TwoSlopeNorm(vcenter=centro, vmin=centro - lim, vmax=centro + lim)
    gdf.plot(column=col, ax=ax, cmap=cmap, legend=True, linewidth=0.1, edgecolor="#ffffff",
             missing_kwds={"color": "#eeeeee", "hatch": "///", "label": "sin dato"},
             legend_kwds={"shrink": 0.6, "label": etiqueta}, **kw)
    ax.set_axis_off()
    ax.set_title(titulo)
    guardar(fig, ident, titulo, fuente, fecha, capa, nota, alt)


def peninsula(g):
    """Recoloca Canarias junto a la península para los mapas de España (solo visual)."""
    g = g.copy()
    can = g.cod_provincia.isin(["35", "38"]) if "cod_provincia" in g else g.index.isin([])
    g.loc[can, "geometry"] = g.loc[can, "geometry"].translate(xoff=5.5, yoff=6.5)
    return g


def f05_mapa_provincias_esfuerzo():
    p = pd.read_csv(ATLAS / "d_espana_provincias.csv", dtype={"cod_provincia": str})
    g = gpd.read_parquet(BASE / "geo" / "provincias.parquet").merge(p, on="cod_provincia", how="left")
    mapa(peninsula(g), "alquiler_anual_80m2_pct_renta_persona", "F05_mapa_provincias_alquiler_renta",
         "Alquiler de 80 m² sobre la renta neta por persona, 2024", "MIVAU SERPAVI; INE ADRH y censo anual",
         "alquiler 2024; renta 2023", "C4", "Indicador comparativo (vivienda tipo de 80 m²; renta por persona). Canarias recolocada.",
         "Mapa coroplético de provincias; los valores por provincia están en output/v10/atlas/d_espana_provincias.csv.", etiqueta="% de la renta por persona")


def f06_mapa_deficit():
    d = q("SELECT territorio_codigo cod_provincia, valor FROM h WHERE variable = 'v5_deficit_2021_2025' AND desagregacion = 'estadistico=mediana'")
    pob = q("SELECT territorio_codigo cod_provincia, valor pob FROM h WHERE variable = 'pob_censo_anual' AND nivel = 'provincia' AND periodo = '2025' AND desagregacion = 'nacionalidad=Total'")
    d = d.merge(pob, on="cod_provincia")
    d["por_1000"] = 1000 * d.valor / d.pob
    g = gpd.read_parquet(BASE / "geo" / "provincias.parquet").merge(d, on="cod_provincia", how="left")
    mapa(peninsula(g), "por_1000", "F06_mapa_deficit_provincias", "Déficit de vivienda 2021-2025 por 1.000 habitantes (mediana)",
         "Resultado publicado V5 (A4) desde la base; INE censo anual", "2021-2025", "C4",
         "Mediana de las variantes de A4; rango en la base (estadístico min/max). Figura clave de V5.",
         "Mapa de provincias con el déficit relativo; negativo = sin déficit.", cmap=DIVERGENTE, centro=0,
         etiqueta="viviendas por 1.000 hab.")


def f07_mapa_cv_alquiler():
    d = pd.read_csv(ATLAS / "d_cv_municipios.csv", dtype={"cod_municipio": str})
    g = gpd.read_parquet(BASE / "geo" / "municipios.parquet")
    g = g[g.cod_ccaa == "10"].merge(d, left_on="cod_municipio", right_on="cod_municipio", how="left")
    mapa(g, "var_alquiler_2019_2024_pct", "F07_mapa_cv_alquiler", "Comunitat Valenciana: variación del alquiler 2019-2024",
         "MIVAU SERPAVI (stock de contratos)", "2019-2024", "C4", "Mediana €/m² de vivienda colectiva; municipios sin dato en gris.",
         "Mapa coroplético de municipios de la Comunitat Valenciana; valores en output/v10/atlas/d_cv_municipios.csv.", etiqueta="%")


def f08_mapa_vlc_barrios():
    b = pd.read_csv(ATLAS / "c_valencia_barrio.csv", dtype={"cod_barrio": str})
    g = gpd.read_parquet(BASE / "geo" / "barrios_valencia.parquet").merge(b.drop(columns=["nombre"]), on="cod_barrio", how="left")
    mapa(g, "indice_presion_descriptivo", "F08_mapa_valencia_indice", "València: índice descriptivo de presión residencial por barrio",
         "INE (censo anual, viviendas turísticas, Censo 2021), MIVAU SERPAVI, Ajuntament de València", "2019-2026", "C4",
         "Media de puntuaciones z de 4 componentes (alquiler 2024, su variación 2019-2024, viviendas turísticas por 100 "
         "viviendas y cambio del % de extranjeros). Solo descriptivo.", "Mapa de barrios de València.", cmap=SECUENCIAL,
         etiqueta="puntuación z media")


def f09_mapa_vlc_vut():
    s = pd.read_csv(ATLAS / "c_valencia_seccion.csv", dtype={"cod_seccion": str})
    g = gpd.read_parquet(BASE / "geo" / "secciones.parquet")
    g = g[g.cod_municipio == "46250"].merge(s, on="cod_seccion", how="left")
    g["vut_por_100_viv"] = g.vut_por_100_viv.clip(upper=g.vut_por_100_viv.quantile(0.98))
    mapa(g, "vut_por_100_viv", "F09_mapa_valencia_vut", "València: viviendas turísticas por 100 viviendas, mayo de 2026",
         "INE, medición experimental de viviendas turísticas; Censo 2021", "2026-05", "C4",
         "Denominador: viviendas del Censo 2021. Escala truncada al percentil 98.", "Mapa de secciones censales.",
         etiqueta="por 100 viviendas")


def f10_ciudades():
    e = pd.read_csv(ATLAS / "e_ciudades_comparables.csv", dtype={"periodo": str})
    d = e[(e.indicador == "alquiler_m2_mediana") & (e.periodo >= "2015")]
    fig, ax = plt.subplots()
    for i, (c, x) in enumerate(d.groupby("ciudad")):
        x = x.sort_values("periodo")
        ax.plot(x.periodo.astype(int), x.valor, marker="o", ms=2.5, label=c, color=OKABE[i % 8], lw=2.2 if c == "València" else 1.2)
    ax.set_ylabel("€/m²/mes (mediana)")
    ax.set_title("Alquiler mediano en València y ciudades comparables")
    ax.legend(fontsize=7, ncol=2)
    guardar(fig, "F10_ciudades_alquiler", "Alquiler mediano 2015-2024: València y ciudades comparables", "MIVAU SERPAVI",
            "2015-2024", "C4", "Bilbao solo 2024 (territorios forales). Sin inferencia causal.", "Líneas por ciudad.")


def f11_factor_comun():
    d = q("SELECT periodo, valor FROM h WHERE variable = 'v8_factor_comun_precios' ORDER BY periodo")
    fig, ax = plt.subplots()
    x = pd.PeriodIndex(d.periodo.str.replace("T", "Q"), freq="Q").to_timestamp()
    ax.plot(x, d.valor, color=OKABE[0])
    ax.axhline(0, color="#999999", lw=0.6)
    ax.set_title("Factor común de las fuentes de precio de la vivienda (V8, M1)")
    ax.set_ylabel("Primer componente principal")
    guardar(fig, "F11_factor_comun", "Factor común de precios (V8 M1)", "Resultado publicado V8 (M1) desde la base",
            "1996T1-2026T2", "C4", "Figura clave de V8 regenerada desde la base.", "Serie trimestral del factor común.")


def f12_descomposicion():
    d = q("""SELECT * FROM atr WHERE ambito = 'nacional' AND metodo = 'svar_hd' AND variante = 'V3'""")
    if d.empty:
        d = q("SELECT * FROM atr WHERE ambito = 'nacional'")
    fig, axes = plt.subplots(1, 2, sharey=True)
    for ax, (mercado, x) in zip(axes, d.groupby("mercado")):
        piv = x.pivot_table(index="periodo", columns="factor", values="contribucion_pp")
        lo = x.pivot_table(index="periodo", columns="factor", values="b68_lo")
        hi = x.pivot_table(index="periodo", columns="factor", values="b68_hi")
        n = len(piv.columns)
        ancho = 0.8 / max(n, 1)
        for i, f in enumerate(piv.columns):
            pos = np.arange(len(piv)) + (i - n / 2) * ancho + ancho / 2
            ax.bar(pos, piv[f], width=ancho, color=OKABE[i % 8], label=f)
            ax.errorbar(pos, piv[f], yerr=[piv[f] - lo[f], hi[f] - piv[f]], fmt="none", ecolor="#555555", lw=0.6)
        ax.set_xticks(np.arange(len(piv)), piv.index)
        ax.set_title(mercado)
        ax.axhline(0, color="#999999", lw=0.6)
    axes[0].set_ylabel("Contribución (puntos)")
    axes[-1].legend(fontsize=6)
    capa = ",".join(sorted(d.capa.unique()))
    guardar(fig, "F12_descomposicion_periodos", "Descomposición por periodo (V8, atribución con bandas del 68 %)",
            "Resultado publicado V8 (F5, atribución combinada) desde la base", "periodos P1-P5 de V8", capa,
            "C3s: condicionada a las restricciones de signo explícitas. Figura clave de V8.",
            "Barras por factor y periodo con bandas, para compra y alquiler.")


def f13_cotas():
    d = q("SELECT id, indicador, valor, min, max, unidad, periodo, capa FROM cif WHERE capa = 'C2'")
    for c in ("valor", "min", "max"):
        d[c] = pd.to_numeric(d[c], errors="coerce")
    d = d[d.unidad == d.unidad.mode().iloc[0]] if len(d) else d
    fig, ax = plt.subplots()
    y = np.arange(len(d))
    ax.scatter(d.valor, y, color=OKABE[0], zorder=3)
    ok = d["min"].notna() & d["max"].notna()
    ax.hlines(y[ok], d["min"][ok], d["max"][ok], color=OKABE[1], lw=3, alpha=0.6)
    ax.set_yticks(y, [t[:70] for t in d.indicador], fontsize=6)
    ax.set_xlabel(d.unidad.iloc[0] if len(d) else "")
    ax.set_title("Cotas (C2) publicadas: valor y rango de supuestos")
    guardar(fig, "F13_cotas_c2", "Cotas C2 publicadas (verificador)", "publicacion/cifras_clave.csv desde la base",
            "según cada cifra", "C2", "Cotas de Manski con supuestos explícitos (ver la ficha de cada cifra).",
            "Puntos y rangos de las cotas.")


def f14_emancipacion():
    t = pd.read_csv(ATLAS / "a_quien_epa.csv")
    d = t[(t.grupo == "nacionalidad") & (t.tramo_edad.isin(["25-29", "30-34"]))]
    fig, ax = plt.subplots()
    i = 0
    for (tramo, nac), x in d.groupby(["tramo_edad", "categoria"]):
        if nac == "doble nacionalidad":
            continue
        x = x.sort_values("anio")
        ax.plot(x.anio, x.valor, marker="o", ms=2.5, label=f"{tramo}, {nac}", color=OKABE[i % 8], ls="-" if tramo == "25-29" else "--")
        i += 1
    ax.set_ylabel("% que vive con al menos uno de sus padres")
    ax.set_title("Jóvenes que viven con sus padres, por edad y nacionalidad")
    ax.legend(fontsize=7)
    guardar(fig, "F14_emancipacion_epa", "Jóvenes que viven con sus padres (EPA), 2018-2026",
            "INE, EPA (microdatos), cálculo propio", "2018T1-2026T2 (2026: media de T1-T2)", "C4",
            "Media anual de trimestres; IC en la tabla del atlas.", "Líneas por tramo de edad y nacionalidad.")


def main() -> dict:
    FIG.mkdir(parents=True, exist_ok=True)
    FICHAS.clear()
    for f in (f01_sobrecarga_tenencia, f02_esfuerzo_grupos, f03_ipva_brecha_ccaa, f04_contratos_nuevos_existentes,
              f05_mapa_provincias_esfuerzo, f06_mapa_deficit, f07_mapa_cv_alquiler, f08_mapa_vlc_barrios, f09_mapa_vlc_vut,
              f10_ciudades, f11_factor_comun, f12_descomposicion, f13_cotas, f14_emancipacion):
        f()
    (FIG / "fichas.json").write_text(json.dumps(FICHAS, ensure_ascii=False, indent=1), encoding="utf-8")
    lin = ["# Figuras de publicación (V10)", "", "Generadas por `make figuras` (src/v10/figuras.py); no editar a mano.",
           "Paleta Okabe-Ito (apta para daltonismo); mapas con «cividis» (secuencial) o «PuOr» (divergente).", "",
           "| id | título | fuente | dato | capa | nota |", "|---|---|---|---|---|---|"]
    lin += [f"| {f['id']} | {f['titulo']} | {f['fuente']} | {f['fecha_dato']} | {f['capa']} | {f['nota']} |" for f in FICHAS]
    (FIG / "README.md").write_text("\n".join(lin) + "\n", encoding="utf-8")
    return {"figuras": len(FICHAS)}


if __name__ == "__main__":
    print(main())
