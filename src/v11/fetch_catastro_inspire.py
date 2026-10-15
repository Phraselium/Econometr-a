"""V11-DATOS (bloque 3, punto 11): Catastro, servicio ATOM INSPIRE de edificios (Buildings), València ciudad, su área
metropolitana y las otras capitales de la Comunitat Valenciana, agregado a sección censal (y barrio en València).

- Feed por provincia: https://www.catastro.hacienda.gob.es/INSPIRE/buildings/<PP>/ES.SDGC.bu.atom_<PP>.xml; un zip por
  municipio con building.gml (un elemento por edificio: uso actual, nº de inmuebles, nº de viviendas, superficie
  construida oficial, año de construcción, estado, envolvente en EPSG:25830).
- CÓDIGOS: el Catastro usa su propio código de municipio (DGC), distinto del INE (p. ej., DGC 46900 = València,
  INE 46250; DGC 46250 = Turís). Para no cruzar por nombre ni por código DGC, cada edificio se asigna por POSICIÓN
  (centro del envolvente) a la sección censal 2025 del INE (data/base/geo/secciones.parquet) y de ahí al municipio INE.
  La correspondencia DGC → INE resultante (municipio INE que recibe la mayoría de los edificios de cada zip) se
  guarda en correspondencia_dgc_ine.csv.
- Ámbito: València (INE 46250); municipios de la provincia 46 cuyo centroide está a ≤ 20 km del de València (definición
  operativa de área metropolitana, documentada en decisiones_datos.md) UNIDOS a los 90 del ámbito oficial PATEVAL (GVA); Alicante/Alacant (03014) y Castelló de la
  Plana (12040). La selección de zips se hace por nombre normalizado frente al nomenclátor INE y se verifica después
  con la asignación espacial.
- Salidas: edificios_seccion.csv.gz (sección × uso × periodo de construcción: edificios, inmuebles, viviendas,
  superficie construida); edificios_barrio_valencia.csv.gz; correspondencia_dgc_ine.csv. Los zips originales no se
  versionan.
Licencia Catastro: reutilización libre con reconocimiento (Resolución DGC de 2016; datos INSPIRE de libre acceso).
"""
from __future__ import annotations

import difflib
import re
import sys
import unicodedata
import zipfile
from pathlib import Path

import geopandas as gpd
import numpy as np
import pandas as pd
import requests

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from src.v11.comun import CABECERAS, GZ_PANDAS, RAIZ, RAW11, descargar, registrar, verificar_manifiesto  # noqa: E402

FUENTE = "catastro_inspire"
DIR = RAW11 / FUENTE
ATOM = "https://www.catastro.hacienda.gob.es/INSPIRE/buildings/{p}/ES.SDGC.bu.atom_{p}.xml"
LIC = "Catastro (DGC): reutilización libre con reconocimiento de la fuente"
GEO = RAIZ / "data" / "base" / "geo"
VLC, RADIO_KM = "46250", 20
CAPITALES = ["03014", "12040"]
PERIODOS = [0, 1940, 1960, 1980, 2000, 2010, 2100]
ETIQ = ["<1941", "1941-1960", "1961-1980", "1981-2000", "2001-2010", ">2010"]
RX = {k: re.compile(v) for k, v in {
    "uso": r"<bu-ext2d:currentUse>([^<]+)<", "inm": r"<bu-ext2d:numberOfBuildingUnits>(\d+)<",
    "viv": r"<bu-ext2d:numberOfDwellings>(\d+)<", "sup": r"<bu-ext2d:value uom=\"m2\">([\d.]+)<",
    "anio": r"<bu-core2d:end>(\d{4})-", "estado": r"<bu-core2d:conditionOfConstruction>([^<]+)<",
    "lo": r"<gml:lowerCorner>([\d.]+) ([\d.]+)<", "up": r"<gml:upperCorner>([\d.]+) ([\d.]+)<"}.items()}


def candidatos(nombre: str) -> list[str]:
    """Variantes normalizadas de un nombre INE: cada parte bilingüe («A/B») y el artículo pospuesto («Pobla, la»)."""
    out = []
    for parte in nombre.split("/"):
        m = re.match(r"^(.*), (la|el|les|els|l'|los|las)$", parte.strip(), re.I)
        out += [norm(parte)] + ([norm(f"{m.group(2)} {m.group(1)}"), norm(m.group(1))] if m else [])
    partes = nombre.split("/")
    if len(partes) == 2:  # el Catastro escribe «ALICANTE ALACANT», «MONTCADA MONCADA»
        out += [norm(partes[0] + partes[1]), norm(partes[1] + partes[0])]
    return out


