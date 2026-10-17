"""V16-F1 · Normalización de la familia alquiler_turismo al formato largo de data/base/hechos.parquet.

Determinista (SEED=20261010; no hay aleatoriedad) y sin red. Lee data/raw/v16/alquiler_turismo/ (salvo las instantáneas de
Inside Airbnb de septiembre de 2026 de data/raw/v9/insideairbnb/, que el encargo pide incluir) y tablas versionadas de códigos
(data/base/publica/territorios.parquet y la geometría data/base/geo/secciones.parquet, solo para punto-en-polígono).
Salidas:
- data/processed/v16/alquiler_turismo.parquet (solo redistribuible = sí);
- data/processed/v16/alquiler_turismo_terceros.parquet (_terceros/: recuentos por municipio, redistribuible = False; NO se versiona;
  solo si existen los ficheros);
- data/processed/v16/alquiler_turismo_resultado.json, docs/v16/fuentes/alquiler_turismo_variables.csv y
  docs/v16/fuentes/alquiler_turismo_correspondencia.csv (tabla explícita nombre -> código INE, con descartes).
capa = C4; posterior_prereg = False (el corte de V16 no está fijado); muestra_sellada_v6 = True en provincia, municipio, distrito y
sección de las provincias de holdout.provincias_selladas_v6().
Si faltan los listings_*.csv.gz de Inside Airbnb (ignorados por git), se conservan las filas Inside Airbnb del parquet versionado y se avisa.
"""
from __future__ import annotations

import csv
import gzip
import io
import json
import re
import sys
import unicodedata
import zipfile
from pathlib import Path

import numpy as np
import pandas as pd

SEED = 20261010
RAIZ = Path(__file__).resolve().parents[3]
ENT = RAIZ / "data" / "raw" / "v16" / "alquiler_turismo"
V9_IA = RAIZ / "data" / "raw" / "v9" / "insideairbnb"
SAL = RAIZ / "data" / "processed" / "v16"
DOCS = RAIZ / "docs" / "v16" / "fuentes"
P_OUT = SAL / "alquiler_turismo.parquet"
P_TER = SAL / "alquiler_turismo_terceros.parquet"
COLS = ["territorio_codigo", "nivel", "periodo", "frecuencia", "variable", "desagregacion", "valor", "unidad", "fuente", "edicion",
        "fecha_dato", "capa", "licencia", "redistribuible", "metodo_dato", "origen", "posterior_prereg", "muestra_sellada_v6"]
PIEZA = ["territorio_codigo", "nivel", "periodo", "frecuencia", "variable", "desagregacion", "valor", "unidad", "fuente", "edicion",
         "fecha_dato", "licencia", "redistribuible", "metodo_dato", "origen"]
AVISOS: list[str] = []
CORRESP: list[dict] = []   # tabla de correspondencia nombre -> código INE (con descartes)

# ----------------------------------------------------------------------------------------------------------------------
# Nombres -> códigos INE (solo coincidencias únicas)
# ----------------------------------------------------------------------------------------------------------------------
ART = {"el", "la", "los", "las", "l", "els", "les", "a", "o", "as", "os", "es", "sa", "ses", "s"}


def _n(s) -> str:
    s = unicodedata.normalize("NFKD", str(s))
    s = "".join(c for c in s if not unicodedata.combining(c)).lower()
    return re.sub(r"[^a-z0-9]+", " ", s).strip()


def claves(nombre) -> set[str]:
    """Variantes normalizadas de un nombre: partes separadas por «/», «X, Art» y «X (Art)» reordenados."""
    out: set[str] = set()
    if "/" in str(nombre):
        out.add(_n(str(nombre).replace("/", " ")))
    for parte in str(nombre).split("/"):
        p = parte.strip()
        if not p:
            continue
        out.add(_n(p))
        m = re.match(r"^(.*?),\s*([^,]+)$", p)
        if m and _n(m.group(2)) in ART:
            out.add(_n(m.group(2) + " " + m.group(1)))
        m = re.match(r"^(.*?)\s*\(([^)]+)\)\s*$", p)
        if m and _n(m.group(2)) in ART:
            out.add(_n(m.group(2) + " " + m.group(1)))
    return {k for k in out if k}


# Alias explícitos y versionados (nombre de la fuente normalizado -> nombre oficial INE). Solo ortografías documentadas.
ALIAS_PROV = {"guipuzcoa": "Gipuzkoa", "vizcaya": "Bizkaia", "santa cruz tenerife": "Santa Cruz de Tenerife",
              "baleares": "Balears, Illes", "baleares illes": "Balears, Illes", "baleares illes de": "Balears, Illes"}
ALIAS_CCAA = {"baleares illes": "Balears, Illes", "baleares": "Balears, Illes", "castilla la mancha": "Castilla-La Mancha"}
ALIAS_MUNI = {"santa cruz tenerife": "Santa Cruz de Tenerife", "palma de mallorca": "Palma", "coruna": "Coruña, A", "ciutadella": "Ciutadella de Menorca",
              "vega san mateo": "Vega de San Mateo", "guia isora": "Guía de Isora", "zahara de la sierra": "Zahara",
              "gargantilla del lozoya": "Gargantilla del Lozoya y Pinilla de Buitrago", "san lorenzo del escorial": "San Lorenzo de El Escorial",
              "torremocha del jarama": "Torremocha de Jarama", "valdeolmo alalpardo": "Valdeolmos-Alalpardo", "villalvilla": "Villalbilla"}


class Terr:
    def __init__(self):
        t = pd.read_parquet(RAIZ / "data" / "base" / "publica" / "territorios.parquet")
        self.t = t
        self.validos = {n: set(g.territorio_codigo) for n, g in t.groupby("nivel")}
        self.nac = {"nacional": "00", "total nacional": "00"}
        self.ccaa = self._idx(t[t.nivel == "ccaa"], ALIAS_CCAA)
        self.prov = self._idx(t[t.nivel == "provincia"], ALIAS_PROV)
        m = t[(t.nivel == "municipio") & t.vigente_2025 & ~t.nombre.str.startswith("municipio ")]
        self.muni = self._idx(m, ALIAS_MUNI)
        self.muni_nombre = dict(zip(m.territorio_codigo, m.nombre))
        self.ccaa_por_nombre = dict(zip(t[t.nivel == "ccaa"].nombre, t[t.nivel == "ccaa"].territorio_codigo))
        pv = t[t.nivel == "provincia"]
        cnt = pv.groupby("cod_ccaa").territorio_codigo.agg(list)
        # CCAA uniprovinciales (derivado de la tabla de códigos): CCAA -> su única provincia
        self.uniprov = {c: l[0] for c, l in cnt.items() if len(l) == 1}

    def _idx(self, df, alias):
        d: dict[str, set] = {}
        por_nombre: dict[str, set] = {}
        for cod, nom in zip(df.territorio_codigo, df.nombre):
            por_nombre.setdefault(nom, set()).add(cod)
            for k in claves(nom):
                d.setdefault(k, set()).add(cod)
        for k, oficial in alias.items():
            if oficial in por_nombre:
                d.setdefault(_n(k), set()).update(por_nombre[oficial])
        return d

    def buscar(self, indice: dict, nombre: str, prov: str | None = None):
        cands: set[str] = set()
        for k in claves(nombre):
            cands |= indice.get(k, set())
        if prov is not None:
            cands = {c for c in cands if c.startswith(prov)}
        if len(cands) == 1:
            return next(iter(cands)), "coincidencia_unica"
        return None, ("ambigua" if cands else "sin_coincidencia")


