"""V15 · Fase 1.2 · Auditoría de datos del grupo ALQUILER (capa C4, DESCRIPTIVO).

Sin efectos ni regresiones. Cruces territoriales solo por código INE. SEED=20261010 (el script no
usa aleatoriedad; la semilla se fija por regla del proyecto).
Lee data/base y data/raw (solo lectura); escribe en output/v15/auditoria/alquiler/.
Incasòl e Inside Airbnb (licencia no abierta): solo estadísticos resumen en las salidas.
"""
from __future__ import annotations

import hashlib
import json
import re
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
            f2["t"] = [f"{int(x) // 4}T{int(x) % 4 + 1}" if s.endswith("_trimestral") else str(int(x))
                       for x in f2["t"]]
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
    it = base("ipc_alquiler_indice", "provincia", "T")
    it["anio"] = it["periodo"].astype(str).str[:4].astype(int)
    ia = it.groupby(["territorio", "anio"])["valor"].agg(["mean", "size"]).reset_index()
    ia = ia[ia["size"] == 4].groupby("anio")["mean"].mean()
    out["ipc_indice_provincial_media_2025_trimestral"] = round(float(ia.loc[2025]), 2)
    out["ipc_indice_provincial_anio_con_media_mas_cercana_a_100_(trimestral)"] = int((ia - 100).abs().idxmin())
    nac = base("ipc_alquiler", "nacional", "T")
    na = annual_from_quarterly(nac, ["territorio"]).set_index("t")["valor"]
    out["ipc_nacional_indice_anio_con_media_mas_cercana_a_100"] = int((na - 100).abs().idxmin())
    out["ipc_nacional_media_2021"] = round(float(na.loc[2021]), 2)
    out["ipc_nacional_media_2025"] = round(float(na.loc[2025]), 2)
    ipv_terr = set(base("ipva_indice", "provincia", desag="")["territorio"].unique())
    out["ipva_provincias_ausentes_codigo_INE"] = sorted(f"{i:02d}" for i in range(1, 53) if f"{i:02d}" not in ipv_terr)
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


# ----------------------------------------------------------------------------- 2b. brecha nuevos - stock
def resumen_dif(m: pd.DataFrame) -> dict:
    d = m["ya"] - m["yb"]
    return {"n_terr": int(m["territorio"].nunique()), "n_obs": len(m), "media_pp": round(float(d.mean()), 2),
            "mediana_pp": round(float(d.median()), 2), "p10_pp": round(float(d.quantile(0.1)), 2),
            "p90_pp": round(float(d.quantile(0.9)), 2), "pct_positivo": round(100 * float((d > 0).mean()), 1)}


def brecha(R: dict) -> tuple[pd.DataFrame, pd.DataFrame]:
    P, F = R["P"], R["F"]
    pares = [
        ("IPVA nuevos - existentes", "IPVA_NUEVO_nacional", "IPVA_EXIST_nacional"),
        ("IPVA nuevos - existentes", "IPVA_NUEVO_ccaa", "IPVA_EXIST_ccaa"),
        ("IPVA nuevos - existentes", "IPVA_NUEVO_provincia", "IPVA_EXIST_provincia"),
        ("fianzas GVA - IPVA existentes", "GVA_provincia", "IPVA_EXIST_provincia"),
        ("fianzas GVA - SERPAVI VC", "GVA_provincia", "SERPAVI_VC_provincia"),
        ("fianzas GVA - SERPAVI VC", "GVA_municipio", "SERPAVI_VC_municipio"),
        ("fianzas GVA - IPVA total municipal", "GVA_municipio", "IPVA_TAM_municipio"),
        ("EMAL - SERPAVI VC", "EMAL_municipio", "SERPAVI_VC_municipio"),
        ("EMAL - IPVA total municipal", "EMAL_municipio", "IPVA_TAM_municipio"),
        ("Incasòl - SERPAVI VC", "INCASOL_municipio", "SERPAVI_VC_municipio"),
        ("Incasòl - SERPAVI VC", "INCASOL_provincia", "SERPAVI_VC_provincia"),
        ("Incasòl - IPC", "INCASOL_provincia", "IPC_provincia"),
        ("Incasòl - IPVA total municipal", "INCASOL_municipio", "IPVA_TAM_municipio"),
    ]
    filas = []
    for medida, sa, sb in pares:
        a = P[sa][["territorio", "t", "yoy"]].rename(columns={"yoy": "ya"}).dropna()
        b = P[sb][["territorio", "t", "yoy"]].rename(columns={"yoy": "yb"}).dropna()
        m = a.merge(b, on=["territorio", "t"])
        if m.empty:
            continue
        restr = not (ABIERTA[F[sa]] and ABIERTA[F[sb]])
        nivel = P[sa]["nivel"].iloc[0]
        if restr:
            for etq, sel in (("resumen_hasta_2019", m["t"] <= 2019), ("resumen_desde_2020", m["t"] >= 2020),
                             ("resumen_total", m["t"] > 0)):
                if sel.sum():
                    filas.append({"medida": medida, "nivel": nivel, "serie_a": sa, "serie_b": sb, "t": etq,
                                  **resumen_dif(m[sel]), "restringido_licencia": True})
        else:
            for t, g in m.groupby("t"):
                filas.append({"medida": medida, "nivel": nivel, "serie_a": sa, "serie_b": sb, "t": int(t),
                              **resumen_dif(g), "restringido_licencia": False})
    tab = pd.DataFrame(filas)
    # nivel: razón de índices IPVA nuevo/existente (base común 2015=100)
    ix = base("ipva_indice", "nacional")
    ix["t"] = ix["periodo"].astype(int)
    pv = ix.pivot_table(index="t", columns="desag", values="valor")
    razon = pd.DataFrame({"t": pv.index,
                          "indice_nuevo": pv["contrato=Nuevo contrato"].values,
                          "indice_existente": pv["contrato=Contrato existente"].values})
    razon["razon_nuevo_existente_x100"] = (100 * razon["indice_nuevo"] / razon["indice_existente"]).round(2)
    return tab, razon.round(2)


# ----------------------------------------------------------------------------- 3. rupturas y cambios de base
def sup_t(y: np.ndarray, anios: np.ndarray, recorte: float = 0.2) -> dict:
    n = len(y)
    mn = max(3, int(np.ceil(recorte * n)))
    mejor = (0.0, None, np.nan, np.nan)
    for k in range(mn, n - mn + 1):
        a, b = y[:k], y[k:]
        se = np.sqrt(a.var(ddof=1) / len(a) + b.var(ddof=1) / len(b))
        if se > 0:
            t = (b.mean() - a.mean()) / se
            if abs(t) > abs(mejor[0]):
                mejor = (t, int(anios[k]), a.mean(), b.mean())
    return {"n": n, "t_max_abs": round(abs(float(mejor[0])), 2), "primer_anio_tras_corte": mejor[1],
            "media_antes": round(float(mejor[2]), 2), "media_despues": round(float(mejor[3]), 2)}


