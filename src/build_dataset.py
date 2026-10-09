#!/usr/bin/env python3
"""Construye data/processed a partir de data/raw (solo lectura de raw).

Salidas:
  data/processed/nacional_q.csv            trimestral nacional, 1995Q1+ (muestra base 2008Q1+)
  data/processed/panel_ccaa_q.csv          17 CCAA x trimestre (formato largo)
  data/processed/panel_ccaa_nacionalidad.csv  flujos de inmigracion CCAA x nacionalidad (59013, sin rellenar)
  data/processed/valencia.csv              territorio x trimestre x variable (formato largo)
  docs/diccionario_variables.md            generado por este script (no editar a mano)

Uso: make clean   (o python3 src/build_dataset.py)
"""
from __future__ import annotations

import re
import unicodedata
import warnings
from pathlib import Path

import numpy as np
import pandas as pd
from statsmodels.tsa.seasonal import STL

warnings.filterwarnings("ignore", category=pd.errors.PerformanceWarning)

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw"
PROC = ROOT / "data" / "processed"
DOCS = ROOT / "docs"

QIDX = pd.period_range("1995Q1", "2026Q4", freq="Q")
MUESTRA_INI = pd.Period("2008Q1", freq="Q")

# ----------------------------------------------------------------------------
# Lectura y utilidades
# ----------------------------------------------------------------------------

def read_raw(name: str, usecols: list[str] | None = None) -> pd.DataFrame:
    cols = usecols
    df = pd.read_csv(RAW / name, dtype=str, usecols=cols)
    if "valor" in df:
        df["valor"] = pd.to_numeric(df["valor"], errors="coerce")
    if "fecha" in df:
        df["fecha"] = pd.to_datetime(df["fecha"])
    return df


def slug(text: str) -> str:
    t = unicodedata.normalize("NFKD", str(text)).encode("ascii", "ignore").decode()
    return re.sub(r"[^a-z0-9]+", "_", t.lower()).strip("_")


def by_serie(df: pd.DataFrame, code: str) -> pd.Series:
    d = df.loc[df["serie"] == code, ["fecha", "valor"]].drop_duplicates("fecha", keep="last")
    if d.empty:
        raise ValueError(f"serie no encontrada: {code}")
    return pd.Series(d["valor"].values, index=pd.DatetimeIndex(d["fecha"])).sort_index()


def one(df: pd.DataFrame) -> pd.Series:
    if df["serie"].nunique() != 1:
        raise ValueError(f"se esperaba una sola serie y hay {df['serie'].nunique()}")
    return by_serie(df, df["serie"].iloc[0])


def add_geo(df: pd.DataFrame) -> pd.DataFrame:
    """Separa 'nombre' en territorio (geo) y resto (tail): 'Andalucía. General. Índice.'"""
    parts = df["nombre"].str.split(r"\. ", n=1, regex=True)
    df["geo"] = parts.str[0].map(lambda x: slug(x) if isinstance(x, str) else x)
    df["tail"] = parts.str[1]
    return df


DUP_NOTES: list[str] = []


def by_geo(df: pd.DataFrame, geo: str, tail: str) -> pd.Series:
    """Serie por territorio y resto del nombre. Si hay codigos duplicados con valores
    identicos (duplicado en origen), usa el primero y lo anota; si difieren, falla."""
    d = df[(df["geo"] == geo) & (df["tail"] == tail)]
    codes = list(d["serie"].unique())
    if not codes:
        raise ValueError(f"geo={geo} tail={tail}: sin series")
    ref = by_serie(d, codes[0])
    for c in codes[1:]:
        other = by_serie(d, c)
        if not (ref.index.equals(other.index) and np.allclose(ref.values, other.values, equal_nan=True)):
            raise ValueError(f"geo={geo} tail={tail}: series {codes} distintas")
        DUP_NOTES.append(f"{geo} / '{tail}': {codes} idénticas en origen; se usa {codes[0]}")
    return ref


def q_direct(s: pd.Series) -> pd.Series:
    """Series ya trimestral (o semestral/anual que cae en un trimestre): asigna su trimestre."""
    p = pd.PeriodIndex(pd.DatetimeIndex(s.index), freq="Q")
    out = pd.Series(s.values, index=p)
    out = out[~out.index.duplicated(keep="last")].sort_index()
    return out.reindex(QIDX)


def m_agg(s: pd.Series, how: str) -> pd.Series:
    """Mensual -> trimestral. Exige los 3 meses (si no, NaN). how='mean' o 'sum'."""
    p = pd.PeriodIndex(pd.DatetimeIndex(s.index), freq="M")
    m = pd.Series(s.values, index=p)
    m = m[~m.index.duplicated(keep="last")].sort_index()
    q = m.index.asfreq("Q")
    g = m.groupby(q)
    n = g.size()
    c = g.count()
    val = g.mean() if how == "mean" else g.sum()
    ok = (n == 3) & (c == 3)
    return val[ok].reindex(QIDX)


def m_end(s: pd.Series) -> pd.Series:
    """Stock mensual -> valor de fin de trimestre (mes 3, 6, 9, 12)."""
    p = pd.PeriodIndex(pd.DatetimeIndex(s.index), freq="M")
    m = pd.Series(s.values, index=p)
    m = m[~m.index.duplicated(keep="last")].sort_index()
    m = m[m.index.month % 3 == 0]
    return pd.Series(m.values, index=m.index.asfreq("Q")).reindex(QIDX)


def interp_loglin(s: pd.Series) -> tuple[pd.Series, pd.Series]:
    """Interpola en logaritmos entre observaciones (nunca fuera del rango observado).
    Devuelve (serie rellenada, flag booleano de filas interpoladas)."""
    obs = s.dropna().sort_index()
    flag = pd.Series(False, index=s.index)
    out = s.copy()
    if len(obs) < 2:
        return out, flag
    x = np.array([p.ordinal for p in obs.index], dtype=float)
    y = np.log(obs.values.astype(float))
    lo, hi = x.min(), x.max()
    for i, p in enumerate(s.index):
        if pd.isna(s.iloc[i]) and lo < p.ordinal < hi:
            out.iloc[i] = np.exp(np.interp(p.ordinal, x, y))
            flag.iloc[i] = True
    return out, flag


def stl_sa(s: pd.Series) -> pd.Series:
    """Desestacionalizacion STL(period=4, robust) sobre log, bloque contiguo mas largo.
    Salida en niveles: exp(log - estacional). Fuera del bloque: NaN."""
    v = s.dropna().sort_index()
    ords = np.array([p.ordinal for p in v.index])
    blocks, start = [], 0
    for i in range(1, len(ords) + 1):
        if i == len(ords) or ords[i] - ords[i - 1] != 1:
            blocks.append((start, i))
            start = i
    a, b = max(blocks, key=lambda t: t[1] - t[0])
    idx = v.index[a:b]
    y = np.log(v.values[a:b].astype(float))
    res = STL(y, period=4, robust=True).fit()
    out = pd.Series(np.nan, index=s.index)
    out.loc[idx] = np.exp(y - res.seasonal)
    return out


def mrr_q() -> tuple[pd.Series, pd.Series]:
    """Tipo MRR del BCE: escalonado diario (ultimo valor vigente, sin extrapolar tras la ultima
    fecha observada) y media trimestral de los dias. Flag: trimestre sin cambio de tipo."""
    r = read_raw("ecb_tipo_oficial.csv", ["fecha", "valor"]).dropna(subset=["valor"])
    r = r.drop_duplicates("fecha", keep="last").sort_values("fecha")
    fechas = pd.DatetimeIndex(r["fecha"])
    days = pd.date_range(fechas.min(), fechas.max(), freq="D")
    daily = pd.Series(r["valor"].values, index=fechas).reindex(days).ffill()
    q = pd.PeriodIndex(days, freq="Q")
    g = daily.groupby(q)
    mean = g.mean()
    cnt = g.count()
    full = pd.Series([(p.end_time.normalize() - p.start_time.normalize()).days + 1 for p in mean.index],
                     index=mean.index)
    mean = mean[cnt == full].reindex(QIDX)
    changes = pd.PeriodIndex(fechas, freq="Q").value_counts()
    sin_cambio = pd.Series([(p in mean.dropna().index) and (changes.get(p, 0) == 0) for p in QIDX],
                           index=QIDX)
    return mean, sin_cambio.astype(bool)


# ----------------------------------------------------------------------------
# Constantes CCAA
# ----------------------------------------------------------------------------

