"""V11-DATOS, segunda pasada: Generalitat Valenciana (ICV), ámbito del Plan de Acción Territorial Metropolitano de
València (PATEVAL, en tramitación; CKAN dadesobertes.gva.es, CC BY 4.0), servicio ArcGIS REST
carto.icv.gva.es/.../ordenacion_territorial/MapServer/56. Se guarda la envolvente (GeoJSON) y la lista de municipios INE
cuyo punto representativo (seccionado 2025 del proyecto) cae dentro: definición OFICIAL del área metropolitana, que
sustituye a la operativa de 20 km en el Catastro INSPIRE (se usa la unión de ambas).
"""
from __future__ import annotations

import sys
from pathlib import Path

import geopandas as gpd
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from src.v11.comun import RAIZ, RAW11, descargar, registrar, verificar_manifiesto  # noqa: E402

FUENTE = "gva_pateval"
DIR = RAW11 / FUENTE
URL = ("https://carto.icv.gva.es/arcgis/rest/services/tm_infraestructuras/ordenacion_territorial/MapServer/56/query"
       "?where=1%3D1&outFields=*&outSR=4326&f=geojson")
LIC = "Generalitat Valenciana (ICV): CC BY 4.0"


def municipios() -> pd.DataFrame:
    p = gpd.read_file(DIR / "pateval_ambito.geojson")
    m = gpd.read_parquet(RAIZ / "data/base/geo/municipios.parquet")
    pt = m.to_crs(25830).representative_point().to_crs(4326)
    dentro = m[pt.within(p.union_all())]
    return dentro[["cod_municipio", "nombre_municipio"]].sort_values("cod_municipio")


def main(verificar: bool = False) -> int:
    DIR.mkdir(parents=True, exist_ok=True)
    if verificar:
        return verificar_manifiesto(FUENTE)
    g = descargar(URL, DIR / "pateval_ambito.geojson", timeout=300)
    registrar(FUENTE, g, URL, edicion="PATEVAL, ámbito en tramitación (CKAN modificado 2026-09-23)", periodo="2026",
              nivel_territorial="polígono", licencia=LIC, redistribuible=True, notas="envolvente del ámbito")
    m = municipios()
    r = DIR / "pateval_municipios.csv"
    m.to_csv(r, index=False)
    registrar(FUENTE, r, URL, edicion="elaboración propia (punto representativo del municipio dentro del ámbito)", periodo="2026",
              nivel_territorial="municipio (código INE)", licencia=LIC, redistribuible=True, notas=f"{len(m)} municipios")
    print(len(m))
    return 0


if __name__ == "__main__":
    sys.exit(main("--verificar" in sys.argv))