def consistencia_indice_tasa(R: dict) -> pd.DataFrame:
    A = R["AUX"]
    filas = []

    def comp(nombre: str, rec: pd.DataFrame, pub: pd.DataFrame) -> None:
        m = rec[["territorio", "t", "yoy"]].merge(pub[["territorio", "t", "yoy"]], on=["territorio", "t"],
                                                  suffixes=("_recalc", "_pub"))
        d = (m["yoy_recalc"] - m["yoy_pub"]).abs()
        filas.append({"comparacion": nombre, "n": len(m), "dif_abs_media_pp": round(float(d.mean()), 4),
                      "dif_abs_max_pp": round(float(d.max()), 3),
                      "pct_dif_mayor_0.15pp": round(100 * float((d > 0.15).mean()), 2)})

    comp("IPC provincial anual: tasa recalculada del índice vs tasa publicada", A["ipc_idx_prov_yoy_recalc"],
         A["ipc_yoy_prov_pub"])
    it = base("ipc_alquiler_indice", "provincia", "T")
    it["t"] = t_index(it["periodo"])
    comp("IPC provincial trimestral (lag 4)", yoy(it, ["territorio"], lag=4), A["ipc_prov_T_pub"])
    for nivel in ("distrito", "municipio"):
        ix = base("ipva_tam_indice", nivel)
        ix["t"] = ix["periodo"].astype(int)
        pb = base("ipva_tam_var_anual", nivel)
        pb["t"] = pb["periodo"].astype(int)
        pb["yoy"] = pb["valor"]
        comp(f"IPVA tam. {nivel}: índice vs tasa publicada", yoy(ix, ["territorio"]), pb)
    ix = base("ipva_indice", "provincia", desag="contrato=Total")
    ix["t"] = ix["periodo"].astype(int)
    pb = base("ipva_var_anual", "provincia", desag="contrato=Total")
    pb["t"] = pb["periodo"].astype(int)
    pb["yoy"] = pb["valor"]
    comp("IPVA provincial (contrato=Total): índice vs tasa publicada", yoy(ix, ["territorio"]), pb)
    return pd.DataFrame(filas)


def rupturas_estadisticas(R: dict) -> pd.DataFrame:
    P = R["P"]
    series = {
        "IPC nacional (media anual)": P["IPC_nacional"].set_index("t")["yoy"],
        "HICP alquileres ES (media anual)": P["HICP_nacional"].set_index("t")["yoy"],
        "SERPAVI VC nacional (aprox.)": P["SERPAVI_VC_nacional"].set_index("t")["yoy"],
        "IPC provincial: media entre provincias": P["IPC_provincia"].groupby("t")["yoy"].mean(),
        "IPVA panel provincial: media entre provincias": P["IPVA_PANEL_provincia"].groupby("t")["yoy"].mean(),
        "SERPAVI VC provincial: mediana entre provincias": P["SERPAVI_VC_provincia"].groupby("t")["yoy"].median(),
        "SERPAVI VC municipal: mediana entre municipios": P["SERPAVI_VC_municipio"].groupby("t")["yoy"].median(),
    }
    filas = []
    for k, s in series.items():
        s = s.sort_index().dropna()
        if len(s) >= 8:
            filas.append({"serie": k, **sup_t(s.to_numpy(float), s.index.to_numpy())})
    return pd.DataFrame(filas)


def cobertura_ipva() -> pd.DataFrame:
    q = """select variable, nivel, desagregacion as desag, periodo, count(distinct territorio_codigo) as n_terr
           from h where variable in ('ipva_indice','ipva_var_anual','ipva_tam_indice','ipva_tam_var_anual')
           group by all order by 1,2,3,4"""
    d = CON.execute(q).fetchdf()
    return d.pivot_table(index=["variable", "nivel", "desag"], columns="periodo", values="n_terr").reset_index()


def serpavi_cobertura(R: dict) -> tuple[pd.DataFrame, dict]:
    ser, nmun = R["AUX"]["serpavi_niveles"], R["AUX"]["serpavi_n_mun"]
    filas = []
    diag = {}
    for tip in ("VC", "VU"):
        d = ser[(tip, "municipio")][["territorio", "t", "valor"]]
        n = nmun[nmun["desag"] == f"tipologia={tip}"][["territorio", "t", "valor"]].rename(columns={"valor": "n"})
        d = d.merge(n, on=["territorio", "t"], how="left")
        diag[f"serpavi_{tip}_pct_valores_con_n_contratos_cero_o_ausente"] = round(
            100 * float(((d["n"].fillna(0)) == 0).mean()), 2)
        diag[f"serpavi_{tip}_n_contratos_minimo_publicado_positivo"] = float(d.loc[d["n"] > 0, "n"].min())
        prev = d.assign(t=d["t"] + 1)[["territorio", "t", "valor", "n"]].rename(columns={"valor": "v_prev",
                                                                                          "n": "n_prev"})
        mm = d.merge(prev, on=["territorio", "t"], how="left")
        for t, g in mm.groupby("t"):
            ent = g[g["v_prev"].isna()]
            con = g[g["v_prev"].notna()]
            sal = d[d["t"] == t - 1]["territorio"].nunique() - len(con) if (t - 1) in set(d["t"]) else np.nan
            yoy_con = 100 * (con["valor"] / con["v_prev"] - 1)
            filas.append({"tipologia": tip, "t": int(t), "n_municipios": len(g), "entrantes": len(ent),
                          "salientes": sal if t > d["t"].min() else np.nan,
                          "mediana_n_contratos": float(g["n"].median()),
                          "n_municipios_n_ge_30": int((g["n"] >= 30).sum()),
                          "mediana_nivel_entrantes_sobre_continuos": (
                              round(float(ent["valor"].median() / con["valor"].median()), 3)
                              if len(ent) and len(con) else np.nan),
                          "tasa_mediana_municipios_continuos_pct": round(float(yoy_con.median()), 2) if len(con) else np.nan,
                          "tasa_mediana_nivel_todos_pct": np.nan})
    tab = pd.DataFrame(filas)
    # tasa de la mediana de niveles (todos los municipios con dato) frente a la de los continuos
    for tip in ("VC", "VU"):
        d = ser[(tip, "municipio")]
        med = d.groupby("t")["valor"].median()
        tasa = (100 * (med / med.shift(1) - 1)).round(2)
        sel = tab["tipologia"] == tip
        tab.loc[sel, "tasa_mediana_nivel_todos_pct"] = tab.loc[sel, "t"].map(tasa).values
    return tab, diag