CCAA = [  # codigo INE, nombre normalizado, slug (INE/MIVAU)
    ("01", "Andalucía", "andalucia"),
    ("02", "Aragón", "aragon"),
    ("03", "Asturias", "asturias_principado_de"),
    ("04", "Illes Balears", "balears_illes"),
    ("05", "Canarias", "canarias"),
    ("06", "Cantabria", "cantabria"),
    ("07", "Castilla y León", "castilla_y_leon"),
    ("08", "Castilla-La Mancha", "castilla_la_mancha"),
    ("09", "Cataluña", "cataluna"),
    ("10", "Comunitat Valenciana", "comunitat_valenciana"),
    ("11", "Extremadura", "extremadura"),
    ("12", "Galicia", "galicia"),
    ("13", "Comunidad de Madrid", "madrid_comunidad_de"),
    ("14", "Región de Murcia", "murcia_region_de"),
    ("15", "Comunidad Foral de Navarra", "navarra_comunidad_foral_de"),
    ("16", "País Vasco", "pais_vasco"),
    ("17", "La Rioja", "rioja_la"),
]
# alias de slugs que aparecen en MIVAU
SLUG_ALIAS = {
    "asturias": "asturias_principado_de",
    "comunidad_valenciana": "comunitat_valenciana",
    "navarra_com_foral_de": "navarra_comunidad_foral_de",
    "navarra_c_foral_de": "navarra_comunidad_foral_de",
    "rioja_la": "rioja_la",
}
SLUG2COD = {sl: cod for cod, _, sl in CCAA}
SLUG2COD.update({k: SLUG2COD[v] for k, v in SLUG_ALIAS.items() if v in SLUG2COD})
COD2NAME = {cod: nm for cod, nm, _ in CCAA}
COD2SLUG = {cod: sl for cod, _, sl in CCAA}


def ccaa_from_slug(sl: str) -> str | None:
    sl = SLUG_ALIAS.get(sl, sl)
    return SLUG2COD.get(sl)


# ----------------------------------------------------------------------------
# Construccion de la base nacional (A)
# ----------------------------------------------------------------------------

LEVELS_POS = ["ipv", "ipv_nueva", "ipv_usada", "ipv15", "p_tasado", "p_bde", "hpi_eurostat",
              "ocupados", "ocupados_sa", "renta_hog", "deflactor", "renta_hog_real", "ipc_alquiler",
              "credito_nuevo", "credito_stock", "permisos", "costes", "prod_constr", "visados",
              "terminadas", "compraventas", "compraventas_sa", "trans_total", "trans_extranjeros",
              "pob_total", "pob_extranj", "hogares"]
RATES = ["tipo_hip", "euribor", "tipo_bce", "tipo_hip_real", "ipc_alquiler_yoy",
         "inflacion_deflactor"]
BASE_CHECK = LEVELS_POS + RATES + ["inmig_anual"]


def build_nacional() -> pd.DataFrame:
    d = pd.DataFrame(index=QIDX)

    ipv = add_geo(read_raw("ine_ipv_80270.csv", ["fecha", "serie", "valor", "nombre"]))
    d["ipv"] = q_direct(by_serie(ipv, "IPV1209"))
    d["ipv_nueva"] = q_direct(by_serie(ipv, "IPV1613"))
    d["ipv_usada"] = q_direct(by_serie(ipv, "IPV1618"))
    d["ipv15"] = q_direct(one(read_raw("ine_ipv_25171.csv", ["fecha", "serie", "valor"]).query("serie=='IPV769'")))

    d["p_tasado"] = q_direct(by_serie(
        read_raw("mivau_valor_tasado_nacional_ccaa_prov.csv", ["fecha", "serie", "valor"]),
        "valor_tasado_libre_nacional"))
    d["p_bde"] = q_direct(by_serie(read_raw("bde_precio_vivienda_libre.csv", ["fecha", "serie", "valor"]),
                                   "DHIVTNOAPLPMMUVT_RLI.T"))
    d["hpi_eurostat"] = q_direct(by_serie(read_raw("eurostat_hpi.csv", ["fecha", "serie", "valor"]),
                                          "Q|TOTAL|I15_Q|ES"))
    d["ocupados"] = q_direct(one(read_raw("ine_epa_ocupados.csv", ["fecha", "serie", "valor"])))
    d["renta_hog"] = q_direct(one(read_raw("eurostat_renta_hogares.csv", ["fecha", "serie", "valor"])))

    # Deflactor implicito del PIB: nominal NSA (CNTR6548) / volumen encadenado NSA (CNTR6721)
    nom = by_serie(read_raw("ine_cnt_pib_oferta_corrientes.csv", ["fecha", "serie", "valor"]), "CNTR6548")
    vol = by_serie(read_raw("ine_cnt_pib_oferta_volumen.csv", ["fecha", "serie", "valor"]), "CNTR6721")
    # Volumen encadenado con media anual 2020 = 100: el deflactor se normaliza a 2020 = 100
    ratio = nom / vol
    base_2020 = ratio[ratio.index.year == 2020].mean()
    d["deflactor"] = q_direct(100 * ratio / base_2020)
    d["renta_hog_real"] = d["renta_hog"] / d["deflactor"] * 100
    d["inflacion_deflactor"] = (d["deflactor"] / d["deflactor"].shift(4) - 1) * 100

    d["tipo_hip"] = m_agg(one(read_raw("ecb_tipo_hipotecario_es.csv", ["fecha", "serie", "valor"])), "mean")
    d["euribor"] = m_agg(one(read_raw("ecb_euribor1y.csv", ["fecha", "serie", "valor"])), "mean")
    tipo_bce, bce_sin_cambio = mrr_q()
    d["tipo_bce"] = tipo_bce
    d["tipo_bce_interp"] = bce_sin_cambio & tipo_bce.notna()
    d["tipo_hip_real"] = d["tipo_hip"] - d["inflacion_deflactor"]

    ipc = add_geo(read_raw("ine_ipc_alquiler.csv", ["fecha", "serie", "valor", "nombre"]))
    d["ipc_alquiler"] = m_agg(by_serie(ipc, "IPC290887"), "mean")
    d["ipc_alquiler_yoy"] = m_agg(by_serie(ipc, "IPC290886"), "mean")

    d["credito_nuevo"] = m_agg(one(read_raw("ecb_nuevo_credito_vivienda_es.csv", ["fecha", "serie", "valor"])), "sum")
    d["credito_stock"] = m_end(one(read_raw("ecb_stock_credito_vivienda_es.csv", ["fecha", "serie", "valor"])))

    d["permisos"] = q_direct(one(read_raw("eurostat_permisos.csv", ["fecha", "serie", "valor"])))
    d["costes"] = q_direct(one(read_raw("eurostat_costes.csv", ["fecha", "serie", "valor"])))
    d["prod_constr"] = q_direct(one(read_raw("eurostat_produccion_construccion.csv", ["fecha", "serie", "valor"])))

    d["visados"] = m_agg(by_serie(read_raw("mivau_visados.csv", ["fecha", "serie", "valor"]),
                                  "viv_libres_iniciadas_nacional"), "sum")
    d["terminadas"] = m_agg(by_serie(read_raw("mivau_fin_obra.csv", ["fecha", "serie", "valor"]),
                                     "viv_libres_terminadas_nacional"), "sum")

    ine_etdp = read_raw("ine_etdp_compraventas.csv", ["fecha", "serie", "valor", "nombre"])
    ine_etdp = add_geo(ine_etdp)
    d["compraventas"] = m_agg(by_serie(ine_etdp, "ETDP1826"), "sum")  # Total Nacional. General. Compraventa.

    d["trans_total"] = q_direct(by_serie(read_raw("mivau_transacciones_total.csv", ["fecha", "serie", "valor"]),
                                         "tx_total_nacional"))
    d["trans_extranjeros"] = q_direct(by_serie(
        read_raw("mivau_transacciones_extranjeros.csv", ["fecha", "serie", "valor"]),
        "tx_extranj_residentes_total_nacional"))

    ecp = read_raw("ine_ecp_nacional.csv", ["fecha", "serie", "valor"])
    pob_t, f_t = interp_loglin(q_direct(by_serie(ecp, "ECP320")))
    pob_e, f_e = interp_loglin(q_direct(by_serie(ecp, "ECP701")))
    d["pob_total"], d["pob_total_interp"] = pob_t, f_t
    d["pob_extranj"], d["pob_extranj_interp"] = pob_e, f_e

    d["hogares"] = q_direct(by_serie(read_raw("ine_hogares_60131.csv", ["fecha", "serie", "valor"]),
                                     "ECP355533"))

    mig = read_raw("ine_migraciones_total_anual.csv", ["fecha", "serie", "valor", "nombre"])
    mig_serie = mig.loc[mig["nombre"] == "Todas las edades. Total. Dato base. Inmigraciones procedentes del extranjero.", "serie"].unique()
    assert len(mig_serie) == 1
    anual = by_serie(mig, mig_serie[0])
    inmig = pd.Series(np.nan, index=QIDX)
    for dt, v in anual.items():  # valor anual asignado solo al primer trimestre del año
        inmig[pd.Period(dt, freq="Q")] = v
    d["inmig_anual"] = inmig

    # Desestacionalizacion (solo ocupados y compraventas)
    d["ocupados_sa"] = stl_sa(d["ocupados"])
    d["compraventas_sa"] = stl_sa(d["compraventas"])

    # Recorte de filas finales totalmente vacias
    base = [c for c in BASE_CHECK if c in d.columns]
    last = d[base].notna().any(axis=1)
    last_q = last[last].index.max()
    d = d.loc[:last_q].copy()
    d.index.name = "trimestre"
    return d


