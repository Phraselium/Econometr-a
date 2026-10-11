"""M0 v6: paneles de datos, diccionario, sellado v6 (solo entrenamiento), hechos y potencia. Sin red. SEED=20261010.

Lee solo data/raw y las salidas versionadas de v5 y v5_1. Escribe en output/v6/M0 y docs/v6/{diccionario,potencia}.md.
Los paneles de modelización pasan por holdout.sellar_v6: la parte sellada la escribe holdout en data/sealed y este
script NO la lee. Solo se guarda la parte de entrenamiento (*_train.csv.gz).
Las fuentes sin dato o sin cobertura provincial se marcan «sin dato» en el diccionario; no se estima nada aquí.
"""
from __future__ import annotations

import json
import math
import re
import sys
import unicodedata
from pathlib import Path

import numpy as np
import pandas as pd

RAIZ = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(RAIZ / "src"))
import holdout  # noqa: E402

SEED = holdout.SEED
RAW = RAIZ / "data" / "raw"
V5 = RAIZ / "output" / "v5"
V51 = RAIZ / "output" / "v5_1"
OUT = RAIZ / "output" / "v6" / "M0"
PAN = OUT / "paneles"
DOCS = RAIZ / "docs" / "v6"
FECHA = "2026-10-11"
ULT_PRECIO = 2025   # último año completo del valor tasado (2026T1 existe solo trimestral)
ULT_SERPAVI = 2024  # último año SERPAVI (2011-2024)
ULT_ANUAL = 2025    # último año completo en fuentes anuales/mensuales (2026 parcial, excluido)
INI_PROV = 2015
REG = []            # diccionario: (panel, col, nivel, frec, fuente, fecha_dato, capa, transf, nota)


def rd(ruta, **kw):
    kw.setdefault("low_memory", False)
    return pd.read_csv(RAW / ruta, **kw)


def num(s):
    return pd.to_numeric(s, errors="coerce")


def norm(s):
    s = unicodedata.normalize("NFKD", str(s)).encode("ascii", "ignore").decode().lower()
    return re.sub(r"[^a-z0-9]", "", s)


def aliases(nom: str) -> set[str]:
    b = [nom]
    if "/" in nom:
        b += nom.split("/")
    m = re.match(r"^(.*)\((.*)\)$", nom.strip())
    if m:
        b += [m.group(1), m.group(2), f"{m.group(2)} {m.group(1)}", f"{m.group(1)}, {m.group(2)}"]
    if ", " in nom:
        a, c = nom.split(", ", 1)
        b += [f"{c} {a}", a]
    return {norm(x) for x in b if norm(x)}


def _mapa_prov():
    e = rd("ine_v2_etdp_prov.csv", usecols=["territorio", "nivel", "codigo"], dtype=str)
    e = e[e.nivel == "provincia"].drop_duplicates("codigo")
    m: dict[str, str] = {}
    for cod, nom in zip(e.codigo.str.zfill(2), e.territorio):
        for a in aliases(nom):
            m.setdefault(a, cod)
    return m


PROV_MAP = _mapa_prov()
NOMBRE_PROV = {}  # cod -> nombre ETDP
for _n, _c in PROV_MAP.items():
    NOMBRE_PROV.setdefault(_c, _n)


SINONIMOS_PROV = {"guipuzcoa": "20", "vizcaya": "48"}  # nombres de MIVAU/SERPAVI no presentes en el alias de ETDP


def cod_prov(nombre) -> str | None:
    s = re.sub(r"\s*\(\d+\)\s*$", "", str(nombre)).strip()  # notas al pie tipo «Extremadura (1)»
    return PROV_MAP.get(norm(s)) or SINONIMOS_PROV.get(norm(s))


def trim(fecha: pd.Series) -> pd.Series:
    d = pd.to_datetime(fecha)
    return d.dt.year.astype(str) + "T" + d.dt.quarter.astype(str)


def S(df: pd.DataFrame, keys: list[str], fn="mean", n_req=1) -> pd.Series:
    """Agregado por clave; NaN si hay menos de n_req observaciones (sin interpolar)."""
    g = df.groupby(keys)["valor"]
    return g.agg(fn).where(g.count() >= n_req)


def anio_de(fecha: pd.Series) -> pd.Series:
    return pd.to_datetime(fecha).dt.year


LOG: list[dict] = []


def log(paso, n, nota=""):
    LOG.append({"paso": paso, "n": int(n), "nota": nota})
    print(f"[{paso}] n={n} {nota}")


# ============================================================================ 1. PROVINCIAS: precio (compra)
def precio_tasado_prov():
    d = rd("mivau_valor_tasado_nacional_ccaa_prov.csv", usecols=["fecha", "serie", "valor", "territorio", "nivel"], dtype=str)
    d = d[(d.nivel == "provincia") & d.serie.str.startswith("valor_tasado_libre_provincia_")].copy()
    d["cod"] = d.territorio.map(cod_prov)
    d["valor"] = num(d.valor)
    log("tasado_prov_filas", len(d), f"sin cod={d.cod.isna().sum()} | provincias={d.cod.nunique()}")
    d["anio"] = anio_de(d.fecha)
    d["t"] = trim(d.fecha)
    return d


def registradores_prov():
    r = rd("pdf/registradores_opendata_anual.csv", usecols=["fecha", "serie", "valor", "territorio", "nivel"], dtype=str)
    r = r[r.nivel == "provincia"].copy()
    r["cod"] = r.territorio.map(cod_prov)
    r["valor"] = num(r.valor)
    r["anio"] = anio_de(r.fecha)
    return r


def etdp_prov():
    e = rd("ine_v2_etdp_prov.csv", usecols=["fecha", "valor", "nivel", "codigo", "desglose"], dtype={"codigo": str})
    e = e[e.nivel == "provincia"].copy()
    e["cod"] = e.codigo.str.zfill(2)
    e["valor"] = num(e.valor)
    e["anio"] = anio_de(e.fecha)
    e["t"] = trim(e.fecha)
    return e


def ipc_alquiler_prov():
    i = rd("ine_v2_ipc_alquiler_prov.csv", usecols=["fecha", "valor", "nivel", "codigo", "medida"], dtype={"codigo": str})
    i = i[i.medida == "IPC_alquiler_vivienda_indice"].copy()
    i["valor"] = num(i.valor)
    i["anio"] = anio_de(i.fecha)
    i["t"] = trim(i.fecha)
    i["cod"] = i.codigo.str.zfill(2)
    return i


# ============================================================================ 2. PROVINCIAS: alquiler y contratos
def serpavi_prov():
    s = rd("pdf/serpavi_provincias.csv", usecols=["fecha", "valor", "codigo", "tipologia", "variable", "estadistico"],
           dtype={"codigo": str})
    s["cod"] = s.codigo.str.zfill(2)
    s["valor"] = num(s.valor)
    s["anio"] = anio_de(s.fecha)
    return s


def epa_prov(nivel="provincia"):
    e = rd("ine_v2_epa_prov.csv", usecols=["fecha", "valor", "nivel", "codigo", "medida"], dtype={"codigo": str})
    e = e[e.nivel == nivel].copy()
    e["cod"] = e.codigo.str.zfill(2)
    e["valor"] = num(e.valor)
    e["anio"] = anio_de(e.fecha)
    e["t"] = trim(e.fecha)
    return e


def gva_fianzas():
    frames = []
    for y in range(2020, 2027):
        f = RAW / "v5" / f"gva_fianzas_{y}.csv"
        if f.exists():
            frames.append(pd.read_csv(f, sep=";", dtype=str))
    g = pd.concat(frames, ignore_index=True)
    g["valor"] = num(g.importe_fianza)
    g["anio"] = num(g.anyo_datos).astype("Int64")
    g["cod_prov"] = g.cod_provincia.str.zfill(2)
    g["cod_mun"] = g.cod_provincia.str.zfill(2) + g.cod_municipio.str.zfill(3)
    g = g[g.anio <= ULT_ANUAL]
    return g


