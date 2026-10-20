"""V18 · E2 (topes al alquiler) · capa de datos: paneles de Cataluña con el sellado de V18 (sellado.filtrar + holdout.excluir_sellados_v6).

Análisis V18; capa C4; pre-registro interno plan-replicacion-v18. Sin red; SEED 20261010.
Cada serie pasa por _e2e8_comun.leer_hechos / filtrar. La lista de municipios regulados por la Ley 11/2020 y las fechas de las zonas tensionadas
son hechos normativos (data/raw/v3/cataluna_contencion_rentas_v3.csv), no resultados; la geometría (data/base/geo) solo da distancias y vecindad.
"""
from __future__ import annotations

import re
import unicodedata

import geopandas as gpd
import numpy as np
import pandas as pd

import _e2e8_comun as K

RAW = K.RAIZ / "data" / "raw"
CAT = ("08", "17", "25", "43")
Q_INI, Q_FIN = "2019T1", "2022T1"
PER13 = K.trimestres(Q_INI, Q_FIN)
BARCELONA = "08019"


def regulados_ley11() -> set[str]:
    c = pd.read_csv(RAW / "v3" / "cataluna_contencion_rentas_v3.csv", dtype=str)
    return set(c[c.regimen == "ley11_2020"].cod_ine.str.zfill(5))


def anual(df: pd.DataFrame) -> pd.DataFrame:
    return df.pivot_table(index="territorio_codigo", columns="periodo", values="valor", aggfunc="first")


def serie_t(variable: str, ini: str = "2019T1", fin: str = "2026T1") -> pd.DataFrame:
    s = K.leer_hechos(variable, "municipio", "T")
    return K.ancho(s, K.trimestres(ini, fin))


def poblacion() -> pd.DataFrame:
    """Padrón municipal (total) por año 2019-2022, con el sellado de V18 (variable «padron_municipal_nacionalidad», tope 2022)."""
    d = pd.read_csv(RAW / "v9" / "ine_padron_nacionalidad" / "padron_nacionalidad_2003_2022.csv.gz", dtype=str)
    d = d[d.nacionalidad == "Total"].copy()
    d["cod"] = d.cod_municipio.str.zfill(5)
    d["periodo"] = d.anio.astype(str)
    d["valor"] = pd.to_numeric(d.poblacion, errors="coerce")
    d = K.filtrar(d, "cod", "municipio", "periodo", "padron_municipal_nacionalidad", "A")
    w = d.pivot_table(index="cod", columns="periodo", values="valor", aggfunc="first")
    return w


def geografia() -> dict:
    """Centroides (km, EPSG:25831) de los municipios de Cataluña, vecindad por frontera común y 42 conglomerados espaciales (k-medias) que
    sustituyen a las comarcas, que no están en el repositorio."""
    m = gpd.read_parquet(K.GEO)
    m = m[m.cod_provincia.isin(CAT)].copy().to_crs(25831)
    m["cod"] = m.cod_municipio.astype(str).str.zfill(5)
    m = K.holdout.excluir_sellados_v6(m, "cod", "municipio")      # ninguna provincia catalana está sellada en v6: no cambia nada
    m = m.sort_values("cod").reset_index(drop=True)
    c = np.column_stack([m.geometry.centroid.x, m.geometry.centroid.y]) / 1000.0
    from sklearn.cluster import KMeans
    km = KMeans(n_clusters=42, n_init=10, random_state=K.SEMILLA).fit(c)
    cod = m.cod.values
    idx = {x: i for i, x in enumerate(cod)}
    sidx = m.geometry.sindex
    veci: dict[str, set[str]] = {x: set() for x in cod}
    for i, g in enumerate(m.geometry):
        for j in sidx.query(g, predicate="touches"):
            if j != i:
                veci[cod[i]].add(cod[j])
    return {"cod": cod, "xy": c, "idx": idx, "conglomerado": dict(zip(cod, km.labels_)), "vecinos": veci}


def dist_min(xy: np.ndarray, origen: np.ndarray) -> np.ndarray:
    d = np.sqrt(((xy[:, None, :] - origen[None, :, :]) ** 2).sum(-1))
    return d.min(1)


# --------------------------------------------------------------------------------------------- correspondencia por nombre (MIVAU)
CODAUTO = {"Andalucía": "01", "Cantabria": "06", "Castilla Y León": "07", "Castilla-La Mancha": "08", "Cataluña": "09",
           "Comunidad Valenciana": "10", "Extremadura": "11", "Galicia": "12"}


