"""V16-F2.3 · Atlas multiescala: lectores y construcción de indicadores en formato largo.

Reglas (CLAUDE.md, plan V16 fase 2.3):
- Nunca se lee data/sealed. Toda lectura de la base o de data/processed/v16 filtra muestra_sellada_v6 == False y
  posterior_prereg == False; además, en municipio/distrito/seccion/partido_judicial (y provincia) se excluyen las
  unidades con holdout.unidad_sellada_v16 (solo booleanos). Esas unidades NO figuran: están en blanco «por validación
  sellada», no por falta de dato (K8 de docs/v16/decisiones.md).
- Supresión: base < 10 unidades (contratos, anuncios, hogares, viviendas, personas) o CV > 30 % => valor NaN y suprimida.
- Los valores sustitutos de provincia/comarca del ADRH nunca se muestran como municipales (suprimida, calidad propia).
- Intervalos 95 % solo donde hay error de estimación: alquiler SERPAVI (aproximación normal a la mediana con cuartiles y n),
  esfuerzo (propaga solo el IC del alquiler; la renta ADRH es un registro) y ECV (bootstrap del módulo f2_esfuerzo).
  Registros administrativos: sin intervalo, con marca de calidad.
"""
from __future__ import annotations

import gzip  # noqa: F401
import sys
from pathlib import Path

import duckdb
import numpy as np
import pandas as pd

RAIZ = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(RAIZ / "src"))
import holdout  # noqa: E402

SEED = 20261010
FECHA = "2026-10-17"
N_MIN = 10
CV_MAX = 0.30
SUPERFICIE_M2 = 80.0
BASE = RAIZ / "data" / "base" / "hechos.parquet"
P16 = RAIZ / "data" / "processed" / "v16"
CENSO = RAIZ / "data" / "raw" / "v11" / "ine_censo2021"
INTERV = RAIZ / "output" / "v16" / "f1" / "intervenciones.csv"
ESFUERZO_ECV = RAIZ / "output" / "v16" / "f2_esfuerzo" / "esfuerzo_por_anio.csv"
LANZ_CCAA = RAIZ / "output" / "v16" / "f2_hechos" / "lanzamientos_ccaa.csv"
GEO = RAIZ / "data" / "base" / "geo"
COLS = ["territorio_codigo", "nivel", "periodo", "indicador", "valor", "ic_inf", "ic_sup", "calidad", "suprimida", "fuente",
        "unidad", "n_base", "cv"]
FINOS = ("municipio", "distrito", "seccion", "partido_judicial", "provincia")
ANOS_FINOS = None  # None = todos los años; si el fichero superase 50 MB, restringir aquí distrito y sección
PROV_SMOKE = ("08", "46", "41")
NUTS2 = {"ES11": "12", "ES12": "03", "ES13": "06", "ES21": "16", "ES22": "15", "ES23": "17", "ES24": "02", "ES30": "13",
         "ES41": "07", "ES42": "08", "ES43": "11", "ES51": "09", "ES52": "10", "ES53": "04", "ES61": "01", "ES62": "14",
         "ES63": "18", "ES64": "19", "ES70": "05"}
TSJ = [("ANDALUCIA", "01"), ("ARAGON", "02"), ("ASTURIAS", "03"), ("BALEARS", "04"), ("CANARIAS", "05"), ("CANTABRIA", "06"),
       ("CASTILLA Y LEON", "07"), ("CASTILLA - LA MANCHA", "08"), ("CATALUNA", "09"), ("VALENCIANA", "10"),
       ("EXTREMADURA", "11"), ("GALICIA", "12"), ("MADRID", "13"), ("MURCIA", "14"), ("NAVARRA", "15"), ("PAIS VASCO", "16"),
       ("RIOJA", "17")]

_CACHE: dict[str, dict[str, bool]] = {}


# ------------------------------------------------------------------------------------------------ sellado
def es_sellada(codigos: pd.Series, nivel: str) -> pd.Series:
    """True si la unidad está sellada en V16 (holdout.unidad_sellada_v16; solo booleanos). Memoriza por nivel."""
    c = codigos.astype(str)
    memo = _CACHE.setdefault(nivel, {})
    nuevos = pd.Series(sorted(set(c) - set(memo)), dtype=str)
    if len(nuevos):
        r = holdout.unidad_sellada_v16(nuevos, nivel)
        memo.update(dict(zip(nuevos.tolist(), [bool(x) for x in r.tolist()])))
    return c.map(memo).astype(bool)


def sin_sellados(df: pd.DataFrame, col: str = "territorio_codigo") -> pd.DataFrame:
    if df.empty:
        return df
    mant = pd.Series(True, index=df.index)
    for nivel, idx in df.groupby("nivel").groups.items():
        if nivel in FINOS:
            mant.loc[idx] = ~es_sellada(df.loc[idx, col], nivel).values
    return df[mant]


def _smoke_sql(smoke: bool) -> str:
    if not smoke:
        return "true"
    p = ",".join(f"'{x}'" for x in PROV_SMOKE)
    return (f"(nivel in ('nacional','ccaa','provincia') or substr(territorio_codigo,1,2) in ({p}) "
            f"or (starts_with(territorio_codigo,'PJ-') and substr(territorio_codigo,4,2) in ({p})))")


