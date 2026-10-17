"""V15 fase 1.2 · Auditoría de datos, grupo DEMOGRAFÍA Y HOGARES (capa C4, DESCRIPTIVO, sin efectos estimados).

Fuentes: padrón continuo (provincia y municipio por nacionalidad, 2003-2022), censo anual (sección, municipio, provincia,
2021-2025), ECP (provincia y hogares nacionales/provinciales), EPA (hogares y población), censo 2021 (hogares), EVR/EMCR/EM
(migraciones), MNP, contabilidad V12-B1/B3 y padrón de València por barrio (2001-2026).
Cruces territoriales SOLO por código INE (provincia de 2 dígitos, municipio de 5, sección de 10, barrio de 9).
Determinista (SEED=20261010; no hay aleatoriedad). Uso: python3 src/v15/auditoria/demografia_hogares.py
Salida: output/v15/auditoria/demografia_hogares/ (CSV y resultado.json). Nada de terceros no redistribuibles: solo INE,
Catastro y Ajuntament de València (reutilización con cita) y agregados propios.
"""
from __future__ import annotations

import json
import re
import unicodedata
from functools import lru_cache
from pathlib import Path

import duckdb
import numpy as np
import pandas as pd
from shapely import wkb

SEED = 20261010
np.random.seed(SEED)
RAIZ = Path(__file__).resolve().parents[3]
RAW = RAIZ / "data" / "raw"
BASE = RAIZ / "data" / "base"
B1 = RAIZ / "output" / "v12" / "b1"
B3 = RAIZ / "output" / "v12" / "b3"
OUT = RAIZ / "output" / "v15" / "auditoria" / "demografia_hogares"
HECHOS = str(BASE / "hechos.parquet")
UMBRAL_Z = 5.0
MIN_OBS = 8
UMBRAL_RESIDUO_PCT = 1.0
COMPONENTES = ["crecimiento", "vegetativo", "saldo_exterior", "saldo_interior", "residuo"]
PERIODOS_REPARTO = {"2008-2013": (2008, 2013), "2014-2019": (2014, 2019), "2020-2021": (2020, 2021), "2022-2024": (2022, 2024)}
SIN_CATASTRO_ESTATAL = ("01", "20", "48", "31", "51", "52")

CON = duckdb.connect()


# ---------------------------------------------------------------- utilidades


def hechos(variable: str, nivel: str | None = None, desag: str | None = None, cols: str = "territorio_codigo, periodo, desagregacion, valor") -> pd.DataFrame:
    """Lectura agregada de la base: solo las columnas necesarias."""
    w = [f"variable = '{variable}'"]
    if nivel:
        w.append(f"nivel = '{nivel}'")
    if desag:
        w.append(f"desagregacion = '{desag}'")
    return CON.sql(f"SELECT {cols} FROM '{HECHOS}' WHERE " + " AND ".join(w)).df()


def zrob(x) -> tuple[float, float]:
    x = np.asarray(x, float)
    m = np.nanmedian(x)
    mad = np.nanmedian(np.abs(x - m))
    return float(m), float(1.4826 * mad)


def z_temporal(df: pd.DataFrame, grupo: list[str], col: str, min_obs: int = MIN_OBS) -> pd.DataFrame:
    """z robusto (mediana, MAD) dentro de cada grupo; NaN si el grupo es corto o MAD = 0."""
    d = df.copy()
    g = d.groupby(grupo)[col]
    d["mediana"] = g.transform("median")
    d["n_serie"] = g.transform("count")
    d["_dev"] = (d[col] - d["mediana"]).abs()
    d["mad_esc"] = 1.4826 * d.groupby(grupo)["_dev"].transform("median")
    d["z"] = np.where((d.n_serie >= min_obs) & (d.mad_esc > 0), (d[col] - d["mediana"]) / d["mad_esc"], np.nan)
    return d.drop(columns="_dev")


def z_corte(df: pd.DataFrame, grupo: list[str], col: str, min_n: int = 30) -> pd.DataFrame:
    return z_temporal(df, grupo, col, min_obs=min_n)


def norm(s: str) -> str:
    s = unicodedata.normalize("NFKD", str(s)).encode("ascii", "ignore").decode().lower().split("/")[0]
    return re.sub(r"[^a-z0-9 ]", " ", s).strip()


STOP = {"de", "del", "la", "las", "el", "los", "a", "y", "l", "comunidad", "region", "principado", "foral", "com"}


def pal(s: str) -> set[str]:
    return {w for w in norm(s).split() if w not in STOP}


def qidx(p: str) -> int:
    m = re.match(r"^(\d{4})T([1-4])$", str(p))
    return int(m.group(1)) * 4 + int(m.group(2)) - 1


def qlab(t: int) -> str:
    return f"{t // 4}T{t % 4 + 1}"


def corr(a: pd.Series, b: pd.Series, metodo: str = "pearson") -> float:
    d = pd.concat([pd.Series(a).reset_index(drop=True), pd.Series(b).reset_index(drop=True)], axis=1).dropna()
    if len(d) < 5 or d.iloc[:, 0].std() == 0 or d.iloc[:, 1].std() == 0:
        return float("nan")
    return float(d.iloc[:, 0].corr(d.iloc[:, 1], method=metodo))


def a_json(o):
    if isinstance(o, (np.floating, float)):
        return None if pd.isna(o) else float(o)
    if isinstance(o, np.integer):
        return int(o)
    if isinstance(o, np.bool_):
        return bool(o)
    return str(o)


def limpio(o):
    """Sustituye NaN/inf por None de forma recursiva (JSON válido)."""
    if isinstance(o, dict):
        return {str(k): limpio(v) for k, v in o.items()}
    if isinstance(o, (list, tuple)):
        return [limpio(v) for v in o]
    if isinstance(o, (np.floating, float)):
        return None if not np.isfinite(o) else float(o)
    if isinstance(o, np.integer):
        return int(o)
    if isinstance(o, np.bool_):
        return bool(o)
    return o


def guardar(df: pd.DataFrame, nombre: str) -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    df.to_csv(OUT / nombre, index=False, float_format="%.6g")


@lru_cache(maxsize=1)
def territorios() -> pd.DataFrame:
    return pd.read_parquet(BASE / "territorios.parquet")


@lru_cache(maxsize=1)
def prov_ccaa() -> dict:
    t = territorios()
    return t[t.nivel == "provincia"].set_index("territorio_codigo").cod_ccaa.to_dict()


@lru_cache(maxsize=1)
def padron_municipal() -> pd.DataFrame:
    """Padrón continuo municipal 2003-2022 por nacionalidad (todos los municipios)."""
    p = pd.read_csv(RAW / "v9" / "ine_padron_nacionalidad" / "padron_nacionalidad_2003_2022.csv.gz", usecols=["anio", "cod_municipio", "nacionalidad", "poblacion"],
                    dtype={"cod_municipio": str, "nacionalidad": str})
    p = p[p.cod_municipio.notna()].copy()
    p["poblacion"] = pd.to_numeric(p.poblacion, errors="coerce")
    p["anio"] = p.anio.astype(int)
    return p


# ---------------------------------------------------------------- población: fuentes provinciales


def poblacion_provincial() -> pd.DataFrame:
    """Población a 1 de enero por provincia (INE, 2 dígitos): padrón, censo anual, ECP. Columnas: fuente, nac, cod, anio, v."""
    filas = []
    for fuente, var in (("padron", "padron_pob_nacionalidad"), ("censo_anual", "pob_censo_anual"), ("ecp", "ecp_pob_nacionalidad")):
        d = hechos(var, "provincia")
        d = d[d.desagregacion.isin(["nacionalidad=Total", "nacionalidad=Extranjera", "nacionalidad=España", "nacionalidad=Española"])].copy()
        if fuente == "ecp":
            d = d[d.periodo.str.endswith("-01-01")]
        d["anio"] = d.periodo.str[:4].astype(int)
        d["nac"] = d.desagregacion.map({"nacionalidad=Total": "TOTAL", "nacionalidad=Extranjera": "EXT", "nacionalidad=España": "ES", "nacionalidad=Española": "ES"})
        d = d.rename(columns={"territorio_codigo": "cod", "valor": "v"})[["cod", "anio", "nac", "v"]].assign(fuente=fuente)
        filas.append(d)
    p = pd.concat(filas, ignore_index=True)
    c = p[(p.fuente == "censo_anual") & p.nac.isin(["TOTAL", "ES"])].pivot_table(index=["cod", "anio"], columns="nac", values="v").reset_index()
    c = c.assign(nac="EXT", v=c.TOTAL - c.ES, fuente="censo_anual")[["cod", "anio", "nac", "v", "fuente"]]
    p = pd.concat([p[~((p.fuente == "censo_anual") & (p.nac == "ES"))], c], ignore_index=True)
    return p[p.nac.isin(["TOTAL", "EXT"])]


def a_ccaa(p: pd.DataFrame) -> pd.DataFrame:
    q = p.copy()
    q["cod"] = q.cod.map(prov_ccaa())
    return q.groupby(["fuente", "nac", "cod", "anio"], as_index=False).v.sum()


def tasas(p: pd.DataFrame) -> pd.DataFrame:
    """Tasa de variación anual (%) entre el 1 de enero de t y t+1, indexada por t; solo años consecutivos."""
    a = p.rename(columns={"v": "v0"})
    b = p.assign(anio=p.anio - 1).rename(columns={"v": "v1"})
    m = a.merge(b, on=["fuente", "nac", "cod", "anio"])
    m["g"] = 100 * (m.v1 / m.v0 - 1)
    return m[["fuente", "nac", "cod", "anio", "v0", "v1", "g"]]


# ---------------------------------------------------------------- 1. atípicos