def sellada_set() -> set[str]:
    sys.path.insert(0, str(RAIZ / "src"))
    import holdout  # solo devuelve la lista de códigos; no abre nada sellado
    return set(holdout.provincias_selladas_v6())


def marcar(df: pd.DataFrame, selladas: set[str]) -> pd.DataFrame:
    df = df.copy()
    pref = df.territorio_codigo.str[:2]
    df["capa"] = "C4"
    df["posterior_prereg"] = False
    df["muestra_sellada_v6"] = df.nivel.isin(["provincia", "municipio", "distrito", "seccion"]) & pref.isin(selladas)
    df["valor"] = df["valor"].astype(float)
    df["redistribuible"] = df["redistribuible"].astype(bool)
    return df[COLS]


def manifiestos() -> dict:
    m: dict[str, dict] = {}
    for p in (ENT / "_manifest.csv", V9_IA / "_manifest.csv"):
        if p.exists():
            with open(p, encoding="utf-8", newline="") as f:
                for r in csv.DictReader(f):
                    m[r["fichero"]] = r
    return m


def rel(p: Path) -> str:
    return str(p.relative_to(RAIZ))


def lic(man: dict, p: Path) -> tuple[str, bool]:
    r = man.get(rel(p))
    if r is None:
        raise KeyError(f"fichero sin entrada en el manifiesto: {rel(p)}")
    return r["licencia"], r["redistribuible"].strip().lower() in ("sí", "si", "true")


def fin_mes(per: pd.Series) -> pd.Series:
    return pd.PeriodIndex(per, freq="M").to_timestamp(how="end").strftime("%Y-%m-%d")


# ----------------------------------------------------------------------------------------------------------------------
# INE (Tempus, JSON): EOAP, EOH, EOT, OAT, IPAP, VTE
# ----------------------------------------------------------------------------------------------------------------------
KIND = {"1989": "nac", "2050": "nac",
        "1993": "ccaa", "2021": "ccaa", "2025": "ccaa", "61766": "ccaa", "61768": "ccaa", "75192": "ccaa", "48423": "ccaa", "48428": "ccaa",
        "2063": "prov", "2066": "mixto", "2072": "mixto", "48427": "prov",
        "2074": "mixto", "49371": "mixto", "39364": "mixto", "39365": "mixto", "46141": "mixto", "48440": "mixto", "48441": "mixto",
        "39363": "muni", "39366": "muni",
        "2076": "punto", "2078": "punto", "2082": "punto", "2083": "punto", "48424": "punto", "48426": "punto", "48429": "punto",
        "48431": "punto", "75191": "punto", "75193": "punto", "75197": "punto", "75198": "punto",
        "2013": "zona", "2022": "zona", "2039": "zona", "48432": "zona"}
ORDEN_KIND = ["nac", "ccaa", "prov", "mixto", "muni", "punto", "zona"]
PRIORIDAD_OP = ["ine_ipap", "ine_eoap", "ine_eoh", "ine_oat", "ine_vte", "ine_eot", "ine_eot_eoap_eoh"]
PREFIJO = {"ine_ipap": "ine_ipap", "ine_eoap": "ine_eoap", "ine_eoh": "ine_eoh", "ine_oat": "ine_oat", "ine_vte": "ine_vte",
           "ine_eot": "ine_eot", "ine_eot_eoap_eoh": "ine_eot"}
OP_NOMBRE = {"ine_ipap": "IPAP", "ine_eoap": "EOAP", "ine_eoh": "EOH", "ine_oat": "OAT", "ine_vte": "VTE", "ine_eot": "EOT"}
DESCARTE = {"dato base", "dato", "nacional", "total nacional"}


def unidad_ine(txt: str, fk_unidad: int) -> str:
    n = _n(txt)
    if fk_unidad == 133 and "tasa de variacion" not in n:
        return "índice (base propia del INE)"
    if "tasa de variacion" in n:
        return "% (tasa de variación interanual)"
    if "porcentaje" in n or "grado de ocupacion" in n:
        return "%"
    if "estancia media" in n:
        return "noches"
    if "plazas por vivienda" in n:
        return "plazas por vivienda turística"
    if "noches ocupadas" in n:
        return "noches"
    if "alojamientos turisticos ocupados" in n:
        return "alojamientos"
    if "viajero" in n:
        return "viajeros"
    if "pernoctaciones" in n:
        return "pernoctaciones"
    if "viviendas turisticas" in n:
        return "viviendas turísticas"
    if "plazas" in n:
        return "plazas"
    if "establecimientos" in n:
        return "establecimientos"
    if "apartamentos" in n:
        return "apartamentos"
    if "habitaciones" in n:
        return "habitaciones"
    if "personal empleado" in n:
        return "personas"
    raise ValueError(f"unidad no determinada: {txt!r} (FK_Unidad={fk_unidad})")


def resolver_serie(nombre: str, kind: str, T: Terr):
    """Devuelve (nivel, código, segmentos de variable) o (None, motivo, None)."""
    segs = [s.strip() for s in re.split(r"\.\s+", re.sub(r"\.\s*$", "", nombre.strip())) if s.strip()]
    if kind == "zona":
        return None, "zona_turistica_sin_codigo_ine", None
    hallazgos = []   # (índice de segmento, nivel, código, estado)
    for i, s in enumerate(segs):
        if _n(s) in DESCARTE and kind != "punto":
            if _n(s) in T.nac and kind in ("nac", "ccaa", "prov", "mixto", "muni"):
                hallazgos.append((i, "nacional", "00", "coincidencia_unica"))
            continue
        if kind in ("ccaa", "mixto"):
            c, e = T.buscar(T.ccaa, s)
            cc = (c, e)
        if kind == "ccaa":
            if cc[0]:
                hallazgos.append((i, "ccaa", cc[0], "coincidencia_unica"))
        elif kind == "prov":
            c, e = T.buscar(T.prov, s)
            if c:
                hallazgos.append((i, "provincia", c, "coincidencia_unica"))
        elif kind == "mixto":
            c2, e2 = T.buscar(T.prov, s)
            if cc[0] and c2 and T.uniprov.get(cc[0]) == c2:
                hallazgos.append((i, "dual", (cc[0], c2), "coincidencia_unica"))
            elif cc[0] and c2:
                hallazgos.append((i, "ambiguo", None, "ambigua_ccaa_provincia"))
            elif cc[0]:
                hallazgos.append((i, "ccaa", cc[0], "coincidencia_unica"))
            elif c2:
                hallazgos.append((i, "provincia", c2, "coincidencia_unica"))
        elif kind in ("muni", "punto"):
            m = re.match(r"^(\d{5})-(.+)$", s)
            if m and kind == "punto":
                cod = m.group(1)
                if cod in T.validos["municipio"]:
                    hallazgos.append((i, "municipio", cod, "coincidencia_unica"))
                continue
            c, e = T.buscar(T.muni, s)
            if c:
                hallazgos.append((i, "municipio", c, "coincidencia_unica"))
            elif e == "ambigua":
                hallazgos.append((i, "ambiguo", None, "ambigua_municipio"))
    if kind == "nac":
        hallazgos = [h for h in hallazgos if h[1] == "nacional"]
    if len(hallazgos) == 0:
        return None, "sin_coincidencia", None
    if len(hallazgos) > 1:
        # «Nacional» más un territorio concreto: gana el concreto; varios concretos: descarte
        conc = [h for h in hallazgos if h[1] != "nacional"]
        if len(conc) != 1:
            return None, "varios_territorios", None
        hallazgos = conc
    i, nivel, cod, est = hallazgos[0]
    if nivel == "ambiguo":
        return None, est, None
    var = [s for j, s in enumerate(segs) if j != i and _n(s) not in DESCARTE]
    return nivel, cod, (segs[i], var)