def _clave(nombre: str) -> str:
    s = unicodedata.normalize("NFKD", str(nombre)).encode("ascii", "ignore").decode().lower()
    s = re.sub(r"[^a-z0-9 ]", " ", s.replace("'", " "))
    return " ".join(sorted(s.split()))


def correspondencia_ine(df: pd.DataFrame, col_nombre: str = "territorio", col_ccaa: str = "ccaa") -> pd.DataFrame:
    """Código INE de cada municipio de MIVAU (que solo trae nombre) por nombre dentro de su comunidad, con el diccionario oficial del INE.
    Devuelve (nombre, ccaa) -> cod; los no resueltos o ambiguos quedan sin código y se cuentan. Solo las 8 CCAA de régimen común no selladas."""
    d = pd.read_excel(RAW / "ine_diccionario_municipios_2026.xlsx", header=1, dtype=str)
    d["cod"] = d.CPRO.str.zfill(2) + d.CMUN.str.zfill(3)
    d["clave"] = d.NOMBRE.map(_clave)
    out = []
    for nombre, ccaa in df[[col_nombre, col_ccaa]].drop_duplicates().itertuples(index=False):
        ca = CODAUTO.get(ccaa)
        if ca is None:
            continue
        cand = d[(d.CODAUTO.str.zfill(2) == ca) & (d.clave == _clave(nombre))]
        if len(cand) == 0:
            cand = d[(d.CODAUTO.str.zfill(2) == ca) & d.NOMBRE.map(lambda x: _clave(x.split("/")[0]) == _clave(nombre) or any(_clave(p) == _clave(nombre) for p in x.split("/")))]
        out.append((nombre, ccaa, cand.cod.iloc[0] if len(cand) == 1 else None, len(cand)))
    return pd.DataFrame(out, columns=[col_nombre, col_ccaa, "cod", "n_candidatos"])


def mivau_municipal(archivo: str, variable: str) -> pd.DataFrame:
    """Serie municipal trimestral de MIVAU con código INE por nombre (diccionario oficial) y sellado de V18."""
    t = pd.read_csv(RAW / archivo, dtype=str)
    t = t[t.ccaa.isin(CODAUTO)]
    corr = correspondencia_ine(t.dropna(subset=["ccaa"]))
    t = t.merge(corr[["territorio", "ccaa", "cod"]], on=["territorio", "ccaa"], how="inner").dropna(subset=["cod"])
    t["valor"] = pd.to_numeric(t.valor, errors="coerce")
    t["periodo"] = t.periodo.astype(str)
    t = t[t.periodo.str.fullmatch(r"\d{4}T[1-4]")]
    t = K.filtrar(t, "cod", "municipio", "periodo", variable, "T")
    return t.rename(columns={"cod": "territorio_codigo"})[["territorio_codigo", "periodo", "valor"]]


def paro_trimestral() -> pd.DataFrame:
    """Paro registrado por municipio y trimestre (media de los meses del fichero mensual del SEPE; adenda R-1). El anual de la base no tiene 2020.
    El mensual es el mismo dato que «sepe_paro_registrado_media_anual» y hereda su tope temporal (regla (f) de la adenda 1.4: mismo dato, mismo
    nivel); pasa por K.filtrar (sellado.filtrar + holdout.excluir_sellados_v6). Los meses con «<5» vienen vacíos y diciembre de 2020 no está en el fichero (202012 ausente: 2020T4 = media de octubre y noviembre);
    la media trimestral exige al menos 2 meses con dato."""
    m = pd.read_csv(RAW / "v9" / "sepe_municipios" / "paro_registrado_municipio_mensual.csv.gz", dtype={"cod_municipio": str, "mes": str})
    m["cod_municipio"] = m.cod_municipio.str.zfill(5)
    m["anio"] = m["mes"].str[:4]
    m = m[(m.anio >= "2019") & (m.anio <= "2022")]
    m = K.filtrar(m, "cod_municipio", "municipio", "anio", "sepe_paro_registrado_media_anual", "A")
    m["trim"] = m["anio"] + "T" + ((m["mes"].str[4:6].astype(int) - 1) // 3 + 1).astype(str)
    g = m.groupby(["cod_municipio", "trim"]).paro_registrado.agg(["mean", "count"])
    g.loc[g["count"] < 2, "mean"] = np.nan
    return g["mean"].unstack().reindex(columns=K.trimestres("2019T1", "2022T4"))
