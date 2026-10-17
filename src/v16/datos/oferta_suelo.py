"""V16-F1 · Normalización de la familia oferta_suelo al formato largo de data/base/hechos.parquet.

Determinista (SEED=20261010, sin aleatoriedad) y sin red. Lee solo data/raw/v16/oferta_suelo/, data/base/publica/territorios.parquet
y la geometría municipal versionada data/base/geo/municipios.parquet.
Salidas:
- data/processed/v16/oferta_suelo.parquet: INE IMM (tablas 8381, 8382, 8377), nacional, mensual, redistribuible = sí.
- data/processed/v16/oferta_suelo_terceros.parquet (NO versionado; redistribuible = False): superficie y % de superficie municipal
  en Red Natura 2000 (MITECO, edición 2025; licencia dudosa). Solo si existe el zip en _terceros/_grandes y geopandas/shapely/pyogrio
  están instalados; si no, se omite sin fallar.
- data/processed/v16/oferta_suelo_resultado.json y docs/v16/fuentes/oferta_suelo_variables.csv.
capa = C4 (dato bruto). posterior_prereg = False (el corte de V16 no está fijado).
"""
from __future__ import annotations

import csv
import json
import sys
from pathlib import Path

import pandas as pd

SEED = 20261010
RAIZ = Path(__file__).resolve().parents[3]
ENT = RAIZ / "data" / "raw" / "v16" / "oferta_suelo"
SAL = RAIZ / "data" / "processed" / "v16"
DICC = RAIZ / "docs" / "v16" / "fuentes" / "oferta_suelo_variables.csv"
ZIP_N2000 = ENT / "_terceros" / "_grandes" / "n2000_2025_shp.zip"
REL_N2000 = "data/raw/v16/oferta_suelo/_terceros/_grandes/n2000_2025_shp.zip"
COLS = ["territorio_codigo", "nivel", "periodo", "frecuencia", "variable", "desagregacion", "valor", "unidad", "fuente", "edicion",
        "fecha_dato", "capa", "licencia", "redistribuible", "metodo_dato", "origen", "posterior_prereg", "muestra_sellada_v6"]

# Tabla de correspondencia versionada: código de serie INE (COD) -> nombre de variable (sin tildes, minúsculas).
SERIES = {
    "IMM1": "ine_imm_mano_obra_construccion_indice",
    "IMM32": "ine_imm_materiales_aluminio_indice", "IMM55": "ine_imm_materiales_ligantes_indice",
    "IMM30": "ine_imm_materiales_cemento_indice", "IMM29": "ine_imm_materiales_energia_indice",
    "IMM28": "ine_imm_materiales_focos_luminarias_indice", "IMM27": "ine_imm_materiales_ceramica_indice",
    "IMM26": "ine_imm_materiales_madera_indice", "IMM110": "ine_imm_materiales_plantas_indice",
    "IMM25": "ine_imm_materiales_productos_plasticos_indice", "IMM24": "ine_imm_materiales_productos_quimicos_indice",
    "IMM23": "ine_imm_materiales_aridos_rocas_indice", "IMM54": "ine_imm_materiales_acero_indice",
    "IMM21": "ine_imm_materiales_electronicos_indice", "IMM20": "ine_imm_materiales_cobre_indice",
    "IMM19": "ine_imm_materiales_vidrio_indice", "IMM18": "ine_imm_materiales_explosivos_indice",
    "IMM37": "ine_imm_materiales_especificos_cabezas_explosivas_indice",
    "IMM36": "ine_imm_materiales_especificos_textiles_indice",
    "IMM35": "ine_imm_materiales_especificos_calzado_indice",
    "IMM34": "ine_imm_materiales_especificos_minerales_no_metalicos_indice",
    "IMM33": "ine_imm_materiales_especificos_equipos_electricos_indice",
}
DESC = {
    "IMM1": "Mano de obra en la construcción", "IMM32": "Precio de materiales: aluminio", "IMM55": "Precio de materiales: ligantes",
    "IMM30": "Precio de materiales: cemento", "IMM29": "Precio de materiales: energía", "IMM28": "Precio de materiales: focos y luminarias",
    "IMM27": "Precio de materiales: cerámica", "IMM26": "Precio de materiales: madera", "IMM110": "Precio de materiales: plantas",
    "IMM25": "Precio de materiales: productos plásticos", "IMM24": "Precio de materiales: productos químicos",
    "IMM23": "Precio de materiales: áridos y rocas", "IMM54": "Precio de materiales: acero",
    "IMM21": "Precio de materiales: materiales electrónicos", "IMM20": "Precio de materiales: cobre",
    "IMM19": "Precio de materiales: vidrio", "IMM18": "Precio de materiales: materiales explosivos",
    "IMM37": "Precio de materiales específicos: cabezas explosivas", "IMM36": "Precio de materiales específicos: textiles",
    "IMM35": "Precio de materiales específicos: fabricación de calzado",
    "IMM34": "Precio de materiales específicos: minerales no metálicos",
    "IMM33": "Precio de materiales específicos: materiales y equipos eléctricos",
}
TABLAS = {8381: "ine_imm/imm_8381.json", 8382: "ine_imm/imm_8382.json", 8377: "ine_imm/imm_8377.json"}


