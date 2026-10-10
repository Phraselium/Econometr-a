"""B3 · construcción del panel provincial (corte transversal, 50 provincias). Determinista, sin red.
Lee solo ficheros versionados de data/raw y output/v5/A4. Ceuta y Melilla se excluyen (sin A4 completo, sin SERPAVI
ni F-completa en 2015; ver desviaciones.md)."""
from __future__ import annotations

import re
import unicodedata
from pathlib import Path

import numpy as np
import pandas as pd

RAIZ = Path(__file__).resolve().parents[2]
RAW = RAIZ / "data/raw"
COSTA = {"03", "04", "07", "08", "12", "15", "17", "18", "20", "21", "29", "30", "33", "35", "36", "38", "39",
         "27", "43", "46", "48", "51", "52"}   # clasificación geográfica de src/v2/bi_core.py (repo); Ceuta/Melilla fuera de muestra
ISLA = {"07", "35", "38"}
GRANDES = {"28", "08", "07", "35", "38"}      # Madrid, Barcelona, Baleares, Canarias (multiverso)
SECT = ["Agricultura", "Industria", "Construcción", "Servicios"]


def key(s: str) -> str:
    s = unicodedata.normalize("NFKD", str(s)).encode("ascii", "ignore").decode().lower()
    return re.sub(r"[^a-z0-9/]", "", s)


def provincias() -> pd.DataFrame:
    a = pd.read_csv(RAIZ / "output/v5/A4/clasificacion_provincias.csv", dtype={"cod_prov": str})
    a = a[~a.cod_prov.isin(["51", "52"])].copy()
    return a


def mapa_nombres(a: pd.DataFrame) -> dict:
    m = {key(n): c for c, n in zip(a.cod_prov, a.provincia)}
    alias = {"15": ["Coruña (A)", "A Coruña", "Coruña, A"], "35": ["Palmas (Las)", "Las Palmas", "Palmas, Las"],
             "07": ["Balears (Illes)", "Illes Balears", "Balears, Illes"], "26": ["Rioja (La)", "La Rioja", "Rioja, La"],
             "01": ["Araba/Alava", "Araba / Álava"], "33": ["Asturias (Principado de )", "Principado de Asturias"],
             "28": ["Madrid (Comunidad de)", "Comunidad de Madrid"], "30": ["Murcia (Región de)", "Región de Murcia"],
             "31": ["Navarra (Com. Foral de)", "Navarra (Comunidad Foral de)", "C. Foral de Navarra"],
             "03": ["Alicante / Alacant"], "12": ["Castellón / Castelló"], "46": ["Valencia / València"]}
    extra = {key(n): c for c, ns in alias.items() for n in ns}
    m.update(extra)
    return m


def cod_de(nombre, m):
    return m.get(key(nombre))


def lee_tasado(a, m):
    t = pd.read_csv(RAW / "mivau_valor_tasado_nacional_ccaa_prov.csv")
    uni = {"07", "26", "28", "30", "31", "33", "39"}
    t["cod"] = [cod_de(x, m) for x in t.territorio]
    t = t[((t.nivel == "provincia")) | ((t.nivel == "ccaa") & t.cod.isin(uni))].dropna(subset=["cod"])
    t["anio"] = t.periodo.str[:4].astype(int)
    t = t.drop_duplicates(["cod", "periodo"])      # Navarra figura con dos rótulos en 2015-2018
    g = t.groupby(["cod", "anio"]).valor.agg(["mean", "count"]).reset_index()
    g = g[g["count"] == 4]
    return g.pivot(index="cod", columns="anio", values="mean")


def lee_registradores(m):
    r = pd.read_csv(RAW / "pdf/registradores_opendata_anual.csv")
    r = r[(r.nivel == "provincia") & (r.serie == "compraventas_viv_pm2")].copy()
    r["cod"] = [cod_de(x, m) for x in r.territorio]
    return r.dropna(subset=["cod"]).pivot(index="cod", columns="periodo", values="valor")


def lee_epa(m):
    s = pd.read_csv(RAW / "v5/ine_r1c_t65354.csv")
    s["terr"] = s.nombre.str.split(".").str[0]
    s["sector"] = s.nombre.str.split(".").str[3].str.strip()
    s["cod"] = [cod_de(x, m) for x in s.terr]
    s = s[s.sector.isin(SECT)].dropna(subset=["cod"])
    s["anio"] = s.periodo.str[:4].astype(int)
    s["q"] = s.periodo.str[5:].astype(int)
    g = s.groupby(["cod", "sector", "anio"]).valor.agg(["mean", "count"]).reset_index()
    return g[g["count"] == 4]


def bartik(epa, anio_w, a0, a1, cods):
    """Bartik: pesos sectoriales del año anio_w x crecimiento log nacional leave-one-out del sector entre a0 y a1."""
    E = epa.pivot_table(index=["cod", "sector"], columns="anio", values="mean")
    out = {}
    nat = E.groupby(level="sector").sum()
    for c in cods:
        w = E.loc[c][anio_w]
        w = w / w.sum()
        e0, e1 = E.loc[c][a0], E.loc[c][a1]
        g = np.log((nat[a1] - e1) / (nat[a0] - e0))
        out[c] = float((w.reindex(SECT) * g.reindex(SECT)).sum())
    return pd.Series(out)


