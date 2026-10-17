"""V16-F1 · Normalización de la familia renta_parque al formato largo de data/base/hechos.parquet.

Determinista (SEED=20261010; no hay aleatoriedad) y sin red. Lee data/raw/v16/renta_parque/ (ADRH en _grandes/adrh/, anotado
redistribuible «sí»; Catastro URBANA2026.xls) y tablas versionadas de códigos (data/base/publica/territorios.parquet).
ECV y EPF son microdatos: NO se normalizan aquí (los usa el módulo de fase 2 directamente).
Salidas:
- data/processed/v16/renta_parque.parquet (versionado, < 50 MB): ADRH, variables principales, municipio/distrito/sección
  (sin la parte ya presente en la base pública: sección 2019-2023 de renta neta por persona, por hogar y Gini) + Catastro municipal;
- data/processed/v16/renta_parque_adrh_completo.parquet (NO versionado): todo el ADRH normalizado;
- docs/v16/fuentes/renta_parque_variables.csv, docs/v16/fuentes/renta_parque_correspondencia.csv (nombre -> código INE, con descartes),
  data/processed/v16/renta_parque_resultado.json y data/processed/v16/renta_parque_estadisticas.json.
capa = C4; posterior_prereg = False (el corte de V16 no está fijado); muestra_sellada_v6 = True en municipio, distrito y sección de
las provincias de holdout.provincias_selladas_v6().
Cruce por código INE. El ADRH trae solo nombres de municipio: se cruzan con territorios.parquet dentro de la provincia inferida de
cada tabla (provincia donde caen >= 80 % de los nombres de coincidencia nacional única); solo coincidencias únicas; el resto se lista y se descarta.
Si falta _grandes/adrh/ (ignorado por git), se conservan las filas ADRH del parquet versionado y se avisa.
"""
from __future__ import annotations

import collections
import csv
import gzip
import json
import re
import sys
import unicodedata
from pathlib import Path

import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq

SEED = 20261010
RAIZ = Path(__file__).resolve().parents[3]
ENT = RAIZ / "data" / "raw" / "v16" / "renta_parque"
ADRH = ENT / "_grandes" / "adrh"
CAT = ENT / "catastro" / "URBANA2026.xls"
SAL = RAIZ / "data" / "processed" / "v16"
DOCS = RAIZ / "docs" / "v16" / "fuentes"
P_OUT = SAL / "renta_parque.parquet"
P_COMP = SAL / "renta_parque_adrh_completo.parquet"
COLS = ["territorio_codigo", "nivel", "periodo", "frecuencia", "variable", "desagregacion", "valor", "unidad", "fuente", "edicion",
        "fecha_dato", "capa", "licencia", "redistribuible", "metodo_dato", "origen", "posterior_prereg", "muestra_sellada_v6"]
CLAVE = ["territorio_codigo", "nivel", "periodo", "variable", "desagregacion"]
AVISOS: list[str] = []

sys.path.insert(0, str(RAIZ / "src"))
import holdout  # noqa: E402  (solo devuelve la lista de provincias selladas)

SELLADAS = set(holdout.provincias_selladas_v6())

LIC_ADRH = "INE: reutilización con cita (Ley 37/2007); aviso legal https://www.ine.es/aviso_legal (ver también https://www.ine.es/normativa/normativa.htm)"
FUENTE_ADRH = "INE, ADRH (Atlas de distribución de renta de los hogares), API wstempus"
LIC_CAT = "Catastro: reutilización libre con reconocimiento de la fuente (docs/v5/licencias_datos.md)"
EDICION_MOD = "última modificación 2025-10-21; descarga 2026-10-17"