def proc_ine(T: Terr, man: dict):
    import glob
    ficheros = sorted(glob.glob(str(ENT / "original" / "ine_turismo" / "ine_tabla_*.json.gz")))
    if not ficheros:
        AVISOS.append("INE: no hay ficheros ine_tabla_*.json.gz")
        return pd.DataFrame(columns=PIEZA)
    meta_tab = {}
    series: dict[str, dict] = {}
    reg = []
    for f in ficheros:
        p = Path(f)
        tid = re.search(r"tabla_(\d+)_", p.name).group(1)
        if tid not in KIND:
            raise KeyError(f"tabla INE sin tipo territorial declarado: {tid}")
        r = man[rel(p)]
        op = r["fuente"]
        meta_tab[tid] = (op, rel(p), r["licencia"], r["redistribuible"].strip().lower() in ("sí", "si"))
        for s in json.load(gzip.open(p, "rt", encoding="utf-8")):
            cod = s["COD"]
            d = series.setdefault(cod, {"nombre": s["Nombre"], "tablas": [], "unidad": s["FK_Unidad"]})
            d["tablas"].append(tid)
            for y in s["Data"]:
                if y["Valor"] is None or y.get("Secreto"):
                    continue
                reg.append((cod, tid, y["Fecha"], y["FK_Periodo"], y["FK_TipoDato"], y["Valor"]))
    # tabla «principal» de cada serie (prioridad de operación) -> tipo territorial, prefijo, origen
    def pri(tid):
        return (PRIORIDAD_OP.index(meta_tab[tid][0]), int(tid))
    info = {}
    for cod, d in series.items():
        tp = sorted(d["tablas"], key=pri)[0]
        op = meta_tab[tp][0]
        # el tipo territorial lo fija la tabla de menor alcance (si el COD figura en una tabla provincial/CCAA, «Albacete» no es el municipio)
        tk = sorted(d["tablas"], key=lambda t: (ORDEN_KIND.index(KIND[t]), int(t)))[0]
        nivel, codigo, resto = resolver_serie(d["nombre"], KIND[tk], T)
        if nivel is None:
            CORRESP.append({"fuente": f"ine_tempus:{op}", "nombre_fuente": d["nombre"], "ambito": f"tabla {tk} ({KIND[tk]})",
                            "codigo_ine": "", "nivel": "", "estado": codigo, "n": 1})
            continue
        terr_txt, var = resto
        if KIND[tk] in ("muni", "punto") or nivel == "municipio":
            CORRESP.append({"fuente": f"ine_tempus:{op}", "nombre_fuente": terr_txt, "ambito": f"tabla {tk} ({KIND[tk]})",
                            "codigo_ine": codigo, "nivel": nivel, "estado": "coincidencia_unica", "n": 1})
        slug = "_".join(_n(s).replace(" ", "_") for s in var)
        variable = f"{PREFIJO[op]}_{slug}"
        info[cod] = dict(nivel=nivel, codigo=codigo, variable=variable, descr=" ".join(var), op=op, tp=tp,
                         unidad=unidad_ine(" ".join(var) + (" tasa de variacion" if "Tasa de variación" in d["nombre"] else ""), d["unidad"]),
                         tablas=",".join(sorted(set(d["tablas"]), key=int)))
    df = pd.DataFrame(reg, columns=["cod", "tid", "fecha", "fkp", "td", "valor"])
    df = df[df.cod.isin(info)]
    df["prio"] = df.tid.map(lambda t: pri(t)[0] * 1_000_000 + pri(t)[1])
    df = df.sort_values(["cod", "fecha", "prio"], kind="mergesort")
    # solapes entre tablas: se verifica que no haya valores discrepantes y se conserva la tabla principal
    nun = df.groupby(["cod", "fecha"]).valor.nunique()
    if (nun > 1).any():
        AVISOS.append(f"INE: {(nun > 1).sum()} pares (serie, fecha) con valores distintos entre tablas (se conserva la tabla principal)")
    n_antes = len(df)
    df = df.drop_duplicates(["cod", "fecha"], keep="first")
    n_dup = n_antes - len(df)
    f_loc = pd.to_datetime(df.fecha, unit="ms", utc=True).dt.tz_convert("Europe/Madrid")
    df["anual"] = df.fkp == 28
    df["periodo"] = np.where(df.anual, f_loc.dt.strftime("%Y"), f_loc.dt.strftime("%Y-%m"))
    df["frecuencia"] = np.where(df.anual, "A", "M")
    df["fecha_dato"] = np.where(df.anual, f_loc.dt.strftime("%Y") + "-12-31", fin_mes(f_loc.dt.strftime("%Y-%m")))
    for k in ("nivel", "codigo", "variable", "unidad", "op", "tp", "tablas"):
        df[k] = df.cod.map({c: v[k] for c, v in info.items()})
    df["dual"] = df.nivel == "dual"
    if df.dual.any():   # CCAA uniprovincial con nombre idéntico: mismo valor en nivel ccaa y en provincia
        a, b = df[df.dual].copy(), df[df.dual].copy()
        a["nivel"], a["codigo"] = "ccaa", a.codigo.map(lambda x: x[0])
        b["nivel"], b["codigo"] = "provincia", b.codigo.map(lambda x: x[1])
        df = pd.concat([df[~df.dual], a, b], ignore_index=True)
    df["territorio_codigo"] = df.codigo
    df["fuente"] = "INE, " + df.op.map(lambda o: OP_NOMBRE.get(PREFIJO[o].replace("ine_", "ine_"), OP_NOMBRE.get(o, o))) + " (Tempus)"
    df["fuente"] = df.op.map(lambda o: "INE, " + OP_NOMBRE[PREFIJO[o]] + " (Tempus)" if PREFIJO[o] in OP_NOMBRE else "INE (Tempus)")
    df["edicion"] = "INE Tempus DATOS_TABLA nult=1000, tablas " + df.tablas + ", descarga 2026-10-17"
    df["licencia"] = df.tp.map(lambda t: meta_tab[t][2])
    df["redistribuible"] = df.tp.map(lambda t: meta_tab[t][3])
    df["origen"] = df.tp.map(lambda t: meta_tab[t][1])
    df["metodo_dato"] = np.where(df.td == 2, "observado (FK_TipoDato=2; el JSON no documenta su significado, probable dato provisional)",
                                 "observado")
    df.loc[df.dual, "metodo_dato"] = df.loc[df.dual, "metodo_dato"] + "; CCAA uniprovincial: el mismo valor se asigna a nivel ccaa y provincia"
    df["desagregacion"] = ""
    # colisiones: mismo territorio, periodo y variable con series (COD) distintos -> el COD pasa a desagregacion
    k = ["territorio_codigo", "nivel", "periodo", "variable"]
    kg = ["territorio_codigo", "nivel", "variable"]
    col = df.duplicated(k, keep=False)
    if col.any():   # series distintas con idéntico contenido (p. ej. la misma CCAA uniprovincial en dos tablas) se reducen a una
        sub = df[col]
        sig = sub.groupby(kg + ["cod"]).apply(lambda g: hash(tuple(zip(g.periodo, g.valor))), include_groups=False).rename("sig").reset_index()
        mant = sig.sort_values("cod", kind="mergesort").drop_duplicates(kg + ["sig"])[kg + ["cod"]]
        mant["_m"] = True
        df = df.merge(mant, on=kg + ["cod"], how="left")
        idx_col = df.set_index(kg).index.isin(sub.set_index(kg).index)
        df = df[~idx_col | df._m.fillna(False).astype(bool)].drop(columns="_m").reset_index(drop=True)
        col = df.duplicated(k, keep=False)
    if col.any():
        df.loc[col, "desagregacion"] = "serie=" + df.loc[col, "cod"]
        AVISOS.append(f"INE: {int(col.sum())} filas con colisión de variable entre COD distintos de contenido distinto (COD en desagregacion)")
    AVISOS.append(f"INE: {n_dup} solapes exactos (serie, fecha) entre tablas eliminados")
    df["_descr"] = df.variable
    out = df[PIEZA].copy()
    out.attrs["descr"] = {v["variable"]: v["descr"] for v in info.values()}
    out.attrs["n_dup"] = n_dup
    return out


