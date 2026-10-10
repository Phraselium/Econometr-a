"""P-A (C1): lectura de insumos. Sin red: lee data/ y data/raw/v3/pa_aux/ (cache de la API del INE)."""
from __future__ import annotations

import json
import re
import sys
import unicodedata
from pathlib import Path

import numpy as np
import pandas as pd

RAIZ = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(RAIZ / "src"))
import holdout  # noqa: E402

RAW = RAIZ / "data" / "raw"
V3 = RAW / "v3"
AUX = RAIZ / "data" / "raw" / "v3" / "pa_aux"
SEED = 20261010


def clave(s: str) -> str:
    """Clave de nombre de provincia comparable entre fuentes (sin tildes, sin artículos)."""
    s = unicodedata.normalize("NFKD", str(s)).encode("ascii", "ignore").decode().lower()
    s = s.split("/")[0].split(",")[0].strip()
    for pref in ("a ", "las ", "la ", "illes ", "el "):
        if s.startswith(pref):
            s = s[len(pref):]
    return s.strip()


def panel(nombre: str) -> pd.DataFrame:
    return holdout.load_full(nombre, "PA")


def mapa_prov(pp: pd.DataFrame) -> dict[str, str]:
    t = pp[["cod_prov", "provincia"]].drop_duplicates()
    return {clave(r.provincia): str(r.cod_prov).zfill(2) for r in t.itertuples()}


def _json(nombre: str):
    return json.loads((AUX / nombre).read_text())


def censo2011_provincias() -> pd.DataFrame:
    """Censo 2011, tabla INE 3457: viviendas total y principal por provincia (clave: nombre)."""
    out: dict[str, dict[str, float]] = {}
    for x in _json("ine_t3457.json"):
        n = x["Nombre"]
        v = x["Data"][0].get("Valor") if x["Data"] else None
        m = re.match(r"(.+?)\. (Total viviendas|Vivienda principal|Vivienda no principal|Vivienda vacía)\.", n)
        if m and v is not None:
            out.setdefault(clave(m.group(1)), {}).setdefault(m.group(2), v)
    df = pd.DataFrame(out).T
    df.index.name = "clave"
    return df


def censo2011_nacional() -> dict[str, float]:
    for x in _json("ine_t3457.json"):
        if x["Nombre"].startswith("Total Nacional. Total viviendas"):
            tot = x["Data"][0]["Valor"]
        if x["Nombre"].startswith("Total Nacional. Vivienda principal"):
            pri = x["Data"][0]["Valor"]
        if x["Nombre"].startswith("Total Nacional. Vivienda vacía"):
            vac = x["Data"][0]["Valor"]
    return {"total": tot, "principal": pri, "vacia": vac}


def censo2011_municipios() -> pd.DataFrame:
    """Censo 2011, tabla INE 3456 (municipios de >2.000 habitantes; solo nombre, sin código)."""
    filas = []
    for x in _json("ine_t3456.json"):
        m = re.match(r"(.+?)\. (Total viviendas|Vivienda principal|Vivienda vacía)\.", x["Nombre"])
        if m and x["Data"] and x["Data"][0].get("Valor") is not None:
            filas.append((m.group(1), m.group(2), x["Data"][0]["Valor"]))
    d = pd.DataFrame(filas, columns=["nombre", "m", "v"]).drop_duplicates(["nombre", "m"])
    return d.pivot(index="nombre", columns="m", values="v")


def censo2021_municipios() -> pd.DataFrame:
    m = pd.read_csv(V3 / "ine_v3_censo2021_municipio_viviendas.csv", dtype={"codigo": str})
    m = m[m.nivel == "municipio"]
    d = m.pivot(index="codigo", columns="serie", values="valor")
    d["nombre"] = m.drop_duplicates("codigo").set_index("codigo").territorio
    return d


def censo2021_hogares_nacional() -> float:
    for x in _json("ine_t59533.json"):
        if x["Nombre"].startswith("Total (tipo de hogar)") or x["Nombre"].startswith("Total (tamaño de municipio), Total"):
            return float(x["Data"][0]["Valor"])
    return 18539223.0


def vacias2021() -> pd.DataFrame:
    """Censo 2021, tabla INE 59531: viviendas totales, vacías y de uso esporádico por municipio."""
    filas = []
    for x in _json("ine_t59531.json"):
        m = re.match(r"(\d{5}) (.+), (Viviendas totales|Viviendas vacías|Viviendas de uso esporádico|Viviendas con bajo consumo)$",
                     x["Nombre"])
        if m and x["Data"] and x["Data"][0].get("Valor") is not None and not x["Data"][0].get("Secreto"):
            filas.append((m.group(1), m.group(2), m.group(3), x["Data"][0]["Valor"]))
    d = pd.DataFrame(filas, columns=["codigo", "nombre", "m", "v"])
    p = d.pivot(index="codigo", columns="m", values="v")
    p["nombre"] = d.drop_duplicates("codigo").set_index("codigo").nombre
    p.columns.name = None
    return p.rename(columns={"Viviendas totales": "total", "Viviendas vacías": "vacias",
                             "Viviendas de uso esporádico": "esporadico", "Viviendas con bajo consumo": "bajo"})


def vacias2021_nacional() -> dict[str, float]:
    out = {}
    for x in _json("ine_t59531.json")[:6]:
        n = x["Nombre"].replace("Total Nacional, ", "")
        out[n] = x["Data"][0]["Valor"]
    return {"total": out["Viviendas totales"], "vacias": out["Viviendas vacías"],
            "esporadico": out["Viviendas de uso esporádico"], "bajo": out["Viviendas con bajo consumo"]}