# ----------------------------------------------------------------------------------------------------------------------
# Variables
# ----------------------------------------------------------------------------------------------------------------------
V_RENTA = {
    "Renta neta media por persona": ("ine_adrh_renta_neta_media_persona_eur", "euros/año", "Renta neta media por persona"),
    "Renta neta media por hogar": ("ine_adrh_renta_neta_media_hogar_eur", "euros/año", "Renta neta media por hogar"),
    "Media de la renta por unidad de consumo": ("ine_adrh_renta_media_uc_eur", "euros/año", "Media de la renta por unidad de consumo"),
    "Mediana de la renta por unidad de consumo": ("ine_adrh_renta_mediana_uc_eur", "euros/año", "Mediana de la renta por unidad de consumo"),
    "Renta bruta media por persona": ("ine_adrh_renta_bruta_media_persona_eur", "euros/año", "Renta bruta media por persona"),
    "Renta bruta media por hogar": ("ine_adrh_renta_bruta_media_hogar_eur", "euros/año", "Renta bruta media por hogar"),
    "Renta mediana por hogar": ("ine_adrh_renta_mediana_hogar_eur", "euros/año", "Renta mediana por hogar"),
    "Índice de Gini": ("ine_adrh_gini_indice", "índice (0-100)", "Índice de Gini de la renta por unidad de consumo"),
    "Distribución de la renta P80/P20": ("ine_adrh_p80p20_ratio", "ratio", "Cociente P80/P20 de la renta por unidad de consumo"),
    "Población": ("ine_adrh_poblacion_personas", "personas", "Población residente (ADRH)"),
    "Edad media de la población": ("ine_adrh_edad_media_anios", "años", "Edad media de la población"),
    "Tamaño medio del hogar": ("ine_adrh_tamano_medio_hogar_personas", "personas por hogar", "Tamaño medio del hogar"),
    "Porcentaje de hogares unipersonales": ("ine_adrh_hogares_unipersonales_pct", "porcentaje", "Porcentaje de hogares unipersonales"),
    "Porcentaje de población española": ("ine_adrh_poblacion_espanola_pct", "porcentaje", "Porcentaje de población española"),
}
PRINCIPALES = {"ine_adrh_renta_neta_media_persona_eur", "ine_adrh_renta_neta_media_hogar_eur", "ine_adrh_renta_mediana_uc_eur",
               "ine_adrh_gini_indice", "ine_adrh_p80p20_ratio", "ine_adrh_poblacion_personas"}
# variables y niveles que la base pública ya tiene (sección, 2019-2023): no se duplican en el parquet versionado
YA_EN_BASE = {"ine_adrh_renta_neta_media_persona_eur", "ine_adrh_renta_neta_media_hogar_eur", "ine_adrh_gini_indice"}
RX_UMBRAL = re.compile(r"^Población con ingresos por unidad de consumo por (debajo|encima)(?: de)? (?:(\d+)% de la mediana|([\d.]+) Euros)$")
RX_FUENTE = re.compile(r"^Fuente de ingreso: (.+)$")
RX_MENOR = re.compile(r"^Porcentaje de población menor de (\d+) años$")
RX_MAYOR = re.compile(r"^Porcentaje de población de (\d+) y más años$")
RX_EDAD = re.compile(r"^(Menos de \d+ años|De \d+ a \d+ años|\d+ y más años)$")
RX_GEO = re.compile(r"^(.+) (sección|distrito) (\d+)$")
VARS_DESCR: dict[str, tuple[str, str]] = {}   # variable -> (descripcion, unidad)


def _slug(s: str) -> str:
    s = unicodedata.normalize("NFKD", s)
    s = "".join(c for c in s if not unicodedata.combining(c)).lower()
    return re.sub(r"[^a-z0-9]+", "_", s).strip("_")


def _nk(s: str) -> str:
    s = unicodedata.normalize("NFKD", str(s))
    s = "".join(c for c in s if not unicodedata.combining(c)).lower()
    return re.sub(r"[^a-z0-9]+", " ", s).strip()


_CACHE: dict[str, tuple] = {}