# ----------------------------------------------------------------------------------------------------------------------
# Inside Airbnb: agregado propio por sección y municipio (punto en polígono)
# ----------------------------------------------------------------------------------------------------------------------
IA_VARS = {  # columna -> (variable, unidad)
    "tot": ("ia_anuncios_total_numero", "anuncios"),
    "act": ("ia_anuncios_activos_numero", "anuncios"),
    "ent": ("ia_anuncios_vivienda_entera_numero", "anuncios"),
    "multi_h": ("ia_anfitriones_multianuncio_numero", "anfitriones"),
    "multi_a": ("ia_anuncios_de_multianfitriones_numero", "anuncios"),
    "lic": ("ia_anuncios_con_licencia_numero", "anuncios"),
    "pn": ("ia_precio_noche_n_numero", "anuncios con precio"),
    "pm": ("ia_precio_noche_mediana", "moneda del fichero (símbolo $, no verificada) por noche"),
    "av365": ("ia_disponibilidad_365_mediana_dias", "días"),
    "av30": ("ia_disponibilidad_30_mediana_dias", "días"),
}
MIN_MEDIANA = 5   # no se publica mediana con menos de 5 anuncios (evita exponer un anuncio individual)


def agregar_ia(d: pd.DataFrame, clave: str) -> pd.DataFrame:
    a = d[d.activo]
    o = pd.DataFrame({"tot": d.groupby(clave).size()})
    o["act"] = a.groupby(clave).size()
    o["ent"] = a[a.entera].groupby(clave).size()
    h = a.groupby([clave, "host_id"]).size().rename("n").reset_index()
    o["multi_h"] = h[h.n > 1].groupby(clave).size()
    o["multi_a"] = h[h.n > 1].groupby(clave).n.sum()
    o["lic"] = a[a.licencia].groupby(clave).size()
    p = a[a.price > 0]
    o["pn"] = p.groupby(clave).size()
    o["pm"] = p.groupby(clave).price.median()
    o["av365"] = a.groupby(clave).availability_365.median()
    o["av30"] = a.groupby(clave).availability_30.median()
    for c in ("act", "ent", "multi_h", "multi_a", "lic", "pn"):
        o[c] = o[c].fillna(0)
    o.loc[o.pn < MIN_MEDIANA, "pm"] = np.nan
    o.loc[o.act < MIN_MEDIANA, ["av365", "av30"]] = np.nan
    return o


def proc_ia(man: dict, previo: pd.DataFrame | None):
    patron = re.compile(r"^listings_([a-z]+)_(\d{4}-\d{2}-\d{2})\.csv\.gz$")
    arch = []
    for base in (ENT / "original" / "insideairbnb", V9_IA):
        if base.exists():
            for p in sorted(base.iterdir()):
                m = patron.match(p.name)
                if m:
                    arch.append((m.group(1), m.group(2), p))
    conservadas = pd.DataFrame(columns=PIEZA)
    if not arch:
        AVISOS.append("Inside Airbnb: no hay listings_*.csv.gz en disco (están ignorados por git); se conservan las filas "
                      "Inside Airbnb del parquet versionado" + ("" if previo is not None else " (pero NO existe parquet previo: sin filas IA)"))
        if previo is not None:
            conservadas = previo[previo.variable.str.startswith("ia_")][PIEZA]
        return conservadas, []
    import shapely
    from shapely import STRtree
    s = pd.read_parquet(RAIZ / "data" / "base" / "geo" / "secciones.parquet", columns=["cod_seccion", "cod_municipio", "geometry"])
    s = s.sort_values("cod_seccion", kind="mergesort").reset_index(drop=True)
    geoms = shapely.from_wkb(s.geometry.values)
    arbol = STRtree(geoms)
    cod_sec = s.cod_seccion.values
    cod_mun = s.cod_municipio.values
    piezas, log = [], []
    hechos = set()
    for area, fecha, p in arch:
        d = pd.read_csv(p, usecols=lambda c: c in ["id", "host_id", "latitude", "longitude", "room_type", "price", "has_availability",
                                                   "availability_30", "availability_365", "license"], low_memory=False)
        d["price"] = pd.to_numeric(d.price.astype(str).str.replace(r"[^0-9.\-]", "", regex=True), errors="coerce")
        d["activo"] = d.has_availability.eq("t")
        d["entera"] = d.room_type.eq("Entire home/apt")
        d["licencia"] = d["license"].notna() & d["license"].astype(str).str.strip().ne("")
        pts = shapely.points(d.longitude.values, d.latitude.values)
        par = arbol.query(pts, predicate="intersects")
        idx = np.full(len(d), -1)
        if par.shape[1]:
            ordn = np.lexsort((par[1], par[0]))
            par = par[:, ordn]
            _, primero = np.unique(par[0], return_index=True)
            idx[par[0][primero]] = par[1][primero]
        n_dentro = int((idx >= 0).sum())
        fuera = np.where(idx < 0)[0]
        n_cerca = 0
        if len(fuera):
            cerca = arbol.query_nearest(pts[fuera], max_distance=0.002, all_matches=False)
            if cerca.shape[1]:
                idx[fuera[cerca[0]]] = cerca[1]
                n_cerca = int(cerca.shape[1])
        asig = idx >= 0
        d["seccion"] = np.where(asig, cod_sec[np.where(asig, idx, 0)], None)
        d["municipio"] = np.where(asig, cod_mun[np.where(asig, idx, 0)], None)
        log.append({"area": area, "fecha": fecha, "anuncios": len(d), "en_poligono": n_dentro, "asignados_por_cercania": n_cerca,
                    "sin_asignar": int((~asig).sum())})
        d = d[asig]
        lic_txt, redis = lic(man, p)
        edicion = f"Inside Airbnb listings.csv.gz, area={area}, instantánea={fecha}"
        meta_ia = ("agregado propio de anuncios (sin anuncios individuales); punto en polígono con secciones INE 2025 "
                   "(anuncios fuera de polígono: sección más cercana a ≤0,002°); medianas solo con ≥5 anuncios; "
                   "activo = has_availability = t")
        for nivel, clave in (("municipio", "municipio"), ("seccion", "seccion")):
            o = agregar_ia(d, clave)
            for col, (var, uni) in IA_VARS.items():
                v = o[col].dropna()
                q = pd.DataFrame({"territorio_codigo": v.index.astype(str), "valor": v.values})
                q["nivel"], q["variable"], q["unidad"] = nivel, var, uni
                q["periodo"], q["frecuencia"], q["desagregacion"] = fecha, "D", ""
                q["fuente"] = "Inside Airbnb (CC BY 4.0), agregado propio por municipio/sección"
                q["edicion"], q["fecha_dato"], q["licencia"], q["redistribuible"] = edicion, fecha, lic_txt, redis
                q["metodo_dato"], q["origen"] = meta_ia, rel(p)
                piezas.append(q[PIEZA])
        hechos.add((area, fecha))
    nuevo = pd.concat(piezas, ignore_index=True)[PIEZA] if piezas else pd.DataFrame(columns=PIEZA)
    if previo is not None:   # instantáneas sin fichero en este clon: se conservan del parquet versionado
        pv = previo[previo.variable.str.startswith("ia_")]
        ed = pv.edicion.str.extract(r"area=([a-z]+), instantánea=(\d{4}-\d{2}-\d{2})")
        falta = ~pd.Series(list(zip(ed[0], ed[1])), index=pv.index).isin(hechos)
        if falta.any():
            AVISOS.append(f"Inside Airbnb: {int(falta.sum())} filas de instantáneas sin fichero en disco conservadas del parquet versionado")
            nuevo = pd.concat([nuevo, pv[falta][PIEZA]], ignore_index=True)
    return nuevo, log