def incasol():
    f = pd.read_csv(RAW / "v3" / "incasol_fianzas_municipio_v3.csv.gz", dtype={"codigo": str}, low_memory=False,
                    usecols=["fecha", "valor", "codigo", "banda", "serie"])
    f["valor"] = num(f.valor)
    f["anio"] = anio_de(f.fecha)
    f["cod_mun"] = f.codigo.str.zfill(5)
    f["cod_prov"] = f.cod_mun.str[:2]
    f = f[f.anio <= ULT_ANUAL]
    return f


def share_600(f: pd.DataFrame, keys: list[str]) -> pd.Series:
    tot = f[f.banda == "TOTAL_bandas"].groupby(keys)["valor"].sum()
    alto = f[f.banda == ">600euros/mes"].groupby(keys)["valor"].sum()
    return (100 * alto / tot).where(tot > 0)


def zonas_vigentes(df: pd.DataFrame, col_mun: str, ini: str, fin: str, anios) -> pd.DataFrame:
    """Municipio vigente en el año Y si ini <= 31/12/Y y (fin vacío o fin >= 01/01/Y)."""
    d = df.copy()
    d["ini"] = pd.to_datetime(d[ini], errors="coerce")
    d["fin"] = pd.to_datetime(d[fin], errors="coerce") if fin in d else pd.NaT
    d[col_mun] = d[col_mun].astype(str).str.zfill(5)
    rows = []
    for y in anios:
        v = (d.ini <= pd.Timestamp(y, 12, 31)) & (d.fin.isna() | (d.fin >= pd.Timestamp(y, 1, 1)))
        rows.append(pd.DataFrame({"cod_mun": d.loc[v, col_mun], "anio": y}))
    return pd.concat(rows, ignore_index=True).drop_duplicates()


# ============================================================================ 3. ENSAMBLE PROVINCIAL
def construir_provincial():
    cods = sorted(set(PROV_MAP.values()))
    cods = [c for c in cods if c not in ("00",)]
    anios = list(range(INI_PROV, ULT_ANUAL + 1))
    idx = pd.MultiIndex.from_product([cods, anios], names=["cod", "anio"])
    A = {}

    tas = precio_tasado_prov()
    A["pm2_tasado"] = S(tas, ["cod", "anio"], "mean", 4)
    log("tasado_prov_anual", A["pm2_tasado"].notna().sum(), "media de 4 trimestres completos")

    rg = registradores_prov()
    A["pm2_reg"] = S(rg[rg.serie == "compraventas_viv_pm2"], ["cod", "anio"], "mean", 1)
    A["cv_reg"] = S(rg[rg.serie == "compraventas_viv_num"], ["cod", "anio"], "mean", 1)

    et = etdp_prov()
    tot = et[et.desglose == "total"]
    A["cv_etdp"] = S(tot, ["cod", "anio"], "sum", 12)
    nue = S(et[et.desglose == "nueva"], ["cod", "anio"], "sum", 12)
    A["share_nueva_etdp"] = 100 * nue / A["cv_etdp"]

    ipc = ipc_alquiler_prov()
    A["ipc_alq_idx"] = S(ipc[ipc.nivel == "provincia"], ["cod", "anio"], "mean", 12)

    sp = serpavi_prov()
    vc = sp[sp.tipologia == "VC"]
    A["alq_m2_serpavi"] = S(vc[(vc.variable == "alquiler_m2") & (vc.estadistico == "mediana")], ["cod", "anio"], "mean", 1)
    A["alq_mes_serpavi"] = S(vc[(vc.variable == "alquiler_mes") & (vc.estadistico == "mediana")], ["cod", "anio"], "mean", 1)
    A["n_contratos_serpavi"] = S(vc[(vc.variable == "n_contratos")], ["cod", "anio"], "mean", 1)

    ep = epa_prov()
    A["ocupados_miles"] = S(ep[ep.medida == "EPA_ocupados"], ["cod", "anio"], "mean", 4)
    A["parados_miles"] = S(ep[ep.medida == "EPA_parados"], ["cod", "anio"], "mean", 4)
    A["paro_tasa"] = 100 * A["parados_miles"] / (A["parados_miles"] + A["ocupados_miles"])

    pib = rd("ine_v2_cre.csv", usecols=["fecha", "valor", "nivel", "codigo", "unidad"], dtype={"codigo": str})
    pib = pib[pib.nivel == "provincia"].copy()
    unidad = str(pib.unidad.iloc[0]).lower()
    factor = 1e6 if "millones" in unidad else (1e3 if "miles" in unidad else 1.0)
    pib["valor"] = num(pib.valor) * factor
    pib["cod"] = pib.codigo.str.zfill(2)
    pib["anio"] = anio_de(pib.fecha)
    pib_eur = S(pib, ["cod", "anio"], "mean", 1)
    log("pib_unidad", factor, f"unidad original: {unidad}")

    pa = rd("ine_v2_padron_prov_pais.csv", usecols=["fecha", "valor", "nivel", "codigo", "desglose"], dtype={"codigo": str})
    pa = pa[pa.nivel == "provincia"].copy()
    pa["cod"] = pa.codigo.str.zfill(2)
    pa["valor"] = num(pa.valor)
    pa["anio"] = anio_de(pa.fecha)
    A["pob_total"] = S(pa[pa.desglose == "nacionalidad=Total"], ["cod", "anio"], "sum", 1)
    A["pob_ext"] = S(pa[pa.desglose == "nacionalidad=Extranjera"], ["cod", "anio"], "sum", 1)
    A["share_ext_pob"] = 100 * A["pob_ext"] / A["pob_total"]
    A["pib_pc"] = pib_eur / A["pob_total"]

    pe = rd("ine_v2_padron_prov_edad_nac.csv", usecols=["fecha", "valor", "nivel", "codigo", "desglose"], dtype={"codigo": str})
    pe = pe[pe.nivel == "provincia"].copy()
    pe["cod"] = pe.codigo.str.zfill(2)
    pe["valor"] = num(pe.valor)
    pe["anio"] = anio_de(pe.fecha)
    dd = pe.desglose.astype(str)
    j = pe[dd.str.fullmatch(r"nacionalidad=(Española|Extranjera); edad=20-34")]
    t_ = pe[dd.str.fullmatch(r"nacionalidad=(Española|Extranjera); edad=Todas")]
    m19 = pe[dd.str.fullmatch(r"nacionalidad=(Española|Extranjera); edad=0-19")]
    jov = S(j, ["cod", "anio"], "sum", 2)
    tod = S(t_, ["cod", "anio"], "sum", 2)
    m19s = S(m19, ["cod", "anio"], "sum", 2)
    A["share_20_34"] = 100 * jov / tod
    adultos20 = tod - m19s

    ho = rd("ine_v2_hogares_prov.csv", usecols=["fecha", "valor", "nivel", "codigo", "desglose"], dtype={"codigo": str})
    ho = ho[(ho.nivel == "provincia") & (ho.desglose == "tamaño=Total")].copy()
    ho["cod"] = ho.codigo.str.zfill(2)
    ho["valor"] = num(ho.valor)
    ho["anio"] = anio_de(ho.fecha)
    A["hogares_miles_proxy"] = S(ho, ["cod", "anio"], "mean", 4) / 1000
    A["jefatura_proxy_pct"] = 100 * (S(ho, ["cod", "anio"], "mean", 4)) / adultos20

    mg = rd("ine_v2_migraciones_prov.csv", usecols=["fecha", "valor", "nivel", "codigo", "desglose"], dtype={"codigo": str})
    mg = mg[mg.nivel == "provincia"].copy()
    mg["cod"] = mg.codigo.str.zfill(2)
    mg["valor"] = num(mg.valor)
    mg["anio"] = anio_de(mg.fecha)
    A["llegada_esp_desde_ext"] = S(mg[mg.desglose == "nacionalidad=Española; sexo=Ambos; edad=Total"], ["cod", "anio"], "sum", 2)
    A["llegada_ext_desde_ext"] = S(mg[mg.desglose == "nacionalidad=Extranjero; sexo=Ambos; edad=Total"], ["cod", "anio"], "sum", 2)
    A["llegada_total_desde_ext"] = S(mg[mg.desglose == "nacionalidad=Total; sexo=Ambos; edad=Total"], ["cod", "anio"], "sum", 2)

    vu = rd("ine_v2_vut.csv", usecols=["fecha", "valor", "nivel", "codigo", "medida"], dtype={"codigo": str})
    vu = vu[(vu.nivel == "provincia") & (vu.medida == "viviendas_turisticas")].copy()
    vu["cod"] = vu.codigo.str.zfill(2)
    vu["valor"] = num(vu.valor)
    vu["anio"] = anio_de(vu.fecha)
    A["vut_viviendas"] = S(vu, ["cod", "anio"], "mean", 1)  # INE VTE: 1-2 meses publicados por año

    tt = rd("mivau_v2_iniciadas_terminadas_prov.csv", usecols=["fecha", "valor", "serie", "territorio", "nivel"], dtype=str)
    tt = tt[tt.nivel == "provincia"].copy()
    tt["valor"] = num(tt.valor)
    tt["cod"] = tt.territorio.map(cod_prov)
    tt["anio"] = anio_de(tt.fecha)
    ter = tt[tt.serie.str.startswith("viv_libres_terminadas_mensual_provincia_")]
    ini = tt[tt.serie.str.startswith("viv_libres_iniciadas_anual_provincia_")]
    A["terminadas_libres"] = S(ter, ["cod", "anio"], "sum", 12)
    A["iniciadas_libres"] = S(ini, ["cod", "anio"], "mean", 1)

    bj = pd.read_csv(V51 / "T1" / "tablas" / "bajas_provincia_anio.csv", dtype={"cod_prov": str}, low_memory=False)
    bj["cod"] = bj.cod_prov.str.zfill(2)
    A["bajas_tasa_C_amplia_pct"] = (100 * bj.set_index(["cod", "anio"]).tasa_C_amplia).reindex(idx)

    su = rd("mivau_v2_suelo.csv", usecols=["fecha", "valor", "serie", "territorio", "nivel"], dtype=str)
    su = su[(su.nivel == "provincia") & su.serie.str.startswith("suelo_pm2_m50k_provincia_")].copy()
    su["valor"] = num(su.valor)
    su["cod"] = su.territorio.map(cod_prov)
    su["anio"] = anio_de(su.fecha)
    A["suelo_pm2_m50k"] = S(su, ["cod", "anio"], "mean", 4)

    ip = rd("ine_v2_ipva.csv", usecols=["fecha", "valor", "nivel", "codigo", "medida", "desglose"], dtype={"codigo": str})
    ip = ip[(ip.nivel == "provincia") & (ip.desglose == "Nuevo contrato") & (ip.medida == "IPVA_indice")].copy()
    ip["cod"] = ip.codigo.str.zfill(2)
    ip["valor"] = num(ip.valor)
    ip["anio"] = anio_de(ip.fecha)
    A["ipva_nuevo_idx"] = S(ip, ["cod", "anio"], "mean", 1)

    hip = rd("ine_v2_hipotecas_prov.csv", usecols=["fecha", "valor", "nivel", "codigo", "medida"], dtype={"codigo": str})
    hip = hip[(hip.nivel == "provincia") & (hip.medida == "hipotecas_viviendas_numero")].copy()
    hip["cod"] = hip.codigo.str.zfill(2)
    hip["valor"] = num(hip.valor)
    hip["anio"] = anio_de(hip.fecha)
    hip_a = S(hip, ["cod", "anio"], "sum", 12)
    A["hip_viv_num"] = hip_a
    A["share_contado_proxy"] = (100 * (1 - hip_a / A["cv_etdp"])).where((hip_a / A["cv_etdp"]).between(0, 1))

    tx = rd("mivau_transacciones_extranjeros.csv", usecols=["fecha", "valor", "serie", "territorio", "nivel"], dtype=str)
    tx = tx[(tx.nivel == "provincia") & tx.serie.str.startswith("tx_extranj_residentes_libre_provincia_")].copy()
    tx["valor"] = num(tx.valor)
    tx["cod"] = tx.territorio.map(cod_prov)
    tx["anio"] = anio_de(tx.fecha)
    tx_ext = S(tx, ["cod", "anio"], "sum", 4)
    A["tx_ext_residentes"] = tx_ext
    A["share_compra_ext_res_pct"] = (100 * tx_ext / A["cv_etdp"]).where(tx_ext.notna())

    rowsP = []
    for k, v in A.items():
        s = v.reindex(idx) if isinstance(v, pd.Series) else v
        rowsP.append(s.rename(k))
    P = pd.concat(rowsP, axis=1).reset_index()
    P["cod"] = P["cod"].astype(str)
    P["provincia"] = P.cod.map(NOMBRE_PROV)
    return P, tas, idx


