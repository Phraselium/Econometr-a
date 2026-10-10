#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Construcción v2 de paneles (provincial trimestral y anual, municipal anual,
UE anual y trimestral, nacional v2, eventos de política) a partir de data/raw.

Lectura: solo data/raw/ y data/processed/nacional_q.csv (v1, bloque nacional).
Escritura: data/processed/v2/ y docs/v2/diccionario_v2.md.
No modifica data/processed/*.csv de v1 (se comprueba md5 antes y después).

Reglas: ln_ en niveles positivos; d_ (Δ1) y d4_ (interanual trimestral) sobre ln_;
método por dato en <var>_metodo; <var>_interp = True solo en interpolaciones
(log-lineal entre dos observaciones). Sin extrapolación: huecos al final = NaN.
"""
from __future__ import annotations

import gzip
import hashlib
import re
import sys
import unicodedata
from pathlib import Path

import warnings

import numpy as np
import pandas as pd

warnings.simplefilter("ignore", pd.errors.PerformanceWarning)

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw"
PROC = ROOT / "data" / "processed"
V1_NAC = PROC / "nacional_q.csv"
V1_FILES = sorted(PROC.glob("*.csv"))  # ficheros v1: no se tocan; md5 antes/después
V1_MD5_BEFORE = {p.name: hashlib.md5(p.read_bytes()).hexdigest() for p in V1_FILES}
OUT = PROC / "v2"
DOCS = ROOT / "docs" / "v2"

QL = [str(p) for p in pd.period_range("2002Q1", "2026Q2", freq="Q")]
AY = list(range(2002, 2026))  # 2002..2025
MAX_BYTES = 50 * 1024 * 1024

REG: list[dict] = []   # filas del diccionario de variables
LOG: list[str] = []    # avisos de casamiento / cobertura
CHECKS: list[str] = []


def log(msg: str) -> None:
    print(msg, flush=True)
    LOG.append(msg)


def reg(panel, var, fuente, archivo, tabla, unidad, freq, agreg, metodo, notas=""):
    REG.append(dict(panel=panel, var=var, fuente=fuente, archivo=archivo, tabla=tabla,
                    unidad=unidad, freq=freq, agreg=agreg, metodo=metodo, notas=notas))


# ---------------------------------------------------------------- utilidades
def norm(s) -> str:
    if s is None or (isinstance(s, float) and np.isnan(s)):
        return ""
    s = unicodedata.normalize("NFKD", str(s))
    s = "".join(c for c in s if not unicodedata.combining(c)).lower()
    return re.sub(r"[^a-z0-9]+", " ", s).strip()


def rd(name: str) -> pd.DataFrame:
    return pd.read_csv(RAW / name, dtype=str)


def num(d: pd.DataFrame, col: str = "valor") -> pd.DataFrame:
    d[col] = pd.to_numeric(d[col], errors="coerce")
    return d


def qlab(fecha: pd.Series) -> pd.Series:
    return pd.to_datetime(fecha).dt.to_period("Q").astype(str)


def mlab(fecha: pd.Series) -> pd.Series:
    return pd.to_datetime(fecha).dt.to_period("M").astype(str)


def dedup(d: pd.DataFrame, keys: list[str]) -> pd.DataFrame:
    """Duplicados de clave: si el valor es idéntico se conserva una fila; si hay conflicto, NaN y aviso."""
    dup = d.duplicated(subset=keys, keep=False)
    if not dup.any():
        return d
    g = d[dup].groupby(keys)["valor"].agg(["nunique", "first"]).reset_index()
    conf = g[g["nunique"] > 1]
    log(f"  aviso: {int(dup.sum())} filas con clave duplicada {keys}; {len(g)} claves; conflictos de valor: {len(conf)} (→ NaN)")
    base_ = d[~dup]
    uniq = g[g["nunique"] == 1][keys + ["first"]].rename(columns={"first": "valor"})
    fixed = pd.concat([base_, uniq, conf[keys].assign(valor=np.nan)], ignore_index=True)
    return fixed


def monthly_to_q(d: pd.DataFrame, keys: list[str], how: str) -> pd.DataFrame:
    """Agrega mensual -> trimestral. Exige 3 meses; si falta alguno -> NaN (no se agrega)."""
    d = d.dropna(subset=["valor"]).copy()
    d["trimestre"] = qlab(d["fecha"])
    g = d.groupby(keys + ["trimestre"]).agg(
        v=("valor", "sum" if how == "sum" else "mean"),
        n=("fecha", "nunique")).reset_index()
    g = g[g["n"] == 3].rename(columns={"v": "valor"})
    return g


def wide(df: pd.DataFrame, idx: str, col: str, val: str, index: list, columns: list) -> pd.DataFrame:
    d = dedup(df.dropna(subset=[val]), [idx, col])
    return d.pivot(index=idx, columns=col, values=val).reindex(index=index, columns=columns)


def mask_method(W: pd.DataFrame, label: str) -> pd.DataFrame:
    return pd.DataFrame(np.where(W.notna(), label, ""), index=W.index, columns=W.columns, dtype=object)


def md5(path: Path) -> str:
    return hashlib.md5(path.read_bytes()).hexdigest()


def write_csv(df: pd.DataFrame, name: str) -> Path:
    OUT.mkdir(parents=True, exist_ok=True)
    p = OUT / f"{name}.csv"
    df.to_csv(p, index=False, float_format="%.10g")
    if p.stat().st_size > MAX_BYTES:
        gz = OUT / f"{name}.csv.gz"
        with gzip.GzipFile(gz, "wb", mtime=0, compresslevel=9) as f:
            f.write(p.read_bytes())
        p.unlink()
        log(f"  {name}: >50 MB -> {gz.name}")
        return gz
    return p


def add_logs(df: pd.DataFrame, cols: list[str], gcol: str, quarterly: bool) -> pd.DataFrame:
    """ln_ en niveles positivos; d_ln_ (Δ1) y, si trimestral, d4_ln_ (Δ4)."""
    df = df.sort_values([gcol, "trimestre" if quarterly else "anio"]).reset_index(drop=True)
    for c in cols:
        if c not in df:
            continue
        df["ln_" + c] = np.log(df[c].where(df[c] > 0))
        g = df.groupby(gcol)["ln_" + c]
        df["d_ln_" + c] = g.diff(1)
        if quarterly:
            df["d4_ln_" + c] = g.diff(4)
    return df


# ---------------------------------------------------------------- provincias
epa = num(rd("ine_v2_epa_prov.csv"))
_pn = epa[epa.nivel == "provincia"][["territorio", "codigo"]].drop_duplicates()
PROV_NAME = dict(zip(_pn.codigo, _pn.territorio))
PROVS = sorted(PROV_NAME)
assert len(PROVS) == 52, len(PROVS)

_ALIAS: dict[str, set] = {}


def _add_alias(k: str, code: str) -> None:
    k = norm(k)
    if k:
        _ALIAS.setdefault(k, set()).add(code)


for _c, _n in PROV_NAME.items():
    _add_alias(_n, _c)
    if ", " in _n:
        _a, _b = _n.split(", ", 1)
        _add_alias(f"{_b} {_a}", _c)
    for _part in _n.split("/"):
        _add_alias(_part, _c)
MANUAL_PROV = {
    "alava": "01", "vizcaya": "48", "guipuzcoa": "20", "lerida": "25", "gerona": "17",
    "la coruna": "15", "coruna": "15", "castellon": "12", "alicante": "03", "baleares": "07",
    "islas baleares": "07", "las palmas": "35", "palmas": "35", "la rioja": "26", "rioja": "26",
    "orense": "32", "avila": "05", "valencia": "46", "bizkaia": "48", "gipuzkoa": "20",
}


def prov_code(name) -> str | None:
    k = norm(name)
    cands = _ALIAS.get(k, set()) | ({MANUAL_PROV[k]} if k in MANUAL_PROV else set())
    return next(iter(cands)) if len(cands) == 1 else None


# ---------------------------------------------------------------- municipios (diccionario INE)
dic = pd.read_excel(RAW / "ine_diccionario_municipios_2026.xlsx", sheet_name=0, header=1, dtype=str)
dic = dic.dropna(subset=["CPRO", "CMUN", "NOMBRE"]).copy()
dic["cod_prov"] = dic.CPRO.str.zfill(2)
dic["cod_muni"] = dic.cod_prov + dic.CMUN.str.zfill(3)
dic["ccaa"] = dic.CODAUTO.str.zfill(2)
dic = dic.drop_duplicates("cod_muni")
MUNI_NAME = dict(zip(dic.cod_muni, dic.NOMBRE))
MUNI_PROV = dict(zip(dic.cod_muni, dic.cod_prov))
MUNI_CCAA = dict(zip(dic.cod_muni, dic.ccaa))
_MK: dict[str, set] = {}
for _c, _n in MUNI_NAME.items():
    for _k in {norm(_n)} | {norm(p) for p in _n.split("/")}:
        if _k:
            _MK.setdefault(_k, set()).add(_c)
_MATCH_LOG: dict[str, list] = {"no_casado": [], "ambiguo": [], "casado_con_provincia": 0, "casado_unico": 0}
_MATCH_CACHE: dict[tuple, str | None] = {}


def muni_code(name, hint: str | None = None) -> str | None:
    key = (norm(name), norm(hint) if hint else "")
    if key in _MATCH_CACHE:
        return _MATCH_CACHE[key]
    cands = set(_MK.get(norm(name), set()))
    res = None
    if len(cands) == 1:
        res = next(iter(cands))
        _MATCH_LOG["casado_unico"] += 1
    elif len(cands) > 1 and hint:
        hp = prov_code(hint)
        if hp:
            c2 = {c for c in cands if MUNI_PROV[c] == hp}
        else:
            hn = norm(hint)
            c2 = {c for c in cands if norm(PROV_NAME[MUNI_PROV[c]]).startswith(hn)}
        if len(c2) == 1:
            res = next(iter(c2))
            _MATCH_LOG["casado_con_provincia"] += 1
    if res is None:
        if len(cands) > 1:
            _MATCH_LOG["ambiguo"].append(f"{name} ({hint or ''}): {len(cands)} candidatos")
        else:
            _MATCH_LOG["no_casado"].append(name)
    _MATCH_CACHE[key] = res
    return res


PROV_DF = pd.DataFrame({"cod_prov": PROVS, "provincia": [PROV_NAME[c] for c in PROVS]})
PROV_DF["cod_ccaa"] = PROV_DF.cod_prov.map(
    lambda p: next(iter({MUNI_CCAA[m] for m in MUNI_PROV if MUNI_PROV[m] == p}), None))
log(f"Provincias: {len(PROVS)}; cod_ccaa asignado a {PROV_DF.cod_ccaa.notna().sum()}")

# ---------------------------------------------------------------- nacional v1 (bloque común)
v1 = pd.read_csv(V1_NAC, dtype={"trimestre": str})
v1 = v1.set_index("trimestre")
NAC_VARS = {"tipo_hip": "tipo_hip", "euribor": "euribor", "tipo_hip_real": "tipo_hip_real",
            "inflacion": "inflacion_deflactor"}
NAC = pd.DataFrame(index=QL)
NAC_METODO = {}
for v2n, v1n in NAC_VARS.items():
    NAC[v2n] = pd.to_numeric(v1[v1n], errors="coerce").reindex(QL)
    NAC_METODO[v2n] = v1[v1n + "_metodo"].reindex(QL) if (v1n + "_metodo") in v1 else None
NAC_INTERP = {k: (v1[NAC_VARS[k] + "_interp"].reindex(QL).astype("boolean") if NAC_VARS[k] + "_interp" in v1 else None)
              for k in NAC_VARS}
# coste de uso: tipo hipotecario - inflación esperada (media móvil 4T de la inflación interanual)
_infl_full = pd.to_numeric(v1["inflacion_deflactor"], errors="coerce")
_infl_esp = _infl_full.rolling(4, min_periods=4).mean()
NAC["coste_uso_aprox"] = (NAC["tipo_hip"] - _infl_esp.reindex(QL))
NAC["coste_uso_aprox"] = NAC["coste_uso_aprox"].where(NAC["tipo_hip"].notna() & _infl_esp.reindex(QL).notna())

# BdE v2 (crédito) — nacional
bde = num(rd("bde_credito_finalidad.csv"))
bde["trimestre"] = qlab(bde.fecha)


def bde_flow(serie: str) -> pd.Series:
    d = bde[bde.serie == serie]
    return monthly_to_q(d[["fecha", "valor"]].assign(k="n"), ["k"], "sum").set_index("trimestre")["valor"].reindex(QL)


def bde_stock(serie: str) -> pd.Series:
    d = bde[bde.serie == serie].dropna(subset=["valor"])
    d = d[pd.to_datetime(d.fecha).dt.month.isin([3, 6, 9, 12])]   # fin de trimestre
    s = d.set_index("trimestre")["valor"]
    return s[~s.index.duplicated()].reindex(QL)


NAC["credito_vivienda_nuevo"] = bde_flow("DN_1TI2TIE96")       # nuevas operaciones vivienda, Millones €
NAC["saldo"] = bde_stock("DF_MESNAA22A1U62251Z01E")           # saldo crédito vivienda hogares, Millones €
NAC_BDE_EXTRA = {
    "credito_nuevo_consumo_bde": bde_flow("DN_1TI2TIE99"),
    "credito_nuevo_otros_bde": bde_flow("DN_1TI2TIE102"),
    "saldo_consumo_bde": bde_stock("DF_MESNAA21A1U62251Z01E"),
}
log(f"Nacional: tipo_hip/euribor/tipo_hip_real/inflacion de v1; BdE crédito vivienda y saldo")

# ---------------------------------------------------------------- VARIABLES PROVINCIALES (trimestral)
PV: dict[str, tuple[pd.DataFrame, pd.DataFrame]] = {}   # nombre -> (valores, metodo) wide prov x QL


def put(name, W, label, panel="prov_q", fuente="", archivo="", tabla="", unidad="", freq="",
        agreg="", notas=""):
    M = mask_method(W, label) if isinstance(label, str) else label
    PV[name] = (W, M)
    reg(panel, name, fuente, archivo, tabla, unidad, freq, agreg, label if isinstance(label, str) else "mixto", notas)


# p_tasado y p_suelo (MIVAU, trimestral)
vt = rd("mivau_valor_tasado_nacional_ccaa_prov.csv")
vt = num(vt)
vt = vt[(vt.nivel == "provincia") & vt.serie.str.startswith("valor_tasado_libre_provincia_")].copy()
vt["cod"] = vt.territorio.map(prov_code)
log(f"  p_tasado: {vt.cod.isna().sum()} filas sin provincia casada: {sorted(vt[vt.cod.isna()].territorio.unique())}")
vt["trimestre"] = qlab(vt.fecha)
put("p_tasado", wide(vt.dropna(subset=["cod"]), "cod", "trimestre", "valor", PROVS, QL), "observado",
    fuente="MIVAU Boletín Online (sedal) valor tasado vivienda libre", archivo="mivau_valor_tasado_nacional_ccaa_prov.csv",
    tabla="35101000", unidad="€/m²", freq="trimestral", agreg="ninguna", notas="serie provincial (nivel provincia)")

sl = rd("mivau_v2_suelo.csv")
sl = num(sl)
sl = sl[(sl.nivel == "provincia") & sl.serie.str.startswith("suelo_pm2_provincia_")].copy()
sl["cod"] = sl.territorio.map(prov_code)
sl["trimestre"] = sl.periodo.str.replace("T", "Q")
put("p_suelo", wide(sl.dropna(subset=["cod"]), "cod", "trimestre", "valor", PROVS, QL), "observado",
    fuente="MIVAU Boletín Online (sedal) precio medio suelo urbano", archivo="mivau_v2_suelo.csv",
    tabla="36400500", unidad="€/m²", freq="trimestral", agreg="ninguna",
    notas="serie provincial de todos los municipios (no la de municipios >50.000 hab., tabla 36403000)")

# IPC alquiler (INE 76142, índice mensual -> media trimestral)
ipc = num(rd("ine_v2_ipc_alquiler_prov.csv"))
ipc = ipc[(ipc.nivel == "provincia") & (ipc.medida == "IPC_alquiler_vivienda_indice")].copy()
ipc["cod"] = ipc.codigo.str.zfill(2)
g = monthly_to_q(ipc[["cod", "fecha", "valor"]], ["cod"], "mean")
put("ipc_alquiler", wide(g, "cod", "trimestre", "valor", PROVS, QL), "agregado_media",
    fuente="INE IPC subclase alquiler de vivienda", archivo="ine_v2_ipc_alquiler_prov.csv", tabla="76142",
    unidad="índice (base INE)", freq="mensual", agreg="media de 3 meses (NaN si falta alguno)")

# Compraventas ETDP (6150, mensual, suma)
et_all = num(rd("ine_v2_etdp_prov.csv"))
et = et_all[(et_all.nivel == "provincia")].copy()
et["cod"] = et.codigo.str.zfill(2)
for des in ["total", "nueva", "usada", "libre", "protegida"]:
    d = et[et.desglose == des][["cod", "fecha", "valor"]]
    g = monthly_to_q(d, ["cod"], "sum")
    nm = "compraventas_" + des
    put(nm, wide(g, "cod", "trimestre", "valor", PROVS, QL), "agregado_suma",
        fuente="INE ETDP compraventas de viviendas", archivo="ine_v2_etdp_prov.csv", tabla="6150",
        unidad="número de compraventas", freq="mensual", agreg="suma de 3 meses (NaN si falta alguno)")

# Hipotecas (76317, mensual, suma)
hp_all = num(rd("ine_v2_hipotecas_prov.csv"))
hp = hp_all[(hp_all.nivel == "provincia")].copy()
hp["cod"] = hp.codigo.str.zfill(2)
for med, nm, unit in [("hipotecas_viviendas_numero", "hipotecas_n", "número"),
                      ("hipotecas_viviendas_importe", "hipotecas_importe", "miles de euros (NO VERIFICADO: inferido de magnitud)")]:
    g = monthly_to_q(hp[hp.medida == med][["cod", "fecha", "valor"]], ["cod"], "sum")
    put(nm, wide(g, "cod", "trimestre", "valor", PROVS, QL), "agregado_suma",
        fuente="INE HPT hipotecas sobre fincas viviendas (base nueva)", archivo="ine_v2_hipotecas_prov.csv",
        tabla="76317", unidad=unit, freq="mensual", agreg="suma de 3 meses",
        notas="unidad no verificada contra metadatos de la API" if "importe" in nm else "")

# EPA ocupados/parados (65345, trimestral)
ep = num(rd("ine_v2_epa_prov.csv"))
ep = ep[ep.nivel == "provincia"].copy()
ep["cod"] = ep.codigo.str.zfill(2)
ep["trimestre"] = qlab(ep.fecha)
for med, nm in [("EPA_ocupados", "ocupados"), ("EPA_parados", "parados")]:
    put(nm, wide(ep[ep.medida == med], "cod", "trimestre", "valor", PROVS, QL), "observado",
        fuente="INE EPA ocupados/parados por provincia", archivo="ine_v2_epa_prov.csv", tabla="65345",
        unidad="miles de personas", freq="trimestral", agreg="ninguna")

# Iniciadas/terminadas libres (MIVAU 32100500/32101000, mensual, suma) y protegidas (31205000)
def mivau_monthly(file, tabla, prefix, how="sum"):
    d = num(rd(file))
    d = d[(d.nivel == "provincia") & (d.tabla_codigo == tabla) & d.serie.str.startswith(prefix)].copy()
    d["cod"] = d.territorio.map(prov_code)
    return monthly_to_q(d.dropna(subset=["cod"])[["cod", "fecha", "valor"]], ["cod"], how)


g_ini = mivau_monthly("mivau_v2_iniciadas_terminadas_prov.csv", "32100500", "viv_libres_iniciadas_mensual_provincia_")
put("iniciadas_libres", wide(g_ini, "cod", "trimestre", "valor", PROVS, QL), "agregado_suma",
    fuente="MIVAU Boletín Online viviendas libres iniciadas (mensual)", archivo="mivau_v2_iniciadas_terminadas_prov.csv",
    tabla="32100500", unidad="viviendas", freq="mensual", agreg="suma de 3 meses")
g_ter = mivau_monthly("mivau_v2_iniciadas_terminadas_prov.csv", "32101000", "viv_libres_terminadas_mensual_provincia_")
put("terminadas_libres", wide(g_ter, "cod", "trimestre", "valor", PROVS, QL), "agregado_suma",
    fuente="MIVAU Boletín Online viviendas libres terminadas (mensual)", archivo="mivau_v2_iniciadas_terminadas_prov.csv",
    tabla="32101000", unidad="viviendas", freq="mensual", agreg="suma de 3 meses")
g_prot = mivau_monthly("mivau_v2_protegida.csv", "31205000", "prot_definitiva_mensual_provincia_")
put("protegida", wide(g_prot, "cod", "trimestre", "valor", PROVS, QL), "agregado_suma",
    fuente="MIVAU Boletín Online calificaciones definitivas VPO (mensual)", archivo="mivau_v2_protegida.csv",
    tabla="31205000", unidad="viviendas", freq="mensual", agreg="suma de 3 meses")

# VUT provincial (INE 39364): observación en 02/05/08/11 -> trimestre de la observación
vut = num(rd("ine_v2_vut.csv"))
vut = vut[(vut.nivel == "provincia") & (vut.medida == "viviendas_turisticas")].copy()
vut["cod"] = vut.codigo.str.zfill(2)
_mes_q = {2: "Q1", 5: "Q2", 8: "Q3", 11: "Q4"}
vut["mes"] = pd.to_datetime(vut.fecha).dt.month
vut = vut[vut.mes.isin(_mes_q)].copy()
vut["trimestre"] = pd.to_datetime(vut.fecha).dt.year.astype(str) + vut.mes.map(_mes_q)
put("vut_viviendas", wide(vut, "cod", "trimestre", "valor", PROVS, QL), "observado",
    fuente="INE Estadística experimental VTE (viviendas turísticas), provincias", archivo="ine_v2_vut.csv",
    tabla="39364", unidad="número de viviendas turísticas", freq="semestral irregular (meses 02/05/08/11 en la serie)",
    agreg="sin agregación: valor del mes observado asignado a su trimestre (Feb→T1, May→T2, Ago→T3, Nov→T4)",
    notas="sin interpolación; trimestres sin observación = NaN")

# Población (ECP 77023, 1 de enero -> T1; T2-T4 log-lineal entre dos 1-enero)
pe = num(rd("ine_v2_padron_prov_edad_nac.csv"))
pe = pe[pe.nivel == "provincia"].copy()
pe["cod"] = pe.codigo.str.zfill(2)
pe["cod_prov"] = pe["cod"]
pe["anio"] = pd.to_datetime(pe.fecha).dt.year


def stock_q(d: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    """d: cod, anio, valor (1 de enero). Devuelve (valores, métodos) prov x QL."""
    A = wide(d, "cod", "anio", "valor", PROVS, list(range(2002, 2027)))
    V = pd.DataFrame(np.nan, index=PROVS, columns=QL)
    M = pd.DataFrame("", index=PROVS, columns=QL, dtype=object)
    for y in AY:
        v0 = A[y]
        v1 = A[y + 1] if (y + 1) in A.columns else pd.Series(np.nan, index=PROVS)
        V[f"{y}Q1"] = v0
        M[f"{y}Q1"] = np.where(v0.notna(), "observado", "")
        for k in (2, 3, 4):
            ok = v0.notna() & v1.notna() & (v0 > 0) & (v1 > 0)
            val = np.exp(np.log(v0) + (k - 1) / 4 * (np.log(v1) - np.log(v0)))
            V[f"{y}Q{k}"] = val.where(ok)
            M[f"{y}Q{k}"] = np.where(ok, "interpolado_loglineal", "")
    return V, M


def put_stock(name, d, **kw):
    V, M = stock_q(d)
    PV[name] = (V, M)
    reg("prov_q", name, kw.get("fuente", ""), kw.get("archivo", ""), kw.get("tabla", ""), kw.get("unidad", "personas"),
        "anual (1 enero) -> trimestral", "T1 = 1 de enero; T2-T4 interpolados", "observado (T1) / interpolado_loglineal (T2-T4)",
        kw.get("notas", ""))


_ecp = dict(fuente="INE ECP población residente 1 de enero (77023)", archivo="ine_v2_padron_prov_edad_nac.csv",
            tabla="77023", unidad="personas")
put_stock("pob_total", pe[pe.desglose == "nacionalidad=Total; edad=Todas"][["cod", "anio", "valor"]], **_ecp)
put_stock("pob_extranj", pe[pe.desglose == "nacionalidad=Extranjera; edad=Todas"][["cod", "anio", "valor"]], **_ecp)
put_stock("pob_20_34", pe[pe.desglose == "nacionalidad=Total; edad=20-34"][["cod", "anio", "valor"]], **_ecp,
          notas="grupo 20-34 años, total nacionalidades")

# Inmigración desde el extranjero (24420, semestral): S1 -> T2, S2 -> T4, sin repartir
mg = num(rd("ine_v2_migraciones_prov.csv"))
mg = mg[(mg.nivel == "provincia") & (mg.tabla == "24420") &
        (mg.desglose == "nacionalidad=Total; sexo=Ambos; edad=Total")].copy()
mg["cod"] = mg.codigo.str.zfill(2)
mg["trimestre"] = mg.periodo.str[:4] + np.where(mg.periodo.str.endswith("S1"), "Q2", "Q4")
put("inmig_flujo", wide(mg, "cod", "trimestre", "valor", PROVS, QL), "semestral_asignado",
    fuente="INE EM inmigración procedente del extranjero, provincia (24420)", archivo="ine_v2_migraciones_prov.csv",
    tabla="24420", unidad="personas (flujo semestral)", freq="semestral (2008S1-2022S1)",
    agreg="semestre asignado al último trimestre del semestre (S1→T2, S2→T4)", notas="sin repartir entre trimestres")

# Zonas tensionadas: fracción de inmuebles residenciales (Catastro) en municipios con zona vigente
zon = rd("v2_zonas_tensionadas.csv")
zon["cod_muni"] = zon.cod_ine_municipio.str.zfill(5)
zon["ini"] = pd.to_datetime(zon.fecha_efecto.fillna(zon.fecha_publicacion_boe))
zon["fin"] = pd.to_datetime(zon.fecha_fin_prevista)
cat = rd("catastro_urbana_municipios.csv.gz")
cat = num(cat)
cat = cat[cat.serie.str.startswith("catastro_uu_res_")].copy()
cat["cod_muni"] = cat.codigo.str.zfill(5)
cat["anio"] = cat.periodo.astype(int)   # periodo N = stock a 31-dic de N-1 (disponible al inicio de N)
CAT_W = cat.pivot_table(index="cod_muni", columns="anio", values="valor", aggfunc="first")
CAT_YEARS = list(CAT_W.columns)


def weight_year(y: int) -> int:
    if y in CAT_YEARS:
        return y
    return min(CAT_YEARS, key=lambda z: (abs(z - y), z))


def active_mask(qend: pd.Timestamp, zz: pd.DataFrame) -> pd.Series:
    act = (zz.ini <= qend) & (zz.fin.isna() | (zz.fin >= qend))
    return zz.loc[act, "cod_muni"]


ZONA_START = 2024  # primera declaración en el fichero (2024-03-16)
zona_rows = []
for q in QL:
    per = pd.Period(q, freq="Q")
    qend = per.end_time.normalize()
    if per.year < ZONA_START:
        continue
    w = CAT_W[weight_year(per.year)].dropna()
    act = set(active_mask(qend, zon))
    for prov in PROVS:
        wp = w[w.index.str[:2] == prov]
        tot = wp.sum()
        if tot <= 0:
            continue
        ac = wp[wp.index.isin(act)].sum()
        zona_rows.append((prov, q, ac / tot))
ZONA_Q = pd.DataFrame(zona_rows, columns=["cod", "trimestre", "valor"])
put("zona_tensionada_share", wide(ZONA_Q, "cod", "trimestre", "valor", PROVS, QL), "escalonado",
    fuente="BOE declaraciones de zona tensionada (Ley 12/2023 art. 18) + Catastro uu residenciales por municipio",
    archivo="v2_zonas_tensionadas.csv; catastro_urbana_municipios.csv.gz", tabla="—", unidad="fracción [0,1]",
    freq="declaración (escalonada)", agreg="peso = unidades urbanas residenciales del municipio (año de stock disponible más cercano)",
    notas="NaN antes de 2024T1 (sin declaraciones en el fichero). Municipios fuera del fichero = 0 desde 2024 (supuesto de cobertura completa del fichero).")
log(f"  zona_tensionada_share: {ZONA_Q.shape[0]} celdas prov-trimestre con dato")

# ---------------------------------------------------------------- ensamblado trimestral provincial
base = pd.DataFrame({"cod_prov": np.repeat(PROVS, len(QL)), "trimestre": np.tile(QL, len(PROVS))})
base["anio"] = base.trimestre.str[:4].astype(int)
base = base.merge(PROV_DF, on="cod_prov", how="left")
LEVEL_PROV = []
for nm, (W, M) in PV.items():
    base[nm] = W.values.reshape(-1)
    base[nm + "_metodo"] = M.values.reshape(-1)
    base[nm + "_interp"] = base[nm + "_metodo"].eq("interpolado_loglineal")
    LEVEL_PROV.append(nm)
for nm in ["ocupados", "parados"]:
    pass  # ya incluidos
for nat in NAC.columns:
    base[nat] = np.tile(NAC[nat].values, len(PROVS))
    lab = NAC_METODO.get(nat)
    if lab is not None:
        base[nat + "_metodo"] = np.tile(lab.fillna("").values, len(PROVS))
    elif nat == "coste_uso_aprox":
        base[nat + "_metodo"] = np.where(base[nat].notna(), "derivado", "")
    elif nat in ("credito_vivienda_nuevo", "saldo"):
        base[nat + "_metodo"] = np.where(base[nat].notna(), "agregado_suma" if nat == "credito_vivienda_nuevo" else "fin_periodo", "")
    else:
        base[nat + "_metodo"] = ""
    ii = NAC_INTERP.get(nat)
    base[nat + "_interp"] = (np.tile(ii.fillna(False).astype(bool).values, len(PROVS)) if ii is not None
                             else base[nat + "_metodo"].eq("interpolado_loglineal"))
    LEVEL_PROV.append(nat)
for nm, s in NAC_BDE_EXTRA.items():
    pass
LEVEL_PROV = [c for c in LEVEL_PROV if c not in ("coste_uso_aprox",)] + ["coste_uso_aprox"]
base = add_logs(base, LEVEL_PROV, "cod_prov", quarterly=True)
base["ratio_precio_alquiler_idx"] = base["ln_p_tasado"] - base["ln_ipc_alquiler"]
base["ratio_precio_alquiler_idx_metodo"] = np.where(base["ratio_precio_alquiler_idx"].notna(), "derivado", "")
base["ratio_precio_alquiler_idx_interp"] = base["p_tasado_interp"].fillna(False) | base["ipc_alquiler_interp"].fillna(False)
reg("prov_q", "ratio_precio_alquiler_idx", "derivado", "—", "—", "índice (diferencia de logs)", "trimestral",
    "ln p_tasado − ln ipc_alquiler", "derivado", "índice relativo; no es un nivel de precio/alquiler")
reg("prov_q", "coste_uso_aprox", "derivado (Poterba)", "nacional_q v1 (tipo_hip, inflacion_deflactor)", "—", "pp",
    "trimestral", "tipo_hip − media móvil 4T de la inflación interanual",
    "derivado", "aproximación SIN impuestos, sin depreciación ni prima de riesgo; mismo valor en todas las provincias")
reg("prov_q", "credito_vivienda_nuevo", "BdE nuevas operaciones crédito vivienda hogares (DN_1TI2TIE96)", "bde_credito_finalidad.csv",
    "be1916", "Millones €", "mensual", "suma de 3 meses", "agregado_suma", "nacional (mismo valor en todas las provincias)")
reg("prov_q", "saldo", "BdE saldo crédito vivienda hogares (DF_MESNAA22A1U62251Z01E)", "bde_credito_finalidad.csv",
    "be1916", "Millones €", "mensual", "último mes del trimestre", "fin_periodo", "nacional; unidad 'Millones de euros' según metadatos del fichero")
for k in ["tipo_hip", "euribor", "tipo_hip_real", "inflacion"]:
    reg("prov_q", k, "v1 nacional_q.csv (ECB/BdE/INE CNT)", "data/processed/nacional_q.csv (v1)", "—",
        "% / pp", "trimestral", "según v1", "según v1 (copiado)", "nacional; inflacion = inflacion_deflactor (% interanual)")
reg("prov_q", "ln_* / d_ln_* / d4_ln_*", "derivado", "—", "—", "log natural", "trimestral",
    "ln de niveles > 0; d_ = Δ1 trimestre; d4_ = Δ4 (interanual)", "derivado", "NaN si nivel ≤ 0 o falta")

# orden de columnas
ID = ["trimestre", "anio", "cod_prov", "provincia", "cod_ccaa"]
cols = ID + [c for c in base.columns if c not in ID]
base = base[cols]
base = base.sort_values(["cod_prov", "trimestre"]).reset_index(drop=True)
assert not base.duplicated(["cod_prov", "trimestre"]).any()
PANEL_PROV_Q = base

# ---------------------------------------------------------------- ANUAL PROVINCIAL
q = base.copy()
q["anio"] = q.trimestre.str[:4].astype(int)
ANUAL_MEDIA = ["p_tasado", "p_suelo", "ipc_alquiler", "ocupados", "parados", "zona_tensionada_share"]
ANUAL_SUMA = ["compraventas_total", "compraventas_nueva", "compraventas_usada", "compraventas_libre",
              "compraventas_protegida", "hipotecas_n", "hipotecas_importe", "iniciadas_libres",
              "terminadas_libres", "protegida"]
ANUAL_SUMA = [c for c in ANUAL_SUMA if c in q.columns]
ANUAL_STOCK = ["pob_total", "pob_extranj", "pob_20_34"]
gb = q.groupby(["cod_prov", "anio"])
ann = pd.DataFrame(index=gb.size().index)
for c in ANUAL_MEDIA:
    cnt = gb[c].count()
    ann[c] = gb[c].mean().where(cnt == 4 if c != "zona_tensionada_share" else cnt >= 1)
for c in ANUAL_SUMA:
    cnt = gb[c].count()
    ann[c] = gb[c].sum().where(cnt == 4)
for c in ANUAL_STOCK:
    ann[c] = q[q.trimestre.str.endswith("Q1")].set_index(["cod_prov", "anio"])[c]
ann["vut_viviendas"] = q[q.trimestre.str.endswith("Q3")].set_index(["cod_prov", "anio"])["vut_viviendas"]
ann["inmig_flujo"] = (q[q.trimestre.str.endswith("Q2")].set_index(["cod_prov", "anio"])["inmig_flujo"] +
                      q[q.trimestre.str.endswith("Q4")].set_index(["cod_prov", "anio"])["inmig_flujo"])
ann["inmig_flujo"] = ann["inmig_flujo"].where(
    q[q.trimestre.str.endswith("Q2")].set_index(["cod_prov", "anio"])["inmig_flujo"].notna() &
    q[q.trimestre.str.endswith("Q4")].set_index(["cod_prov", "anio"])["inmig_flujo"].notna())
ann = ann.reset_index()
ann = ann[ann.anio.between(2002, 2025)]

# SERPAVI provincial (2011-2024)
sp = pd.read_csv(RAW / "pdf" / "serpavi_v2_municipios.csv.gz", dtype=str)
sp = num(sp)
spp = sp[sp.nivel == "PROV"].copy()
spp["anio"] = pd.to_datetime(spp.fecha).dt.year
spp["cod_prov"] = spp.codigo.str.zfill(2)
for ten in ["VC", "VU"]:
    m = spp[(spp.tipologia == ten) & (spp.variable == "alquiler_m2") & (spp.estadistico == "mediana")]
    ann = ann.merge(m[["cod_prov", "anio", "valor"]].rename(columns={"valor": f"serpavi_mediana_{ten.lower()}"}),
                    on=["cod_prov", "anio"], how="left")
    m = spp[(spp.tipologia == ten) & (spp.variable == "n_contratos")]
    ann = ann.merge(m[["cod_prov", "anio", "valor"]].rename(columns={"valor": f"serpavi_n_inmuebles_{ten.lower()}"}),
                    on=["cod_prov", "anio"], how="left")
reg("prov_a", "serpavi_mediana_vc/vu", "MIVAU-SERPAVI (AEAT IRPF) mediana alquiler €/m²/mes, provincia",
    "pdf/serpavi_v2_municipios.csv.gz (nivel PROV)", "—", "€/m²/mes", "anual", "observado", "observado", "2011-2024")
reg("prov_a", "serpavi_n_inmuebles_vc/vu", "MIVAU-SERPAVI nº de inmuebles (contratos) en alquiler, provincia",
    "pdf/serpavi_v2_municipios.csv.gz (nivel PROV)", "—", "inmuebles", "anual", "observado", "observado", "2011-2024")

# IPVA provincial (INE, 59058 Total, 48 provincias)
ip = num(rd("ine_v2_ipva.csv"))
ip = ip[(ip.nivel == "provincia") & (ip.tabla == "59058") & (ip.desglose == "Total")].copy()
ip["cod_prov"] = ip.codigo.str.zfill(2)
ip["anio"] = pd.to_datetime(ip.fecha).dt.year
for med, nm in [("IPVA_indice", "ipva_indice"), ("IPVA_variacion_anual", "ipva_var")]:
    d = ip[ip.medida == med][["cod_prov", "anio", "valor"]].rename(columns={"valor": nm})
    ann = ann.merge(d, on=["cod_prov", "anio"], how="left")
reg("prov_a", "ipva_indice / ipva_var", "INE IPVA índice de precios de vivienda en alquiler, total (59058)",
    "ine_v2_ipva.csv", "59058", "índice / % var. anual", "anual", "observado", "observado",
    "48 provincias; sin País Vasco ni Navarra")

# PIB provincial (CRE 80109) y PIB per cápita
cre = num(rd("ine_v2_cre.csv"))
cre = cre[(cre.nivel == "provincia")].copy()
cre["cod_prov"] = cre.codigo.str.zfill(2)
cre["anio"] = pd.to_datetime(cre.fecha).dt.year
ann = ann.merge(cre[["cod_prov", "anio", "valor"]].rename(columns={"valor": "pib_prov"}), on=["cod_prov", "anio"], how="left")
ann = ann.merge(pe[pe.desglose == "nacionalidad=Total; edad=Todas"][["cod_prov", "anio", "valor"]].rename(
    columns={"valor": "_pob_chk"}), on=["cod_prov", "anio"], how="left")
ann["pib_pc"] = ann.pib_prov * 1000 / ann["_pob_chk"]
ann = ann.drop(columns=["_pob_chk"])
reg("prov_a", "pib_prov", "INE CRE PIB a precios de mercado, precios corrientes, provincia (80109)", "ine_v2_cre.csv",
    "80109", "miles de € (NO VERIFICADO: inferido de FK_Unidad)", "anual", "observado", "observado", "2000-2025")
reg("prov_a", "pib_pc", "derivado: pib_prov × 1000 / pob_total (1 enero del mismo año)", "ine_v2_cre.csv + ine_v2_padron_prov_edad_nac.csv",
    "80109 / 77023", "€ por habitante", "anual", "cociente", "derivado",
    "NO existe renta disponible provincial en v2; PIB per cápita es el proxy de renta")

# Población por edad × nacionalidad y por agrupación de países
EDAD = {"Todas": "todas", "0-19": "0_19", "20-34": "20_34", "35-64": "35_64", "65+": "65_mas"}
NAC_S = {"Total": "total", "Española": "espanola", "Extranjera": "extranjera"}
for des in sorted(pe.desglose.unique()):
    m_ = re.match(r"nacionalidad=(.+); edad=(.+)$", des)
    if not m_:
        continue
    nac, edad = m_.group(1), m_.group(2)
    if nac not in NAC_S or edad not in EDAD:
        continue
    nm = f"pob_{NAC_S[nac]}_{EDAD[edad]}"
    d = pe[pe.desglose == des][["cod_prov", "anio", "valor"]].rename(columns={"valor": nm})
    ann = ann.merge(d, on=["cod_prov", "anio"], how="left")
pp = num(rd("ine_v2_padron_prov_pais.csv"))
pp = pp[pp.nivel == "provincia"].copy()
pp["cod_prov"] = pp.codigo.str.zfill(2)
pp["anio"] = pd.to_datetime(pp.fecha).dt.year
for des in sorted(pp.desglose.unique()):
    grp = des.replace("nacionalidad=", "")
    if grp in ("Total", "Española", "Extranjera"):
        continue
    nm = "pob_nac_" + norm(grp).replace(" ", "_")
    d = pp[pp.desglose == des][["cod_prov", "anio", "valor"]].rename(columns={"valor": nm})
    ann = ann.merge(d, on=["cod_prov", "anio"], how="left")
reg("prov_a", "pob_<nac>_<edad>", "INE ECP población 1 enero por nacionalidad y edad (77023)", "ine_v2_padron_prov_edad_nac.csv",
    "77023", "personas", "anual (1 enero)", "observado", "observado", "nombres: pob_{total,espanola,extranjera}_{todas,0_19,20_34,35_64,65_mas}")
reg("prov_a", "pob_nac_<grupo>", "INE ECP población por agrupación de países de nacionalidad (77023)", "ine_v2_padron_prov_pais.csv",
    "77023", "personas", "anual (1 enero)", "observado", "observado", "grupos según fichero; algunos con cobertura parcial")

# Ratios de nivel y esfuerzo
ann["precio_alquiler_ratio_nivel"] = ann.p_tasado / (12 * ann.serpavi_mediana_vc)
ann["esfuerzo_aprox"] = ann.p_tasado * 90 / ann.pib_pc
for nm, n_, u in [("precio_alquiler_ratio_nivel", "derivado", "años de alquiler (ratio)"),
                  ("esfuerzo_aprox", "derivado", "años de PIB per cápita (proxy)")]:
    reg("prov_a", nm, "derivado", "—", "—", u, "anual", "cociente", "derivado",
        "vivienda de 90 m² (supuesto); renta disponible provincial NO existe en v2" if nm == "esfuerzo_aprox"
        else "p_tasado / (12 × serpavi_mediana_vc); años con ambos datos")
ann["vut_viviendas_metodo"] = np.where(ann.get("vut_viviendas", pd.Series(dtype=float)).notna(), "observado", "")
ann = ann.merge(PROV_DF, on="cod_prov", how="left")
ANNUAL_LEVEL = [c for c in ann.columns if c not in ("cod_prov", "anio", "provincia", "cod_ccaa") and not c.endswith("_metodo")]
ANNUAL_LEVEL = [c for c in ANNUAL_LEVEL if pd.api.types.is_numeric_dtype(ann[c])]
ann = add_logs(ann, ANNUAL_LEVEL, "cod_prov", quarterly=False)
ann = ann[["anio", "cod_prov", "provincia", "cod_ccaa"] + [c for c in ann.columns if c not in ("anio", "cod_prov", "provincia", "cod_ccaa")]]
ann = ann.sort_values(["cod_prov", "anio"]).reset_index(drop=True)
assert not ann.duplicated(["cod_prov", "anio"]).any()
PANEL_PROV_A = ann
reg("prov_a", "agregados anuales de trimestrales", "derivado", "panel_prov_q", "—", "según variable", "anual",
    "media (p_tasado, p_suelo, ipc, EPA, zona) o suma (ETDP, hipotecas, MIVAU); NaN si falta un trimestre",
    "agregado_media / agregado_suma", "stock (pob_*): valor 1 enero (T1); vut: agosto (T3); inmig: suma S1+S2")

# ---------------------------------------------------------------- MUNICIPAL ANUAL
MUN = {}   # nombre -> wide (cod_muni x anio)


def mun_annual(df, val, how):
    return df


# SERPAVI municipal (codigo 5 dígitos)
spm = sp[sp.nivel == "MUN"].copy()
spm["anio"] = pd.to_datetime(spm.fecha).dt.year
spm["cod_muni"] = spm.codigo.str.zfill(5)
SER = {}
for ten in ["VC", "VU"]:
    m = spm[(spm.tipologia == ten) & (spm.variable == "alquiler_m2") & (spm.estadistico == "mediana")]
    SER[f"serpavi_mediana_{ten.lower()}"] = m.drop_duplicates(["cod_muni", "anio"])[["cod_muni", "anio", "valor"]].rename(columns={"valor": f"serpavi_mediana_{ten.lower()}"})
    m = spm[(spm.tipologia == ten) & (spm.variable == "n_contratos")]
    SER[f"serpavi_n_{ten.lower()}"] = m.drop_duplicates(["cod_muni", "anio"])[["cod_muni", "anio", "valor"]].rename(columns={"valor": f"serpavi_n_{ten.lower()}"})

# p_tasado municipal (>25.000 hab.; media anual de trimestres disponibles)
vtm = num(rd("mivau_valor_tasado_municipios.csv"))
vtm = vtm[vtm.serie.str.startswith("valor_tasado_mun_")].copy()
vtm["cod_muni"] = [muni_code(n, h) for n, h in zip(vtm.territorio, vtm.provincia)]
vtm["anio"] = pd.to_datetime(vtm.fecha).dt.year
mu_pt = vtm.dropna(subset=["cod_muni"]).groupby(["cod_muni", "anio"]).valor.agg(["mean", "count"]).reset_index()
mu_pt = mu_pt[mu_pt["count"] >= 1].rename(columns={"mean": "p_tasado"})
log(f"  p_tasado municipal: {vtm.cod_muni.nunique()} munis con código, {vtm.cod_muni.isna().sum()} filas sin casar")

# trans_total municipal (suma de 4 trimestres)
trm = num(rd("mivau_transacciones_municipios.csv"))
trm = trm[trm.serie.str.startswith("tx_municipio_")].copy()
trm["cod_muni"] = [muni_code(n, h) for n, h in zip(trm.territorio, trm.provincia)]
trm["anio"] = pd.to_datetime(trm.fecha).dt.year
tg = trm.dropna(subset=["cod_muni"]).groupby(["cod_muni", "anio"]).valor.agg(["sum", "count"]).reset_index()
tg = tg[tg["count"] == 4].rename(columns={"sum": "trans_total"})[["cod_muni", "anio", "trans_total"]]

# VUT municipal (INE 39363): observación más cercana a agosto (máx. 3 meses) de cada año
vm = num(rd("ine_v2_vut.csv"))
vm = vm[(vm.nivel == "municipio") & (vm.medida == "viviendas_turisticas")].copy()
vm["cod_muni"] = [muni_code(n) for n in vm.territorio]
vm["fd"] = pd.to_datetime(vm.fecha)
vm["anio"] = vm.fd.dt.year
vm["dist"] = (vm.fd.dt.month - 8).abs()
vm = vm.dropna(subset=["cod_muni"])
vm = vm[vm.dist <= 3].sort_values(["cod_muni", "anio", "dist"]).drop_duplicates(["cod_muni", "anio"])
VUT_M = vm[["cod_muni", "anio", "valor"]].rename(columns={"valor": "vut_viviendas"})
log(f"  VUT municipal: {vm.cod_muni.nunique()} munis casados (de {vm.territorio.nunique()} nombres)")

# Catastro uu residenciales (código directo)
UU = cat[["cod_muni", "anio", "valor"]].rename(columns={"valor": "uu_residenciales"}).drop_duplicates(["cod_muni", "anio"])

# IPVA municipal (INE 59060 Total; por nombre)
ipm = num(rd("ine_v2_ipva.csv"))
ipm = ipm[(ipm.nivel == "municipio") & (ipm.tabla == "59060") & (ipm.desglose == "Total")].copy()
ipm["cod_muni"] = [muni_code(n) for n in ipm.territorio]
ipm["anio"] = pd.to_datetime(ipm.fecha).dt.year
IPVA_M = {}
for med, nm in [("IPVA_indice", "ipva_indice"), ("IPVA_variacion_anual", "ipva_var")]:
    d = ipm[ipm.medida == med].dropna(subset=["cod_muni"]).drop_duplicates(["cod_muni", "anio"])
    IPVA_M[nm] = d[["cod_muni", "anio", "valor"]].rename(columns={"valor": nm})
log(f"  IPVA municipal: {ipm.cod_muni.notna().sum()} filas casadas; sin casar: {ipm.cod_muni.isna().sum()}")

# Zona tensionada municipal: fracción de días del año vigente (años >= 2024; munis fuera del fichero = 0)
ZM_ROWS = []
for y in (2024, 2025):
    d0, d1 = pd.Timestamp(f"{y}-01-01"), pd.Timestamp(f"{y}-12-31")
    ndays = (d1 - d0).days + 1
    days = pd.date_range(d0, d1, freq="D")
    for cm, g_ in zon.groupby("cod_muni"):
        act = np.zeros(len(days), dtype=bool)
        for _, r in g_.iterrows():
            ini = r.ini
            fin = r.fin if pd.notna(r.fin) else pd.Timestamp("2100-01-01")
            act |= (days >= ini) & (days <= fin)
        ZM_ROWS.append((cm, y, act.sum() / ndays))
ZM = pd.DataFrame(ZM_ROWS, columns=["cod_muni", "anio", "zona_tensionada"])

# Municipios con al menos una variable de precio o alquiler
pr_muni = set(SER["serpavi_mediana_vc"].cod_muni) | set(SER["serpavi_mediana_vu"].cod_muni) | set(mu_pt.cod_muni)
MUN_SET = sorted(pr_muni)
log(f"Municipios con precio/alquiler: {len(MUN_SET)}")
MA = pd.MultiIndex.from_product([MUN_SET, range(2002, 2026)], names=["cod_muni", "anio"]).to_frame(index=False)
for df_ in [SER["serpavi_mediana_vc"], SER["serpavi_mediana_vu"], SER["serpavi_n_vc"], SER["serpavi_n_vu"],
            mu_pt[["cod_muni", "anio", "p_tasado"]], tg, VUT_M, UU, IPVA_M["ipva_indice"], IPVA_M["ipva_var"], ZM]:
    dd = df_.copy()
    dd.columns = ["cod_muni", "anio"] + [c for c in dd.columns if c not in ("cod_muni", "anio")]
    MA = MA.merge(dd, on=["cod_muni", "anio"], how="left")
MA = MA[MA.anio.between(2002, 2025)]
MA = MA.drop(columns=[c for c in MA.columns if c == "count"], errors="ignore")
# zona: NaN antes de 2024 (ya lo es por construcción), 0 para munis con datos (fuera del fichero)
MA["zona_tensionada"] = np.where(MA.anio >= 2024, MA["zona_tensionada"].fillna(0.0), np.nan)
con_precio = MA.loc[MA[["serpavi_mediana_vc", "serpavi_mediana_vu", "p_tasado"]].notna().any(axis=1), "cod_muni"].unique()
MA = MA[MA.cod_muni.isin(con_precio)]
MA["municipio"] = MA.cod_muni.map(MUNI_NAME)
MA["cod_prov"] = MA.cod_muni.map(MUNI_PROV)
MA["metodo_p_tasado"] = np.where(MA.p_tasado.notna(), "agregado_media", "")
MA["metodo_trans_total"] = np.where(MA.trans_total.notna(), "agregado_suma", "")
MA["metodo_vut"] = np.where(MA.vut_viviendas.notna(), "observado", "")
MA = MA.rename(columns={"vut_viviendas": "vut_viviendas"})
MUN_LEVEL = ["serpavi_mediana_vc", "serpavi_mediana_vu", "serpavi_n_vc", "serpavi_n_vu", "p_tasado", "trans_total",
             "vut_viviendas", "uu_residenciales", "ipva_indice", "ipva_var"]
MA = add_logs(MA, MUN_LEVEL, "cod_muni", quarterly=False)
MA = MA[["cod_muni", "municipio", "cod_prov", "anio"] + [c for c in MA.columns if c not in ("cod_muni", "municipio", "cod_prov", "anio")]]
MA = MA.sort_values(["cod_muni", "anio"]).reset_index(drop=True)
assert not MA.duplicated(["cod_muni", "anio"]).any()
PANEL_MUNI_A = MA
for nm, n_, u, fu in [
    ("serpavi_mediana_vc", "observado", "€/m²/mes", "SERPAVI municipal (AEAT IRPF)"),
    ("serpavi_mediana_vu", "observado", "€/m²/mes", "SERPAVI municipal (AEAT IRPF)"),
    ("serpavi_n_vc", "observado", "inmuebles", "SERPAVI municipal"),
    ("serpavi_n_vu", "observado", "inmuebles", "SERPAVI municipal"),
    ("p_tasado", "agregado_media", "€/m²", "MIVAU valor tasado municipios >25.000 hab. (media de trimestres disponibles)"),
    ("trans_total", "agregado_suma", "transacciones", "MIVAU transacciones municipales (solo años con 4 trimestres)"),
    ("vut_viviendas", "observado", "número", "INE VTE municipal (mes más cercano a agosto, máx. 3 meses)"),
    ("uu_residenciales", "observado", "unidades urbanas residenciales", "Catastro (periodo N = stock 31-dic de N-1)"),
    ("ipva_indice", "observado", "índice", "INE IPVA municipal (59060)"),
    ("ipva_var", "observado", "% var. anual", "INE IPVA municipal (59060)"),
    ("zona_tensionada", "derivado", "fracción de días del año", "BOE zonas tensionadas; munis fuera del fichero = 0 desde 2024")]:
    reg("muni_a", nm, fu, "varios (ver docs)", "—", u, "anual", "según fuente", n_, "")
reg("muni_a", "municipio / cod_muni", "INE diccionario municipios 2026 (ine_diccionario_municipios_2026.xlsx)",
    "ine_diccionario_municipios_2026.xlsx", "—", "código", "—", "casado por nombre si no hay código",
    "observado", f"casados por nombre: {_MATCH_LOG['casado_unico']} únicos + {_MATCH_LOG['casado_con_provincia']} con provincia; no casados: {len(_MATCH_LOG['no_casado'])}; ambiguos: {len(_MATCH_LOG['ambiguo'])}")

# ---------------------------------------------------------------- UE (Eurostat, BIS, OCDE, BCE)
GEO_ISO3 = {"AUT": "AT", "BEL": "BE", "CZE": "CZ", "DNK": "DK", "EST": "EE", "FIN": "FI", "FRA": "FR", "DEU": "DE",
            "GRC": "EL", "HUN": "HU", "ISL": "IS", "IRL": "IE", "ITA": "IT", "LVA": "LV", "LTU": "LT", "LUX": "LU",
            "NLD": "NL", "NOR": "NO", "POL": "PL", "PRT": "PT", "SVK": "SK", "SVN": "SI", "ESP": "ES", "SWE": "SE",
            "CHE": "CH", "GBR": "UK", "TUR": "TR"}
GEO_BIS = {"GB": "UK", "GR": "EL"}


def ue_q(df_geo_period: pd.DataFrame) -> pd.DataFrame:
    return df_geo_period


UE_GEO = sorted({g for g in pd.read_csv(RAW / "eu_hpi.csv", dtype=str, usecols=["geo"]).geo.unique()
                 if not str(g).startswith("EU") and not str(g).startswith("EA")} | {"EL"})
log(f"UE: {len(UE_GEO)} geos Eurostat")
UE_A = pd.MultiIndex.from_product([UE_GEO, AY], names=["geo", "anio"]).to_frame(index=False)
UE_Q = pd.MultiIndex.from_product([UE_GEO, QL], names=["geo", "trimestre"]).to_frame(index=False)

UE_SER: dict[str, pd.DataFrame] = {}   # nombre -> long (geo, periodo_str, valor, metodo) con periodo Q o A
UE_META: dict[str, tuple] = {}


def ue_put(nm, long_q=None, long_a=None, meta=()):
    UE_SER[nm] = (long_q, long_a)
    UE_META[nm] = meta


# HPI Eurostat (trimestral I15_Q; anual I15_A_AVG)
ehp = num(rd("eu_hpi.csv"))
ehq = ehp[(ehp.unit == "I15_Q") & (ehp.purchase == "TOTAL")].assign(trimestre=lambda x: x.periodo.str.replace("-", ""))
eha = ehp[(ehp.unit == "I15_A_AVG") & (ehp.purchase == "TOTAL")].assign(anio=lambda x: x.periodo.astype(int))
ue_put("hpi", long_q=ehq[["geo", "trimestre", "valor"]].assign(metodo="observado"),
       long_a=eha[["geo", "anio", "valor"]].assign(metodo="observado"),
       meta=("Eurostat prc_hpi (índice precios vivienda compra, total)", "prc_hpi_q / prc_hpi_a", "I15 (2015=100)"))

# BIS (nominal, trimestral, 2010=100) -> columna alternativa hpi_bis
bis = num(rd("bis_rpp.csv"))
bis = bis[bis.precio == "nominal"].copy()
bis["geo"] = bis.territorio.replace(GEO_BIS)
bis["trimestre"] = bis.periodo.str.replace("-", "")
bis = bis[bis.geo.isin(UE_GEO)]
bis_a = bis.assign(anio=bis.trimestre.str[:4].astype(int)).groupby(["geo", "anio"]).valor.agg(["mean", "count"]).reset_index()
bis_a = bis_a[bis_a["count"] == 4]
ue_put("hpi_bis", long_q=bis[["geo", "trimestre", "valor"]].assign(metodo="observado"),
       long_a=bis_a.rename(columns={"mean": "valor"})[["geo", "anio", "valor"]].assign(metodo="agregado_media"),
       meta=("BIS WS_SPP precios residenciales nominal", "WS_SPP", "índice 2010=100"))

# OCDE (ISO3): HPI nominal, precio/renta (HPI_YDH), precio/alquiler (HPI_RPI)
oc = num(rd("oecd_house_prices.csv"))
oc["geo"] = oc.territorio.map(GEO_ISO3)
oc = oc.dropna(subset=["geo"])
oc_q = oc[oc.frecuencia == "Q"].assign(trimestre=lambda x: x.periodo.str.replace("-", ""))
oc_a = oc[oc.frecuencia == "A"].assign(anio=lambda x: x.periodo.str[:4].astype(int))
for med, nm in [("HPI", "hpi_oecd"), ("HPI_YDH", "ocde_precio_ingreso"), ("HPI_RPI", "ocde_precio_alquiler")]:
    ue_put(nm, long_q=oc_q[oc_q.medida == med][["geo", "trimestre", "valor"]].assign(metodo="observado"),
           long_a=oc_a[oc_a.medida == med][["geo", "anio", "valor"]].assign(metodo="observado"),
           meta=(f"OCDE {med}", "DF_HOUSE_PRICES", "índice / ratio"))

# Alquiler HICP CP041 (mensual I15 -> trimestre; anual INX_A_AVG)
er = num(rd("eu_hicp_rent.csv"))
erm = er[(er.unit == "I15") & (er.freq == "M")].copy()
erm["trimestre"] = pd.PeriodIndex(erm.periodo, freq="M").asfreq("Q").astype(str)
gq = erm.groupby(["geo", "trimestre"]).valor.agg(["mean", "count"]).reset_index()
gq = gq[gq["count"] == 3]
era = er[(er.unit == "INX_A_AVG") & (er.freq == "A")].assign(anio=lambda x: x.periodo.astype(int))
ue_put("alquiler_hicp", long_q=gq.rename(columns={"mean": "valor"})[["geo", "trimestre", "valor"]].assign(metodo="agregado_media"),
       long_a=era[["geo", "anio", "valor"]].assign(metodo="observado"),
       meta=("Eurostat HICP CP041 alquiler", "prc_hicp_midx/aind", "índice"))

# Permisos (BPRM_DW): trimestral índice SCA; anual miles de viviendas (THS)
ep2 = num(rd("eu_permits.csv"))
pq = ep2[(ep2.indic_bt == "BPRM_DW") & (ep2.unit == "I21") & (ep2.freq == "Q")].assign(trimestre=lambda x: x.periodo.str.replace("-", ""))
pa = ep2[(ep2.indic_bt == "BPRM_DW") & (ep2.unit == "THS") & (ep2.freq == "A")].assign(anio=lambda x: x.periodo.astype(int))
ue_put("permisos", long_q=pq[["geo", "trimestre", "valor"]].assign(metodo="observado"),
       long_a=pa[["geo", "anio", "valor"]].assign(metodo="observado"),
       meta=("Eurostat permisos de construcción de viviendas", "sts_cobp_a / q", "THS viviendas (A); índice 2021=100 (Q)"))

# Población y migración (demo_pjan total; migr_imm1ctz total) -> inmigración por 1.000 hab.
ePop = num(rd("eu_migr_pop.csv"))
pop = ePop[ePop.serie.str.startswith("demo_pjan|A|NR|TOTAL|T|")].assign(anio=lambda x: x.periodo.astype(int))
mig = ePop[ePop.serie.str.startswith("migr_imm1ctz|A|TOTAL|REACH|TOTAL|NR|T|")].assign(anio=lambda x: x.periodo.astype(int))
pop_a = pop[["geo", "anio", "valor"]].drop_duplicates(["geo", "anio"])
mig_a = mig[["geo", "anio", "valor"]].drop_duplicates(["geo", "anio"]).rename(columns={"valor": "mig"})
mx = pop_a.merge(mig_a, on=["geo", "anio"], how="inner")
mx["valor"] = mx.mig / mx.valor * 1000
ue_put("inmig_por_1000", long_q=None, long_a=mx[["geo", "anio", "valor"]].assign(metodo="derivado"),
       meta=("Eurostat migr_imm1ctz / demo_pjan × 1000", "migr_imm1ctz, demo_pjan", "por 1.000 hab."))
ue_put("poblacion", long_q=None, long_a=pop_a[["geo", "anio", "valor"]].assign(metodo="observado"),
       meta=("Eurostat demo_pjan población 1 enero, total", "demo_pjan", "personas"))

# Tipos: MIR hipotecario (BCE, solo euro; mensual -> trimestre); tipo largo (anual)
rt = rd("eu_rates.csv")
rt = num(rt)
rtm = rt[rt.serie.str.startswith("MIR.M.")].copy()
rtm["geo"] = rtm.serie.str.split(".").str[2]
rtm["trimestre"] = pd.PeriodIndex(rtm.periodo, freq="M").asfreq("Q").astype(str)
gm = rtm.groupby(["geo", "trimestre"]).valor.agg(["mean", "count"]).reset_index()
gm = gm[gm["count"] == 3].rename(columns={"mean": "valor"})
rtl = rt[rt.serie.str.startswith("irt_lt_mcby_a")].copy()
rtl["anio"] = rtl.periodo.astype(int)
rta = rtm.assign(anio=rtm.periodo.str[:4].astype(int)).groupby(["geo", "anio"]).valor.agg(["mean", "count"]).reset_index()
rta = rta[rta["count"] == 12].rename(columns={"mean": "valor"})[["geo", "anio", "valor"]].assign(metodo="agregado_media")
ue_put("tipo_hip_mir", long_q=gm[["geo", "trimestre", "valor"]].assign(metodo="agregado_media"),
       long_a=rta,
       meta=("BCE MIR tipo hipotecario compra vivienda (solo zona euro)", "MIR.M.<geo>.B.A2C.AM.R.A.2250.EUR.N", "% anual"))
ue_put("tipo_largo", long_q=None, long_a=rtl[["geo", "anio", "valor"]].assign(metodo="observado"),
       meta=("Eurostat/BCE tipo de interés largo plazo (irt_lt_mcby_a)", "irt_lt_mcby_a", "% anual"))

# Renta bruta disponible hogares (B6G, nasa_10_nf_tr) y empleo (EMP_LFS 15-64)
inc = num(rd("eu_income_emp.csv"))
ren = inc[(inc.na_item == "B6G") & (inc.unit == "CP_MEUR")].assign(anio=lambda x: x.periodo.astype(int))
emp = inc[(inc.indic_em == "EMP_LFS") & (inc.sex == "T") & (inc.age == "Y15-64")].assign(anio=lambda x: x.periodo.astype(int))
ue_put("renta_bruta_disp", long_q=None, long_a=ren[["geo", "anio", "valor"]].drop_duplicates(["geo", "anio"]).assign(metodo="observado"),
       meta=("Eurostat nasa_10_nf_tr, código B6G (renta disponible bruta hogares, S14_S15)", "nasa_10_nf_tr", "millones € corrientes"))
ue_put("empleo", long_q=None, long_a=emp[["geo", "anio", "valor"]].drop_duplicates(["geo", "anio"]).assign(metodo="observado"),
       meta=("Eurostat lfsi_emp_a empleo 15-64", "lfsi_emp_a", "miles de personas"))

# HICP general (anual)
eh = num(rd("eu_hicp.csv"))
eh = eh[(eh.coicop == "CP00") & (eh.unit == "INX_A_AVG")].assign(anio=lambda x: x.periodo.astype(int))
ue_put("hicp_general", long_q=None, long_a=eh[["geo", "anio", "valor"]].assign(metodo="observado"),
       meta=("Eurostat HICP general CP00 (índice medio anual)", "prc_hicp_aind", "índice"))

# Armado de paneles UE
def ue_assemble(freq: str) -> pd.DataFrame:
    base_ = (UE_A if freq == "A" else UE_Q).copy()
    for nm, (lq, la) in UE_SER.items():
        if freq == "A":
            src = la
            if src is None:
                continue
            m_ = src.drop_duplicates(["geo", "anio"])
            base_ = base_.merge(m_[["geo", "anio", "valor", "metodo"]].rename(columns={"valor": nm, "metodo": nm + "_metodo"}),
                                on=["geo", "anio"], how="left")
        else:
            if lq is not None:
                m_ = lq.drop_duplicates(["geo", "trimestre"])
                base_ = base_.merge(m_[["geo", "trimestre", "valor", "metodo"]].rename(columns={"valor": nm, "metodo": nm + "_metodo"}),
                                    on=["geo", "trimestre"], how="left")
            elif la is not None:   # anual -> asignado a cada trimestre del año (sin interpolar)
                base_["anio"] = base_.trimestre.str[:4].astype(int)
                m_ = la.drop_duplicates(["geo", "anio"])
                base_ = base_.merge(m_[["geo", "anio", "valor"]].rename(columns={"valor": nm}), on=["geo", "anio"], how="left")
                base_[nm + "_metodo"] = np.where(base_[nm].notna(), "anual_asignado", "")
                base_ = base_.drop(columns="anio")
    if freq == "Q":
        base_["anio"] = base_.trimestre.str[:4].astype(int)
    return base_


UE_A_DF = ue_assemble("A")
UE_Q_DF = ue_assemble("Q")
LEVEL_UE = [c for c in UE_A_DF.columns if c in UE_SER and pd.api.types.is_numeric_dtype(UE_A_DF[c])]
for dfu in (UE_A_DF, UE_Q_DF):
    for nm in list(UE_SER):
        if nm + "_metodo" in dfu:
            dfu[nm + "_interp"] = False
# derivados UE: precio/alquiler y precio/renta ya OCDE; añadimos logs
UE_A_DF = add_logs(UE_A_DF, [c for c in LEVEL_UE if c in UE_A_DF], "geo", quarterly=False)
LEVEL_UE_Q = [c for c in UE_Q_DF.columns if c in UE_SER and pd.api.types.is_numeric_dtype(UE_Q_DF[c])]
UE_Q_DF = add_logs(UE_Q_DF, LEVEL_UE_Q, "geo", quarterly=True)
UE_A_DF = UE_A_DF.sort_values(["geo", "anio"]).reset_index(drop=True)
UE_Q_DF = UE_Q_DF.sort_values(["geo", "trimestre"]).reset_index(drop=True)
for nm, meta in UE_META.items():
    reg("ue_a/q", nm, meta[0], "eu_*.csv / bis_rpp.csv / oecd_house_prices.csv", meta[1], meta[2],
        "anual / trimestral", "según fuente", "observado / agregado_media / anual_asignado", "UE geo ISO2 Eurostat (EL, UK)")

# ---------------------------------------------------------------- EVENTOS
ev = rd("v2_eventos_politica.csv")
ev = ev[ev.estado == "VERIFICADO"].copy()
ev["ini"] = pd.to_datetime(ev.fecha_entrada_vigor)
ev["fin"] = pd.to_datetime(ev.fecha_fin)
rows = []
for q in QL:
    per = pd.Period(q, freq="Q")
    qs, qe = per.start_time, per.end_time.normalize()
    for _, r in ev.iterrows():
        act = (r.ini <= qe) and (pd.isna(r.fin) or r.fin >= qs)
        rows.append(dict(trimestre=q, evento_id=r.id, nombre=r.nombre, ambito=r.ambito, mercado=r.mercado,
                         codigos_ine_ccaa=r.codigos_ine_ccaa, codigos_ine_provincia=r.codigos_ine_provincia,
                         dummy_vigente=int(bool(act))))
EVQ = pd.DataFrame(rows)
reg("eventos", "dummy_vigente", "BOE (eventos verificados, estado VERIFICADO)", "v2_eventos_politica.csv", "—",
    "0/1", "trimestral", "vigencia en algún día del trimestre", "derivado",
    f"{ev.shape[0]} eventos verificados de {len(rd('v2_eventos_politica.csv'))}; no verificados excluidos")

# ---------------------------------------------------------------- NACIONAL v2
nac = pd.read_csv(V1_NAC, dtype={"trimestre": str})
nac = nac.copy()
_nat_ser = {}
ETQ = et_all[(et_all.nivel == "nacional") & (et_all.desglose == "total")].copy()
g_e = monthly_to_q(ETQ[["fecha", "valor"]].assign(k="n"), ["k"], "sum").set_index("trimestre")["valor"].reindex(QL)
hpn = hp_all[(hp_all.nivel == "nacional")]
g_hn = monthly_to_q(hpn[hpn.medida == "hipotecas_viviendas_numero"][["fecha", "valor"]].assign(k="n"), ["k"], "sum").set_index("trimestre")["valor"]
g_hi = monthly_to_q(hpn[hpn.medida == "hipotecas_viviendas_importe"][["fecha", "valor"]].assign(k="n"), ["k"], "sum").set_index("trimestre")["valor"]
extra = pd.DataFrame(index=QL)
extra["compraventas_nac"] = g_e.reindex(QL)
extra["hipotecas_n_nac"] = g_hn.reindex(QL)
extra["hipotecas_importe_nac"] = g_hi.reindex(QL)
for k, s in NAC_BDE_EXTRA.items():
    extra[k] = s.reindex(QL)
extra_metodo = {k: ("agregado_suma" if not k.startswith("saldo") else "fin_periodo") for k in extra.columns}
nac = nac.set_index("trimestre")
for c in extra.columns:
    nac[c] = extra[c].reindex(nac.index)
    nac[c + "_metodo"] = np.where(nac[c].notna(), extra_metodo[c], "")
    nac[c + "_interp"] = False
nac["coste_uso_aprox"] = (pd.to_numeric(nac["tipo_hip"], errors="coerce") -
                          pd.to_numeric(nac["inflacion_deflactor"], errors="coerce").rolling(4, min_periods=4).mean())
nac["coste_uso_aprox_metodo"] = np.where(nac["coste_uso_aprox"].notna(), "derivado", "")
nac["coste_uso_aprox_interp"] = False
lnipv = np.log(pd.to_numeric(nac["ipv"], errors="coerce").where(lambda s: s > 0))
lnipc = np.log(pd.to_numeric(nac["ipc_alquiler"], errors="coerce").where(lambda s: s > 0))
nac["ratio_precio_alquiler_idx"] = lnipv - lnipc
nac["ratio_precio_alquiler_idx_metodo"] = np.where(nac["ratio_precio_alquiler_idx"].notna(), "derivado", "")
nac["ratio_precio_alquiler_idx_interp"] = False
ev_nac = EVQ[EVQ.ambito == "nacional"].pivot_table(index="trimestre", columns="evento_id", values="dummy_vigente", aggfunc="max")
for eid in ev_nac.columns:
    nac[f"ev_{eid}"] = ev_nac[eid].reindex(nac.index).fillna(0).astype(int)
nac = nac.reset_index()
reg("nacional_v2", "copia v1 nacional_q", "v1 (ver docs/diccionario_variables.md)", "data/processed/nacional_q.csv", "—",
    "según v1", "trimestral", "según v1", "según v1", "todas las columnas de v1 copiadas tal cual")
reg("nacional_v2", "compraventas_nac / hipotecas_n_nac / hipotecas_importe_nac", "INE ETDP (6150) / INE HPT (76317) nacional",
    "ine_v2_etdp_prov.csv / ine_v2_hipotecas_prov.csv", "6150 / 76317", "número / miles € (NO VERIFICADO)",
    "mensual -> trimestral", "suma de 3 meses", "agregado_suma", "serie nacional (no suma de provincias)")
reg("nacional_v2", "credito_*_bde / saldo_*_bde", "BdE be1916/be1906", "bde_credito_finalidad.csv", "be1916",
    "Millones €", "mensual", "flujo: suma; saldo: fin de trimestre", "agregado_suma / fin_periodo", "")
reg("nacional_v2", "eventos ev_<ID>", "derivado de eventos_q", "v2_eventos_politica.csv", "—", "0/1",
    "trimestral", "vigencia", "derivado", "solo eventos VERIFICADOS de ámbito nacional")

# ---------------------------------------------------------------- CONTROLES
def check(name, got, exp, tol=1e-6):
    ok = (np.isnan(got) and np.isnan(exp)) or (not np.isnan(got) and np.isclose(got, exp, rtol=tol, atol=1e-6))
    CHECKS.append(f"{'OK ' if ok else 'FALLO'} {name}: salida={got} raw={exp}")
    if not ok:
        raise SystemExit(f"Control fallido: {name}: salida={got} raw={exp}")


_pq = PANEL_PROV_Q.set_index(["cod_prov", "trimestre"])
_r = epa[(epa.nivel == "provincia") & (epa.codigo == "28") & (epa.medida == "EPA_ocupados") & (epa.fecha.str.startswith("2002-01"))]
check("EPA ocupados Madrid 2002T1", float(_pq.loc[("28", "2002Q1"), "ocupados"]), float(_r.valor.iloc[0]))
_r = et[(et.codigo == "28") & (et.desglose == "total") & (et.fecha.isin(["2019-01-01", "2019-02-01", "2019-03-01"]))]
check("ETDP total Madrid 2019T1 (suma 3 meses)", float(_pq.loc[("28", "2019Q1"), "compraventas_total"]), float(_r.valor.sum()))
_r = pe[(pe.codigo == "52") & (pe.desglose == "nacionalidad=Total; edad=Todas") & (pe.fecha == "2010-01-01")]
check("ECP pob_total Melilla 1-ene-2010 -> 2010T1", float(_pq.loc[("52", "2010Q1"), "pob_total"]), float(_r.valor.iloc[0]))
_r = ipc[(ipc.cod == "41") & (ipc.fecha.str[:7].isin(["2019-01", "2019-02", "2019-03"]))]
check("IPC alquiler Sevilla 2019T1 (media 3 meses)", float(_pq.loc[("41", "2019Q1"), "ipc_alquiler"]), float(_r.valor.mean()))
_r = hp[(hp.cod == "29") & (hp.medida == "hipotecas_viviendas_numero") & (hp.fecha.isin(["2021-04-01", "2021-05-01", "2021-06-01"]))]
check("HPT nº hipotecas Málaga 2021T2 (suma)", float(_pq.loc[("29", "2021Q2"), "hipotecas_n"]), float(_r.valor.sum()))
_r = vt[(vt.cod == "46") & (vt.fecha == "2015-01-01")]
check("Valor tasado Valencia 2015T1", float(_pq.loc[("46", "2015Q1"), "p_tasado"]), float(_r.valor.iloc[0]))
_ann = PANEL_PROV_A.set_index(["cod_prov", "anio"])
_r = sp[(sp.nivel == "PROV") & (sp.codigo == "28") & (sp.tipologia == "VC") & (sp.variable == "alquiler_m2") & (sp.estadistico == "mediana") & (sp.fecha.str.startswith("2019"))]
check("SERPAVI mediana VC Madrid 2019 (provincia)", float(_ann.loc[("28", 2019), "serpavi_mediana_vc"]), float(_r.valor.iloc[0]))

# ---------------------------------------------------------------- ESCRITURA
DOCS.mkdir(parents=True, exist_ok=True)
outs = {}
outs["panel_prov_q"] = write_csv(PANEL_PROV_Q, "panel_prov_q")
outs["panel_prov_a"] = write_csv(PANEL_PROV_A, "panel_prov_a")
outs["panel_muni_a"] = write_csv(PANEL_MUNI_A, "panel_muni_a")
outs["panel_ue_a"] = write_csv(UE_A_DF, "panel_ue_a")
outs["panel_ue_q"] = write_csv(UE_Q_DF, "panel_ue_q")
outs["nacional_q_v2"] = write_csv(nac, "nacional_q_v2")
outs["eventos_q"] = write_csv(EVQ, "eventos_q")

# comprobaciones de clave y filas
dup = {"panel_prov_q": PANEL_PROV_Q.duplicated(["cod_prov", "trimestre"]).sum(),
       "panel_prov_a": PANEL_PROV_A.duplicated(["cod_prov", "anio"]).sum(),
       "panel_muni_a": PANEL_MUNI_A.duplicated(["cod_muni", "anio"]).sum(),
       "panel_ue_a": UE_A_DF.duplicated(["geo", "anio"]).sum(),
       "panel_ue_q": UE_Q_DF.duplicated(["geo", "trimestre"]).sum(),
       "nacional_q_v2": nac.duplicated(["trimestre"]).sum(),
       "eventos_q": EVQ.duplicated(["trimestre", "evento_id"]).sum()}
FILAS = {"panel_prov_q": PANEL_PROV_Q, "panel_prov_a": PANEL_PROV_A, "panel_muni_a": PANEL_MUNI_A,
         "panel_ue_a": UE_A_DF, "panel_ue_q": UE_Q_DF, "nacional_q_v2": nac, "eventos_q": EVQ}


# ---------------------------------------------------------------- DICCIONARIO (generado)
def cobertura(df: pd.DataFrame, unit_col: str, time_col: str, var: str) -> tuple:
    d = df[df[var].notna()]
    if d.empty:
        return ("—", "—", 0)
    t = sorted(d[time_col].astype(str).unique())
    return (t[0], t[-1], d[unit_col].nunique())


lines = ["# Diccionario de variables v2 (generado por src/build_dataset_v2.py)", "",
         "Generado automáticamente. Fuentes en data/raw; ningún dato de PDF/OCR no validado entra en el panel principal.", "",
         "Convenciones: `<var>_metodo` ∈ {observado, agregado_media, agregado_suma, fin_periodo, escalonado, "
         "interpolado_loglineal, anual_asignado, semestral_asignado, derivado}; `<var>_interp` = TRUE solo si "
         "interpolado_loglineal (entre dos observaciones). Huecos al final y fuera de rango = NaN.", "",
         "## Registro de variables", "",
         "| panel | variable | fuente | archivo raw | tabla | unidad | frecuencia original | agregación | método | notas |",
         "|---|---|---|---|---|---|---|---|---|---|"]
for r in REG:
    lines.append("| " + " | ".join(str(r[k]).replace("|", "/") for k in
                                  ["panel", "var", "fuente", "archivo", "tabla", "unidad", "freq", "agreg", "metodo", "notas"]) + " |")
lines += ["", "## Cobertura y huecos por panel", ""]
cov_specs = [("panel_prov_q", PANEL_PROV_Q, "cod_prov", "trimestre"),
             ("panel_prov_a", PANEL_PROV_A, "cod_prov", "anio"),
             ("panel_muni_a", PANEL_MUNI_A, "cod_muni", "anio"),
             ("panel_ue_a", UE_A_DF, "geo", "anio"),
             ("panel_ue_q", UE_Q_DF, "geo", "trimestre")]
for pname, df, ucol, tcol in cov_specs:
    lines += [f"### {pname}", "", f"Filas: {len(df)}; unidades ({ucol}): {df[ucol].nunique()}; claves duplicadas: {int(dup[pname])}", "",
              "| variable | primer dato | último dato | nº unidades con dato | nº interpolaciones | nº NaN |",
              "|---|---|---|---|---|---|"]
    for c in df.columns:
        if c.endswith("_metodo") or c.endswith("_interp") or c.startswith(("ln_", "d_", "d4_")) or c in (ucol, tcol, "provincia", "municipio", "cod_ccaa", "cod_prov", "geo", "anio", "trimestre", "cod_muni"):
            continue
        if not pd.api.types.is_numeric_dtype(df[c]):
            continue
        p0, p1, nu = cobertura(df, ucol, tcol, c)
        ni = int(df[c + "_interp"].sum()) if (c + "_interp") in df else 0
        lines.append(f"| {c} | {p0} | {p1} | {nu} | {ni} | {int(df[c].isna().sum())} |")
    lines.append("")
lines += ["## Notas de limitación", "",
          "- Renta disponible provincial NO existe en los datos v2: el proxy de esfuerzo usa PIB per cápita.",
          "- IPVA provincial sin País Vasco ni Navarra (no publicado por la fuente).",
          "- Unidades de hipotecas_importe y pib_prov inferidas de FK_Unidad/magnitud: no verificadas contra metadatos.",
          "- zona_tensionada: NaN antes de 2024; municipios fuera del fichero BOE = 0 desde 2024 (supuesto).",
          "- Casamiento de municipios por nombre (VUT INE, IPVA municipal, valor tasado y transacciones MIVAU) con ine_diccionario_municipios_2026.xlsx: "
          f"{_MATCH_LOG['casado_unico']} casados por nombre único, {_MATCH_LOG['casado_con_provincia']} con ayuda de provincia, "
          f"{len(_MATCH_LOG['no_casado'])} nombres sin casar, {len(_MATCH_LOG['ambiguo'])} ambiguos (no casados).",
          f"- Nombres sin casar (muestra): {sorted(set(_MATCH_LOG['no_casado']))[:40]}",
          f"- Ambiguos (muestra): {_MATCH_LOG['ambiguo'][:20]}",
          "- coste_uso_aprox: aproximación sin impuestos, depreciación ni prima de riesgo (método derivado).",
          "- ratio_precio_alquiler_idx es una diferencia de logaritmos (índice), no un nivel.", ""]
(DOCS / "diccionario_v2.md").write_text("\n".join(lines), encoding="utf-8")

# ---------------------------------------------------------------- RESUMEN
print("\n== Filas y unidades por panel ==")
for k, df in FILAS.items():
    uc = {"panel_prov_q": "cod_prov", "panel_prov_a": "cod_prov", "panel_muni_a": "cod_muni",
          "panel_ue_a": "geo", "panel_ue_q": "geo", "nacional_q_v2": "trimestre", "eventos_q": "evento_id"}[k]
    print(f"  {k}: filas={len(df)} unidades={df[uc].nunique()} duplicados_clave={int(dup[k])}")
print("\n== Controles contra data/raw ==")
for c in CHECKS:
    print("  " + c)
print("\n== Cobertura clave (prov × trimestre) ==")
for v in ["p_tasado", "p_suelo", "ipc_alquiler", "compraventas_total", "hipotecas_n", "ocupados", "iniciadas_libres", "vut_viviendas", "pob_total", "inmig_flujo", "zona_tensionada_share"]:
    d = PANEL_PROV_Q[PANEL_PROV_Q[v].notna()]
    print(f"  {v}: {len(d)} celdas; {d.cod_prov.nunique()} provincias; {d.trimestre.min() if len(d) else '—'}–{d.trimestre.max() if len(d) else '—'}")
print("\n== Salidas ==")
for k, p in outs.items():
    print(f"  {p}")
print(f"  {DOCS / 'diccionario_v2.md'}")
print("\n== md5 ficheros v1 (data/processed/*.csv) ==")
_v1_after = {p.name: hashlib.md5(p.read_bytes()).hexdigest() for p in V1_FILES}
_same = _v1_after == V1_MD5_BEFORE
print(f"  {len(V1_MD5_BEFORE)} ficheros; idénticos antes/después: {_same}")
if not _same:
    raise SystemExit("ERROR: cambió un fichero v1 durante la ejecución")
print("\nFin build_dataset_v2.py")