def add_transforms(d: pd.DataFrame, levels: list[str], rates: list[str]) -> pd.DataFrame:
    for v in levels:
        if v not in d:
            continue
        x = d[v].where(d[v] > 0)
        ln = np.log(x)
        d[f"ln_{v}"] = ln
        d[f"d_ln_{v}"] = ln.diff()
        d[f"d4_ln_{v}"] = ln.diff(4)
    for v in rates:
        if v in d:
            d[f"d_{v}"] = d[v].diff()
    return d


def finalize_nacional(d: pd.DataFrame) -> pd.DataFrame:
    d = add_transforms(d, LEVELS_POS, RATES)
    out = pd.DataFrame(index=d.index)
    out["fecha"] = d.index.to_timestamp(how="start").strftime("%Y-%m-%d")
    cols_levels = [c for c in ["ipv", "ipv_nueva", "ipv_usada", "ipv15", "p_tasado", "p_bde", "hpi_eurostat",
                               "ocupados", "ocupados_sa", "renta_hog", "deflactor", "renta_hog_real",
                               "ipc_alquiler", "ipc_alquiler_yoy", "credito_nuevo", "credito_stock",
                               "permisos", "costes", "prod_constr", "visados", "terminadas",
                               "compraventas", "compraventas_sa", "trans_total", "trans_extranjeros",
                               "pob_total", "pob_extranj", "hogares", "tipo_hip", "euribor", "tipo_bce",
                               "tipo_hip_real", "inflacion_deflactor", "inmig_anual"]]
    cols_ln = [f"{p}{v}" for v in LEVELS_POS if v in d for p in ("ln_", "d_ln_", "d4_ln_")]
    cols_d = [f"d_{v}" for v in RATES]
    flags = ["pob_total_interp", "pob_extranj_interp", "tipo_bce_interp"]
    for c in cols_levels + cols_ln + cols_d:
        if c in d:
            out[c] = d[c]
    # ipc_alquiler_yoy ya esta en cols_levels (tipo %); su diferencia se llama d_ipc_alquiler_yoy
    for f in flags:
        out[f] = d[f].astype(bool)
    out["muestra_base"] = False
    last_ipv = d["ipv"].dropna().index.max()
    out["muestra_base"] = [(p >= MUESTRA_INI) and (p <= last_ipv) for p in d.index]
    for k in range(1, 5):
        out[f"q{k}"] = [int(p.quarter == k) for p in d.index]
    out.insert(0, "trimestre", [str(p) for p in d.index])
    out = out.reset_index(drop=True)
    return out


# ----------------------------------------------------------------------------
# Panel CCAA (B) y nacionalidad (B2)
# ----------------------------------------------------------------------------

def _is_epa_total(nombre: str, sl: str) -> bool:
    """Total de ocupados (ambos sexos, todas las edades) de una CCAA. El orden de las
    palabras varía en el origen ('Ambos sexos. Andalucía. Ocupados. Total.')."""
    parts = {slug(x) for x in str(nombre).split(". ")}
    return {"ambos_sexos", "total", "ocupados", sl} <= parts


def build_panel() -> pd.DataFrame:
    ipv = add_geo(read_raw("ine_ipv_80270.csv", ["fecha", "serie", "valor", "nombre"]))
    epa = add_geo(read_raw("ine_epa_ocupados_ccaa.csv", ["fecha", "serie", "valor", "nombre"]))
    etdp = add_geo(read_raw("ine_etdp_compraventas.csv", ["fecha", "serie", "valor", "nombre"]))
    ipc = add_geo(read_raw("ine_ipc_alquiler.csv", ["fecha", "serie", "valor", "nombre"]))
    tas = read_raw("mivau_valor_tasado_nacional_ccaa_prov.csv", ["fecha", "serie", "valor", "nivel"])
    tx_t = read_raw("mivau_transacciones_total.csv", ["fecha", "serie", "valor"])
    tx_e = read_raw("mivau_transacciones_extranjeros.csv", ["fecha", "serie", "valor"])
    vis = read_raw("mivau_visados.csv", ["fecha", "serie", "valor"])
    fin = read_raw("mivau_fin_obra.csv", ["fecha", "serie", "valor"])

    def mivau_ccaa(df: pd.DataFrame, prefix: str) -> dict[str, pd.Series]:
        """Serie MIVAU por CCAA. Si hay alias de nombre (p. ej. Navarra), usa el de mas datos."""
        cands: dict[str, list[str]] = {}
        for sid in df["serie"].unique():
            m = re.match(rf"^{prefix}_ccaa_(.+)$", sid)
            if m and ccaa_from_slug(m.group(1)):
                cands.setdefault(ccaa_from_slug(m.group(1)), []).append(sid)
        out = {}
        for cod, sids in cands.items():
            best = max(sids, key=lambda x: by_serie(df, x).notna().sum())
            out[cod] = by_serie(df, best)
            if len(sids) > 1:
                DUP_NOTES.append(f"MIVAU CCAA {cod} ({prefix}): alias {sids}; se usa '{best}' (más observaciones)")
        return out

    tas_c = mivau_ccaa(tas, "valor_tasado_libre")
    txt_c = mivau_ccaa(tx_t, "tx_total")
    txe_c = mivau_ccaa(tx_e, "tx_extranj_residentes_total")
    vis_c = mivau_ccaa(vis, "viv_libres_iniciadas")
    fin_c = mivau_ccaa(fin, "viv_libres_terminadas")

    frames = []
    for cod, nombre, sl in CCAA:
        d = pd.DataFrame(index=QIDX)
        d["ccaa"] = nombre
        d["codigo_ine_ccaa"] = cod
        d["ipv"] = q_direct(by_geo(ipv, sl, "General. Índice."))
        d["ipv_nueva"] = q_direct(by_geo(ipv, sl, "Vivienda nueva. Índice."))
        d["ipv_usada"] = q_direct(by_geo(ipv, sl, "Vivienda segunda mano. Índice."))
        d["p_tasado"] = q_direct(tas_c[cod]) if cod in tas_c else np.nan
        d["ocupados"] = q_direct(one(epa[epa["nombre"].map(lambda t: _is_epa_total(t, sl))]))
        d["compraventas"] = m_agg(by_geo(etdp, sl, "General. Compraventa. Número."), "sum")
        d["trans_total"] = q_direct(txt_c[cod]) if cod in txt_c else np.nan
        d["trans_extranjeros"] = q_direct(txe_c[cod]) if cod in txe_c else np.nan
        d["visados"] = m_agg(vis_c[cod], "sum") if cod in vis_c else np.nan
        d["terminadas"] = m_agg(fin_c[cod], "sum") if cod in fin_c else np.nan
        d["ipc_alquiler"] = m_agg(by_geo(ipc, sl, "Alquiler de vivienda. Índice."), "mean")
        frames.append(d)
    panel = pd.concat(frames, keys=[c for c, _, _ in CCAA], names=["cod", "trimestre"]).reset_index(level=0, drop=True)
    panel = panel.reset_index()
    panel["trimestre"] = panel["trimestre"].astype(str)
    return panel


PANEL_LEVELS = ["ipv", "ipv_nueva", "ipv_usada", "p_tasado", "ocupados", "compraventas",
                "trans_total", "trans_extranjeros", "visados", "terminadas", "ipc_alquiler"]