def atipicos() -> dict:
    filas, resumen = [], []
    pp = poblacion_provincial()
    for niv, g in (("provincia", tasas(pp)), ("ccaa", tasas(a_ccaa(pp)))):
        g = g[g.nac == "TOTAL"]
        z = z_temporal(g, ["fuente", "cod"], "g")
        filas.append(z[z.z.abs() > UMBRAL_Z].assign(nivel=niv, dominio="poblacion_total_tasa_anual_pct"))
        resumen.append({"dominio": "poblacion_total_tasa_anual_pct", "tipo": "temporal_por_serie", "nivel": niv, "series": int(z.dropna(subset=["z"]).groupby(["fuente", "cod"]).ngroups),
                        "obs": int(z.z.notna().sum()), "atipicos": int((z.z.abs() > UMBRAL_Z).sum()), "z_max_abs": round(float(z.z.abs().max()), 2)})
    m = pd.read_csv(B1 / "contabilidad_anual_municipio.csv.gz", dtype={"cod_territorio": str})
    m = m[m.nac == "TOTAL"].copy()
    m["g"] = 100 * m.crecimiento / m.poblacion_inicio
    m["fuente"], m["cod"] = m.fuente_poblacion, m.cod_territorio
    z = z_temporal(m, ["cod"], "g")
    filas.append(z[z.z.abs() > UMBRAL_Z].assign(nivel="municipio", dominio="poblacion_total_tasa_anual_pct"))
    resumen.append({"dominio": "poblacion_total_tasa_anual_pct", "tipo": "temporal_por_serie", "nivel": "municipio", "series": int(z.dropna(subset=["z"]).cod.nunique()),
                    "obs": int(z.z.notna().sum()), "atipicos": int((z.z.abs() > UMBRAL_Z).sum()), "z_max_abs": round(float(z.z.abs().max()), 2)})
    zc = z_corte(m, ["anio"], "g")
    resumen.append({"dominio": "poblacion_total_tasa_anual_pct", "tipo": "corte_por_anio", "nivel": "municipio", "series": int(zc.anio.nunique()), "obs": int(zc.z.notna().sum()),
                    "atipicos": int((zc.z.abs() > UMBRAL_Z).sum())})
    for etiqueta, msk in (("pob<20000", zc.poblacion_inicio < 20000), ("pob>=20000", zc.poblacion_inicio >= 20000)):
        resumen.append({"dominio": "poblacion_total_tasa_anual_pct", "tipo": f"corte_por_anio_{etiqueta}", "nivel": "municipio", "series": int(zc[msk].anio.nunique()),
                        "obs": int(zc[msk].z.notna().sum()), "atipicos": int((zc[msk].z.abs() > UMBRAL_Z).sum())})
    filas.append(zc[zc.z.abs() > UMBRAL_Z].assign(nivel="municipio", dominio="corte_por_anio").sort_values("z", key=abs, ascending=False).head(300))
    c = hechos("pob_censo_anual", "municipio", "nacionalidad=Total")
    c["anio"] = c.periodo.astype(int)
    c = c.rename(columns={"territorio_codigo": "cod", "valor": "v"})[["cod", "anio", "v"]].assign(fuente="censo_anual", nac="TOTAL")
    tc = tasas(c)
    for etiqueta, msk in (("todos", tc.v0 >= 0), ("v0>=1000", tc.v0 >= 1000), ("v0>=10000", tc.v0 >= 10000)):
        z = z_corte(tc[msk], ["anio"], "g")
        resumen.append({"dominio": "censo_anual_municipal_tasa_pct", "tipo": f"corte_por_anio_{etiqueta}", "nivel": "municipio", "series": int(z.anio.nunique()),
                        "obs": int(z.z.notna().sum()), "atipicos": int((z.z.abs() > UMBRAL_Z).sum()), "z_max_abs": round(float(z.z.abs().max()), 2)})
        if etiqueta == "v0>=1000":
            filas.append(z[z.z.abs() > UMBRAL_Z].assign(nivel="municipio", dominio="censo_anual_corte").sort_values("z", key=abs, ascending=False).head(300))
    hh = pd.concat([hechos("hogares_epa", "nacional").assign(fuente="epa"), hechos("hogares_ecp", "nacional").assign(fuente="ecp")], ignore_index=True)
    hh["t"] = hh.periodo.map(qidx)
    hh = hh.sort_values(["fuente", "t"])
    hh["qoq"] = 100 * hh.groupby("fuente").valor.pct_change()
    hh.loc[hh.groupby("fuente").t.diff() != 1, "qoq"] = np.nan
    hh["cod"] = "00"
    z = z_temporal(hh.dropna(subset=["qoq"]), ["fuente"], "qoq", min_obs=MIN_OBS)
    resumen.append({"dominio": "hogares_nacional_variacion_trimestral_pct", "tipo": "temporal_por_serie", "nivel": "nacional", "series": 2, "obs": int(z.z.notna().sum()),
                    "atipicos": int((z.z.abs() > UMBRAL_Z).sum()), "z_max_abs": round(float(z.z.abs().max()), 2)})
    filas.append(z[z.z.abs() > UMBRAL_Z].rename(columns={"qoq": "g"}).assign(nivel="nacional", dominio="hogares_nacional_qoq"))
    hp = pd.read_csv(RAW / "ine_v2_hogares_prov.csv", dtype={"codigo": str})
    hp = hp[(hp.nivel == "provincia") & (hp.desglose == "tamaño=Total")].copy()
    hp["cod"], hp["t"] = hp.codigo.str.zfill(2), hp.periodo.map(qidx)
    hp = hp.sort_values(["cod", "t"])
    hp["qoq"] = 100 * hp.groupby("cod").valor.pct_change()
    hp.loc[hp.groupby("cod").t.diff() != 1, "qoq"] = np.nan
    z = z_temporal(hp.dropna(subset=["qoq"]), ["cod"], "qoq", min_obs=MIN_OBS)
    resumen.append({"dominio": "hogares_ecp_provincial_variacion_trimestral_pct", "tipo": "temporal_por_serie", "nivel": "provincia", "series": int(z.dropna(subset=["z"]).cod.nunique()),
                    "obs": int(z.z.notna().sum()), "atipicos": int((z.z.abs() > UMBRAL_Z).sum()), "z_max_abs": round(float(z.z.abs().max()), 2)})
    filas.append(z[z.z.abs() > UMBRAL_Z].rename(columns={"qoq": "g"}).assign(nivel="provincia", dominio="hogares_ecp_prov_qoq", fuente="ecp"))
    d3 = pd.read_csv(B3 / "descomposicion_2011_2021_provincia.csv", dtype={"cpro": str})
    d3["g"] = 100 * (d3.hogares_2021 / d3.hogares_2011 - 1)
    d3["sh"] = d3.personas_por_hogar_2021 - d3.personas_por_hogar_2011
    d3["_k"] = 1
    for col, nom in (("g", "tasa_pct"), ("sh", "delta_personas_por_hogar")):
        z = z_temporal(d3, ["_k"], col, min_obs=30)
        resumen.append({"dominio": f"hogares_2011_2021_provincia_{nom}", "tipo": "corte_provincias", "nivel": "provincia", "series": 1, "obs": int(z.z.notna().sum()),
                        "atipicos": int((z.z.abs() > UMBRAL_Z).sum()), "z_max_abs": round(float(z.z.abs().max()), 2)})
        filas.append(z[z.z.abs() > UMBRAL_Z].rename(columns={"cpro": "cod", col: "g"}).assign(nivel="provincia", dominio=f"hogares_2011_2021_{nom}", fuente="censos"))
    v = hechos("vlc_padron_pob", "barrio", "sexo=Total")
    v["anio"] = v.periodo.str[:4].astype(int)
    v = v.rename(columns={"territorio_codigo": "cod", "valor": "v"})[["cod", "anio", "v"]].assign(fuente="vlc_padron", nac="TOTAL")
    z = z_temporal(tasas(v), ["cod"], "g", min_obs=MIN_OBS)
    resumen.append({"dominio": "valencia_barrio_tasa_anual_pct", "tipo": "temporal_por_serie", "nivel": "barrio", "series": int(z.dropna(subset=["z"]).cod.nunique()), "obs": int(z.z.notna().sum()),
                    "atipicos": int((z.z.abs() > UMBRAL_Z).sum()), "z_max_abs": round(float(z.z.abs().max()), 2)})
    filas.append(z[z.z.abs() > UMBRAL_Z].assign(nivel="barrio", dominio="valencia_barrio_tasa"))
    cols = ["dominio", "nivel", "fuente", "cod", "anio", "periodo", "g", "mediana", "mad_esc", "z", "n_serie"]
    det = pd.concat([f.reindex(columns=cols) for f in filas if len(f)], ignore_index=True)
    det["z"] = det.z.round(2)
    det = det.reindex(det.z.abs().sort_values(ascending=False).index)
    res = pd.DataFrame(resumen)
    res["pct_atipicos"] = (100 * res.atipicos / res.obs).round(3)
    guardar(res, "atipicos_resumen.csv")
    guardar(det.head(3000), "atipicos_detalle.csv")
    top = det[(det.nivel.isin(["provincia", "ccaa"])) & (det.dominio == "poblacion_total_tasa_anual_pct")].head(10)
    return {"resumen": res.to_dict("records"), "top_provincia_ccaa": top[["nivel", "fuente", "cod", "anio", "g", "z"]].to_dict("records")}


# ---------------------------------------------------------------- 2. coherencia