def manifiesto() -> dict:
    m = {}
    with open(ENT / "_manifest.csv", encoding="utf-8", newline="") as f:
        for r in csv.DictReader(f):
            m[r["fichero"]] = r
    return m


def sellada(df: pd.DataFrame) -> pd.Series:
    sys.path.insert(0, str(RAIZ / "src"))
    import holdout  # solo devuelve la lista de códigos; no abre nada sellado
    prov = {str(p).zfill(2) for p in holdout.provincias_selladas_v6()}
    return df.nivel.isin(["provincia", "municipio", "distrito", "seccion"]) & df.territorio_codigo.str[:2].isin(prov)


def fin_mes(periodo: pd.Series) -> pd.Series:
    return (pd.to_datetime(periodo + "-01") + pd.offsets.MonthEnd(0)).dt.strftime("%Y-%m-%d")


def cabecera(df: pd.DataFrame, r: dict, rel: str) -> pd.DataFrame:
    df = df.copy()
    df["fuente"] = r["fuente"]
    df["edicion"] = r["edicion"] + " (descarga " + r["fecha_descarga"] + ")"
    df["licencia"] = r["licencia"]
    df["redistribuible"] = r["redistribuible"].strip().lower() == "sí"
    df["origen"] = rel
    df["capa"] = "C4"
    df["posterior_prereg"] = False
    df["metodo_dato"] = "observado"
    df["muestra_sellada_v6"] = sellada(df)
    return df[COLS]


def imm(man: dict) -> pd.DataFrame:
    partes = []
    for tabla, rel_corto in TABLAS.items():
        rel = "data/raw/v16/oferta_suelo/" + rel_corto
        datos = json.loads((ENT / rel_corto).read_text(encoding="utf-8"))
        filas = []
        for s in datos:
            cod = s["COD"]
            base = "índice base julio 1980" if cod == "IMM1" else "índice base 2011=100"
            for d in s["Data"]:
                if d.get("Secreto") or d["Valor"] is None:
                    continue
                filas.append((f"{d['Anyo']}-{int(d['FK_Periodo']):02d}", SERIES[cod], cod, float(d["Valor"]), base))
        df = pd.DataFrame(filas, columns=["periodo", "variable", "desagregacion", "valor", "unidad"])
        df["territorio_codigo"], df["nivel"], df["frecuencia"] = "00", "nacional", "M"
        df["fecha_dato"] = fin_mes(df.periodo)
        partes.append(cabecera(df, man[rel], rel))
    out = pd.concat(partes, ignore_index=True)
    return out.sort_values(["variable", "periodo"]).reset_index(drop=True)