def finalize_panel(panel: pd.DataFrame) -> pd.DataFrame:
    panel = panel.copy()
    # Recorte global de trimestres finales vacios
    base = [c for c in PANEL_LEVELS if c in panel]
    has = panel.groupby("trimestre")[base].apply(lambda g: g.notna().any().any())
    last = has[has].index.max()
    panel = panel[panel["trimestre"] <= last].copy()
    panel = panel.sort_values(["codigo_ine_ccaa", "trimestre"]).reset_index(drop=True)
    for v in PANEL_LEVELS:
        if v not in panel or panel[v].isna().all():
            continue
        x = panel[v].where(panel[v] > 0)
        ln = np.log(x)
        panel[f"ln_{v}"] = ln
        g = ln.groupby(panel["codigo_ine_ccaa"])
        panel[f"d_ln_{v}"] = g.diff()
        panel[f"d4_ln_{v}"] = g.diff(4)
    panel["fecha"] = [pd.Period(t, freq="Q").start_time.strftime("%Y-%m-%d") for t in panel["trimestre"]]
    cols = ["ccaa", "codigo_ine_ccaa", "trimestre", "fecha"]
    rest = [c for c in panel.columns if c not in cols]
    return panel[cols + rest]


def build_nacionalidad() -> pd.DataFrame:
    """Flujos de inmigracion 59013 por CCAA x nacionalidad (solo celdas con valor)."""
    df = add_geo(read_raw("ine_migraciones_ccaa_nacionalidad.csv", ["fecha", "serie", "valor", "nombre"]))
    df = df[df["geo"].isin(list(SLUG2COD.keys()))].copy()
    df = df[df["valor"].notna()].copy()
    df["codigo_ine_ccaa"] = df["geo"].map(ccaa_from_slug)
    df = df[df["codigo_ine_ccaa"].notna()].copy()
    df["ccaa"] = df["codigo_ine_ccaa"].map(COD2NAME)
    df["nacionalidad"] = df["tail"].str.split(r"\. ", n=1, regex=True).str[0]
    df["trimestre"] = pd.PeriodIndex(df["fecha"], freq="Q").astype(str)
    df = df.rename(columns={"valor": "inmig_flujo", "serie": "serie_ine"})
    out = df[["ccaa", "codigo_ine_ccaa", "nacionalidad", "trimestre", "fecha", "inmig_flujo", "serie_ine"]]
    return out.sort_values(["codigo_ine_ccaa", "nacionalidad", "trimestre"]).reset_index(drop=True)


# ----------------------------------------------------------------------------
# Valencia (C)
# ----------------------------------------------------------------------------

VAL_SRC: dict[tuple[str, str], str] = {}


def build_valencia() -> pd.DataFrame:
    rows = []

    def add(terr: str, var: str, s: pd.Series, src: str):
        q = q_direct(s).dropna()
        VAL_SRC[(terr, var)] = src
        for p, v in q.items():
            rows.append((terr, str(p), var, v))

    tas_m = read_raw("mivau_valor_tasado_municipios.csv", ["fecha", "serie", "valor"])
    tas = read_raw("mivau_valor_tasado_nacional_ccaa_prov.csv", ["fecha", "serie", "valor"])
    tx_m = read_raw("mivau_transacciones_municipios.csv", ["fecha", "serie", "valor"])
    tx_t = read_raw("mivau_transacciones_total.csv", ["fecha", "serie", "valor"])
    tx_e = read_raw("mivau_transacciones_extranjeros.csv", ["fecha", "serie", "valor"])
    ipv = read_raw("ine_ipv_80270.csv", ["fecha", "serie", "valor", "nombre"])
    ipv = add_geo(ipv)
    vut = read_raw("ine_vut_valencia_municipio.csv", ["fecha", "serie", "valor"])
    ipva = add_geo(read_raw("ine_ipva_municipal.csv", ["fecha", "serie", "valor", "nombre"]))

    V = "València (municipio)"
    P = "Provincia de València"
    C = "Comunitat Valenciana"
    E = "España"
    add(V, "p_tasado", by_serie(tas_m, "valor_tasado_mun_valencia"), "mivau_valor_tasado_municipios.csv | valor_tasado_mun_valencia")
    add(P, "p_tasado", by_serie(tas, "valor_tasado_libre_provincia_valencia_valencia"), "mivau_valor_tasado_nacional_ccaa_prov.csv | valor_tasado_libre_provincia_valencia_valencia")
    add(C, "p_tasado", by_serie(tas, "valor_tasado_libre_ccaa_comunidad_valenciana"), "mivau_valor_tasado_nacional_ccaa_prov.csv | valor_tasado_libre_ccaa_comunidad_valenciana")
    add(E, "p_tasado", by_serie(tas, "valor_tasado_libre_nacional"), "mivau_valor_tasado_nacional_ccaa_prov.csv | valor_tasado_libre_nacional")
    add(V, "trans_total", by_serie(tx_m, "tx_municipio_valencia"), "mivau_transacciones_municipios.csv | tx_municipio_valencia")
    add(C, "trans_total", by_serie(tx_t, "tx_total_ccaa_comunitat_valenciana"), "mivau_transacciones_total.csv | tx_total_ccaa_comunitat_valenciana")
    add(E, "trans_total", by_serie(tx_t, "tx_total_nacional"), "mivau_transacciones_total.csv | tx_total_nacional")
    add(C, "trans_extranjeros", by_serie(tx_e, "tx_extranj_residentes_total_ccaa_comunitat_valenciana"), "mivau_transacciones_extranjeros.csv | tx_extranj_residentes_total_ccaa_comunitat_valenciana")
    add(E, "trans_extranjeros", by_serie(tx_e, "tx_extranj_residentes_total_nacional"), "mivau_transacciones_extranjeros.csv | tx_extranj_residentes_total_nacional")
    add(C, "ipv", by_geo(ipv, "comunitat_valenciana", "General. Índice."), "ine_ipv_80270.csv | IPV1392 (Comunitat Valenciana. General. Índice.)")
    add(E, "ipv", by_geo(ipv, "nacional", "General. Índice."), "ine_ipv_80270.csv | IPV1209 (Nacional. General. Índice.)")
    for code, var in [("ine_vut_valencia_valencia_viviendas_turisticas", "vut_viviendas_turisticas"),
                      ("ine_vut_valencia_valencia_plazas", "vut_plazas"),
                      ("ine_vut_valencia_valencia_plazas_por_vivienda", "vut_plazas_por_vivienda"),
                      ("ine_vut_valencia_valencia_pct_viv_turisticas_sobre_total", "vut_pct_sobre_total")]:
        add(V, var, by_serie(vut, code), f"ine_vut_valencia_municipio.csv | {code}")  # semestral: Feb -> T1, Ago -> T3; sin interpolar
    add(V, "ipva", by_geo(ipva, "valencia", "Índice. Total."), "ine_ipva_municipal.csv | IPVA8471 (Valencia. Índice. Total.)")  # anual: enero -> T1; sin interpolar
    out = pd.DataFrame(rows, columns=["territorio", "trimestre", "variable", "valor"])
    return out.sort_values(["territorio", "variable", "trimestre"]).reset_index(drop=True)


# ----------------------------------------------------------------------------
# Diccionario y comprobaciones
# ----------------------------------------------------------------------------