def no_residentes_r1a() -> pd.DataFrame:
    """Reutiliza R1A (no residentes por provincia, 2015-2025); definiciones en output/v5/R1A/registro.csv."""
    r = pd.read_csv(V5 / "R1A" / "tablas" / "no_residentes_panel_provincias.csv", dtype={"ine": str}, low_memory=False)
    r = r[r.nivel == "provincia"].copy()
    r["cod"] = r.ine.map(cod_prov)
    rows = []
    for y in range(INI_PROV, ULT_ANUAL + 1):
        if f"nr{y}" in r.columns:
            rows.append(pd.DataFrame({"cod": r.cod, "anio": y, "no_res_share_R1A_pct": num(r[f"nr{y}"]) * 100}))
    return pd.concat(rows, ignore_index=True)


def estatico_prov():
    """Variables sin variación temporal o de corte transversal (fuera del panel: evita extrapolar en el tiempo)."""
    r = pd.read_csv(V5 / "R1A" / "tablas" / "no_residentes_panel_provincias.csv", dtype={"ine": str}, low_memory=False)
    r = r[r.nivel == "provincia"].copy()
    r["cod"] = r.ine.map(cod_prov)
    e = r[["cod", "costa", "isla", "costa_sol"]].drop_duplicates("cod").set_index("cod")
    cen = pd.read_csv(RAW / "v5" / "municipio_centroides_utm30.csv", dtype={"codigo": str}, low_memory=False)
    a4 = pd.read_csv(V5 / "A4" / "clasificacion_municipios.csv", dtype={"cod_mun": str, "cod_prov": str}, low_memory=False)
    a4["cod_mun"] = a4.cod_mun.str.zfill(5)
    a4["cod_prov"] = a4.cod_mun.str[:2]
    cen["codigo"] = cen.codigo.str.zfill(5)
    m = a4[["cod_mun", "cod_prov", "pob_2021", "municipio"]].merge(cen, left_on="cod_mun", right_on="codigo", how="inner")
    m = m.dropna(subset=["pob_2021"])
    centro = m.sort_values("pob_2021", ascending=False).groupby("cod_prov").head(1).set_index("cod_prov")
    m = m.join(centro[["x_m", "y_m"]].rename(columns=lambda c: c + "_c"), on="cod_prov")
    m["dist_centro_km"] = np.hypot(m.x_m - m.x_m_c, m.y_m - m.y_m_c) / 1000
    mun = m[["cod_mun", "cod_prov", "dist_centro_km"]]
    dist_prov = mun.groupby("cod_prov").dist_centro_km.median().rename("dist_centro_mediana_km")
    cen_name = centro.municipio.rename("municipio_centro_proxy")
    e = e.join(dist_prov.rename_axis("cod"), how="left")
    e = e.join(cen_name.rename_axis("cod"), how="left")
    cen_b = rd("v3/ine_v3_censo2021_municipio_viviendas.csv", dtype={"codigo": str, "serie": str, "nivel": str, "valor": str},
               usecols=["codigo", "serie", "nivel", "valor"])
    cen_b = cen_b[cen_b.nivel == "municipio"].copy()
    cen_b["valor"] = num(cen_b.valor)
    cen_b["cod_prov"] = cen_b.codigo.str.zfill(5).str[:2]
    tot = cen_b[cen_b.serie == "V_TOTAL"].groupby("cod_prov").valor.sum()
    npr = cen_b[cen_b.serie == "V_NOPRINCIPAL"].groupby("cod_prov").valor.sum()
    e["pct_no_principal_2021"] = (100 * npr / tot).rename_axis("cod")
    log("estatico_prov", len(e), "costa/isla (R1A), distancia mediana al mayor municipio (A4+centroides), censo 2021")
    return e.reset_index(), mun, centro