def red_natura(man: dict, terr: pd.DataFrame):
    """Superficie y % municipal en Red Natura 2000 (LAEA EPSG:3035; solapes disueltos). Devuelve (df, info) o (None, motivo)."""
    if not ZIP_N2000.exists():
        return None, "zip de Red Natura 2000 ausente"
    try:
        import geopandas as gpd
        import pyogrio  # noqa: F401
        import shapely
        from shapely.strtree import STRtree
    except ImportError as e:  # sin librerías: no se calcula
        return None, f"librerías no disponibles ({e})"
    geo_p = RAIZ / "data" / "base" / "geo" / "municipios.parquet"
    if not geo_p.exists():
        return None, "geometría municipal ausente"
    mun = gpd.read_parquet(geo_p)
    mun["cod_municipio"] = mun.cod_municipio.astype(str).str.zfill(5)
    validos = set(terr.loc[terr.nivel == "municipio", "territorio_codigo"])
    sin_terr = sorted(set(mun.cod_municipio) - validos)
    mun = mun[mun.cod_municipio.isin(validos)].drop_duplicates("cod_municipio").reset_index(drop=True)
    sin_geo = sorted(validos - set(mun.cod_municipio))
    mun = mun.to_crs(3035)
    mun["geometry"] = shapely.make_valid(mun.geometry.values)
    base = "/vsizip/" + str(ZIP_N2000) + "/"
    capas = ["n2000_spatial_es_pibal_proy_end25.shp", "n2000_spatial_es_can_proy_end25.shp"]
    geoms = []
    for c in capas:
        g = gpd.read_file(base + c, engine="pyogrio").to_crs(3035)
        geoms.extend(shapely.make_valid(g.geometry.values))
    union = shapely.union_all(geoms)  # disuelve solapes LIC/ZEPA y entre capas
    partes = [p for p in shapely.get_parts(union) if p.geom_type in ("Polygon", "MultiPolygon") and not p.is_empty]
    arbol = STRtree(partes)
    areas_mun, areas_rn = [], []
    for geom in mun.geometry.values:
        a = geom.area
        cand = arbol.query(geom, predicate="intersects")
        r = 0.0
        if len(cand):
            r = sum(geom.intersection(partes[i]).area for i in cand)  # partes disjuntas tras la unión
        areas_mun.append(a)
        areas_rn.append(min(r, a))
    mun["sup_mun_ha"] = [a / 1e4 for a in areas_mun]
    mun["sup_rn_ha"] = [a / 1e4 for a in areas_rn]
    mun["pct"] = 100.0 * mun.sup_rn_ha / mun.sup_mun_ha
    r = man[REL_N2000]
    ed = r["edicion"] + " (descarga " + r["fecha_descarga"] + ")"
    filas = []
    for var, col, uni in [("miteco_rn2000_superficie_municipio_ha", "sup_rn_ha", "hectáreas (EPSG:3035, solapes disueltos)"),
                          ("miteco_rn2000_porcentaje_superficie_municipal", "pct", "% de la superficie municipal"),
                          ("ine_geo_superficie_municipio_ha", "sup_mun_ha", "hectáreas (EPSG:3035, polígono INE 2025)")]:
        d = pd.DataFrame({"territorio_codigo": mun.cod_municipio, "variable": var, "valor": mun[col].astype(float), "unidad": uni})
        filas.append(d)
    df = pd.concat(filas, ignore_index=True)
    df["nivel"], df["periodo"], df["frecuencia"], df["desagregacion"] = "municipio", "2025", "A", ""
    df["fecha_dato"] = "2025-12-31"
    df["fuente"] = r["fuente"]
    df["edicion"] = ed
    df["licencia"] = r["licencia"]
    df["redistribuible"] = False
    df["origen"] = REL_N2000
    df["capa"], df["posterior_prereg"] = "C4", False
    df["metodo_dato"] = "calculado: intersección geométrica municipio x Red Natura 2000 disuelta (LAEA EPSG:3035)"
    df.loc[df.variable == "ine_geo_superficie_municipio_ha", "metodo_dato"] = "calculado: área del polígono municipal (LAEA EPSG:3035)"
    df["muestra_sellada_v6"] = sellada(df)
    info = {"municipios_calculados": int(len(mun)), "sin_geometria": sin_geo, "geometria_sin_territorio": sin_terr,
            "municipios_con_rn2000": int((mun.sup_rn_ha > 0).sum())}
    return df[COLS].sort_values(["variable", "territorio_codigo"]).reset_index(drop=True), info