META_NAC = [
    # var, fuente, archivo raw, código/serie, unidad, frecuencia original, agregación
    ("ipv", "INE IPV, tabla 80270", "ine_ipv_80270.csv", "IPV1209 (Nacional. General. Índice.)", "índice", "trimestral (2007T1+)", "nativo"),
    ("ipv_nueva", "INE IPV, tabla 80270", "ine_ipv_80270.csv", "IPV1613 (Vivienda nueva. Índice.)", "índice", "trimestral (2007T1+)", "nativo"),
    ("ipv_usada", "INE IPV, tabla 80270", "ine_ipv_80270.csv", "IPV1618 (Vivienda segunda mano. Índice.)", "índice", "trimestral (2007T1+)", "nativo"),
    ("ipv15", "INE IPV, tabla 25171 (base 2015, robustez)", "ine_ipv_25171.csv", "IPV769 (Nacional. General. Índice.)", "índice", "trimestral (2007T1-2025T4)", "nativo"),
    ("p_tasado", "MIVAU, Boletín (tabla 35101000)", "mivau_valor_tasado_nacional_ccaa_prov.csv", "valor_tasado_libre_nacional", "€/m2", "trimestral (1995T1+)", "nativo"),
    ("p_bde", "Banco de España, be2507", "bde_precio_vivienda_libre.csv", "DHIVTNOAPLPMMUVT_RLI.T (total nacional)", "€/m2", "trimestral (fecha = mes de cierre)", "nativo"),
    ("hpi_eurostat", "Eurostat prc_hpi_q", "eurostat_hpi.csv", "Q|TOTAL|I15_Q|ES", "índice 2015=100", "trimestral (2005T4+)", "nativo"),
    ("ocupados", "INE EPA, tabla 65302 / EPA387796", "ine_epa_ocupados.csv", "EPA387796 (Total Nacional. Ambos sexos. Total. Ocupados.)", "miles de personas (NSA)", "trimestral (2002T1+)", "nativo"),
    ("ocupados_sa", "Derivada (STL)", "ine_epa_ocupados.csv", "EPA387796", "miles (SA)", "trimestral", "STL(period=4, robust=True) sobre log; nivel = exp(log - estacional)"),
    ("renta_hog", "Eurostat nasq_10_nf_tr", "eurostat_renta_hogares.csv", "Q|CP_MEUR|RECV|S14_S15|B6G|SCA|ES", "M€ corrientes (SCA)", "trimestral (1999T1+)", "nativo"),
    ("deflactor", "Derivada: INE CNT", "ine_cnt_pib_oferta_corrientes.csv / ine_cnt_pib_oferta_volumen.csv", "CNTR6548 (PIB mercado, corrientes, NSA) / CNTR6721 (PIB mercado, volumen encadenado, NSA)", "índice 2020=100", "trimestral (1995T1+)", "cociente nominal/volumen, reescalado a media 2020 = 100"),
    ("renta_hog_real", "Derivada", "eurostat_renta_hogares.csv + INE CNT", "renta_hog / deflactor x 100", "M€ a precios de 2020", "trimestral", "cociente"),
    ("tipo_hip", "BCE MIR, nuevas operaciones vivienda", "ecb_tipo_hipotecario_es.csv", "MIR.M.ES.B.A2C.AM.R.A.2250.EUR.N", "% anual", "mensual (2003-01+)", "media de 3 meses (exige 3)"),
    ("euribor", "BCE, Euribor 1 año", "ecb_euribor1y.csv", "FM.M.U2.EUR.RT.MM.EURIBOR1YD_.HSTA", "% anual", "mensual (1994-01+)", "media de 3 meses"),
    ("tipo_bce", "BCE, tipo MRR (operaciones principales)", "ecb_tipo_oficial.csv", "FM.B.U2.EUR.4F.KR.MRR_FR.LEV", "% anual", "cambios de tipo (48 obs.)", "escalonado diario (último valor vigente hasta la última fecha observada) y media trimestral de días"),
    ("tipo_hip_real", "Derivada", "ecb_tipo_hipotecario_es.csv + INE CNT", "tipo_hip - inflacion_deflactor", "pp", "trimestral", "resta"),
    ("inflacion_deflactor", "Derivada", "INE CNT", "100 x (deflactor_t / deflactor_{t-4} - 1)", "% interanual", "trimestral", "tasa interanual exacta"),
    ("ipc_alquiler", "INE IPC, subclase alquiler de vivienda", "ine_ipc_alquiler.csv", "IPC290887 (Nacional. Alquiler de vivienda. Índice.)", "índice", "mensual (2002-01+)", "media de 3 meses"),
    ("ipc_alquiler_yoy", "INE IPC, subclase alquiler de vivienda", "ine_ipc_alquiler.csv", "IPC290886 (Variación anual)", "% interanual", "mensual (2002-01+)", "media de 3 meses"),
    ("credito_nuevo", "BCE MIR, nuevo crédito vivienda", "ecb_nuevo_credito_vivienda_es.csv", "MIR.M.ES.B.A2C.A.B.A.2250.EUR.N", "M€ (flujo)", "mensual (2003-01+)", "suma de 3 meses"),
    ("credito_stock", "BCE BSI, stock crédito vivienda", "ecb_stock_credito_vivienda_es.csv", "BSI.M.ES.N.A.A22.A.1.U2.2250.Z01.E", "M€ (stock)", "mensual (2003-01+)", "valor de fin de trimestre (mes 3)"),
    ("permisos", "Eurostat sts_cobp_q", "eurostat_permisos.csv", "Q|BPRM_DW|CPA_F41001_X_410014|SCA|I21|ES", "índice 2021=100 (SCA)", "trimestral (2000T1+)", "nativo"),
    ("costes", "Eurostat sts_copi_q", "eurostat_costes.csv", "Q|COST|CPA_F41001_X_410014|NSA|I21|ES", "índice 2021=100 (NSA)", "trimestral (1980T1+)", "nativo"),
    ("prod_constr", "Eurostat sts_copr_q", "eurostat_produccion_construccion.csv", "Q|PRD|F|SCA|I21|ES", "índice 2021=100 (SCA)", "trimestral (2005T1+)", "nativo"),
    ("visados", "MIVAU Boletín, tabla 32100500 (PROXY)", "mivau_visados.csv", "viv_libres_iniciadas_nacional", "viviendas (flujo)", "mensual (2008-01+)", "suma de 3 meses. Proxy: viviendas libres iniciadas MIVAU, no visados CSCAE"),
    ("terminadas", "MIVAU Boletín, tabla 32101000 (PROXY)", "mivau_fin_obra.csv", "viv_libres_terminadas_nacional", "viviendas (flujo)", "mensual (2008-01+)", "suma de 3 meses. Proxy: viviendas libres terminadas MIVAU, no certificados de fin de obra CSCAE"),
    ("compraventas", "INE ETDP, tabla 6150", "ine_etdp_compraventas.csv", "ETDP1826 (Total Nacional. General. Compraventa. Número.)", "número (flujo)", "mensual (2007-01+)", "suma de 3 meses"),
    ("compraventas_sa", "Derivada (STL)", "ine_etdp_compraventas.csv", "ETDP1826", "número (SA)", "trimestral", "STL(period=4, robust=True) sobre log; nivel = exp(log - estacional)"),
    ("trans_total", "MIVAU Boletín, tabla 34010110 (notarios)", "mivau_transacciones_total.csv", "tx_total_nacional", "transacciones (flujo)", "trimestral (2004T1+)", "nativo"),
    ("trans_extranjeros", "MIVAU Boletín, tabla 340101i0 / residentes extranjeros", "mivau_transacciones_extranjeros.csv", "tx_extranj_residentes_total_nacional", "transacciones (flujo)", "trimestral (2007T1+)", "nativo"),
    ("pob_total", "INE ECP, serie nacional", "ine_ecp_nacional.csv", "ECP320 (Total Nacional. Todas las edades. Total.)", "personas (a 1 de enero/julio, stock)", "semestral 1971-2020 (ene/jul); trimestral 2021+", "stock: trimestre de la fecha; trimestres intermedios interpolados"),
    ("pob_extranj", "INE ECP, serie nacional", "ine_ecp_nacional.csv", "ECP701 (Total Nacional. Extranjera. Todas las edades. Total.)", "personas (stock)", "semestral 2002-2020; trimestral 2021+", "como pob_total"),
    ("hogares", "INE ECP, tabla 60131", "ine_hogares_60131.csv", "ECP355533 (Total Nacional. Total. Hogares en viviendas familiares.)", "hogares (stock)", "trimestral (2021T1+)", "nativo; sin interpolación ni retropolación"),
    ("inmig_anual", "INE EMCR, tabla 69687 (ANUAL)", "ine_migraciones_total_anual.csv", "EM1765217 (Todas las edades. Total. Dato base. Inmigraciones procedentes del extranjero.)", "personas (flujo anual)", "anual (2021-2024)", "anual asignado solo al primer trimestre del año (no trimestralizar)"),
]

