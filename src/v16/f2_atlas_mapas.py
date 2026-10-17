"""V16-F2.3 · Atlas: mapas PNG (6 indicadores) a escala municipal (municipios de la provincia) y por sección (municipio) para
Barcelona, València y Sevilla. Estilo del repositorio (src/v10/figuras.py): Okabe-Ito, cividis, DejaVu Sans, rejilla ligera.
Gris claro: sin dato o suprimida; gris hachurado: unidad de la muestra sellada (en blanco por validación sellada)."""
from __future__ import annotations

from pathlib import Path

import geopandas as gpd
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402

import f2_atlas_datos as D  # noqa: E402

OKABE = ["#0072B2", "#E69F00", "#009E73", "#D55E00", "#CC79A7", "#56B4E9", "#F0E442", "#000000"]
AREAS = {"barcelona": ("Barcelona", "08019", "08"), "valencia": ("València", "46250", "46"), "sevilla": ("Sevilla", "41091", "41")}
# (título, indicador municipal, periodo, indicador sección, periodo, unidad)
PANELES = [
    ("Renta mediana por unidad de consumo", "renta_mediana_uc", "2023", "renta_mediana_uc", "2023", "€"),
    ("Alquiler mediano (SERPAVI)", "alquiler_m2_mediana", "2024", "alquiler_m2_mediana", "2024", "€/m² y mes"),
    ("Ratio de esfuerzo descriptiva", "esfuerzo_alquiler_renta_hogar", "2023", "esfuerzo_alquiler_renta_hogar", "2023", "% (no es la tasa ECV)"),
    ("Viviendas turísticas", "viviendas_turisticas_pct_ine", "2026-05", "anuncios_activos_ia_por_100_viviendas", None, "% (INE VTE) / anuncios por 100 viv. (IA)"),
    ("Población extranjera", "poblacion_extranjera_pct", "2025", "poblacion_extranjera_pct", "2022", "%"),
    ("Viviendas no principales", "viviendas_no_principales_pct", "2021", "viviendas_no_principales_pct", "2021", "%"),
]


def _estilo() -> None:
    plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 8, "axes.titlesize": 9, "axes.titleweight": "bold",
                         "axes.grid": False, "legend.frameon": False, "figure.dpi": 100, "savefig.bbox": "tight",
                         "axes.prop_cycle": matplotlib.cycler(color=OKABE)})


def _geo(escala: str, prov: str, mun: str) -> gpd.GeoDataFrame:
    if escala == "municipio":
        g = gpd.read_parquet(D.GEO / "municipios.parquet", columns=["cod_municipio", "geometry"], filters=[("cod_provincia", "==", prov)])
        g = g.rename(columns={"cod_municipio": "cod"})
    else:
        g = gpd.read_parquet(D.GEO / "secciones.parquet", columns=["cod_seccion", "geometry"], filters=[("cod_municipio", "==", mun)])
        g = g.rename(columns={"cod_seccion": "cod"})
    g["cod"] = g.cod.astype(str)
    g["sellada"] = D.es_sellada(g.cod, escala).values
    return g


def _valores(a: pd.DataFrame, ind: str, nivel: str, per: str | None) -> pd.Series:
    s = a[(a.indicador == ind) & (a.nivel == nivel) & ~a.suprimida & a.valor.notna()]
    if per is None:  # última instantánea de cada unidad (Inside Airbnb: fechas distintas por ciudad)
        return s.sort_values("periodo").drop_duplicates("territorio_codigo", keep="last").set_index("territorio_codigo").valor
    return s[s.periodo == per].drop_duplicates("territorio_codigo").set_index("territorio_codigo").valor


def mapas(a: pd.DataFrame, out: Path) -> list[Path]:
    _estilo()
    out.mkdir(parents=True, exist_ok=True)
    ficheros = []
    for clave, (nombre, mun, prov) in AREAS.items():
        for escala in ("municipio", "seccion"):
            g = _geo(escala, prov, mun)
            fig, axs = plt.subplots(2, 3, figsize=(15, 10), constrained_layout=True)
            for ax, (tit, im, pm, is_, ps, uni) in zip(axs.ravel(), PANELES):
                ind, per = (im, pm) if escala == "municipio" else (is_, ps)
                if " / " in uni:
                    uni = uni.split(" / ")[0 if escala == "municipio" else 1]
                v = _valores(a, ind, escala, per)
                g["v"] = g.cod.map(v)
                ok = g[~g.sellada]
                vv = ok.v.dropna()
                ax.set_axis_off()
                ax.set_aspect("equal")
                if (~g.sellada).any():
                    ok.plot(ax=ax, color="#e6e6e6", linewidth=0.1, edgecolor="white")
                if g.sellada.any():
                    g[g.sellada].plot(ax=ax, facecolor="#bdbdbd", hatch="////", edgecolor="white", linewidth=0.1)
                if len(vv) >= 3:
                    lo, hi = np.percentile(vv, [2, 98])
                    ok[ok.v.notna()].plot(column="v", ax=ax, cmap="cividis", vmin=lo, vmax=hi, linewidth=0.1, edgecolor="white",
                                          legend=True, legend_kwds={"shrink": 0.6, "label": uni})
                perm = per or (a[(a.indicador == ind) & (a.nivel == escala)].periodo.max())
                ax.set_title(f"{tit} ({perm})\n{len(vv)} de {len(ok)} unidades con valor", loc="left", fontsize=8.5)
            ambito = f"municipios de la provincia de {nombre}" if escala == "municipio" else f"secciones censales de {nombre}"
            fig.suptitle(f"Atlas V16 (C4, descriptivo): {ambito}", fontsize=11, fontweight="bold", x=0.01, ha="left")
            fig.text(0.01, 0.005, "Gris claro: sin dato o suprimida (base < 10 o CV > 30 %). Gris hachurado: en blanco por validación sellada, "
                     "no por falta de dato. Fuentes: INE (ADRH, VTE, padrón, Censo 2021), MIVAU SERPAVI, Inside Airbnb. Sin causalidad.",
                     fontsize=7, ha="left")
            f = out / f"{clave}_{escala}.png"
            fig.savefig(f, dpi=110)
            plt.close(fig)
            ficheros.append(f)
    return ficheros