def serpavi(m, a0, a1):
    d = pd.read_csv(RAW / "pdf/serpavi_v2_municipios.csv.gz", usecols=["periodo", "codigo", "provincia_codigo", "tipologia", "variable", "estadistico", "valor"])
    d = d[(d.tipologia == "VC") & (d.periodo.isin([a0, a1]))]
    r = d[(d.variable == "alquiler_m2") & (d.estadistico == "mediana")].pivot(index=["provincia_codigo", "codigo"], columns="periodo", values="valor")
    w = d[(d.variable == "n_contratos")].pivot(index=["provincia_codigo", "codigo"], columns="periodo", values="valor")[a0]
    r = r.dropna()
    r["w"] = w.reindex(r.index).fillna(1.0).values
    r["dl"] = np.log(r[a1]) - np.log(r[a0])
    r = r.reset_index()
    g = r.groupby("provincia_codigo").apply(lambda x: pd.Series({"dl": np.average(x.dl, weights=x.w), "nmun": len(x)}), include_groups=False)
    g.index = [f"{int(i):02d}" for i in g.index]
    return g


def lee_ipva(a0, a1):
    i = pd.read_csv(RAW / "ine_v2_ipva.csv")
    i = i[(i.nivel == "provincia") & (i.medida == "IPVA_indice") & (i.desglose == "Total")]
    i["cod"] = i.codigo.astype(int).map(lambda v: f"{v:02d}")
    p = i.pivot_table(index="cod", columns="periodo", values="valor", aggfunc="mean")
    return np.log(p[a1]) - np.log(p[a0])


def construir():
    a = provincias()
    m = mapa_nombres(a)
    cods = list(a.cod_prov)
    D = pd.DataFrame(index=pd.Index(cods, name="cod"))
    D["provincia"] = a.set_index("cod_prov").provincia
    meta = {}
    # ---- Y1
    T = lee_tasado(a, m)
    R = lee_registradores(m)
    for nom, S in (("t", T), ("r", R)):
        for y in (2015, 2021, 2025):
            D[f"p{nom}{y}"] = S[y].reindex(cods)
    # ---- población
    pp = pd.read_csv(RAW / "ine_v2_padron_prov_pais.csv")
    pp = pp[(pp.nivel == "provincia") & pp.desglose.isin(["nacionalidad=Total", "nacionalidad=Extranjera"])].copy()
    pp["cod"] = pp.codigo.astype(int).map(lambda v: f"{v:02d}")
    pp["anio"] = pp.periodo.str[:4].astype(int)
    pob = pp.pivot_table(index="cod", columns=["desglose", "anio"], values="valor")
    for y in (2015, 2021, 2023, 2025):
        D[f"pob{y}"] = pob[("nacionalidad=Total", y)].reindex(cods)
        D[f"ext{y}"] = pob[("nacionalidad=Extranjera", y)].reindex(cods)
    # ---- CRE (PIB corrientes) -> año común último con las 50 provincias
    c = pd.read_csv(RAW / "ine_v2_cre.csv")
    c = c[c.nivel == "provincia"].copy()
    c["cod"] = c.codigo.astype(int).map(lambda v: f"{v:02d}")
    pib = c.pivot_table(index="cod", columns="periodo", values="valor")
    full = [y for y in pib.columns if pib.loc[pib.index.isin(cods), y].notna().sum() == 50]
    ycre = max(full)
    meta["ycre"] = int(ycre)
    for y in (2015, 2021, ycre):
        D[f"pib{y}"] = pib[y].reindex(cods)
    pobycre = pob[("nacionalidad=Total", ycre)].reindex(cods) if ycre in pob.columns.get_level_values(1) else None
    if ycre not in (2015, 2021, 2023, 2025):
        D[f"pob{ycre}"] = pobycre
    # ---- hipotecas nº (suma anual 2015)
    h = pd.read_csv(RAW / "ine_v2_hipotecas_prov.csv")
    h = h[(h.nivel == "provincia") & (h.medida == "hipotecas_viviendas_numero")].copy()
    h["cod"] = h.codigo.astype(int).map(lambda v: f"{v:02d}")
    h["anio"] = h.periodo.str[:4].astype(int)
    hh = h.groupby(["cod", "anio"]).valor.agg(["sum", "count"]).reset_index()
    hh = hh[hh["count"] == 12].pivot(index="cod", columns="anio", values="sum")
    D["hip2015"] = hh[2015].reindex(cods)
    D["hip2021"] = hh[2021].reindex(cods)
    # ---- VUT 2021 (media feb y ago) y viviendas Censo 2021
    v = pd.read_csv(RAW / "ine_v2_vut.csv")
    v = v[(v.nivel == "provincia") & (v.medida == "viviendas_turisticas") & v.periodo.isin(["2021M02", "2021M08"])].copy()
    v["cod"] = v.codigo.astype(int).map(lambda x: f"{x:02d}")
    D["vut2021"] = v.groupby("cod").valor.mean().reindex(cods)
    cv = pd.read_csv(RAW / "v3/ine_v3_censo2021_municipio_viviendas.csv", dtype={"codigo": str})
    cv = cv[(cv.nivel == "municipio") & (cv.serie == "V_TOTAL")].copy()
    cv["cod"] = cv.codigo.str[:2]
    D["viv2021"] = cv.groupby("cod").valor.sum().reindex(cods)
    # ---- A4
    a4 = a.set_index("cod_prov")
    D["brecha"] = ((a4.brecha_cmin + a4.brecha_cmax) / 2).reindex(cods)
    D["clase1"] = (a4.clase_2021_2025 == 1).astype(float).reindex(cods)
    D["resp_oferta"] = a4.resp_oferta.reindex(cods)
    # ---- Bartik
    epa = lee_epa(m)
    for lab, (a0, a1) in {"P1": (2015, 2025), "P2": (2021, 2025)}.items():
        for w in (2015, 2011):
            D[f"bartik_{lab}_w{w}"] = bartik(epa, w, a0, a1, cods)
    # ---- Y2
    for lab, (a0, a1) in {"P1": (2015, 2024), "P2": (2021, 2024)}.items():
        s = serpavi(m, a0, a1)
        D[f"y2_{lab}"] = s.dl.reindex(cods)
        D[f"y2n_{lab}"] = s.nmun.reindex(cods)
        D[f"y2i_{lab}"] = lee_ipva(a0, a1).reindex(cods)
    # ---- geografía
    cm = pd.read_csv(RAW / "v5/municipio_centroides_utm30.csv", dtype={"codigo": str})
    cm["cod"] = cm.codigo.str[:2]
    wx = cm.groupby("cod").apply(lambda x: pd.Series({"x_km": np.average(x.x_m, weights=x.n_secciones) / 1000,
                                                      "y_km": np.average(x.y_m, weights=x.n_secciones) / 1000}), include_groups=False)
    D["x_km"] = wx.x_km.reindex(cods)
    D["y_km"] = wx.y_km.reindex(cods)
    D["costa"] = [float(c in COSTA) for c in cods]
    D["isla"] = [float(c in ISLA) for c in cods]
    D["grande"] = [float(c in GRANDES) for c in cods]
    D.attrs.update(meta)
    D.attrs["T"], D.attrs["R"] = T, R
    return D, meta