def norm(s: str) -> str:
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode().upper()
    s = re.sub(r"\(([^)]*)\)", r"\1", s)
    return re.sub(r"[^A-Z]", "", s)


def ambito() -> pd.DataFrame:
    m = gpd.read_parquet(GEO / "municipios.parquet").to_crs(25830)
    c = m.geometry.centroid
    d = c.distance(c[m.cod_municipio == VLC].iloc[0]) / 1000
    pat = RAIZ / "data/raw/v11/gva_pateval/pateval_municipios.csv"   # ámbito oficial PATEVAL (segunda pasada)
    oficial = set(pd.read_csv(pat, dtype=str).cod_municipio) if pat.exists() else set()
    sel = m[((m.cod_provincia == "46") & (d <= RADIO_KM)) | m.cod_municipio.isin(CAPITALES) | m.cod_municipio.isin(oficial)]
    return pd.DataFrame({"cod_municipio": sel.cod_municipio, "nombre": sel.nombre_municipio, "dist_km": d[sel.index].round(1)})


def zips(prov: str) -> dict[str, tuple[str, str]]:
    x = requests.get(ATOM.format(p=prov), headers=CABECERAS, timeout=120).text
    out = {}
    for u in re.findall(r'href="(https?://[^"]+A\.ES\.SDGC\.BU\.(\d{5})\.zip)"', x):
        nombre = u[0].split("/")[-2].split("-", 1)[1]
        for k in [nombre] + nombre.split("-"):  # «ALICANTE-ALACANT»: cada variante
            out.setdefault(norm(k), (u[1], u[0]))
    return out


def edificios(zp: Path) -> pd.DataFrame:
    with zipfile.ZipFile(zp) as z:
        n = next(x for x in z.namelist() if x.endswith(".building.gml"))
        texto = z.read(n).decode("utf-8", "replace")
    filas = []
    for b in texto.split("</bu-ext2d:Building>")[:-1]:
        g = {k: r.search(b) for k, r in RX.items()}
        if not (g["lo"] and g["up"]):
            continue
        filas.append((g["uso"].group(1) if g["uso"] else "", int(g["inm"].group(1)) if g["inm"] else 0,
                      int(g["viv"].group(1)) if g["viv"] else 0, float(g["sup"].group(1)) if g["sup"] else np.nan,
                      int(g["anio"].group(1)) if g["anio"] else np.nan, g["estado"].group(1) if g["estado"] else "",
                      (float(g["lo"].group(1)) + float(g["up"].group(1))) / 2, (float(g["lo"].group(2)) + float(g["up"].group(2))) / 2))
    return pd.DataFrame(filas, columns=["uso", "inmuebles", "viviendas", "superficie", "anio", "estado", "x", "y"])


