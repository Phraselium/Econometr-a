"""Fuente 1 (demanda_internacional): sorpresas de política monetaria del BCE.

- EA-MPD (Altavilla, Brugnolini, Gürkaynak, Motto y Ragusa, 2019), libro oficial del BCE.
- Choques de Jarociński-Karadi (2020), actualización de los autores (repositorio jkshocks_update_ecb).
- Choques de Jarociński-Karadi, paquete zip publicado en la web de los autores (shocks_median.zip).

Caché: no vuelve a descargar si el fichero existe, salvo FORCE=1.
Uso: python3 -I bce_sorpresas.py
"""
import csv
import hashlib
import os
import sys
import zipfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from manifiesto import FAMILIA_DIR, ahora_utc, descargar, registrar, relativa, sha256_fichero  # noqa: E402

DESTINO = os.path.join(FAMILIA_DIR, "bce_sorpresas")
FORCE = os.environ.get("FORCE") == "1"

FUENTES = [
    {
        "fichero": "Dataset_EA-MPD.xlsx",
        "url": "https://www.ecb.europa.eu/pub/pdf/annex/Dataset_EA-MPD.xlsx",
        "fuente": "BCE, EA-MPD (Altavilla et al. 2019)",
        "nivel": "euro_area",
        "licencia": "Copyright BCE (https://www.ecb.europa.eu/services/using-our-site/disclaimer/html/index.en.html): el libro es anexo de un documento de trabajo del BCE; la página no concede licencia expresa de redistribución del anexo (solo aviso de copyright). Sin licencia explícita para el libro.",
        "redistribuible": "dudoso",
        "notas": "Ventanas de evento de decisiones del Consejo de Gobierno desde 1999. Libro de Excel (anexo del WP 2281 del BCE). Fecha de modificación del libro desde docProps/core.xml (2025-11-13). Va a _terceros por licencia no explícita; los choques derivados se publican bajo CC BY 4.0 (JK).",
    },
    {
        "fichero": "jk_shocks_ecb_mpd_me_d.csv",
        "url": "https://raw.githubusercontent.com/marekjarocinski/jkshocks_update_ecb/master/shocks_ecb_mpd_me_d.csv",
        "fuente": "Jarociński-Karadi (2020), choques BCE actualizados (diarios por reunión)",
        "nivel": "reunion_CG",
        "licencia": "CC BY 4.0 (datos) y BSD-3 (código); https://github.com/marekjarocinski/jkshocks_update_ecb (README, sección Licensing)",
        "redistribuible": "sí",
        "notas": "Columnas: pc1 (factor de sorpresa, OIS 1M-1Y), STOXX50, MP_pm/CBI_pm (sign restrictions simples), MP_median/CBI_median (rotación mediana). Se construye sobre Dataset_EA-MPD.xlsx.",
    },
    {
        "fichero": "jk_shocks_ecb_mpd_me_m.csv",
        "url": "https://raw.githubusercontent.com/marekjarocinski/jkshocks_update_ecb/master/shocks_ecb_mpd_me_m.csv",
        "fuente": "Jarociński-Karadi (2020), choques BCE actualizados (mensuales)",
        "nivel": "mensual_euro_area",
        "licencia": "CC BY 4.0 (datos) y BSD-3 (código); https://github.com/marekjarocinski/jkshocks_update_ecb (README, sección Licensing)",
        "redistribuible": "sí",
        "notas": "Agregado mensual; cero si no hay choques en el mes. Misma descomposición que la versión diaria.",
    },
    {
        "fichero": "jk_shocks_median.zip",
        "url": "https://marekjarocinski.github.io/jkshocks/shocks_median.zip",
        "fuente": "Jarociński-Karadi, paquete publicado en la web de los autores",
        "nivel": "reunion_CG",
        "licencia": "Sin licencia explícita en la página; ver https://marekjarocinski.github.io/jkshocks/jkshocks.html; uso académico con cita del artículo (DOI 10.1257/mac.20180090)",
        "redistribuible": "dudoso",
        "notas": "Versión de la web («most updated ECB shocks»). Se usa solo para contrastar con el repositorio. Va a _terceros por la regla del coordinador (licencia no explícita).",
    },
]


def contar_filas_csv(ruta):
    with open(ruta, newline="", encoding="utf-8") as f:
        return sum(1 for _ in csv.reader(f)) - 1


def info_xlsx(ruta):
    with zipfile.ZipFile(ruta) as z:
        nombres = z.namelist()
        hojas = [n for n in nombres if n.startswith("xl/worksheets/sheet")]
        fecha = ""
        if "docProps/core.xml" in nombres:
            txt = z.read("docProps/core.xml").decode("utf-8", "replace")
            for etiqueta in ("dcterms:modified", "dcterms:created"):
                if etiqueta in txt:
                    fecha = txt.split(etiqueta + ' xsi:type="dcterms:W3CDTF">')[1].split("<")[0]
                    break
    return len(hojas), fecha


def main():
    for f in FUENTES:
        # Regla del coordinador: redistribuible «no» o «dudoso» va a _terceros (no versionada).
        carpeta = DESTINO if f["redistribuible"] == "sí" else os.path.join(DESTINO, "..", "_terceros", "bce_sorpresas")
        carpeta = os.path.normpath(carpeta)
        os.makedirs(carpeta, exist_ok=True)
        ruta = os.path.join(carpeta, f["fichero"])
        if os.path.exists(ruta) and not FORCE:
            print("caché:", relativa(ruta))
        else:
            descargar(f["url"], ruta)
            print("descargado:", relativa(ruta))
        sha = sha256_fichero(ruta)
        edicion, periodo, n_filas = "", "", ""
        if f["fichero"].endswith(".csv"):
            n_filas = contar_filas_csv(ruta)
            with open(ruta, newline="", encoding="utf-8") as h:
                primera = next(csv.reader(h))
                cab = primera
            filas = []
            with open(ruta, newline="", encoding="utf-8") as h:
                lector = csv.reader(h)
                next(lector)
                for fila in lector:
                    filas.append(fila[0])
            periodo = f"{filas[0]} a {filas[-1]}" if filas else ""
            edicion = "actualización del repositorio (README: Updated shocks)"
            notas_extra = f" Columnas: {','.join(cab)}."
        elif f["fichero"].endswith(".xlsx"):
            n_hojas, fecha_mod = info_xlsx(ruta)
            edicion = f"libro con {n_hojas} hojas; modificado {fecha_mod or 'NO CONSTA'}"
            periodo = "desde 1999 (ver notas)"
            notas_extra = ""
        else:
            with zipfile.ZipFile(ruta) as z:
                n_filas = len(z.namelist())
                edicion = "zip: " + ", ".join(z.namelist()[:6])
            periodo = "NO CONSTA (ver contenido del zip)"
            notas_extra = ""
        registrar({
            "fuente": f["fuente"],
            "fichero": relativa(ruta),
            "url": f["url"],
            "fecha_descarga": ahora_utc(),
            "edicion": edicion,
            "periodo": periodo,
            "nivel_territorial": f["nivel"],
            "n_filas": n_filas,
            "sha256": sha,
            "licencia": f["licencia"],
            "redistribuible": f["redistribuible"],
            "notas": f["notas"] + notas_extra,
        })
        print("sha256", f["fichero"], sha)


if __name__ == "__main__":
    main()