# ============================================================================ 4. PANEL TRIMESTRAL PROVINCIAL
def construir_trim_prov(tas: pd.DataFrame):
    tq = S(tas, ["cod", "t"], "mean", 1).rename("pm2_tasado")
    et = etdp_prov()
    et_tot = et[et.desglose == "total"]
    cv_t = S(et_tot, ["cod", "t"], "sum", 3).rename("cv_etdp")
    ipc = ipc_alquiler_prov()
    ipc_t = S(ipc[ipc.nivel == "provincia"], ["cod", "t"], "mean", 3).rename("ipc_alq_idx")
    hip = rd("ine_v2_hipotecas_prov.csv", usecols=["fecha", "valor", "nivel", "codigo", "medida"], dtype={"codigo": str})
    hip = hip[(hip.nivel == "provincia") & (hip.medida == "hipotecas_viviendas_numero")].copy()
    hip["cod"] = hip.codigo.str.zfill(2)
    hip["valor"] = num(hip.valor)
    hip["t"] = trim(hip.fecha)
    hip_t = S(hip, ["cod", "t"], "sum", 3).rename("hip_viv_num")
    Q = pd.concat([tq, cv_t, ipc_t, hip_t], axis=1).reset_index()
    Q["anio"] = Q.t.str[:4].astype(int)
    Q["provincia"] = Q.cod.map(NOMBRE_PROV)
    return Q.dropna(subset=["pm2_tasado"], how="all")


# ============================================================================ 5. MUNICIPAL Y DISTRITO
def construir_municipal(a4_names: dict):
    mv = rd("mivau_valor_tasado_municipios.csv", usecols=["fecha", "valor", "territorio", "nivel", "serie"], dtype=str)
    mv = mv[mv.nivel == "municipio"].copy()
    mv["valor"] = num(mv.valor)
    mv["cod_mun"] = mv.territorio.map(lambda t: a4_names.get(norm(t)))
    mv["anio"] = anio_de(mv.fecha)
    mv_a = S(mv, ["cod_mun", "anio"], "mean", 4).rename("pm2_tasado_mun")
    log("tasado_mun", mv.cod_mun.notna().sum(), f"municipios con código por nombre único: {mv.cod_mun.nunique()}")

    sm = pd.read_csv(RAW / "pdf" / "serpavi_v2_municipios.csv.gz", dtype={"codigo": str, "provincia_codigo": str},
                     usecols=["fecha", "valor", "nivel", "codigo", "tipologia", "variable", "estadistico"], low_memory=False)
    sm = sm[(sm.nivel == "MUN") & (sm.tipologia == "VC") & (sm.variable == "alquiler_m2") & (sm.estadistico == "mediana")].copy()
    sm["cod_mun"] = sm.codigo.str.zfill(5)
    sm["valor"] = num(sm.valor)
    sm["anio"] = anio_de(sm.fecha)
    sm_a = S(sm, ["cod_mun", "anio"], "mean", 1).rename("alq_m2_serpavi_mun")

    vu = rd("ine_v2_vut.csv", usecols=["fecha", "valor", "nivel", "codigo", "medida"], dtype={"codigo": str})
    vu = vu[(vu.nivel == "municipio") & (vu.medida == "viviendas_turisticas")].copy()
    vu["cod_mun"] = vu.codigo.str.zfill(5)
    vu["valor"] = num(vu.valor)
    vu["anio"] = anio_de(vu.fecha)
    vu_a = S(vu, ["cod_mun", "anio"], "mean", 1).rename("vut_viviendas_mun")

    gv = gva_fianzas()
    gv_a = gv.groupby(["cod_mun", "anio"]).agg(n_fianzas_gva_mun=("valor", "size"), fianza_media_gva_mun_eur=("valor", "mean"))

    inc = incasol()
    inc_n = inc[inc.banda == "TOTAL_bandas"].groupby(["cod_mun", "anio"]).valor.sum().rename("n_fianzas_incasol_mun")
    inc_s = share_600(inc, ["cod_mun", "anio"]).rename("pct_fianzas_600_incasol_mun")

    zt = rd("v3/zonas_tensionadas_v3.csv", dtype=str, low_memory=False)
    zt = zt[zt.cod_ine_municipio.notna()].copy()
    zt["cod_ine_municipio"] = zt.cod_ine_municipio.astype(str).str.zfill(5)
    zv = zonas_vigentes(zt, "cod_ine_municipio", "fecha_efecto", "fecha_fin_prevista", range(INI_PROV, ULT_ANUAL + 1))
    zv["tensionada_mun"] = 1

    cc = rd("v3/cataluna_contencion_rentas_v3.csv", dtype=str, low_memory=False)
    cc = cc[cc.cod_ine.notna()].copy()
    cc = cc.rename(columns={"cod_ine": "cod_ine_municipio"})
    cv = zonas_vigentes(cc, "cod_ine_municipio", "fecha_vigencia_inicio", "fecha_vigencia_fin", range(INI_PROV, ULT_ANUAL + 1))
    cv["tope_cat_mun"] = 1

    M = pd.concat([mv_a, sm_a, vu_a, gv_a, inc_n, inc_s], axis=1).reset_index()
    M = M.merge(zv, on=["cod_mun", "anio"], how="left")
    M = M.merge(cv, on=["cod_mun", "anio"], how="left")
    M["tensionada_mun"] = M.tensionada_mun.fillna(0)
    M["tope_cat_mun"] = M.tope_cat_mun.fillna(0)
    M["cod_prov"] = M.cod_mun.str[:2]
    M = M[M.anio.between(INI_PROV, ULT_ANUAL)]
    return M


def construir_distrito():
    sd = pd.read_csv(RAW / "v3" / "serpavi_distritos_nacional_v3.csv.gz", usecols=["serie", "valor", "fecha"], low_memory=False)
    sd = sd[sd.serie.str.match(r"SERPAVI_DIS_\d{7}_ALQM2_LV_\d+_VC$")].copy()
    sd["percentil"] = sd.serie.str.extract(r"LV_(\d+)_VC$")[0]
    sd["distrito"] = sd.serie.str.extract(r"SERPAVI_DIS_(\d{7})_")[0]
    sd["valor"] = num(sd.valor)
    sd["anio"] = anio_de(sd.fecha)
    pct = sorted(sd.percentil.unique())
    log("serpavi_dis_percentiles", len(pct), ",".join(pct))  # v3 solo trae p25 y p75: no hay mediana de distrito
    p = sd.pivot_table(index=["distrito", "anio"], columns="percentil", values="valor", aggfunc="mean").reset_index()
    p = p.rename(columns={"25": "alq_m2_p25_dis", "75": "alq_m2_p75_dis"})
    p["alq_m2_serpavi_dis"] = (p.alq_m2_p25_dis + p.alq_m2_p75_dis) / 2  # punto medio p25-p75 (aproximación de la mediana)
    D = p[["distrito", "anio", "alq_m2_serpavi_dis", "alq_m2_p25_dis", "alq_m2_p75_dis"]]
    vs = pd.read_csv(RAW / "v3" / "ine_v3_vut_seccion.csv.gz", usecols=["serie", "valor", "fecha"], low_memory=False)
    vs = vs[vs.serie.str.match(r"VUT_distrito_\d{7}_plazas$")].copy()
    vs["distrito"] = vs.serie.str.extract(r"VUT_distrito_(\d{7})_")[0]
    vs["valor"] = num(vs.valor)
    vs["anio"] = anio_de(vs.fecha)
    v_a = S(vs, ["distrito", "anio"], "mean", 1).rename("vut_plazas_dis").reset_index()
    D = D.merge(v_a, on=["distrito", "anio"], how="outer")
    D["cod_prov"] = D.distrito.str[:2]
    D = D[D.anio.between(2011, ULT_SERPAVI)]
    return D