def gva_cobertura(R: dict) -> tuple[pd.DataFrame, dict]:
    g = R["AUX"]["gva_raw"]
    ok = g[g["importe"] > 0]
    filas = []
    prev = set()
    for a, x in g.groupby("anio"):
        xo = ok[ok["anio"] == a]
        c = xo.groupby("territorio").size()
        muns = set(c.index)
        filas.append({"t": int(a), "filas": len(x), "importe_nulo_o_no_positivo": int(len(x) - len(xo)),
                      "n_municipios": len(muns), "n_municipios_ge10": int((c >= 10).sum()),
                      "n_municipios_ge30": int((c >= 30).sum()), "n_cp_distintos": int(x["cp"].nunique()),
                      "n_provincias": int(x["cod_provincia"].nunique()),
                      "entrantes": len(muns - prev) if prev else np.nan,
                      "salientes": len(prev - muns) if prev else np.nan,
                      "mediana_fianza": float(xo["importe"].median()),
                      "pct_devuelta_si": round(100 * float((x["devuelta"] == "SI").mean()), 1)})
        prev = muns
    tab = pd.DataFrame(filas)
    diag = {"gva_2026_filas_sobre_2025": round(float(tab.loc[tab.t == 2026, "filas"].iloc[0]
                                                      / tab.loc[tab.t == 2025, "filas"].iloc[0]), 3)}
    cs = ok[ok["anio"].between(2020, 2025)].groupby("territorio")["anio"].nunique()
    n10 = ok[ok["anio"].between(2020, 2025)].groupby(["territorio", "anio"]).size().unstack()
    diag["gva_municipios_panel_equilibrado_2020_2025_n_ge10"] = int((n10.fillna(0) >= 10).all(axis=1).sum())
    diag["gva_municipios_panel_equilibrado_2020_2025_n_ge30"] = int((n10.fillna(0) >= 30).all(axis=1).sum())
    diag["gva_municipios_con_dato_todos_los_anios_2020_2025"] = int((cs == 6).sum())
    # la base solo conserva València ciudad en municipio
    mb = CON.execute("select count(distinct territorio_codigo) from h where variable='fianzas_n' and "
                     "nivel='municipio'").fetchone()[0]
    diag["gva_municipios_en_base_hechos"] = int(mb)
    diag["gva_municipios_en_crudo_v9"] = int(g["territorio"].nunique())
    return tab, diag


def incasol_cobertura(R: dict) -> tuple[pd.DataFrame, dict]:
    inc = R["AUX"]["incasol"]
    filas = []
    for t, x in inc.groupby("t"):
        filas.append({"t": int(t), "n_municipios_con_contratos": int((x["contratos"] > 0).sum()),
                      "n_municipios_ge10": int((x["contratos"] >= 10).sum()),
                      "n_municipios_ge30": int((x["contratos"] >= 30).sum()),
                      "n_municipios_renta_cobertura_ge90": int(((x["cobertura_renta"] >= 0.9)
                                                                & (x["contratos"] >= 10)).sum())})
    tab = pd.DataFrame(filas)
    esq = CON.execute("""select cast(left(periodo,4) as int) as t, count(distinct desagregacion) as n_tramos,
                          string_agg(distinct desagregacion, ' | ') as tramos
                          from h where variable='incasol_contratos' and frecuencia='A' group by 1 order by 1"""
                      ).fetchdf()
    esq["esquema_tramos"] = np.where(esq["tramos"].str.contains("450"), "nuevo (>350-450, >450-600, >600)",
                                     "antiguo (>350-500, >500-650, >650)")
    tab = tab.merge(esq[["t", "n_tramos", "esquema_tramos"]], on="t", how="left")
    diag = {}
    sub = inc[inc["t"].between(2019, 2025)]
    n10 = sub.pivot_table(index="territorio", columns="t", values="contratos")
    diag["incasol_municipios_panel_equilibrado_2019_2025_n_ge10"] = int((n10.fillna(0) >= 10).all(axis=1).sum())
    diag["incasol_municipios_panel_equilibrado_2019_2025_n_ge30"] = int((n10.fillna(0) >= 30).all(axis=1).sum())
    ant = esq[esq["esquema_tramos"].str.startswith("antiguo")]["t"]
    nue = esq[esq["esquema_tramos"].str.startswith("nuevo")]["t"]
    diag["incasol_anios_esquema_antiguo"] = f"{int(ant.min())}-{int(ant.max())}" if len(ant) else None
    diag["incasol_anios_esquema_nuevo"] = f"{int(nue.min())}-{int(nue.max())}" if len(nue) else None
    return tab, diag


# ----------------------------------------------------------------------------- 4. revisiones entre vintages
def fila_rev(comparacion: str, fuente: str, a: str, b: str, x: pd.Series, y: pd.Series, unidad: str,
             nota: str = "", restringido: bool = False) -> dict:
    d = (x - y).dropna()
    return {"comparacion": comparacion, "fuente": fuente, "vintage_a": a, "vintage_b": b, "n_comparados": len(d),
            "revision_media_abs": round(float(d.abs().mean()), 4) if len(d) else np.nan,
            "revision_media": round(float(d.mean()), 4) if len(d) else np.nan,
            "revision_max_abs": round(float(d.abs().max()), 4) if len(d) else np.nan,
            "unidad": unidad, "nota": nota, "restringido_licencia": restringido}


def cruza(a: pd.DataFrame, b: pd.DataFrame, claves: list[str]) -> tuple[pd.Series, pd.Series]:
    m = a[claves + ["valor"]].merge(b[claves + ["valor"]], on=claves, suffixes=("_a", "_b"))
    return m["valor_a"], m["valor_b"]


def sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def revisiones(R: dict) -> pd.DataFrame:
    f = []
    # IPVA: panel del proyecto vs IPVA 2024 publicado (índice provincial, 2021-2024)
    pn = base("ipva_indice", "provincia", desag="", edicion_like="panel%")
    pb = base("ipva_indice", "provincia", desag="contrato=Total", edicion_like="IPVA 2024%")
    x, y = cruza(pn, pb, ["territorio", "periodo"])
    f.append(fila_rev("IPVA índice provincial: panel v1-v8 vs IPVA 2024 (descarga 2026-10-14)", "IPVA",
                      "panel procesado (descargas hasta 2026-10-10)", "IPVA 2024 publicado 2026-05", x, y,
                      "puntos de índice (2015=100)"))
    # IPVA distrito: csv 59061 (14-oct) vs API tempus 59061 (15-oct)
    a = base("ipva_indice", "distrito")
    b = base("ipva_tam_indice", "distrito")
    x, y = cruza(a, b, ["territorio", "periodo"])
    f.append(fila_rev("IPVA índice distrital: csv 59061 vs API tempus 59061", "IPVA", "csv INE (2026-10-14)",
                      "API tempus (2026-10-15)", x, y, "puntos de índice (2015=100)"))
    a = base("ipva_var_anual", "distrito")
    b = base("ipva_tam_var_anual", "distrito")
    x, y = cruza(a, b, ["territorio", "periodo"])
    f.append(fila_rev("IPVA tasa distrital: csv 59061 vs API tempus 59061", "IPVA", "csv INE (2026-10-14)",
                      "API tempus (2026-10-15)", x, y, "pp"))
    a = base("ipva", "municipio")
    b = base("ipva_tam_indice", "municipio")
    x, y = cruza(a, b, ["territorio", "periodo"])
    f.append(fila_rev("IPVA índice municipal: serie 59060 (v1-v8) vs API tempus 59060", "IPVA",
                      "ine_ipva_municipal.csv (2026-10-09)", "API tempus (2026-10-15)", x, y,
                      "puntos de índice", "solo 1 municipio solapa (46250)"))
    # SERPAVI: tablas procesadas del proyecto frente a la serie municipal/provincial/distrital
    a = base("serpavi_vc_alq_m2_mediana", "provincia")
    b = base("serpavi_alquiler_m2_mediana", "provincia", desag="tipologia=VC")
    x, y = cruza(a, b, ["territorio", "periodo"])
    f.append(fila_rev("SERPAVI provincial: pdf/serpavi_provincias.csv vs serie municipal-provincial base", "SERPAVI",
                      "serpavi_provincias.csv", "xlsx provincial/municipal", x, y, "€/m²/mes", "3 provincias CV"))
    a = base("serpavi_vc_mediana", "municipio")
    b = base("serpavi_alquiler_m2_mediana", "municipio", desag="tipologia=VC")
    x, y = cruza(a, b, ["territorio", "periodo"])
    f.append(fila_rev("SERPAVI municipal 46250: tabla del proyecto vs serie base", "SERPAVI", "tabla XLSX",
                      "serie base", x, y, "€/m²/mes", "1 municipio"))
    a = base("serpavi_dist_vc_mediana", "distrito")
    b = base("serpavi_alquiler_m2_mediana", "distrito", desag="tipologia=VC")
    x, y = cruza(a, b, ["territorio", "periodo"])
    f.append(fila_rev("SERPAVI distritos de València: tabla del proyecto vs serie base", "SERPAVI", "tabla distritos",
                      "serie base", x, y, "€/m²/mes", "19 distritos"))
    # SERPAVI crudo (pdf/serpavi_v2_municipios.csv) frente a la base municipal
    raw = pd.read_csv(RAIZ / "data" / "raw" / "pdf" / "serpavi_v2_municipios.csv", dtype={"codigo": str})
    raw = raw[(raw["variable"] == "alquiler_m2") & (raw["estadistico"] == "mediana")].copy()
    raw["territorio"] = raw["codigo"].str.zfill(5)
    raw["periodo"] = raw["periodo"].astype(str)
    for tip in ("VC", "VU"):
        a = raw[raw["tipologia"] == tip]
        b = base("serpavi_alquiler_m2_mediana", "municipio", desag=f"tipologia={tip}")
        b["periodo"] = b["periodo"].astype(str)
        x, y = cruza(a, b, ["territorio", "periodo"])
        f.append(fila_rev(f"SERPAVI municipal {tip}: crudo serpavi_v2_municipios.csv vs base", "SERPAVI",
                          "crudo data/raw/pdf (2026-10-10)", "base", x, y, "€/m²/mes"))
    # IPC: tabla 76137 (ine_ipc_alquiler.csv) vs tabla 76142 (ECOICOP v2) para los mismos códigos de serie
    r1 = pd.read_csv(RAIZ / "data" / "raw" / "ine_ipc_alquiler.csv")
    r1 = r1[r1["unidad"] == "Variación anual"][["serie", "periodo", "valor"]]
    r2 = pd.read_csv(RAIZ / "data" / "raw" / "ine_v2_ipc_alquiler_prov.csv")
    r2 = r2[r2["medida"].str.contains("variacion_anual")][["serie", "periodo", "valor"]]
    x, y = cruza(r1, r2, ["serie", "periodo"])
    f.append(fila_rev("IPC alquiler tasa anual: tabla 76137 vs tabla 76142 (mismos códigos de serie)", "IPC",
                      "ine_ipc_alquiler.csv (2026-10-09)", "ine_v2_ipc_alquiler_prov.csv (2026-10-10)", x, y, "pp",
                      f"series solapadas: {r1['serie'].nunique()} vs {r2['serie'].nunique()}"))
    # GVA: v5 vs v9 (hash)
    iguales, tot = 0, 0
    for a_ in range(2020, 2027):
        p5 = RAIZ / "data" / "raw" / "v5" / f"gva_fianzas_{a_}.csv"
        p9 = RAIZ / "data" / "raw" / "v9" / "gva_fianzas" / f"gva_fianzas_{a_}.csv"
        if p5.exists() and p9.exists():
            tot += 1
            iguales += int(sha(p5) == sha(p9))
    f.append({"comparacion": "GVA fianzas: descarga v5 vs v9", "fuente": "GVA", "vintage_a": "data/raw/v5",
              "vintage_b": "data/raw/v9 (2026-10-14)", "n_comparados": tot, "revision_media_abs": 0.0 if iguales == tot else np.nan,
              "revision_media": 0.0 if iguales == tot else np.nan, "revision_max_abs": 0.0 if iguales == tot else np.nan,
              "unidad": "ficheros anuales idénticos (SHA-256)", "nota": f"{iguales}/{tot} idénticos",
              "restringido_licencia": False})
    # base frente al crudo (GVA): mediana de fianza por provincia y año
    g = R["AUX"]["gva_raw"]
    ok = g[g["importe"] > 0]
    pr = ok.assign(territorio=ok["cod_provincia"].str.zfill(2), periodo=ok["anio"].astype(str)).groupby(
        ["territorio", "periodo"])["importe"].median().rename("valor").reset_index()
    bb = base("fianzas_importe_mediana", "provincia")
    bb["periodo"] = bb["periodo"].astype(str)
    x, y = cruza(pr, bb, ["territorio", "periodo"])
    f.append(fila_rev("GVA mediana provincial: recalculada del crudo vs base hechos", "GVA", "crudo v9", "base", x, y,
                      "euros", "derivación reproducible si es 0"))
    # Incasòl: v3 (2026-10-10) vs v9 (2026-10-14), contratos anuales totales por municipio
    v3 = pd.read_csv(RAIZ / "data" / "raw" / "v3" / "incasol_fianzas_municipio_v3.csv.gz")
    v3 = v3[v3["serie"].str.contains("n_contratos_TOTAL_bandas") & v3["periodo"].str.endswith("gener-desembre")].copy()
    v3["territorio"] = v3["codigo"].astype(int).astype(str).str.zfill(5)
    v3["periodo"] = v3["periodo"].str[:4]
    v9 = pd.read_csv(RAIZ / "data" / "raw" / "v9" / "incasol" / "incasol_qww9-bvhh_actual.csv.gz")
    v9 = v9[v9["periode"] == "gener-desembre"].copy()
    v9["territorio"] = v9["codi_territorial"].astype(int).astype(str).str.zfill(5)
    v9["periodo"] = v9["any"].astype(str)
    s9 = v9.groupby(["territorio", "periodo"])["habitatges"].sum().rename("valor").reset_index()
    s3 = v3.groupby(["territorio", "periodo"])["valor"].sum().reset_index()
    x, y = cruza(s3, s9, ["territorio", "periodo"])
    r = fila_rev("Incasòl contratos anuales por municipio: v3 vs v9", "INCASOL", "v3 (2026-10-10)",
                 "v9 (2026-10-14)", x, y, "contratos", restringido=True)
    r["nota"] = (f"claves solo en v3: {len(set(map(tuple, s3[['territorio', 'periodo']].values)) - set(map(tuple, s9[['territorio', 'periodo']].values)))}; "
                 f"solo en v9: {len(set(map(tuple, s9[['territorio', 'periodo']].values)) - set(map(tuple, s3[['territorio', 'periodo']].values)))}")
    f.append(r)
    return pd.DataFrame(f)