def epa_parentesco() -> pd.DataFrame:
    """EPA, tabla INE 65944: población de 25-29 y 30-34 por relación de parentesco (miles, media anual)."""
    filas = []
    for x in _json("ine_t65944.json"):
        m = re.match(r"Total Nacional\. Ambos sexos\. De (25 a 29|30 a 34) años\. (Total|Hijo/a)\. Personas", x["Nombre"])
        if m:
            for d in x["Data"]:
                filas.append((int(d["Anyo"]), m.group(1), m.group(2), d["Valor"]))
    t = pd.DataFrame(filas, columns=["anio", "edad", "rel", "v"])
    p = t.pivot_table(index="anio", columns=["edad", "rel"], values="v", aggfunc="first")
    out = pd.DataFrame({"pob_25_34": (p[("25 a 29", "Total")] + p[("30 a 34", "Total")]) * 1000,
                        "hijos_25_34": (p[("25 a 29", "Hijo/a")] + p[("30 a 34", "Hijo/a")]) * 1000})
    out["tasa_epa"] = 100 * out.hijos_25_34 / out.pob_25_34
    return out


def adrh_hogar() -> pd.DataFrame:
    """ADRH: renta neta media por hogar por sección (largo: codigo, anio, valor)."""
    d = pd.read_csv(V3 / "ine_v3_gis_seccion.csv.gz", dtype={"codigo": str},
                    usecols=["codigo", "campo", "valor", "servicio", "indicador", "anio"])
    d = d[d.indicador.fillna("").str.startswith("Renta neta media por hogar") & (d.campo == "dato2")]
    d = d.drop_duplicates(["codigo", "anio"])  # los servicios por hogar y por persona de un mismo año repiten el valor
    return d[["codigo", "anio", "valor"]].rename(columns={"valor": "renta_hogar"}).dropna()


def censo2021_secciones() -> pd.DataFrame:
    """Hogares (t21_1), personas (t1_1), viviendas principales y alquiler por sección."""
    d = pd.read_csv(V3 / "ine_v3_censo2021_seccion_indicadores.csv.gz", dtype={"codigo": str},
                    usecols=["codigo", "serie", "valor"])
    d = d[d.serie.isin(["t21_1", "t1_1", "t19_1", "t20_2"])]
    p = d.pivot(index="codigo", columns="serie", values="valor")
    return p.rename(columns={"t21_1": "hogares", "t1_1": "personas", "t19_1": "principales", "t20_2": "alquiler"})


def catastro() -> pd.DataFrame:
    c = pd.read_csv(RAW / "catastro_urbana_municipios.csv.gz", dtype={"codigo": str, "provincia_codigo": str},
                    usecols=["periodo", "codigo", "valor", "provincia_codigo", "unidad"])
    c = c[c.unidad == "unidades_urbanas_residenciales"]
    return c.rename(columns={"valor": "uu_res", "provincia_codigo": "cod_prov"})[["periodo", "codigo", "cod_prov", "uu_res"]]


def mivau_nacional_anual() -> pd.DataFrame:
    a = pd.read_csv(RAW / "mivau_v2_iniciadas_terminadas_prov.csv")
    lib = a[(a.nivel == "nacional") & a.serie.str.contains("viv_libres_terminadas_anual")].set_index("periodo").valor
    p = pd.read_csv(RAW / "mivau_v2_protegida.csv")
    prot = p[(p.nivel == "nacional") & (p.tabla_codigo == 31306000)].set_index("periodo").valor
    q = pd.read_csv(RAW / "mivau_parque.csv")
    parque = q[q.nivel == "nacional"].set_index("periodo").valor
    for sr in (lib, prot, parque):
        sr.index = sr.index.astype(int)
    out = pd.concat([lib.rename("libres"), prot.rename("protegida"), parque.rename("parque")], axis=1)
    return out.sort_index()


def nacional_q() -> pd.DataFrame:
    return panel("nacional_q_v2").set_index("trimestre")


def registradores_prov() -> pd.DataFrame:
    r = pd.read_csv(RAW / "pdf" / "registradores_opendata_anual.csv")
    r = r[(r.serie == "compraventas_viv_pm2") & (r.nivel == "provincia")].copy()
    r["clave"] = r.territorio.map(clave)
    return r[["periodo", "clave", "valor"]].rename(columns={"valor": "reg_pm2"})


def incasol_renta(anio: int) -> pd.DataFrame:
    """Renta media mensual de los contratos depositados (Incasòl), por municipio, año natural completo."""
    d = pd.read_csv(V3 / "incasol_fianzas_municipio_v3.csv.gz", dtype={"codigo": str})
    d = d[d.periodo == f"{anio} gener-desembre"]
    d["tipo"] = np.where(d.serie.str.contains("renta_media"), "renta",
                         np.where(d.serie.str.contains("TOTAL_bandas"), "tot", "n"))
    n = d[d.tipo == "n"].set_index(["codigo", "banda"]).valor.rename("n")
    r = d[d.tipo == "renta"].set_index(["codigo", "banda"]).valor.rename("renta")
    x = pd.concat([n, r], axis=1).dropna()
    x = x[x.n > 0]
    g = x.groupby(level=0).apply(lambda t: pd.Series({"renta_mes": np.average(t.renta, weights=t.n), "n_contratos": t.n.sum()}),
                                 include_groups=False)
    return g