def clasifica(seg: str) -> tuple:
    """Clasifica un segmento del nombre de serie ADRH."""
    r = _CACHE.get(seg)
    if r is not None:
        return r
    if seg in ("Dato base", "Porcentaje"):
        r = ("skip",)
    elif seg in ("Total", "Hombres", "Mujeres"):
        r = ("sexo", seg)
    elif seg in ("Española", "Extranjera"):
        r = ("nac", seg)
    elif RX_EDAD.match(seg):
        r = ("edad", seg)
    elif seg in V_RENTA:
        v, u, d = V_RENTA[seg]
        r = ("var", v, u, d, None)
    elif (m := RX_UMBRAL.match(seg)):
        sentido = "bajo" if m.group(1) == "debajo" else "sobre"
        if m.group(2):
            v = f"ine_adrh_pob_{sentido}_umbral_rel_pct"
            d = f"Porcentaje de población con ingresos por unidad de consumo {'por debajo' if sentido == 'bajo' else 'por encima'} de un umbral relativo (% de la mediana)"
            r = ("var", v, "porcentaje", d, f"umbral_pct_mediana={m.group(2)}")
        else:
            v = f"ine_adrh_pob_{sentido}_umbral_fijo_pct"
            d = "Porcentaje de población con ingresos por unidad de consumo por debajo de un umbral fijo (euros)"
            r = ("var", v, "porcentaje", d, f"umbral_eur={m.group(3).replace('.', '')}")
    elif (m := RX_FUENTE.match(seg)):
        r = ("var", f"ine_adrh_fuente_ingreso_{_slug(m.group(1))}_pct", "porcentaje",
             f"Porcentaje de la renta procedente de: {m.group(1)}", None)
    elif (m := RX_MENOR.match(seg)):
        r = ("var", f"ine_adrh_poblacion_menor{m.group(1)}_pct", "porcentaje", f"Porcentaje de población menor de {m.group(1)} años", None)
    elif (m := RX_MAYOR.match(seg)):
        r = ("var", f"ine_adrh_poblacion_{m.group(1)}_mas_pct", "porcentaje", f"Porcentaje de población de {m.group(1)} y más años", None)
    elif (m := RX_GEO.match(seg)):
        r = ("geo", m.group(1), m.group(2), m.group(3))
    else:
        r = ("geo", seg, "municipio", "")   # resto: candidato a nombre de municipio
    _CACHE[seg] = r
    return r


def parsea(nombre: str):
    """-> (variable, unidad, descripcion, desagregacion, geo_nombre, geo_nivel, geo_sufijo) o motivo de descarte (str)."""
    n = re.sub(r"\s+", " ", nombre).strip()
    if n.endswith("."):
        n = n[:-1]
    n = re.sub(r"\. (sección|distrito) (\d+)", r" \1 \2", n, flags=re.I)   # «X. distrito 01.» -> «X distrito 01.»
    n = re.sub(r" (Sección|Distrito) (\d+)", lambda m: " " + m.group(1).lower() + " " + m.group(2), n)
    var = None
    geos = []
    part = {}
    for seg in n.split(". "):
        c = clasifica(seg.strip())
        k = c[0]
        if k == "var":
            if var is not None:
                return "dos_variables"
            var = c
        elif k in ("sexo", "nac", "edad"):
            part[k] = c[1]
        elif k == "geo":
            geos.append(c)
    if var is None:
        return "sin_variable"
    if len(geos) != 1:
        return "geo_" + str(len(geos))
    ds = []
    if var[4]:
        ds.append(var[4])
    for k in ("sexo", "edad", "nac"):
        if k in part:
            ds.append(f"{k}={part[k]}")
    return var[1], var[2], var[3], "|".join(ds), geos[0][1], geos[0][2], geos[0][3]


# ----------------------------------------------------------------------------------------------------------------------
# Territorios
# ----------------------------------------------------------------------------------------------------------------------
# Alias explícitos nombre ADRH -> código INE (cambios de nombre o grafía; juzgados a mano contra los nombres de territorios.parquet de la
# misma provincia; los fusionados o dudosos —Cesuras, Oza dos Ríos, Cerdedo, Cotobade, Darrical, Candín, Alfarp, Goñi— NO se incluyen).
ALIAS = {
    ("01", "Erriberabeitia"): "01047",
    ("03", "Sant Vicent del Raspeig/San Vincente del Raspeig"): "03122",
    ("09", "Santa María Rivarredonda"): "09353",
    ("10", "Aldehuela de Jerte"): "10016",
    ("12", "Castelló de la Plana"): "12040",
    ("17", "Castell-Platja d'Aro"): "17048",
    ("31", "Atez/Atetz"): "31040",
    ("31", "Castillonuevo"): "31071",
    ("31", "Noáin (Valle de Elorz)/Noain (Elortzibar)"): "31088",
    ("43", "Bisbal de Falset, La"): "43027",
    ("46", "Novetlè/Novelé"): "46180",
}
NK_ALIAS = {"castilla la mancha": "Castilla-La Mancha", "alicante alacant": "Alicante/Alacant"}
NOM_CCAA: dict[str, str] = {}
NOM_PROV: dict[str, str] = {}