# ============================================================================ 6. NACIONAL Y CCAA (descriptivos)
def construir_nacional_trim():
    hip =rd("ecb_tipo_hipotecario_es.csv", usecols=["fecha", "valor"])
    hip["valor"] = num(hip.valor)
    hip["t"] = trim(hip.fecha)
    s1 = S(hip, ["t"], "mean", 3).rename("tipo_hip_ecb_pct")

    cr = rd("bde_credito_finalidad.csv", usecols=["fecha", "valor", "titulo"])
    cr["valor"] = num(cr.valor)
    cr["t"] = trim(cr.fecha)
    stock = cr[cr.titulo == "Saldo vivo (importe) crédito a la vivienda, hogares"]
    nuevo = cr[cr.titulo == "Nuevas operaciones (importe) crédito a la vivienda, hogares"]
    s2 = S(stock, ["t"], "last", 3).rename("credito_viv_stock_mill_eur")
    s3 = S(nuevo, ["t"], "sum", 3).rename("credito_viv_nuevas_mill_eur")

    ca = pd.read_csv(V5 / "CA" / "tablas" / "credito_iniciadas_trimestral.csv")
    s4 = pd.Series(num(ca.constr_mas_inmob).values, index=ca.p.str.replace("Q", "T")).rename("credito_constr_inmob_bde")
    s4 = s4.groupby(level=0).last()

    hi = rd("ecb_hicp_es.csv", usecols=["fecha", "valor"])
    hi["valor"] = num(hi.valor)
    hi["t"] = trim(hi.fecha)
    hq = S(hi, ["t"], "mean", 3).sort_index()
    s5 = (100 * (hq / hq.shift(4) - 1)).rename("inflacion_hicp_ia_pct")

    ec = rd("eurostat_costes.csv", usecols=["fecha", "valor", "serie"])
    ec["valor"] = num(ec.valor)
    ec["t"] = trim(ec.fecha)
    ec = ec[ec.serie.astype(str).str.startswith("Q|COST")]
    s6 = S(ec, ["t"], "mean", 1).rename("coste_construccion_idx")

    vt = rd("mivau_valor_tasado_nacional_ccaa_prov.csv", usecols=["fecha", "valor", "serie", "nivel"])
    vt = vt[(vt.nivel == "nacional") & (vt.serie == "valor_tasado_libre_nacional")].copy()
    vt["valor"] = num(vt.valor)
    vt["t"] = trim(vt.fecha)
    s7 = S(vt, ["t"], "mean", 1).rename("pm2_tasado_nacional")

    ipc = ipc_alquiler_prov()
    ipn = ipc[(ipc.nivel == "nacional")]
    s8 = S(ipn, ["t"], "mean", 3).rename("ipc_alq_nacional_idx")

    et = etdp_prov()
    et_m = et[et.desglose == "total"].groupby("fecha").valor.sum(min_count=1).reset_index()
    et_m["t"] = trim(et_m.fecha)
    s9 = S(et_m, ["t"], "sum", 3).rename("cv_etdp_nacional_suma_prov")

    ipv = rd("ine_ipv_80270.csv", usecols=["fecha", "valor", "nombre"])
    ipv = ipv[ipv.nombre == "Nacional. General. Índice."].copy()
    ipv["valor"] = num(ipv.valor)
    ipv["t"] = trim(ipv.fecha)
    s10 = S(ipv, ["t"], "mean", 3).rename("ipv_ine_nacional_idx")

    ep = epa_prov("nacional")
    oc = S(ep[ep.medida == "EPA_ocupados"], ["t"], "mean", 1)
    pa = S(ep[ep.medida == "EPA_parados"], ["t"], "mean", 1)
    s11 = (100 * pa / (pa + oc)).rename("paro_tasa_nacional_pct")

    hq2 = rd("ine_v2_hipotecas_prov.csv", usecols=["fecha", "valor", "nivel", "medida"])
    hq2 = hq2[(hq2.nivel == "provincia") & (hq2.medida == "hipotecas_viviendas_numero")].copy()
    hq2["valor"] = num(hq2.valor)
    hm = hq2.groupby("fecha").valor.sum(min_count=1).reset_index()
    hm["t"] = trim(hm.fecha)
    s12 = S(hm, ["t"], "sum", 3).rename("hip_viv_num_nacional_suma_prov")

    N = pd.concat([s1, s2, s3, s4, s5, s6, s7, s8, s9, s10, s11, s12], axis=1).sort_index()
    N = N.reset_index().rename(columns={"index": "t"})
    N["anio"] = N.t.str[:4].astype(int)
    N = N[N.anio.between(2005, ULT_ANUAL)]
    return N


def construir_ccaa_anual():
    ipv = rd("ine_ipv_80270.csv", usecols=["fecha", "valor", "nombre"])
    ipv = ipv[ipv.nombre.str.endswith(". General. Índice.", na=False) & ~ipv.nombre.str.startswith("Nacional")].copy()
    ipv["ccaa"] = ipv.nombre.str.split(".").str[0]
    ipv["valor"] = num(ipv.valor)
    ipv["anio"] = anio_de(ipv.fecha)
    ipv = ipv[ipv.anio.between(2015, ULT_ANUAL)]
    g = ipv.groupby(["ccaa", "anio"]).valor.agg(["mean", "count"])
    g = g[g["count"] >= 4]["mean"].rename("ipv_ine_ccaa_idx_media_anual").reset_index()
    cb = pd.read_csv(V5 / "CB" / "tablas" / "c5_panel_ccaa.csv", index_col=0)
    cb = cb[["alq_share_censo", "usurp_x100k", "verb_pos_x100k"]].rename_axis("ccaa").reset_index()
    cb["ccaa"] = cb.ccaa.astype(str)
    return g, cb


def a23_anual():
    t = pd.read_csv(V5 / "A23" / "tablas" / "indice_triangulado.csv")
    p = pd.read_csv(V5 / "A23" / "tablas" / "precio_m2_nivel.csv")
    m = t.merge(p, on="anio", how="outer").sort_values("anio")
    return m.rename(columns={"min": "idx_triang_min", "max": "idx_triang_max", "mediana_4": "idx_triang_mediana"})


# ============================================================================ 7. SELLADO, ESCRITURA, DOCS
def sellar_panel(df, nombre, nivel, col_anio, ult, **kw):
    """Devuelve la parte de entrenamiento; registra unidades y años del lado sellado con el panel en memoria."""
    tr = holdout.sellar_v6(df, nombre, nivel, col_anio, ult, **kw)
    unidad = kw.get("col_prov") or kw.get("col_mun") or kw.get("col_dist")
    u_tot = df[unidad].astype(str).nunique()
    u_tr = tr[unidad].astype(str).nunique()
    a_tot = sorted(pd.to_numeric(df[col_anio], errors="coerce").dropna().unique().astype(int).tolist())
    a_tr = sorted(pd.to_numeric(tr[col_anio], errors="coerce").dropna().unique().astype(int).tolist())
    info = {"panel": nombre, "nivel": nivel, "ultimo_anio": ult, "filas_total": int(len(df)), "filas_train": int(len(tr)),
            "filas_sealed": int(len(df) - len(tr)), "unidades_total": u_tot, "unidades_train": u_tr,
            "unidades_sealed": u_tot - u_tr, "anios_total": [min(a_tot), max(a_tot)] if a_tot else None,
            "anios_train": [min(a_tr), max(a_tr)] if a_tr else None,
            "anios_sealed": [int(ult), max(a_tot)] if a_tot else None}
    return tr, info


def escribir_train(tr: pd.DataFrame, nombre: str):
    PAN.mkdir(parents=True, exist_ok=True)
    ruta = PAN / f"{nombre}_train.csv.gz"
    tr.to_csv(ruta, index=False, compression="gzip", float_format="%.6g")
    return ruta


def cobertura(df: pd.DataFrame, unidad: str, anio: str = "anio"):
    res = {}
    for c in df.columns:
        if c in (unidad, anio, "provincia", "t", "municipio", "distrito", "cod_prov", "cod_mun", "cod", "anio_sealed") \
                or c.endswith("_interp"):
            continue
        s = df[[unidad, anio, c]].dropna(subset=[c])
        if s.empty:
            res[c] = {"n": 0, "unidades": 0, "anios": None}
        else:
            res[c] = {"n": int(len(s)), "unidades": int(s[unidad].nunique()),
                      "anios": [str(s[anio].min()), str(s[anio].max())]}
    return res