# ----------------------------------------------------------------------------- 5. Inside Airbnb (solo resumen)
def airbnb_resumen() -> dict:
    d = CON.execute("""select territorio_codigo, valor from h where variable='iab_n_anuncios'""").fetchdf()
    pos = d[d["valor"] > 0]["valor"]
    z = rz(pos)
    barrio = pd.read_csv(RAIZ / "data" / "raw" / "v9" / "insideairbnb" / "insideairbnb_barrio.csv.gz")
    per = CON.execute("select min(periodo), max(periodo), count(distinct periodo) from h where "
                      "variable='iab_n_anuncios'").fetchone()
    return {"secciones_con_dato": int(d["territorio_codigo"].nunique()), "secciones_con_anuncios": int(len(pos)),
            "anuncios_total_secciones": int(d["valor"].sum()),
            "ciudades_en_fichero_de_barrios": sorted(barrio["ciudad"].unique().tolist()),
            "atipicos_transversales_z_gt_5_n": int((z.abs() > UMBRAL_Z).sum()),
            "periodos_distintos": int(per[2]), "periodo_min": str(per[0]), "periodo_max": str(per[1]),
            "nota": "instantánea única (no hay serie temporal): sin tasas interanuales ni coherencia temporal"}


# ----------------------------------------------------------------------------- 5b. cobertura consolidada
def cobertura_consolidada(R: dict, gva: pd.DataFrame, inc: pd.DataFrame, ser: pd.DataFrame) -> pd.DataFrame:
    filas = []
    for _, r in ser.iterrows():
        filas.append({"fuente": f"SERPAVI_{r['tipologia']}", "tipo": "stock", "t": int(r["t"]),
                      "n_municipios": int(r["n_municipios"]), "n_municipios_ge10": int(r["n_municipios"]),
                      "n_municipios_ge30": int(r["n_municipios_n_ge_30"]),
                      "nota": "umbral de publicación n>=10 contratos"})
    for _, r in gva.iterrows():
        filas.append({"fuente": "GVA_fianzas", "tipo": "nuevos", "t": int(r["t"]),
                      "n_municipios": int(r["n_municipios"]), "n_municipios_ge10": int(r["n_municipios_ge10"]),
                      "n_municipios_ge30": int(r["n_municipios_ge30"]),
                      "nota": "2026 parcial" if r["t"] == 2026 else "crudo v9; la base solo trae València ciudad"})
    for _, r in inc.iterrows():
        filas.append({"fuente": "Incasol_fianzas", "tipo": "nuevos", "t": int(r["t"]),
                      "n_municipios": int(r["n_municipios_con_contratos"]),
                      "n_municipios_ge10": int(r["n_municipios_ge10"]), "n_municipios_ge30": int(r["n_municipios_ge30"]),
                      "nota": "licencia no abierta: solo recuento de municipios"})
    ip = CON.execute("""select cast(periodo as int) t, count(distinct territorio_codigo) n from h
                        where variable='ipva_tam_indice' and nivel='municipio' group by 1 order by 1""").fetchdf()
    for _, r in ip.iterrows():
        filas.append({"fuente": "IPVA_total_municipal", "tipo": "stock", "t": int(r["t"]), "n_municipios": int(r["n"]),
                      "n_municipios_ge10": np.nan, "n_municipios_ge30": np.nan,
                      "nota": "índice total sin desglose nuevo/existente"})
    em = CON.execute("""select cast(left(periodo,4) as int) t, count(distinct territorio_codigo) n from h
                        where variable='emal_renta_mensual_eur' and nivel='municipio' group by 1 order by 1""").fetchdf()
    for _, r in em.iterrows():
        filas.append({"fuente": "EMAL_Euskadi", "tipo": "nuevos", "t": int(r["t"]), "n_municipios": int(r["n"]),
                      "n_municipios_ge10": np.nan, "n_municipios_ge30": np.nan, "nota": "municipios >20.000 hab."})
    return pd.DataFrame(filas)


def ultimo_periodo() -> pd.DataFrame:
    q = """select variable, nivel, frecuencia, min(periodo) as primer_periodo, max(periodo) as ultimo_periodo,
           count(distinct territorio_codigo) as n_territorios
           from h where variable in ('ipc_alquiler_yoy','ipc_alquiler_indice','ipc_alquiler','ipva_indice',
           'ipva_var_anual','ipva_tam_indice','serpavi_alquiler_m2_mediana','serpavi_n_contratos_recuento',
           'fianzas_importe_mediana','incasol_contratos','incasol_renta_media','emal_renta_mensual_eur',
           'hicp_alquiler_indice','monitor_ipc_alquiler','monitor_fianzas_gva')
           group by all order by 1,2,3"""
    return CON.execute(q).fetchdf()


def potencia_p5_p6(R: dict) -> dict:
    """Municipios con >=10 contratos nuevos antes y después de 2024 (condiciona P5/P6); solo recuentos."""
    out = {}
    g = R["AUX"]["gva_mun_nivel"]
    pv = g.pivot_table(index="territorio", columns="t", values="n")
    out["gva_municipios_n_ge10_en_2023_y_2025"] = int(((pv[2023] >= 10) & (pv[2025] >= 10)).sum())
    out["gva_municipios_n_ge10_en_2021_2022_2023_2024_2025"] = int((pv[[2021, 2022, 2023, 2024, 2025]] >= 10).all(axis=1).sum())
    inc = R["AUX"]["incasol"].pivot_table(index="territorio", columns="t", values="contratos")
    out["incasol_municipios_n_ge10_en_2023_y_2025"] = int(((inc[2023] >= 10) & (inc[2025] >= 10)).sum())
    out["incasol_municipios_n_ge30_en_2023_y_2025"] = int(((inc[2023] >= 30) & (inc[2025] >= 30)).sum())
    # provincias de Cataluña y CV: clústeres provinciales disponibles
    out["provincias_con_fianzas_nuevos_contratos"] = {"GVA": 3, "Incasol": 4, "EMAL (municipios)": 20}
    return out


# ----------------------------------------------------------------------------- salida
def escribir(df: pd.DataFrame, nombre: str) -> str:
    OUT.mkdir(parents=True, exist_ok=True)
    df.to_csv(OUT / nombre, index=False, encoding="utf-8")
    return nombre


def fila_par(pares: pd.DataFrame, nivel: str, a: str, b: str) -> dict:
    x = pares[(pares["nivel"] == nivel) & (((pares["serie_a"] == a) & (pares["serie_b"] == b))
                                           | ((pares["serie_a"] == b) & (pares["serie_b"] == a)))]
    if x.empty:
        return {}
    r = x.iloc[0].to_dict()
    if r["serie_a"] != a:  # invierte el signo de la diferencia para respetar el orden pedido
        r["dif_media_pp"], r["dif_mediana_pp"] = -r["dif_media_pp"], -r["dif_mediana_pp"]
        r["serie_a"], r["serie_b"] = a, b
    return {k: (None if isinstance(v, float) and np.isnan(v) else v) for k, v in r.items()
            if k in ("n_obs", "n_territorios", "n_periodos", "t_min", "t_max", "corr_conjunta",
                     "corr_temporal_media", "corr_transversal_media", "dif_media_pp", "dif_abs_media_pp",
                     "pct_signo_opuesto", "pct_divergencia")}