# ----------------------------------------------------------------------------------------------------------------------
# Registros autonómicos (recuentos por municipio y fecha)
# ----------------------------------------------------------------------------------------------------------------------
def leer_csv(src, **kw):
    try:
        return pd.read_csv(src, sep=";", encoding="utf-8-sig", dtype=str, keep_default_na=False, low_memory=False, **kw)
    except UnicodeDecodeError:
        return pd.read_csv(src, sep=";", encoding="latin-1", dtype=str, keep_default_na=False, low_memory=False, **kw)


def mapear(T: Terr, nombres: pd.Series, prov: str | None, fuente: str, ambito: str, provs: pd.Series | None = None) -> dict:
    """Tabla explícita nombre -> código INE (único). Registra todos los casos en CORRESP. Clave: (prov, nombre)."""
    res = {}
    pares = pd.DataFrame({"n": nombres.astype(str).str.strip(), "p": (provs if provs is not None else pd.Series([prov] * len(nombres), index=nombres.index))})
    for (n, pv), g in pares.groupby(["n", "p"], dropna=False, sort=True):
        c, e = T.buscar(T.muni, n, pv if isinstance(pv, str) and pv else None)
        res[(pv, n)] = c
        CORRESP.append({"fuente": fuente, "nombre_fuente": n, "ambito": f"{ambito}" + (f" prov={pv}" if pv else ""),
                        "codigo_ine": c or "", "nivel": "municipio" if c else "", "estado": e, "n": len(g)})
    return res


def pieza_recuento(df, mun_col, prov, T, fuente, ambito, variable, unidad, periodo, freq, fecha_dato, edicion, lic_txt, redis, origen,
                   metodo, desag=None, valor=None, provs=None) -> pd.DataFrame:
    mp = mapear(T, df[mun_col], prov, fuente, ambito, provs)
    pv = provs if provs is not None else pd.Series([prov] * len(df), index=df.index)
    cod = [mp[(p, str(n).strip())] for p, n in zip(pv, df[mun_col])]
    d = pd.DataFrame({"territorio_codigo": cod, "desagregacion": (desag if desag is not None else pd.Series([""] * len(df), index=df.index)).values,
                      "valor": (valor if valor is not None else pd.Series([1.0] * len(df), index=df.index)).values})
    desc = int(d.territorio_codigo.isna().sum())
    d = d.dropna(subset=["territorio_codigo"])
    g = d.groupby(["territorio_codigo", "desagregacion"], as_index=False).valor.sum()
    g["nivel"] = "municipio"
    g["periodo"], g["frecuencia"], g["variable"], g["unidad"] = periodo, freq, variable, unidad
    g["fuente"], g["edicion"], g["fecha_dato"], g["licencia"], g["redistribuible"] = fuente, edicion, fecha_dato, lic_txt, redis
    g["metodo_dato"], g["origen"] = metodo, origen
    g.attrs["descartados"] = desc
    return g[PIEZA]


def proc_madrid(T: Terr, man: dict):
    piezas = []
    meta = "recuento de filas por municipio (código INE por tabla de correspondencia de Localidad, solo coincidencias únicas en provincia 28)"
    base = ENT / "original" / "madrid_vut"
    f_act = base / "declaraciones_actividad_vut_2026-10-17.csv"
    z = base / "declaraciones_actividad_vut_historico_2026-10-17.zip"
    if f_act.exists():
        l, r = lic(man, f_act)
        d = leer_csv(f_act)
        piezas.append(pieza_recuento(d, "Localidad", "28", T, "madrid_vut", "Localidad (Madrid)", "madrid_vut_declaraciones_numero",
                                     "declaraciones de actividad VUT", "2026-10", "M", "2026-10-17",
                                     "Comunidad de Madrid, declaraciones de actividad VUT, corte descargado 2026-10-17", l, r, rel(f_act), meta))
    if z.exists():
        l, r = lic(man, z)
        with zipfile.ZipFile(z) as zf:
            for nom in sorted(zf.namelist()):
                m = re.search(r"(\d{4})(\d{2})_declaraciones", nom)
                if not m:
                    continue
                per = f"{m.group(1)}-{m.group(2)}"
                crudo = zf.read(nom)
                try:
                    txt = crudo.decode("utf-8-sig")
                except UnicodeDecodeError:
                    txt = crudo.decode("latin-1")
                d = pd.read_csv(io.StringIO(txt), sep=";", dtype=str, keep_default_na=False)
                col_loc = "Localidad" if "Localidad" in d.columns else "MUNICIPIO"   # ruptura de formato en los cortes 2025-04 a 2025-09
                piezas.append(pieza_recuento(d, col_loc, "28", T, "madrid_vut", "Localidad (Madrid)", "madrid_vut_declaraciones_numero",
                                             "declaraciones de actividad VUT", per, "M", str(pd.Period(per, "M").end_time.date()),
                                             f"Comunidad de Madrid, declaraciones de actividad VUT, corte mensual {per} (zip histórico)",
                                             l, r, rel(z) + "::" + nom, meta))
    f_al = base / "alojamientos_turisticos_2026-10-17.csv"
    if f_al.exists():
        l, r = lic(man, f_al)
        d = leer_csv(f_al)
        for nombre, desag in (("tipo=Total", pd.Series([""] * len(d), index=d.index).replace("", "tipo=Total")),
                              ("", "tipo=" + d.alojamiento_tipo.str.strip())):
            piezas.append(pieza_recuento(d, "localidad", "28", T, "madrid_alojamientos", "localidad (Madrid)",
                                         "madrid_alojamientos_establecimientos_numero", "establecimientos", "2026-10", "M", "2026-10-17",
                                         "Comunidad de Madrid, alojamientos turísticos, corte descargado 2026-10-17", l, r, rel(f_al), meta,
                                         desag=desag))
    return pd.concat(piezas, ignore_index=True) if piezas else pd.DataFrame(columns=PIEZA)