def carga_terr():
    t = pd.read_parquet(RAIZ / "data" / "base" / "publica" / "territorios.parquet")
    NOM_CCAA.update({n: c for c, n in zip(t.loc[t.nivel == "ccaa", "territorio_codigo"], t.loc[t.nivel == "ccaa", "nombre"])})
    NOM_PROV.update({n: c for c, n in zip(t.loc[t.nivel == "provincia", "territorio_codigo"], t.loc[t.nivel == "provincia", "nombre"])})
    mu = t[(t.nivel == "municipio") & (~t.nombre.str.startswith("municipio "))]
    cods = {n: set(t.loc[t.nivel == n, "territorio_codigo"]) for n in ("municipio", "distrito", "seccion", "provincia", "ccaa", "nacional")}
    exacto = collections.defaultdict(list)
    norm = collections.defaultdict(list)
    for c, n in zip(mu.territorio_codigo, mu.nombre):
        exacto[n].append(c)
        norm[_nk(n)].append(c)
    return cods, exacto, norm


def sellada(codigo: str, nivel: str) -> bool:
    return nivel in ("provincia", "municipio", "distrito", "seccion") and codigo[:2] in SELLADAS


# ----------------------------------------------------------------------------------------------------------------------
# ADRH
# ----------------------------------------------------------------------------------------------------------------------
def procesa_adrh(cods, exacto, norm):
    man = {}
    with open(ENT / "_manifest.csv", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            if "ADRH" in r["fuente"]:
                tid = re.search(r"/(\d+)\.json", r["fichero"]).group(1)
                man[tid] = r
    est = collections.Counter()
    notas_txt = collections.Counter()
    descartes = collections.Counter()
    corresp: dict[tuple, dict] = {}
    cod_vistos: set[int] = set()
    anios_nivel = collections.defaultdict(collections.Counter)
    sec_invalidas = collections.Counter()
    ya_en_base = 0
    principal_rows = []
    SAL.mkdir(parents=True, exist_ok=True)
    writer = None
    schema = pa.schema([(c, pa.bool_() if c in ("redistribuible", "posterior_prereg", "muestra_sellada_v6") else
                         pa.float64() if c == "valor" else pa.string()) for c in COLS])
    for tid in sorted(man, key=int):
        fich = ADRH / f"{tid}.json.gz"
        if not fich.exists():
            descartes["tabla_sin_fichero"] += 1
            continue
        r = man[tid]
        titulo = re.search(r"'([^']*)'", r["edicion"]).group(1)
        d = json.load(gzip.open(fich))
        parsed = []
        votos = collections.Counter()
        for s in d:
            p = parsea(s["Nombre"])
            if isinstance(p, str):
                descartes["nombre_" + p] += 1
                descartes[f"tabla_{tid}_nombre_{p}"] += 1
                parsed.append(None)
                continue
            parsed.append(p)
            if p[5] == "municipio" and len(exacto.get(p[4], ())) == 1:
                votos[exacto[p[4]][0][:2]] += 1
        es_nac = "(NAC-CCAA-PROV)" in r["edicion"]
        ocurr = collections.Counter()
        prov = None
        if votos and not es_nac:
            pv, nv = votos.most_common(1)[0]
            if nv / sum(votos.values()) >= 0.8:
                prov = pv
        cache_cod: dict[str, str | None] = {}

        def codigo_muni(nombre):
            if nombre in cache_cod:
                return cache_cod[nombre]
            cand = [c for c in exacto.get(nombre, ()) if prov is None or c[:2] == prov]
            via = "exacto"
            if not cand and (prov, nombre) in ALIAS:
                cand, via = [ALIAS[(prov, nombre)]], "alias_explicito"
            if not cand:
                cand = [c for c in norm.get(_nk(nombre), ()) if prov is None or c[:2] == prov]
                via = "normalizado"
            if len(cand) == 1:
                res, estado = cand[0], "unica_" + via
            elif len(cand) > 1:
                res, estado = None, "ambigua"
            else:
                res, estado = None, "sin_coincidencia"
            k = (prov or "", nombre)
            if k not in corresp:
                corresp[k] = {"provincia_inferida": prov or "", "nombre_adrh": nombre, "codigo_ine": res or "", "estado": estado, "n_series": 0}
            cache_cod[nombre] = res
            return res

        cols = {c: [] for c in ("territorio_codigo", "nivel", "periodo", "variable", "desagregacion", "valor", "unidad", "metodo_dato")}
        for s, p in zip(d, parsed):
            if p is None:
                continue
            cid = int(re.sub(r"\D", "", s["COD"]) or 0)
            if cid in cod_vistos:
                descartes["serie_duplicada_en_otra_tabla"] += 1
                continue
            cod_vistos.add(cid)
            var, uni, _desc, desag, gnom, gniv, gsuf = p
            VARS_DESCR[var] = (_desc, uni)
            if es_nac:
                k_oc = (var, desag, gnom)
                oc = ocurr[k_oc]
                ocurr[k_oc] += 1
                gnom = NK_ALIAS.get(_nk(gnom), gnom)
                if gnom == "Total Nacional":
                    tc, nv = "00", "nacional"
                elif gnom in NOM_CCAA and gnom in NOM_PROV:
                    tc, nv = (NOM_CCAA[gnom], "ccaa") if oc == 0 else (NOM_PROV[gnom], "provincia")
                elif gnom in NOM_CCAA:
                    tc, nv = NOM_CCAA[gnom], "ccaa"
                elif gnom in NOM_PROV:
                    tc, nv = NOM_PROV[gnom], "provincia"
                else:
                    descartes["nac_ccaa_prov_sin_codigo_ine(islas_u_otros)"] += 1
                    corresp.setdefault(("NAC", gnom), {"provincia_inferida": "NAC", "nombre_adrh": gnom, "codigo_ine": "", "estado": "sin_coincidencia", "n_series": 0})["n_series"] += 1
                    continue
                corresp.setdefault(("NAC", gnom), {"provincia_inferida": "NAC", "nombre_adrh": gnom, "codigo_ine": NOM_CCAA.get(gnom, "") + "/" + NOM_PROV.get(gnom, "") if gnom in NOM_CCAA and gnom in NOM_PROV else tc, "estado": "unica_exacto" if not (gnom in NOM_CCAA and gnom in NOM_PROV) else "unica_por_orden_ccaa_provincia", "n_series": 0})["n_series"] += 1
                mcod = tc
            else:
                mcod = codigo_muni(gnom)
            if mcod is None:
                descartes["serie_municipio_sin_codigo_unico"] += 1
                corresp[(prov or "", gnom)]["n_series"] += 1
                continue
            if not es_nac:
                corresp[(prov or "", gnom)]["n_series"] += 1
            if es_nac:
                pass
            elif gniv == "municipio":
                tc, nv = mcod, "municipio"
            elif gniv == "distrito":
                tc, nv = mcod + gsuf.zfill(2), "distrito"
            else:
                tc, nv = mcod + gsuf.zfill(5), "seccion"
            if tc not in cods[nv]:  # nacional/ccaa/provincia también están en cods (ver carga_terr)
                descartes[f"codigo_{nv}_no_existe_en_territorios_2025"] += 1
                sec_invalidas[nv] += 1
                continue
            for x in s["Data"]:
                if x.get("FK_Periodo") not in (28, None) or x.get("FK_TipoDato", 1) != 1:
                    est["punto_periodo_o_tipo_distinto"] += 1
                    continue
                v = x.get("Valor")
                if x.get("Secreto"):
                    est["secretos"] += 1
                    est["secretos_" + nv] += 1
                    continue
                if v is None:
                    est["nulos"] += 1
                    est["nulos_" + nv] += 1
                    continue
                meto = "observado"
                if x.get("Notas"):
                    txt = " ".join(n.get("texto", "") for n in x["Notas"])
                    notas_txt[txt] += 1
                    if "comarca agraria" in txt:
                        meto = "valor_sustituto_media_comarca_agraria_pob_menor_100"
                    elif "de los municipios de la provincia" in txt:
                        meto = "valor_sustituto_media_provincia_pob_menor_100"
                    elif "del distrito al que pertenece" in txt:
                        meto = "valor_sustituto_media_distrito"
                    elif "Estrategia Territorial de Navarra" in txt:
                        meto = "valor_subarea_estrategia_territorial_navarra"
                    elif "cota superior" in txt:
                        meto = "cota_superior_por_secreto_estadistico"
                    elif "cota inferior" in txt:
                        meto = "cota_inferior_por_secreto_estadistico"
                    else:
                        meto = "observado_con_nota"
                anio = str(x["Anyo"])
                cols["territorio_codigo"].append(tc)
                cols["nivel"].append(nv)
                cols["periodo"].append(anio)
                cols["variable"].append(var)
                cols["desagregacion"].append(desag)
                cols["valor"].append(float(v))
                cols["unidad"].append(uni)
                cols["metodo_dato"].append(meto)
                anios_nivel[(var in PRINCIPALES, nv)][anio] += 1
        n = len(cols["valor"])
        if n == 0:
            continue
        df = pd.DataFrame(cols)
        df["frecuencia"] = "A"
        df["fuente"] = FUENTE_ADRH + f", tabla {tid}"
        df["edicion"] = f"ADRH tabla {tid} ({titulo}); {EDICION_MOD}"
        df["fecha_dato"] = df["periodo"] + "-12-31"
        df["capa"] = "C4"
        df["licencia"] = LIC_ADRH
        df["redistribuible"] = True
        df["origen"] = f"data/raw/v16/renta_parque/_grandes/adrh/{tid}.json.gz"
        df["posterior_prereg"] = False
        df["muestra_sellada_v6"] = [sellada(c, nv) for c, nv in zip(df.territorio_codigo, df.nivel)]
        df = df[COLS]
        tab = pa.Table.from_pandas(df, schema=schema, preserve_index=False)
        if writer is None:
            writer = pq.ParquetWriter(P_COMP, schema, compression="zstd")
        writer.write_table(tab)
        est["filas_validas"] += n
        sel = df[df.variable.isin(PRINCIPALES) & (df.desagregacion == "")]
        dup = sel[(sel.nivel == "seccion") & sel.variable.isin(YA_EN_BASE) & (sel.periodo.astype(int) >= 2019)]
        ya_en_base += len(dup)
        principal_rows.append(sel.drop(dup.index))
        print(f"tabla {tid}: {n} filas; provincia inferida {prov}", flush=True)
    if writer is not None:
        writer.close()
    pr = pd.concat(principal_rows, ignore_index=True) if principal_rows else pd.DataFrame(columns=COLS)
    return pr, est, notas_txt, descartes, corresp, ya_en_base, anios_nivel


# ----------------------------------------------------------------------------------------------------------------------
# Catastro
# ----------------------------------------------------------------------------------------------------------------------
USOS = ["ALMACEN", "COMERCIAL", "CULTURAL", "HOSTELERIA", "INDUSTRIAL", "DEPORTIVO", "SOLAR", "OFICINAS", "SINGULAR", "RELIGIOSO",
        "ESPECTACULOS", "RES", "SANIDAD"]
USO_NOM = {"RES": "residencial"}
CAT_VARS = [
    ("UURBANAS", "catastro_urbano_unidades_numero", "", "unidades urbanas", "Unidades urbanas catastrales (total)"),
    ("V_CATASTRAL", "catastro_urbano_valor_catastral_eur", "", "euros", "Valor catastral total de bienes urbanos"),
    ("V_CONSTRUCCION", "catastro_urbano_valor_construccion_eur", "", "euros", "Valor catastral de construcción"),
    ("V_SUELO", "catastro_urbano_valor_suelo_eur", "", "euros", "Valor catastral de suelo"),
    ("SUPERF_URB", "catastro_urbano_superficie_suelo_m2", "", "m2 (supuesto por el nombre del campo; unidad no verificada)", "Superficie de suelo urbano (campo SUPERF_URB)"),
    ("PARCELAS_URB", "catastro_urbano_parcelas_numero", "", "parcelas", "Parcelas urbanas"),
    ("ULT_REVISION", "catastro_urbano_ano_ultima_revision", "", "año", "Año de la última revisión catastral del municipio"),
]


def procesa_catastro(cods):
    if not CAT.exists():
        AVISOS.append("falta catastro/URBANA2026.xls")
        return pd.DataFrame(columns=COLS), {}
    c = pd.read_excel(CAT, dtype=str)
    c["COD_INE_MUNI"] = c["COD_INE_MUNI"].str.zfill(5)
    est = {"municipios": int(len(c)), "provincias": sorted(c["COD_INE_PROV"].str.zfill(2).unique().tolist())}
    inval = c.loc[~c.COD_INE_MUNI.isin(cods["municipio"]), "COD_INE_MUNI"].tolist()
    est["municipios_codigo_no_valido_descartados"] = inval
    c = c[c.COD_INE_MUNI.isin(cods["municipio"])]
    piezas = []
    esp = list(CAT_VARS)
    for u in USOS:
        n = USO_NOM.get(u, u.lower())
        esp.append((f"UU_{u}", "catastro_urbano_unidades_uso_numero", f"uso={n}", "unidades urbanas", "Unidades urbanas por uso"))
        esp.append((f"V_CAT_{u}", "catastro_urbano_valor_catastral_uso_eur", f"uso={n}", "euros", "Valor catastral por uso"))
    nulos = 0
    for col, var, desag, uni, descr in esp:
        VARS_DESCR[var] = (descr, uni)
        v = pd.to_numeric(c[col], errors="coerce")
        nulos += int(v.isna().sum())
        m = v.notna()
        p = pd.DataFrame({"territorio_codigo": c.loc[m, "COD_INE_MUNI"].values, "valor": v[m].values})
        p["variable"], p["desagregacion"], p["unidad"] = var, desag, uni
        piezas.append(p)
    df = pd.concat(piezas, ignore_index=True)
    est["valores_nulos_omitidos"] = nulos
    df["nivel"] = "municipio"
    df["periodo"] = "2026"
    df["frecuencia"] = "A"
    df["fuente"] = "Catastro, estadísticas catastrales municipales (bienes urbanos), URBANA2026"
    df["edicion"] = "URBANA2026.xls (fecha de referencia 2026-01-01; descargado 2026-10-17)"
    df["fecha_dato"] = "2026-01-01"
    df["capa"] = "C4"
    df["licencia"] = LIC_CAT
    df["redistribuible"] = True
    df["metodo_dato"] = "observado"
    df["origen"] = "data/raw/v16/renta_parque/catastro/URBANA2026.xls"
    df["posterior_prereg"] = False
    df["muestra_sellada_v6"] = [sellada(x, "municipio") for x in df.territorio_codigo]
    return df[COLS], est


# ----------------------------------------------------------------------------------------------------------------------
def main():
    cods, exacto, norm = carga_terr()
    if ADRH.exists():
        pr, est, notas_txt, descartes, corresp, ya_en_base, anios = procesa_adrh(cods, exacto, norm)
    else:
        AVISOS.append("falta _grandes/adrh/: se conservan las filas ADRH del parquet versionado")
        old = pd.read_parquet(P_OUT) if P_OUT.exists() else pd.DataFrame(columns=COLS)
        pr = old[old.fuente.str.startswith("INE, ADRH")]
        est, notas_txt, descartes, corresp, ya_en_base, anios = collections.Counter(), collections.Counter(), collections.Counter(), {}, 0, {}
    cat, est_cat = procesa_catastro(cods)
    out = pd.concat([pr, cat], ignore_index=True)[COLS]
    out = out.sort_values(CLAVE, kind="stable").reset_index(drop=True)
    dup = out.duplicated(CLAVE, keep=False)
    if dup.any():
        AVISOS.append(f"{int(dup.sum())} filas con clave duplicada en el parquet versionado: se conserva la primera")
        out = out.drop_duplicates(CLAVE, keep="first").reset_index(drop=True)
    out.to_parquet(P_OUT, index=False, compression="zstd")

    # diccionario de variables
    filas = []
    for var, g in out.groupby("variable"):
        filas.append(var)
    dic = []
    for var, g in out.groupby("variable"):
        descr, uni = VARS_DESCR.get(var, ("", g.unidad.iloc[0]))
        es_cat = var.startswith("catastro_")
        niv = ",".join(sorted(g.nivel.unique(), key=["nacional", "ccaa", "provincia", "municipio", "distrito", "seccion"].index))
        dic.append({"variable": var, "descripcion": descr + (" (desagregacion: " + "; ".join(sorted({x.split("=")[0] for x in g.desagregacion.unique() for x in x.split("|") if x})) + ")" if (g.desagregacion != "").any() else ""),
                    "unidad": g.unidad.iloc[0], "nivel": niv, "frecuencia": "A", "periodo_min": g.periodo.min(), "periodo_max": g.periodo.max(),
                    "fuente": g.fuente.iloc[0].split(", tabla")[0],
                    "rupturas": ("Catastro del Estado: no incluye Navarra ni el País Vasco (haciendas forales); solo corte 2026-01-01." if es_cat else
                                 "ADRH 2015-2023; seccionado y base de renta por declarar (ver ficha)")})
    # variables del completo no presentes en el versionado
    ya = {d["variable"] for d in dic}
    for var, (descr, uni) in sorted(VARS_DESCR.items()):
        if var not in ya and var.startswith("ine_adrh_"):
            dic.append({"variable": var, "descripcion": descr + " [solo en data/processed/v16/renta_parque_adrh_completo.parquet, no versionado]",
                        "unidad": uni, "nivel": "municipio,distrito,seccion", "frecuencia": "A", "periodo_min": "2015", "periodo_max": "2023",
                        "fuente": "INE, ADRH (Atlas de distribución de renta de los hogares), API wstempus",
                        "rupturas": "ADRH 2015-2023; seccionado y base de renta por declarar (ver ficha)"})
    pd.DataFrame(dic).sort_values("variable").to_csv(DOCS / "renta_parque_variables.csv", index=False, quoting=csv.QUOTE_MINIMAL)
    if corresp:
        cr = pd.DataFrame(list(corresp.values())).sort_values(["provincia_inferida", "nombre_adrh"])
        cr.to_csv(DOCS / "renta_parque_correspondencia.csv", index=False)
        est["correspondencia_estados"] = cr.groupby("estado").size().to_dict()
        est["correspondencia_series_descartadas_por_estado"] = cr[cr.codigo_ine == ""].groupby("estado")["n_series"].sum().to_dict()
    est = dict(est)
    est.update({"descartes": dict(descartes), "notas_de_dato": dict(notas_txt), "filas_ya_en_base_no_duplicadas": int(ya_en_base),
                "catastro": est_cat, "avisos": AVISOS,
                "puntos_por_anio_nivel_principales": {f"{'principal' if k[0] else 'resto'}|{k[1]}": dict(v) for k, v in anios.items()}})
    (SAL / "renta_parque_estadisticas.json").write_text(json.dumps(est, ensure_ascii=False, indent=1, sort_keys=True), encoding="utf-8")
    res = {"rama": "v16-f1-datos-renta_parque",
           "pregunta": "Normalizar al formato largo de la base el ADRH (renta, desigualdad, demografía, municipio/distrito/sección 2015-2023) y el Catastro urbano municipal 2026",
           "capa": "C4", "N": int(len(out)), "metodo": "normalización",
           "notas": f"Filas versionadas {len(out)}; ADRH completo (no versionado) {est.get('filas_validas', 0)} filas; ECV y EPF no normalizadas (microdatos, fase 2). "
                    "posterior_prereg=False (corte V16 sin fijar). Detalle en data/processed/v16/renta_parque_estadisticas.json y docs/v16/fuentes/renta_parque.md."}
    (SAL / "renta_parque_resultado.json").write_text(json.dumps(res, ensure_ascii=False, indent=1), encoding="utf-8")
    for a in AVISOS:
        print("AVISO:", a)
    print("filas versionadas:", len(out))


if __name__ == "__main__":
    main()