def estad_par(a: pd.DataFrame, b: pd.DataFrame, nombre: str, nivel: str, nac: str, glob: list) -> tuple[list, list]:
    """Niveles (diferencia % 1-ene) y tasas anuales entre dos fuentes, por año y por territorio."""
    A = a[a.nac == nac].rename(columns={"v": "va"})[["cod", "anio", "va"]]
    B = b[b.nac == nac].rename(columns={"v": "vb"})[["cod", "anio", "vb"]]
    m = A.merge(B, on=["cod", "anio"])
    m["dif_pct"] = 100 * (m.va / m.vb - 1)
    por_anio = []
    for y, g in m.groupby("anio"):
        k = g.loc[g.dif_pct.abs().idxmax()]
        por_anio.append({"par": nombre, "nivel": nivel, "nac": nac, "anio": int(y), "n_terr": len(g), "dif_nacional_pct": round(100 * (g.va.sum() / g.vb.sum() - 1), 3),
                         "dif_mediana_abs_pct": round(g.dif_pct.abs().median(), 3), "dif_max_abs_pct": round(g.dif_pct.abs().max(), 3), "terr_max": k.cod,
                         "n_dif_gt1pct": int((g.dif_pct.abs() > 1).sum()), "n_dif_gt5pct": int((g.dif_pct.abs() > 5).sum())})
    ta = tasas(a[a.nac == nac])[["cod", "anio", "g"]].rename(columns={"g": "ga"})
    tb = tasas(b[b.nac == nac])[["cod", "anio", "g"]].rename(columns={"g": "gb"})
    t = ta.merge(tb, on=["cod", "anio"])
    t["d"] = t.ga - t.gb
    t["opuesto"] = (np.sign(t.ga) != np.sign(t.gb)) & (t.ga.abs() > 0.05) & (t.gb.abs() > 0.05)
    por_terr = [{"par": nombre, "nivel": nivel, "nac": nac, "cod": c, "n_tasas": len(g), "corr_tasas": round(corr(g.ga, g.gb), 4), "dif_media_tasa_pp": round(g.d.mean(), 4),
                 "dif_max_abs_tasa_pp": round(g.d.abs().max(), 3), "anios_signo_opuesto": ",".join(str(int(y)) for y in g[g.opuesto].anio), "n_signo_opuesto": int(g.opuesto.sum())}
                for c, g in t.groupby("cod")]
    if len(t):
        glob.append({"par": nombre, "nivel": nivel, "nac": nac, "n_tasas": len(t), "corr_tasas": round(corr(t.ga, t.gb), 4), "dif_media_tasa_pp": round(t.d.mean(), 4),
                     "dif_max_abs_tasa_pp": round(t.d.abs().max(), 3), "n_signo_opuesto": int(t.opuesto.sum()), "n_tasas_con_signo_opuesto_o_cero": int(t.opuesto.sum())})
    return por_anio, por_terr


def coherencia_poblacion() -> dict:
    pp = poblacion_provincial()
    pa_all, pt_all, glob = [], [], []
    for niv, base in (("provincia", pp), ("ccaa", a_ccaa(pp))):
        for nombre, f1, f2 in (("padron_vs_ecp", "padron", "ecp"), ("censo_anual_vs_ecp", "censo_anual", "ecp"), ("padron_vs_censo_anual", "padron", "censo_anual")):
            for nac in ("TOTAL", "EXT"):
                pa, pt = estad_par(base[base.fuente == f1], base[base.fuente == f2], nombre, niv, nac, glob)
                pa_all += pa
                pt_all += pt
    pa_df, pt_df, gl = pd.DataFrame(pa_all), pd.DataFrame(pt_all), pd.DataFrame(glob)
    guardar(pa_df, "coherencia_poblacion_por_anio.csv")
    guardar(pt_df, "coherencia_poblacion_por_territorio.csv")
    guardar(gl, "coherencia_poblacion_resumen.csv")
    resumen = {}
    for (niv, par, nac), g in pa_df.groupby(["nivel", "par", "nac"]):
        resumen[f"{niv}|{par}|{nac}"] = {"anios": [int(g.anio.min()), int(g.anio.max())], "dif_nacional_pct_min": float(g.dif_nacional_pct.min()), "dif_nacional_pct_max": float(g.dif_nacional_pct.max()),
                                         "max_dif_territorial_abs_pct": float(g.dif_max_abs_pct.max()), "terr_dif_max": g.loc[g.dif_max_abs_pct.idxmax(), "terr_max"],
                                         "anio_dif_max": int(g.loc[g.dif_max_abs_pct.idxmax(), "anio"]), "max_territorios_con_dif_gt1pct_en_un_anio": int(g.n_dif_gt1pct.max()),
                                         "anios_con_dif_nacional_gt0_5pct": [int(a) for a in g[g.dif_nacional_pct.abs() > 0.5].anio]}
    tasas_res = {f"{r.nivel}|{r.par}|{r.nac}": {"corr_tasas": float(r.corr_tasas), "dif_media_pp": float(r.dif_media_tasa_pp), "n_signo_opuesto": int(r.n_signo_opuesto), "n_tasas": int(r.n_tasas)}
                 for r in gl.itertuples()}
    # años con signo opuesto en agregados nacionales (suma de provincias)
    nacl = pp.groupby(["fuente", "nac", "anio"], as_index=False).v.sum().assign(cod="00")
    na = nacl[nacl.nac == "TOTAL"]
    t_n = {f: tasas(na[na.fuente == f]).set_index("anio").g for f in ("padron", "censo_anual", "ecp")}
    nac_tabla = pd.DataFrame({"padron": t_n["padron"], "censo_anual": t_n["censo_anual"], "ecp": t_n["ecp"]}).round(4).reset_index().rename(columns={"index": "anio"})
    guardar(nac_tabla, "coherencia_poblacion_nacional_tasas.csv")
    opuesto = nac_tabla[(np.sign(nac_tabla.padron) != np.sign(nac_tabla.ecp)) & nac_tabla.padron.notna() & nac_tabla.ecp.notna()]
    return {"niveles_y_dispersion": resumen, "tasas": tasas_res, "nacional_anios_padron_ecp_signo_opuesto": [int(a) for a in opuesto.anio],
            "nacional_tasas_pct": nac_tabla.to_dict("records")}


def coherencia_hogares() -> dict:
    epa = hechos("hogares_epa", "nacional")[["periodo", "valor"]].rename(columns={"valor": "epa"})
    ecp = hechos("hogares_ecp", "nacional")[["periodo", "valor"]].rename(columns={"valor": "ecp"})
    m = epa.merge(ecp, on="periodo")
    m["t"] = m.periodo.map(qidx)
    m = m.sort_values("t").reset_index(drop=True)
    m["brecha_pct"] = 100 * (m.epa / m.ecp - 1)
    m["yoy_epa"] = 100 * (m.epa / m.epa.shift(4) - 1)
    m["yoy_ecp"] = 100 * (m.ecp / m.ecp.shift(4) - 1)
    m["qoq_epa"] = 100 * m.epa.pct_change()
    m["qoq_ecp"] = 100 * m.ecp.pct_change()
    m["opuesto_qoq"] = (np.sign(m.qoq_epa) != np.sign(m.qoq_ecp)) & m.qoq_epa.notna()
    guardar(m.drop(columns="t"), "hogares_epa_vs_ecp_trimestral.csv")
    pend = float(np.polyfit(m.t.values, m.brecha_pct.values, 1)[0] * 4)
    censo_total = censo_viv = None
    for ln in open(RAW / "v11" / "ine_censo2021" / "censo2021_tpx59534.csv", encoding="utf-8-sig"):
        if ln.startswith("Total (tipo de hogar);Total (tamaño del hogar)"):
            censo_total = int(ln.strip().split(";")[-1].replace(".", ""))
    for ln in open(RAW / "v11" / "ine_censo2021" / "censo2021_tpx59519.csv", encoding="utf-8-sig"):
        if ln.startswith("Total (tamaño del hogar);Total (superficie"):
            censo_viv = int(ln.strip().split(";")[-1].replace(".", ""))
    epa21 = float(m.loc[m.periodo == "2021T1", "epa"].iloc[0])
    ecp21 = float(m.loc[m.periodo == "2021T1", "ecp"].iloc[0])
    prov = territorios()
    prov = prov[prov.nivel == "provincia"].set_index("territorio_codigo").nombre.to_dict()
    cen = {}
    for ln in open(RAW / "v11" / "ine_censo2021" / "censo2021_tpx59524.csv", encoding="utf-8-sig"):
        p = ln.rstrip("\n").split(";")
        if len(p) == 4 and p[1] == "Total (tamaño del hogar)" and p[2].startswith("Total (superficie"):
            mm = re.match(r"^(\d{2}) (.+)$", p[0])
            if mm and mm.group(1) in prov and pal(mm.group(2)) & pal(prov[mm.group(1)]):
                cen[mm.group(1)] = int(p[3].replace(".", ""))
    hp = pd.read_csv(RAW / "ine_v2_hogares_prov.csv", dtype={"codigo": str})
    hp = hp[(hp.nivel == "provincia") & (hp.desglose == "tamaño=Total") & (hp.periodo == "2021T1")]
    hp = hp.assign(cod=hp.codigo.str.zfill(2)).set_index("cod").valor
    cc = pd.DataFrame({"censo_tabla_59524": pd.Series(cen), "ecp_2021T1": hp}).dropna()
    cc["dif_pct"] = 100 * (cc.ecp_2021T1 / cc.censo_tabla_59524 - 1)
    guardar(cc.rename_axis("cod_provincia").reset_index(), "hogares_ecp_vs_censo2021_provincia.csv")
    e = hechos("hogares_epa", "nacional")[["periodo", "valor"]]
    e["t"] = e.periodo.map(qidx)
    e = e.sort_values("t")
    e["qoq"] = 100 * e.valor.pct_change()
    e["yoy"] = 100 * (e.valor / e.valor.shift(4) - 1)
    out = {}
    for col in ("qoq", "yoy"):
        base = e[e.periodo != "2021T1"].dropna(subset=[col])
        med, mad = zrob(base[col])
        v = float(e.loc[e.periodo == "2021T1", col].iloc[0])
        out[col] = {"valor_2021T1": round(v, 3), "mediana_resto": round(med, 3), "mad_esc_resto": round(mad, 3), "z_robusto": round((v - med) / mad, 2) if mad > 0 else None}
    return {"epa_vs_ecp_2021T1_2026T2": {"n_trimestres": int(len(m)), "brecha_pct_2021T1": round(float(m.brecha_pct.iloc[0]), 3), "brecha_pct_2026T2": round(float(m.brecha_pct.iloc[-1]), 3),
                                          "pendiente_brecha_pp_por_anio": round(pend, 3), "corr_qoq": round(corr(m.qoq_epa, m.qoq_ecp), 3), "corr_yoy": round(corr(m.yoy_epa, m.yoy_ecp), 3),
                                          "dif_media_yoy_pp_epa_menos_ecp": round(float((m.yoy_epa - m.yoy_ecp).mean()), 3),
                                          "trimestres_qoq_signo_opuesto": m[m.opuesto_qoq].periodo.tolist(),
                                          "crecimiento_acumulado_pct_epa": round(float(100 * (m.epa.iloc[-1] / m.epa.iloc[0] - 1)), 3),
                                          "crecimiento_acumulado_pct_ecp": round(float(100 * (m.ecp.iloc[-1] / m.ecp.iloc[0] - 1)), 3)},
            "epa_vs_censo2021": {"censo_hogares_tabla_59534": censo_total, "censo_hogares_tabla_59519_sup_util": censo_viv, "epa_2021T1_miles": epa21, "ecp_2021T1_miles": ecp21,
                                  "dif_epa_vs_censo_pct": round(100 * (epa21 * 1000 / censo_total - 1), 3) if censo_total else None,
                                  "dif_ecp_vs_censo_pct": round(100 * (ecp21 * 1000 / censo_total - 1), 4) if censo_total else None,
                                  "nota": "la ECP de 2021T1 reproduce el total del censo por construcción: no es un contraste independiente"},
            "ecp_vs_censo2021_provincial": {"provincias": int(len(cc)), "dif_pct_mediana_abs": round(float(cc.dif_pct.abs().median()), 4) if len(cc) else None,
                                              "dif_pct_max_abs": round(float(cc.dif_pct.abs().max()), 4) if len(cc) else None, "provincias_dif_gt1pct": int((cc.dif_pct.abs() > 1).sum())},
            "ruptura_epa_2021T1_hogares": out}


