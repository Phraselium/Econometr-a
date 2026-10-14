"""V9-DATOS: BCE (ECB Data Portal, dataflow MIR). Tipos de nuevas operaciones de préstamos a hogares para vivienda
por país de la zona euro y periodo de fijación inicial. Solo descarga y registro (sin estimaciones).

Salida: data/raw/v9/bce_hipotecas/bce_mir_vivienda_zona_euro.csv.gz (CSV largo, con el título oficial de cada serie).
Brecha: volúmenes de nuevas operaciones no localizados con las claves probadas (ver notas del informe).
"""
from __future__ import annotations

import csv
import gzip
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from src.v9.comun import RAW9, descargar, registrar, sha256  # noqa: E402

FUENTE = "bce_hipotecas"
DIR = RAW9 / FUENTE
SALIDA = DIR / "bce_mir_vivienda_zona_euro.csv.gz"
API = "https://data-api.ecb.europa.eu/service/data/MIR/M.{pais}.B.A2C.{mat}.R.A.2250.EUR.N?format=csvdata&startPeriod=2003-01"
# AM = coste de financiación (TAE acordada); F = variable y fijación hasta 1 año; I, K, O, P = fijación >1-5, >1, >5-10, >10
MATURIDADES = "F+I+K+O+P+AM"
PAISES = ["AT", "BE", "BG", "HR", "CY", "EE", "FI", "FR", "DE", "GR", "IE", "IT", "LV", "LT", "LU", "MT", "NL", "PT",
          "SK", "SI", "ES"]
LICENCIA = "BCE: reutilización con cita (ECB Data Portal)"
COLS = ["pais", "fijacion_codigo", "periodo", "valor", "estado_obs", "titulo", "clave"]


def main(verificar: bool = False) -> int:
    DIR.mkdir(parents=True, exist_ok=True)
    if verificar:
        man = DIR / "_manifest.csv"
        if not man.exists():
            print("falta _manifest.csv"); return 1
        with open(man, encoding="utf-8") as f:
            for fila in csv.DictReader(f):
                ruta = RAW9.parent.parent / fila["fichero"]
                if not ruta.exists() or sha256(ruta) != fila["sha256"]:
                    print("FALLO", fila["fichero"]); return 1
        print("OK bce_hipotecas"); return 0
    filas, fallos = [], []
    tmp = DIR / "original_csv"
    for pais in PAISES:
        url = API.format(pais=pais, mat=MATURIDADES)
        try:
            bruto = descargar(url, tmp / f"{pais}.csv", timeout=300)
        except RuntimeError as e:
            fallos.append(f"{pais}: {e}")
            continue
        with open(bruto, encoding="utf-8") as f:
            for x in csv.DictReader(f):
                filas.append({"pais": x["REF_AREA"], "fijacion_codigo": x["MATURITY_NOT_IRATE"],
                              "periodo": x["TIME_PERIOD"], "valor": x["OBS_VALUE"], "estado_obs": x["OBS_STATUS"],
                              "titulo": x["TITLE"].strip(), "clave": x["KEY"]})
    with gzip.open(SALIDA, "wt", encoding="utf-8", newline="") as g:
        w = csv.DictWriter(g, fieldnames=COLS)
        w.writeheader(); w.writerows(filas)
    periodos = sorted({r["periodo"] for r in filas})
    paises_ok = sorted({r["pais"] for r in filas})
    registrar(FUENTE, SALIDA, API.format(pais="{pais}", mat=MATURIDADES), edicion="ECB Data Portal (MIR, API SDMX)",
              periodo=f"{periodos[0]}–{periodos[-1]}" if periodos else "", nivel_territorial="país (zona euro)",
              licencia=LICENCIA, redistribuible=True,
              notas=f"filas={len(filas)}; países={len(paises_ok)}; fallos={'; '.join(fallos) or 'ninguno'}")
    print("filas", len(filas), "paises", len(paises_ok), "fallos", fallos)
    return 0


if __name__ == "__main__":
    sys.exit(main("--verificar" in sys.argv))
