"""C1 (P-C1): panel sección-año 2016-2024, sellado inmediato y preparación de variables.
build_panel() -> sellar_v3 ('c1_panel') -> solo el entrenamiento sale de aquí. prep() es idéntica en
entrenamiento y en sellado (misma función dentro de fn)."""
import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
import gl_data as gl  # noqa: E402  (constantes y rutas del panel GL)

holdout = gl.holdout
D, SEED, RAIZ = gl.D, gl.SEED, gl.RAIZ
OUT = RAIZ / "output/v3/C1"
ANIOS_ALQ = list(range(2016, 2025))
ANIOS = [2021, 2022, 2023, 2024]
CIUDADES = {"08019": "Barcelona", "28079": "Madrid", "46250": "València", "41091": "Sevilla", "29067": "Málaga",
            "07040": "Palma"}
CIUDADES5 = [m for m in CIUDADES if m != "07040"]
CTRL = {"t10_1": "paro", "t5_1": "extranjeros", "t4_3": "mayores64", "t9_1": "est_sup", "t3_1": "edad_media",
        "t20_2": "viv_alq", "t19_1": "viv_ppal", "t22_1": "hog_1p"}


def _lee_alquiler():
    s = pd.read_csv(D / "serpavi_secciones_nacional_v3.csv.gz", usecols=["periodo", "serie", "valor", "codigo"],
                    dtype={"codigo": str})
    s = s[s.periodo.isin(ANIOS_ALQ)]
    mapa = {"ALQM2_LV_M_VC": "alq", "ALQM2_LV_M_VU": "alq_vu", "ALQTBID12_M_VC": "alq_eur",
            "ALQTBID12_M_VU": "alq_eur_vu"}
    s["m"] = s.serie.str.split("_", n=3).str[3].map(mapa)
    s = s.dropna(subset=["m"])
    s["codigo"] = s.codigo.str.zfill(10)
    return s.pivot_table(index=["codigo", "periodo"], columns="m", values="valor").reset_index().rename(
        columns={"periodo": "anio"})


def _lee_vut():
    v = pd.read_csv(D / "ine_v3_vut_seccion.csv.gz", usecols=["periodo", "nivel", "codigo", "medida", "valor"],
                    dtype={"codigo": str})
    v = v[(v.nivel == "seccion") & (v.medida == "vivienda_turistica") & (v.periodo < "2025")]   # nunca 2026M05
    v["codigo"] = v.codigo.str.zfill(10)
    v["anio"] = v.periodo.str[:4].astype(int)
    ago = v[v.periodo.str.endswith("M08")].rename(columns={"valor": "vut"})[["codigo", "anio", "vut"]]
    feb = v[v.periodo == "2021M02"].rename(columns={"valor": "vut_2102"})[["codigo", "vut_2102"]]
    return ago, feb


def _lee_censo():
    c = pd.read_csv(D / "ine_v3_censo2021_seccion_indicadores.csv.gz", usecols=["serie", "codigo", "valor"],
                    dtype={"codigo": str})
    c = c[c.serie.isin(["t18_1", "t21_1"] + list(CTRL))].pivot_table(index="codigo", columns="serie",
                                                                       values="valor").reset_index()
    c["codigo"] = c.codigo.str.zfill(10)
    c["t20_2"] = c.t20_2 / c.t19_1.where(c.t19_1 > 0)          # cuota de alquiler en principales
    c["t19_1"] = c.t19_1 / c.t18_1.where(c.t18_1 > 0)          # cuota de principales
    c["t22_1"] = c.t22_1 / c.t21_1.where(c.t21_1 > 0)
    return c.rename(columns={"t18_1": "viv", "t21_1": "hog", **CTRL})


def _lee_adrh():
    g = pd.read_csv(D / "ine_v3_gis_seccion.csv.gz", dtype={"codigo": str},
                    usecols=["codigo", "campo", "valor", "indicador", "anio"])
    g = g[(g.indicador == "Renta neta media por hogar") & (g.campo == "dato2")]
    g["codigo"] = g.codigo.str.zfill(10)
    g["anio"] = g.anio.astype(int)
    return g.groupby(["codigo", "anio"], as_index=False).valor.mean().rename(columns={"valor": "adrh"})


