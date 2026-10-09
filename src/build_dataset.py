#!/usr/bin/env python3
"""Construye data/processed a partir de data/raw (solo lectura de raw).

Salidas:
  data/processed/nacional_q.csv            trimestral nacional, 1995Q1+ (muestra base 2008Q1+)
  data/processed/nacional_a.csv            anual nacional (medias/sumas de nacional_q + flujos anuales)
  data/processed/panel_ccaa_q.csv          17 CCAA x trimestre (formato largo)
  data/processed/panel_ccaa_a.csv          17 CCAA x año (IV shift-share, F3)
  data/processed/panel_ccaa_nacionalidad.csv  flujos 59013 CCAA x nacionalidad + stocks 77019 CCAA x grupo (1 ene)
  data/processed/valencia.csv              territorio x periodo x variable (formato largo)
  data/processed/validacion_gva.csv        contrastes del registro GVA (VUT y padrón) con nota de independencia
  docs/diccionario_variables.md            generado por este script (no editar a mano)

Banderas de método: cada variable con transformación temporal lleva <var>_metodo (categórica:
observado, agregado_media, agregado_suma, fin_periodo, escalonado, interpolado_loglineal, anual_asignado,
desestacionalizado_stl). <var>_interp = (<var>_metodo == 'interpolado_loglineal') por compatibilidad.

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


# Banderas de método (<var>_metodo). Criterio único para nacional_q, nacional_a, panel_ccaa_q, panel_ccaa_a y valencia.
METODOS = ["observado", "agregado_media", "agregado_suma", "fin_periodo", "escalonado",
           "interpolado_loglineal", "anual_asignado", "desestacionalizado_stl"]
# 'anual_asignado' incluye también las series semestrales asignadas a un trimestre (S1->T2, S2->T4; feb->T1, ago->T3).
# 'desestacionalizado_stl' se añade al conjunto inicial para no etiquetar el STL como otro método.


def mcol(valores: pd.Series, metodo) -> pd.Series:
    """Columna <var>_metodo: etiqueta del método donde hay valor; NaN (vacío) donde no hay dato.
    metodo: cadena (mismo método en toda la serie) o Series/array alineada con valores."""
    m = np.where(valores.notna(), metodo, None)
    out = pd.Series(m, index=valores.index, dtype=object)
    assert set(out.dropna().unique()) <= set(METODOS), "método fuera del conjunto cerrado"
    return out


def interp_de(metodo: pd.Series) -> pd.Series:
    """Bandera <var>_interp = (metodo == interpolado_loglineal). Solo esta transformación es interpolación."""
    return (metodo == "interpolado_loglineal").fillna(False).astype(bool)


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
              "pob_total", "pob_extranj", "hogares_epa", "hogares_ecp",
              "registradores_compraventas_anual", "notariado_cgn_extranj", "serpavi_esp_constante",
              "pob_extranj_ccaa_sum"]
RATES = ["tipo_hip", "euribor", "tipo_bce", "tipo_hip_real", "ipc_alquiler_yoy",
         "inflacion_deflactor", "registradores_extranj_pct"]
BASE_CHECK = LEVELS_POS + RATES + ["inmig_anual"]


def build_nacional(pob_ccaa: pd.DataFrame | None = None) -> pd.DataFrame:
    """pob_ccaa: DataFrame indexado por Period trimestral con columnas valor (suma 17 CCAA) e interp."""
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

    # Deflactor implicito del PIB, SA: PIB a precios corrientes SA (CNTR6597, M€) / PIB volumen encadenado SA
    # (CNTR6652, indice de volumen encadenado). Las dos series son "Datos ajustados de estacionalidad y calendario".
    # (La version anterior usaba CNTR6548/CNTR6721, NSA: generaba un ciclo estacional espurio en renta_hog_real.)
    nom = by_serie(read_raw("ine_cnt_pib_oferta_corrientes.csv", ["fecha", "serie", "valor"]), "CNTR6597")
    vol = by_serie(read_raw("ine_cnt_pib_oferta_volumen.csv", ["fecha", "serie", "valor"]), "CNTR6652")
    # Reescalado como antes: media anual 2020 = 100
    ratio = nom / vol
    base_2020 = ratio[ratio.index.year == 2020].mean()
    d["deflactor"] = q_direct(100 * ratio / base_2020)
    d["renta_hog_real"] = d["renta_hog"] / d["deflactor"] * 100
    d["inflacion_deflactor"] = (d["deflactor"] / d["deflactor"].shift(4) - 1) * 100

    d["tipo_hip"] = m_agg(one(read_raw("ecb_tipo_hipotecario_es.csv", ["fecha", "serie", "valor"])), "mean")
    d["euribor"] = m_agg(one(read_raw("ecb_euribor1y.csv", ["fecha", "serie", "valor"])), "mean")
    tipo_bce, bce_sin_cambio = mrr_q()
    d["tipo_bce"] = tipo_bce
    # escalonado: trimestre sin cambio de tipo (valor vigente de un cambio anterior); agregado_media: con cambio
    d["tipo_bce_metodo"] = mcol(tipo_bce, np.where(bce_sin_cambio.values, "escalonado", "agregado_media"))
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
    d["pob_total"] = pob_t
    d["pob_total_metodo"] = mcol(pob_t, np.where(f_t.values, "interpolado_loglineal", "observado"))
    d["pob_extranj"] = pob_e
    d["pob_extranj_metodo"] = mcol(pob_e, np.where(f_e.values, "interpolado_loglineal", "observado"))

    d["hogares_ecp"] = q_direct(by_serie(read_raw("ine_hogares_60131.csv", ["fecha", "serie", "valor"]),
                                         "ECP355533"))
    ehog = read_raw("ine_epa_hogares.csv", ["fecha", "serie", "valor", "nombre"])
    d["hogares_epa"] = q_direct(one(ehog[ehog["nombre"] == "Hogares. Total Nacional. Ambos sexos. Total. Total."]))

    # Series anuales y semestrales: asignadas a un trimestre, sin interpolar (metodo anual_asignado)
    rg = read_raw("pdf/registradores_opendata_anual.csv", ["fecha", "serie", "valor", "nivel"])
    rg = rg[rg["nivel"] == "nacional"]
    d["registradores_compraventas_anual"] = anual_a_trimestre(by_serie(rg, "compraventas_viv_num"), 4)
    rex = read_raw("pdf/registradores_eri_anuario.csv", ["fecha", "serie", "valor", "nivel"])
    rex = rex[rex["nivel"] == "nacional"]
    d["registradores_extranj_pct"] = anual_a_trimestre(by_serie(rex, "viv_pct_compras_extranjeros"), 4)
    cgn = read_raw("pdf/notariado_cgn_extranjeros_semestral.csv",
                   ["fecha", "serie", "valor", "tabla", "territorio", "categoria"])
    cgn_nac = cgn[(cgn["tabla"] == "T1") & (cgn["serie"] == "op_viv_libre") &
                  (cgn["categoria"] == "Extranjero") & (cgn["territorio"] == "Espana")]
    d["notariado_cgn_extranj"] = semestral_a_trimestre(by_serie(cgn_nac, "op_viv_libre"))
    spe = read_raw("pdf/serpavi_esp_agregado.csv", ["fecha", "serie", "valor"])
    d["serpavi_esp_constante"] = anual_a_trimestre(
        by_serie(spe, "SERPAVI_ESP_VC_alquiler_m2_mediana_pond_composicion_constante"), 4)

    mig = read_raw("ine_migraciones_total_anual.csv", ["fecha", "serie", "valor", "nombre"])
    mig_serie = mig.loc[mig["nombre"] == "Todas las edades. Total. Dato base. Inmigraciones procedentes del extranjero.", "serie"].unique()
    assert len(mig_serie) == 1
    anual = by_serie(mig, mig_serie[0])
    inmig = pd.Series(np.nan, index=QIDX)
    for dt, v in anual.items():  # valor anual asignado solo al primer trimestre del año
        inmig[pd.Period(dt, freq="Q")] = v
    d["inmig_anual"] = inmig  # EMCR (69687), 2021-2024: rol robustez (N=4)

    # Inmigración anual TOTAL (Eurostat migr_imm1ctz, todas las ciudadanías), 1998-2024: asignada a T4
    eu = pd.read_csv(RAW / "eurostat_inmigracion_anual.csv", dtype=str, keep_default_na=False)
    eu = eu[(eu["citizen"] == "TOTAL") & (eu["valor"] != "")].copy()
    eu["valor"] = pd.to_numeric(eu["valor"])
    eu["fecha"] = pd.to_datetime(eu["fecha"])
    d["inmig_anual_eurostat"] = anual_a_trimestre(
        pd.Series(eu["valor"].values, index=pd.DatetimeIndex(eu["fecha"])).sort_index(), 4)
    d["inmig_anual_eurostat_metodo"] = mcol(d["inmig_anual_eurostat"], "anual_asignado")
    # Quiebres de serie (escalones desde 2021T1)
    d["quiebre_epa_2021"] = [int(p >= pd.Period("2021Q1", freq="Q")) for p in QIDX]
    d["quiebre_emcr_2021"] = [int(p >= pd.Period("2021Q1", freq="Q")) for p in QIDX]

    # Desestacionalizacion (solo ocupados y compraventas)
    d["ocupados_sa"] = stl_sa(d["ocupados"])
    d["compraventas_sa"] = stl_sa(d["compraventas"])

    # Control: suma de 17 CCAA de pob_extranj (panel); bandera = alguna CCAA interpolada en ese trimestre
    if pob_ccaa is not None:
        d["pob_extranj_ccaa_sum"] = pob_ccaa["valor"].reindex(QIDX).astype(float)
        fl_c = pob_ccaa["interp"].reindex(QIDX).fillna(False).astype(bool).values
        d["pob_extranj_ccaa_sum_metodo"] = mcol(d["pob_extranj_ccaa_sum"],
                                                np.where(fl_c, "interpolado_loglineal", "observado"))
    else:
        d["pob_extranj_ccaa_sum"] = np.nan
        d["pob_extranj_ccaa_sum_metodo"] = None
    # Banderas <var>_metodo: transformaciones temporales (agregacion, fin de trimestre, STL, asignacion)
    for v, m in METODO_NAC.items():
        if v in d and f"{v}_metodo" not in d:
            d[f"{v}_metodo"] = mcol(d[v], m)

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
                               "pob_total", "pob_extranj", "hogares_epa", "hogares_ecp", "tipo_hip", "euribor",
                               "tipo_bce", "tipo_hip_real", "inflacion_deflactor", "inmig_anual",
                               "registradores_compraventas_anual", "registradores_extranj_pct",
                               "notariado_cgn_extranj", "serpavi_esp_constante", "pob_extranj_ccaa_sum",
                               "inmig_anual_eurostat"]]
    cols_ln = [f"{p}{v}" for v in LEVELS_POS if v in d for p in ("ln_", "d_ln_", "d4_ln_")]
    cols_d = [f"d_{v}" for v in RATES]
    for c in cols_levels + cols_ln + cols_d:
        if c in d:
            out[c] = d[c]
    # ipc_alquiler_yoy ya esta en cols_levels (tipo %); su diferencia se llama d_ipc_alquiler_yoy
    # Banderas: <var>_metodo (categorica) y <var>_interp = (metodo == interpolado_loglineal)
    for f in [c for c in d.columns if c.endswith("_metodo")]:
        out[f] = d[f].values
        out[f.replace("_metodo", "_interp")] = interp_de(d[f]).values
    out["quiebre_epa_2021"] = d["quiebre_epa_2021"].values
    out["quiebre_emcr_2021"] = d["quiebre_emcr_2021"].values
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


def build_panel(pob77: pd.DataFrame) -> pd.DataFrame:
    ipv = add_geo(read_raw("ine_ipv_80270.csv", ["fecha", "serie", "valor", "nombre"]))
    epa = add_geo(read_raw("ine_epa_ocupados_ccaa.csv", ["fecha", "serie", "valor", "nombre"]))
    etdp = add_geo(read_raw("ine_etdp_compraventas.csv", ["fecha", "serie", "valor", "nombre"]))
    ipc = add_geo(read_raw("ine_ipc_alquiler.csv", ["fecha", "serie", "valor", "nombre"]))
    tas = read_raw("mivau_valor_tasado_nacional_ccaa_prov.csv", ["fecha", "serie", "valor", "nivel"])
    tx_t = read_raw("mivau_transacciones_total.csv", ["fecha", "serie", "valor"])
    tx_e = read_raw("mivau_transacciones_extranjeros.csv", ["fecha", "serie", "valor"])
    vis = read_raw("mivau_visados.csv", ["fecha", "serie", "valor"])
    fin = read_raw("mivau_fin_obra.csv", ["fecha", "serie", "valor"])
    epa_p = ser_por_ccaa(epa_pob_long(read_raw("ine_epa_poblacion_ccaa.csv", ["fecha", "serie", "valor", "nombre"])),
                         "valor")
    pob_g = {g: ser_por_ccaa(x, "pob_stock") for g, x in pob77.groupby("grupo")}

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
        # Metodos de agregacion temporal (mensual -> trimestral)
        for v, m in [("compraventas", "agregado_suma"), ("visados", "agregado_suma"),
                     ("terminadas", "agregado_suma"), ("ipc_alquiler", "agregado_media")]:
            d[f"{v}_metodo"] = mcol(d[v], m)
        # Poblacion por CCAA (77019, 1 ene en T1; interpolacion log-lineal entre observaciones) y EPA
        for var, grp in [("pob_total", "Total"), ("pob_extranj", "Extranjera"), ("pob_espanola", "Española")]:
            ser = pob_g.get(grp, {}).get(cod)
            if ser is None:
                d[var] = np.nan
                d[f"{var}_metodo"] = mcol(d[var], "observado")
            else:
                vals, fl = interp_loglin(q_direct(ser))
                d[var] = vals
                # Stock a 1 de enero (anual) asignado a T1; T2-T4 interpolados entre observaciones
                es_t1 = np.array([p.quarter == 1 for p in d.index])
                met = np.where(fl.values, "interpolado_loglineal", np.where(es_t1, "anual_asignado", None))
                d[f"{var}_metodo"] = mcol(vals, met)
        d["epa_pob_total"] = q_direct(epa_p[cod]) if cod in epa_p else np.nan
        frames.append(d)
    panel = pd.concat(frames, keys=[c for c, _, _ in CCAA], names=["cod", "trimestre"]).reset_index(level=0, drop=True)
    panel = panel.reset_index()
    panel["trimestre"] = panel["trimestre"].astype(str)
    for c in [c for c in panel.columns if c.endswith("_metodo")]:
        panel[c.replace("_metodo", "_interp")] = interp_de(panel[c])
    return panel


PANEL_LEVELS = ["ipv", "ipv_nueva", "ipv_usada", "p_tasado", "ocupados", "compraventas",
                "trans_total", "trans_extranjeros", "visados", "terminadas", "ipc_alquiler",
                "pob_total", "pob_extranj", "pob_espanola", "epa_pob_total"]


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


def build_nacionalidad(pob77: pd.DataFrame) -> pd.DataFrame:
    """Flujos de inmigracion 59013 por CCAA x nacionalidad (solo celdas con valor; tipo_registro=flujo_59013)
    y stocks 77019 por CCAA x grupo de paises a 1 de enero (tipo_registro=stock_77019_1ene)."""
    df = add_geo(read_raw("ine_migraciones_ccaa_nacionalidad.csv", ["fecha", "serie", "valor", "nombre"]))
    df = df[df["geo"].isin(list(SLUG2COD.keys()))].copy()
    df = df[df["valor"].notna()].copy()
    df["codigo_ine_ccaa"] = df["geo"].map(ccaa_from_slug)
    df = df[df["codigo_ine_ccaa"].notna()].copy()
    df["ccaa"] = df["codigo_ine_ccaa"].map(COD2NAME)
    df["nacionalidad"] = df["tail"].str.split(r"\. ", n=1, regex=True).str[0]
    df["trimestre"] = pd.PeriodIndex(df["fecha"], freq="Q").astype(str)
    df = df.rename(columns={"valor": "inmig_flujo", "serie": "serie_ine"})
    flujos = df[["ccaa", "codigo_ine_ccaa", "nacionalidad", "trimestre", "fecha", "inmig_flujo", "serie_ine"]].copy()
    flujos["tipo_registro"] = "flujo_59013"
    flujos["pob_stock"] = np.nan
    st = pob77[["ccaa", "codigo_ine_ccaa", "grupo", "trimestre", "fecha", "pob_stock", "serie_ine"]].rename(
        columns={"grupo": "nacionalidad"}).copy()
    st["inmig_flujo"] = np.nan
    st["tipo_registro"] = "stock_77019_1ene"
    out = pd.concat([flujos, st[flujos.columns]], ignore_index=True)
    return out.sort_values(["codigo_ine_ccaa", "tipo_registro", "nacionalidad", "trimestre"]).reset_index(drop=True)


# ----------------------------------------------------------------------------
# Utilidades nuevas (fuentes F1: EPA, 77019 por grupos, anuales/semestrales)
# ----------------------------------------------------------------------------

def anual_a_trimestre(s: pd.Series, q: int) -> pd.Series:
    """Serie anual (fecha = 1 de enero del año) asignada al trimestre q del mismo año. Sin interpolar."""
    out = pd.Series(np.nan, index=QIDX)
    for dt, v in s.dropna().items():
        out[pd.Period(year=dt.year, quarter=q, freq="Q")] = v
    return out


def semestral_a_trimestre(s: pd.Series) -> pd.Series:
    """Serie semestral: S1 (fecha 1 ene) -> T2; S2 (fecha 1 jul) -> T4. Sin interpolar."""
    out = pd.Series(np.nan, index=QIDX)
    for dt, v in s.dropna().items():
        if dt.month not in (1, 7):
            raise ValueError(f"fecha semestral inesperada: {dt}")
        q = 2 if dt.month == 1 else 4
        out[pd.Period(year=dt.year, quarter=q, freq="Q")] = v
    return out


def pob77_long(df: pd.DataFrame) -> pd.DataFrame:
    """INE 77019 (CCAA x grupo de paises, todas las edades). Stock a 1 de enero (el CSV lo etiqueta T1).
    Formato largo, solo las 17 CCAA (Ceuta y Melilla se excluyen)."""
    p = df["nombre"].str.split(r"\. ", regex=True)
    m = (p.str[1] == "Todas las edades") & (p.str[3] == "Total") & df["valor"].notna()
    sub = df.loc[m].copy()
    partes = p[sub.index]
    sub["ccaa_nombre"] = partes.str[0]
    sub["grupo"] = partes.str[2]
    sub["codigo_ine_ccaa"] = sub["ccaa_nombre"].map(lambda x: ccaa_from_slug(slug(x)))
    sub = sub[sub["codigo_ine_ccaa"].notna()].copy()
    sub["ccaa"] = sub["codigo_ine_ccaa"].map(COD2NAME)
    sub["anio"] = sub["fecha"].dt.year
    sub["trimestre"] = [f"{y}Q1" for y in sub["anio"]]
    sub = sub.rename(columns={"valor": "pob_stock", "serie": "serie_ine"})
    cols = ["ccaa", "codigo_ine_ccaa", "grupo", "anio", "trimestre", "fecha", "pob_stock", "serie_ine"]
    return sub[cols].sort_values(["codigo_ine_ccaa", "grupo", "anio"]).reset_index(drop=True)


def epa_pob_long(df: pd.DataFrame) -> pd.DataFrame:
    """INE EPA 65285: poblacion total (todas las edades, incluye 'Menores de 16') por CCAA, trimestral."""
    p = df["nombre"].str.split(r"\. ", regex=True)
    m = (p.str[0] == "Ambos sexos") & (p.str[2] == "Total") & (p.str[3] == "Valor absoluto.") & df["valor"].notna()
    sub = df.loc[m].copy()
    sub["codigo_ine_ccaa"] = p[sub.index].str[1].map(lambda x: ccaa_from_slug(slug(x)))
    return sub[sub["codigo_ine_ccaa"].notna()][["codigo_ine_ccaa", "fecha", "valor"]].copy()


def ser_por_ccaa(d: pd.DataFrame, col: str) -> dict[str, pd.Series]:
    """Diccionario codigo -> serie (indice fecha) a partir de un DataFrame largo con codigo_ine_ccaa y fecha."""
    out: dict[str, pd.Series] = {}
    for cod, g in d.groupby("codigo_ine_ccaa"):
        g = g.drop_duplicates("fecha", keep="last").sort_values("fecha")
        out[cod] = pd.Series(g[col].values, index=pd.DatetimeIndex(g["fecha"]))
    return out


# Nombres de CCAA del CGN (tabla T2) -> codigo INE
CGN_NAME2COD = {
    "Andalucía": "01", "Aragón": "02", "Asturias": "03", "Islas Baleares": "04", "Islas Canarias": "05",
    "Cantabria": "06", "Castilla y León": "07", "Castilla-La Mancha": "08", "Cataluña": "09",
    "Comunidad Valenciana": "10", "Extremadura": "11", "Galicia": "12", "Comunidad de Madrid": "13",
    "Región de Murcia": "14", "Navarra": "15", "País Vasco": "16", "La Rioja": "17",
}

# Grupos de paises de 77019 -> columna del panel anual
GRUPO_VAR = {
    "Total": "pob_total", "Extranjera": "pob_extranj", "Española": "pob_espanola",
    "Apátridas": "pob_apatridas", "De Oceanía": "pob_oceania", "De Asia": "pob_asia",
    "De Sudamérica": "pob_sudamerica", "De Centro América y Caribe": "pob_centroamerica_caribe",
    "De América del Norte": "pob_norteamerica", "De Africa": "pob_africa",
    "País de Europa menos UE28": "pob_europa_no_ue28", "País de Europa menos UE27_2020": "pob_europa_no_ue27",
    "País de la UE28 sin España": "pob_ue28_sin_espana", "País de la UE27_2020 sin España": "pob_ue27_sin_espana",
}
POB_GRUPOS = [v for k, v in GRUPO_VAR.items() if k not in ("Total", "Extranjera", "Española")]

# Metodo <var>_metodo (nacional_q) para variables con transformacion temporal fija. pob_*, tipo_bce y
# pob_extranj_ccaa_sum se etiquetan fila a fila (ver build_nacional).
METODO_NAC = {
    "tipo_hip": "agregado_media", "euribor": "agregado_media", "ipc_alquiler": "agregado_media",
    "ipc_alquiler_yoy": "agregado_media", "credito_nuevo": "agregado_suma", "credito_stock": "fin_periodo",
    "visados": "agregado_suma", "terminadas": "agregado_suma", "compraventas": "agregado_suma",
    "ocupados_sa": "desestacionalizado_stl", "compraventas_sa": "desestacionalizado_stl",
    "inmig_anual": "anual_asignado", "inmig_anual_eurostat": "anual_asignado",
    "registradores_compraventas_anual": "anual_asignado", "registradores_extranj_pct": "anual_asignado",
    "notariado_cgn_extranj": "anual_asignado", "serpavi_esp_constante": "anual_asignado",
}

CHECK: dict[str, object] = {}  # resultados de contrastes calculados en la construccion (para diccionario y checks)


# ----------------------------------------------------------------------------
# Valencia (C): formato largo territorio x periodo x variable
# ----------------------------------------------------------------------------

VAL_SRC: dict[tuple[str, str], str] = {}
VAL_META: dict[tuple[str, str], dict] = {}
VAL_ROWS: list[dict] = []


def ser_trimestral(s: pd.Series) -> pd.Series:
    """Mensual/diaria/fecha -> trimestre (q_direct): indice 'YYYYQn'."""
    q = q_direct(s).dropna()
    return pd.Series(q.values, index=[str(p) for p in q.index])


def ser_periodo_q(s: pd.Series) -> pd.Series:
    """Serie ya indexada por Period trimestral (p. ej. salida de m_end): indice 'YYYYQn'."""
    s = s.dropna()
    return pd.Series(s.values, index=[str(p) for p in s.index])


def ser_anual(s: pd.Series) -> pd.Series:
    """Serie con fecha -> indice 'YYYY' (sin asignar a trimestre)."""
    s = s.dropna()
    return pd.Series(s.values, index=[str(d.year) for d in pd.DatetimeIndex(s.index)])


def val_add(terr: str, var: str, s: pd.Series, frec: str, origen: str, validado: str, rol: str,
            src: str, error_max: str = "—", transf: str = "nativo", nota: str = "", metodo: str = "observado") -> None:
    s = s.dropna()
    assert metodo in METODOS, metodo
    VAL_SRC[(terr, var)] = src
    VAL_META[(terr, var)] = dict(frecuencia=frec, origen=origen, validado=validado, rol=rol,
                                 error_max=error_max, transformacion=transf, nota=nota, metodo=metodo)
    for per, v in s.items():
        VAL_ROWS.append(dict(territorio=terr, periodo=str(per), frecuencia=frec, variable=var, valor=float(v),
                             origen=origen, rol=rol, validado=validado, metodo=metodo,
                             interp=(metodo == "interpolado_loglineal")))


def build_valencia() -> pd.DataFrame:
    VAL_ROWS.clear(); VAL_SRC.clear(); VAL_META.clear()
    V = "València (municipio)"
    P = "Provincia de València"
    C = "Comunitat Valenciana"
    E = "España"

    # --- Series ya existentes (MIVAU, INE IPV, INE IPVA) ---
    tas_m = read_raw("mivau_valor_tasado_municipios.csv", ["fecha", "serie", "valor"])
    tas = read_raw("mivau_valor_tasado_nacional_ccaa_prov.csv", ["fecha", "serie", "valor"])
    tx_m = read_raw("mivau_transacciones_municipios.csv", ["fecha", "serie", "valor"])
    tx_t = read_raw("mivau_transacciones_total.csv", ["fecha", "serie", "valor"])
    tx_e = read_raw("mivau_transacciones_extranjeros.csv", ["fecha", "serie", "valor"])
    ipv = add_geo(read_raw("ine_ipv_80270.csv", ["fecha", "serie", "valor", "nombre"]))
    ipva = add_geo(read_raw("ine_ipva_municipal.csv", ["fecha", "serie", "valor", "nombre"]))

    val_add(V, "p_tasado", ser_trimestral(by_serie(tas_m, "valor_tasado_mun_valencia")), "trimestral", "xls",
            "sí", "principal", "mivau_valor_tasado_municipios.csv | valor_tasado_mun_valencia")
    val_add(P, "p_tasado", ser_trimestral(by_serie(tas, "valor_tasado_libre_provincia_valencia_valencia")),
            "trimestral", "xls", "sí", "principal",
            "mivau_valor_tasado_nacional_ccaa_prov.csv | valor_tasado_libre_provincia_valencia_valencia")
    val_add(C, "p_tasado", ser_trimestral(by_serie(tas, "valor_tasado_libre_ccaa_comunidad_valenciana")),
            "trimestral", "xls", "sí", "principal",
            "mivau_valor_tasado_nacional_ccaa_prov.csv | valor_tasado_libre_ccaa_comunidad_valenciana")
    val_add(E, "p_tasado", ser_trimestral(by_serie(tas, "valor_tasado_libre_nacional")), "trimestral", "xls",
            "sí", "principal", "mivau_valor_tasado_nacional_ccaa_prov.csv | valor_tasado_libre_nacional")
    val_add(V, "trans_total", ser_trimestral(by_serie(tx_m, "tx_municipio_valencia")), "trimestral", "xls",
            "sí", "principal", "mivau_transacciones_municipios.csv | tx_municipio_valencia")
    val_add(C, "trans_total", ser_trimestral(by_serie(tx_t, "tx_total_ccaa_comunitat_valenciana")), "trimestral",
            "xls", "sí", "principal", "mivau_transacciones_total.csv | tx_total_ccaa_comunitat_valenciana")
    val_add(E, "trans_total", ser_trimestral(by_serie(tx_t, "tx_total_nacional")), "trimestral", "xls", "sí",
            "principal", "mivau_transacciones_total.csv | tx_total_nacional")
    val_add(C, "trans_extranjeros",
            ser_trimestral(by_serie(tx_e, "tx_extranj_residentes_total_ccaa_comunitat_valenciana")), "trimestral",
            "xls", "sí", "principal",
            "mivau_transacciones_extranjeros.csv | tx_extranj_residentes_total_ccaa_comunitat_valenciana")
    val_add(E, "trans_extranjeros", ser_trimestral(by_serie(tx_e, "tx_extranj_residentes_total_nacional")),
            "trimestral", "xls", "sí", "principal",
            "mivau_transacciones_extranjeros.csv | tx_extranj_residentes_total_nacional")
    val_add(C, "ipv", ser_trimestral(by_geo(ipv, "comunitat_valenciana", "General. Índice.")), "trimestral", "api",
            "sí", "principal", "ine_ipv_80270.csv | IPV1392 (Comunitat Valenciana. General. Índice.)")
    val_add(E, "ipv", ser_trimestral(by_geo(ipv, "nacional", "General. Índice.")), "trimestral", "api", "sí",
            "principal", "ine_ipv_80270.csv | IPV1209 (Nacional. General. Índice.)")
    val_add(V, "ipva", ser_anual(by_geo(ipva, "valencia", "Índice. Total.")), "anual", "api", "sí", "principal",
            "ine_ipva_municipal.csv | IPVA8471 (Valencia. Índice. Total.)", transf="nativo anual (sin asignar a trimestre)")

    # --- INE experimental VUT: municipio (ine_vut_valencia_municipio.csv) y provincia (ine_vut_valencia_provincia.csv) ---
    vut_m = read_raw("ine_vut_valencia_municipio.csv", ["fecha", "serie", "valor"])
    vut_p = read_raw("ine_vut_valencia_provincia.csv", ["fecha", "serie", "valor"])
    VUT_NOTA = ("estadística experimental INE (tabla 39366 por la URL del fichero); publicación semestral: "
                "feb y ago -> T1 y T3 (hasta 2024-08); desde 2024-11 la publicación es en may y nov -> T2 y T4 "
                "(2024-11, 2025-05, 2025-11, 2026-05). Sin interpolar; 2024T3 y 2024T4 distan solo 3 meses; "
                "no comparable en niveles con el registro GVA")
    for terr, df, pre in [(V, vut_m, "ine_vut_valencia_"), (P, vut_p, "ine_vut_valencia_valencia_")]:
        for var, code in [("vut_viviendas_turisticas", "viviendas_turisticas"), ("vut_plazas", "plazas"),
                          ("vut_plazas_por_vivienda", "plazas_por_vivienda"),
                          ("vut_pct_sobre_total", "pct_viv_turisticas_sobre_total")]:
            serie = f"{pre}{code}"
            val_add(terr, var, ser_trimestral(by_serie(df, serie)), "semestral irregular (feb/ago -> T1/T3 hasta 2024-08; may/nov -> T2/T4 desde 2024-11)", "api",
                    "plausibilidad", "robustez", f"{'ine_vut_valencia_municipio.csv' if terr == V else 'ine_vut_valencia_provincia.csv'} | {serie}",
                    transf="asignado desde semestral: feb->T1, ago->T3 (hasta 2024-08); may->T2, nov->T4 (desde 2024-11)",
                    nota=VUT_NOTA, metodo="anual_asignado")

    # --- Padron de València ciudad (INE): total DPOP 1996-2025; nacionalidad 1998-2022 ---
    pad = read_raw("ine_padron_valencia.csv", ["fecha", "serie", "valor"])
    pvn = read_raw("ine_padron_vlc_nacionalidad.csv", ["fecha", "serie", "valor"])

    def pvn_s(grupo: str) -> pd.Series:
        return by_serie(pvn, f"vlc_46250|Ambos sexos|{grupo}")

    total_dpop = by_serie(pad, "DPOP21796")
    CHECK["vlc_total_dpop_vs_padron_nac_max_dif"] = float(
        (total_dpop.loc[pvn_s("Total").index.intersection(total_dpop.index)] -
         pvn_s("Total").loc[pvn_s("Total").index.intersection(total_dpop.index)]).abs().max())
    CHECK["vlc_esp_mas_ext_vs_total_max_dif"] = float(
        (pvn_s("Total") - pvn_s("Española") - pvn_s("Extranjera")).abs().max())
    val_add(V, "pob_total", ser_anual(total_dpop), "anual (1 ene)", "api", "sí", "principal",
            "ine_padron_valencia.csv | DPOP21796 (València. Total. Total habitantes.)")
    VLC_NAC_NOTA = "PC-Axis INE (padrón continuo, tabla 33946); 1998-2022 (2023-2025 no publicado por nacionalidad a nivel municipal)"
    val_add(V, "pob_espanola", ser_anual(pvn_s("Española")), "anual (1 ene)", "xls", "sí", "principal",
            "ine_padron_vlc_nacionalidad.csv | vlc_46250|Ambos sexos|Española", nota=VLC_NAC_NOTA)
    val_add(V, "pob_extranjera", ser_anual(pvn_s("Extranjera")), "anual (1 ene)", "xls", "sí", "principal",
            "ine_padron_vlc_nacionalidad.csv | vlc_46250|Ambos sexos|Extranjera", nota=VLC_NAC_NOTA)
    for grupo, var in [("Total América", "pob_vlc_america"), ("Total Asia", "pob_vlc_asia"),
                       ("Total Europa", "pob_vlc_europa"), ("Total África", "pob_vlc_africa"),
                       ("Alemania", "pob_vlc_alemania"), ("Reino Unido", "pob_vlc_reino_unido")]:
        val_add(V, var, ser_anual(pvn_s(grupo)), "anual (1 ene)", "xls", "sí", "robustez",
                f"ine_padron_vlc_nacionalidad.csv | vlc_46250|Ambos sexos|{grupo}",
                nota="grupo con cobertura completa 1998-2022 (25 años)")

    # --- GVA padron extranjeros (contraste) ---
    gva_pad = read_raw("gva_padron_extranjeros_municipio.csv", ["fecha", "serie", "valor"])
    gva_ext = by_serie(gva_pad, "padron_pob_extranjera_mun_46250")
    ine_ext = pvn_s("Extranjera")
    comunes = gva_ext.index.intersection(ine_ext.index)
    dif = (gva_ext.loc[comunes] - ine_ext.loc[comunes]).dropna()
    CHECK["gva_ext_vs_ine_ext_max_dif"] = float(dif.abs().max())
    CHECK["gva_ext_vs_ine_ext_n"] = int(len(dif))
    val_add(V, "pob_extranjera_gva", ser_anual(gva_ext), "anual (1 ene)", "api",
            "sí" if float(dif.abs().max()) == 0 else "plausibilidad", "robustez",
            "gva_padron_extranjeros_municipio.csv | padron_pob_extranjera_mun_46250",
            error_max=f"{dif.abs().max():.0f} personas frente al padrón INE nacionalidad ({len(dif)} años)",
            nota="contraste de transcripción: IVE/GVA frente al padrón INE por nacionalidad. Ambos publican el mismo padrón municipal, así que NO es un contraste independiente; 2005-2022")

    # --- SERPAVI València ciudad (municipio 46250) y agregado de distritos ---
    sp_mun = read_raw("pdf/serpavi_municipios_46.csv", ["fecha", "serie", "valor"])
    val_add(V, "serpavi_vc_mediana", ser_anual(by_serie(sp_mun, "SERPAVI_MUN_46250_VC_alquiler_m2_mediana")),
            "anual", "xls", "plausibilidad", "principal",
            "serpavi_municipios_46.csv | SERPAVI_MUN_46250_VC_alquiler_m2_mediana",
            error_max="6,43 pp frente al IPVA València 2019 (no independiente: ambos AEAT)",
            nota="alquiler €/m²/mes, vivienda colectiva (VC); mediana municipal")
    dist = read_raw("pdf/serpavi_valencia_distritos.csv", ["fecha", "serie", "valor"])
    md = dist[dist["serie"].str.match(r"^SERPAVI_DIST_\d+_VC_alquiler_m2_mediana$")].copy()
    nd = dist[dist["serie"].str.match(r"^SERPAVI_DIST_\d+_VC_n_contratos_recuento$")].copy()
    md["cod"] = md["serie"].str.extract(r"SERPAVI_DIST_(\d+)_")[0]
    nd["cod"] = nd["serie"].str.extract(r"SERPAVI_DIST_(\d+)_")[0]
    jj = md[["fecha", "cod", "valor"]].merge(nd[["fecha", "cod", "valor"]], on=["fecha", "cod"],
                                             suffixes=("_med", "_n")).dropna()
    jj["w"] = jj["valor_med"] * jj["valor_n"]
    agg = jj.groupby("fecha").agg(w=("w", "sum"), n=("valor_n", "sum"), ndist=("cod", "nunique"))
    CHECK["serpavi_dist_n_distritos"] = sorted(set(agg["ndist"].astype(int)))
    val_add(V, "serpavi_vc_dist_agg", ser_anual(agg["w"] / agg["n"]), "anual", "derivado", "plausibilidad",
            "robustez", "serpavi_valencia_distritos.csv | SERPAVI_DIST_*_VC_alquiler_m2_mediana (ponderado por n_contratos VC)",
            transf="derivado: media de medianas de distritos ponderada por nº contratos VC (no es una mediana)",
            nota="19 distritos; unidades pequeñas (mínimo 10 viviendas): descriptivo")

    # --- SERPAVI por distrito de València (19 distritos, 2011-2024, xls): rol descriptivo ---
    # El raw no trae nombres de distrito (la columna 'nombre' es 'Valencia' en todas las filas): se usa el código.
    # serpavi_validacion.csv no tiene fila de contraste por distrito: validado = plausibilidad.
    SP_DIST_NOTA = ("SERPAVI por distrito (xls, 2011-2024): descriptivo, no entra en los modelos. Sin fila de contraste "
                    "por distrito en serpavi_validacion.csv (validado = plausibilidad). VU sin dato en algunos distritos-años (no se rellena)")
    SP_DIST_VAR = {"alquiler_m2_mediana": ("mediana", "€/m²/mes"), "alquiler_m2_p25": ("p25", "€/m²/mes"),
                   "alquiler_m2_p75": ("p75", "€/m²/mes"), "n_contratos_recuento": ("n_contratos", "viviendas (contratos)")}
    sp_dd = read_raw("pdf/serpavi_valencia_distritos.csv", ["fecha", "serie", "valor"])
    sp_dd = sp_dd[sp_dd["serie"].str.match(r"^SERPAVI_DIST_\d+_V[CU]_(alquiler_m2_mediana|alquiler_m2_p25|alquiler_m2_p75|n_contratos_recuento)$")].copy()
    sp_dd["cod"] = sp_dd["serie"].str.extract(r"SERPAVI_DIST_(\d+)_")[0]
    sp_dd["tip"] = sp_dd["serie"].str.extract(r"_(VC|VU)_")[0].str.lower()
    sp_dd["est"] = sp_dd["serie"].str.extract(r"_V[CU]_(\w+)$")[0]
    for (cod, tip, est), g in sp_dd.groupby(["cod", "tip", "est"]):
        estad, _ = SP_DIST_VAR[est]
        serie_txt = g["serie"].iloc[0]
        val_add(f"València distrito {cod}", f"serpavi_dist_{tip}_{estad}",
                ser_anual(g["valor"].set_axis(pd.DatetimeIndex(g["fecha"]))),
                "anual", "xls", "plausibilidad", "descriptivo",
                f"serpavi_valencia_distritos.csv | {serie_txt}",
                transf="nativo (tipología " + ("vivienda colectiva" if tip == "vc" else "vivienda unifamiliar") + ")",
                nota=SP_DIST_NOTA)

    # --- Notariado: València ciudad, Total general (NO sumar nacionalidades: 4T2022 no es aditiva) ---
    nmun = read_raw("pdf/notariado_cv_municipios_anual.csv", ["fecha", "serie", "valor", "territorio", "nacionalidad"])
    nv = nmun[(nmun["territorio"] == "Valencia") & (nmun["nacionalidad"] == "Total general")]
    val_add(V, "notariado_viv_extranj", ser_anual(nv["valor"].set_axis(pd.DatetimeIndex(nv["fecha"]))),
            "anual (edición 4T del año)", "pdf", "sí", "robustez",
            "notariado_cv_municipios_anual.csv | Valencia / Total general",
            error_max="0 frente a relectura independiente del revisor de los 5 PDF (docs/revision_f1.md §2); completitud 19/19 municipios",
            nota="viviendas compradas por extranjeros (notarios). Solo 'Total general'. Corregido tras el fallo de "
                 "4T2022/4T2025; validado por relectura independiente del revisor (N = 5 años: rol robustez)")

    # --- Notariado CV provincia de Valencia trimestral (PDF, edición 4T2025) ---
    nprov = read_raw("pdf/notariado_cv_prov_trimestral.csv", ["fecha", "serie", "valor", "territorio"])
    nprov = nprov[nprov["territorio"] == "Valencia"]
    NPROV_NOTA = ("edición 4T2025; la remisión del IUI del 4T2025 es 99,90 %; no mezclar niveles con MIVAU "
                  "(ratio 1,06-1,20)")
    for var, serie, unid in [("notariado_viv_esp_prov", "viv_vendidas_esp", "viviendas"),
                             ("notariado_viv_ext_prov", "viv_vendidas_ext", "viviendas"),
                             ("notariado_cuantia_esp_prov", "cuantia_media_esp", "€"),
                             ("notariado_cuantia_ext_prov", "cuantia_media_ext", "€")]:
        val_add(P, var, ser_trimestral(by_serie(nprov, serie)), "trimestral", "pdf", "sí", "principal",
                f"notariado_cv_prov_trimestral.csv | {serie} (Valencia)",
                error_max="0 frente a totales anuales del PDF; suma 3 prov. vs CGN: 7,5 % (1.463)",
                nota=NPROV_NOTA)

    # --- GVA VUT registro (stock fin de trimestre 2010-2024; NO se encadena con la lista 2026) ---
    gva_vut = read_raw("gva_vut_municipio.csv", ["fecha", "serie", "valor"])
    GVA_NOTA = ("registro administrativo (GVA, CKAN); stock = último mes del trimestre; 2010-2024; "
                "saltos regulatorios 2016-2019, 2021 y purga 2025-26; no encadenar con vut_foto (lista 2026)")
    for terr, serie, rol, extra in [
            (V, "vut_stock_mun_46250", "robustez", "municipio València"),
            (P, "vut_stock_prov_46", "principal", "condicionado a los saltos regulatorios"),
            (C, "vut_stock_cv", "principal", "condicionado a los saltos regulatorios")]:
        val_add(terr, "vut_stock_gva", ser_periodo_q(m_end(by_serie(gva_vut, serie))), "trimestral (fin de trimestre)",
                "api", "sí", rol, f"gva_vut_municipio.csv | {serie}",
                error_max="0 frente a Σ municipios (CV) y frente a la reconstrucción altas-bajas (identidad contable: no independiente; ver validacion_gva.csv)",
                transf="stock mensual: valor de fin de trimestre", nota=f"{GVA_NOTA}. {extra}", metodo="fin_periodo")

    out = pd.DataFrame(VAL_ROWS, columns=["territorio", "periodo", "frecuencia", "variable", "valor", "origen",
                                          "rol", "validado", "metodo", "interp"])
    return out.sort_values(["territorio", "variable", "periodo"]).reset_index(drop=True)


# ----------------------------------------------------------------------------
# Panel anual CCAA (C2): panel_ccaa_a.csv, para el IV shift-share de F3
# ----------------------------------------------------------------------------

ANIOS = list(range(2002, 2026))


def europa_sin_espana(out: pd.DataFrame) -> pd.Series:
    """Grupo 'Europa sin España' coherente a lo largo del quiebre UE28/UE27 (salida del Reino Unido, 2020/2021).
    77019 publica en cada año UNA de dos familias de grupos, nunca ambas:
      2002-2020: UE28 sin España + País de Europa menos UE28
      2021-2025: UE27 sin España + País de Europa menos UE27
    El grupo es la suma de los grupos europeos disponibles de la familia completa de cada año (NaN si falta
    algún componente). Comprobación (CHECK): coincide con pob_extranj − Σ grupos no europeos (≤ 2 personas)."""
    f28 = ["pob_ue28_sin_espana", "pob_europa_no_ue28"]
    f27 = ["pob_ue27_sin_espana", "pob_europa_no_ue27"]
    ok28 = out[f28].notna().all(axis=1)
    ok27 = out[f27].notna().all(axis=1)
    assert not (ok28 & ok27).any(), "ambas familias UE28 y UE27 presentes en el mismo año"
    res = np.where(ok28, out[f28].sum(axis=1), np.where(ok27, out[f27].sum(axis=1), np.nan))
    return pd.Series(res, index=out.index)


def build_panel_a(panel: pd.DataFrame, pob77: pd.DataFrame) -> pd.DataFrame:
    idx = pd.MultiIndex.from_product([[c for c, _, _ in CCAA], ANIOS], names=["codigo_ine_ccaa", "anio"])
    out = pd.DataFrame(index=idx)

    # Stock 77019 a 1 de enero (anual nativo; sin interpolar)
    for grp, var in GRUPO_VAR.items():
        x = pob77[pob77["grupo"] == grp].set_index(["codigo_ine_ccaa", "anio"])["pob_stock"]
        out[var] = x.reindex(idx)
    out["pob_europa_sin_espana"] = europa_sin_espana(out)

    # Agregados anuales de trimestres completos (4 trimestres obligatorios; si falta alguno, NaN)
    AGG = [("ipv", "mean", "agregado_media"), ("p_tasado", "mean", "agregado_media"),
           ("ocupados", "mean", "agregado_media"), ("compraventas", "sum", "agregado_suma"),
           ("trans_total", "sum", "agregado_suma"), ("trans_extranjeros", "sum", "agregado_suma"),
           ("visados", "sum", "agregado_suma"), ("terminadas", "sum", "agregado_suma"),
           ("ipc_alquiler", "mean", "agregado_media")]
    q = panel[["codigo_ine_ccaa", "trimestre"] + [v for v, _, _ in AGG]].copy()
    q["anio"] = q["trimestre"].str[:4].astype(int)
    g = q.groupby(["codigo_ine_ccaa", "anio"])
    for v, how, _ in AGG:
        n = g[v].count()
        val = g[v].mean() if how == "mean" else g[v].sum()
        out[v] = val.where(n == 4).reindex(idx)
        out[f"{v}_metodo"] = mcol(out[v], dict((x, m) for x, _, m in AGG)[v])

    # SERPAVI CCAA: mediana alquiler €/m²/mes, vivienda colectiva (anual nativo)
    sc = read_raw("pdf/serpavi_ccaa.csv", ["fecha", "serie", "valor", "codigo", "tipologia", "variable", "estadistico"])
    sc = sc[(sc["tipologia"] == "VC") & (sc["variable"] == "alquiler_m2") & (sc["estadistico"] == "mediana")].copy()
    sc["anio"] = sc["fecha"].dt.year
    sc = sc.rename(columns={"codigo": "codigo_ine_ccaa"}).set_index(["codigo_ine_ccaa", "anio"])["valor"]
    out["serpavi_vc_mediana"] = sc.reindex(idx)

    # Notariado CGN: compras de extranjeros (vivienda libre), suma de los dos semestres (solo si ambos existen)
    cgn = read_raw("pdf/notariado_cgn_extranjeros_semestral.csv",
                   ["fecha", "serie", "valor", "tabla", "territorio", "categoria"])
    cg = cgn[(cgn["tabla"] == "T2") & (cgn["serie"] == "op_viv_libre_extranjeros") & (cgn["categoria"] == "Extranjero")].copy()
    cg["codigo_ine_ccaa"] = cg["territorio"].map(CGN_NAME2COD)
    cg = cg[cg["codigo_ine_ccaa"].notna()].copy()
    cg["anio"] = cg["fecha"].dt.year
    gg = cg.groupby(["codigo_ine_ccaa", "anio"])["valor"]
    out["notariado_cgn_extranj"] = gg.sum().where(gg.count() == 2).reindex(idx)
    out["notariado_cgn_extranj_metodo"] = mcol(out["notariado_cgn_extranj"], "agregado_suma")

    # Registradores: % compras de extranjeros por CCAA (serie 8 años, ultima edicion por año)
    er = read_raw("pdf/registradores_eri_anuario.csv", ["fecha", "serie", "valor", "nivel", "territorio", "edicion"])
    er = er[(er["serie"] == "viv_pct_compras_extranjeros_serie8a") & (er["nivel"] == "ccaa")].copy()
    er["codigo_ine_ccaa"] = er["territorio"].map(lambda t: ccaa_from_slug(slug(t)))
    er = er[er["codigo_ine_ccaa"].notna()].copy()
    er["anio"] = er["fecha"].dt.year
    er = er.sort_values("edicion").drop_duplicates(["codigo_ine_ccaa", "anio"], keep="last")
    out["registradores_extranj_pct"] = er.set_index(["codigo_ine_ccaa", "anio"])["valor"].reindex(idx)

    out = out.reset_index()
    out["ccaa"] = out["codigo_ine_ccaa"].map(COD2NAME)
    out["fecha"] = [f"{a}-01-01" for a in out["anio"]]
    out = out.sort_values(["codigo_ine_ccaa", "anio"]).reset_index(drop=True)

    LN = ["pob_total", "pob_extranj", "pob_espanola"] + POB_GRUPOS + ["pob_europa_sin_espana", "ipv", "p_tasado",
                                                                    "ocupados", "compraventas", "trans_total",
                                                                    "trans_extranjeros", "visados", "terminadas",
                                                                    "ipc_alquiler", "serpavi_vc_mediana",
                                                                    "notariado_cgn_extranj"]
    for v in LN:
        out[f"ln_{v}"] = np.log(out[v].where(out[v] > 0))
        out[f"d_ln_{v}"] = out.groupby("codigo_ine_ccaa")[f"ln_{v}"].diff()
    out["d_registradores_extranj_pct"] = out.groupby("codigo_ine_ccaa")["registradores_extranj_pct"].diff()

    # Banderas: <var>_metodo (categorica) y <var>_interp = (metodo == interpolado_loglineal); aqui no hay interpolacion
    metodos = [c for c in out.columns if c.endswith("_metodo")]
    for m in metodos:
        out[m.replace("_metodo", "_interp")] = interp_de(out[m])

    lv = [v for v in GRUPO_VAR.values()] + ["pob_europa_sin_espana", "ipv", "p_tasado", "ocupados", "compraventas",
                                             "trans_total", "trans_extranjeros", "visados", "terminadas",
                                             "ipc_alquiler", "serpavi_vc_mediana", "notariado_cgn_extranj",
                                             "registradores_extranj_pct"]
    lv = list(dict.fromkeys(lv))
    flags = [f"{m.replace('_metodo', '')}_{k}" for m in metodos for k in ("metodo", "interp")]
    cols = ["ccaa", "codigo_ine_ccaa", "anio", "fecha"] + lv + flags + \
           [f"ln_{v}" for v in LN] + [f"d_ln_{v}" for v in LN] + ["d_registradores_extranj_pct"]
    return out[cols]


# ----------------------------------------------------------------------------
# Panel anual nacional (nacional_a.csv): medias/sumas anuales de nacional_q + flujos anuales nativos
# ----------------------------------------------------------------------------

def build_nacional_a(nac: pd.DataFrame) -> pd.DataFrame:
    """nac: salida de finalize_nacional (trimestral). Medias y sumas solo con 4 trimestres completos.
    inmig_anual_eurostat e inmig_anual son flujos anuales nativos (sin agregar): metodo 'observado'."""
    q = nac.copy()
    q["anio"] = q["trimestre"].str[:4].astype(int)
    g = q.groupby("anio")
    out = pd.DataFrame(index=pd.Index(range(int(q["anio"].min()), int(q["anio"].max()) + 1), name="anio"))
    AGG = [("ipv", "mean", "agregado_media"), ("ocupados", "mean", "agregado_media"),
           ("pob_extranj", "mean", "agregado_media"), ("hogares_epa", "mean", "agregado_media"),
           ("terminadas", "sum", "agregado_suma"), ("visados", "sum", "agregado_suma")]
    for v, how, met in AGG:
        n = g[v].count().reindex(out.index)
        val = (g[v].mean() if how == "mean" else g[v].sum()).reindex(out.index)
        out[v] = val.where(n == 4)
        out[f"{v}_metodo"] = mcol(out[v], met)
    for v in ["inmig_anual_eurostat", "inmig_anual"]:
        out[v] = g[v].first().reindex(out.index)  # un único valor anual no NaN por año
        out[f"{v}_metodo"] = mcol(out[v], "observado")
    out["quiebre_emcr_2021"] = [int(a >= 2021) for a in out.index]
    out["quiebre_epa_2021"] = [int(a >= 2021) for a in out.index]
    LN = ["ipv", "ocupados", "pob_extranj", "hogares_epa", "terminadas", "visados", "inmig_anual_eurostat", "inmig_anual"]
    for v in LN:
        out[f"ln_{v}"] = np.log(out[v].where(out[v] > 0))
        out[f"d_ln_{v}"] = out[f"ln_{v}"].diff()
    for m in [c for c in out.columns if c.endswith("_metodo")]:
        out[m.replace("_metodo", "_interp")] = interp_de(out[m])
    out = out.reset_index()
    out = out[out[["ipv", "ocupados", "pob_extranj", "hogares_epa", "terminadas", "visados",
                   "inmig_anual_eurostat", "inmig_anual"]].notna().any(axis=1)].copy()
    out.insert(1, "fecha", [f"{a}-01-01" for a in out["anio"]])
    return out.reset_index(drop=True)


# ----------------------------------------------------------------------------
# Validación del registro GVA (validacion_gva.csv): VUT y padrón
# ----------------------------------------------------------------------------

def build_validacion_gva(pad_ext: pd.DataFrame | None = None) -> pd.DataFrame:
    """Contrastes del registro GVA. Columna 'independiente': 'sí' solo si el contraste usa una fuente distinta;
    'no independiente' si ambos lados proceden del mismo registro/padrón (consistencia interna);
    'no comparable' si la definición o la fecha no coinciden (solo plausibilidad)."""
    R = []

    def add(bloque, check, territorio, n, error_max, independiente, nota, valor=""):
        R.append(dict(bloque=bloque, check=check, territorio=territorio, n_obs=n,
                      error_max=error_max, valor_ref=valor, independiente=independiente, nota=nota))

    gv = read_raw("gva_vut_municipio.csv", ["fecha", "serie", "valor"])
    gv = gv.drop_duplicates(["fecha", "serie"], keep="last")
    wide = gv.pivot(index="fecha", columns="serie", values="valor").sort_index()
    mun_stock = wide[[c for c in wide.columns if c.startswith("vut_stock_mun_")]]
    mun46 = [c for c in mun_stock.columns if c.startswith("vut_stock_mun_46")]
    alt_cv = wide["vut_altas_cv"]

    # 1) CV = Σ municipios (stock VUT)
    suma_cv = mun_stock.sum(axis=1, min_count=1)
    dif_cv = (wide["vut_stock_cv"] - suma_cv).dropna()
    add("VUT stock", "CV (vut_stock_cv) − Σ municipios (vut_stock_mun_*)", "Comunitat Valenciana",
        int(len(dif_cv)), float(dif_cv.abs().max()), "no independiente (mismo registro GVA)",
        f"{mun_stock.shape[1]} municipios con serie; error máximo en valor absoluto (viviendas) sobre "
        f"{len(dif_cv)} meses comunes", valor=f"{int(wide['vut_stock_cv'].dropna().iloc[-1])}")

    # 2) Provincia 46 = Σ municipios de la provincia
    suma_46 = mun_stock[mun46].sum(axis=1, min_count=1)
    dif_46 = (wide["vut_stock_prov_46"] - suma_46).dropna()
    add("VUT stock", "Provincia 46 (vut_stock_prov_46) − Σ municipios 46*", "Provincia de València",
        int(len(dif_46)), float(dif_46.abs().max()), "no independiente (mismo registro GVA)",
        f"{len(mun46)} municipios de la provincia; error máximo sobre {len(dif_46)} meses")

    # 3) Stock 'reconstruido' por altas − bajas. La baja implícita es altas − Δstock: el stock reconstruido es
    #    identidad contable, no un contraste; se reportan los meses con bajas implícitas incoherentes.
    for terr, st, al in [("Comunitat Valenciana", wide["vut_stock_cv"], alt_cv),
                         ("Municipio de València (46250)", wide.get("vut_stock_mun_46250"), wide.get("vut_altas_mun_46250"))]:
        if st is None or al is None:
            continue
        dst = st.diff()
        baja = (al - dst).dropna()
        rec = st.iloc[0] + (al - baja).fillna(0).cumsum().reindex(st.index)  # = stock por identidad
        dif_rec = (rec - st).dropna()
        n_neg = int((baja < 0).sum())
        n_pos = int((baja > 0).sum())
        add("VUT stock", "Stock reconstruido (altas acumuladas − bajas implícitas) vs stock publicado", terr,
            int(len(dif_rec)), float(dif_rec.abs().max()) if len(dif_rec) else np.nan,
            "no independiente (identidad contable: las bajas se derivan del propio stock)",
            f"Bajas implícitas = altas − Δstock. Meses con bajas implícitas < 0 (stock sube más que altas): {n_neg}. "
            f"Meses con bajas > 0: {n_pos} de {len(baja)}.")

    # 4) Publicado: INE VUT (municipio y provincia, semestral) vs stock GVA a fin de mes en los mismos meses
    ine_m = read_raw("ine_vut_valencia_municipio.csv", ["fecha", "serie", "valor"])
    ine_p = read_raw("ine_vut_valencia_provincia.csv", ["fecha", "serie", "valor"])
    for terr, df, serie, gva_col in [
            ("València (municipio) vs 46250", ine_m, "ine_vut_valencia_viviendas_turisticas", "vut_stock_mun_46250"),
            ("Provincia de València vs 46", ine_p, "ine_vut_valencia_valencia_viviendas_turisticas", "vut_stock_prov_46")]:
        ine = by_serie(df, serie)
        ine.index = ine.index.to_period("M").to_timestamp()
        gv_s = wide[gva_col].copy()
        gv_s.index = pd.to_datetime(gv_s.index).to_period("M").to_timestamp()
        com = pd.concat([ine.rename("ine"), gv_s.rename("gva")], axis=1).dropna()
        ratio = (com["ine"] / com["gva"])
        add("VUT publicado", "INE VUT (tabla 39366, semestral) / stock GVA a fin de mes", terr, int(len(com)),
            np.nan, "no comparable (definición, fecha y ámbito distintos): solo plausibilidad",
            f"ratio INE/GVA en {len(com)} meses comunes: mín {ratio.min():.3f}, máx {ratio.max():.3f}",
            valor="")

    # 5) vut_foto_* (lista vigente, fecha de modificación del recurso): nota, no serie temporal
    foto_cv = wide["vut_foto_cv"].dropna()
    foto_mun = wide[[c for c in wide.columns if c.startswith("vut_foto_mun_")]]
    suma_foto = foto_mun.sum(axis=1, min_count=1)
    dif_foto = (wide["vut_foto_cv"] - suma_foto).dropna()
    NOTA_FOTO = ("lista vigente (recurso GVA tur-gestur-vt; fecha = modificación del recurso). No es serie temporal "
                 "y no es encadenable con vut_stock_* 2010-2024 (renumeración de signaturas y purga de 2025-26: "
                 "101.171 en 2024-12 frente a 90.122 en la lista de 2026). Excluida de valencia.csv y de los modelos.")
    add("VUT foto (nota)", "vut_foto_cv − Σ vut_foto_mun_*", "Comunitat Valenciana", int(len(dif_foto)),
        float(dif_foto.abs().max()) if len(dif_foto) else np.nan, "no independiente (mismo recurso GVA)",
        f"{foto_mun.shape[1]} municipios con foto. " + NOTA_FOTO, valor=str(int(foto_cv.iloc[-1])) if len(foto_cv) else "")
    for c in ["vut_foto_prov_46", "vut_foto_prov_03", "vut_foto_prov_12"]:
        s_ = wide[c].dropna() if c in wide else pd.Series(dtype=float)
        if len(s_):
            add("VUT foto (nota)", f"{c} (último valor)", c.replace("vut_foto_prov_", "Provincia "),
                int(len(s_)), np.nan, "no comparable (foto, no serie)", NOTA_FOTO, valor=str(int(s_.iloc[-1])))

    # 6) Padrón GVA frente a INE (València ciudad, 46250): NO independiente (mismo padrón municipal)
    pg = read_raw("gva_padron_extranjeros_municipio.csv", ["fecha", "serie", "valor"])
    pg = pg.drop_duplicates(["fecha", "serie"], keep="last")
    pgw = pg.pivot(index="fecha", columns="serie", values="valor").sort_index()
    pin = read_raw("ine_padron_valencia.csv", ["fecha", "serie", "valor"])
    pvn = read_raw("ine_padron_vlc_nacionalidad.csv", ["fecha", "serie", "valor"])
    tot_ine = by_serie(pin, "DPOP21796")
    tot_gva = pgw["padron_pob_total_mun_46250"].dropna()
    tot_gva.index = pd.DatetimeIndex(tot_gva.index)
    com_t = tot_gva.index.intersection(tot_ine.index)
    dt_ = (tot_gva.loc[com_t] - tot_ine.loc[com_t]).abs()
    add("Padrón", "GVA población total 46250 vs INE DPOP21796 (València)", "València (municipio)", int(len(dt_)),
        float(dt_.max()), "no independiente (ambos publican el padrón municipal)",
        "0 de diferencia = coincidencia de la misma cifra oficial, no un contraste externo")
    ext_gva = pgw["padron_pob_extranjera_mun_46250"].dropna()
    ext_gva.index = pd.DatetimeIndex(ext_gva.index)
    ext_ine = by_serie(pvn, "vlc_46250|Ambos sexos|Extranjera")
    com_e = ext_gva.index.intersection(ext_ine.index)
    de_ = (ext_gva.loc[com_e] - ext_ine.loc[com_e]).abs()
    add("Padrón", "GVA población extranjera 46250 vs INE padrón por nacionalidad (Extranjera)", "València (municipio)",
        int(len(de_)), float(de_.max()), "no independiente (mismo padrón municipal; el total es suma de grupos)",
        "Contraste de transcripción, no independiente. Ver validado/error_max de valencia.csv")
    CHECK["gva_padron_total_vs_ine_max"] = float(dt_.max())

    return pd.DataFrame(R, columns=["bloque", "check", "territorio", "n_obs", "error_max", "valor_ref",
                                    "independiente", "nota"])


def metodo_resumen(df: pd.DataFrame) -> list[tuple[str, dict[str, int]]]:
    """Recuento de filas por valor de <var>_metodo para un fichero (NaN = sin dato, no se cuenta)."""
    out = []
    for c in [c for c in df.columns if c.endswith("_metodo")]:
        vc = df[c].dropna().value_counts()
        out.append((c, {k: int(vc.get(k, 0)) for k in METODOS if int(vc.get(k, 0)) > 0}))
    return out


# ----------------------------------------------------------------------------
# Diccionario de variables: metadatos (origen, validado, error_max, rol)
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
    ("deflactor", "Derivada: INE CNT (SA)", "ine_cnt_pib_oferta_corrientes.csv / ine_cnt_pib_oferta_volumen.csv", "CNTR6597 (PIB mercado, corrientes, SA, M€) / CNTR6652 (PIB mercado, volumen encadenado, SA, índice)", "índice 2020=100", "trimestral (1995T1+)", "cociente nominal SA / volumen SA, reescalado a media 2020 = 100"),
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
    ("pob_total", "INE ECP, serie nacional", "ine_ecp_nacional.csv", "ECP320 (Total Nacional. Todas las edades. Total.)", "personas (a 1 de enero/julio, stock)", "semestral 1971-2020 (ene/jul); trimestral 2021+", "stock: trimestre de la fecha; trimestres intermedios interpolados (log-lineal entre observaciones)"),
    ("pob_extranj", "INE ECP, serie nacional", "ine_ecp_nacional.csv", "ECP701 (Total Nacional. Extranjera. Todas las edades. Total.)", "personas (stock)", "semestral 2002-2020; trimestral 2021+", "como pob_total"),
    ("hogares_epa", "INE EPA, tabla 65269 (hogares, total)", "ine_epa_hogares.csv", "EPA430446 (Hogares. Total Nacional. Ambos sexos. Total. Total.)", "miles de hogares (valor en miles, EPA)", "trimestral (2002T1+)", "nativo; serie PRINCIPAL de hogares"),
    ("hogares_ecp", "INE ECP, tabla 60131", "ine_hogares_60131.csv", "ECP355533 (Total Nacional. Total. Hogares en viviendas familiares.)", "hogares (UNIDADES, no miles: 1.000 veces hogares_epa)", "trimestral (2021T1+)", "nativo; sin interpolación ni retropolación; ROBUSTEZ (antes 'hogares')"),
    ("inmig_anual_eurostat", "Eurostat migr_imm1ctz (inmigración anual, ciudadanía TOTAL)", "eurostat_inmigracion_anual.csv", "migr_imm1ctz, citizen=TOTAL, age=TOTAL, sex=T, geo=ES", "personas (flujo anual)", "anual (1998-2024)", "anual asignado a T4 (sin interpolar)"),
    ("inmig_anual", "INE EMCR, tabla 69687 (ANUAL)", "ine_migraciones_total_anual.csv", "EM1765217 (Todas las edades. Total. Dato base. Inmigraciones procedentes del extranjero.)", "personas (flujo anual)", "anual (2021-2024)", "anual asignado solo al primer trimestre del año (no trimestralizar)"),
    ("registradores_compraventas_anual", "Colegio de Registradores, OpenData (compraventas viviendas, nacional)", "pdf/registradores_opendata_anual.csv", "compraventas_viv_num (nivel nacional)", "viviendas (año natural)", "anual (2007-2025)", "anual = T4 de la suma móvil de 4 trimestres; asignado a T4, sin interpolar"),
    ("registradores_extranj_pct", "Colegio de Registradores, Anuario ERI (% compras de extranjeros)", "pdf/registradores_eri_anuario.csv", "viv_pct_compras_extranjeros (nivel nacional)", "% de compraventas", "anual (2023-2025)", "asignado a T4, sin interpolar"),
    ("notariado_cgn_extranj", "Consejo General del Notariado, CIEN (anexo XLSX)", "pdf/notariado_cgn_extranjeros_semestral.csv", "T1 op_viv_libre, categoría 'Extranjero', España", "operaciones (vivienda libre)", "semestral (2007S1+)", "S1 -> T2, S2 -> T4; sin interpolar"),
    ("serpavi_esp_constante", "MIVAU-SERPAVI (XLSX) → agregado propio", "pdf/serpavi_esp_agregado.csv", "SERPAVI_ESP_VC_alquiler_m2_mediana_pond_composicion_constante", "€/m²/mes (alquiler, VC)", "anual (2011-2024)", "media ponderada de medianas de 17 CCAA con pesos fijos; asignado a T4; sin interpolar"),
    ("pob_extranj_ccaa_sum", "Derivada: suma de 17 CCAA de INE 77019", "ine_ecp_ccaa_paises.csv", "ECP701-equivalente por CCAA (suma de panel_ccaa_q$pob_extranj)", "personas (stock)", "trimestral (derivada)", "control: suma de 17 CCAA (sin Ceuta y Melilla) y pob_extranj nacional"),
]

NAC_ORIG = {
    # var: (origen, validado, error_max, rol, nota)
    "ipv": ("api", "sí", "—", "principal", ""), "ipv_nueva": ("api", "sí", "—", "principal", ""),
    "ipv_usada": ("api", "sí", "—", "principal", ""), "ipv15": ("api", "sí", "—", "robustez", "serie base 2015"),
    "p_tasado": ("xls", "sí", "—", "principal", ""), "p_bde": ("xls", "sí", "—", "principal", ""),
    "hpi_eurostat": ("api", "sí", "—", "principal", ""), "ocupados": ("api", "sí", "—", "principal", ""),
    "ocupados_sa": ("derivado", "plausibilidad", "—", "principal", "STL"),
    "renta_hog": ("api", "sí", "—", "principal", ""), "deflactor": ("derivado", "plausibilidad", "—", "principal", "PIB SA corrientes / volumen SA; no es el deflactor oficial del INE"),
    "renta_hog_real": ("derivado", "plausibilidad", "—", "principal", ""),
    "tipo_hip": ("api", "sí", "—", "principal", ""), "euribor": ("api", "sí", "—", "principal", ""),
    "tipo_bce": ("api", "sí", "—", "principal", "escalonado"), "tipo_hip_real": ("derivado", "plausibilidad", "—", "principal", ""),
    "inflacion_deflactor": ("derivado", "plausibilidad", "—", "principal", ""),
    "ipc_alquiler": ("api", "sí", "—", "principal", ""), "ipc_alquiler_yoy": ("api", "sí", "—", "principal", ""),
    "credito_nuevo": ("api", "sí", "—", "principal", ""), "credito_stock": ("api", "sí", "—", "principal", ""),
    "permisos": ("api", "sí", "—", "principal", ""), "costes": ("api", "sí", "—", "principal", ""),
    "prod_constr": ("api", "sí", "—", "principal", ""),
    "visados": ("xls", "plausibilidad", "—", "principal", "proxy MIVAU, no visados CSCAE"),
    "terminadas": ("xls", "plausibilidad", "—", "principal", "proxy MIVAU, no certificados CSCAE"),
    "compraventas": ("api", "sí", "—", "principal", ""), "compraventas_sa": ("derivado", "plausibilidad", "—", "principal", "STL"),
    "trans_total": ("xls", "sí", "—", "principal", ""), "trans_extranjeros": ("xls", "sí", "—", "principal", ""),
    "pob_total": ("api", "plausibilidad", "—", "principal", "semestral hasta 2020; interpolación log-lineal"),
    "pob_extranj": ("api", "plausibilidad", "0 frente a ECP701 de 56936/59585 (trimestres publicados)", "principal", "semestral hasta 2020; interpolación log-lineal"),
    "hogares_epa": ("api", "sí", "EPA 0,4–1,0 % mayor que ECP 60131 en el solape (ver nota)", "principal", "quiebre EPA 2021T1 (quiebre_epa_2021)"),
    "hogares_ecp": ("api", "sí", "—", "robustez", "solo 2021+"),
    "inmig_anual": ("api", "sí", "—", "robustez", "4 observaciones anuales (EMCR); N=4 no sirve como principal"),
    "inmig_anual_eurostat": ("api", "sí", "0 frente a EMCR 2021 (887.960 en ambas)", "principal", "anual TOTAL 1998-2024 asignado a T4; quiebre_emcr_2021"),
    "registradores_compraventas_anual": ("xls", "sí", "0 frente al Anuario 2023-2025; ≤1,4 % frente a INE ETDP", "principal", "solo T4"),
    "registradores_extranj_pct": ("pdf", "sí", "0 (nacionales + extranjeros = 100 %)", "robustez", "anual 2023-2025"),
    "notariado_cgn_extranj": ("xls", "sí", "0 (suma interna); 9,4 % frente a MIVAU (concepto distinto)", "principal", "semestral"),
    "serpavi_esp_constante": ("derivado", "plausibilidad", "4,39 pp frente al IPVA nacional (no independiente)", "robustez", "composición fija: 17 CCAA sin Navarra ni País Vasco"),
    "pob_extranj_ccaa_sum": ("derivado", "plausibilidad", "ver nota", "excluida", "control; no es variable del modelo"),
}

PANEL_META = {
    # var: (origen, validado, error_max, rol)
    "ipv": ("api", "sí", "—", "principal"), "ipv_nueva": ("api", "sí", "—", "principal"),
    "ipv_usada": ("api", "sí", "—", "principal"), "p_tasado": ("xls", "sí", "—", "principal"),
    "ocupados": ("api", "sí", "—", "principal"), "compraventas": ("api", "sí", "—", "principal"),
    "trans_total": ("xls", "sí", "—", "principal"), "trans_extranjeros": ("xls", "sí", "—", "principal"),
    "visados": ("xls", "plausibilidad", "proxy MIVAU", "principal"), "terminadas": ("xls", "plausibilidad", "proxy MIVAU; sin Extremadura", "principal"),
    "ipc_alquiler": ("api", "sí", "—", "principal"),
    "pob_total": ("api", "plausibilidad", "stock 1 ene; T2-T4 interpolados (error de interpolación, ver nacional_q)", "principal"),
    "pob_extranj": ("api", "plausibilidad", "suma 17 CCAA frente a nacional: -2,1 % a +1,3 % (interpolación anual; ver nacional_q)", "principal"),
    "pob_espanola": ("api", "plausibilidad", "stock 1 ene; T2-T4 interpolados", "principal"),
    "epa_pob_total": ("api", "sí", "—", "robustez"),
}

PANEL_A_EXTRA = {
    "serpavi_vc_mediana": ("xls", "plausibilidad", "6,43 pp frente al IPVA València (no independiente)", "principal"),
    "notariado_cgn_extranj": ("xls", "sí", "0 (suma interna de semestres)", "principal"),
    "registradores_extranj_pct": ("pdf", "sí", "0 (suma 100 %; CCAA = España)", "robustez"),
}

NO_USADAS = [
    ("bde_tipo_hipotecario_referencia.csv", "BdE D_1T9H0000 (tipo medio adquisición vivienda libre). Se usa el MIR del BCE según especificación."),
    ("ecb_hicp_es.csv", "IAPC España (ICP ANR), termina 2025-12. El deflactor del PIB se usa como inflación; no entra en nacional_q."),
    ("ine_cnt_demanda_corrientes.csv / ine_cnt_demanda_volumen.csv", "Mismo PIB a precios de mercado que la oferta; el deflactor usa ine_cnt_pib_oferta_*."),
    ("ine_cnt_renta_disponible.csv", "Serie 80333 es capacidad/necesidad de financiación, no renta de hogares."),
    ("eurostat_empleo_nuts2.csv", "No especificado en la base; disponible para trabajo posterior."),
    ("pdf/registradores_opendata_compraventas.csv (*_pm2_4T_movil, *_imp_4T_movil)", "Precio €/m² e importe medio de la ventana de 4 trimestres: son medias o ratios, NO sumas ni flujos. El raw los etiqueta 'suma móvil 4 trimestres' (error de la etiqueta; raw no editable). No se usan en ningún fichero procesado; si se usan, no se suman."),
    ("ine_migraciones_nacionalidad.csv (59011)", "No existe serie total: las nacionalidades solo tienen dato en pocas celdas por trimestre. No se usa."),
    ("ine_ecp_56936.csv", "Población solo a nivel nacional por nacionalidad y edad (sin CCAA). Se usa solo para validar ECP701."),
    ("ine_ecp_59585.csv", "Continuación 2025T2+ (ECP4961, ECP701). Se usa solo para validar ECP701."),
    ("ine_ecp_ccaa_nacionalidad.csv", "Subconjunto de 77019 (Total, Española, Extranjera). Se usa solo para comprobar que coincide con ine_ecp_ccaa_paises.csv (0 de diferencia)."),
    ("ine_ipva_nacional_ccaa.csv, ine_vut_nacional_ccaa_prov.csv", "No especificados para este módulo."),
    ("mivau_parque.csv, mivau_transacciones_residencia.csv", "No especificados."),
    ("ine_ipv_25171.csv", "Solo IPV769 (base 2015) como robustez: incluido en nacional_q (ipv15)."),
    ("vlc_precio_vivienda_libre.csv", "Excluido de valencia.csv: 5 trimestres (2021T2-2022T2), fuente primaria no indicada."),
    ("pdf/notariado_cv_actos_mensual.csv", "ROBUSTEZ según revisor (actos sobre inmuebles, no viviendas; revisiones de hasta 6 % entre ediciones). No exportado en esta versión."),
    ("pdf/serpavi_valencia_secciones.csv, pdf/serpavi_provincias.csv", "Descriptivos (secciones: ruido muestral; provincias: no requeridas en esta versión). No exportados."),
    ("pdf/registradores_eri_anuario.csv (compraventas CCAA/provincias/capital)", "Redundante con registradores_opendata_anual.csv (revisor). Capitales sin cuadre: ROBUSTEZ, no exportado."),
    ("gva_vut_municipio.csv (vut_foto_*)", "Lista vigente 2026: no encadenable con el stock 2010-2024 (revisor §3.4). Excluida de valencia.csv y de los modelos; contrastes y nota en validacion_gva.csv (sección G)."),
    ("ine_padron_valencia.csv (series ECP182xxx de CV)", "Series de la Comunitat Valenciana por nacionalidad (ECP): solo se usan DPOP21796 (València)."),
]


def _stats(s: pd.Series, flag: pd.Series | None = None) -> tuple[str, str, str, str]:
    v = s.dropna()
    if v.empty:
        return "-", "-", "0", "-"
    first, last = v.index.min(), v.index.max()
    n_gap = int(s[(s.index >= first) & (s.index <= last)].isna().sum())
    n_int = int(flag.sum()) if flag is not None else 0
    return str(first), str(last), str(n_gap), str(n_int)


def es(x: float, d: int = 2, signo: bool = False) -> str:
    """Numero en formato español (coma decimal)."""
    s = f"{x:+.{d}f}" if signo else f"{x:.{d}f}"
    return s.replace(".", ",")


def _esc(t) -> str:
    return str(t).replace("|", "\\|").replace("\n", " ")


def _met_txt(df: pd.DataFrame, var: str) -> str:
    """Recuento por método de <var>_metodo en un DataFrame (texto para tablas)."""
    c = f"{var}_metodo"
    if c not in df.columns:
        return "—"
    vc = df[c].dropna().value_counts()
    partes = [f"{k} {int(vc[k])}" for k in METODOS if k in vc.index]
    return ("; ".join(partes) if partes else "sin dato") + f" (`{var}_interp` {int(interp_de(df[c]).sum())})"


def write_dictionary(nac: pd.DataFrame, panel: pd.DataFrame, panel_a: pd.DataFrame, valencia: pd.DataFrame,
                     nacionalidad: pd.DataFrame, nacional_a: pd.DataFrame, validacion: pd.DataFrame) -> None:
    nac_i = nac.copy()
    nac_i.index = pd.PeriodIndex(nac_i["trimestre"], freq="Q")
    L: list[str] = []
    A = L.append
    ep = nac_i[["hogares_epa", "hogares_ecp"]].dropna()
    solape = ep[ep["hogares_ecp"].notna() & ep["hogares_epa"].notna()]
    ratio = (solape["hogares_epa"] / (solape["hogares_ecp"] / 1000) - 1) * 100  # ECP en unidades; EPA en miles
    ccaa_sum = nac_i["pob_extranj_ccaa_sum"]
    cs = pd.DataFrame({"s": ccaa_sum, "n": nac_i["pob_extranj"]}).dropna()
    cs_rel = ((cs["s"] - cs["n"]) / cs["n"] * 100) if len(cs) else pd.Series(dtype=float)
    _pp = panel.groupby("trimestre")["pob_extranj"].sum(min_count=17).rename("suma")
    _rel = pd.DataFrame({"suma": _pp}).join(nac.set_index("trimestre")["pob_extranj"], how="inner").dropna()
    _rel = (_rel["suma"] / _rel["pob_extranj"] - 1) * 100
    _ry = _rel.groupby(_rel.index.str[:4]).agg(["min", "max"])
    rel_txt = "; ".join(f"{y}: {es(r['min'], 1, True)} a {es(r['max'], 1, True)}" for y, r in _ry.iterrows()
                        if y in ("2002", "2008", "2014", "2020", "2021", "2025"))
    last_pob = panel.dropna(subset=["pob_total"])["trimestre"].max()
    last_pob_e = panel.dropna(subset=["pob_extranj"])["trimestre"].max()
    eu_n = int(nac_i["inmig_anual_eurostat"].notna().sum())

    A("# Diccionario de variables\n")
    A("> Generado por `src/build_dataset.py` (no editar a mano). Reconstrucción: `make clean`.\n")
    A("Convenciones comunes:\n")
    A("- **Trimestre**: `trimestre` = `2008Q1`; `fecha` = primer día del trimestre. En `panel_ccaa_a.csv` y `nacional_a.csv` la clave es `anio` (año natural).")
    A("- **Logs**: `ln_<var>` = ln(var) con NaN si var <= 0. **Diferencias**: `d_ln_<var>` = Δ1 del log (trimestral en `_q`, anual en `_a`); `d4_ln_<var>` = Δ4 (interanual) del log en los trimestrales.")
    A("- **Tipos y porcentajes (en %)**: sin log; `d_<var>` = Δ1 en puntos porcentuales.")
    A("- **Agregación mensual→trimestral**: media o suma de los 3 meses, exigiendo los 3 meses (si falta alguno, NaN). Stock: valor del último mes del trimestre.")
    A("- **Interpolación**: solo log-lineal entre observaciones (nunca fuera del rango observado); huecos finales = NaN, sin extrapolar.")
    A("- **Banderas de método**: `<var>_metodo` (categórica, ver 'Criterio de banderas') marca toda transformación temporal. `<var>_interp` (booleana) = (`<var>_metodo` == `interpolado_loglineal`), solo por compatibilidad. En `valencia.csv` la columna es `metodo` (y `interp` con la misma regla).")
    A("- **Retardos**: no se crean aquí (se hacen en los scripts de modelos).")
    A("- **Dummies de quiebre**: `quiebre_epa_2021` y `quiebre_emcr_2021` valen 1 desde 2021 (trimestre 2021Q1 en `nacional_q`; año 2021 en `nacional_a`). No son variables de nivel: no tienen `ln_`.")
    A("- **origen**: `api` (API INE/BCE/Eurostat o CKAN GVA), `xls` (XLS/XLSX/CSV oficial descargado), `pdf` (PDF con texto nativo, pdfplumber; **sin OCR** en ninguna serie), `derivado` (cálculo propio sobre fuentes anteriores).")
    A("- **validado**: `sí` = fuente oficial sin transformación no trivial, o contraste/cuadre pasado (incluida la relectura independiente del revisor); `plausibilidad` = proxy, derivada, contraste no independiente o interpolada; `no` = no validada (**obligatoriamente rol=robustez**; ninguna variable actual tiene `no`).")
    A("- **error_max**: error máximo del contraste (de `*_validacion.csv` o del informe del revisor `docs/revision_f1_fuentes.md`); `—` = sin contraste específico.")
    A("- **rol**: `principal` (entra en el modelo principal), `robustez` (solo especificaciones alternativas), `excluida` (no entra en modelos; control).\n")

    A("## Criterio de banderas `<var>_metodo`\n")
    A("Un único criterio en `nacional_q`, `nacional_a`, `panel_ccaa_q`, `panel_ccaa_a` y `valencia` (columna `metodo`). Vacío = sin dato.\n")
    A("| Valor de `_metodo` | Significado | Ejemplos |")
    A("|---|---|---|")
    A("| `observado` | Dato nativo a la frecuencia de la columna, sin transformación temporal. Incluye los stocks a 1 de enero de frecuencia anual en `panel_ccaa_a` y `valencia`, y los datos semestrales de población observados en S1/S2 | `ipv`, `ocupados`, `pob_total` (T1/T3 pre-2021) |")
    A("| `agregado_media` | Media de 3 meses (o de 4 trimestres en anuales) exigiendo todos los periodos | `tipo_hip`, `euribor`, `ipc_alquiler`, `tipo_bce` (trimestre con cambio de tipo) |")
    A("| `agregado_suma` | Suma de 3 meses (o de 4 trimestres / de 2 semestres) exigiendo todos | `credito_nuevo`, `visados`, `terminadas`, `compraventas`, `notariado_cgn_extranj` (panel anual) |")
    A("| `fin_periodo` | Stock al último mes del trimestre | `credito_stock`, `vut_stock_gva` |")
    A("| `escalonado` | Tipo oficial vigente sin cambio en el trimestre (escalón no interpolado) | `tipo_bce` |")
    A("| `interpolado_loglineal` | Valor interpolado en logaritmos entre dos observaciones (única transformación que pone `_interp` = TRUE) | `pob_*` en T2-T4 de los años anuales/semestrales |")
    A("| `anual_asignado` | Dato de frecuencia menor asignado a un trimestre sin interpolar: anual a T4 (T1 para `inmig_anual` EMCR y para los stocks 1 de enero de 77019 en `panel_ccaa_q`); semestral S1→T2, S2→T4 (`notariado_cgn_extranj`); VUT semestral feb/ago→T1/T3 hasta 2024-08 y may/nov→T2/T4 desde 2024-11 | `registradores_*_anual`, `serpavi_esp_constante`, `inmig_anual_eurostat`, `vut_*` |")
    A("| `desestacionalizado_stl` | **Añadido a la lista inicial**: desestacionalización STL(period=4, robust) sobre log, nivel = exp(log − estacional). No cabe en ninguna de las anteriores | `ocupados_sa`, `compraventas_sa` |\n")
    A("Conteo de filas por valor de `_metodo` (filas con dato) en cada fichero:\n")
    for nom, df_ in [("nacional_q", nac), ("nacional_a", nacional_a), ("panel_ccaa_q", panel),
                     ("panel_ccaa_a", panel_a), ("valencia", valencia)]:
        if nom == "valencia":
            vc = valencia["metodo"].dropna().value_counts()
            txt = "; ".join(f"`{k}` {int(vc[k])}" for k in METODOS if k in vc.index)
            A(f"- **valencia.csv** (columna `metodo`): {txt}.")
            continue
        for c, cnt in metodo_resumen(df_):
            if cnt:
                A(f"- **{nom}** `{c}`: " + "; ".join(f"`{k}` {v}" for k, v in cnt.items()) +
                  f" (`{c.replace('_metodo', '_interp')}` = {int(cnt.get('interpolado_loglineal', 0))} TRUE).")
    A("")
    A("- Las series trimestrales nativas no llevan bandera. Los vacíos en origen no se imputan.\n")

    A("## A. `data/processed/nacional_q.csv` (trimestral, nacional)\n")
    A("Muestra base 2008Q1+. Serie PRINCIPAL de hogares: `hogares_epa`. `hogares` (60131) pasa a llamarse `hogares_ecp` (robustez).\n")
    A("| Variable | Fuente | Archivo raw | Código / serie | Unidad | Frecuencia original | Agregación / asignación | Transformaciones | Banderas de método (nº filas por valor) | origen | validado | error_max | rol | Primer dato | Último dato | Huecos internos |")
    A("|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|")
    order = [r[0] for r in META_NAC]
    meta_by = {r[0]: r for r in META_NAC}
    for var in order:
        if var not in nac_i.columns:
            continue
        nombre, fuente, archivo, cod, unidad, freq, agreg = meta_by[var]
        if var in LEVELS_POS:
            tr = "ln_, d_ln_, d4_ln_"
        elif var in RATES:
            tr = "d_ (Δ1 pp)"
        else:
            tr = "ninguna"
        if var in ("inmig_anual", "inmig_anual_eurostat"):
            tr = "ninguna (anual)"
        fl = nac_i[f"{var}_interp"].astype(bool) if f"{var}_interp" in nac_i.columns else None
        fl_txt = _met_txt(nac_i, var)
        if var in ("pob_total", "pob_extranj"):
            fl_txt += " — interpolados log-lineal entre observaciones"
        o, v_, e_, r_, nt = NAC_ORIG[var]
        first, last, gaps, _ = _stats(nac_i[var], fl)
        A(f"| `{var}` | {_esc(fuente)} | `{archivo}` | {_esc(cod)} | {_esc(unidad)} | {_esc(freq)} | {_esc(agreg)} | {tr} | {_esc(fl_txt)} | {o} | {v_} | {_esc(e_)} | {r_} | {first} | {last} | {gaps} |")
    A("")
    A("Variables derivadas con la misma regla de transformación: `ln_`, `d_ln_`, `d4_ln_` para niveles positivos; `d_` para tipos y tasas.\n")
    A("**Notas de método y de contraste**")
    A(f"- `hogares_epa` (EPA430446, total de hogares, miles) es la serie **principal** de hogares desde 2002T1. En el solape con `hogares_ecp` (60131, 2021T1+; {len(solape)} trimestres) la EPA es entre **{es(ratio.min())} % y {es(ratio.max())} %** mayor (media {es(ratio.mean())} %). No se enlazan ambas series.")
    A("- **Quiebre metodológico de la EPA desde 2021T1** (`quiebre_epa_2021` = 1 desde 2021Q1). Cambian (i) la definición de hogar, que pasa a basarse en el presupuesto compartido en lugar de la vivienda (Reglamento UE 2019/1700), y (ii) los factores de elevación, que pasan a la base poblacional del Censo 2021 (2002-2020 sigue en base 2011). Fuentes: INE, 'Medida del efecto de los cambios en la EPA 2021' y nota de prensa `cbEPA2021`. Efecto observado en `hogares_epa`: **−1,1 %** en 2021T1 (de 18.817,8 a 18.610,0 miles; único descenso de la serie y mayor variación absoluta desde 2002). **La creación neta de hogares de 2021T1 no debe interpretarse como dato real.** Usar `quiebre_epa_2021` como control en cualquier regresión que use `hogares_epa`.")
    A("- **`ocupados` (EPA387796)** comparte el cambio de base de factores de elevación de la EPA desde 2021T1 (Censo 2021). El INE indica que el efecto en los agregados principales no es relevante; **no se ha corregido ni medido** en esta versión. Se anota para F2 y se dispone de `quiebre_epa_2021`.")
    A(f"- `pob_extranj_ccaa_sum` = suma de 17 CCAA de la tabla 77019 (sin Ceuta ni Melilla) de `pob_extranj` por trimestre (requiere las 17 CCAA). No coincide con `pob_extranj` nacional (ECP701): la diferencia relativa va de **{es(cs_rel.min(), signo=True)} % a {es(cs_rel.max(), signo=True)} %**. Parte es Ceuta y Melilla (suma menor, ~-0,3 %) y el resto es **error de interpolación**: las CCAA son stocks anuales a 1 de enero interpolados en logaritmos, mientras que la nacional es observada cada trimestre desde 2021. Por año (% suma CCAA / nacional − 1): {rel_txt}. Se conserva como control (`rol=excluida`), no entra en el modelo.")
    A("- `registradores_compraventas_anual` = compraventas de viviendas nacionales (suma móvil de 4 trimestres en T4 = año natural). Se usa **solo en T4** de cada año; el dato trimestral no se reconstruye (requiere valor semilla). No mezclar con `compraventas` (INE ETDP).")
    A("- `registradores_extranj_pct` (% de compras de extranjeros), `serpavi_esp_constante` (alquiler €/m²/mes, agregado propio) y `notariado_cgn_extranj` (operaciones de extranjeros, semestral: S1→T2, S2→T4) se asignan sin interpolar (`anual_asignado`).")
    A("- `serpavi_esp_constante` usa 17 CCAA con pesos fijos (15 de régimen común + Ceuta y Melilla): **excluye Navarra y País Vasco** para que la composición no cambie. Un agregado de medianas no es una mediana nacional.")
    A("- `ipv15` (IPV base 2015) solo como robustez. `ipc_alquiler_yoy` está en el CSV como tasa (%) con `d_`.")
    A("- `deflactor` = PIB a precios corrientes **desestacionalizado** (CNTR6597, 'Datos ajustados de estacionalidad y calendario', M€) / PIB volumen encadenado **desestacionalizado** (CNTR6652, índice de volumen encadenado), reescalado a media 2020 = 100. Deflactor implícito aproximado, no el oficial del INE. Corrige la versión anterior (CNTR6548/CNTR6721, NSA), que generaba un ciclo estacional espurio en `renta_hog_real` (ver 'Validación del deflactor' abajo).")
    A("- `renta_hog_real` = renta_hog / deflactor × 100 (M€ a precios de 2020). `renta_hog` (Eurostat, SCA) se divide entre un deflactor SA: coherente en ambas series.")
    A("- `tipo_hip_real` = tipo_hip − inflacion_deflactor (pp). La HICP del BCE (`ecb_hicp_es.csv`) termina en 2025-12 y no se usa.")
    A("- `visados`: faltan abril-junio de 2016 y de 2017 en el origen (MIVAU), así que 2016T2 y 2017T2 quedan NaN (regla de los 3 meses).")
    A("- `ocupados_sa` y `compraventas_sa`: STL(period=4, robust=True) sobre log, en el bloque contiguo más largo de datos; nivel = exp(log − estacional). `metodo` = `desestacionalizado_stl`.")
    A("- `pob_total` (ECP320) y `pob_extranj` (ECP701) son semestrales hasta 2020 (1 ene y 1 jul) y trimestrales desde 2021; T2 y T4 de 1995-2020 se interpolan en logaritmos entre observaciones (`interpolado_loglineal`).")
    A("- `tipo_bce_metodo`: `escalonado` cuando el trimestre no tiene cambio de tipo (valor vigente desde un cambio anterior); `agregado_media` (media de días) cuando sí lo tiene. `tipo_bce_interp` = FALSE en todas las filas (no es interpolación).")
    A("- `visados` y `terminadas` son proxies del Boletín MIVAU (viviendas libres iniciadas/terminadas), no visados CSCAE ni certificados de fin de obra.")
    A("- `hogares_ecp`: serie trimestral solo desde 2021T1 (60131). No se interpola ni se retropola.")
    A(f"- `inmig_anual` (EMCR, tabla 69687): flujo anual 2021-2024 (N = 4), asignado al primer trimestre de cada año (`anual_asignado`). **Rol robustez** (N = 4 no sirve para modelos). No usar sin agregación anual.")
    A(f"- `inmig_anual_eurostat`: inmigración anual **TOTAL** (todas las ciudadanías) de Eurostat, `migr_imm1ctz` (archivo `eurostat_inmigracion_anual.csv`), 1998-2024 ({eu_n} años). Asignada al **T4** de cada año (`anual_asignado`). En 2021 coincide con la cifra EMCR (887.960). Quiebre de fuente 2021 (paso a la EMCR; 2019 = 750.480, 2020 = 467.918 por COVID, 2021 = 887.960): usar `quiebre_emcr_2021`. Según el revisor, el desglose por ciudadanía (FOR/NAT) solo es completo desde 2020.")
    A("- `inmig_q` (59011) **no se incluye**: no hay serie total y las nacionalidades están casi vacías (ver `docs/fuentes_fallidas.md`).")
    A("- `credito_stock`: fin de trimestre. `credito_nuevo`: suma de 3 meses (M€).\n")
    A("### Dummies y muestra\n")
    A("- `q1`…`q4`: dummies trimestrales. `quiebre_epa_2021` (1 desde 2021Q1; cambio metodológico EPA) y `quiebre_emcr_2021` (1 desde 2021Q1; cambio de fuente de inmigración EMCR). `muestra_base` = True desde 2008Q1 hasta el último trimestre con `ipv` no NaN.\n")
    A("### Validación del deflactor (cambio de 2026-10-09)\n")
    A("Media de `d_ln_renta_hog_real` (%, 2008Q1+) por trimestre del año, antes y después de sustituir el deflactor NSA (CNTR6548/CNTR6721) por el SA (CNTR6597/CNTR6652):")
    # Antes: medias de la versión NSA (CNTR6548/CNTR6721), medidas en la ejecución previa (2008Q1-2026Q2).
    ANTES = {"Q1": 0.99, "Q2": -0.79, "Q3": 2.57, "Q4": -1.76}
    _x = nac_i[nac_i.index >= MUESTRA_INI].dropna(subset=["d_ln_renta_hog_real"])
    _m = (_x["d_ln_renta_hog_real"] * 100).groupby(_x["trimestre"].str[-2:]).mean()
    _d = (nac_i[nac_i.index >= MUESTRA_INI].dropna(subset=["d_ln_deflactor"])["d_ln_deflactor"] * 100)
    _dm = _d.groupby(nac_i.loc[_d.index, "trimestre"].str[-2:]).mean()
    # Mismo cálculo excluyendo 2020-2021 (choque COVID: volumen SA 2020T2 −17,8 %, 2020T3 +15,9 %)
    ANTES_EX = {"Q1": 1.05, "Q2": -0.28, "Q3": 1.84, "Q4": -1.50}
    _xe = _x[~_x["trimestre"].str[:4].isin(["2020", "2021"])]
    _me = (_xe["d_ln_renta_hog_real"] * 100).groupby(_xe["trimestre"].str[-2:]).mean()
    A("| Trimestre | `d_ln_renta_hog_real` antes (%) | después (%) | antes, sin 2020-2021 (%) | después, sin 2020-2021 (%) | `d_ln_deflactor` después (%) |")
    A("|---|---|---|---|---|---|")
    for qq in ["Q1", "Q2", "Q3", "Q4"]:
        A(f"| T{qq[1]} | {es(ANTES[qq])} | {es(_m[qq])} | {es(ANTES_EX[qq])} | {es(_me[qq])} | {es(_dm[qq])} |")
    A("")
    A("Rango estacional (máx − mín de las medias trimestrales): antes 4,3 pp; después 1,3 pp con 2020-2021 incluidos, y 3,3 pp antes frente a 0,6 pp después sin 2020-2021. "
      "El patrón T3 positivo / T4 negativo del deflactor NSA desaparece. Con 2020 incluido, el T3 positivo que queda es el rebote de 2020T3 del volumen SA (choque COVID), no estacionalidad. "
      "Queda un residuo de unas décimas en `d_ln_deflactor` (T1 y T4 algo mayores que T2) que procede de la serie SA del INE y no se corrige aquí. Los valores de 'antes' son de la ejecución con deflactor NSA y se fijan como referencia.")
    A("")

    A("## B. `data/processed/panel_ccaa_q.csv` (17 CCAA × trimestre, formato largo)\n")
    A("Códigos INE de CCAA: 01 Andalucía, 02 Aragón, 03 Asturias (Principado de), 04 Balears (Illes), 05 Canarias, 06 Cantabria, 07 Castilla y León, 08 Castilla-La Mancha, 09 Cataluña, 10 Comunitat Valenciana, 11 Extremadura, 12 Galicia, 13 Madrid (Comunidad de), 14 Murcia (Región de), 15 Navarra (Comunidad Foral de), 16 País Vasco, 17 La Rioja. **Ceuta (18) y Melilla (19) excluidas.** Nombres normalizados con `slug()` y `SLUG_ALIAS`.\n")
    A(f"> **ADVERTENCIA (población en el panel trimestral)**: `pob_total`, `pob_extranj` y `pob_espanola` son **anuales disfrazadas de trimestrales**. El dato es un stock a 1 de enero (asignado a T1, `anual_asignado`) y T2-T4 son interpolaciones log-lineales (`interpolado_loglineal`). Su `d_ln_` es constante dentro de cada año. **Usar `panel_ccaa_a` (anual) o Δ4; nunca Δ1 trimestral como regresor**: multiplica el N por 4 y crea autocorrelación mecánica. La serie de población termina en **{last_pob}** (77019 llega a 1-ene-2025); no se extrapola (2025 T2-T4 = NaN).\n")
    A("| Variable | Fuente | Archivo raw | Código / serie | Unidad | Frecuencia | Agregación | Transformaciones | Banderas de método (filas por valor) | origen | validado | error_max | rol | Primer dato (mín. CCAA) | Último dato (máx. CCAA) |")
    A("|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|")
    panel_meta = {
        "ipv": ("INE IPV, tabla 80270", "ine_ipv_80270.csv", "IPV1392 (CCAA General)", "índice", "trimestral", "nativo"),
        "ipv_nueva": ("INE IPV, tabla 80270", "ine_ipv_80270.csv", "'<CCAA>. Vivienda nueva. Índice.'", "índice", "trimestral", "nativo"),
        "ipv_usada": ("INE IPV, tabla 80270", "ine_ipv_80270.csv", "'<CCAA>. Vivienda segunda mano. Índice.'", "índice", "trimestral", "nativo"),
        "p_tasado": ("MIVAU, tabla 35101000", "mivau_valor_tasado_nacional_ccaa_prov.csv", "valor_tasado_libre_ccaa_<slug>", "€/m2", "trimestral", "nativo"),
        "ocupados": ("INE EPA, tabla 65302", "ine_epa_ocupados_ccaa.csv", "'<CCAA>. Ambos sexos. Total. Ocupados. Valor absoluto.'", "miles", "trimestral", "nativo; cambio de base EPA 2021 (ver nacional_q)"),
        "compraventas": ("INE ETDP, tabla 6150", "ine_etdp_compraventas.csv", "'<CCAA>. General. Compraventa. Número.'", "número", "mensual", "suma de 3 meses"),
        "trans_total": ("MIVAU, tabla 34010110", "mivau_transacciones_total.csv", "tx_total_ccaa_<slug>", "transacciones", "trimestral", "nativo"),
        "trans_extranjeros": ("MIVAU, tabla 340101i0 (total)", "mivau_transacciones_extranjeros.csv", "tx_extranj_residentes_total_ccaa_<slug>", "transacciones", "trimestral", "nativo"),
        "visados": ("MIVAU, tabla 32100500 (PROXY)", "mivau_visados.csv", "viv_libres_iniciadas_ccaa_<slug>", "viviendas", "mensual", "suma de 3 meses"),
        "terminadas": ("MIVAU, tabla 32101000 (PROXY)", "mivau_fin_obra.csv", "viv_libres_terminadas_ccaa_<slug>", "viviendas", "mensual", "suma de 3 meses"),
        "ipc_alquiler": ("INE IPC, alquiler de vivienda", "ine_ipc_alquiler.csv", "'<CCAA>. Alquiler de vivienda. Índice.'", "índice", "mensual", "media de 3 meses"),
        "pob_total": ("INE 77019 (ECP, CCAA x nacionalidad)", "ine_ecp_ccaa_paises.csv", "'<CCAA>. Todas las edades. Total. Total. Población.'", "personas (stock 1 ene)", "anual (T1 en el CSV)", "stock a 1 de enero en T1; T2-T4 interpolados log-lineal entre observaciones"),
        "pob_extranj": ("INE 77019 (ECP)", "ine_ecp_ccaa_paises.csv", "'<CCAA>. Todas las edades. Extranjera. Total.'", "personas (stock 1 ene)", "anual", "como pob_total"),
        "pob_espanola": ("INE 77019 (ECP)", "ine_ecp_ccaa_paises.csv", "'<CCAA>. Todas las edades. Española. Total.'", "personas (stock 1 ene)", "anual", "como pob_total"),
        "epa_pob_total": ("INE EPA, tabla 65285", "ine_epa_poblacion_ccaa.csv", "'Ambos sexos. <CCAA>. Total. Valor absoluto.'", "miles (todas las edades)", "trimestral", "nativo; incluye menores de 16 (no es población de 16+)"),
    }
    for v in PANEL_LEVELS:
        nm, arch, cod, uni, fr, ag = panel_meta[v]
        per_ccaa = panel.dropna(subset=[v]).groupby("codigo_ine_ccaa")["trimestre"].agg(["min", "max", "count"])
        ncc = len(per_ccaa)
        fmin = per_ccaa["min"].min() if ncc else "-"
        fmax = per_ccaa["max"].max() if ncc else "-"
        tr = "ln_, d_ln_, d4_ln_ (dentro de cada CCAA)"
        fl = _met_txt(panel, v)
        o, v_, e_, r_ = PANEL_META[v]
        A(f"| `{v}` | {nm} | `{arch}` | {_esc(cod)} | {uni} | {fr} | {ag} | {tr} | {_esc(fl)} ({ncc}/17 CCAA) | {o} | {v_} | {_esc(e_)} | {r_} | {fmin} | {fmax} |")
    A("")
    A("**Huecos de origen**: `terminadas` (MIVAU 32101000) no tiene Extremadura en el Boletín. `p_tasado` de Navarra tiene solo los trimestres en que MIVAU publica esa CCAA (ver `DUP_NOTES`).\n")
    A("**Población por CCAA**: 77019 (tabla de población por CCAA y grupo de países) publica **un dato anual a 1 de enero**; el CSV lo etiqueta como T1 (`anual_asignado`). Los trimestres T2-T4 entre dos observaciones se interpolan en logaritmos (`interp_loglin`, `interpolado_loglineal`). No se extrapola. `epa_pob_total` (65285) es población EPA de **todas las edades** (incluye menores de 16); se usa como contraste, no como sustituto.\n")
    A("**Validación**: suma de las 17 CCAA de `pob_extranj` frente a ECP701 nacional: ver `pob_extranj_ccaa_sum` en nacional_q (diferencia por Ceuta y Melilla). `pob_total` de CCAA = suma de CCAA + Ceuta y Melilla = total nacional. La suma de 17 CCAA de `pob_extranj` en el trimestral termina en {last_pob_e}.\n")
    A("**Inmigración por CCAA**: la tabla 59013 (flujos CCAA × nacionalidad) no tiene total por CCAA y sus celdas están casi vacías; el flujo anual por CCAA no está en `data/raw` (la tabla 69691 **no se ha descargado**; ver `docs/fuentes_fallidas.md`). Por eso `panel_ccaa_a` **no** incluye inmigración anual por CCAA.\n")

    A("## B2. `data/processed/panel_ccaa_nacionalidad.csv` (flujos 59013 y stocks 77019)\n")
    n_fl = int((nacionalidad["tipo_registro"] == "flujo_59013").sum())
    n_st = int((nacionalidad["tipo_registro"] == "stock_77019_1ene").sum())
    A(f"Formato largo con `tipo_registro`: **`flujo_59013`** (inmigración trimestral por CCAA × nacionalidad, tabla 59013, desde 2023T2; solo celdas con valor: {n_fl} filas; el resto está vacío en origen y no se rellena) y **`stock_77019_1ene`** (stock de población por CCAA × grupo de países a 1 de enero, tabla 77019, {n_st} filas; `trimestre` = `AAAAT1`, `pob_stock` en personas; grupos: Total, Española, Extranjera y grupos de países). Ceuta y Melilla excluidas. Las columnas `inmig_flujo` y `pob_stock` son disjuntas por tipo.\n")

    A("## B3. `data/processed/panel_ccaa_a.csv` (17 CCAA × año, para el IV shift-share de F3)\n")
    A("Clave: `codigo_ine_ccaa` × `anio`. Años 2002-2025 (rellenos NaN donde no hay dato; no se extrapola). Stocks a 1 de enero (`observado`); agregados anuales solo con los 4 trimestres completos (si falta uno, NaN); logs y Δ1 año (`d_ln_`). Banderas `<var>_metodo` en las variables agregadas (`agregado_media`, `agregado_suma`) y en `notariado_cgn_extranj` (`agregado_suma`, S1+S2).\n")
    A("| Variable | Fuente | Archivo raw | Código / serie | Unidad | Transformación anual | origen | validado | error_max | rol |")
    A("|---|---|---|---|---|---|---|---|---|---|")
    pa_rows = [
        ("pob_total / pob_extranj / pob_espanola / pob_<grupo>", "INE 77019", "ine_ecp_ccaa_paises.csv", "'<CCAA>. Todas las edades. <grupo>. Total.'", "personas (stock 1 ene)", "nativo anual (sin interpolar; `observado`)", "api", "sí (grupos suman exactamente a Extranjera; ver checks)", "0 (aditividad)", "principal (totales); robustez (grupos)"),
        ("pob_europa_sin_espana", "Derivada de 77019 (ver nota)", "ine_ecp_ccaa_paises.csv", "UE28 sin España + Europa menos UE28 (2002-2020); UE27 sin España + Europa menos UE27 (2021-2025)", "personas (stock 1 ene)", "suma de grupos europeos de la familia del año", "derivado", "plausibilidad", "ver nota (residuo ≤ 2 personas)", "principal"),
        ("ipv", "INE IPV 80270 (de panel_ccaa_q)", "ine_ipv_80270.csv", "IPV1392 y CCAA", "índice", "media de 4 trimestres (`agregado_media`)", "api", "sí", "—", "principal"),
        ("p_tasado", "MIVAU 35101000 (de panel_ccaa_q)", "mivau_valor_tasado_nacional_ccaa_prov.csv", "valor_tasado_libre_ccaa_<slug>", "€/m²", "media de 4 trimestres (`agregado_media`)", "xls", "sí", "—", "principal"),
        ("ocupados", "INE EPA 65302 (de panel_ccaa_q)", "ine_epa_ocupados_ccaa.csv", "Ocupados (ambos sexos, total)", "miles", "media de 4 trimestres (`agregado_media`); cambio de base EPA 2021 sin corregir", "api", "sí", "—", "principal"),
        ("compraventas", "INE ETDP 6150 (de panel_ccaa_q)", "ine_etdp_compraventas.csv", "Compraventas número", "número", "suma de 4 trimestres (`agregado_suma`)", "api", "sí", "—", "principal"),
        ("trans_total", "MIVAU 34010110 (de panel_ccaa_q)", "mivau_transacciones_total.csv", "tx_total_ccaa_<slug>", "transacciones", "suma de 4 trimestres (`agregado_suma`)", "xls", "sí", "—", "principal"),
        ("trans_extranjeros", "MIVAU 340101i0 (de panel_ccaa_q)", "mivau_transacciones_extranjeros.csv", "tx_extranj_residentes_total_ccaa_<slug>", "transacciones", "suma de 4 trimestres (`agregado_suma`); resultado directo de demanda extranjera", "xls", "sí", "—", "principal"),
        ("visados", "MIVAU 32100500 PROXY (de panel_ccaa_q)", "mivau_visados.csv", "viv_libres_iniciadas_ccaa_<slug>", "viviendas", "suma de 4 trimestres (`agregado_suma`)", "xls", "plausibilidad", "proxy MIVAU, no visados CSCAE", "principal (control de oferta)"),
        ("terminadas", "MIVAU 32101000 PROXY (de panel_ccaa_q)", "mivau_fin_obra.csv", "viv_libres_terminadas_ccaa_<slug>", "viviendas", "suma de 4 trimestres (`agregado_suma`); NaN en Extremadura", "xls", "plausibilidad", "proxy MIVAU, no certificados CSCAE", "principal (control de oferta)"),
        ("ipc_alquiler", "INE IPC, alquiler de vivienda (de panel_ccaa_q)", "ine_ipc_alquiler.csv", "'<CCAA>. Alquiler de vivienda. Índice.'", "índice", "media de 4 trimestres (`agregado_media`)", "api", "sí", "—", "principal"),
        ("serpavi_vc_mediana", "MIVAU-SERPAVI (XLSX)", "pdf/serpavi_ccaa.csv", "alquiler_m2 mediana VC por CCAA", "€/m²/mes", "nativo anual (`observado`)", "xls", "plausibilidad", "6,43 pp frente al IPVA València (no independiente)", "principal"),
        ("notariado_cgn_extranj", "Consejo General del Notariado (CIEN)", "pdf/notariado_cgn_extranjeros_semestral.csv", "T2 op_viv_libre_extranjeros, 'Extranjero', por CCAA", "operaciones", "suma S1+S2 (`agregado_suma`; solo si ambos existen)", "xls", "sí", "0 (suma interna)", "principal"),
        ("registradores_extranj_pct", "Colegio de Registradores, Anuario ERI", "pdf/registradores_eri_anuario.csv", "viv_pct_compras_extranjeros_serie8a (CCAA)", "%", "nativo anual, última edición por año (`observado`)", "pdf", "sí", "0 (nacionales + extranjeros = 100 %)", "robustez"),
    ]
    for r in pa_rows:
        A("| " + " | ".join(_esc(x) for x in r) + " |")
    A("")
    # Verificación de la definición de pob_europa_sin_espana frente al residuo (pob_extranj − no europeos)
    nonEU = ["pob_africa", "pob_asia", "pob_sudamerica", "pob_centroamerica_caribe", "pob_norteamerica",
             "pob_oceania", "pob_apatridas"]
    resid = panel_a["pob_extranj"] - panel_a[nonEU].sum(axis=1, min_count=len(nonEU))
    dif_eu = (panel_a["pob_europa_sin_espana"] - resid).abs().dropna()
    A("- Logs: `ln_<var>` para niveles positivos; diferencias anuales `d_ln_<var>` (Δ1 año, dentro de cada CCAA). `d_registradores_extranj_pct` = Δ1 año en pp.")
    A("- **Grupo `pob_europa_sin_espana` (coherente con el quiebre UE28/UE27)**: 77019 publica en cada año **una** de dos familias, nunca ambas: 2002-2020 = `pob_ue28_sin_espana` + `pob_europa_no_ue28`; 2021-2025 = `pob_ue27_sin_espana` + `pob_europa_no_ue27`. El grupo es la suma de los grupos europeos disponibles de la familia completa de cada año (NaN si falta alguno). Comprobación: coincide con `pob_extranj` − Σ grupos no europeos con diferencia máxima de **{dif_eu.max():.0f} personas** ({len(dif_eu)} CCAA-años). **No enlazar** `pob_ue28_sin_espana` con `pob_ue27_sin_espana` (ni los `pob_europa_no_*`): usar `pob_europa_sin_espana`.")
    A("- **Grupos de origen**: quedan 7 grupos no europeos + Europa (8 grupos con pob_europa_sin_espana). Para identificar por shocks (Borusyak et al.) son pocos; la identificación tendría que venir de las cuotas (Goldsmith-Pinkham et al.), con 17 unidades. Esto se dice en F3.")
    A("- **Trimestres vs anual**: `ocupados`, `ipv`, `p_tasado`, `ipc_alquiler` son medias de 4 trimestres (sin 4 trimestres = NaN); `compraventas`, `trans_*`, `visados`, `terminadas`, `notariado_cgn_extranj` son sumas de 4 trimestres (o 2 semestres).")
    A("- `pob_ue28_sin_espana` (2002-2020) y `pob_ue27_sin_espana` (2021+) cambian de definición en 2020-2021 (salida del Reino Unido): no enlazar. Ver `pob_europa_no_ue28` / `pob_europa_no_ue27` por la misma razón.\n")

    A("## B4. `data/processed/nacional_a.csv` (anual nacional)\n")
    A("Clave: `anio`. Medias o sumas anuales de `nacional_q` (solo con 4 trimestres completos; si falta uno, NaN) y flujos anuales nativos. Sirve para análisis anual y para contrastar `panel_ccaa_a` con el total nacional. `inmig_anual_eurostat` e `inmig_anual` son flujos nativos anuales (`observado`); el resto son agregados (`_metodo`). Dummies `quiebre_epa_2021` y `quiebre_emcr_2021` (1 desde 2021).\n")
    A("| Variable | Agregación anual (método) | Fuente de nacional_q | Rol | Años con dato | Primer año | Último año |")
    A("|---|---|---|---|---|---|---|")
    na_meta = [
        ("ipv", "media de 4 trimestres (`agregado_media`)", "principal"),
        ("ocupados", "media de 4 trimestres (`agregado_media`); cambio de base EPA 2021", "principal"),
        ("pob_extranj", "media de 4 trimestres (`agregado_media`); T2 y T4 interpolados antes de 2021", "principal"),
        ("hogares_epa", "media de 4 trimestres (`agregado_media`); quiebre EPA 2021", "principal"),
        ("terminadas", "suma de 4 trimestres (`agregado_suma`); proxy MIVAU", "principal"),
        ("visados", "suma de 4 trimestres (`agregado_suma`); proxy MIVAU; 2016 y 2017 sin año completo", "principal"),
        ("inmig_anual_eurostat", "flujo anual nativo, TOTAL (`observado`)", "principal"),
        ("inmig_anual", "flujo anual nativo EMCR 2021-2024 (`observado`)", "robustez"),
    ]
    for v, ag, rol in na_meta:
        s_ = nacional_a[v].dropna() if v in nacional_a else pd.Series(dtype=float)
        A(f"| `{v}` | {ag} | `{v}` de nacional_q | {rol} | {len(s_)} | {int(s_.index.min()) if len(s_) else '-'} | {int(s_.index.max()) if len(s_) else '-'} |")
    A("")
    A(f"- `inmig_anual_eurostat`: {int(nacional_a['inmig_anual_eurostat'].notna().sum())} años (1998-2024). Quiebre de fuente en 2021 (`quiebre_emcr_2021`).")
    A("- Logs y Δ1 año (`ln_`, `d_ln_`) para las variables de nivel positivas.\n")

    A("## C. `data/processed/valencia.csv` (formato largo: territorio × periodo × variable)\n")
    A("Columnas: `territorio`, `periodo` (`2008Q1` trimestral; `2019` anual), `frecuencia`, `variable`, `valor`, `origen`, `rol`, `validado`, `metodo` (mismo criterio que `<var>_metodo` de los demás ficheros; vacío = sin dato), `interp` (= `metodo` == `interpolado_loglineal`, por compatibilidad).\n")
    A("**Correcciones de esta versión**: (1) el fichero `ine_vut_valencia_municipio.csv` es ahora el **municipio** de València (2024-08 = 7.976 viviendas; el revisor describía una versión anterior con la provincia). `ine_vut_valencia_provincia.csv` es la **provincia** (2024-08 = 17.853, igual que la provincia en `ine_vut_nacional_ccaa_prov.csv`). La versión anterior de `valencia.csv` tenía en 'València (municipio)' las cifras de la provincia (p. ej. 0,92 % en 2020T3 frente a 1,64 % del municipio): esas filas se han corregido. (2) `ipva` (anual) se guarda como `periodo=AAAA`, sin asignar a T1. (3) Notariado municipal: **solo 'Total general'** de València (no se suman nacionalidades: 4T2022 no es aditiva). (4) **Calendario VUT INE**: hasta 2024-08 la publicación es en feb y ago (→ T1 y T3); desde 2024-11 es en **may y nov** (→ T2 y T4): 2024-11, 2025-05, 2025-11 y 2026-05. Por tanto 2024T3 y 2024T4 distan solo 3 meses. La versión anterior del diccionario decía feb→T1, ago→T3 sin excepción.\n")
    A("| Variable | Territorio | Archivo raw | Código / serie | Unidad | Frecuencia | Transformación | `metodo` | origen | validado | error_max | rol | Primer | Último | Nº |")
    A("|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|")
    units = {"p_tasado": "€/m2", "trans_total": "transacciones", "trans_extranjeros": "transacciones", "ipv": "índice",
             "vut_viviendas_turisticas": "viviendas", "vut_plazas": "plazas", "vut_plazas_por_vivienda": "plazas/vivienda",
             "vut_pct_sobre_total": "%", "ipva": "índice", "pob_total": "personas", "pob_espanola": "personas",
             "pob_extranjera": "personas", "pob_vlc_america": "personas", "pob_vlc_asia": "personas",
             "pob_vlc_europa": "personas", "pob_vlc_africa": "personas", "pob_vlc_alemania": "personas",
             "pob_vlc_reino_unido": "personas", "pob_extranjera_gva": "personas", "serpavi_vc_mediana": "€/m²/mes",
             "serpavi_vc_dist_agg": "€/m²/mes", "notariado_viv_extranj": "viviendas", "notariado_viv_esp_prov": "viviendas",
             "notariado_viv_ext_prov": "viviendas", "notariado_cuantia_esp_prov": "€", "notariado_cuantia_ext_prov": "€",
             "vut_stock_gva": "viviendas (stock)"}
    vt = valencia.copy()
    for (terr, var), m in VAL_META.items():
        ss = vt[(vt["territorio"] == terr) & (vt["variable"] == var)]
        if ss.empty:
            continue
        arch, cod = VAL_SRC[(terr, var)].split(" | ", 1) if " | " in VAL_SRC[(terr, var)] else (VAL_SRC[(terr, var)], "")
        A(f"| `{var}` | {terr} | `{_esc(arch)}` | {_esc(cod)} | {units.get(var, '')} | {m['frecuencia']} | {_esc(m['transformacion'])} | {m['metodo']} | {m['origen']} | {m['validado']} | {_esc(m['error_max'])} | {m['rol']} | {ss['periodo'].min()} | {ss['periodo'].max()} | {len(ss)} |")
    A("")
    A("Notas por variable (valencia.csv):")
    notas_done = set()
    for (terr, var), m in VAL_META.items():
        if m["nota"] and (var, m["nota"]) not in notas_done:
            notas_done.add((var, m["nota"]))
            A(f"- `{var}` ({terr}): {m['nota']}.")
    A("")
    A("- **Notariado municipal (València ciudad)**: solo el 'Total general'. El PDF de municipios no publica total provincial, así que la comparación provincial usa el PDF trimestral de la provincia. Excluido: el desglose por nacionalidad (suma ≠ Total en 4T2022: 995 de error, comprobado).")
    A("- **Padrón**: `pob_total` (DPOP21796, 1996-2025) y `pob_espanola`/`pob_extranjera` (padrón por nacionalidad, 1998-2022). Diferencia máxima Total − (Española + Extranjera): {:.0f}. Diferencia máxima DPOP − Total por nacionalidad (1998-2022): {:.0f}.".format(CHECK.get("vlc_esp_mas_ext_vs_total_max_dif", float('nan')), CHECK.get("vlc_total_dpop_vs_padron_nac_max_dif", float('nan'))))
    A("- **Excluidos**: `vlc_precio_vivienda_libre.csv` (5 trimestres, fuente no indicada). `notariado_cv_actos_mensual` (actos sobre inmuebles, ROBUSTEZ del revisor, no exportado en esta versión).")
    A("- **Registros GVA** (`vut_stock_gva`, `pob_extranjera_gva`): ver `validacion_gva.csv`, con los contrastes y la indicación de independencia.\n")

    A("## D. Datos de PDF (origen = pdf)\n")
    A("Ninguna serie procede de OCR. Todas las series `pdf` tienen texto nativo (pdfplumber). Validación según `*_validacion.csv` y `docs/revision_f1_fuentes.md`. Regla: datos de PDF no validados = solo robustez.\n")
    A("| Variable | Archivo raw | Validación | error_max | rol | Nota |")
    A("|---|---|---|---|---|---|")
    for var in ["registradores_extranj_pct"]:
        o, v_, e_, r_, nt = NAC_ORIG[var]
        A(f"| `{var}` (nacional_q) | `pdf/registradores_eri_anuario.csv` | {v_} | {_esc(e_)} | {r_} | serie anual 2023-2025; el CSV open data (`registradores_opendata_*`) es xls y no se duplica |")
    for (terr, var), m in VAL_META.items():
        if m["origen"] == "pdf":
            A(f"| `{var}` ({terr}) | `{_esc(VAL_SRC[(terr, var)].split(' | ')[0])}` | {m['validado']} | {_esc(m['error_max'])} | {m['rol']} | {_esc(m['nota'])} |")
    for var, (o, v_, e_, r_) in PANEL_A_EXTRA.items():
        if o == "pdf":
            A(f"| `{var}` (panel_ccaa_a) | `pdf/registradores_eri_anuario.csv` | {v_} | {_esc(e_)} | {r_} | por CCAA, serie 8 años |")
    A("")
    A("**Validación de los PDF (resumen del revisor, `docs/revision_f1_fuentes.md`)**:")
    A("- Notariado CV provincias trimestral (4T2025): sumas exactas frente a totales del PDF; 1.463 (7,5 %) frente al CGN; IUI 99,90 %. PRINCIPAL.")
    A("- Notariado municipios (València ciudad, `notariado_viv_extranj`): el fallo de 4T2022 y 4T2025 queda corregido en el extractor (19/19 municipios en las 5 ediciones; `notariado_validacion.csv`: `municipios_completitud = sí`). **Validado = sí** tras la relectura independiente del revisor de los 5 PDF (València 2.302 / 2.171 / 3.314 / 2.960 / 2.538; `docs/revision_f1.md` §2). Rol **robustez** por N = 5.")
    A("- Registradores ERI anuario: sumas CCAA = provincias = España = 0 de diferencia; % de extranjeros: nacionales + extranjeros = 100 %. La tabla de nacionalidades suma 97,96 % (defecto del origen, no se usa).")
    A("")

    A("## E. Fuentes raw no utilizadas, excluidas o con duplicados\n")
    A("Duplicados idénticos en origen (se usa el primer código, verificado valor a valor):\n")
    for note in sorted(set(DUP_NOTES)):
        A(f"- {note}")
    A("")
    A("| Archivo | Motivo |")
    A("|---|---|")
    for f, m in NO_USADAS:
        A(f"| `{f}` | {m} |")
    A("")

    A("## F. Cobertura de la muestra base 2008Q1+\n")
    key = ["ln_ipv", "ln_ocupados", "tipo_hip", "ln_permisos", "ln_costes", "ln_renta_hog_real",
           "ln_pob_extranj", "ln_terminadas", "ln_hogares_epa"]
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
    sin_h = base[[c for c in key if c != "ln_hogares_epa"]].dropna()
    last_sin_h = nac_i.loc[sin_h.index.max(), "trimestre"] if len(sin_h) else "-"
    A(f"- `ln_hogares_epa` (principal) cubre desde 2002T1 y no restringe la muestra. Con `ln_hogares_ecp` (robustez, 2021T1+) la muestra común empezaría en 2021: ver `hogares_ecp`.")
    A(f"- Sin hogares (8 variables): N = **{len(sin_h)}**, último trimestre común = **{last_sin_h}**.")
    A("- Los N son de las variables `ln_`; las diferencias `d_ln_` pierden 1 trimestre al inicio y `d4_ln_` pierde 4.\n")

    A("## G. `data/processed/validacion_gva.csv` (contrastes del registro GVA: VUT y padrón)\n")
    A("Generado por `build_validacion_gva()`. Columna `independiente`: **sí** solo si el contraste usa una fuente distinta; **no independiente** si ambos lados son el mismo registro o padrón (consistencia interna); **no comparable** si definición, fecha o ámbito difieren (solo plausibilidad). `nota` de `vut_foto_*`: la lista vigente no es una serie temporal.\n")
    A("| Bloque | Contraste | Territorio | N | error_max | valor_ref | independiente | nota |")
    A("|---|---|---|---|---|---|---|---|")
    for _, r in validacion.iterrows():
        em = "—" if pd.isna(r["error_max"]) else f"{r['error_max']:.0f}" if float(r["error_max"]).is_integer() else f"{r['error_max']:.3f}"
        A(f"| {_esc(r['bloque'])} | {_esc(r['check'])} | {_esc(r['territorio'])} | {int(r['n_obs'])} | {em} | {_esc(r['valor_ref'])} | {_esc(r['independiente'])} | {_esc(r['nota'])} |")
    A("")
    A("Sin GVA: `vut_stock_*` 2010-2024 es un **registro administrativo** (no padrón ni encuesta). Su 'reconstrucción' por altas acumuladas es una identidad contable, no un contraste independiente. La ratio frente al INE VUT (tabla 39366) solo sirve de plausibilidad.\n")

    (DOCS / "diccionario_variables.md").write_text("\n".join(L) + "\n", encoding="utf-8")


def checks(nac: pd.DataFrame, panel: pd.DataFrame, panel_a: pd.DataFrame, valencia: pd.DataFrame,
           nacionalidad: pd.DataFrame, pob77: pd.DataFrame) -> None:
    print("=== COMPROBACIONES FINALES ===")
    m08 = nac[nac["trimestre"] >= "2008Q1"]
    print(f"N nacional_q (filas 2008Q1+): {len(m08)}  (rango total {nac['trimestre'].iloc[0]}..{nac['trimestre'].iloc[-1]}, filas {len(nac)})")
    print(f"N nacional_q 2008Q1+ con hogares_epa: {int(m08['hogares_epa'].notna().sum())}  (rango hogares_epa {nac.loc[nac['hogares_epa'].notna(), 'trimestre'].iloc[0]}..{nac.loc[nac['hogares_epa'].notna(), 'trimestre'].iloc[-1]})")
    last_ipv = nac.loc[nac["ipv"].notna(), "trimestre"].iloc[-1]
    print(f"Último trimestre con ipv: {last_ipv}  (N ipv 2008Q1+ = {int(m08['ipv'].notna().sum())})")
    print(f"Nº CCAA en panel_ccaa_q: {panel['codigo_ine_ccaa'].nunique()}  |  panel_ccaa_a: {panel_a['codigo_ine_ccaa'].nunique()} CCAA x {panel_a['anio'].nunique()} años ({panel_a['anio'].min()}-{panel_a['anio'].max()})")
    print(f"Nº filas panel_ccaa_a con pob_extranj: {int(panel_a['pob_extranj'].notna().sum())}; con ipv anual: {int(panel_a['ipv'].notna().sum())}")

    # Duplicados de clave
    dups = {
        "nacional_q (trimestre)": int(nac["trimestre"].duplicated().sum()),
        "panel_ccaa_q (codigo,trimestre)": int(panel.duplicated(["codigo_ine_ccaa", "trimestre"]).sum()),
        "panel_ccaa_a (codigo,anio)": int(panel_a.duplicated(["codigo_ine_ccaa", "anio"]).sum()),
        "valencia (territorio,periodo,variable)": int(valencia.duplicated(["territorio", "periodo", "variable"]).sum()),
        "panel_ccaa_nacionalidad (ccaa,nacionalidad,trimestre,tipo)": int(nacionalidad.duplicated(["codigo_ine_ccaa", "nacionalidad", "trimestre", "tipo_registro"]).sum()),
    }
    print("Duplicados de clave: " + "; ".join(f"{k}={v}" for k, v in dups.items()))

    # Aditividad de grupos 77019 (CCAA) y extranjera = suma de grupos
    pv = pob77.pivot_table(index=["codigo_ine_ccaa", "anio"], columns="grupo", values="pob_stock", aggfunc="first")
    base_g = ["Apátridas", "De Oceanía", "De Asia", "De Sudamérica", "De Centro América y Caribe",
              "De América del Norte", "De Africa"]
    g27 = base_g + ["País de Europa menos UE27_2020", "País de la UE27_2020 sin España"]
    g28 = base_g + ["País de Europa menos UE28", "País de la UE28 sin España"]
    d27 = (pv["Extranjera"] - pv[g27].sum(axis=1, min_count=len(g27))).abs().dropna()
    d28 = (pv["Extranjera"] - pv[g28].sum(axis=1, min_count=len(g28))).abs().dropna()
    print(f"77019: Extranjera - suma(grupos, familia UE27) max |dif| = {d27.max():.0f} ({len(d27)} CCAA-años)")
    print(f"77019: Extranjera - suma(grupos, familia UE28) max |dif| = {d28.max():.0f} ({len(d28)} CCAA-años)")
    difa = pd.concat([d27, d28])
    difb = (pv["Total"] - pv["Española"] - pv["Extranjera"]).abs()
    print(f"77019: Total - Española - Extranjera max |dif| = {difb.max():.0f}")

    # Contrastes ya calculados en la construccion
    print(f"Padrón València: DPOP21796 vs Total padrón nacionalidad (1998-2022) max |dif| = {CHECK.get('vlc_total_dpop_vs_padron_nac_max_dif')}")
    print(f"Padrón València: Total - Española - Extranjera max |dif| = {CHECK.get('vlc_esp_mas_ext_vs_total_max_dif')}")
    print(f"Padrón València: GVA extranjeros vs INE padrón extranjeros: max |dif| = {CHECK.get('gva_ext_vs_ine_ext_max_dif')} personas ({CHECK.get('gva_ext_vs_ine_ext_n')} años)")
    print(f"SERPAVI València: distritos agregados con nº distritos por año = {CHECK.get('serpavi_dist_n_distritos')}")

    # Controles (3 cifras nuevas contra data/raw)
    ctrl = []
    nm_raw = pd.read_csv(RAW / "pdf" / "notariado_cv_municipios_anual.csv", dtype=str)
    nm_raw = nm_raw[(nm_raw["territorio"] == "Valencia") & (nm_raw["nacionalidad"] == "Total general") & (nm_raw["fecha"] == "2025-01-01")]
    v_csv = valencia[(valencia["territorio"] == "València (municipio)") & (valencia["variable"] == "notariado_viv_extranj") & (valencia["periodo"] == "2025")]
    ctrl.append(("notariado València Total general 2025 (raw vs valencia.csv)", float(nm_raw["valor"].iloc[0]), float(v_csv["valor"].iloc[0])))
    pr = pd.read_csv(RAW / "ine_ecp_ccaa_paises.csv", dtype=str)
    pr_row = pr[(pr["nombre"] == "Comunitat Valenciana. Todas las edades. Extranjera. Total. Población. Número.") & (pr["fecha"] == "2024-01-01")]
    pa24 = panel_a[(panel_a["codigo_ine_ccaa"] == "10") & (panel_a["anio"] == 2024)]["pob_extranj"].iloc[0]
    ctrl.append(("población extranjera C. Valenciana 2024 (77019 raw vs panel_ccaa_a)", float(pr_row["valor"].iloc[0]), float(pa24)))
    eh = pd.read_csv(RAW / "ine_epa_hogares.csv", dtype=str)
    eh_row = eh[(eh["serie"] == "EPA430446") & (eh["fecha"] == "2025-10-01")]
    eh25 = nac.loc[nac["trimestre"] == "2025Q4", "hogares_epa"].iloc[0]
    ctrl.append(("hogares EPA total 2025T4 (raw EPA430446 vs nacional_q)", float(eh_row["valor"].iloc[0]), float(eh25)))
    for name, raw_v, out_v in ctrl:
        ok = np.isclose(raw_v, out_v, rtol=1e-9)
        print(f"Control {name}: raw={raw_v} salida={out_v} -> {'OK' if ok else 'DIFERENTE'}")

    # Controles previos (se mantienen)
    ipv_raw = pd.read_csv(RAW / "ine_ipv_80270.csv", dtype=str)
    ipv_raw = ipv_raw[(ipv_raw["serie"] == "IPV1209") & (ipv_raw["fecha"] == "2015-01-01")]
    epa_raw = pd.read_csv(RAW / "ine_epa_ocupados.csv", dtype=str)
    epa_raw = epa_raw[epa_raw["fecha"] == "2019-10-01"]
    st_raw = pd.read_csv(RAW / "ecb_stock_credito_vivienda_es.csv", dtype=str)
    st_raw = st_raw[st_raw["fecha"] == "2020-12-01"]
    for name, raw_v, csv_v in [
        ("ipv 2015Q1 (IPV1209)", float(ipv_raw["valor"].iloc[0]), nac.loc[nac["trimestre"] == "2015Q1", "ipv"].iloc[0]),
        ("ocupados 2019Q4 (EPA387796)", float(epa_raw["valor"].iloc[0]), nac.loc[nac["trimestre"] == "2019Q4", "ocupados"].iloc[0]),
        ("credito_stock 2020Q4 (BSI, fin de trimestre)", float(st_raw["valor"].iloc[0]), nac.loc[nac["trimestre"] == "2020Q4", "credito_stock"].iloc[0]),
    ]:
        ok = np.isclose(raw_v, float(csv_v), rtol=1e-9)
        print(f"Control {name}: raw={raw_v} csv={csv_v} -> {'OK' if ok else 'DIFERENTE'}")

    # pob_extranj nacional (ECP701) frente a 56936/59585 y suma de CCAA
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
    cs = nac[["trimestre", "pob_extranj", "pob_extranj_ccaa_sum"]].dropna()
    print(f"pob_extranj_ccaa_sum vs pob_extranj nacional: {len(cs)} trimestres; max |dif| = {(cs.pob_extranj_ccaa_sum - cs.pob_extranj).abs().max():.0f} (Ceuta y Melilla y error de interpolación anual; ver diccionario)")

    # EPA frente a ECP en solape
    sol = nac[["trimestre", "hogares_epa", "hogares_ecp"]].dropna()
    rt = sol["hogares_epa"] / (sol["hogares_ecp"] / 1000) - 1  # ECP en unidades, EPA en miles
    print(f"hogares EPA / (ECP60131/1000) - 1 en el solape ({len(sol)} trimestres): min {rt.min()*100:.2f} %, max {rt.max()*100:.2f} %")
    cgn = pd.read_csv(RAW / "pdf" / "notariado_cgn_extranjeros_semestral.csv", dtype=str)
    cgn["valor"] = pd.to_numeric(cgn["valor"], errors="coerce")
    a_ = cgn[(cgn["tabla"] == "T1") & (cgn["serie"] == "op_viv_libre") & (cgn["categoria"] == "Extranjero") & (cgn["territorio"] == "Espana")][["fecha", "valor"]]
    b_ = cgn[(cgn["tabla"] == "T2") & (cgn["serie"] == "op_viv_libre_extranjeros") & (cgn["categoria"] == "Extranjero") & (cgn["territorio"] == "Nacional")][["fecha", "valor"]]
    mm_ = a_.merge(b_, on="fecha")
    print(f"CGN: T1 Espana vs T2 Nacional (extranjeros, vivienda libre): {len(mm_)} semestres; max |dif| = {(mm_.valor_x - mm_.valor_y).abs().max():.0f}")


def checks_nuevos(nac: pd.DataFrame, panel: pd.DataFrame, panel_a: pd.DataFrame, valencia: pd.DataFrame,
                  nacional_a: pd.DataFrame, validacion: pd.DataFrame) -> None:
    print("=== COMPROBACIONES NUEVAS (deflactor SA, banderas, cobertura, GVA) ===")
    # 1) Patron estacional del deflactor: media de d_ln_renta_hog_real por trimestre (2008Q1+)
    x = nac[nac["trimestre"] >= "2008Q1"].dropna(subset=["d_ln_renta_hog_real"])
    m_q = (x["d_ln_renta_hog_real"] * 100).groupby(x["trimestre"].str[-2:]).mean()
    print("d_ln_renta_hog_real media por trimestre (%, 2008Q1+, deflactor SA): " +
          ", ".join(f"{k} {v:+.2f}" for k, v in m_q.items()) + "  (antes NSA: Q1 +0,99, Q2 -0,79, Q3 +2,57, Q4 -1,76)")
    xe = x[~x["trimestre"].str[:4].isin(["2020", "2021"])]
    m_qe = (xe["d_ln_renta_hog_real"] * 100).groupby(xe["trimestre"].str[-2:]).mean()
    print("d_ln_renta_hog_real media por trimestre sin 2020-2021 (%): " +
          ", ".join(f"{k} {v:+.2f}" for k, v in m_qe.items()) + "  (antes: Q1 +1,05, Q2 -0,28, Q3 +1,84, Q4 -1,50)")
    y = nac[nac["trimestre"] >= "2008Q1"].dropna(subset=["d_ln_deflactor"])
    m_d = (y["d_ln_deflactor"] * 100).groupby(y["trimestre"].str[-2:]).mean()
    print("d_ln_deflactor media por trimestre (%, SA): " + ", ".join(f"{k} {v:+.2f}" for k, v in m_d.items()))
    # 2) Quiebre EPA
    e = nac.set_index("trimestre")
    print(f"d_ln_hogares_epa 2021Q1 = {e.loc['2021Q1', 'd_ln_hogares_epa'] * 100:+.2f} % ; quiebre_epa_2021 = 1 desde 2021Q1: "
          f"suma {int(nac['quiebre_epa_2021'].sum())} trimestres")
    # 3) Banderas por fichero
    print("Banderas _metodo por fichero (filas con dato):")
    for nom, df_ in [("nacional_q", nac), ("nacional_a", nacional_a), ("panel_ccaa_q", panel), ("panel_ccaa_a", panel_a)]:
        for c, cnt in metodo_resumen(df_):
            if cnt:
                print(f"  {nom}.{c}: " + ", ".join(f"{k}={v}" for k, v in cnt.items()))
    vc = valencia["metodo"].dropna().value_counts()
    print("  valencia.metodo: " + ", ".join(f"{k}={int(vc[k])}" for k in METODOS if k in vc.index))
    print(f"  _interp TRUE por fichero: nacional_q={sum(int(nac[c].sum()) for c in nac.columns if c.endswith('_interp'))}, "
          f"panel_ccaa_q={sum(int(panel[c].sum()) for c in panel.columns if c.endswith('_interp'))}, "
          f"panel_ccaa_a={sum(int(panel_a[c].sum()) for c in panel_a.columns if c.endswith('_interp'))}, "
          f"valencia={int(valencia['interp'].sum())}")
    # 4) Cobertura de columnas nuevas de panel_ccaa_a
    print("Cobertura panel_ccaa_a (CCAA-años con dato, de 17 x 24 = 408):")
    for v in ["trans_extranjeros", "trans_total", "visados", "terminadas", "ipc_alquiler",
              "pob_europa_sin_espana", "ipv", "compraventas"]:
        n_ = int(panel_a[v].notna().sum())
        yrs = panel_a.dropna(subset=[v])["anio"]
        rng = f"{yrs.min()}-{yrs.max()}" if n_ else "-"
        print(f"  {v}: {n_} ({rng})")
    # Residuo 'Europa sin España' frente a pob_extranj − no europeos
    nonEU = ["pob_africa", "pob_asia", "pob_sudamerica", "pob_centroamerica_caribe", "pob_norteamerica",
             "pob_oceania", "pob_apatridas"]
    resid = panel_a["pob_extranj"] - panel_a[nonEU].sum(axis=1, min_count=len(nonEU))
    dif = (panel_a["pob_europa_sin_espana"] - resid).abs().dropna()
    print(f"pob_europa_sin_espana vs residuo (pob_extranj − no europeos): max |dif| = {dif.max():.0f} personas ({len(dif)} CCAA-años)")
    # 5) nacional_a
    print(f"nacional_a: {len(nacional_a)} años ({int(nacional_a['anio'].min())}-{int(nacional_a['anio'].max())}); "
          f"inmig_anual_eurostat {int(nacional_a['inmig_anual_eurostat'].notna().sum())} años")
    # 6) GVA
    print("validacion_gva.csv:")
    for _, r in validacion.iterrows():
        print(f"  [{r['independiente'][:22]}] {r['check'][:70]} | n={r['n_obs']} | error_max={r['error_max']}")


def main() -> None:
    PROC.mkdir(parents=True, exist_ok=True)
    DOCS.mkdir(parents=True, exist_ok=True)

    pob77 = pob77_long(read_raw("ine_ecp_ccaa_paises.csv", ["fecha", "serie", "valor", "nombre"]))
    panel = finalize_panel(build_panel(pob77))
    panel.to_csv(PROC / "panel_ccaa_q.csv", index=False)

    # Control: suma de 17 CCAA de pob_extranj por trimestre (solo si estan las 17)
    g = panel.groupby("trimestre")
    suma = g["pob_extranj"].agg(lambda x: x.sum() if x.notna().sum() == 17 else np.nan)
    flag = g["pob_extranj_interp"].any()
    ccaa_sum = pd.DataFrame({"valor": suma, "interp": flag})
    ccaa_sum.index = pd.PeriodIndex(ccaa_sum.index, freq="Q")

    nac = finalize_nacional(build_nacional(ccaa_sum))
    nac.to_csv(PROC / "nacional_q.csv", index=False)

    nacional_a = build_nacional_a(nac)
    nacional_a.to_csv(PROC / "nacional_a.csv", index=False)

    nacionalidad = build_nacionalidad(pob77)
    nacionalidad.to_csv(PROC / "panel_ccaa_nacionalidad.csv", index=False)

    panel_a = build_panel_a(panel, pob77)
    panel_a.to_csv(PROC / "panel_ccaa_a.csv", index=False)

    valencia = build_valencia()
    valencia.to_csv(PROC / "valencia.csv", index=False)

    validacion = build_validacion_gva()
    validacion.to_csv(PROC / "validacion_gva.csv", index=False)

    write_dictionary(nac, panel, panel_a, valencia, nacionalidad, nacional_a, validacion)
    checks(nac, panel, panel_a, valencia, nacionalidad, pob77)
    checks_nuevos(nac, panel, panel_a, valencia, nacional_a, validacion)
    print(f"Escritos: {PROC/'nacional_q.csv'}, {PROC/'nacional_a.csv'}, {PROC/'panel_ccaa_q.csv'}, "
          f"{PROC/'panel_ccaa_a.csv'}, {PROC/'panel_ccaa_nacionalidad.csv'}, {PROC/'valencia.csv'}, "
          f"{PROC/'validacion_gva.csv'}, {DOCS/'diccionario_variables.md'}")


if __name__ == "__main__":
    main()