def a4_nombres() -> dict:
    a4 = pd.read_csv(V5 / "A4" / "clasificacion_municipios.csv", dtype={"cod_mun": str, "cod_prov": str}, low_memory=False)
    a4["cod_mun"] = a4.cod_mun.str.zfill(5)
    a4["k"] = a4.municipio.map(norm)
    n_cod = a4.groupby("k").cod_mun.nunique()
    u = a4.drop_duplicates("k").set_index("k").cod_mun
    return u[n_cod.reindex(u.index) == 1].to_dict()


def construir_provincial_completo():
    P, tas, _ = construir_provincial()
    P = P.merge(no_residentes_r1a(), on=["cod", "anio"], how="left")
    gv = gva_fianzas()
    gvp = gv.groupby(["cod_prov", "anio"]).valor.agg(n_fianzas_gva="size", fianza_media_gva_eur="mean").reset_index()
    inc = incasol()
    inc_n = inc[inc.banda == "TOTAL_bandas"].groupby(["cod_prov", "anio"]).valor.sum().rename("n_fianzas_incasol")
    inc_s = share_600(inc, ["cod_prov", "anio"]).rename("pct_fianzas_600_incasol")
    extra = pd.concat([inc_n, inc_s], axis=1).reset_index().rename(columns={"cod_prov": "cod"})
    gvp = gvp.rename(columns={"cod_prov": "cod"})
    P = P.merge(gvp, on=["cod", "anio"], how="left").merge(extra, on=["cod", "anio"], how="left")
    return P, tas


def derivadas(P: pd.DataFrame) -> pd.DataFrame:
    P = P.sort_values(["cod", "anio"]).copy()

    def L(s):
        return np.log(s.where(s > 0))

    P["ln_pm2_tasado"] = L(P.pm2_tasado)
    P["ln_pm2_registradores"] = L(P.pm2_reg)
    P["ln_cv_etdp"] = L(P.cv_etdp)
    P["ln_cv_registradores"] = L(P.cv_reg)
    P["ln_hip_viv_num"] = L(P.hip_viv_num)
    P["ln_pob"] = L(P.pob_total)
    P["ln_ocupados_miles"] = L(P.ocupados_miles)
    P["ln_pib_pc"] = L(P.pib_pc)
    P["ln_vut"] = L(P.vut_viviendas)
    P["ln_terminadas_libres"] = L(P.terminadas_libres)
    P["ln_iniciadas_libres"] = L(P.iniciadas_libres)
    P["ln_suelo_pm2_m50k"] = L(P.suelo_pm2_m50k)
    P["ln_llegada_total_ext"] = L(P.llegada_total_desde_ext)
    P["ln_llegada_esp_ext"] = L(P.llegada_esp_desde_ext)
    P["ln_llegada_ext_ext"] = L(P.llegada_ext_desde_ext)
    P["ln_alq_m2_serpavi_vc"] = L(P.alq_m2_serpavi)
    P["ln_alq_mes_serpavi_vc"] = L(P.alq_mes_serpavi)
    P["ln_n_contratos_serpavi_vc"] = L(P.n_contratos_serpavi)
    P["ln_ipc_alq_idx"] = L(P.ipc_alq_idx)
    P["d_ln_ipc_alq"] = P.groupby("cod").ln_ipc_alq_idx.diff()
    P["d_ln_pm2_tasado"] = P.groupby("cod").ln_pm2_tasado.diff()
    P["ln_ratio_precio_alquiler"] = P.ln_pm2_tasado - P.ln_alq_m2_serpavi_vc - math.log(12)
    P["rentabilidad_bruta_pct"] = 100 * 12 * P.alq_m2_serpavi / P.pm2_tasado
    P["ln_fianza_media_gva_eur"] = L(P.fianza_media_gva_eur)
    P["ln_n_fianzas_gva"] = L(P.n_fianzas_gva)
    P["ln_n_fianzas_incasol"] = L(P.n_fianzas_incasol)
    P["ln_ipva_nuevo_idx"] = L(P.ipva_nuevo_idx)
    return P


def tensionadas_prov(M: pd.DataFrame) -> pd.DataFrame:
    t = M.assign(prov=M.cod_mun.str[:2]).groupby(["prov", "anio"]).agg(
        n_mun_tensionados=("tensionada_mun", "sum"), n_mun_topes_cat=("tope_cat_mun", "sum")).reset_index()
    return t.rename(columns={"prov": "cod"})


def mde(N: int, clusters: int, icc: float, K: int, alpha: float = 0.05, power: float = 0.8):
    from statistics import NormalDist
    nd = NormalDist()
    za = nd.inv_cdf(1 - alpha / (2 * K))
    zb = nd.inv_cdf(power)
    rho_iid = math.tanh((za + zb) / math.sqrt(N - 3))
    m = N / max(clusters, 1)
    deff = 1 + (m - 1) * icc
    neff = N / deff
    rho_cl = math.tanh((za + zb) / math.sqrt(neff - 3)) if neff > 4 else float("nan")
    return rho_iid, rho_cl, deff, neff