def build_panel():
    """Panel largo sección-año 2016-2024 SIN separar sellado. Llamar y pasar a seal_panel() de inmediato."""
    alq = _lee_alquiler()
    ago, feb = _lee_vut()
    cen = _lee_censo()
    adrh = _lee_adrh()
    p = alq.merge(ago, on=["codigo", "anio"], how="left").merge(cen, on="codigo", how="inner")
    p = p.merge(feb, on="codigo", how="left").merge(adrh, on=["codigo", "anio"], how="left")
    p["distrito"] = p.codigo.str[:7]
    p["muni"] = p.codigo.str[:5]
    p["prov"] = p.codigo.str[:2]
    # vut_2108 estático (base 2021M08) para el instrumento
    b = ago[ago.anio == 2021].set_index("codigo").vut.rename("vut_2108")
    p = p.join(b, on="codigo")
    return p.sort_values(["codigo", "anio"]).reset_index(drop=True)


def conteos_presello(p):
    """Recuentos (sin valores de resultado) de secciones/distritos balanceados 2021-24 sellados, para P2."""
    m = p[p.anio.isin(ANIOS) & (p.alq > 0) & (p.viv > 0) & p.vut.notna()]
    ok = m.groupby("codigo").anio.nunique()
    m = m[m.codigo.isin(ok[ok == 4].index)]
    s = holdout.es_sellado_v3(m.codigo)
    out = {}
    for nom, msk in (("nacional", m.muni.notna()), ("6 ciudades", m.muni.isin(CIUDADES)),
                     ("5 ciudades", m.muni.isin(CIUDADES5))):
        a = m[msk & s]
        out[nom] = {"secciones": int(a.codigo.nunique()), "distritos": int(a.distrito.nunique())}
    return out


def seal_panel(p):
    """Separa el sellado v3 INMEDIATAMENTE; devuelve solo el entrenamiento."""
    return holdout.sellar_v3(p, "c1_panel", col_codigo="codigo", col_periodo=None)


def prep(df, tipo="VC", resultado="mediana", min_viv=0):
    """Variables derivadas, idéntica para entrenamiento y sellado. Devuelve (panel 2021-24 balanceado, lead).
    panel: lnalq, vut100, dvut100, lvut. lead: Δ ln alq 2016-2020 por sección con ΔVUT 2021-24 y nivel 2021."""
    col = {("VC", "mediana"): "alq", ("VU", "mediana"): "alq_vu", ("VC", "eur"): "alq_eur",
           ("VU", "eur"): "alq_eur_vu"}[(tipo, resultado)]
    d = df.copy()
    d["y_niv"] = d[col]
    pan = d[d.anio.isin(ANIOS) & (d.y_niv > 0) & (d.viv > 0) & d.vut.notna() & (d.viv >= min_viv)].copy()
    ok = pan.groupby("codigo").anio.nunique()
    pan = pan[pan.codigo.isin(ok[ok == 4].index)].copy()
    # municipios con una sola sección no aportan variación con FE año×municipio, pero se conservan (se absorben)
    pan["lnalq"] = np.log(pan.y_niv)
    pan["vut100"] = 100 * pan.vut / pan.viv
    pan["lvut"] = np.log1p(pan.vut)
    pan["lvut100"] = np.log1p(pan.vut100)
    pan = pan.sort_values(["codigo", "anio"]).reset_index(drop=True)
    # lead (test de adelanto): alquiler 2016 y 2020 + VUT 2021-24 de las secciones del panel
    a = d[d.anio.isin([2016, 2020])].pivot(index="codigo", columns="anio", values="y_niv")
    a = a[(a > 0).all(axis=1)]
    dl = np.log(a[2020]) - np.log(a[2016])
    w = pan.pivot(index="codigo", columns="anio", values="vut100")
    lead = pd.DataFrame({"dln_prev": dl}).join(pd.DataFrame({"d_vut100": w[2024] - w[2021], "vut100_2021": w[2021]}),
                                               how="inner")
    st = pan.drop_duplicates("codigo").set_index("codigo")[["muni", "distrito", "prov", "viv", "vut_2108",
                                                            "vut_2102"]]
    lead = lead.join(st).reset_index()
    return pan, lead