# Fuentes raw descargadas que no entran en nacional_q (motivo)
NO_USADAS = [
    ("bde_tipo_hipotecario_referencia.csv", "BdE D_1T9H0000 (tipo medio adquisición vivienda libre). Se usa el MIR del BCE según especificación."),
    ("ecb_hicp_es.csv", "IAPC España (ICP ANR), termina 2025-12. El deflactor del PIB se usa como inflación; no entra en nacional_q."),
    ("ine_cnt_demanda_corrientes.csv / ine_cnt_demanda_volumen.csv", "Mismo PIB a precios de mercado que la oferta; el deflactor usa ine_cnt_pib_oferta_*."),
    ("ine_cnt_renta_disponible.csv", "Serie 80333 es capacidad/necesidad de financiación, no renta de hogares."),
    ("eurostat_empleo_nuts2.csv, eurostat_inmigracion_anual.csv", "No especificados en la base; disponibles para trabajo posterior."),
    ("ine_migraciones_nacionalidad.csv (59011)", "No existe serie total: las 61 nacionalidades solo tienen dato en ~10 celdas por trimestre. Sumar daría cifras parciales; no se usa (inmig_q omitida)."),
    ("ine_ecp_56936.csv", "Población solo a nivel nacional por nacionalidad y edad (sin CCAA). Se usa solo para validar ECP701."),
    ("ine_ecp_59585.csv", "Continuación 2025T2+ (ECP4961, ECP701). Se usa solo para validar ECP701."),
    ("ine_ipva_nacional_ccaa.csv, ine_vut_nacional_ccaa_prov.csv", "No especificados para este módulo."),
    ("mivau_parque.csv, mivau_transacciones_residencia.csv", "No especificados."),
    ("ine_ipv_25171.csv", "Solo IPV769 (base 2015) como robustez: incluido en nacional_q (ipv15)."),
    ("vlc_precio_vivienda_libre.csv", "Excluido de valencia.csv: 5 trimestres (2021T2-2022T2), fuente primaria no indicada, las series están etiquetadas 'barcelona/madrid/...' con cabecera CKAN; no sirve para el modelo."),
]


def _stats(s: pd.Series, flag: pd.Series | None = None) -> tuple[str, str, str, str]:
    v = s.dropna()
    if v.empty:
        return "-", "-", "0", "-"
    first, last = v.index.min(), v.index.max()
    n_gap = int(s[(s.index >= first) & (s.index <= last)].isna().sum())
    n_int = int(flag.sum()) if flag is not None else 0
    return str(first), str(last), str(n_gap), str(n_int)