def informe_md(o: dict) -> str:
    pf = o["por_fuente"].set_index("fuente")
    r = o["resultado"]["diagnosticos"]
    cl = r["coherencia_pares_clave"]
    tb = o["tab_b"]
    rz_ = o["razon"].set_index("t")["razon_nuevo_existente_x100"]
    nac = tb[(tb["serie_a"] == "IPVA_NUEVO_nacional")].set_index("t")["media_pp"]
    gs = tb[(tb["serie_a"] == "GVA_municipio") & (tb["serie_b"] == "SERPAVI_VC_municipio")].set_index("t")["media_pp"]
    sc = o["ser_c"][o["ser_c"]["tipologia"] == "VC"].set_index("t")
    gv = o["gva_c"].set_index("t")
    pot = o["pot"]
    u = o["dud"]
    rev = o["rev"]
    ven = {v["par"]: v["ventanas"] for v in o["vent"]}
    d = lambda k, c: cl[k][c]  # noqa: E731
    return f"""# Auditoría de datos · grupo ALQUILER (V15, fase 1.2, capa C4, DESCRIPTIVO)

Script: `src/v15/auditoria/alquiler.py` (SEED=20261010). Tablas CSV y `resultado.json` en esta carpeta. Sin efectos estimados. Cruces solo por código INE. Incasòl e Inside Airbnb: solo estadísticos resumen y recuentos.

## Hallazgos

1. **Atípicos (|z robusto|>5 sobre tasas interanuales).** SERPAVI concentra casi todos ({int(pf.loc['SERPAVI','n_atipicos'])} de {int(pf.loc['SERPAVI','n_evaluables'])} evaluables, sobre todo en sección y distrito); el 48,5 % de los municipales tiene n<30 contratos (17,9 % en el resto). Con escala mínima de 1 pp quedan {int(pf.loc['SERPAVI','n_atipicos_escala_min_1pp'])}: muchos son MAD casi nulo (p. ej. municipio 10019, MAD 0,001 pp), no errores. IPVA {int(pf.loc['IPVA','n_atipicos'])} (tasas redondeadas a 0,1 pp con MAD de 0,2 pp, sobre todo municipales), IPC {int(pf.loc['IPC','n_atipicos'])} (entre los mayores, Ceuta, Melilla y Lugo), GVA {int(pf.loc['GVA','n_atipicos'])} (tasas de la mediana de fianza municipal, evaluación transversal), EMAL {int(pf.loc['EMAL','n_atipicos'])}. Los 20 mayores están en `atipicos_top20_y_top5_por_fuente.csv`.
2. **Unidad dudosa en el catálogo.** `ipc_alquiler_indice` se rotula «2021=100», pero la media provincial de 2021 es {u['ipc_indice_provincial_etiqueta_2021=100_media_2021']} y la de 2025 es {u['ipc_indice_provincial_media_2025_trimestral']}: la base efectiva es 2025=100 (nacional: 2021 = {u['ipc_nacional_media_2021']}, 2025 = {u['ipc_nacional_media_2025']}). Las tasas no se ven afectadas; los niveles sí. A corregir en `variables.parquet`, no aquí.
3. **Stock frente a stock.** IPC y HICP de alquileres efectivos coinciden a escala nacional (corr. {d('IPC_vs_HICP_nacional','corr_conjunta')}, dif. media {d('IPC_vs_HICP_nacional','dif_media_pp')} pp). IPC e IPVA existentes: corr. {d('IPC_vs_IPVA_existentes_nacional','corr_conjunta')} nacional (4 años) pero solo {d('IPC_vs_IPVA_existentes_provincia','corr_transversal_media')} transversal provincial. SERPAVI frente al IPVA total: {d('SERPAVI_vs_IPVA_panel_provincia','corr_conjunta')} provincial (13 años), {d('SERPAVI_vs_IPVA_total_distrito','corr_conjunta')} distrital, {d('SERPAVI_vs_IPVA_total_municipio','corr_conjunta')} municipal. SERPAVI crece de media {d('IPC_vs_SERPAVI_nacional','dif_media_pp')*-1:.1f} pp más que el IPC y diverge del IPC en {', '.join(ven['IPC_nacional vs SERPAVI_VC_nacional'])} (signo opuesto o >3 pp).
4. **Contratos nuevos frente a stock.** El IPVA «nuevo contrato» supera al «existente» en {nac.loc[2021]:.1f}, {nac.loc[2022]:.1f}, {nac.loc[2023]:.1f} y {nac.loc[2024]:.1f} pp (2021-2024; mediana provincial 3,2/3,2/1,3/5,2). La razón de índices nuevo/existente (2015=100) pasa de {rz_.loc[2021]} a {rz_.loc[2024]}. Fianzas GVA menos SERPAVI (municipal, media): {gs.loc[2021]:.1f}, {gs.loc[2022]:.1f}, {gs.loc[2023]:.1f}, {gs.loc[2024]:.1f} pp. Solo hay 4 tasas con desglose por tipo de contrato: la evolución de la brecha es sugerente, no concluyente.
5. **Las series municipales de contratos nuevos concuerdan poco con el stock.** Correlación conjunta de tasas: GVA-SERPAVI {d('GVA_vs_SERPAVI_municipio','corr_conjunta')}, Incasòl-SERPAVI {d('Incasol_vs_SERPAVI_municipio_(resumen)','corr_conjunta')} (resumen), diferencia absoluta media 7,4 y 7,3 pp. Mezclan ruido de muestra (n pequeño, fianza redondeada, fianza ≠ renta) con diferencias genuinas. Provincial, GVA-IPVA nuevos {d('GVA_vs_IPVA_nuevos_provincia','corr_conjunta')} (3 provincias) e Incasòl-IPVA nuevos {d('Incasol_vs_IPVA_nuevos_provincia_(resumen)','corr_conjunta')} (4): sin acuerdo medible.
6. **Rupturas y cambios de base.** El IPVA con desglose por contrato empieza en 2021; el panel total, en 2011. Cubre 48 provincias (faltan 01, 20, 31 y 48, los territorios forales; causa probable datos de la AEAT, no verificada), municipios 702→716 (+11 en 2024) y distritos 349→378. La tasa publicada y la recalculada del índice coinciden (dif. media 0,01-0,03 pp). SERPAVI sin tasa VC para 01 y 48; publica solo con n≥10; los municipios pasan de {int(sc.loc[2011,'n_municipios'])} (2011) a {int(sc.loc[2024,'n_municipios'])} (2024) y los entrantes tienen niveles 0,75-0,88 veces los de los continuos (1,35 en 2022, 1,15 en 2024): la tasa de la mediana de niveles difiere de la de municipios continuos hasta 1,8 pp ({sc.loc[2022,'tasa_mediana_nivel_todos_pct']} frente a {sc.loc[2022,'tasa_mediana_municipios_continuos_pct']} en 2022). Incasòl cambió los tramos en 2021 (2007-2020 frente a 2021-2025); se usó la renta ponderada de todos los tramos, que no depende del esquema. El contraste de cambio de media (sin p-valor) apunta a 2009 en IPC (4,3 a 1,0 %) y a 2015-2016 en SERPAVI e IPVA (de negativo a positivo): son fases del ciclo, no pruebas de ruptura.
7. **Fianzas GVA.** La base de hechos conserva solo València ciudad (1 municipio); el crudo trae {r['gva_cobertura']['gva_municipios_en_crudo_v9']}. Municipios con dato: {int(gv.loc[2020,'n_municipios'])} (2020) a {int(gv.loc[2025,'n_municipios'])} (2025); con ≥10 contratos, {int(gv.loc[2020,'n_municipios_ge10'])} a {int(gv.loc[2025,'n_municipios_ge10'])}. 2026 es parcial ({r['gva_cobertura']['gva_2026_filas_sobre_2025']} de las filas de 2025) y el indicador «devuelta» cae de 74,7 % (2020) a 5,7 % (2026), compatible con censura por antigüedad: no sirve como resultado.
8. **Revisiones.** Las {len(rev)} comparaciones entre descargas dan revisión media absoluta 0 (GVA v5 = v9 byte a byte; descargas del 9 al 15-10-2026 para IPVA, SERPAVI e IPC). Son el mismo lote: la revisión real queda sin medir hasta la próxima edición.
9. **Cobertura para P5 y P6.** Municipios con ≥10 contratos nuevos en 2023 y 2025: GVA {pot['gva_municipios_n_ge10_en_2023_y_2025']}, Incasòl {pot['incasol_municipios_n_ge10_en_2023_y_2025']} (≥30: {pot['incasol_municipios_n_ge30_en_2023_y_2025']}). Clústeres provinciales: 3 (GVA) y 4 (Incasòl). SERPAVI e IPVA terminan en 2024: no cubren 2025-2026. Solo IPC (a 2026T2, provincial), Incasòl (a 2026T1), GVA (2026 parcial) y EMAL (20 municipios, a 2025T4) llegan al periodo de P6. Inside Airbnb es una instantánea (2026-09): sin tasas.

## Medida recomendada (a confirmar con la potencia de la fase 1.3)

| Pregunta | Principal | Robustez |
|---|---|---|
| P2 fundamentales (panel largo) | IPC provincial (stock, 2002-2026T2, 52 provincias) para dinámica; SERPAVI €/m² (VC) para niveles | IPVA panel provincial total (2011-2024); HICP a escala nacional |
| P5 pisos turísticos (barrio, CV, València) | SERPAVI VC en sección y distrito (stock, a 2024) | IPVA distrital (corr. con SERPAVI {d('SERPAVI_vs_IPVA_total_distrito','corr_conjunta')}); fianzas GVA y Incasòl a nivel municipal (contratos nuevos); Inside Airbnb solo como covariable |
| P6 topes y zonas tensionadas 2024-2026 | Contratos nuevos: Incasòl (renta ponderada, municipios con n mínimo) y fianzas GVA del crudo, comparando dentro de cada fuente | IPC provincial (stock, hasta 2026T2); EMAL; IPVA nuevo contrato hasta 2024 (solo preperiodo) |

Fuera del cruce (sin código INE): barrios de Inside Airbnb y la tabla de alquiler por CP de la Comunidad de Madrid (origen no verificado).

Reglas: no mezclar niveles de fuentes distintas; tasas con n mínimo (≥10 contratos en t y t-1); excluir 2026 parcial; declarar siempre si la medida es stock o contratos nuevos.
"""