def main(verificar: bool = False) -> int:
    DIR.mkdir(parents=True, exist_ok=True)
    if verificar:
        return verificar_manifiesto(FUENTE)
    amb = ambito()
    sec = gpd.read_parquet(GEO / "secciones.parquet").to_crs(25830)
    col_sec = next(c for c in sec.columns if "seccion" in c)
    bar = gpd.read_parquet(GEO / "barrios_valencia.parquet").to_crs(25830)
    feeds = {p: zips(p) for p in sorted({c[:2] for c in amb.cod_municipio})}
    partes, corr, sin = [], [], []
    for r in amb.itertuples():
        f = feeds[r.cod_municipio[:2]]
        k = next((f[c] for c in candidatos(r.nombre) if c in f), None)
        if k is None:   # último recurso (p. ej. «PUOL» por «PUÇOL»: el feed pierde la Ç); se verifica con la asignación espacial
            cerca = difflib.get_close_matches(candidatos(r.nombre)[0], list(f), n=1, cutoff=0.85)
            k = f[cerca[0]] if cerca else None
        if k is None:
            sin.append(f"{r.cod_municipio} {r.nombre}")
            continue
        dgc, url = k
        try:
            zp = descargar(url, DIR / "original" / f"BU_{dgc}.zip", timeout=900)
        except RuntimeError as e:
            sin.append(f"{r.cod_municipio} {r.nombre} (descarga: {e})")
            continue
        e = edificios(zp)
        p = gpd.GeoDataFrame(e, geometry=gpd.points_from_xy(e.x, e.y), crs=25830)
        p = gpd.sjoin(p, sec[[col_sec, "geometry"]], how="left", predicate="within").drop(columns="index_right")
        p["cod_municipio_ine"] = p[col_sec].str[:5]
        moda = p.cod_municipio_ine.value_counts()
        corr.append({"dgc": dgc, "nombre_catastro": url.split("/")[-2], "cod_municipio_ine": moda.index[0] if len(moda) else "",
                     "cuota_edificios_en_ine": round(moda.iloc[0] / len(p), 4) if len(moda) else np.nan,
                     "cod_municipio_seleccion": r.cod_municipio, "dist_km_valencia": r.dist_km, "edificios": len(p)})
        if r.cod_municipio == VLC:
            b = gpd.sjoin(p.drop(columns=[col_sec]), bar[[c for c in bar.columns if c != "geometry"][:2] + ["geometry"]],
                          how="left", predicate="within")
            partes.append(("barrio", b))
        partes.append(("seccion", p))
        print(r.cod_municipio, r.nombre, dgc, len(p), moda.index[0] if len(moda) else "")
    for nivel in ("seccion", "barrio"):
        d = pd.concat([x for n, x in partes if n == nivel], ignore_index=True)
        d["periodo_construccion"] = pd.cut(d.anio, PERIODOS, labels=ETIQ).astype(str)
        clave = col_sec if nivel == "seccion" else [c for c in d.columns if c.startswith(("cod_barrio", "codbarrio", "barrio"))][0]
        if nivel == "barrio":
            d[clave] = pd.to_numeric(d[clave], errors="coerce").astype("Int64").astype("string")
        g = (d.groupby([clave, "uso", "periodo_construccion"], dropna=False)
             .agg(edificios=("uso", "size"), inmuebles=("inmuebles", "sum"), viviendas=("viviendas", "sum"),
                  superficie_construida_m2=("superficie", "sum")).reset_index().rename(columns={clave: "cod_" + nivel}))
        r = DIR / (f"edificios_{nivel}.csv.gz" if nivel == "seccion" else "edificios_barrio_valencia.csv.gz")
        g.to_csv(r, index=False, compression=GZ_PANDAS)
        registrar(FUENTE, r, ATOM.format(p="<PP>"), edicion="Catastro INSPIRE Buildings (ATOM; fecha de los GML 2026)", periodo="stock vigente (2026)",
                  nivel_territorial="sección censal INE 2025" if nivel == "seccion" else "barrio de València", licencia=LIC, redistribuible=True,
                  notas=f"asignación espacial por centro del envolvente; sin sección = cod vacío; edificios={int(g.edificios.sum())}")
    # obra nueva: viviendas en edificios residenciales por municipio INE y AÑO EXACTO de construcción (stock vigente;
    # edificios demolidos no constan, por lo que los años antiguos son cota inferior de lo construido entonces)
    d = pd.concat([x for n, x in partes if n == "seccion"], ignore_index=True)
    d = d[d.uso.str.contains("residential", na=False) & d.anio.notna()]
    ob = d.groupby(["cod_municipio_ine", "anio"], as_index=False).agg(edificios=("uso", "size"), viviendas=("viviendas", "sum"))
    ob["anio"] = ob.anio.astype(int)
    ro = DIR / "viviendas_por_anio_construccion_municipio.csv.gz"
    ob.rename(columns={"cod_municipio_ine": "cod_municipio", "anio": "anio_construccion"}).to_csv(ro, index=False, compression=GZ_PANDAS)
    registrar(FUENTE, ro, ATOM.format(p="<PP>"), edicion="Catastro INSPIRE Buildings (agregado propio)", periodo="stock vigente (2026)",
              nivel_territorial="municipio INE (asignación espacial)", licencia=LIC, redistribuible=True,
              notas="viviendas y edificios residenciales por año de construcción (dateOfConstruction); obra nueva por año = stock "
                    "superviviente construido ese año")
    C = pd.DataFrame(corr)
    rc = DIR / "correspondencia_dgc_ine.csv"
    C.to_csv(rc, index=False)
    registrar(FUENTE, rc, ATOM.format(p="<PP>"), edicion="elaboración propia (asignación espacial)", periodo="2026",
              nivel_territorial="municipio", licencia=LIC, redistribuible=True, notas=f"no encontrados: {sin}")
    for z in sorted((DIR / "original").glob("BU_*.zip")):
        registrar(FUENTE, z, ATOM.format(p=z.stem[3:5]), edicion="Catastro INSPIRE Buildings", periodo="2026", nivel_territorial="microdatos (edificio)",
                  licencia=LIC, redistribuible=True, notas="no versionado (tamaño): se regenera con make datos_v11")
    print("sin zip:", sin)
    return 0


if __name__ == "__main__":
    sys.exit(main("--verificar" in sys.argv))