def residuo_b1() -> dict:
    """Saldo migratorio (exterior + interior) frente a ΔP − vegetativo, por provincia y periodo (B1, nac = TOTAL)."""
    per = pd.read_csv(B1 / "contabilidad_periodos_provincia.csv", dtype={"cod_territorio": str})
    per = per[per.nac == "TOTAL"].copy()
    per["cod"] = per.cod_territorio.str.zfill(2)
    per["migratorio_evr_emcr"] = per.saldo_exterior + per.saldo_interior
    per["dp_menos_vegetativo"] = per.crecimiento - per.vegetativo
    per["residuo_pct_pob_inicio"] = 100 * per.residuo / per.poblacion_inicio
    per["residuo_pct_pob_anual"] = per.residuo_pct_pob_inicio / per.anios
    per["flag_residuo_gt1pct_periodo"] = per.residuo_pct_pob_inicio.abs() > UMBRAL_RESIDUO_PCT
    per["flag_residuo_gt1pct_anual"] = per.residuo_pct_pob_anual.abs() > UMBRAL_RESIDUO_PCT
    per["signo_residuo"] = np.sign(per.residuo)
    cols = ["periodo", "cod", "anios", "poblacion_inicio", "crecimiento", "vegetativo", "saldo_exterior", "saldo_interior", "residuo", "migratorio_evr_emcr", "dp_menos_vegetativo",
            "residuo_pct_pob_inicio", "residuo_pct_pob_anual", "flag_residuo_gt1pct_periodo", "flag_residuo_gt1pct_anual", "signo_residuo"]
    guardar(per[cols].sort_values(["periodo", "cod"]), "residuo_b1_provincia_periodo.csv")
    nac = pd.read_csv(B1 / "contabilidad_periodos_nacional.csv", dtype={"cod_territorio": str})
    nac = nac[nac.nac == "TOTAL"].set_index("periodo")
    res = {}
    for p, g in per.groupby("periodo"):
        res[p] = {"provincias": int(len(g)), "residuo_nacional": float(nac.loc[p, "residuo"]), "residuo_nacional_pct_pob_inicio": round(float(100 * nac.loc[p, "residuo"] / nac.loc[p, "poblacion_inicio"]), 3),
                  "provincias_residuo_negativo": int((g.residuo < 0).sum()), "provincias_residuo_positivo": int((g.residuo > 0).sum()),
                  "residuo_pct_pob_mediana": round(float(g.residuo_pct_pob_inicio.median()), 3), "residuo_pct_pob_min": round(float(g.residuo_pct_pob_inicio.min()), 3),
                  "residuo_pct_pob_max": round(float(g.residuo_pct_pob_inicio.max()), 3), "n_provincias_residuo_gt1pct_periodo": int(g.flag_residuo_gt1pct_periodo.sum()),
                  "n_provincias_residuo_gt1pct_anual": int(g.flag_residuo_gt1pct_anual.sum()), "provincias_gt1pct_periodo": sorted(g[g.flag_residuo_gt1pct_periodo].cod.tolist()),
                  "corr_migratorio_vs_dp_menos_veg": round(corr(g.migratorio_evr_emcr, g.dp_menos_vegetativo), 4),
                  "signo_migratorio_igual_a_dp_menos_veg": int((np.sign(g.migratorio_evr_emcr) == np.sign(g.dp_menos_vegetativo)).sum())}
    an = pd.read_csv(B1 / "contabilidad_anual_provincia.csv", dtype={"cod_territorio": str})
    an = an[an.nac == "TOTAL"].copy()
    an["pct"] = 100 * an.residuo / an.poblacion_inicio
    anual = an.groupby("anio").agg(n=("pct", "size"), n_gt1=("pct", lambda s: int((s.abs() > UMBRAL_RESIDUO_PCT).sum())), n_neg=("pct", lambda s: int((s < 0).sum())), mediana=("pct", "median"),
                                   minimo=("pct", "min"), maximo=("pct", "max")).round(3).reset_index()
    guardar(anual, "residuo_b1_provincia_anual_resumen.csv")
    ev = per[per.periodo == "2014-2019"].set_index("cod").residuo_pct_pob_anual
    em = per[per.periodo == "2022-2024"].set_index("cod").residuo_pct_pob_anual
    return {"por_periodo": res, "anual_resumen": anual.to_dict("records"),
            "provincias_residuo_negativo_2014_2019_y_positivo_2022_2024": int(((ev < 0) & (em > 0)).sum()),
            "corr_residuo_anual_pct_2014_2019_vs_2022_2024": round(corr(ev, em), 3)}


# ---------------------------------------------------------------- 3. rupturas y revisiones


@lru_cache(maxsize=1)
def flujos_exterior() -> pd.DataFrame:
    """Flujos exteriores por provincia (EVR y EMCR) desde microdatos municipales (PP999 incluidos; sin códigos 66)."""
    filas = []
    for fuente, cin, cout in (("ine_evr", "altas_desde_extranjero", "bajas_al_extranjero"), ("ine_emcr", "inmigracion_exterior", "emigracion_exterior")):
        e = pd.read_csv(RAW / "v11" / fuente / "flujos_exterior_municipio.csv.gz", dtype=str)
        e = e[~e.cod_municipio.str.startswith("66")].copy()
        e["anio"] = e.anio.astype(int)
        e["cod"] = e.cod_municipio.str[:2]
        for c in (cin, cout):
            e[c] = pd.to_numeric(e[c])
        g = e.groupby(["anio", "cod"], as_index=False)[[cin, cout]].sum().rename(columns={cin: "inmigracion", cout: "emigracion"})
        filas.append(g.assign(fuente=fuente))
    return pd.concat(filas, ignore_index=True)


def revisiones_y_empalme() -> dict:
    fl = flujos_exterior()
    out = {}
    for v, col in (("em_inmigracion_extranjero", "inmigracion"), ("em_emigracion_extranjero", "emigracion")):
        em = hechos(v, "provincia", "nacionalidad=Total")
        em["anio"] = em.periodo.astype(int)
        em = em.rename(columns={"territorio_codigo": "cod", "valor": "em"})[["cod", "anio", "em"]]
        rows = []
        for fuente in ("ine_evr", "ine_emcr"):
            f = fl[fl.fuente == fuente][["anio", "cod", col]]
            m = em.merge(f, on=["anio", "cod"])
            m["dif_pct"] = 100 * (m[col] / m.em - 1)
            for y, g in m.groupby("anio"):
                rows.append({"serie": v, "microdato": fuente, "anio": int(y), "provincias": len(g), "total_em": float(g.em.sum()), "total_microdato": float(g[col].sum()),
                             "dif_total_pct": round(float(100 * (g[col].sum() / g.em.sum() - 1)), 3), "dif_mediana_abs_prov_pct": round(float(g.dif_pct.abs().median()), 3),
                             "dif_max_abs_prov_pct": round(float(g.dif_pct.abs().max()), 3)})
        out[v] = pd.DataFrame(rows)
    rev = pd.concat(out.values(), ignore_index=True)
    guardar(rev, "revisiones_evr_vs_em_provincia.csv")
    e21 = fl[fl.anio == 2021].pivot_table(index="cod", columns="fuente", values=["inmigracion", "emigracion"])
    emp = pd.DataFrame({"inm_evr": e21[("inmigracion", "ine_evr")], "inm_emcr": e21[("inmigracion", "ine_emcr")], "emi_evr": e21[("emigracion", "ine_evr")], "emi_emcr": e21[("emigracion", "ine_emcr")]})
    emp["ratio_inm"] = emp.inm_emcr / emp.inm_evr
    emp["ratio_emi"] = emp.emi_emcr / emp.emi_evr
    guardar(emp.rename_axis("cod_provincia").reset_index(), "empalme_2021_evr_emcr_provincia.csv")
    nacl = fl.groupby(["fuente", "anio"])[["inmigracion", "emigracion"]].sum().reset_index()
    nacl["saldo"] = nacl.inmigracion - nacl.emigracion
    guardar(nacl, "flujos_exteriores_nacional_evr_emcr.csv")
    s = nacl.set_index(["fuente", "anio"])
    resum = {}
    for v in ("em_inmigracion_extranjero", "em_emigracion_extranjero"):
        r = out[v]
        ev = r[(r.microdato == "ine_evr") & (r.anio <= 2020)]
        resum[v] = {"EVR_vs_EM_dif_total_pct_2008_2020": [float(ev.dif_total_pct.min()), float(ev.dif_total_pct.max())], "EVR_vs_EM_max_dif_provincial_abs_pct_2008_2020": float(ev.dif_max_abs_prov_pct.max()),
                    "EMCR_vs_EM_dif_total_pct_2021": float(r[(r.microdato == "ine_emcr") & (r.anio == 2021)].dif_total_pct.iloc[0]) if len(r[(r.microdato == "ine_emcr") & (r.anio == 2021)]) else None,
                    "EVR_vs_EM_dif_total_pct_2021": float(r[(r.microdato == "ine_evr") & (r.anio == 2021)].dif_total_pct.iloc[0]) if len(r[(r.microdato == "ine_evr") & (r.anio == 2021)]) else None}
    resum["empalme_2021_nacional"] = {"inmigracion_evr": float(s.loc[("ine_evr", 2021), "inmigracion"]), "inmigracion_emcr": float(s.loc[("ine_emcr", 2021), "inmigracion"]),
                                       "emigracion_evr": float(s.loc[("ine_evr", 2021), "emigracion"]), "emigracion_emcr": float(s.loc[("ine_emcr", 2021), "emigracion"])}
    resum["empalme_2021_cociente_emcr_evr_provincial"] = {"inmigracion_mediana": float(emp.ratio_inm.median()), "inmigracion_min": float(emp.ratio_inm.min()), "inmigracion_max": float(emp.ratio_inm.max()),
                                                          "emigracion_mediana": float(emp.ratio_emi.median()), "emigracion_min": float(emp.ratio_emi.min()), "emigracion_max": float(emp.ratio_emi.max())}
    return resum