def write_dictionary(nac: pd.DataFrame, panel: pd.DataFrame, valencia: pd.DataFrame,
                     nacionalidad: pd.DataFrame) -> None:
    nac_i = nac.copy()
    nac_i.index = pd.PeriodIndex(nac_i["trimestre"], freq="Q")
    lines = []
    A = lines.append
    A("# Diccionario de variables\n")
    A("> Generado por `src/build_dataset.py` (no editar a mano). Reconstrucción: `make clean`.\n")
    A("Convenciones comunes:\n")
    A("- **Trimestre**: `trimestre` = `2008Q1`; `fecha` = primer día del trimestre.")
    A("- **Logs**: `ln_<var>` = ln(var) con NaN si var <= 0. **Diferencias**: `d_ln_<var>` = Δ1 trimestral del log; `d4_ln_<var>` = Δ4 (interanual) del log.")
    A("- **Tipos (en %)**: sin log; `d_<var>` = Δ1 trimestral en puntos porcentuales.")
    A("- **Agregación mensual→trimestral**: media o suma de los 3 meses, exigiendo los 3 meses (si falta alguno, NaN). Stock: valor del último mes del trimestre.")
    A("- **Interpolación**: nunca fuera del rango observado; los huecos finales quedan NaN. Columnas `<var>_interp` marcan filas interpoladas.")
    A("- **Huecos internos**: NaN entre el primer y el último dato no NaN.")
    A("- **Retardos** no se crean aquí (se hacen en los scripts de modelos).\n")

    A("## A. `data/processed/nacional_q.csv` (trimestral, nacional)\n")
    A("| Variable | Fuente | Archivo raw | Código / serie | Unidad | Frecuencia original | Agregación | Transformaciones | Interpolación / nº obs. afectadas | Primer dato | Último dato | Huecos internos |")
    A("|---|---|---|---|---|---|---|---|---|---|---|---|")
    flags_map = {"pob_total": "pob_total_interp", "pob_extranj": "pob_extranj_interp", "tipo_bce": "tipo_bce_interp"}
    order = ["ipv", "ipv_nueva", "ipv_usada", "ipv15", "p_tasado", "p_bde", "hpi_eurostat", "ocupados", "ocupados_sa",
             "renta_hog", "deflactor", "renta_hog_real", "tipo_hip", "euribor", "tipo_bce", "tipo_hip_real",
             "inflacion_deflactor", "ipc_alquiler", "ipc_alquiler_yoy", "credito_nuevo", "credito_stock",
             "permisos", "costes", "prod_constr", "visados", "terminadas", "compraventas", "compraventas_sa",
             "trans_total", "trans_extranjeros", "pob_total", "pob_extranj", "hogares", "inmig_anual"]
    meta_by = {r[0]: r for r in META_NAC}
    for var in order:
        r = meta_by[var]
        nombre, fuente, archivo, cod, unidad, freq, agreg = r
        if var in LEVELS_POS:
            tr = "ln_, d_ln_, d4_ln_"
        elif var in RATES:
            tr = "d_ (Δ1 pp)"
        else:
            tr = "ninguna"
        if var == "inmig_anual":
            tr = "ninguna (anual)"
        if var in flags_map:
            interp_txt = f"log-lineal entre observaciones; {flags_map[var]} (ver nº)"
        elif var == "tipo_bce":
            interp_txt = "escalonado; flag tipo_bce_interp = trimestre sin cambio de tipo"
        else:
            interp_txt = "ninguna"
        fl = nac_i[flags_map[var]].astype(bool) if var in flags_map else None
        if var == "tipo_bce":
            fl = nac_i["tipo_bce_interp"].astype(bool)
        if var in nac_i.columns:
            s = nac_i[var]
        else:
            s = nac_i[var] if var in nac_i else pd.Series(np.nan, index=nac_i.index)
        first, last, gaps, n_int = _stats(s, fl)
        if var in flags_map or var == "tipo_bce":
            interp_txt += f"; nº obs. = {n_int}"
        cod_e = cod.replace("|", "\\|")
        A(f"| `{var}` | {fuente} | `{archivo}` | {cod_e} | {unidad} | {freq} | {agreg} | {tr} | {interp_txt} | {first} | {last} | {gaps} |")
    A("")
    A("Variables derivadas con la misma regla de transformación: `ln_`, `d_ln_`, `d4_ln_` para niveles positivos; `d_` para tipos y tasas (ver lista de columnas en el CSV).\n")
    A("**Notas de método**")
    A("- `ipc_alquiler` usa el índice de la subclase alquiler (IPC290887) y `ipc_alquiler_yoy` la variación anual (IPC290886); en el CSV la tasa aparece como `ipc_alquiler_yoy` con `d_`.")
    A("- `deflactor` = PIB nominal NSA (CNTR6548) / PIB volumen encadenado NSA (CNTR6721), reescalado para que la media de 2020 sea 100 (el volumen encadenado tiene media 2020 = 100). Es un deflactor implícito aproximado, no el oficial del INE.")
    A("- `renta_hog_real` = renta_hog / deflactor × 100 (M€ a precios de 2020).")
    A("- `tipo_hip_real` = tipo_hip − inflacion_deflactor (tasa interanual del deflactor, en pp). La HICP de BCE (`ecb_hicp_es.csv`) termina en 2025-12 y no se usa.")
    A("- `visados`: faltan abril-junio de 2016 y de 2017 en el origen (MIVAU), así que 2016T2 y 2017T2 quedan NaN (regla de los 3 meses).")
    A("- `ocupados_sa` y `compraventas_sa`: STL(period=4, robust=True) sobre log, en el bloque contiguo más largo de datos; nivel = exp(log − estacional). Solo para estas dos series.")
    A("- `pob_total` (ECP320) y `pob_extranj` (ECP701) son semestrales hasta 2020 (1 ene y 1 jul) y trimestrales desde 2021. Los trimestres intermedios (T2 y T4 de 1995-2020) se interpolan en logaritmos entre observaciones. La cifra de interpolados figura en la columna de la tabla y en `pob_*_interp`. Validación cruzada: ECP701 de `ine_ecp_56936.csv` (2002-2025) y de `ine_ecp_59585.csv` (2025T2+), ver sección de comprobaciones.")
    A("- `tipo_bce_interp`: True cuando el trimestre no tiene cambio de tipo (el valor es el vigente desde un cambio anterior).")
    A("- `visados` y `terminadas` son proxies del Boletín MIVAU (viviendas libres iniciadas/terminadas), no los visados de dirección de obra del CSCAE ni los certificados de fin de obra.")
    A("- `hogares`: serie trimestral solo desde 2021T1 (tabla 60131). No se interpola ni se retropola; antes de 2021 es NaN.")
    A("- `inmig_anual`: flujo anual (EMCR, tabla 69687) asignado al **primer trimestre** de cada año. No es un flujo trimestral; no usar sin agregación anual.")
    A("- `inmig_q` (59011 total nacional) **no se incluye**: la tabla no tiene serie total y las nacionalidades están casi todas vacías (ver `docs/fuentes_fallidas.md`).")
    A("- `credito_stock`: fin de trimestre. `credito_nuevo`: suma de 3 meses (M€).")
    A("")
    A("### Dummies y muestra\n")
    A("- `q1`…`q4`: dummies trimestrales. `muestra_base` = True desde 2008Q1 hasta el último trimestre con `ipv` no NaN.\n")

    A("## B. `data/processed/panel_ccaa_q.csv` (17 CCAA × trimestre, formato largo)\n")
    A("Códigos INE de CCAA: 01 Andalucía, 02 Aragón, 03 Asturias (Principado de), 04 Balears (Illes), 05 Canarias, 06 Cantabria, 07 Castilla y León, 08 Castilla-La Mancha, 09 Cataluña, 10 Comunitat Valenciana, 11 Extremadura, 12 Galicia, 13 Madrid (Comunidad de), 14 Murcia (Región de), 15 Navarra (Comunidad Foral de), 16 País Vasco, 17 La Rioja. **Ceuta (18) y Melilla (19) excluidas.** Los nombres se normalizan con `slug()` (sin acentos) y `SLUG_ALIAS` (p. ej. 'Comunidad Valenciana' de MIVAU = 'Comunitat Valenciana' de INE).\n")
    A("| Variable | Fuente | Archivo raw | Código / serie | Unidad | Frecuencia | Agregación | Transformaciones | Cobertura (CCAA con datos) | Primer dato (mín. entre CCAA) | Último dato (máx. entre CCAA) |")
    A("|---|---|---|---|---|---|---|---|---|---|---|")
    panel_meta = {
        "ipv": ("INE IPV, tabla 80270", "ine_ipv_80270.csv", "IPV1392 (CCAA General)", "índice", "trimestral", "nativo"),
        "ipv_nueva": ("INE IPV, tabla 80270", "ine_ipv_80270.csv", "'<CCAA>. Vivienda nueva. Índice.'", "índice", "trimestral", "nativo"),
        "ipv_usada": ("INE IPV, tabla 80270", "ine_ipv_80270.csv", "'<CCAA>. Vivienda segunda mano. Índice.'", "índice", "trimestral", "nativo"),
        "p_tasado": ("MIVAU, tabla 35101000", "mivau_valor_tasado_nacional_ccaa_prov.csv", "valor_tasado_libre_ccaa_<slug>", "€/m2", "trimestral", "nativo"),
        "ocupados": ("INE EPA, tabla 65302", "ine_epa_ocupados_ccaa.csv", "'<CCAA>. Ambos sexos. Total. Ocupados. Valor absoluto.'", "miles", "trimestral", "nativo"),
        "compraventas": ("INE ETDP, tabla 6150", "ine_etdp_compraventas.csv", "'<CCAA>. General. Compraventa. Número.'", "número", "mensual", "suma de 3 meses"),
        "trans_total": ("MIVAU, tabla 34010110", "mivau_transacciones_total.csv", "tx_total_ccaa_<slug>", "transacciones", "trimestral", "nativo"),
        "trans_extranjeros": ("MIVAU, tabla 340101i0 (total)", "mivau_transacciones_extranjeros.csv", "tx_extranj_residentes_total_ccaa_<slug>", "transacciones", "trimestral", "nativo"),
        "visados": ("MIVAU, tabla 32100500 (PROXY)", "mivau_visados.csv", "viv_libres_iniciadas_ccaa_<slug>", "viviendas", "mensual", "suma de 3 meses"),
        "terminadas": ("MIVAU, tabla 32101000 (PROXY)", "mivau_fin_obra.csv", "viv_libres_terminadas_ccaa_<slug>", "viviendas", "mensual", "suma de 3 meses"),
        "ipc_alquiler": ("INE IPC, alquiler de vivienda", "ine_ipc_alquiler.csv", "'<CCAA>. Alquiler de vivienda. Índice.'", "índice", "mensual", "media de 3 meses"),
    }
    for v in PANEL_LEVELS:
        nm, arch, cod, uni, fr, ag = panel_meta[v]
        per_ccaa = panel.dropna(subset=[v]).groupby("codigo_ine_ccaa")["trimestre"].agg(["min", "max", "count"])
        ncc = len(per_ccaa)
        fmin = per_ccaa["min"].min() if ncc else "-"
        fmax = per_ccaa["max"].max() if ncc else "-"
        tr = "ln_, d_ln_, d4_ln_ (dentro de cada CCAA)"
        A(f"| `{v}` | {nm} | `{arch}` | {cod} | {uni} | {fr} | {ag} | {tr} | {ncc}/17 | {fmin} | {fmax} |")
    A("")
    A("**Huecos de origen**: `terminadas` (MIVAU 32101000) no tiene Extremadura en el Boletín, así que esa CCAA queda NaN en esa variable. `p_tasado` de Navarra tiene solo los trimestres en que MIVAU publica esa CCAA (ver `DUP_NOTES`).\n")
    A("**No incluido en el panel (sin dato en `data/raw`)**: `pob_total` y `pob_extranj` por CCAA. Las tablas de población de INE descargadas (56936, 59585 y ECP320/701 de `ine_ecp_nacional.csv`) son solo nacionales; no hay ECP por comunidad. `inmig` por CCAA agregada: la tabla 59013 no tiene total y tiene pocas celdas con valor (ver sección D). Ceuta y Melilla no se incluyen.\n")

    A("## B2. `data/processed/panel_ccaa_nacionalidad.csv`\n")
    A(f"Flujos de inmigración de la tabla INE 59013 (CCAA × nacionalidad, trimestral desde 2023T2). Solo celdas con valor: **{len(nacionalidad)} filas** (de 1.159 series × 14 trimestres; el resto está vacío en el origen y no se rellena). Stock de población extranjera por CCAA × nacionalidad: **no disponible** en `data/raw` (las tablas ECP de nacionalidad son nacionales). El instrumento shift-share requiere ese stock; falta.\n")

    A("## C. `data/processed/valencia.csv` (territorio × trimestre × variable)\n")
    A("| Variable | Territorio | Archivo raw | Código / serie | Unidad | Frecuencia original | Tratamiento | Primer | Último | Nº trimestres |")
    A("|---|---|---|---|---|---|---|---|---|---|")
    vmeta = {
        "p_tasado": ("mivau_valor_tasado_municipios.csv / mivau_valor_tasado_nacional_ccaa_prov.csv", "valor_tasado_mun_valencia; valor_tasado_libre_provincia_valencia_valencia; valor_tasado_libre_ccaa_comunidad_valenciana; valor_tasado_libre_nacional", "€/m2", "trimestral", "nativo"),
        "trans_total": ("mivau_transacciones_municipios.csv / mivau_transacciones_total.csv", "tx_municipio_valencia; tx_total_ccaa_comunitat_valenciana; tx_total_nacional", "transacciones", "trimestral", "nativo"),
        "trans_extranjeros": ("mivau_transacciones_extranjeros.csv", "tx_extranj_residentes_total_ccaa_comunitat_valenciana; tx_extranj_residentes_total_nacional", "transacciones", "trimestral", "nativo (sin dato municipal en raw)"),
        "ipv": ("ine_ipv_80270.csv", "IPV1392 (CV General); IPV1209 (Nacional General)", "índice", "trimestral", "nativo"),
        "vut_viviendas_turisticas": ("ine_vut_valencia_municipio.csv", "ine_vut_valencia_valencia_viviendas_turisticas", "nº viviendas", "semestral (feb/ago)", "sin interpolar; feb→T1, ago→T3"),
        "vut_plazas": ("ine_vut_valencia_municipio.csv", "ine_vut_valencia_valencia_plazas", "plazas", "semestral", "sin interpolar"),
        "vut_plazas_por_vivienda": ("ine_vut_valencia_municipio.csv", "ine_vut_valencia_valencia_plazas_por_vivienda", "plazas/vivienda", "semestral", "sin interpolar"),
        "vut_pct_sobre_total": ("ine_vut_valencia_municipio.csv", "ine_vut_valencia_valencia_pct_viv_turisticas_sobre_total", "proporción", "semestral", "sin interpolar"),
        "ipva": ("ine_ipva_municipal.csv", "IPVA8471 (Valencia. Índice. Total.)", "índice", "anual", "sin interpolar; año→T1"),
    }
    terr_order = sorted(valencia["territorio"].unique())
    for var in ["p_tasado", "trans_total", "trans_extranjeros", "ipv", "vut_viviendas_turisticas", "vut_plazas",
                "vut_plazas_por_vivienda", "vut_pct_sobre_total", "ipva"]:
        _, _, uni, fr, trat = vmeta[var]
        sub = valencia[valencia["variable"] == var]
        for terr in terr_order:
            ss = sub[sub["territorio"] == terr]
            if ss.empty:
                continue
            arch, cod = VAL_SRC[(terr, var)].split(" | ", 1)
            A(f"| `{var}` | {terr} | `{arch}` | {cod} | {uni} | {fr} | {trat} | {ss['trimestre'].min()} | {ss['trimestre'].max()} | {len(ss)} |")
    A("")
    A("Formato largo: filas solo con valor (sin NaN). Los datos semestrales y anuales no se interpolan. **Excluido**: `vlc_precio_vivienda_libre.csv` (ver sección D).\n")

    A("## D. Fuentes raw no utilizadas, excluidas o con duplicados\n")
    A("Duplicados idénticos en origen (se usa el primer código, verificado valor a valor):\n")
    for note in sorted(set(DUP_NOTES)):
        A(f"- {note}")
    A("")
    A("| Archivo | Motivo |")
    A("|---|---|")
    for f, m in NO_USADAS:
        A(f"| `{f}` | {m} |")
    A("")

    A("## Cobertura de la muestra base 2008Q1+\n")
    key = ["ln_ipv", "ln_ocupados", "tipo_hip", "ln_permisos", "ln_costes", "ln_renta_hog_real",
           "ln_pob_extranj", "ln_terminadas", "ln_hogares"]
    base = nac_i[nac_i["muestra_base"].astype(bool)]
    A("| Variable | N en 2008Q1+ | Primer dato (no NaN) | Último dato (no NaN) |")
    A("|---|---|---|---|")
    for v in key:
        s = base[v]
        n = int(s.notna().sum())
        v_nn = s.dropna()
        last = nac_i.loc[v_nn.index.max(), "trimestre"] if len(v_nn) else "-"
        first = nac_i.loc[v_nn.index.min(), "trimestre"] if len(v_nn) else "-"
        A(f"| `{v}` | {n} | {first} | {last} |")
    common = base[key].dropna()
    last_common = nac_i.loc[common.index.max(), "trimestre"] if len(common) else "-"
    A("")
    A(f"- **N completo** (filas con las 9 variables no NaN, 2008Q1+): **{len(common)}**; **último trimestre común**: **{last_common}**.")
    sin_h = base[[c for c in key if c != "ln_hogares"]].dropna()
    last_sin_h = nac_i.loc[sin_h.index.max(), "trimestre"] if len(sin_h) else "-"
    A(f"- `ln_hogares` solo existe desde 2021T1 (tabla 60131) y restringe la muestra común. Sin ella (8 variables): N = **{len(sin_h)}**, último trimestre común = **{last_sin_h}**.")
    A("- Los N de la tabla son de las variables `ln_` (en niveles logarítmicos); las diferencias `d_ln_` pierden 1 trimestre al inicio y `d4_ln_` pierde 4.\n")

    (DOCS / "diccionario_variables.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def checks(nac: pd.DataFrame, panel: pd.DataFrame, valencia: pd.DataFrame) -> None:
    print("=== COMPROBACIONES FINALES ===")
    m08 = nac[nac["trimestre"] >= "2008Q1"]
    print(f"N nacional_q (filas 2008Q1+): {len(m08)}  (rango total {nac['trimestre'].iloc[0]}..{nac['trimestre'].iloc[-1]}, filas {len(nac)})")
    last_ipv = nac.loc[nac["ipv"].notna(), "trimestre"].iloc[-1]
    print(f"Último trimestre con ipv: {last_ipv}  (N ipv 2008Q1+ = {int(m08['ipv'].notna().sum())})")
    print(f"Nº CCAA en panel: {panel['codigo_ine_ccaa'].nunique()}  ({', '.join(sorted(panel['ccaa'].unique()))})")
    print(f"Duplicados: nacional trimestre={int(nac['trimestre'].duplicated().sum())}  "
          f"panel (codigo,trimestre)={int(panel.duplicated(['codigo_ine_ccaa','trimestre']).sum())}  "
          f"valencia (territorio,trimestre,variable)={int(valencia.duplicated(['territorio','trimestre','variable']).sum())}")

    # Valores de control contra data/raw (lectura independiente)
    ctrl = []
    ipv_raw = pd.read_csv(RAW / "ine_ipv_80270.csv", dtype=str)
    ipv_raw = ipv_raw[(ipv_raw["serie"] == "IPV1209") & (ipv_raw["fecha"] == "2015-01-01")]
    ctrl.append(("ipv 2015Q1 (IPV1209)", float(ipv_raw["valor"].iloc[0]), nac.loc[nac["trimestre"] == "2015Q1", "ipv"].iloc[0]))
    epa_raw = pd.read_csv(RAW / "ine_epa_ocupados.csv", dtype=str)
    epa_raw = epa_raw[epa_raw["fecha"] == "2019-10-01"]
    ctrl.append(("ocupados 2019Q4 (EPA387796)", float(epa_raw["valor"].iloc[0]), nac.loc[nac["trimestre"] == "2019Q4", "ocupados"].iloc[0]))
    st_raw = pd.read_csv(RAW / "ecb_stock_credito_vivienda_es.csv", dtype=str)
    st_raw = st_raw[st_raw["fecha"] == "2020-12-01"]
    ctrl.append(("credito_stock 2020Q4 (BSI, fin de trimestre)", float(st_raw["valor"].iloc[0]), nac.loc[nac["trimestre"] == "2020Q4", "credito_stock"].iloc[0]))
    for name, raw_v, csv_v in ctrl:
        ok = np.isclose(raw_v, float(csv_v), rtol=1e-9)
        print(f"Control {name}: raw={raw_v} csv={csv_v} -> {'OK' if ok else 'DIFERENTE'}")

    # Validacion pob_extranj frente a ECP701 de 56936 y 59585
    e56 = pd.read_csv(RAW / "ine_ecp_56936.csv", dtype=str, usecols=["fecha", "serie", "valor"])
    e56 = e56[e56["serie"] == "ECP701"].copy()
    e59 = pd.read_csv(RAW / "ine_ecp_59585.csv", dtype=str, usecols=["fecha", "serie", "valor"])
    e59 = e59[e59["serie"] == "ECP701"].copy()
    ref = pd.concat([e56, e59]).drop_duplicates("fecha", keep="last")
    ref["valor"] = pd.to_numeric(ref["valor"], errors="coerce")
    ref["q"] = pd.PeriodIndex(pd.to_datetime(ref["fecha"]), freq="Q").astype(str)
    cmp = ref.merge(nac[["trimestre", "pob_extranj"]], left_on="q", right_on="trimestre")
    cmp = cmp.dropna(subset=["valor", "pob_extranj"])
    cmp = cmp[cmp["fecha"].str[5:7].isin(["01", "04", "07", "10"])]
    diff = (cmp["valor"] - cmp["pob_extranj"]).abs()
    print(f"Validación ECP701 (56936/59585) vs pob_extranj: {len(cmp)} trimestres con dato; max |dif| = {diff.max():.1f}")


def main() -> None:
    PROC.mkdir(parents=True, exist_ok=True)
    DOCS.mkdir(parents=True, exist_ok=True)

    nac_raw = build_nacional()
    nac = finalize_nacional(nac_raw)
    nac.to_csv(PROC / "nacional_q.csv", index=False)

    panel = finalize_panel(build_panel())
    panel.to_csv(PROC / "panel_ccaa_q.csv", index=False)

    nacionalidad = build_nacionalidad()
    nacionalidad.to_csv(PROC / "panel_ccaa_nacionalidad.csv", index=False)

    valencia = build_valencia()
    valencia.to_csv(PROC / "valencia.csv", index=False)

    write_dictionary(nac, panel, valencia, nacionalidad)
    checks(nac, panel, valencia)
    print(f"Escritos: {PROC/'nacional_q.csv'}, {PROC/'panel_ccaa_q.csv'}, {PROC/'panel_ccaa_nacionalidad.csv'}, "
          f"{PROC/'valencia.csv'}, {DOCS/'diccionario_variables.md'}")


if __name__ == "__main__":
    main()