def cache_sellado():
    """Mismas reglas que holdout.distrito_sellado_v6 / municipio_sellado_v6, con las listas calculadas UNA vez.
    Sin esto, holdout relee el VUT (1,6 M filas) por cada distrito único y el proceso no termina.
    Se verifica la igualdad con las funciones originales sobre una muestra de códigos."""
    dv3 = frozenset(holdout.distritos_sellados_v3())
    pv6 = frozenset(holdout.provincias_selladas_v6())

    def dist_v6(cod):
        d = str(cod).zfill(7)
        if d in dv3:
            return None
        return d[:2] in pv6

    def mun_v6(cod):
        return str(cod).zfill(5)[:2] in pv6

    muestra = ["0100101", "0200201", "2800101", "4400101", "3300101"]
    for d in muestra:
        assert dist_v6(d) == holdout.distrito_sellado_v6(d), d
    for c in ["01001", "07001", "22001", "50001", "03001"]:
        assert mun_v6(c) == holdout.municipio_sellado_v6(c), c
    holdout.distrito_sellado_v6 = dist_v6
    holdout.municipio_sellado_v6 = mun_v6
    log("cache_sellado", len(dv3), f"distritos v3 excluidos; provincias v6={sorted(pv6)}")


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    PAN.mkdir(parents=True, exist_ok=True)
    cache_sellado()
    P, tas = construir_provincial_completo()
    P = derivadas(P)

    M = construir_municipal(a4_nombres())
    M["ln_pm2_tasado_mun"] = np.log(M.pm2_tasado_mun.where(M.pm2_tasado_mun > 0))
    M["ln_alq_m2_serpavi_mun"] = np.log(M.alq_m2_serpavi_mun.where(M.alq_m2_serpavi_mun > 0))
    M["ln_vut_viviendas_mun"] = np.log(M.vut_viviendas_mun.where(M.vut_viviendas_mun > 0))
    M["ln_n_fianzas_gva_mun"] = np.log(M.n_fianzas_gva_mun.where(M.n_fianzas_gva_mun > 0))
    M["ln_fianza_media_gva_mun_eur"] = np.log(M.fianza_media_gva_mun_eur.where(M.fianza_media_gva_mun_eur > 0))
    M["ln_n_fianzas_incasol_mun"] = np.log(M.n_fianzas_incasol_mun.where(M.n_fianzas_incasol_mun > 0))

    P = P.merge(tensionadas_prov(M), on=["cod", "anio"], how="left")
    D = construir_distrito()
    D["ln_alq_m2_serpavi_dis"] = np.log(D.alq_m2_serpavi_dis.where(D.alq_m2_serpavi_dis > 0))
    D["ln_vut_plazas_dis"] = np.log(D.vut_plazas_dis.where(D.vut_plazas_dis > 0))

    Q = construir_trim_prov(tas)
    Q["ln_pm2_tasado"] = np.log(Q.pm2_tasado.where(Q.pm2_tasado > 0))
    Q["ln_cv_etdp"] = np.log(Q.cv_etdp.where(Q.cv_etdp > 0))
    Q["ln_ipc_alq_idx"] = np.log(Q.ipc_alq_idx.where(Q.ipc_alq_idx > 0))
    Q["ln_hip_viv_num"] = np.log(Q.hip_viv_num.where(Q.hip_viv_num > 0))
    Q = Q[Q.anio >= INI_PROV]
    ult_trim = int(Q.anio[Q.pm2_tasado.notna()].max())
    log("ultimo_anio_trim", ult_trim, "último año con valor tasado trimestral")

    # Variables por panel (columnas del panel de modelización)
    C_COMPRA = ["ln_pm2_tasado", "ln_pm2_registradores", "ln_cv_etdp", "ln_cv_registradores", "share_nueva_etdp",
                "ln_hip_viv_num", "share_contado_proxy", "share_compra_ext_res_pct", "no_res_share_R1A_pct",
                "ln_pob", "share_ext_pob", "share_20_34", "jefatura_proxy_pct", "paro_tasa", "ln_ocupados_miles",
                "ln_pib_pc", "ln_vut", "ln_terminadas_libres", "ln_iniciadas_libres", "bajas_tasa_C_amplia_pct",
                "ln_suelo_pm2_m50k", "ln_llegada_total_ext", "ln_llegada_esp_ext", "ln_llegada_ext_ext"]
    C_ALQ = ["ln_alq_m2_serpavi_vc", "ln_alq_mes_serpavi_vc", "ln_n_contratos_serpavi_vc", "ln_ipc_alq_idx",
             "d_ln_ipc_alq", "ln_ratio_precio_alquiler", "rentabilidad_bruta_pct", "ln_vut", "n_mun_tensionados",
             "n_mun_topes_cat"]
    C_NUEVOS = ["ln_fianza_media_gva_eur", "ln_n_fianzas_gva", "pct_fianzas_600_incasol", "ln_n_fianzas_incasol",
                "ln_ipva_nuevo_idx"]
    C_MUN = ["ln_pm2_tasado_mun", "ln_alq_m2_serpavi_mun", "ln_vut_viviendas_mun", "ln_n_fianzas_gva_mun",
             "ln_fianza_media_gva_mun_eur", "ln_n_fianzas_incasol_mun", "pct_fianzas_600_incasol_mun",
             "tensionada_mun", "tope_cat_mun"]
    C_DIS = ["ln_alq_m2_serpavi_dis", "ln_vut_plazas_dis"]
    C_TRIM = ["ln_pm2_tasado", "ln_cv_etdp", "ln_ipc_alq_idx", "ln_hip_viv_num"]

    def sub(df, keys, cols, desde=INI_PROV, hasta=None):
        d = df[keys + [c for c in cols if c in df.columns]].copy()
        d = d[d.anio.between(desde, hasta or 9999)]
        return d.drop_duplicates(keys)

    PANELES = [
        ("prov_compra_anual", sub(P, ["cod", "anio", "provincia"], C_COMPRA, hasta=ULT_ANUAL), "provincia", ULT_PRECIO,
         {"col_prov": "cod"}),
        ("prov_alquiler_anual", sub(P, ["cod", "anio", "provincia"], C_ALQ, hasta=ULT_ANUAL), "provincia", ULT_SERPAVI,
         {"col_prov": "cod"}),
        ("prov_contratos_nuevos_anual", sub(P, ["cod", "anio", "provincia"], C_NUEVOS, hasta=ULT_ANUAL), "provincia",
         ULT_ANUAL, {"col_prov": "cod"}),
        ("prov_trim_compra", Q[["cod", "anio", "t", "provincia"] + [c for c in C_TRIM + ["pm2_tasado", "cv_etdp",
                                                                                          "ipc_alq_idx", "hip_viv_num"]
                                                                  if c in Q.columns]],
         "provincia", ult_trim, {"col_prov": "cod"}),
        ("mun_anual", M[["cod_mun", "anio", "cod_prov"] + C_MUN].copy(), "municipio", ULT_PRECIO, {"col_mun": "cod_mun"}),
        ("dis_alquiler_anual", D[["distrito", "anio", "cod_prov"] + C_DIS].copy(), "distrito", ULT_SERPAVI,
         {"col_dist": "distrito"}),
    ]
    for nombre, df, _, _, _ in PANELES:
        log(f"panel_total_{nombre}", len(df), f"unidades={df.iloc[:, 0].nunique()}")

    infos, trains = [], {}
    for nombre, df, nivel, ult, kw in PANELES:
        df = df.copy()
        tr, info = sellar_panel(df, nombre, nivel, "anio", ult, **kw)
        vacias = [c for c in tr.columns if c not in ("cod", "cod_mun", "distrito", "anio", "t", "provincia", "cod_prov")
                  and tr[c].notna().sum() == 0]
        if vacias:
            log(f"sin_dato_{nombre}", len(vacias), ",".join(vacias))
            tr = tr.drop(columns=vacias)
        infos.append(info)
        trains[nombre] = tr
        escribir_train(tr, nombre)
        log(f"train_{nombre}", len(tr), f"ult={ult} sellado={info['filas_sealed']}")

    # Descriptivos y estáticos (no son paneles de modelización: sin sellado; ver diccionario)
    N_nac = construir_nacional_trim()
    A23 = a23_anual()
    ipv_ccaa, cb = construir_ccaa_anual()
    N_nac.to_csv(PAN / "nacional_trim_desc.csv", index=False)
    A23.to_csv(PAN / "nacional_anual_a23_desc.csv", index=False)
    ipv_ccaa.to_csv(PAN / "ccaa_ipv_anual_desc.csv", index=False)
    cb.to_csv(PAN / "ccaa_seguridad_juridica_transversal_desc.csv", index=False)
    est_p, mun_d, centro = estatico_prov()
    est_p.to_csv(PAN / "prov_estatico.csv", index=False)
    mun_est = mun_d.rename(columns={"cod_prov": "cod_prov"})[["cod_mun", "dist_centro_km"]]
    mun_est.to_csv(PAN / "mun_estatico.csv", index=False)

    resumen_cob = {}
    for nombre, tr in trains.items():
        unidad = {"prov": "cod", "mun": "cod_mun", "dis": "distrito"}[nombre.split("_")[0]]
        if nombre.startswith("prov"):
            unidad = "cod"
        elif nombre.startswith("mun"):
            unidad = "cod_mun"
        else:
            unidad = "distrito"
        resumen_cob[nombre] = cobertura(tr, unidad)

    with open(OUT / "sellado_info.json", "w", encoding="utf-8") as f:
        json.dump(infos, f, ensure_ascii=False, indent=1, default=str)
    with open(OUT / "cobertura_train.json", "w", encoding="utf-8") as f:
        json.dump(resumen_cob, f, ensure_ascii=False, indent=1, default=str)
    with open(OUT / "log_construccion.json", "w", encoding="utf-8") as f:
        json.dump(LOG, f, ensure_ascii=False, indent=1)
    pot = potencia_y_hechos()
    escribir_potencia_md(pot)
    escribir_resultado_hechos(pot, infos)
    print("OK", {i["panel"]: (i["filas_train"], i["filas_sealed"]) for i in infos})


ESPECIFICACIONES_POT = [
    # (panel, desenlace, mercado, nivel, K = variables candidatas del panel, unidad_clúster, fuente)
    ("prov_compra_anual", "ln_pm2_tasado", "precio de compra", "provincia", 22, "cod", "valor tasado MIVAU (anual)"),
    ("prov_compra_anual", "ln_cv_etdp", "volumen de compra", "provincia", 22, "cod", "compraventas INE ETDP"),
    ("prov_trim_compra", "ln_pm2_tasado", "precio de compra", "provincia (trimestral)", 4, "cod", "valor tasado MIVAU (trimestral)"),
    ("prov_trim_compra", "ln_cv_etdp", "volumen de compra", "provincia (trimestral)", 4, "cod", "compraventas INE ETDP"),
    ("prov_alquiler_anual", "ln_alq_m2_serpavi_vc", "alquiler de stock", "provincia", 10, "cod", "SERPAVI mediana VC"),
    ("prov_contratos_nuevos_anual", "ln_fianza_media_gva_eur", "alquiler de contratos nuevos", "provincia (solo CV)", 5, "cod", "fianzas GVA (€ depósito)"),
    ("mun_anual", "ln_pm2_tasado_mun", "precio de compra", "municipio (>25.000 hab., por nombre único)", 9, "cod_prov", "valor tasado MIVAU municipal"),
    ("mun_anual", "ln_alq_m2_serpavi_mun", "alquiler de stock", "municipio", 9, "cod_prov", "SERPAVI municipal mediana VC"),
    ("dis_alquiler_anual", "ln_alq_m2_serpavi_dis", "alquiler de stock", "distrito (aprox. mediana p25-p75)", 2, "cod_prov", "SERPAVI distritos v3"),
]