def ruptura_epa_poblacion() -> dict:
    """EPA población total (CCAA, miles) frente a ECP (suma de provincias): salto de la razón en 2021T1."""
    e = hechos("epa_pob_total", "ccaa")
    e["t"] = e.periodo.map(qidx)
    en = e.groupby("t").valor.sum().rename("epa") * 1000
    p = hechos("ecp_pob_nacionalidad", "provincia", "nacionalidad=Total")
    p["fecha"] = pd.to_datetime(p.periodo)
    p["t"] = p.fecha.dt.year * 4 + (p.fecha.dt.month - 1) // 3
    ecp = p.groupby("t").valor.sum().rename("ecp")
    m = pd.concat([en, ecp], axis=1).dropna()
    m["razon_pct"] = 100 * (m.epa / m.ecp - 1)
    m["periodo"] = [qlab(int(t)) for t in m.index]
    m["dif_razon_pp"] = m.razon_pct.diff()
    guardar(m.reset_index(drop=True), "epa_poblacion_vs_ecp.csv")
    t21 = qidx("2021T1")
    ref = m[m.index < t21].dif_razon_pp.dropna()
    med, mad = zrob(ref)
    v = float(m.loc[t21, "dif_razon_pp"]) if t21 in m.index else float("nan")
    return {"razon_epa_ecp_pct_ultimo_antes_2021T1": float(m[m.index < t21].razon_pct.iloc[-1]), "periodo_ultimo_antes": m[m.index < t21].periodo.iloc[-1],
            "razon_epa_ecp_pct_2021T1": float(m.loc[t21, "razon_pct"]) if t21 in m.index else None, "salto_razon_pp_2021T1": v, "mediana_saltos_previos_pp": med,
            "mad_esc_saltos_previos_pp": mad, "z_robusto_salto_2021T1": (v - med) / mad if mad > 0 else None, "n_pares": int(len(m)),
            "nota": "EPA se recalibra a la población del censo 2021 desde 2021T1; el salto se mide contra la ECP (T1 y T3 hasta 2020, trimestral después)"}


def padron_a_censo() -> dict:
    p = padron_municipal()
    p = p[(p.nacionalidad == "Total") & p.anio.isin([2021, 2022])].rename(columns={"cod_municipio": "cod", "poblacion": "pad"})
    c = hechos("pob_censo_anual", "municipio", "nacionalidad=Total")
    c = c[c.periodo.isin(["2021", "2022"])].rename(columns={"territorio_codigo": "cod", "valor": "cen"})
    c["anio"] = c.periodo.astype(int)
    m = p[["cod", "anio", "pad"]].merge(c[["cod", "anio", "cen"]], on=["cod", "anio"], how="outer", indicator=True)
    res, filas = {}, []
    for y, g in m.groupby("anio"):
        both = g[g._merge == "both"].copy()
        both["dif_pct"] = 100 * (both.cen / both.pad - 1)
        res[int(y)] = {"municipios_ambos": int(len(both)), "solo_padron": int((g._merge == "left_only").sum()), "solo_censo": int((g._merge == "right_only").sum()),
                       "dif_total_pct": round(float(100 * (both.cen.sum() / both.pad.sum() - 1)), 4), "dif_mediana_abs_pct": round(float(both.dif_pct.abs().median()), 3),
                       "municipios_dif_gt1pct": int((both.dif_pct.abs() > 1).sum()), "municipios_dif_gt5pct": int((both.dif_pct.abs() > 5).sum()),
                       "poblacion_en_municipios_dif_gt5pct": int(both[both.dif_pct.abs() > 5].pad.sum()),
                       "municipios_dif_gt1pct_con_pob_ge_10000": int(((both.dif_pct.abs() > 1) & (both.pad >= 10000)).sum())}
        filas.append(both.sort_values("dif_pct", key=abs, ascending=False).head(50))
    guardar(pd.concat(filas)[["anio", "cod", "pad", "cen", "dif_pct"]], "padron_vs_censo_anual_municipios_top50_dif.csv")
    return res


def seccionado() -> dict:
    """Cambios de seccionado observables: censo anual 2021-2025 y ADRH 2019-2023 (secciones con dato por año)."""
    cs = hechos("pob_censo_anual", "seccion", "nacionalidad=Total")
    cs["anio"] = cs.periodo.astype(int)
    conj = {a: set(g.territorio_codigo) for a, g in cs.groupby("anio")}
    ad = hechos("adrh_renta_neta_hogar", "seccion")
    ad["anio"] = ad.periodo.astype(int)
    conj_ad = {a: set(g.territorio_codigo) for a, g in ad.groupby("anio")}
    filas = []
    for nombre, cj in (("censo_anual", conj), ("adrh", conj_ad)):
        ys = sorted(cj)
        for y0, y1 in zip(ys[:-1], ys[1:]):
            filas.append({"fuente": nombre, "desde": y0, "hasta": y1, "secciones_desde": len(cj[y0]), "secciones_hasta": len(cj[y1]), "desaparecen": len(cj[y0] - cj[y1]), "nuevas": len(cj[y1] - cj[y0]),
                          "municipios_con_cambio": len({c[:5] for c in (cj[y0] ^ cj[y1])})})
    filas.append({"fuente": "adrh2023_vs_censo_anual2021", "desde": 2023, "hasta": 2021, "secciones_desde": len(conj_ad[2023]), "secciones_hasta": len(conj[2021]), "desaparecen": len(conj_ad[2023] - conj[2021]),
                  "nuevas": len(conj[2021] - conj_ad[2023]), "municipios_con_cambio": len({c[:5] for c in (conj_ad[2023] ^ conj[2021])})})
    filas.append({"fuente": "censo_anual_2021_vs_2025", "desde": 2021, "hasta": 2025, "secciones_desde": len(conj[2021]), "secciones_hasta": len(conj[2025]), "desaparecen": len(conj[2021] - conj[2025]),
                  "nuevas": len(conj[2025] - conj[2021]), "municipios_con_cambio": len({c[:5] for c in (conj[2021] ^ conj[2025])})})
    t = pd.DataFrame(filas)
    guardar(t, "seccionado_cambios.csv")
    mun = {c[:5] for c in (conj[2021] ^ conj[2025])}
    pm = hechos("pob_censo_anual", "municipio", "nacionalidad=Total")
    pm = pm[pm.periodo == "2025"]
    ter = territorios()
    sec_ant = CON.sql(f"SELECT variable, min(periodo) a FROM '{HECHOS}' WHERE nivel='seccion' GROUP BY 1").df()
    return {"tabla": t.to_dict("records"), "municipios_con_cambio_2021_2025": len(mun),
            "poblacion_2025_en_municipios_con_cambio_pct": round(float(100 * pm[pm.territorio_codigo.isin(mun)].valor.sum() / pm.valor.sum()), 2),
            "secciones_en_territorios_vigente_2025": int(((ter.nivel == "seccion") & ter.vigente_2025).sum()),
            "primer_anio_de_las_variables_con_nivel_seccion": sec_ant.a.astype(str).str[:4].value_counts().sort_index().to_dict(),
            "secciones_2011": "no hay seccionado ni datos por sección de 2011 en data/raw ni en la base: la comparación 2011-2021 por sección NO es auditable; solo el seccionado vigente (2019-2025)"}


# ---------------------------------------------------------------- 4. reparto espacial B1


def catastro_unidades() -> pd.DataFrame:
    d = hechos("catastro_unidades_urbanas_residenciales", "municipio")
    d["anio"] = d.periodo.astype(int)
    return d.rename(columns={"territorio_codigo": "cod", "valor": "viv"})[["cod", "anio", "viv"]]