def proc_canarias(T: Terr, man: dict):
    piezas = []
    f = ENT / "original" / "canarias" / "vivienda_vacacional_registro_2026-10-17.csv"
    if f.exists():
        l, r = lic(man, f)
        d = leer_csv(f)
        pmap = {"Palmas (Las)": "35", "Santa Cruz De Tenerife": "38"}
        d["_p"] = d.direccion_provincia_nombre.map(pmap)
        sin = int(d._p.isna().sum())
        d2 = d[d._p.notna()]
        meta = "recuento de registros por municipio (código INE por correspondencia de nombre dentro de la provincia, solo coincidencias únicas)"
        plazas = pd.to_numeric(d2.plazas, errors="coerce").fillna(0)
        for var, uni, val in (("canarias_vv_viviendas_numero", "viviendas vacacionales", None),
                              ("canarias_vv_plazas_numero", "plazas", plazas)):
            piezas.append(pieza_recuento(d2, "direccion_municipio_nombre", None, T, "canarias_vv", "municipio (Canarias)", var, uni,
                                         "2026-10", "M", "2026-10-17", "Gobierno de Canarias, registro de vivienda vacacional, descarga 2026-10-17",
                                         l, r, rel(f), meta, valor=val, provs=d2._p))
        AVISOS.append(f"Canarias VV: {sin} registros sin provincia válida descartados")
    f = ENT / "original" / "canarias" / "istac_C00065A_000061_v1.29_2026-10-17.csv"
    if f.exists():
        l, r = lic(man, f)
        d = pd.read_csv(f, dtype={"TERRITORIO_CODE": str})
        d = d.dropna(subset=["OBS_VALUE"])
        canarias = T.ccaa_por_nombre["Canarias"]
        nivel = np.where(d.TERRITORIO_CODE.eq("ES70"), "ccaa", np.where(d.TERRITORIO_CODE.str.fullmatch(r"\d{5}"), "municipio", ""))
        cod = np.where(nivel == "ccaa", canarias, d.TERRITORIO_CODE)
        d["nivel"], d["territorio_codigo"] = nivel, cod
        ok = (d.nivel != "") & ~((d.nivel == "municipio") & ~d.territorio_codigo.isin(T.validos["municipio"]))
        for t, g in d[~ok].groupby(["TERRITORIO#es", "TERRITORIO_CODE"]):
            CORRESP.append({"fuente": "canarias_istac_vv", "nombre_fuente": t[0], "ambito": "isla (sin nivel INE)", "codigo_ine": t[1],
                            "nivel": "", "estado": "descartado_sin_nivel_ine", "n": len(g)})
        d = d[ok]
        MED = {"INGRESOS_TOTALES": ("istac_vv_ingresos_totales", "euros (supuesto: el CSV no declara unidad)"),
               "VIVIENDAS_VACACIONALES_RESERVADAS": ("istac_vv_viviendas_reservadas", "viviendas vacacionales"),
               "TASA_VIVIENDA_RESERVADA": ("istac_vv_tasa_vivienda_reservada", "%"),
               "VIVIENDAS_VACACIONALES_DISPONIBLES": ("istac_vv_viviendas_disponibles", "viviendas vacacionales"),
               "PLAZAS_DISPONIBLES": ("istac_vv_plazas_disponibles", "plazas"),
               "ESTANCIA_MEDIA_VIVIENDA_VACACIONAL": ("istac_vv_estancia_media", "noches")}
        q = pd.DataFrame({"territorio_codigo": d.territorio_codigo.values, "nivel": d.nivel.values,
                          "periodo": d.TIME_PERIOD_CODE.str.replace("-M", "-", regex=False).values, "frecuencia": "M",
                          "variable": d.MEDIDAS_CODE.map(lambda m: MED[m][0]).values, "desagregacion": "",
                          "valor": d.OBS_VALUE.values, "unidad": d.MEDIDAS_CODE.map(lambda m: MED[m][1]).values,
                          "fuente": "ISTAC, viviendas vacacionales (C00065A_000061)", "edicion": "ISTAC C00065A_000061 v1.29, descarga 2026-10-17",
                          "licencia": l, "redistribuible": r, "metodo_dato": "observado", "origen": rel(f)})
        q["fecha_dato"] = fin_mes(q.periodo)
        piezas.append(q[PIEZA])
    return pd.concat(piezas, ignore_index=True) if piezas else pd.DataFrame(columns=PIEZA)


def proc_baleares(T: Terr, man: dict):
    piezas = []
    meta = "recuento de registros por municipio (código INE por correspondencia de nombre en provincia 07, solo coincidencias únicas)"
    f = ENT / "original" / "baleares" / "allotjaments_turistics_mallorca_2026-10-17.csv"
    if f.exists():
        l, r = lic(man, f)
        d = leer_csv(f)
        d["Places"] = pd.to_numeric(d.Places, errors="coerce").fillna(0)
        desag = "grupo=" + d.Grup.str.strip() + "|estado=" + d.Estat.str.strip()
        for var, uni, val in (("baleares_alojamientos_establecimientos_numero", "establecimientos", None),
                              ("baleares_alojamientos_plazas_numero", "plazas", d.Places)):
            piezas.append(pieza_recuento(d, "Municipi", "07", T, "baleares_mallorca_alojamientos", "Municipi (Mallorca)", var, uni,
                                         "2026-10", "M", "2026-10-17", "Govern de les Illes Balears, allotjaments turístics de Mallorca, descarga 2026-10-17",
                                         l, r, rel(f), meta, desag=desag, valor=val))
    f = ENT / "original" / "baleares" / "allotjaments_turistics_menorca_2026-10-17.csv"
    if f.exists():
        l, r = lic(man, f)
        d = leer_csv(f)
        d["nombreplaces"] = pd.to_numeric(d.nombreplaces, errors="coerce").fillna(0)
        desag = "grupo=" + d.tipus.str.strip()
        for var, uni, val in (("baleares_alojamientos_establecimientos_numero", "establecimientos", None),
                              ("baleares_alojamientos_plazas_numero", "plazas", d.nombreplaces)):
            piezas.append(pieza_recuento(d, "poblacio", "07", T, "baleares_menorca_alojamientos", "poblacio (Menorca)", var, uni,
                                         "2026-10", "M", "2026-10-17", "Govern de les Illes Balears, allotjaments turístics de Menorca, descarga 2026-10-17",
                                         l, r, rel(f), meta, desag=desag, valor=val))
    return pd.concat(piezas, ignore_index=True) if piezas else pd.DataFrame(columns=PIEZA)


# ----------------------------------------------------------------------------------------------------------------------
# _terceros: solo recuentos por municipio y fecha (sin ningún dato personal), redistribuible = False
# ----------------------------------------------------------------------------------------------------------------------
def stock_altas(mun: pd.Series, tipo: pd.Series, anio: pd.Series, y_max: int) -> pd.DataFrame:
    d = pd.DataFrame({"m": mun.values, "t": tipo.values, "y": pd.to_numeric(anio, errors="coerce").values}).dropna()
    d = d[(d.y >= 1950) & (d.y <= y_max)]
    d["y"] = d.y.astype(int)
    c = d.groupby(["m", "t", "y"]).size().unstack("y", fill_value=0)
    c = c.reindex(columns=range(int(d.y.min()), y_max + 1), fill_value=0).cumsum(axis=1)
    s = c.stack().rename("valor").reset_index()
    return s[s.valor > 0]