def main() -> dict:
    OUT.mkdir(parents=True, exist_ok=True)
    R = construir()
    P = R["P"]
    ficheros = []
    # 1. atípicos
    res, top, diag_at = atipicos(R)
    ficheros.append(escribir(res, "atipicos_resumen_por_serie.csv"))
    por_fuente = res.groupby("fuente").agg(series=("serie", "size"), n_obs=("n_obs", "sum"),
                                           n_evaluables=("n_evaluables", "sum"), n_atipicos=("n_atipicos", "sum"),
                                           n_atipicos_escala_min_1pp=("n_atipicos_escala_min_1pp", "sum")).reset_index()
    por_fuente["licencia_abierta"] = por_fuente["fuente"].map(ABIERTA)
    ficheros.append(escribir(por_fuente, "atipicos_recuento_por_fuente.csv"))
    ficheros.append(escribir(top, "atipicos_top20_y_top5_por_fuente.csv"))
    dud = unidades_dudosas(R)
    sp = P["SERPAVI_VC_provincia"]["territorio"].unique()
    dud["serpavi_provincias_sin_tasa_VC"] = sorted(f"{i:02d}" for i in range(1, 53) if f"{i:02d}" not in set(sp))
    # 2. coherencia
    pares, nac, sub = coherencia(R)
    ficheros.append(escribir(pares, "coherencia_pares_resumen.csv"))
    ficheros.append(escribir(nac, "coherencia_nacional_anual.csv"))
    ficheros.append(escribir(sub, "coherencia_divergencia_subnacional_anual.csv"))
    vent = ventanas(nac)
    tab_b, razon = brecha(R)
    ficheros.append(escribir(tab_b, "brecha_nuevos_stock.csv"))
    ficheros.append(escribir(razon, "brecha_nivel_ipva_nuevo_existente.csv"))
    # 3. rupturas
    cons = consistencia_indice_tasa(R)
    ficheros.append(escribir(cons, "rupturas_consistencia_indice_tasa.csv"))
    rs = rupturas_estadisticas(R)
    ficheros.append(escribir(rs, "rupturas_cambio_de_media_descriptivo.csv"))
    ficheros.append(escribir(cobertura_ipva(), "rupturas_ipva_cobertura_territorial.csv"))
    ser_c, diag_ser = serpavi_cobertura(R)
    ficheros.append(escribir(ser_c, "rupturas_serpavi_cobertura_y_composicion.csv"))
    gva_c, diag_gva = gva_cobertura(R)
    ficheros.append(escribir(gva_c, "rupturas_fianzas_gva_cobertura.csv"))
    inc_c, diag_inc = incasol_cobertura(R)
    ficheros.append(escribir(inc_c, "rupturas_incasol_cobertura_solo_recuentos.csv"))
    # 4. revisiones
    rev = revisiones(R)
    ficheros.append(escribir(rev, "revisiones_vintages.csv"))
    # 5. cobertura
    cob = cobertura_consolidada(R, gva_c, inc_c, ser_c)
    ficheros.append(escribir(cob, "cobertura_municipal_anual_por_fuente.csv"))
    ficheros.append(escribir(ultimo_periodo(), "cobertura_temporal_variables.csv"))
    pot = potencia_p5_p6(R)
    iab = airbnb_resumen()
    # resultado
    ks = lambda a, b, n: fila_par(pares, n, a, b)  # noqa: E731
    clave = {
        "IPC_vs_HICP_nacional": ks("IPC_nacional", "HICP_nacional", "nacional"),
        "IPC_vs_SERPAVI_nacional": ks("IPC_nacional", "SERPAVI_VC_nacional", "nacional"),
        "IPC_vs_IPVA_existentes_nacional": ks("IPC_nacional", "IPVA_EXIST_nacional", "nacional"),
        "IPC_vs_IPVA_existentes_provincia": ks("IPC_provincia", "IPVA_EXIST_provincia", "provincia"),
        "IPC_vs_IPVA_panel_provincia": ks("IPC_provincia", "IPVA_PANEL_provincia", "provincia"),
        "IPC_vs_SERPAVI_provincia": ks("IPC_provincia", "SERPAVI_VC_provincia", "provincia"),
        "SERPAVI_vs_IPVA_panel_provincia": ks("SERPAVI_VC_provincia", "IPVA_PANEL_provincia", "provincia"),
        "SERPAVI_vs_IPVA_total_municipio": ks("SERPAVI_VC_municipio", "IPVA_TAM_municipio", "municipio"),
        "SERPAVI_vs_IPVA_total_distrito": ks("SERPAVI_VC_distrito", "IPVA_TOTAL_distrito", "distrito"),
        "IPVA_nuevos_vs_existentes_provincia": ks("IPVA_NUEVO_provincia", "IPVA_EXIST_provincia", "provincia"),
        "GVA_vs_SERPAVI_municipio": ks("GVA_municipio", "SERPAVI_VC_municipio", "municipio"),
        "GVA_vs_IPVA_nuevos_provincia": ks("GVA_provincia", "IPVA_NUEVO_provincia", "provincia"),
        "Incasol_vs_SERPAVI_municipio_(resumen)": ks("INCASOL_municipio", "SERPAVI_VC_municipio", "municipio"),
        "Incasol_vs_IPVA_nuevos_provincia_(resumen)": ks("INCASOL_provincia", "IPVA_NUEVO_provincia", "provincia"),
    }
    n_obs_total = int(sum(len(p) for p in P.values()))
    resultado = {
        "rama": "v15/fase1.2-auditoria-alquiler",
        "pregunta": ("¿Son completas, coherentes y estables las series de alquiler (IPC, IPVA, SERPAVI, fianzas GVA, "
                     "Incasòl, EMAL) y cuál conviene como medida principal y de robustez en cada pregunta V15?"),
        "capa": "C4",
        "datos": {
            "base": "data/base/hechos.parquet (consultas agregadas con duckdb)",
            "crudos": ["data/raw/v9/gva_fianzas", "data/raw/v5/gva_fianzas_*.csv", "data/raw/pdf/serpavi_v2_municipios.csv",
                       "data/raw/ine_ipc_alquiler.csv", "data/raw/ine_v2_ipc_alquiler_prov.csv",
                       "data/raw/v3/incasol_fianzas_municipio_v3.csv.gz",
                       "data/raw/v9/incasol/incasol_qww9-bvhh_actual.csv.gz", "data/raw/v9/insideairbnb"],
            "fuentes": ["INE IPC alquiler", "INE IPVA", "MIVAU SERPAVI", "GVA fianzas", "Incasòl fianzas (resumen)",
                        "EMAL Euskadi", "Eurostat HICP CP041", "Inside Airbnb (no oficial, solo resumen)"],
            "descarga_mas_reciente": "2026-10-15",
        },
        "N": {"series_de_tasas": len(P), "observaciones_de_tasas_interanuales": n_obs_total,
              "pares_de_fuentes_comparados": int(len(pares)), "comparaciones_de_vintages": int(len(rev))},
        "metodo": ("Auditoría descriptiva determinista (SEED=20261010): z robusto 0,6745(x-mediana)/MAD sobre tasas "
                   "interanuales, |z|>5, temporal por territorio si hay >=8 tasas y transversal por periodo si no; "
                   "coherencia por pares en código INE (correlación conjunta, temporal y transversal, diferencia media, "
                   "ventanas de divergencia); brechas nuevos-stock; rupturas, revisiones y cobertura. Sin estimación."),
        "estimacion": None,
        "ic95": None,
        "p_ajustado": None,
        "nivel_evidencia": "DESCRIPTIVO",
        "diagnosticos": {
            "atipicos_por_fuente": por_fuente.to_dict(orient="records"),
            "atipicos_diagnostico_serpavi": diag_at,
            "unidades_dudosas": dud,
            "coherencia_pares_clave": clave,
            "ventanas_de_divergencia_nacional": vent,
            "brecha_ipva_nuevos_existentes_razon_de_indices": razon.to_dict(orient="records"),
            "rupturas_consistencia_indice_tasa": cons.to_dict(orient="records"),
            "rupturas_cambio_de_media_descriptivo": rs.to_dict(orient="records"),
            "serpavi_cobertura": diag_ser,
            "gva_cobertura": diag_gva,
            "incasol_cobertura_resumen": diag_inc,
            "revisiones": rev.drop(columns=["vintage_a", "vintage_b"]).to_dict(orient="records"),
            "potencia_p5_p6_recuentos": pot,
            "inside_airbnb_resumen": iab,
            "tablas": sorted(ficheros),
        },
        "fuera_muestra": None,
        "notas": [
            "Auditoría descriptiva C4: sin efectos ni regresiones; el estadístico de cambio de media es solo orientativo, sin p-valor.",
            "Incasòl e Inside Airbnb (licencia no abierta): en output solo estadísticos resumen y recuentos de municipios; sin series por periodo.",
            "Cruces solo por código INE. Excluido del cruce: la tabla de alquiler por CP de la Comunidad de Madrid (origen no verificado, "
            "data/raw/v3/madrid_alquiler_cp_v3) y los barrios de Inside Airbnb (no llevan código INE).",
            "Las comparaciones entre vintages son descargas del mismo lote (2026-10-09 a 2026-10-15): revisión nula no demuestra ausencia de revisiones reales.",
            "GVA 2026 es un año parcial y se excluye de las tasas; la base de hechos solo conserva València ciudad en fianzas municipales.",
            "SERPAVI nacional y autonómico son agregados propios (media de tasas provinciales ponderada por contratos), aproximados.",
        ],
    }
    (OUT / "resultado.json").write_text(json.dumps(resultado, ensure_ascii=False, indent=2, default=str),
                                        encoding="utf-8")
    out = {"R": R, "res": res, "pares": pares, "rev": rev, "resultado": resultado, "tab_b": tab_b, "razon": razon,
            "ser_c": ser_c, "gva_c": gva_c, "inc_c": inc_c, "cob": cob, "top": top, "por_fuente": por_fuente,
            "pot": pot, "dud": dud, "rs": rs, "vent": vent, "diag_ser": diag_ser, "diag_gva": diag_gva,
            "diag_inc": diag_inc, "iab": iab}
    texto = re.sub(r"(?<=\d)\.(?=\d)", ",", informe_md(out))
    (OUT / "informe.md").write_text(texto, encoding="utf-8")
    return out


if __name__ == "__main__":
    main()
    print("auditoría alquiler: ok")
