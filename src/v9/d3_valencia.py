"""V9 F3 · D3 caída del registro de viviendas turísticas por código postal (Comunitat Valenciana). DESCRIPTIVO (C4).
Pre-registro: docs/v9/hipotesis.md (D3) con el addendum A1.4: resultado 2024→2025 (último año completo previo al
2026-07-01): Δ cuota del CP en las fianzas de su provincia (puntos) y Δ log fianza media; exposición ΔVUT GVA por 100
viviendas entre los cortes 2025-01-26 y 2026-10-14 (excepción declarada) y, como alternativa, Δ viviendas turísticas
del INE por sección 2024M11→2025M11 asignadas al CP. Controles: renta ADRH 2022, log población y viviendas (censo 2021),
distancia al centro de València, indicador de València ciudad. Errores de Conley a 5 y 10 km. Placebo 2021→2023.
Salidas: output/v9/d3/{tabla_d3.csv, resultado.json, registry.csv, fig_d3.png}. Sin lenguaje causal.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import matplotlib
import numpy as np
import pandas as pd

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import herramientas as H  # noqa: E402
import paneles as P  # noqa: E402
from econ_utils import Registry  # noqa: E402

OUT = P.RAIZ / "output" / "v9" / "d3"
REG = Registry(OUT / "registry.csv")
CENTRO_VLC = (-0.3763, 39.4699)   # plaza del Ayuntamiento de València (lon, lat)


def seccion_a_cp(valores: pd.Series, cp_tab: pd.DataFrame, media: bool) -> pd.Series:
    """Asigna una variable por sección al CP con los pesos de portales; media ponderada por viviendas o suma."""
    m = cp_tab.merge(valores.rename("v").rename_axis("seccion").reset_index(), on="seccion", how="inner")
    if media:
        m["wv"] = m.peso * m.viviendas.fillna(0)
        return m.groupby("cp").apply(lambda x: np.average(x.v, weights=x.wv) if x.wv.sum() > 0 else np.nan, include_groups=False)
    return (m.v * m.peso).groupby(m.cp).sum()


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    import geopandas as gpd
    from shapely.geometry import Point
    f = P.fianzas_gva_cp()
    f["prov"] = f.cp.str[:2]
    f["cuota"] = 100 * f.fianzas / f.groupby(["anio", "prov"]).fianzas.transform("sum")
    w = f.pivot_table(index="cp", columns="anio", values=["fianzas", "fianza_media", "cuota"])
    v = P.vut_gva_cp().set_index("cp")
    viv = P.viviendas_cp().set_index("cp")
    c = pd.read_csv(P.RAIZ / "data/raw/v9/ine_callejero/seccion_cp_2025.csv.gz", dtype={"seccion": str, "cp": str, "cod_municipio": str})
    c["peso"] = c.portales_aprox / c.groupby("seccion").portales_aprox.transform("sum")
    cen = pd.read_csv(P.RAW / "v3/ine_v3_censo2021_seccion_indicadores.csv.gz", dtype=str, usecols=["serie", "valor", "codigo"])
    cen = cen[cen.serie.isin(["t18_1", "t1_1"])].pivot_table(index="codigo", columns="serie", values="valor", aggfunc="first").astype(float)
    c = c.merge(cen.rename(columns={"t18_1": "viviendas", "t1_1": "personas"}), left_on="seccion", right_index=True, how="left")
    g = pd.read_csv(P.RAW / "v3/ine_v3_gis_seccion.csv.gz", dtype=str)
    adrh = g[(g.campo == "dato1") & (g.servicio == "ADRH_2022_Renta_media_por_persona")].set_index("codigo").valor.astype(float)
    vi = pd.read_csv(P.RAW / "v3/ine_v3_vut_seccion.csv.gz", dtype=str)
    vi = vi[(vi.nivel == "seccion") & (vi.medida == "vivienda_turistica") & vi.periodo.isin(["2024M11", "2025M11"])]
    vi = vi.pivot_table(index="codigo", columns="periodo", values="valor", aggfunc=lambda s: pd.to_numeric(s).sum())
    d_ine = (vi["2025M11"] - vi["2024M11"]).dropna()
    base = pd.DataFrame(index=sorted(set(w.index) & set(v.index) & set(viv.index)))
    base = base[base.index.str[:2].isin(["03", "12", "46"])]
    for a in (2021, 2023, 2024, 2025):
        base[f"n{a}"] = w[("fianzas", a)]
        base[f"m{a}"] = w[("fianza_media", a)]
        base[f"c{a}"] = w[("cuota", a)]
    base["viviendas"] = viv.viviendas
    base["dvut"] = 100 * (v.vut_2026 - v.vut_2025) / viv.viviendas
    base["dvut_ine"] = 100 * seccion_a_cp(d_ine, c, media=False).reindex(base.index) / viv.viviendas
    base["adrh"] = seccion_a_cp(adrh, c, media=True).reindex(base.index) / 1000
    base["lpob"] = np.log(seccion_a_cp(c.set_index("seccion").personas.groupby(level=0).first(), c, media=False).reindex(base.index))
    base["lviv"] = np.log(viv.viviendas)
    pts = gpd.GeoSeries([Point(*CENTRO_VLC)], crs=4326).to_crs(3035).iloc[0]
    base["dist_km"] = np.sqrt((viv.lon - pts.x) ** 2 + (viv.lat - pts.y) ** 2) / 1000
    base["vlc"] = (viv.cod_municipio == "46250").astype(float)
    base["x"], base["y"] = viv.lon, viv.lat
    tabla = []

    def reg(muestra, ycol, xcol, etiqueta, a0, a1):
        d = muestra[[ycol, xcol, "adrh", "lpob", "lviv", "dist_km", "vlc", "x", "y"]].replace([np.inf, -np.inf], np.nan).dropna()
        ctrls = ["adrh", "lpob", "lviv", "dist_km"] + (["vlc"] if d.vlc.nunique() > 1 else [])
        X = np.column_stack([np.ones(len(d)), d[xcol].values, d[ctrls].values])
        for km in (5, 10):
            r = H.conley(d[ycol].values, X, d[["x", "y"]].values, km * 1000.0)
            b, se = r["beta"][1], r["se"][1]
            tabla.append({"diseno": "D3", "hipotesis": "descriptiva (C4)", "resultado": ycol, "exposicion": xcol,
                          "especificacion": f"{etiqueta}; Conley {km} km", "beta": b, "se": se, "ic95_lo": b - 1.96 * se,
                          "ic95_hi": b + 1.96 * se, "p": r["p"][1], "se_hc1": r["se_hc1"][1], "N_unidades": len(d),
                          "confirmatoria": False, "media_exposicion": float(d[xcol].mean()), "de_exposicion": float(d[xcol].std())})
            REG.log("v9-D3", f"{ycol}|{xcol}|{etiqueta}|{km}km", f"{ycol} ~ {xcol} + " + "+".join(ctrls), a0, a1, len(d),
                    np.nan, np.nan, np.nan, coef_interes=b, p_interes=r["p"][1], notas="descriptivo")

    ok = base[(base.n2024 >= 20) & (base.n2025 >= 20)].copy()
    ok["d_cuota"] = ok.c2025 - ok.c2024
    ok["d_lmedia"] = np.log(ok.m2025 / ok.m2024)
    for ycol in ("d_cuota", "d_lmedia"):
        reg(ok, ycol, "dvut", "principal 2024→2025, exposición GVA", 2024, 2025)
        reg(ok, ycol, "dvut_ine", "alternativa: exposición INE 2024M11→2025M11", 2024, 2025)
        reg(ok[ok.vlc == 1], ycol, "dvut", "València ciudad", 2024, 2025)
    pl = base[(base.n2021 >= 20) & (base.n2023 >= 20)].copy()
    pl["d_cuota"] = pl.c2023 - pl.c2021
    pl["d_lmedia"] = np.log(pl.m2023 / pl.m2021)
    for ycol in ("d_cuota", "d_lmedia"):
        reg(pl, ycol, "dvut", "placebo 2021→2023 (misma exposición)", 2021, 2023)
    T = pd.DataFrame(tabla)
    T.to_csv(OUT / "tabla_d3.csv", index=False, float_format="%.5f")
    fig, ax = plt.subplots(1, 2, figsize=(10, 3.8))
    for j, (ycol, nom) in enumerate((("d_cuota", "Δ cuota de fianzas 2024→2025 (puntos)"), ("d_lmedia", "Δ log fianza media 2024→2025"))):
        q = pd.qcut(ok.dvut.rank(method="first"), 10, labels=False)
        bins = ok.groupby(q).agg(x=("dvut", "mean"), y=(ycol, "mean"))
        ax[j].scatter(ok.dvut, ok[ycol], s=6, alpha=0.3)
        ax[j].plot(bins.x, bins.y, "o-", color="C3", ms=4)
        ax[j].set_xlabel("Δ VUT registradas por 100 viviendas (2025-01 → 2026-10)")
        ax[j].set_title(nom, fontsize=9)
    fig.suptitle("D3 (descriptivo, C4): CP de la Comunitat Valenciana; deciles en rojo. Fuente: GVA, INE; elaboración propia", fontsize=8)
    fig.tight_layout()
    fig.savefig(OUT / "fig_d3.png", dpi=130)
    plt.close(fig)
    pr = T[T.especificacion.str.startswith("principal") & T.especificacion.str.endswith("10 km")]
    res = {"rama": "v9/d3", "pregunta": "¿Se asocia la caída del registro VUT por CP con la variación de fianzas (cuota y media)?",
           "capa": "C4 (descriptivo; sin potencia)", "datos": "GVA fianzas por CP 2021-2025, registro VUT GVA, INE VUT por sección, censo 2021, ADRH 2022",
           "N": int(pr.N_unidades.max()) if len(pr) else 0, "metodo": "MCO en diferencias largas con controles; errores de Conley",
           "estimacion": pr[["resultado", "beta"]].to_dict("records"), "ic95": pr[["ic95_lo", "ic95_hi"]].values.tolist(),
           "p_ajustado": "BH exploratorio en output/v9/f3/tabla_capas.csv", "nivel_evidencia": "DESCRIPTIVO",
           "diagnosticos": T[T.especificacion.str.startswith("placebo")][["resultado", "beta", "p"]].to_dict("records"),
           "fuera_muestra": {"modelo": None, "rmse": None, "dm_vs_ar4": None},
           "notas": "Exposición medida con un corte posterior al 2026-07-01 (excepción declarada en el addendum A1.4)."}
    (OUT / "resultado.json").write_text(json.dumps(res, ensure_ascii=False, indent=1, default=float), encoding="utf-8")
    REG.flush()
    with pd.option_context("display.width", 250, "display.max_columns", 12):
        print(T[["resultado", "exposicion", "especificacion", "beta", "se", "p", "N_unidades"]].to_string())
    return 0


if __name__ == "__main__":
    sys.exit(main())
