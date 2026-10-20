"""V18 · E8 (ITP por comunidades) · datos: calendario de cambios del tipo general con las reglas de codificación de la adenda (R-18) y paneles
provinciales y municipales con el sellado de V18.

Análisis V18; capa C4; pre-registro interno plan-replicacion-v18. Sin red; SEED 20261010.
Reglas de codificación de fechas (adenda R-18, fijadas antes de estimar):
  - la fecha es la de entrada en vigor; en datos mensuales cuenta el mes de entrada en vigor si es día 15 o anterior y, si no, el siguiente; en trimestrales, el
    trimestre de ese mes;
  - la dosis es la variación del tipo general en puntos (en escalas, el tipo mínimo de la escala, que es el «tipo general» de la base de intervenciones);
  - dos cambios de una comunidad a menos de 12 meses se tratan como un solo evento, con la dosis acumulada en la primera fecha.
Calidad de las fechas: la base de intervenciones (V16) recoge los tipos de las memorias del Ministerio de Hacienda (fuente SECUNDARIA): las fechas de
1 de enero son aproximadas y las demás constan en la memoria, pero ninguna está contrastada con el BOE ni con el diario autonómico (la fuente
`itp_fechas_entrada_en_vigor` del sellado es posterior a la etiqueta y no está descargada). Se dice en cada resultado.
"""
from __future__ import annotations

import numpy as np
import pandas as pd

import _e2e8_comun as K

RAW = K.RAIZ / "data" / "raw"
CCAA_E8 = {"01": "Andalucía", "06": "Cantabria", "07": "Castilla y León", "08": "Castilla-La Mancha", "09": "Cataluña", "10": "Comunitat Valenciana",
           "11": "Extremadura", "12": "Galicia"}
MESES_MAX = 12


def provincias_e8() -> dict[str, str]:
    """Provincia -> código de comunidad INE para las 8 comunidades de régimen común no selladas (geo/provincias.parquet)."""
    import geopandas as gpd
    p = gpd.read_parquet(K.RAIZ / "data" / "base" / "geo" / "provincias.parquet")
    p = K.holdout.excluir_sellados_v6(p, "cod_provincia", "provincia")      # las 8 comunidades de E8 no contienen provincias selladas en v6
    return {r.cod_provincia: r.cod_ccaa for r in p.itertuples() if r.cod_ccaa in CCAA_E8}


def centroides_provincias(cods) -> np.ndarray:
    """Centroides (km, EPSG:25830) de las provincias dadas (geo/provincias.parquet; solo geometría, sin resultados)."""
    import geopandas as gpd
    p = gpd.read_parquet(K.RAIZ / "data" / "base" / "geo" / "provincias.parquet")
    p = K.holdout.excluir_sellados_v6(p, "cod_provincia", "provincia").to_crs(25830)
    p = p.set_index("cod_provincia").reindex(list(cods))
    c = p.geometry.centroid
    return np.column_stack([c.x, c.y]) / 1000.0


def tipos_generales() -> pd.DataFrame:
    """Serie de tipos generales del ITP por comunidad (base de intervenciones de V16: hechos normativos; no son resultados)."""
    d = pd.read_csv(RAW / "v16" / "intervenciones" / "intervenciones.csv", dtype=str)
    d = d[(d.instrumento == "itp") & d.cod_ine.isin(CCAA_E8) & d.parametro.str.startswith("tipo general ITP")].copy()
    d["fecha"] = pd.to_datetime(d.fecha_efecto)
    d["tipo"] = d.valor.astype(float)
    d["aprox"] = d.notas.str.contains("Fecha de efecto aproximada", na=False)
    return d.sort_values(["cod_ine", "fecha"])[["cod_ine", "fecha", "tipo", "aprox"]].reset_index(drop=True)


def eventos(modo: str = "exacta") -> pd.DataFrame:
    """Cambios del tipo general por comunidad con la regla de fusión a menos de 12 meses. modo: «exacta» (fechas de la base), «enero» (1 de enero del año),
    «mas3» y «menos3» (fechas desplazadas ±3 meses). Devuelve cod_ine, fecha, dosis, aprox, fecha_original."""
    t = tipos_generales()
    filas = []
    for cod, g in t.groupby("cod_ine"):
        g = g.sort_values("fecha")
        previo = g.tipo.iloc[0]
        for r in g.iloc[1:].itertuples():
            if r.tipo != previo:
                filas.append((cod, r.fecha, r.tipo - previo, r.aprox))
            previo = r.tipo
    e = pd.DataFrame(filas, columns=["cod_ine", "fecha_original", "dosis", "aprox"])
    if modo == "enero":
        e["fecha"] = pd.to_datetime(e.fecha_original.dt.year.astype(str) + "-01-01")
    elif modo == "mas3":
        e["fecha"] = e.fecha_original + pd.DateOffset(months=3)
    elif modo == "menos3":
        e["fecha"] = e.fecha_original - pd.DateOffset(months=3)
    else:
        e["fecha"] = e.fecha_original
    out = []
    for cod, g in e.sort_values("fecha").groupby("cod_ine"):
        ini, acum, aprox, orig = None, 0.0, False, None
        for r in g.itertuples():
            if ini is not None and r.fecha < ini + pd.DateOffset(months=MESES_MAX):
                acum += r.dosis
                aprox = aprox or r.aprox
                continue
            if ini is not None and acum != 0:
                out.append((cod, ini, acum, aprox, orig))
            ini, acum, aprox, orig = r.fecha, r.dosis, r.aprox, r.fecha_original
        if ini is not None and acum != 0:
            out.append((cod, ini, acum, aprox, orig))
    return pd.DataFrame(out, columns=["cod_ine", "fecha", "dosis", "aprox", "fecha_original"])