def regresores(D, lab, w=2015, src="t"):
    """Familias de regresores (sin estandarizar) para el periodo lab = 'P1'/'P2'. Devuelve DataFrame y dict familia->columnas."""
    a0, a1 = (2015, 2025) if lab == "P1" else (2021, 2025)
    X = pd.DataFrame(index=D.index)
    X["F1_bartik"] = D[f"bartik_{lab}_w{w}"]
    X["F2_dlnpob"] = np.log(D[f"pob{a1}"] / D[f"pob{a0}"])
    X["F2_dext_pp"] = (D[f"ext{a1}"] / D[f"pob{a1}"] - D[f"ext{a0}"] / D[f"pob{a0}"]) * 100
    X["F3_vut_1000viv"] = D["vut2021"] / D["viv2021"] * 1000
    X["F4_brecha"] = D["brecha"]
    X["F4_clase1"] = D["clase1"]
    X["F4_resp_oferta"] = D["resp_oferta"]
    yc = D.attrs["ycre"]
    X["F5_lnpibpc0"] = np.log(D[f"pib{a0}"] / D[f"pob{a0}"])
    X["F5_dlnpibpc"] = np.log(D[f"pib{yc}"] / D[f"pob{yc}"]) - X["F5_lnpibpc0"]
    X["F6_lnp0"] = np.log(D[f"p{src}{a0}"])
    X["F7_hip_1000hab"] = np.log(D[f"hip{a0}"] / D[f"pob{a0}"] * 1000)
    X["F8_costa"] = D["costa"]
    X["F8_isla"] = D["isla"]
    fam = {}
    for c in X.columns:
        fam.setdefault(c.split("_")[0], []).append(c)
    return X, fam


def dependientes(D, lab, src="t"):
    a0, a1 = (2015, 2025) if lab == "P1" else (2021, 2025)
    yc = D.attrs["ycre"]
    S = D.attrs["T"] if src == "t" else D.attrs["R"]
    Y = pd.DataFrame(index=D.index)
    Y["Y1"] = np.log(D[f"p{src}{a1}"] / D[f"p{src}{a0}"])
    Y["Y2"] = D[f"y2_{lab}"]
    Y["Y2_ipva"] = D[f"y2i_{lab}"]
    # Y3 = esfuerzo (precio / renta): ventana a0 -> ycre (límite de la CRE provincial con las 50 provincias)
    dp = np.log(S[yc].reindex(D.index) / S[a0].reindex(D.index))
    dpib = np.log(D[f"pib{yc}"] / D[f"pob{yc}"]) - np.log(D[f"pib{a0}"] / D[f"pob{a0}"])
    Y["Y3"] = dp - dpib
    return Y
