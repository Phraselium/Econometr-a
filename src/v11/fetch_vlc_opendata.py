"""V11-DATOS (bloque 3, punto 14, y bloque 4, punto 18): Ajuntament de València, portal de datos abiertos (CKAN,
https://opendata.vlci.valencia.es; el antiguo valencia.opendatasoft.com ya no existe). Licencia CC BY 4.0.

Conjuntos (se toma el primer recurso CSV; si no hay, GeoJSON; el GTFS se baja como zip):
- equipamients-municipals-equipamientos-municipales (equipamientos), hospitales;
- vulnerabilidad-por-barrios (índices de vulnerabilidad 2021 por barrio);
- urban-area-by-neighborhoods (superficie urbana por barrio);
- illa-de-cases-cadastrals-amb-dades-de-poblacio (manzanas catastrales con población por edad);
- vivendes-proteccio-publica-vpp-viviendas-proteccion-publica-vpp (promociones de VPP);
- free-housing-square-meter-price (precio del m² de vivienda libre, series del Ajuntament);
- income-per-household-and-person (renta por hogar y persona);
- google-transit-lines-stops-bus-schedules (GTFS de la EMT de València; punto 18).
NO publicados en el portal (documentado en fuentes_fallidas.md y solicitudes): licencias urbanísticas y de cambio de
uso por barrio; padrón por barrio × edad × nacionalidad (solo en los anuarios de la Oficina d'Estadística; los
extranjeros por distrito y sección del IVE ya están en data/raw desde v9).
"""
from __future__ import annotations

import sys
from pathlib import Path

import requests

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from src.v11.comun import CABECERAS, RAW11, descargar, registrar, verificar_manifiesto  # noqa: E402

FUENTE = "vlc_opendata"
DIR = RAW11 / FUENTE
API = "https://opendata.vlci.valencia.es/api/3/action/package_show?id={id}"
LIC = "Ajuntament de València: CC BY 4.0"
CONJUNTOS = ["equipamients-municipals-equipamientos-municipales", "hospitales", "vulnerabilidad-por-barrios",
             "urban-area-by-neighborhoods", "illa-de-cases-cadastrals-amb-dades-de-poblacio",
             "vivendes-proteccio-publica-vpp-viviendas-proteccion-publica-vpp", "free-housing-square-meter-price",
             "income-per-household-and-person", "google-transit-lines-stops-bus-schedules"]
PREF = ["CSV", "GEOJSON", "ZIP", "GTFS", "JSON"]


def main(verificar: bool = False) -> int:
    DIR.mkdir(parents=True, exist_ok=True)
    if verificar:
        return verificar_manifiesto(FUENTE)
    fallos = []
    for c in CONJUNTOS:
        try:
            p = requests.get(API.format(id=c), headers=CABECERAS, timeout=120).json()["result"]
        except Exception as e:  # noqa: BLE001
            fallos.append(f"{c}: {e}")
            continue
        rec = sorted(p["resources"], key=lambda r: PREF.index(r.get("format", "").upper()) if r.get("format", "").upper() in PREF else 99)
        rec = [r for r in rec if r.get("url")]
        if not rec:
            fallos.append(f"{c}: sin recursos")
            continue
        r = rec[0]
        fmt = (r.get("format") or "dat").lower()
        ext = {"geojson": "geojson", "csv": "csv", "zip": "zip", "gtfs": "zip", "json": "json"}.get(fmt, "dat")
        ruta = DIR / f"{c[:60]}.{ext}"
        try:
            descargar(r["url"], ruta, timeout=600)
        except RuntimeError as e:
            fallos.append(f"{c}: {e}")
            continue
        grande = ruta.stat().st_size > 50e6
        registrar(FUENTE, ruta, r["url"], edicion=f"{p['title']} (modificado {p.get('metadata_modified', '')[:10]})",
                  periodo=p.get("metadata_modified", "")[:10], nivel_territorial="València (barrio, manzana, punto o línea)",
                  licencia=LIC, redistribuible=not grande,
                  notas=("no versionado (>50 MB); " if grande else "") + f"CKAN id={c}; formato {fmt}")
        print(c, fmt, ruta.stat().st_size)
    print("fallos:", fallos)
    return 0


if __name__ == "__main__":
    sys.exit(main("--verificar" in sys.argv))