def mes_codificado(f: pd.Timestamp) -> str:
    """Mes de entrada en vigor si el día es ≤ 15; si no, el siguiente (adenda R-18)."""
    m = f.to_period("M") if f.day <= 15 else (f.to_period("M") + 1)
    return str(m)


def trimestre_codificado(f: pd.Timestamp) -> str:
    return str(pd.Period(mes_codificado(f), "M").asfreq("Q")).replace("Q", "T")


def calendarios(ev: pd.DataFrame, periodos: list[str], frecuencia: str, ccaa: list[str] | None = None) -> tuple[np.ndarray, list[str]]:
    """Matriz (CCAA × periodos) con el nivel acumulado de la dosis (variación del tipo general respecto al de 2010) en cada periodo.
    Supuesto declarado: sin cambios en 2007-2009 (la base de intervenciones empieza en 2010)."""
    ccaa = sorted(CCAA_E8) if ccaa is None else sorted(ccaa)
    Dc = np.zeros((len(ccaa), len(periodos)))
    for r in ev.itertuples():
        if r.cod_ine not in ccaa:
            continue
        p = mes_codificado(r.fecha) if frecuencia == "M" else trimestre_codificado(r.fecha)
        if frecuencia == "M":
            idx = [i for i, x in enumerate(periodos) if x >= p]
        else:
            idx = [i for i, x in enumerate(periodos) if x >= p]
        Dc[ccaa.index(r.cod_ine), idx] += r.dosis
    return Dc, ccaa


def n_cambios_efectivos(ev: pd.DataFrame, periodos: list[str], frecuencia: str, ell: int, ccaa: list[str] | None = None) -> tuple[int, int]:
    """Cambios del tipo general que caen dentro de la ventana con al menos ℓ periodos posteriores y número de comunidades distintas."""
    ult = len(periodos) - 1 - ell
    n, cc = 0, set()
    for r in ev.itertuples():
        if ccaa is not None and r.cod_ine not in ccaa:
            continue
        p = mes_codificado(r.fecha) if frecuencia == "M" else trimestre_codificado(r.fecha)
        if p in periodos and periodos.index(p) <= ult and periodos.index(p) >= 1:
            n += 1
            cc.add(r.cod_ine)
    return n, len(cc)


def trimestres_de(ini: str, fin: str) -> list[str]:
    return K.trimestres(ini, fin)


def meses(ini: str, fin: str) -> list[str]:
    return [str(p) for p in pd.period_range(ini, fin, freq="M")]


def panel_valor_tasado(provs: dict[str, str], ini: str = "2007T1", fin: str = "2026T2") -> dict:
    s = K.leer_hechos("valor_tasado", "provincia", "T")
    per = trimestres_de(ini, fin)
    w = K.ancho(s[s.territorio_codigo.isin(provs)], per)
    w = w.dropna()
    cods = list(w.index)
    return {"cod": np.array(cods), "Y": np.log(w.values), "cols": per, "ccaa": np.array([provs[c] for c in cods])}


def panel_compraventas(provs: dict[str, str], desglose: str = "usada", ini: str = "2007-01", fin: str = "2024-12") -> dict:
    """Compraventas provinciales mensuales del INE (ETDP 6150) con el sellado de V18 (clave compraventas|provincia|M, tope 2024-12)."""
    t = pd.read_csv(RAW / "ine_v2_etdp_prov.csv", dtype=str)
    t = t[(t.nivel == "provincia") & (t.desglose == desglose)].copy()
    t["territorio_codigo"] = t.codigo.str.zfill(2)
    t["periodo"] = t.periodo.str.replace("M", "-", regex=False)
    t["valor"] = pd.to_numeric(t.valor, errors="coerce")
    t = K.filtrar(t, "territorio_codigo", "provincia", "periodo", "compraventas", "M")
    per = meses(ini, fin)
    w = K.ancho(t[t.territorio_codigo.isin(provs)], per)
    w = w.dropna()
    w = w[(w > 0).all(axis=1)]
    cods = list(w.index)
    return {"cod": np.array(cods), "Y": np.log(w.values), "cols": per, "ccaa": np.array([provs[c] for c in cods])}


def panel_poblacion(provs: dict[str, str], ini: int = 2007, fin: int = 2024) -> dict:
    s = K.leer_hechos("pob_total", "provincia", "A")
    per = [str(y) for y in range(ini, fin + 1)]
    w = K.ancho(s[s.territorio_codigo.isin(provs)], per).dropna()
    cods = list(w.index)
    return {"cod": np.array(cods), "Y": np.log(w.values), "cols": per, "ccaa": np.array([provs[c] for c in cods])}