def poblacion_inicio_municipal() -> pd.DataFrame:
    """Población total a 1 de enero por municipio (padrón hasta 2021; censo anual desde 2022, como B1)."""
    p = padron_municipal()
    p = p[(p.nacionalidad == "Total") & (p.anio <= 2021)].rename(columns={"cod_municipio": "cod", "poblacion": "pob"})[["cod", "anio", "pob"]]
    c = hechos("pob_censo_anual", "municipio", "nacionalidad=Total")
    c["anio"] = c.periodo.astype(int)
    c = c[c.anio >= 2022].rename(columns={"territorio_codigo": "cod", "valor": "pob"})[["cod", "anio", "pob"]]
    return pd.concat([p, c], ignore_index=True)


def asignar(total: float, w: pd.Series) -> pd.Series:
    s = float(w.sum())
    if not np.isfinite(s) or s <= 0:
        return pd.Series(np.nan, index=w.index)
    return total * w / s


def reparto_municipal() -> tuple[pd.DataFrame, dict]:
    per = pd.read_csv(B1 / "contabilidad_periodos_municipio.csv.gz", dtype={"cod_territorio": str})
    per = per[per.nac == "TOTAL"].copy()
    prv = pd.read_csv(B1 / "contabilidad_periodos_provincia.csv", dtype={"cod_territorio": str})
    prv = prv[prv.nac == "TOTAL"].copy()
    prv["cod"] = prv.cod_territorio.str.zfill(2)
    pob = poblacion_inicio_municipal()
    cat = catastro_unidades()
    filas = []
    for pname, (y0, _) in PERIODOS_REPARTO.items():
        ya = max(y0, 2012)   # fichero t del Catastro = stock a 31-12-(t-1) ≈ 1 de enero de t; el primero disponible es 2012
        po = pob[pob.anio == y0].set_index("cod").pob
        ca = cat[cat.anio == ya].set_index("cod").viv
        obs = per[per.periodo == pname].set_index("cod_territorio")
        for cp, pr in prv[prv.periodo == pname].set_index("cod").iterrows():
            miembros = po[po.index.str[:2] == cp]
            if miembros.empty:
                continue
            o = obs[obs.index.str[:2] == cp]
            o = o[o.index.isin(miembros.index)]
            resto = miembros.index.difference(o.index)
            hay_cat = cp not in SIN_CATASTRO_ESTATAL
            for comp in COMPONENTES:
                tot_o = float(o[comp].sum()) if len(o) else 0.0
                tot_r = float(pr[comp]) - tot_o
                if len(o) >= 2:
                    wp = miembros.loc[o.index].astype(float)
                    wc = ca.reindex(o.index).astype(float)
                    ap = asignar(tot_o, wp)
                    ac = asignar(tot_o, wc.fillna(0.0)) if (hay_cat and wc.notna().all() and (wc > 0).all()) else pd.Series(np.nan, index=o.index)
                    for cm in o.index:
                        filas.append((cm, cp, pname, comp, "observado_ge10000", float(o.loc[cm, comp]), float(ap[cm]), float(ac[cm]), float(wp[cm]), float(wc[cm]) if pd.notna(wc[cm]) else np.nan, ya))
                if len(resto):
                    wp = miembros.loc[resto].astype(float)
                    wc = ca.reindex(resto).astype(float).fillna(0.0)
                    ap = asignar(tot_r, wp)
                    ac = asignar(tot_r, wc) if hay_cat else pd.Series(np.nan, index=resto)
                    for cm in resto:
                        filas.append((cm, cp, pname, comp, "resto_lt10000_o_intermitente", np.nan, float(ap[cm]), float(ac[cm]), float(wp[cm]), float(wc[cm]) if hay_cat else np.nan, ya))
    cols = ["cod", "cod_provincia", "periodo", "componente", "grupo", "valor_original", "reparto_poblacion", "reparto_catastro", "poblacion_inicio", "viviendas_catastro", "anio_catastro"]
    df = pd.DataFrame(filas, columns=cols)
    hay = df.valor_original.notna() & (df.valor_original != 0)
    df["signo_cambia_catastro_vs_original"] = np.where(hay & df.reparto_catastro.notna(), (np.sign(df.valor_original) != np.sign(df.reparto_catastro)).astype(float), np.nan)
    df["signo_cambia_poblacion_vs_original"] = np.where(hay & df.reparto_poblacion.notna(), (np.sign(df.valor_original) != np.sign(df.reparto_poblacion)).astype(float), np.nan)
    df["tipo_unidad"] = "municipio"
    met = []
    for (per_, comp), g in df[df.grupo == "observado_ge10000"].groupby(["periodo", "componente"]):
        g = g.dropna(subset=["reparto_catastro"])
        if len(g) < 10:
            continue
        pm = g.poblacion_inicio
        e_p, e_c = (g.reparto_poblacion - g.valor_original).abs(), (g.reparto_catastro - g.valor_original).abs()
        met.append({"periodo": per_, "componente": comp, "n_municipios": len(g), "corr_nivel_poblacion": corr(g.valor_original, g.reparto_poblacion), "corr_nivel_catastro": corr(g.valor_original, g.reparto_catastro),
                    "corr_tasa_poblacion": corr(1000 * g.valor_original / pm, 1000 * g.reparto_poblacion / pm), "corr_tasa_catastro": corr(1000 * g.valor_original / pm, 1000 * g.reparto_catastro / pm),
                    "spearman_tasa_catastro": corr(1000 * g.valor_original / pm, 1000 * g.reparto_catastro / pm, "spearman"),
                    "error_abs_mediano_por_mil_poblacion": float((1000 * e_p / pm).median()), "error_abs_mediano_por_mil_catastro": float((1000 * e_c / pm).median()),
                    "pct_municipios_catastro_mejor": float(100 * (e_c < e_p).mean()), "n_signo_cambia_catastro": int(g.signo_cambia_catastro_vs_original.sum()),
                    "n_signo_cambia_poblacion": int(g.signo_cambia_poblacion_vs_original.sum()),
                    "pct_signo_cambia_catastro": float(100 * g.signo_cambia_catastro_vs_original.mean()), "pct_signo_cambia_poblacion": float(100 * g.signo_cambia_poblacion_vs_original.mean()),
                    "corr_entre_repartos_nivel": corr(g.reparto_poblacion, g.reparto_catastro)})
    M = pd.DataFrame(met)
    guardar(M, "b1_reparto_metricas_municipal.csv")
    rr = []
    for (per_, comp), g in df[df.grupo == "resto_lt10000_o_intermitente"].groupby(["periodo", "componente"]):
        g = g.dropna(subset=["reparto_catastro"])
        if len(g) < 10:
            continue
        rel = (g.reparto_catastro - g.reparto_poblacion).abs() / g.reparto_poblacion.abs().replace(0, np.nan)
        rr.append({"periodo": per_, "componente": comp, "n_municipios": len(g), "corr_nivel_entre_repartos": corr(g.reparto_poblacion, g.reparto_catastro),
                   "dif_relativa_mediana": float(rel.median()), "dif_relativa_p90": float(rel.quantile(0.9)), "pct_dif_relativa_gt50": float(100 * (rel > 0.5).mean()),
                   "pct_signo_distinto_entre_repartos": float(100 * (np.sign(g.reparto_catastro) != np.sign(g.reparto_poblacion)).mean())})
    R = pd.DataFrame(rr)
    guardar(R, "b1_reparto_metricas_resto_lt10000.csv")
    rest = df[df.grupo == "resto_lt10000_o_intermitente"]
    cobertura = {"municipios_resto_total": int(rest.cod.nunique()), "municipios_resto_con_reparto_catastro": int(rest.dropna(subset=["reparto_catastro"]).cod.nunique()),
                 "municipios_observados_con_reparto_catastro": int(df[df.grupo == "observado_ge10000"].dropna(subset=["reparto_catastro"]).cod.nunique()),
                 "provincias_sin_catastro_estatal_excluidas": list(SIN_CATASTRO_ESTATAL)}
    return df, {"metricas_observados": M.round(4).to_dict("records"), "metricas_resto": R.round(4).to_dict("records"), "cobertura": cobertura}


