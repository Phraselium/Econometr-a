"""V15 · Fase 1.2 · Auditoría de datos del grupo ALQUILER (capa C4, DESCRIPTIVO).

Sin efectos ni regresiones. Cruces territoriales solo por código INE. SEED=20261010 (el script no
usa aleatoriedad; la semilla se fija por regla del proyecto).
Lee data/base y data/raw (solo lectura); escribe en output/v15/auditoria/alquiler/.
Incasòl e Inside Airbnb (licencia no abierta): solo estadísticos resumen en las salidas.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

import duckdb
import numpy as np
import pandas as pd

SEED = 20261010
RAIZ = Path(__file__).resolve().parents[3]
OUT = RAIZ / "output" / "v15" / "auditoria" / "alquiler"
UMBRAL_Z = 5.0
MIN_T_TEMPORAL = 8
MIN_N_FIANZAS = 10
ABIERTA = {"IPC": True, "SERPAVI": True, "IPVA": True, "GVA": True, "EMAL": True, "INCASOL": False, "HICP": True}

CCAA_DE_PROV = {}
for _c, _ps in {
    "01": "04 11 14 18 21 23 29 41", "02": "22 44 50", "03": "33", "04": "07", "05": "35 38", "06": "39",
    "07": "05 09 24 34 37 40 42 47 49", "08": "02 13 16 19 45", "09": "08 17 25 43", "10": "03 12 46",
    "11": "06 10", "12": "15 27 32 36", "13": "28", "14": "30", "15": "31", "16": "01 20 48", "17": "26",
    "18": "51", "19": "52",
}.items():
    for _p in _ps.split():
        CCAA_DE_PROV[_p] = _c

np.random.seed(SEED)
CON = duckdb.connect()
CON.execute(f"create view h as select * from '{RAIZ / 'data' / 'base' / 'hechos.parquet'}'")


# ----------------------------------------------------------------------------- utilidades
def base(variable: str, nivel: str | None = None, freq: str | None = None, desag: str | None = None,
         edicion_like: str | None = None) -> pd.DataFrame:
    w = [f"variable = '{variable}'"]
    if nivel:
        w.append(f"nivel = '{nivel}'")
    if freq:
        w.append(f"frecuencia = '{freq}'")
    if desag is not None:
        w.append(f"desagregacion = '{desag}'")
    if edicion_like:
        w.append(f"edicion like '{edicion_like}'")
    sql = ("select nivel, territorio_codigo as territorio, periodo, desagregacion as desag, valor, edicion "
           "from h where " + " and ".join(w))
    return CON.execute(sql).fetchdf()


def t_index(periodo: pd.Series) -> pd.Series:
    """Entero ordenable: año (anual) o año*4+trimestre-1 (trimestral)."""
    s = periodo.astype(str)
    if s.str.contains("T").any():
        y = s.str[:4].astype(int)
        q = s.str[-1].astype(int)
        return y * 4 + q - 1
    return s.str[:4].astype(int)


def yoy(df: pd.DataFrame, key: list[str], lag: int = 1, tcol: str = "t", vcol: str = "valor") -> pd.DataFrame:
    """Tasa interanual (%) entre t y t-lag (solo si ambos existen)."""
    a = df[key + [tcol, vcol]].copy()
    b = a.rename(columns={vcol: "prev"}).copy()
    b[tcol] = b[tcol] + lag
    m = a.merge(b, on=key + [tcol], how="inner")
    m = m[(m["prev"] > 0) & (m[vcol] > 0)]
    m["yoy"] = 100.0 * (m[vcol] / m["prev"] - 1.0)
    return m


def annual_from_quarterly(df: pd.DataFrame, key: list[str]) -> pd.DataFrame:
    d = df.copy()
    d["anio"] = d["periodo"].astype(str).str[:4].astype(int)
    g = d.groupby(key + ["anio"]).agg(valor=("valor", "mean"), nq=("valor", "size")).reset_index()
    g = g[g["nq"] == 4].rename(columns={"anio": "t"})
    return g.drop(columns="nq")


def rz(x: pd.Series) -> pd.Series:
    med = x.median()
    mad = (x - med).abs().median()
    if not np.isfinite(mad) or mad == 0:
        return pd.Series(np.nan, index=x.index)
    return 0.6745 * (x - med) / mad


def prov_de(cod: str) -> str:
    return str(cod)[:2]


def panel(serie: str, nivel: str, df: pd.DataFrame) -> pd.DataFrame:
    """Normaliza a columnas serie, nivel, territorio, t (año), yoy."""
    d = df[["territorio", "t", "yoy"]].copy()
    d["serie"] = serie
    d["nivel"] = nivel
    return d[["serie", "nivel", "territorio", "t", "yoy"]]


# ----------------------------------------------------------------------------- construcción
def leer_gva() -> pd.DataFrame:
    fs = sorted((RAIZ / "data" / "raw" / "v9" / "gva_fianzas").glob("gva_fianzas_20*.csv"))
    out = []
    for f in fs:
        d = pd.read_csv(f, sep=";", dtype=str)
        d["anio"] = int(f.stem[-4:])
        out.append(d)
    g = pd.concat(out, ignore_index=True)
    g["territorio"] = g["cod_provincia"].str.zfill(2) + g["cod_municipio"].str.zfill(3)
    g["importe"] = pd.to_numeric(g["importe_fianza"], errors="coerce")
    return g


def gva_paneles(g: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    ok = g[(g["importe"] > 0) & (g["anio"] <= 2025)]
    mun = ok.groupby(["territorio", "anio"]).agg(valor=("importe", "median"), n=("importe", "size")).reset_index()
    prv = ok.assign(territorio=ok["cod_provincia"].str.zfill(2)).groupby(["territorio", "anio"]).agg(
        valor=("importe", "median"), n=("importe", "size")).reset_index()
    mun = mun.rename(columns={"anio": "t"})
    prv = prv.rename(columns={"anio": "t"})
    ym = yoy(mun[mun["n"] >= MIN_N_FIANZAS], ["territorio"])
    # exige n mínimo también en t-1
    nprev = mun.assign(t=mun["t"] + 1)[["territorio", "t", "n"]].rename(columns={"n": "n_prev"})
    ym = ym.merge(nprev, on=["territorio", "t"], how="left")
    ym = ym[ym["n_prev"] >= MIN_N_FIANZAS]
    yp = yoy(prv, ["territorio"])
    return mun, ym, yp


def incasol_anual() -> pd.DataFrame:
    c = base("incasol_contratos", "municipio", "A")
    r = base("incasol_renta_media", "municipio", "A")
    m = c.merge(r, on=["territorio", "periodo", "desag"], how="left", suffixes=("_c", "_r"))
    m["t"] = m["periodo"].astype(str).str[:4].astype(int)
    m["cr"] = m["valor_c"] * m["valor_r"]
    m["c_con_renta"] = np.where(m["valor_r"].notna(), m["valor_c"], 0.0)
    g = m.groupby(["territorio", "t"]).agg(contratos=("valor_c", "sum"), c_renta=("c_con_renta", "sum"),
                                             cr=("cr", "sum")).reset_index()
    g["cobertura_renta"] = np.where(g["contratos"] > 0, g["c_renta"] / g["contratos"], np.nan)
    g["valor"] = np.where(g["c_renta"] > 0, g["cr"] / g["c_renta"], np.nan)
    return g


def construir() -> dict:
    P: dict[str, pd.DataFrame] = {}
    F: dict[str, str] = {}  # serie -> familia/fuente
    TIPO: dict[str, str] = {}  # stock | nuevos
    AUX: dict = {}

    # --- IPC alquiler (stock de contratos vigentes)
    for nivel in ("nacional", "ccaa"):
        d = base("ipc_alquiler", nivel, "T")
        d["t"] = t_index(d["periodo"])
        AUX[f"ipc_T_{nivel}"] = yoy(d.assign(territorio=d["territorio"]), ["territorio"], lag=4)
        a = annual_from_quarterly(d, ["territorio"])
        P[f"IPC_{nivel}"] = panel("IPC", nivel, yoy(a, ["territorio"]))
    ipcp = base("ipc_alquiler_yoy", "provincia", "A")
    ipcp["t"] = ipcp["periodo"].astype(int)
    ipcp["yoy"] = ipcp["valor"]
    P["IPC_provincia"] = panel("IPC", "provincia", ipcp)
    ipci = base("ipc_alquiler_indice", "provincia", "A")
    ipci["t"] = ipci["periodo"].astype(int)
    AUX["ipc_idx_prov_A"] = ipci
    AUX["ipc_idx_prov_yoy_recalc"] = yoy(ipci, ["territorio"])
    AUX["ipc_yoy_prov_pub"] = ipcp
    ipcq = base("ipc_alquiler_yoy", "provincia", "T")
    ipcq["t"] = t_index(ipcq["periodo"])
    ipcq["yoy"] = ipcq["valor"]
    AUX["ipc_prov_T_pub"] = ipcq
    for s in ("IPC_nacional", "IPC_ccaa", "IPC_provincia"):
        F[s], TIPO[s] = "IPC", "stock"

    # --- IPVA
    for nivel in ("nacional", "ccaa", "provincia"):
        pub = base("ipva_var_anual", nivel)
        pub["t"] = pub["periodo"].astype(int)
        pub["yoy"] = pub["valor"]
        for etiqueta, nom in (("Contrato existente", "IPVA_EXIST"), ("Nuevo contrato", "IPVA_NUEVO"),
                               ("Total", "IPVA_TOTAL")):
            x = pub[pub["desag"] == f"contrato={etiqueta}"]
            s = f"{nom}_{nivel}"
            P[s] = panel(nom, nivel, x)
            F[s] = "IPVA"
            TIPO[s] = "nuevos" if nom == "IPVA_NUEVO" else "stock"
    ipv = base("ipva_indice", "provincia", desag="")
    ipv["t"] = ipv["periodo"].astype(int)
    AUX["ipva_idx_prov_panel"] = ipv
    y = yoy(ipv, ["territorio"])
    P["IPVA_PANEL_provincia"] = panel("IPVA_PANEL", "provincia", y)
    F["IPVA_PANEL_provincia"], TIPO["IPVA_PANEL_provincia"] = "IPVA", "stock"
    for nivel in ("distrito", "municipio"):
        x = base("ipva_tam_var_anual", nivel)
        x["t"] = x["periodo"].astype(int)
        x["yoy"] = x["valor"]
        s = f"IPVA_TAM_{nivel}"
        P[s] = panel("IPVA_TAM", nivel, x)
        F[s], TIPO[s] = "IPVA", "stock"
    xd = base("ipva_var_anual", "distrito")
    xd["t"] = xd["periodo"].astype(int)
    xd["yoy"] = xd["valor"]
    P["IPVA_TOTAL_distrito"] = panel("IPVA_TOTAL", "distrito", xd)
    F["IPVA_TOTAL_distrito"], TIPO["IPVA_TOTAL_distrito"] = "IPVA", "stock"

    # --- SERPAVI (stock IRPF), vivienda colectiva VC y unifamiliar VU
    ser = {}
    for tip in ("VC", "VU"):
        for nivel in ("municipio", "provincia", "distrito", "seccion"):
            d = base("serpavi_alquiler_m2_mediana", nivel, desag=f"tipologia={tip}")
            d["t"] = d["periodo"].astype(int)
            ser[(tip, nivel)] = d
            y = yoy(d, ["territorio"])
            s = f"SERPAVI_{tip}_{nivel}"
            P[s] = panel(f"SERPAVI_{tip}", nivel, y)
            F[s], TIPO[s] = "SERPAVI", "stock"
    AUX["serpavi_niveles"] = ser
    nprov = base("serpavi_n_contratos_recuento", "provincia", desag="tipologia=VC")
    nprov["t"] = nprov["periodo"].astype(int)
    AUX["serpavi_n_prov"] = nprov
    nmun = base("serpavi_n_contratos_recuento", "municipio")
    nmun["t"] = nmun["periodo"].astype(int)
    AUX["serpavi_n_mun"] = nmun
    # agregados nacional / ccaa de SERPAVI VC (media de tasas provinciales ponderada por contratos)
    yp = yoy(ser[("VC", "provincia")], ["territorio"]).merge(
        nprov[["territorio", "t", "valor"]].rename(columns={"valor": "w"}), on=["territorio", "t"], how="left")
    yp = yp[yp["w"] > 0]
    yp["ccaa"] = yp["territorio"].map(CCAA_DE_PROV)
    agg_c = yp.groupby(["ccaa", "t"]).apply(lambda g: np.average(g["yoy"], weights=g["w"]),
                                            include_groups=False).rename("yoy").reset_index()
    agg_c = agg_c.rename(columns={"ccaa": "territorio"})
    P["SERPAVI_VC_ccaa"] = panel("SERPAVI_VC", "ccaa", agg_c)
    agg_n = yp.groupby("t").apply(lambda g: np.average(g["yoy"], weights=g["w"]),
                                  include_groups=False).rename("yoy").reset_index()
    agg_n["territorio"] = "00"
    P["SERPAVI_VC_nacional"] = panel("SERPAVI_VC", "nacional", agg_n)
    for s in ("SERPAVI_VC_ccaa", "SERPAVI_VC_nacional"):
        F[s], TIPO[s] = "SERPAVI", "stock"

    # --- Fianzas GVA (contratos nuevos; el crudo trae todos los municipios, la base solo València ciudad)
    g = leer_gva()
    AUX["gva_raw"] = g
    mun, ym, yp_ = gva_paneles(g)
    AUX["gva_mun_nivel"] = mun
    P["GVA_municipio"] = panel("GVA", "municipio", ym)
    P["GVA_provincia"] = panel("GVA", "provincia", yp_)
    for s in ("GVA_municipio", "GVA_provincia"):
        F[s], TIPO[s] = "GVA", "nuevos"

    # --- Incasòl (contratos nuevos; licencia no abierta)
    inc = incasol_anual()
    AUX["incasol"] = inc
    ok = inc[(inc["cobertura_renta"] >= 0.9) & inc["valor"].notna() & (inc["contratos"] >= MIN_N_FIANZAS)]
    ymi = yoy(ok, ["territorio"])
    nprev = inc.assign(t=inc["t"] + 1)[["territorio", "t", "contratos"]].rename(columns={"contratos": "n_prev"})
    ymi = ymi.merge(nprev, on=["territorio", "t"], how="left")
    ymi = ymi[ymi["n_prev"] >= MIN_N_FIANZAS]
    P["INCASOL_municipio"] = panel("INCASOL", "municipio", ymi)
    okp = ok.assign(prov=ok["territorio"].str[:2])
    ap = okp.groupby(["prov", "t"]).apply(lambda x: np.average(x["valor"], weights=x["contratos"]),
                                          include_groups=False).rename("valor").reset_index()
    ap = ap.rename(columns={"prov": "territorio"})
    P["INCASOL_provincia"] = panel("INCASOL", "provincia", yoy(ap, ["territorio"]))
    ac = ok.groupby("t").apply(lambda x: np.average(x["valor"], weights=x["contratos"]),
                               include_groups=False).rename("valor").reset_index()
    ac["territorio"] = "09"
    P["INCASOL_ccaa"] = panel("INCASOL", "ccaa", yoy(ac, ["territorio"]))
    for s in ("INCASOL_municipio", "INCASOL_provincia", "INCASOL_ccaa"):
        F[s], TIPO[s] = "INCASOL", "nuevos"

    # --- EMAL (Euskadi, contratos nuevos, 20 municipios; CC BY)
    e = base("emal_renta_mensual_eur", "municipio", "T")
    e["t"] = t_index(e["periodo"])
    AUX["emal_T"] = yoy(e, ["territorio"], lag=4)
    ea = annual_from_quarterly(e, ["territorio"])
    P["EMAL_municipio"] = panel("EMAL", "municipio", yoy(ea, ["territorio"]))
    F["EMAL_municipio"], TIPO["EMAL_municipio"] = "EMAL", "nuevos"

    # --- HICP alquileres efectivos España (control de coherencia del IPC)
    hh = base("hicp_alquiler_indice", "pais")
    hh = hh[hh["territorio"] == "ES"].copy()
    hh["anio"] = hh["periodo"].astype(str).str[:4].astype(int)
    ha = hh.groupby("anio").agg(valor=("valor", "mean"), n=("valor", "size")).reset_index()
    ha = ha[ha["n"] == 12].rename(columns={"anio": "t"})
    ha["territorio"] = "00"
    P["HICP_nacional"] = panel("HICP", "nacional", yoy(ha, ["territorio"]))
    F["HICP_nacional"], TIPO["HICP_nacional"] = "HICP", "stock"
    return {"P": P, "F": F, "TIPO": TIPO, "AUX": AUX}


# ----------------------------------------------------------------------------- 1. atípicos
def z_series(d: pd.DataFrame, modo: str, suelo: float = 0.0) -> tuple[pd.Series, pd.Series]:
    """z robusto = 0,6745 (x - mediana) / MAD; con `suelo` > 0 la escala es max(MAD, suelo). Devuelve (z, MAD)."""
    d = d.copy()
    clave, minimo = ("territorio", MIN_T_TEMPORAL) if modo == "temporal" else ("t", 30)
    g = d.groupby(clave)["yoy"]
    n = g.transform("size")
    med = g.transform("median")
    d["dev"] = (d["yoy"] - med).abs()
    mad = d.groupby(clave)["dev"].transform("median")
    escala = np.maximum(mad, suelo) if suelo > 0 else mad.where(mad > 0)
    z = 0.6745 * (d["yoy"] - med) / escala
    return z.where(n >= minimo), mad.where(n >= minimo)


def atipicos(R: dict) -> tuple[pd.DataFrame, pd.DataFrame, dict]:
    P, F = R["P"], R["F"]
    extra = {
        "IPC_nacional_trimestral": ("IPC", "nacional", R["AUX"]["ipc_T_nacional"]),
        "IPC_ccaa_trimestral": ("IPC", "ccaa", R["AUX"]["ipc_T_ccaa"]),
        "IPC_provincia_trimestral": ("IPC", "provincia", R["AUX"]["ipc_prov_T_pub"]),
        "EMAL_municipio_trimestral": ("EMAL", "municipio", R["AUX"]["emal_T"]),
    }
    items = [(s, F[s], p["nivel"].iloc[0], p) for s, p in P.items()]
    for s, (fte, nivel, d) in extra.items():
        dd = d[["territorio", "t", "yoy"]].copy()
        items.append((s, fte, nivel, dd))
    filas, tops = [], []
    for s, fte, nivel, d in items:
        d = d.dropna(subset=["yoy"]).reset_index(drop=True)
        if d.empty:
            continue
        long_med = d.groupby("territorio").size().median()
        modo = "temporal" if long_med >= MIN_T_TEMPORAL else "transversal"
        z, mad = z_series(d, modo)
        zs, _ = z_series(d, modo, suelo=1.0)
        d = d.assign(z=z, mad=mad)
        evaluables = int(d["z"].notna().sum())
        fl = d[d["z"].abs() > UMBRAL_Z]
        filas.append({"serie": s, "fuente": fte, "nivel": nivel, "modo": modo, "n_obs": len(d),
                      "n_evaluables": evaluables, "n_atipicos": len(fl),
                      "n_atipicos_escala_min_1pp": int((zs.abs() > UMBRAL_Z).sum()),
                      "n_atipicos_con_MAD_menor_0.25pp": int((fl["mad"] < 0.25).sum()),
                      "pct_atipicos": round(100 * len(fl) / evaluables, 3) if evaluables else np.nan,
                      "max_abs_z": round(float(d["z"].abs().max()), 2) if evaluables else np.nan,
                      "licencia_abierta": ABIERTA[fte]})
        if ABIERTA[fte] and len(fl):
            f2 = fl.assign(serie=s, fuente=fte, nivel=nivel)
            tops.append(f2[["fuente", "serie", "nivel", "territorio", "t", "yoy", "z", "mad"]])
    res = pd.DataFrame(filas)
    top = pd.concat(tops, ignore_index=True) if tops else pd.DataFrame()
    top["absz"] = top["z"].abs()
    # un municipio de una sola sección/distrito repite el mismo hecho en tres niveles: se deja el más agregado
    top["familia"] = top["serie"].str.replace(r"_(municipio|distrito|seccion)$", "", regex=True)
    top["muni"] = top["territorio"].astype(str).str[:5]
    top["rango_nivel"] = top["nivel"].map({"nacional": 0, "ccaa": 1, "provincia": 2, "municipio": 3,
                                           "distrito": 4, "seccion": 5}).fillna(9)
    top["zr"] = top["z"].round(0)
    top["yr"] = top["yoy"].round(1)
    top = top.sort_values("rango_nivel").drop_duplicates(["familia", "muni", "t", "yr", "zr"]).drop(
        columns=["familia", "muni", "rango_nivel", "zr", "yr"])
    top = top.sort_values(["absz", "serie", "territorio", "t"], ascending=[False, True, True, True])
    top20 = top.head(20).drop(columns="absz").round({"yoy": 2, "z": 2, "mad": 3})
    por_fuente = top.groupby("fuente").head(5).drop(columns="absz").round({"yoy": 2, "z": 2, "mad": 3})
    # diagnóstico: los atípicos municipales de SERPAVI, ¿tienen pocos contratos?
    diag = {}
    d = P["SERPAVI_VC_municipio"].dropna(subset=["yoy"]).reset_index(drop=True)
    d["z"], _ = z_series(d, "temporal")
    nm = R["AUX"]["serpavi_n_mun"]
    nm = nm[nm["desag"] == "tipologia=VC"][["territorio", "t", "valor"]].rename(columns={"valor": "n"})
    d = d.merge(nm, on=["territorio", "t"], how="left")
    ev = d[d["z"].notna()]
    fl = ev[ev["z"].abs() > UMBRAL_Z]
    diag["serpavi_vc_mun_mediana_n_contratos_atipicos"] = float(fl["n"].median()) if len(fl) else None
    diag["serpavi_vc_mun_mediana_n_contratos_resto"] = float(ev[ev["z"].abs() <= UMBRAL_Z]["n"].median())
    diag["serpavi_vc_mun_pct_atipicos_con_n_menor_30"] = round(100 * float((fl["n"] < 30).mean()), 1) if len(fl) else None
    diag["serpavi_vc_mun_pct_resto_con_n_menor_30"] = round(
        100 * float((ev[ev["z"].abs() <= UMBRAL_Z]["n"] < 30).mean()), 1)
    return res, pd.concat([top20.assign(lista="top20_global"), por_fuente.assign(lista="top5_por_fuente")],
                          ignore_index=True), diag


def unidades_dudosas(R: dict) -> dict:
    ser = R["AUX"]["serpavi_niveles"]
    out = {}
    for (tip, nivel), d in ser.items():
        if nivel in ("municipio", "provincia"):
            out[f"serpavi_{tip}_{nivel}_m2_menor_1_o_mayor_40"] = int(((d["valor"] < 1) | (d["valor"] > 40)).sum())
            out[f"serpavi_{tip}_{nivel}_m2_max"] = round(float(d["valor"].max()), 2)
    nm = R["AUX"]["serpavi_n_mun"]
    out["serpavi_n_contratos_municipio_igual_0"] = int((nm["valor"] == 0).sum())
    g = R["AUX"]["gva_raw"]
    out["gva_filas_total"] = int(len(g))
    out["gva_importe_nulo_o_no_positivo"] = int((g["importe"].isna() | (g["importe"] <= 0)).sum())
    out["gva_importe_mayor_10000"] = int((g["importe"] > 10000).sum())
    out["gva_importe_menor_100"] = int((g["importe"] < 100).sum())
    out["gva_importe_max"] = float(g["importe"].max())
    inc = R["AUX"]["incasol"]
    out["incasol_renta_media_ponderada_menor_100_o_mayor_5000"] = int(
        ((inc["valor"] < 100) | (inc["valor"] > 5000)).sum())
    out["incasol_municipio_anios_con_contratos_sin_renta"] = int(((inc["contratos"] > 0) & inc["valor"].isna()).sum())
    # etiquetas de base de los índices: el año cuya media anual provincial es la más cercana a 100
    ii = R["AUX"]["ipc_idx_prov_A"].groupby("t")["valor"].mean()
    out["ipc_indice_provincial_etiqueta_2021=100_media_2021"] = round(float(ii.loc[2021]), 2)
    out["ipc_indice_provincial_anio_mas_cercano_a_100"] = int((ii - 100).abs().idxmin())
    ip = R["AUX"]["ipva_idx_prov_panel"]
    out["ipva_indice_provincial_media_2015"] = round(float(ip[ip["t"] == 2015]["valor"].mean()), 3)
    return out


# ----------------------------------------------------------------------------- 2. coherencia
NIVELES = {
    "nacional": ["IPC_nacional", "SERPAVI_VC_nacional", "IPVA_EXIST_nacional", "IPVA_TOTAL_nacional",
                 "IPVA_NUEVO_nacional", "HICP_nacional"],
    "ccaa": ["IPC_ccaa", "SERPAVI_VC_ccaa", "IPVA_EXIST_ccaa", "IPVA_TOTAL_ccaa", "IPVA_NUEVO_ccaa", "INCASOL_ccaa"],
    "provincia": ["IPC_provincia", "SERPAVI_VC_provincia", "IPVA_EXIST_provincia", "IPVA_NUEVO_provincia",
                  "IPVA_PANEL_provincia", "GVA_provincia", "INCASOL_provincia"],
    "municipio": ["SERPAVI_VC_municipio", "IPVA_TAM_municipio", "GVA_municipio", "INCASOL_municipio",
                  "EMAL_municipio"],
    "distrito": ["SERPAVI_VC_distrito", "IPVA_TOTAL_distrito"],
}


def tipo_par(ta: str, tb: str) -> str:
    return f"{ta}-{tb}" if ta == tb else "nuevos-stock"


def flag_div(ya: pd.Series, yb: pd.Series) -> pd.Series:
    dif = (ya - yb).abs()
    return ((ya * yb < 0) & (dif > 1.0)) | (dif > 3.0)


def estadisticos_par(m: pd.DataFrame) -> dict:
    pa, pb = m["ya"], m["yb"]
    out = {"n_obs": len(m), "n_territorios": m["territorio"].nunique(), "n_periodos": m["t"].nunique(),
           "t_min": int(m["t"].min()), "t_max": int(m["t"].max())}
    out["corr_conjunta"] = round(float(pa.corr(pb)), 3) if len(m) >= 3 and pa.std() > 0 and pb.std() > 0 else np.nan
    ct = []
    for _, g in m.groupby("territorio"):
        if len(g) >= 5 and g["ya"].std() > 0 and g["yb"].std() > 0:
            ct.append(g["ya"].corr(g["yb"]))
    out["corr_temporal_media"] = round(float(np.mean(ct)), 3) if ct else np.nan
    out["n_terr_corr_temporal"] = len(ct)
    cx = []
    for _, g in m.groupby("t"):
        if len(g) >= 10 and g["ya"].std() > 0 and g["yb"].std() > 0:
            cx.append(g["ya"].corr(g["yb"]))
    out["corr_transversal_media"] = round(float(np.mean(cx)), 3) if cx else np.nan
    dif = pa - pb
    out["dif_media_pp"] = round(float(dif.mean()), 3)
    out["dif_mediana_pp"] = round(float(dif.median()), 3)
    out["dif_abs_media_pp"] = round(float(dif.abs().mean()), 3)
    out["pct_signo_opuesto"] = round(100 * float(((pa * pb) < 0).mean()), 1)
    out["pct_divergencia"] = round(100 * float(flag_div(pa, pb).mean()), 1)
    return out


def coherencia(R: dict) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    P, F, TIPO = R["P"], R["F"], R["TIPO"]
    filas, nacional, subn = [], [], []
    for nivel, series in NIVELES.items():
        disp = [s for s in series if s in P and not P[s].empty]
        for i, sa in enumerate(disp):
            for sb in disp[i + 1:]:
                a = P[sa][["territorio", "t", "yoy"]].rename(columns={"yoy": "ya"}).dropna()
                b = P[sb][["territorio", "t", "yoy"]].rename(columns={"yoy": "yb"}).dropna()
                m = a.merge(b, on=["territorio", "t"])
                if len(m) < 3:
                    continue
                restringido = not (ABIERTA[F[sa]] and ABIERTA[F[sb]])
                fila = {"nivel": nivel, "serie_a": sa, "serie_b": sb, "tipo_par": tipo_par(TIPO[sa], TIPO[sb]),
                        "restringido_licencia": restringido}
                fila.update(estadisticos_par(m))
                filas.append(fila)
                if restringido:
                    continue
                m = m.assign(par=f"{sa} vs {sb}", nivel=nivel, divergente=flag_div(m["ya"], m["yb"]))
                if nivel == "nacional":
                    nacional.append(m)
                else:
                    g = m.groupby(["par", "nivel", "t"]).agg(n_terr=("territorio", "size"),
                                                            pct_divergente=("divergente", "mean"),
                                                            dif_media_pp=("ya", "size")).reset_index()
                    g["dif_media_pp"] = m.groupby(["par", "nivel", "t"]).apply(
                        lambda x: float((x["ya"] - x["yb"]).mean()), include_groups=False).values
                    g["pct_divergente"] = (100 * g["pct_divergente"]).round(1)
                    subn.append(g)
    pares = pd.DataFrame(filas)
    nac = pd.concat(nacional, ignore_index=True) if nacional else pd.DataFrame()
    if not nac.empty:
        nac["dif_pp"] = (nac["ya"] - nac["yb"]).round(2)
        nac = nac[["par", "t", "ya", "yb", "dif_pp", "divergente"]].round({"ya": 2, "yb": 2})
    sub = pd.concat(subn, ignore_index=True) if subn else pd.DataFrame()
    if not sub.empty:
        sub["dif_media_pp"] = sub["dif_media_pp"].round(2)
    return pares, nac, sub


def ventanas(nac: pd.DataFrame) -> list[dict]:
    out = []
    for par, g in nac.groupby("par"):
        ts = sorted(g.loc[g["divergente"], "t"].tolist())
        if not ts:
            out.append({"par": par, "n_anios": int(g["t"].nunique()), "ventanas": []})
            continue
        vs, ini, prev = [], ts[0], ts[0]
        for t in ts[1:]:
            if t != prev + 1:
                vs.append(f"{ini}-{prev}" if ini != prev else str(ini))
                ini = t
            prev = t
        vs.append(f"{ini}-{prev}" if ini != prev else str(ini))
        out.append({"par": par, "n_anios": int(g["t"].nunique()), "ventanas": vs})
    return out