def proc_terceros(T: Terr, man: dict):
    piezas = []
    nota_acum = ("reconstrucción: acumulado de altas a 31-dic de los registros vigentes en el corte (sin bajas históricas: sesgo de "
                 "supervivencia); solo para robustez")

    def anadir(s, var, uni, fuente, edicion, lic_txt, origen, metodo, freq, per_fn, fd_fn):
        g = s.copy()
        g["periodo"], g["fecha_dato"] = per_fn(g), fd_fn(g)
        g["frecuencia"], g["variable"], g["unidad"], g["fuente"], g["edicion"] = freq, var, uni, fuente, edicion
        g["licencia"], g["redistribuible"], g["metodo_dato"], g["origen"], g["nivel"] = lic_txt, False, metodo, origen, "municipio"
        piezas.append(g)

    # Andalucía (OpenRTA): esquema de 92 columnas sin cabecera propia en el bloque final -> posiciones verificadas por anclas
    f = ENT / "_terceros" / "openrta_all_2026-10-17.csv.gz"
    if f.exists():
        l, _ = lic(man, f)
        PROV = {"AL": "04", "CA": "11", "CO": "14", "GR": "18", "H": "21", "J": "23", "MA": "29", "SE": "41"}
        filas = []
        with gzip.open(f, "rt", encoding="utf-8", newline="") as fh:
            rd = csv.reader(fh, delimiter="|")
            h = next(rd)
            ix = {n: i for i, n in enumerate(h)}
            for row in rd:
                if len(row) == 72:
                    muni, reg, fecha, grupo = row[ix["municipalities"]], row[ix["registration_code"]], row[ix["registration_date"]] or row[ix["activity_start_date"]], row[ix["group"]]
                elif len(row) == 92:
                    muni, reg, fecha, grupo = row[51], row[69], row[70] or row[1], row[17]
                else:
                    continue
                m = re.match(r"^[A-Z]{1,4}/([A-Z]{1,2})/", reg)
                prov = PROV.get(m.group(1)) if m else None
                filas.append((muni.strip(), prov, (grupo.strip() or "sin_grupo"), fecha[:4] if fecha[:4].isdigit() else ""))
        d = pd.DataFrame(filas, columns=["muni", "prov", "grupo", "anio"])
        d = d[d.prov.notna() & d.muni.ne("")]
        mp = mapear(T, d.muni, None, "andalucia_rta", "municipalities (Andalucía)", d.prov)
        d["cod"] = [mp[(p, n.strip())] for p, n in zip(d.prov, d.muni)]
        d = d.dropna(subset=["cod"])
        fuente = "Junta de Andalucía, OpenRTA (recuentos por municipio)"
        ed = "OpenRTA /api/v0/openrta/all, descarga 2026-10-17"
        corte = d.groupby(["cod", "grupo"]).size().rename("valor").reset_index()
        corte["territorio_codigo"], corte["desagregacion"] = corte.cod, "grupo=" + corte.grupo
        anadir(corte[["territorio_codigo", "desagregacion", "valor"]], "andalucia_rta_registros_numero", "establecimientos registrados",
               fuente, ed, l, rel(f), "recuento de registros por municipio (nombre -> INE por correspondencia dentro de la provincia, solo únicas)",
               "M", lambda g: "2026-10", lambda g: "2026-10-17")
        sa = stock_altas(d.cod, d.grupo, d.anio, 2025).rename(columns={"m": "territorio_codigo", "t": "grupo", "y": "anio"})
        sa["desagregacion"] = "grupo=" + sa.grupo
        anadir(sa[["territorio_codigo", "desagregacion", "valor", "anio"]], "andalucia_rta_altas_acumuladas_numero", "establecimientos",
               fuente, ed, l, rel(f), nota_acum, "A", lambda g: g.anio.astype(str), lambda g: g.anio.astype(str) + "-12-31")
    # Mallorca ETV/HUT
    f = ENT / "_terceros" / "habitatges_turistics_mallorca_2026-10-17.csv"
    if f.exists():
        l, _ = lic(man, f)
        d = leer_csv(f)
        d["anio"] = d["Inici d'activitat"].str[-4:]
        d["grupo"] = d["Grup"].str.strip().replace("", "sin_grupo")
        d = d[d.Estat.str.strip().eq("Alta")]
        mp = mapear(T, d.Municipi, "07", "baleares_mallorca_etv", "Municipi (Mallorca)")
        d["cod"] = [mp[("07", n.strip())] for n in d.Municipi]
        d = d.dropna(subset=["cod"])
        fuente, ed = "Govern de les Illes Balears, habitatges turístics de Mallorca (recuentos por municipio)", "Habitatges turístics de Mallorca, corte 2026-09, descarga 2026-10-17"
        corte = d.groupby(["cod", "grupo"]).size().rename("valor").reset_index()
        corte["territorio_codigo"], corte["desagregacion"] = corte.cod, "grupo=" + corte.grupo
        anadir(corte[["territorio_codigo", "desagregacion", "valor"]], "baleares_etv_registros_numero", "viviendas/estancias registradas (estado Alta)",
               fuente, ed, l, rel(f), "recuento de registros en alta por municipio (nombre -> INE, solo únicas)", "M",
               lambda g: "2026-09", lambda g: "2026-09-30")
        sa = stock_altas(d.cod, d.grupo, d.anio, 2025).rename(columns={"m": "territorio_codigo", "t": "grupo", "y": "anio"})
        sa["desagregacion"] = "grupo=" + sa.grupo
        anadir(sa[["territorio_codigo", "desagregacion", "valor", "anio"]], "baleares_etv_altas_acumuladas_numero", "viviendas/estancias",
               fuente, ed, l, rel(f), nota_acum, "A", lambda g: g.anio.astype(str), lambda g: g.anio.astype(str) + "-12-31")
    # Menorca ETV (sin fecha de alta)
    f = ENT / "_terceros" / "estades_habitatges_turistics_menorca_2026-10-17.csv"
    if f.exists():
        l, _ = lic(man, f)
        d = leer_csv(f)
        mp = mapear(T, d.poblacio, "07", "baleares_menorca_etv", "poblacio (Menorca)")
        d["cod"] = [mp[("07", n.strip())] for n in d.poblacio]
        d = d.dropna(subset=["cod"])
        corte = d.groupby(["cod", "tipus"]).size().rename("valor").reset_index()
        corte["territorio_codigo"], corte["desagregacion"] = corte.cod, "grupo=" + corte.tipus.str.strip()
        anadir(corte[["territorio_codigo", "desagregacion", "valor"]], "baleares_etv_registros_numero", "viviendas/estancias registradas",
               "Consell Insular de Menorca, estades i habitatges turístics (recuentos por municipio)",
               "Estades i habitatges turístics de Menorca, corte 2026-09, descarga 2026-10-17", l, rel(f),
               "recuento de registros por municipio (nombre -> INE, solo únicas)", "M", lambda g: "2026-09", lambda g: "2026-09-30")
    if not piezas:
        return pd.DataFrame(columns=PIEZA)
    out = pd.concat(piezas, ignore_index=True)
    return out[PIEZA]


# ----------------------------------------------------------------------------------------------------------------------
RUPTURAS = {
    "ine_": ("Series con COD distinto para base/definición distintas (p. ej. «Total categorías. Dato.» desde 2014-2015 frente a series 1999/2005+): "
             "no se empalman. Tablas de «puntos turísticos» con base 2024 (serie nueva 75191-75198, desde 2025-01) solapan sin discrepancias con las "
             "anteriores. Zonas turísticas y puntos no municipales: descartados (sin código INE)."),
    "ine_vte": "Medición experimental; cortes semestrales (feb/ago) y desde 2024-11 cada 6 meses con corte distinto; municipios con nombre repetido descartados.",
    "ine_oat": "Base reciente con residencia del viajero; mensual desde 2018-01 y anual (provincias/puntos) hasta 2025.",
    "ia_": ("Cobertura = área de captura (ciudad, isla o región), no el territorio completo; precio no publicado en 2025-12 ni en Valencia 2026-03; "
            "desde 2026-03 el precio es una cotización de estancia futura; la proporción has_availability=f sube en 2026-09; moneda sin verificar."),
    "madrid_vut": "Cortes mensuales irregulares (faltan 2025-08, 2025-10, 2025-11, 2026-02); sin fecha de alta; el corte 2026-10 es la descarga del 2026-10-17.",
    "madrid_alojamientos": "Un único corte (2026-10).",
    "canarias_vv": "Un único corte (2026-10); sin fecha de alta.",
    "istac_vv": "Mensual desde 2019-01; islas (ES70x) descartadas por no tener nivel INE; unidad de ingresos no declarada.",
    "baleares_alojamientos": "Un único corte (2026-10); Mallorca y Menorca únicamente (Ibiza y Formentera no figuran en el catálogo abierto).",
    "baleares_etv": "Corte 2026-09; acumulado de altas con sesgo de supervivencia (solo vigentes).",
    "andalucia_rta": "Fichero con dos esquemas (72 y 92 columnas) en un mismo CSV; posiciones del bloque de 92 por anclas; acumulado de altas con sesgo de supervivencia.",
}