def reparto_valencia() -> tuple[pd.DataFrame, dict]:
    """Sección -> barrio: criterio V12 (área; entera si >= 95 % del área) frente a área ponderada por la densidad de viviendas del barrio (Catastro INSPIRE)."""
    c = pd.read_csv(RAW / "v9" / "ine_censo_anual" / "censo_seccion_pais.csv.gz", dtype=str, usecols=["nivel", "cod_municipio", "cod_seccion", "edicion", "pais_nacionalidad", "poblacion"])
    s = c[(c.nivel == "seccion") & (c.cod_municipio == "46250")].copy()
    s["poblacion"] = pd.to_numeric(s.poblacion)
    s["anio"] = s.edicion.astype(int)
    w = s[s.pais_nacionalidad.isin(["Total", "España"])].pivot_table(index=["cod_seccion", "anio"], columns="pais_nacionalidad", values="poblacion", aggfunc="sum").fillna(0)
    w["EXT"] = w["Total"] - w["España"]
    sec = w.reset_index()
    k = pd.read_csv(BASE / "geo" / "correspondencia_seccion_barrio_valencia.csv", dtype={"cod_seccion": str, "cod_barrio": str})
    bar = pd.read_parquet(BASE / "geo" / "barrios_valencia.parquet")
    area = pd.Series({r.cod_barrio: wkb.loads(bytes(r.geometry)).area for r in bar.itertuples()})
    ed = pd.read_csv(RAW / "v11" / "catastro_inspire" / "edificios_barrio_valencia.csv.gz", dtype={"cod_barrio": str})
    viv = ed[ed.uso.astype(str).str.contains("residential")].groupby("cod_barrio").viviendas.sum()
    dens = (viv / area).reindex(area.index)
    dens = dens.fillna(dens.median())

    def pesos(alt: bool) -> pd.DataFrame:
        unico = k[k.seccion_en_un_barrio].sort_values("peso_area").groupby("cod_seccion").tail(1).assign(peso=1.0)
        rep = k[~k.seccion_en_un_barrio].copy()
        rep["base"] = rep.peso_area * (rep.cod_barrio.map(dens) if alt else 1.0)
        rep["peso"] = rep.base / rep.groupby("cod_seccion").base.transform("sum")
        return pd.concat([unico, rep])[["cod_seccion", "cod_barrio", "peso"]]

    def a_barrio(pw: pd.DataFrame) -> pd.DataFrame:
        x = sec.merge(pw, how="left", on="cod_seccion")
        x["cod_barrio"] = x.cod_barrio.fillna("sin_asignar")
        x["peso"] = x.peso.fillna(1.0)
        for col in ("Total", "España", "EXT"):
            x[col] = x[col] * x.peso
        return x.groupby(["cod_barrio", "anio"], as_index=False)[["Total", "España", "EXT"]].sum()

    bo, ba = a_barrio(pesos(False)), a_barrio(pesos(True))
    comp = pd.read_csv(B1 / "valencia_barrio_variacion_2021_2025.csv", dtype={"cod_barrio": str}).set_index("cod_barrio")
    filas = []
    for etq, tabla in (("original", bo), ("alt", ba)):
        t = tabla.pivot_table(index="cod_barrio", columns="anio", values=["Total", "EXT"])
        for g in ("Total", "EXT"):
            tc = t[g]
            filas.append(pd.DataFrame({"cod": tc.index, "componente": f"stock_{g}_2025", "v": tc[2025].values, "version": etq}))
            filas.append(pd.DataFrame({"cod": tc.index, "componente": f"var_{g}_2021_2025", "v": (tc[2025] - tc[2021]).values, "version": etq}))
    W = pd.concat(filas, ignore_index=True).pivot_table(index=["cod", "componente"], columns="version", values="v").reset_index()
    W = W[W.cod != "sin_asignar"].rename(columns={"original": "valor_original", "alt": "reparto_catastro"})
    W["comparable_v12"] = W.cod.map(comp.comparable.astype(bool))
    W["signo_cambia_catastro_vs_original"] = np.where(W.valor_original != 0, (np.sign(W.valor_original) != np.sign(W.reparto_catastro)).astype(float), np.nan)
    W["dif_relativa"] = (W.reparto_catastro - W.valor_original).abs() / W.valor_original.abs().replace(0, np.nan)
    W["tipo_unidad"], W["periodo"], W["grupo"], W["cod_provincia"] = "barrio_valencia", "2021-2025", "seccion_a_barrio", "46"
    vv = W[(W.componente == "var_Total_2021_2025") & W.comparable_v12.fillna(False).astype(bool)].set_index("cod").valor_original
    chk = (vv - comp.var_Total_2021_2025.reindex(vv.index)).abs().max()
    st = W[W.componente == "stock_Total_2025"].set_index("cod")
    ppv = st.valor_original / viv.reindex(st.index)
    met = []
    for comp_, g in W.groupby("componente"):
        for etq, d in (("todos", g), ("comparables_v12", g[g.comparable_v12.fillna(False).astype(bool)])):
            if len(d) < 5:
                continue
            met.append({"componente": comp_, "subconjunto": etq, "n_barrios": len(d), "corr_original_vs_catastro": corr(d.valor_original, d.reparto_catastro), "dif_relativa_mediana": float(d.dif_relativa.median()),
                        "dif_relativa_max": float(d.dif_relativa.max()), "n_signo_cambia": int(d.signo_cambia_catastro_vs_original.sum()),
                        "barrios_signo_cambia": ",".join(d[d.signo_cambia_catastro_vs_original == 1].cod)})
    M = pd.DataFrame(met)
    guardar(M, "b1_reparto_metricas_valencia_barrio.csv")
    split = set(k[~k.seccion_en_un_barrio].cod_seccion)
    s25 = sec[sec.anio == 2025]
    sp = float(100 * s25[s25.cod_seccion.isin(split)].Total.sum() / s25.Total.sum())
    diag = {"poblacion_2025_en_secciones_repartidas_por_area_pct": round(sp, 2), "chequeo_reproduce_v12_max_abs_dif_var_total_barrios_comparables": None if pd.isna(chk) else float(chk),
            "corr_poblacion2025_barrio_vs_viviendas_inspire": corr(st.valor_original, viv.reindex(st.index)), "personas_por_vivienda_inspire_mediana": float(ppv.median()),
            "personas_por_vivienda_inspire_p5_p95": [float(ppv.quantile(0.05)), float(ppv.quantile(0.95))], "barrios_con_viviendas_inspire": int(viv.notna().sum()),
            "metricas": M.round(4).to_dict("records")}
    return W, diag


def tabla_uso_reparto() -> pd.DataFrame:
    filas = [
        ("V12-B1 municipal anual y por periodo (>= 10.000 hab.)", "output/v12/b1/contabilidad_*_municipio.csv.gz",
         "ninguno: componentes observados en microdatos MNP/EVR/EMCR por municipio de residencia; municipios < 10.000 hab. excluidos (PP999 solo suma en provincia)",
         "b1_reparto_alternativo.csv.gz (tipo_unidad = municipio, grupo observado_ge10000: contraste de dos repartos con lo observado)", "B2 relacion_precios (b2_flujos.py:253), B5 (b5_propiedad.py:129), base v12_pob_* (base_v12.py)"),
        ("V12-B1 provincia, CCAA y nacional", "output/v12/b1/contabilidad_*_provincia/ccaa/nacional.csv", "suma directa de flujos municipales incluido PP999: sin reparto", "-", "figuras y atlas V12, hechos V12-*"),
        ("V12-B1 València sección a barrio (stocks por nacionalidad)", "output/v12/b1/valencia_barrio_nacionalidad.csv; valencia_barrio_variacion_2021_2025.csv",
         "área: sección entera si >= 95 % de su área cae en un barrio; si no, peso_area (densidad uniforme)", "b1_reparto_alternativo.csv.gz (tipo_unidad = barrio_valencia)", "hechos V12 de València"),
        ("V12-B1 València distrito", "output/v12/b1/valencia_distrito_variacion_2021_2025.csv", "suma exacta de secciones (los distritos no cambian de sección): sin reparto", "-", "B7 distrito (b7_turismo.py:142)"),
        ("V12-B7 València VUT por barrio", "output/v12/b7", "mismo criterio de área que B1 (b7_turismo.py:133-135)", "misma ponderación alternativa aplicable (no aplicada a VUT)", "B7"),
        ("V12-B3 hogares 2021 por municipio y provincia", "output/v12/b3", "factor provincial: hogares de la muestra censal del 10 % x (hogares ECP 1-1-2021 / hogares de la muestra) (b3_hogares.py:56)",
         "no aplicado (hogares, no componentes de B1)", "B3 y B4 (2011-2021)"),
        ("V12-B4 hogares nuevos municipales 2021-2025", "output/v12/b4", "Δ población censo anual / personas por hogar 2021 del municipio (b4_oferta.py:146); no usa los componentes de B1", "no aplicado", "B4"),
        ("V15 reparto del residuo provincial a municipios < 10.000 hab.", "b1_reparto_alternativo.csv.gz (tipo_unidad = municipio, grupo resto_lt10000_o_intermitente)",
         "no existe en V12 (esos municipios no tienen componentes); V15 aporta dos repartos: por población inicial y por viviendas del Catastro", "ambos incluidos", "solo auditoría (C4)"),
    ]
    t = pd.DataFrame(filas, columns=["analisis_V12", "fichero", "criterio_de_reparto_usado_en_V12", "variable_alternativa_V15", "consumidores"])
    guardar(t, "b1_reparto_tabla_uso_v12.csv")
    return t


# ---------------------------------------------------------------- 5. disponibilidad de nacionalidad (P4)


AGREGADOS = re.compile(r"Europa|UE2|Africa|África|América|Asia|Oceanía|Extranjera|Total|Española|Apátridas|Resto|Otros")