def _smoke_df(df: pd.DataFrame, smoke: bool, col: str = "territorio_codigo") -> pd.DataFrame:
    if not smoke:
        return df
    c = df[col].astype(str)
    ok = df.nivel.isin(["nacional", "ccaa", "provincia"]) | c.str[:2].isin(PROV_SMOKE) | (c.str.startswith("PJ-") & c.str[3:5].isin(PROV_SMOKE))
    return df[ok]


def leer(ruta: Path, where: str, smoke: bool) -> pd.DataFrame:
    """Lee un parquet con filtros de muestra (no sellada v6, no posterior al pre-registro) y de sellado V16."""
    con = duckdb.connect()
    d = con.execute(f"""SELECT territorio_codigo, nivel, periodo, variable, desagregacion, valor, metodo_dato, fuente
                        FROM read_parquet('{ruta}') WHERE ({where}) AND NOT coalesce(muestra_sellada_v6, false)
                        AND NOT coalesce(posterior_prereg, false) AND {_smoke_sql(smoke)}""").df()
    con.close()
    d["territorio_codigo"] = d.territorio_codigo.astype(str)
    return sin_sellados(d).drop_duplicates(["territorio_codigo", "nivel", "periodo", "variable", "desagregacion"])


# ------------------------------------------------------------------------------------------------ utilidades
def estandar(df: pd.DataFrame, indicador: str, unidad: str, fuente: str, calidad: str | pd.Series = "") -> pd.DataFrame:
    o = pd.DataFrame({"territorio_codigo": df.territorio_codigo.astype(str).values, "nivel": df.nivel.values,
                      "periodo": df.periodo.astype(str).values, "indicador": indicador,
                      "valor": df["valor"].astype(float).values})
    for c in ("ic_inf", "ic_sup", "n_base", "cv"):
        o[c] = df[c].astype(float).values if c in df else np.nan
    o["calidad"] = (calidad.values if isinstance(calidad, pd.Series) else calidad)
    o["suprimida"] = df["suprimida"].fillna(False).astype(bool).values if "suprimida" in df else False
    o["fuente"], o["unidad"] = fuente, unidad
    return o[COLS].reset_index(drop=True)


def periodos_finos(o: pd.DataFrame) -> pd.DataFrame:
    """Distrito y sección solo en años de referencia (tamaño del fichero < 50 MB). Periodos no anuales se conservan."""
    if ANOS_FINOS is None:
        return o
    fino = o.nivel.isin(["distrito", "seccion"]) & o.periodo.str.fullmatch(r"\d{4}")
    return o[~fino | o.periodo.isin(ANOS_FINOS)]


def suprimir(o: pd.DataFrame) -> pd.DataFrame:
    """Aplica la regla: base < 10 o CV > 30 % => valor/IC/base/CV a NaN, suprimida = True y motivo en calidad."""
    o = o.copy()
    m_n = o.n_base.notna() & (o.n_base < N_MIN)
    m_cv = o.cv.notna() & (o.cv > CV_MAX)
    previa = o.suprimida.astype(bool)
    sup = m_n | m_cv | previa
    motivo = np.select([previa & ~(m_n | m_cv), m_n, m_cv], ["", f"suprimida: base < {N_MIN}", f"suprimida: CV > {int(CV_MAX * 100)} %"], "")
    o["calidad"] = np.where(motivo != "", (o.calidad.astype(str) + "; " + motivo).str.strip("; "), o.calidad)
    o["suprimida"] = sup
    o.loc[sup, ["valor", "ic_inf", "ic_sup", "n_base", "cv"]] = np.nan
    return o


def _num(s: pd.Series) -> pd.Series:
    return pd.to_numeric(s.astype(str).str.replace(".", "", regex=False).str.replace(",", ".", regex=False), errors="coerce")


# ------------------------------------------------------------------------------------------------ Censo 2021 (tablas INE)
def censo_tablas() -> dict[str, pd.DataFrame]:
    """59525 (principal/no principal, municipal) y 59531 (vacías y esporádicas por consumo eléctrico). Solo agregados INE."""
    t = pd.read_csv(CENSO / "censo2021_tpx59525.csv", sep=";", encoding="utf-8-sig")
    t.columns = ["nac", "mun", "tipo", "total"]
    t["total"] = _num(t.total)
    m = t[t.mun.notna()].copy()
    m["cod"] = m.mun.str[:5]
    w = m.pivot_table(index="cod", columns="tipo", values="total", aggfunc="first")
    w = w.rename(columns={"Total": "total", "Vivienda principal": "principal", "Vivienda no principal": "no_principal"})
    p = pd.read_csv(CENSO / "censo2021_tpx59531.csv", sep=";", encoding="utf-8-sig")
    p.columns = ["nac", "ccaa", "prov", "mun", "tipo", "total"]
    p["total"] = _num(p.total)
    p["bruto"] = p.total
    return {"p59525": w.reset_index(), "p59531": p}


def _prov_ccaa() -> pd.Series:
    g = pd.read_parquet(GEO / "provincias.parquet", columns=["cod_provincia", "cod_ccaa"])
    return g.set_index("cod_provincia").cod_ccaa.astype(str)


def viviendas_municipio() -> pd.Series:
    """Viviendas totales del Censo 2021 por municipio (denominador de tasas; es un recuento oficial)."""
    return censo_tablas()["p59525"].set_index("cod").total