def rupt(v: str) -> str:
    for k in sorted(RUPTURAS, key=len, reverse=True):
        if v.startswith(k):
            return RUPTURAS[k]
    return ""


def diccionario(df: pd.DataFrame, descr_ine: dict) -> pd.DataFrame:
    g = df.groupby("variable")
    d = pd.DataFrame({
        "unidad": g.unidad.agg(lambda x: " | ".join(sorted(set(x)))),
        "nivel": g.nivel.agg(lambda x: "|".join(sorted(set(x)))),
        "frecuencia": g.frecuencia.agg(lambda x: "|".join(sorted(set(x)))),
        "periodo_min": g.periodo.min(), "periodo_max": g.periodo.max(),
        "fuente": g.fuente.agg(lambda x: " | ".join(sorted(set(x)))),
    }).reset_index()
    ia = {v[0]: k for k, v in IA_VARS.items()}
    desc_ia = {"ia_anuncios_total_numero": "Anuncios en la instantánea (todos)", "ia_anuncios_activos_numero": "Anuncios activos (has_availability = t)",
               "ia_anuncios_vivienda_entera_numero": "Anuncios activos de vivienda entera", "ia_anfitriones_multianuncio_numero": "Anfitriones con más de un anuncio activo en el territorio",
               "ia_anuncios_de_multianfitriones_numero": "Anuncios activos de anfitriones con más de un anuncio en el territorio",
               "ia_anuncios_con_licencia_numero": "Anuncios activos con número de licencia declarado", "ia_precio_noche_n_numero": "Anuncios activos con precio",
               "ia_precio_noche_mediana": "Mediana del precio por noche de anuncios activos (≥5 anuncios)",
               "ia_disponibilidad_365_mediana_dias": "Mediana de availability_365 de anuncios activos (≥5 anuncios)",
               "ia_disponibilidad_30_mediana_dias": "Mediana de availability_30 de anuncios activos (≥5 anuncios)"}
    otros = {"madrid_vut_declaraciones_numero": "Declaraciones de actividad de VUT por municipio y corte",
             "madrid_alojamientos_establecimientos_numero": "Alojamientos turísticos regulados (tipo en desagregacion)",
             "canarias_vv_viviendas_numero": "Viviendas vacacionales registradas", "canarias_vv_plazas_numero": "Plazas de viviendas vacacionales registradas",
             "baleares_alojamientos_establecimientos_numero": "Alojamientos turísticos (grupo y estado en desagregacion)",
             "baleares_alojamientos_plazas_numero": "Plazas de alojamientos turísticos",
             "baleares_etv_registros_numero": "Registros de viviendas/estancias turísticas (terceros)",
             "baleares_etv_altas_acumuladas_numero": "Altas acumuladas a 31-dic de registros vigentes (terceros)",
             "andalucia_rta_registros_numero": "Registros OpenRTA por grupo (terceros)",
             "andalucia_rta_altas_acumuladas_numero": "Altas acumuladas a 31-dic de registros vigentes (terceros)"}
    d["descripcion"] = d.variable.map(lambda v: desc_ia.get(v) or otros.get(v) or descr_ine.get(v)
                                     or ("ISTAC viviendas vacacionales: " + v.replace("istac_vv_", "").replace("_", " ") if v.startswith("istac_vv_") else v))
    d["rupturas"] = d.variable.map(rupt)
    return d[["variable", "descripcion", "unidad", "nivel", "frecuencia", "periodo_min", "periodo_max", "fuente", "rupturas"]]


def main() -> int:
    SAL.mkdir(parents=True, exist_ok=True)
    DOCS.mkdir(parents=True, exist_ok=True)
    man = manifiestos()
    T = Terr()
    selladas = sellada_set()
    previo = pd.read_parquet(P_OUT) if P_OUT.exists() else None

    ine = proc_ine(T, man)
    descr_ine = ine.attrs.get("descr", {})
    ia, log_ia = proc_ia(man, previo)
    reg = [proc_madrid(T, man), proc_canarias(T, man), proc_baleares(T, man)]
    todo = pd.concat([ine, ia] + reg, ignore_index=True)
    ter = proc_terceros(T, man)
    red = todo[todo.redistribuible.astype(bool)]
    no_red = todo[~todo.redistribuible.astype(bool)]
    if len(no_red):
        AVISOS.append(f"{len(no_red)} filas no redistribuibles apartadas del parquet versionado")
    out = marcar(red, selladas).sort_values(["variable", "nivel", "territorio_codigo", "periodo", "desagregacion"], kind="mergesort").reset_index(drop=True)
    out.to_parquet(P_OUT, index=False, compression="zstd")
    n_ter = 0
    if len(ter):
        ter = marcar(ter.assign(redistribuible=False), selladas).sort_values(["variable", "territorio_codigo", "periodo", "desagregacion"], kind="mergesort")
        ter.to_parquet(P_TER, index=False, compression="zstd")
        n_ter = len(ter)
    elif not (ENT / "_terceros").exists():
        AVISOS.append("No hay _terceros/ en disco: parquet de terceros no generado")
    dic = diccionario(pd.concat([out, ter]) if n_ter else out, descr_ine)
    dic.to_csv(DOCS / "alquiler_turismo_variables.csv", index=False, quoting=csv.QUOTE_MINIMAL)
    c = pd.DataFrame(CORRESP)
    if len(c):
        c = c.groupby(["fuente", "nombre_fuente", "ambito", "codigo_ine", "nivel", "estado"], as_index=False).n.sum()
        c.sort_values(["fuente", "estado", "ambito", "nombre_fuente"], kind="mergesort").to_csv(DOCS / "alquiler_turismo_correspondencia.csv", index=False)
    res = {"rama": "v16-f1-datos-alquiler_turismo",
           "pregunta": "Normalización al formato largo: Inside Airbnb agregado por sección/municipio, registros VUT/alojamientos de Madrid, Canarias y Baleares, ISTAC, INE EOAP/EOH/OAT/IPAP/VTE (terceros aparte)",
           "capa": "C4", "N": int(len(out)), "metodo": "normalización",
           "notas": (f"N_terceros={n_ter} (no versionado, redistribuible=False). posterior_prereg=False porque el corte de V16 no está fijado. "
                     f"Avisos: {' || '.join(AVISOS)}. Inside Airbnb: {json.dumps(log_ia, ensure_ascii=False)}")}
    (SAL / "alquiler_turismo_resultado.json").write_text(json.dumps(res, ensure_ascii=False, indent=1), encoding="utf-8")
    print(json.dumps({"N": len(out), "N_terceros": n_ter, "avisos": AVISOS}, ensure_ascii=False, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
