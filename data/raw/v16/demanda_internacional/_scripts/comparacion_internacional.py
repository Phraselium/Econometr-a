"""Fuente 5 (demanda_internacional): comparación internacional.

- OCDE, Analytical house prices (DSD_AN_HOUSE_PRICES@DF_HOUSE_PRICES), todos los países de la OCDE
  disponibles en el dataflow (lista de 37 áreas, sin filtrar medida; historia completa). Se guarda
  comprimido (.csv.gz). El fichero previo de data/raw/oecd_house_prices.csv cubre 27 países (no se toca).
- Eurostat ilc_lvho07a (sobrecarga de coste de vivienda por edad, sexo y situación de pobreza), todos los
  geos y años desde 2003, formato SDMX-CSV. Se guarda comprimido.

Limitación declarada: ilc_lvho07a no tiene desglose por tenencia; la tenencia está en ilc_lvho02 (ya en
data/raw/v5/ca_eurostat_ilc_lvho02.csv, 32 geos). Se declara en la ficha.

Caché: no vuelve a descargar si el fichero existe, salvo FORCE=1.
Uso: python3 -I comparacion_internacional.py
"""
import gzip
import os
import shutil
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from manifiesto import FAMILIA_DIR, ahora_utc, descargar, registrar, relativa, sha256_fichero  # noqa: E402

FORCE = os.environ.get("FORCE") == "1"
PAISES_OCDE = ("AUS+AUT+BEL+CAN+CHL+COL+CRI+CZE+DNK+EST+FIN+FRA+DEU+GRC+HUN+ISL+IRL+ISR+ITA+JPN+KOR"
               "+LVA+LTU+LUX+MEX+NLD+NZL+NOR+POL+PRT+SVK+SVN+ESP+SWE+CHE+TUR+GBR+USA")
URL_OCDE = ("https://sdmx.oecd.org/public/rest/data/OECD.ECO.MPD,DSD_AN_HOUSE_PRICES@DF_HOUSE_PRICES,/"
            + PAISES_OCDE + ".Q....?format=csvfilewithlabels")
URL_EUROSTAT = ("https://ec.europa.eu/eurostat/api/dissemination/sdmx/2.1/data/ilc_lvho07a/"
                "?format=SDMX-CSV&startPeriod=2003")
CARPETA_OCDE = os.path.join(FAMILIA_DIR, "comparacion_internacional")
CARPETA_EU = os.path.join(FAMILIA_DIR, "eurostat_ilc")


def comprimir(origen, destino):
    with open(origen, "rb") as f_in, gzip.open(destino, "wb") as f_out:
        shutil.copyfileobj(f_in, f_out)
    os.remove(origen)


def contar_lineas_gz(ruta):
    with gzip.open(ruta, "rt", encoding="utf-8") as f:
        return sum(1 for _ in f) - 1


def procesar(url, carpeta, nombre_gz, fuente, nivel, licencia, notas, periodo_nota):
    os.makedirs(carpeta, exist_ok=True)
    destino = os.path.join(carpeta, nombre_gz)
    if os.path.exists(destino) and not FORCE:
        print("caché:", relativa(destino))
    else:
        tmp = destino[:-3]
        descargar(url, tmp, timeout=600)
        comprimir(tmp, destino)
        print("descargado:", relativa(destino))
    sha = sha256_fichero(destino)
    n = contar_lineas_gz(destino)
    registrar({
        "fuente": fuente,
        "fichero": relativa(destino),
        "url": url,
        "fecha_descarga": ahora_utc(),
        "edicion": "endpoint vigente en la fecha de descarga (ver «updated»/«LAST UPDATE» del propio fichero)",
        "periodo": periodo_nota,
        "nivel_territorial": nivel,
        "n_filas": n,
        "sha256": sha,
        "licencia": licencia,
        "redistribuible": "sí",
        "notas": notas,
    })
    print("filas:", n, "sha256:", sha)


def main():
    procesar(
        URL_OCDE, CARPETA_OCDE, "oecd_house_prices_todos.csv.gz",
        "OCDE, Analytical house prices (DF_HOUSE_PRICES)",
        "país (37 áreas OCDE)",
        "Términos de uso del OECD (https://www.oecd.org/termsandconditions/): reutilización con cita de la fuente",
        "Mismos campos que data/raw/oecd_house_prices.csv (medida, ajuste, unidad). Cobertura ampliada respecto a los 27 países previos.",
        "2000-Q1 a último dato del endpoint",
    )
    procesar(
        URL_EUROSTAT, CARPETA_EU, "ilc_lvho07a_todos_desgloses.csv.gz",
        "Eurostat, ilc_lvho07a (sobrecarga de coste de vivienda por edad, sexo y pobreza)",
        "país (todos los geos del dataset)",
        "Eurostat: reutilización con cita (política de reutilización de Eurostat, https://ec.europa.eu/eurostat/about-us/policies/copyright)",
        "Desgloses: age (TOTAL, Y_LT18, Y_GE65, etc.), sex (F/M/T), rskpovth (A_60, B_60, TOTAL). Sin tenencia (ver ilc_lvho02 en data/raw/v5).",
        "2003 a último año publicado",
    )


if __name__ == "__main__":
    main()