def disponibilidad_p4() -> dict:
    p = padron_municipal()
    nac_unicas = sorted(p.nacionalidad.dropna().unique())
    individuales = [n for n in nac_unicas if not AGREGADOS.search(n)]
    filas = []
    for y, g in p.groupby("anio"):
        gt, ge, gi = g[g.nacionalidad == "Total"], g[g.nacionalidad == "Extranjera"], g[g.nacionalidad.isin(individuales)]
        filas.append({"fuente": "padron_continuo_municipal", "anio": int(y), "municipios": int(gt.cod_municipio.nunique()), "municipios_con_extranjera": int(ge.cod_municipio.nunique()),
                      "categorias_nacionalidad": int(g.nacionalidad.nunique()), "paises_individuales": int(gi.nacionalidad.nunique()), "celdas_pais_x_municipio": int(len(gi)),
                      "pct_celdas_cero": round(float(100 * (gi.poblacion == 0).mean()), 2), "poblacion_total_cubierta": float(gt.poblacion.sum()), "poblacion_extranjera": float(ge.poblacion.sum())})
    cm = hechos("pob_censo_anual", "municipio")
    cm["anio"] = cm.periodo.astype(int)
    for y, g in cm.groupby("anio"):
        gp = g[~g.desagregacion.isin(["nacionalidad=Total", "nacionalidad=España"])]
        tot = float(g[g.desagregacion == "nacionalidad=Total"].valor.sum())
        filas.append({"fuente": "censo_anual_municipal", "anio": int(y), "municipios": int(g.territorio_codigo.nunique()), "municipios_con_extranjera": int(g.territorio_codigo.nunique()),
                      "categorias_nacionalidad": int(g.desagregacion.nunique()), "paises_individuales": int(gp.desagregacion.nunique()), "celdas_pais_x_municipio": int(len(gp)),
                      "pct_celdas_cero": round(float(100 * (gp.valor == 0).mean()), 2), "poblacion_total_cubierta": tot, "poblacion_extranjera": tot - float(g[g.desagregacion == "nacionalidad=España"].valor.sum())})
    D = pd.DataFrame(filas)
    guardar(D, "disponibilidad_nacionalidad_municipal.csv")
    tot = p[p.nacionalidad == "Total"]
    anios = sorted(tot.anio.unique())
    balanc = int((tot.groupby("cod_municipio").anio.nunique() == len(anios)).sum())
    ind_anio = {int(y): set(g.nacionalidad.unique()) for y, g in p[p.nacionalidad.isin(individuales)].groupby("anio")}
    estables = sorted(set.intersection(*ind_anio.values()))
    pn = pd.read_csv(RAW / "v9" / "ine_padron_nacionalidad" / "padron_pais_nacimiento_2003_2022.csv.gz", usecols=["anio", "cod_municipio", "pais_nacimiento"], dtype=str)
    pn = pn[pn.cod_municipio.notna()]
    pnac = pn.groupby("anio").agg(municipios=("cod_municipio", "nunique"), categorias=("pais_nacimiento", "nunique")).reset_index()
    px = []
    for f in sorted((RAW / "ine_padron_pcaxis").glob("_px_*")):
        m = re.search(r"_a(\d{4})_l0_(\d+)\.csv", f.name)
        d = pd.read_csv(f, sep=";", encoding="utf-8-sig", dtype=str)
        px.append({"anio": int(m.group(1)), "fichero": m.group(2), "municipios_en_fichero": int(d.iloc[:, 1].dropna().nunique()), "dimension_nacionalidad": d.columns[2] if len(d.columns) > 3 else d.columns[-2], "nota": "solo provincia de València (46)"})
    px = pd.DataFrame(px)
    guardar(px, "disponibilidad_padron_pcaxis_valencia_provincia.csv")
    vb = hechos("vlc_padron_pob", "barrio", "sexo=Total")
    vb["anio"] = vb.periodo.str[:4].astype(int)
    vc = hechos("vlc_padron_ext_continente", "barrio")
    vc["anio"] = vc.periodo.str[:4].astype(int)
    vc["cont"] = vc.desagregacion.str.extract(r"continente=([^|]+)")[0]
    vc["sexo"] = vc.desagregacion.str.extract(r"sexo=(.+)$")[0]
    cont_cov = vc[vc.sexo == "Total"].groupby("cont").agg(anios=("anio", "nunique"), primer_anio=("anio", "min"), ultimo_anio=("anio", "max"), barrios=("territorio_codigo", "nunique")).reset_index()
    guardar(cont_cov, "valencia_barrio_continente_cobertura.csv")
    por_anio = vb.groupby("anio").territorio_codigo.nunique()
    guardar(por_anio.rename("barrios").reset_index(), "valencia_barrio_poblacion_cobertura.csv")
    sin_dato = sorted(set(range(2001, 2027)) - set(por_anio.index))
    vd = vb.groupby("anio").valor.sum()
    ine = p[(p.cod_municipio == "46250") & (p.nacionalidad == "Total")].set_index("anio").poblacion
    cen = hechos("pob_censo_anual", "municipio", "nacionalidad=Total")
    cen = cen[cen.territorio_codigo == "46250"].assign(anio=lambda d: d.periodo.astype(int)).set_index("anio").valor
    cc = pd.DataFrame({"ajuntament_suma_barrios": vd, "ine_padron": ine, "ine_censo_anual": cen})
    cc["dif_vs_padron_ine_pct"] = 100 * (cc.ajuntament_suma_barrios / cc.ine_padron - 1)
    cc["dif_vs_censo_anual_pct"] = 100 * (cc.ajuntament_suma_barrios / cc.ine_censo_anual - 1)
    guardar(cc.rename_axis("anio").reset_index(), "valencia_ajuntament_vs_ine.csv")
    pr, cr = D[D.fuente == "padron_continuo_municipal"], D[D.fuente == "censo_anual_municipal"]
    return {"padron_municipal_por_nacionalidad": {"anios": [int(pr.anio.min()), int(pr.anio.max())], "municipios_por_anio_min_max": [int(pr.municipios.min()), int(pr.municipios.max())],
                                                  "municipios_con_dato_en_todos_los_anios": balanc, "anios_antes_de_2015": int((pr.anio < 2015).sum()),
                                                  "categorias_nacionalidad_por_anio_min_max": [int(pr.categorias_nacionalidad.min()), int(pr.categorias_nacionalidad.max())],
                                                  "paises_individuales_por_anio_min_max": [int(pr.paises_individuales.min()), int(pr.paises_individuales.max())],
                                                  "paises_individuales_estables_todos_los_anios": estables, "paises_individuales_listado": individuales,
                                                  "pct_celdas_cero_2003": float(pr[pr.anio == 2003].pct_celdas_cero.iloc[0]), "pct_celdas_cero_2014": float(pr[pr.anio == 2014].pct_celdas_cero.iloc[0]),
                                                  "poblacion_total_2003_2014_2022": {int(a): float(pr[pr.anio == a].poblacion_total_cubierta.iloc[0]) for a in (2003, 2014, 2022)}},
            "censo_anual_municipal_por_pais": {"anios": [int(cr.anio.min()), int(cr.anio.max())], "municipios": int(cr.municipios.max()), "paises_individuales": int(cr.paises_individuales.max()),
                                                "pct_celdas_cero_2021": float(cr[cr.anio == 2021].pct_celdas_cero.iloc[0])},
            "padron_por_pais_de_nacimiento_municipal": {"anios": [int(pnac.anio.astype(int).min()), int(pnac.anio.astype(int).max())], "municipios_max": int(pnac.municipios.max()), "categorias_max": int(pnac.categorias.max())},
            "padron_pcaxis_valencia_provincia": {"anios": [int(px.anio.min()), int(px.anio.max())], "municipios_max": int(px.municipios_en_fichero.max()), "nota": "provincia 46; incluye 1998-2002"},
            "valencia_barrio_poblacion": {"barrios_por_anio_min_max": [int(por_anio.min()), int(por_anio.max())], "anios_con_dato": int(len(por_anio)), "anio_inicial": int(por_anio.index.min()),
                                          "anio_final": int(por_anio.index.max()), "anios_sin_dato_en_2001_2026": sin_dato, "anios_con_87_barrios": [int(a) for a in por_anio[por_anio == 87].index]},
            "valencia_barrio_nacionalidad_continente": {"categorias": cont_cov.to_dict("records"), "nota": "continente, sin país; nacionalidad por país solo en censo anual por sección 2021-2025"},
            "valencia_ajuntament_vs_ine": {"dif_vs_padron_ine_pct_min_max": [round(float(cc.dif_vs_padron_ine_pct.min()), 3), round(float(cc.dif_vs_padron_ine_pct.max()), 3)],
                                           "dif_vs_censo_anual_pct": {int(a): round(float(v), 3) for a, v in cc.dif_vs_censo_anual_pct.dropna().items()}}}


# ---------------------------------------------------------------- principal


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    diag: dict = {}
    diag["atipicos"] = atipicos()
    diag["coherencia_poblacion"] = coherencia_poblacion()
    diag["coherencia_hogares"] = coherencia_hogares()
    diag["residuo_b1_provincia"] = residuo_b1()
    diag["rupturas"] = {"epa_poblacion_vs_ecp": ruptura_epa_poblacion(), "padron_a_censo_anual_municipal": padron_a_censo(), "seccionado": seccionado(),
                        "evr_emcr_revisiones_y_empalme": revisiones_y_empalme()}
    df_mun, d_mun = reparto_municipal()
    W, d_val = reparto_valencia()
    tabla_uso_reparto()
    cols = ["tipo_unidad", "cod", "cod_provincia", "periodo", "componente", "grupo", "valor_original", "reparto_poblacion", "reparto_catastro", "poblacion_inicio", "viviendas_catastro", "anio_catastro",
            "signo_cambia_catastro_vs_original", "signo_cambia_poblacion_vs_original", "comparable_v12"]
    W["comparable_v12"] = W.comparable_v12.fillna(False).astype(float)
    unido = pd.concat([df_mun, W], ignore_index=True).reindex(columns=cols)
    unido.to_csv(OUT / "b1_reparto_alternativo.csv.gz", index=False, float_format="%.6g", compression={"method": "gzip", "mtime": 0})
    diag["reparto_b1"] = {"municipal": d_mun, "valencia_barrio": d_val, "filas_csv": int(len(unido)),
                          "criterio_v12": "B1 no reparte componentes a municipios: los obtiene observados (>= 10.000 hab.); solo reparte por área (secciones a barrios de València, stocks). Ver b1_reparto_tabla_uso_v12.csv"}
    diag["disponibilidad_p4"] = disponibilidad_p4()
    resultado = {
        "rama": "v15/auditoria/demografia_hogares",
        "pregunta": "¿Son coherentes y utilizables las fuentes de demografía y hogares (padrón/censo anual, ECP, EPA, censos, EVR/EMCR, MNP, València por barrio)? Atípicos, coherencia, rupturas, "
                    "reparto espacial de V12-B1 y cobertura para el shift-share de inmigración (P4).",
        "capa": "C4", "datos": "padrón continuo y censo anual (INE), ECP, EPA, censos 2011 y 2021, EVR/EMCR/EM, MNP, V12-B1/B3, Catastro (unidades urbanas e INSPIRE), padrón de València (Ajuntament)",
        "N": int(len(unido)), "metodo": "auditoría descriptiva: z robusto (mediana, MAD, umbral 5), coherencia de niveles y tasas entre fuentes, rupturas, reparto alternativo por viviendas del Catastro",
        "estimacion": None, "ic95": None, "p_ajustado": None, "nivel_evidencia": "DESCRIPTIVO", "diagnosticos": diag,
        "fuera_muestra": {"modelo": None, "rmse": None, "dm_vs_ar4": None},
        "notas": ["SEED=20261010 (sin aleatoriedad)", "cruces por código INE", "ningún efecto estimado", "solo agregados propios de INE, Catastro y Ajuntament de València"],
    }
    (OUT / "resultado.json").write_text(json.dumps(limpio(resultado), ensure_ascii=False, indent=1, default=a_json), encoding="utf-8")
    print("OK", len(unido))


if __name__ == "__main__":
    main()