def potencia_y_hechos():
    """Potencia (efecto mínimo detectable) con el N de entrenamiento de cada panel, agrupación por CCAA (ICC supuesto)
    y Holm por el número de variables (cota Bonferroni, peor caso de Holm). Solo sobre la parte de entrenamiento."""
    from holdout import CCAA_PROV
    tr = {n: pd.read_csv(PAN / f"{n}_train.csv.gz", dtype={"cod": str, "cod_mun": str, "cod_prov": str, "distrito": str},
                         low_memory=False) for n in ["prov_compra_anual", "prov_trim_compra", "prov_alquiler_anual",
                                                       "prov_contratos_nuevos_anual", "mun_anual", "dis_alquiler_anual"]}
    icc = 0.3
    filas = []
    for panel, y, mercado, nivel, K, cl, fuente in ESPECIFICACIONES_POT:
        d = tr[panel]
        dd = d[d[y].notna()].copy()
        if "cod" in dd and cl == "cod_prov":
            dd["cod_prov"] = dd.cod_prov.astype(str).str.zfill(2) if "cod_prov" in dd else dd.cod.str[:2]
        ccaa = dd[cl].astype(str).str.zfill(2).map(lambda c: CCAA_PROV.get(c, "x")) if cl != "cod" else \
            dd.cod.astype(str).str.zfill(2).map(lambda c: CCAA_PROV.get(c, "x"))
        N = len(dd)
        n_cl = int(ccaa.nunique())
        sd_y = float(dd[y].std())
        rho_iid, rho_cl, deff, neff = mde(N, n_cl, icc, K)
        filas.append({"panel": panel, "desenlace": y, "mercado": mercado, "nivel": nivel, "K_variables_panel": K,
                      "N_train": N, "n_agrupaciones_CCAA": n_cl, "sd_desenlace_train": round(sd_y, 4),
                      "rho_min_iid": round(rho_iid, 4), "rho_min_cluster_ICC0.3": round(rho_cl, 4),
                      "deff": round(deff, 2), "N_eff": round(neff, 1),
                      "efecto_pct_1DE_iid": round(100 * (math.exp(rho_iid * sd_y) - 1), 2),
                      "efecto_pct_1DE_cluster": round(100 * (math.exp(rho_cl * sd_y) - 1), 2) if not math.isnan(rho_cl) else None,
                      "fuente": fuente})
    pot = pd.DataFrame(filas)
    pot.to_csv(OUT / "potencia.csv", index=False)
    return pot


def escribir_potencia_md(pot: pd.DataFrame):
    cab = ("| panel | desenlace (mercado) | nivel | K | N train | CCAA (clusters) | sd(y) | ρ mín. iid | ρ mín. clúster (ICC 0,3) | "
           "efecto mín. % por 1 DE de x (iid / clúster) |")
    lin = ["|---|---|---|---|---|---|---|---|---|---|"]
    for _, r in pot.iterrows():
        ef_cl = "n.d." if r["efecto_pct_1DE_cluster"] is None else f"{r['efecto_pct_1DE_cluster']:.2f}"
        lin.append(f"| {r['panel']} | {r['desenlace']} ({r['mercado']}) | {r['nivel']} | {r['K_variables_panel']} | {r['N_train']} | "
                   f"{r['n_agrupaciones_CCAA']} | {r['sd_desenlace_train']:.3f} | {r['rho_min_iid']:.3f} | "
                   f"{r['rho_min_cluster_ICC0.3']:.3f} | {r['efecto_pct_1DE_iid']:.2f} / {ef_cl} |")
    txt = ("# Potencia v6 (M0): efecto mínimo detectable\n\n"
           f"Fecha del cálculo: {FECHA}. Parte de entrenamiento únicamente (N = filas con desenlace no nulo en *_train).\n\n"
           "Método: ρ mín. = tanh((z_{1-α/(2K)} + z_{1-β}) / √(N_eff − 3)), con α = 0,05, β = 0,20 y K = número de variables "
           "candidatas del panel (cota Bonferroni, que es el peor caso de Holm sobre K contrastes). La columna «iid» usa N; la "
           "columna «clúster» usa N_eff = N / (1 + (m − 1)·ICC), con m = N / nº de CCAA y ICC = 0,3 SUPUESTO (no estimado). "
           "Con 17 CCAA como clústeres, la inferencia clúster robusta es poco fiable: la columna clúster es orientativa.\n\n"
           "El efecto mínimo en % se obtiene como 100·(exp(ρ·sd(ln y)) − 1): cambio de y por cada desviación típica de x.\n\n"
           + "\n".join([cab] + lin) + "\n\n"
           "Lectura: ninguna especificación con N de entrenamiento inferior a ~400 puede detectar efectos pequeños con seguridad "
           "tras Holm; el panel municipal y distrital tienen más N pero menos cobertura por unidad y sesgo de muestra "
           "(solo municipios con valor tasado por nombre único y distritos con SERPAVI).\n")
    (DOCS / "potencia.md").write_text(txt, encoding="utf-8")


def escribir_resultado_hechos(pot: pd.DataFrame, infos: list):
    hechos = []
    for i in infos:
        hechos.append({"id": f"M0-{i['panel']}", "indicador": f"Panel de modelización {i['panel']}: unidades y años de entrenamiento",
                       "valor": i["filas_train"], "min": None, "max": None, "unidad": "filas (entrenamiento)",
                       "periodo": f"{i['anios_train'][0]}-{i['anios_train'][1]}" if i["anios_train"] else None,
                       "cobertura": f"{i['unidades_train']} de {i['unidades_total']} unidades (sellado: {i['unidades_sealed']})",
                       "fuentes": "ver docs/v6/diccionario.md", "capa": "C4", "fecha_dato": FECHA})
    hechos.append({"id": "M0-SELLADO", "indicador": "Filas selladas (no abiertas) por panel", "valor": sum(i["filas_sealed"] for i in infos),
                   "min": None, "max": None, "unidad": "filas", "periodo": "ver output/v6/M0/sellado.md",
                   "cobertura": "validación v6 (holdout.sellar_v6)", "fuentes": "holdout.py", "capa": "C4", "fecha_dato": FECHA})
    with open(OUT / "hechos.json", "w", encoding="utf-8") as f:
        json.dump(hechos, f, ensure_ascii=False, indent=1, default=str)
    res = {
        "rama": "r6/main", "pregunta": "M0: datos, paneles, diccionario, sellado v6, hipótesis y potencia (sin estimación)",
        "capa": "C4", "datos": "output/v6/M0/paneles/*_train.csv.gz (ver docs/v6/diccionario.md)",
        "N": int(sum(i["filas_train"] for i in infos)), "metodo": "construcción de paneles; sellado v6; potencia por Fisher-z",
        "estimacion": None, "ic95": None, "p_ajustado": None, "nivel_evidencia": "DESCRIPTIVO",
        "medida_precio": "valor tasado MIVAU (provincia y municipio); Registradores (provincia, pm2 anual); índice triangulado A23 (nacional); IPV INE solo CCAA",
        "diagnosticos": {"sellado": infos, "potencia": pot[["panel", "desenlace", "N_train", "rho_min_iid"]].to_dict("records")},
        "fuera_muestra": None,
        "notas": "M0 no estima modelos. Validación sellada v6 contaminada descriptivamente por usos v4-v5 (decisiones.md). "
                 "Sin interpolación; ver docs/v6/diccionario.md para sin-dato y cobertura parcial.",
        "fecha_dato": FECHA,
    }
    with open(OUT / "resultado.json", "w", encoding="utf-8") as f:
        json.dump(res, f, ensure_ascii=False, indent=1, default=str)


if __name__ == "__main__":
    main()