def diccionario(frames: list[pd.DataFrame], rup: dict) -> None:
    filas = []
    desc_rn = {
        "miteco_rn2000_superficie_municipio_ha": "Superficie municipal incluida en Red Natura 2000 (LIC/ZEC y ZEPA disueltos), edición 2025",
        "miteco_rn2000_porcentaje_superficie_municipal": "Porcentaje de la superficie municipal incluido en Red Natura 2000, edición 2025",
        "ine_geo_superficie_municipio_ha": "Superficie del polígono municipal (denominador del porcentaje)",
    }
    inv = {v: k for k, v in SERIES.items()}
    for df in frames:
        for (var, nivel, frec, unidad), g in df.groupby(["variable", "nivel", "frecuencia", "unidad"]):
            cod = inv.get(var)
            filas.append({"variable": var, "descripcion": (DESC[cod] + f" (serie INE {cod})") if cod else desc_rn[var], "unidad": unidad,
                          "nivel": nivel, "frecuencia": frec, "periodo_min": g.periodo.min(), "periodo_max": g.periodo.max(),
                          "fuente": "ine_imm" if cod else ("miteco_rn2000 (terceros, no versionado)" if var.startswith("miteco") else "ine_cartografia + calculo propio (terceros)"),
                          "rupturas": rup["imm1"] if cod == "IMM1" else (rup["imm"] if cod else rup["rn"])})
    with open(DICC, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["variable", "descripcion", "unidad", "nivel", "frecuencia", "periodo_min", "periodo_max", "fuente", "rupturas"])
        w.writeheader()
        w.writerows(filas)


def main() -> None:
    SAL.mkdir(parents=True, exist_ok=True)
    man = manifiesto()
    terr = pd.read_parquet(RAIZ / "data" / "base" / "publica" / "territorios.parquet")
    pub = imm(man)
    assert not pub.duplicated(["territorio_codigo", "nivel", "periodo", "variable", "desagregacion"]).any()
    pub.to_parquet(SAL / "oferta_suelo.parquet", index=False)
    rn, info = red_natura(man, terr)
    frames = [pub]
    if rn is not None:
        rn.to_parquet(SAL / "oferta_suelo_terceros.parquet", index=False)
        frames.append(rn)
    rup = {
        "imm1": "Base julio 1980 (distinta de las demás series, base 2011=100): no comparable en nivel. Serie nacional única; sin ruptura de seccionado.",
        "imm": "Base 2011=100 (dic 2011); series nacionales, no municipales. Las series de materiales específicos tienen menos observaciones (comienzan con huecos) sin interpolar.",
        "rn": "Edición única 2025 (sin serie temporal). Áreas en EPSG:3035 sobre polígono municipal INE 2025 derivado de secciones; la franja marina de sitios mixtos queda fuera por intersectar con el polígono terrestre.",
    }
    diccionario(frames, rup)
    notas = ("Normalización INE IMM (tablas 8381, 8382, 8377): nacional mensual, redistribuible sí. "
             + (f"Red Natura 2000 calculada por municipio en terceros (no versionado): {info}." if rn is not None
                else f"Red Natura 2000 no calculada: {info}."))
    res = {"rama": "v16-f1-datos-oferta_suelo",
           "pregunta": "Q4: insumos de oferta de suelo normalizados (costes de construcción nacionales; restricción física Red Natura 2000 por municipio)",
           "capa": "C4", "N": int(len(pub)) , "metodo": "normalización", "notas": notas,
           "N_terceros": int(len(rn)) if rn is not None else 0}
    (SAL / "oferta_suelo_resultado.json").write_text(json.dumps(res, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(res, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
