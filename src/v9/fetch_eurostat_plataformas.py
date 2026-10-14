"""V9-DATOS: Eurostat, alojamiento de corta estancia vía plataformas (familia tour_ce_*). Solo descarga y registro.

Salida: data/raw/v9/eurostat_plataformas/<dataset>.csv.gz en formato largo
(dataset, geo, periodo, indicador, unidad, valor, bandera). Fuente: API SDMX 2.1 de Eurostat (TSV), licencia CC BY 4.0.
Brecha conocida: no hay dataset mensual a NUTS 3 en el catálogo; el mensual llega a NUTS 2 (tour_ce_omn12).
"""
from __future__ import annotations

import csv
import gzip
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from src.v9.comun import RAW9, descargar, registrar, sha256  # noqa: E402

FUENTE = "eurostat_plataformas"
DIR = RAW9 / FUENTE
BASE = "https://ec.europa.eu/eurostat/api/dissemination/sdmx/2.1/data/{ds}?format=TSV"
DATASETS = {
    "tour_ce_omn12": "mensual, NUTS 1/2, por residencia del huésped",
    "tour_ce_omr": "mensual, país, por residencia del huésped",
    "tour_ce_oan3": "anual, NUTS 3",
    "tour_ce_oam": "anual, por modo de alojamiento",
    "tour_ce_oasc": "anual, por tamaño del alojamiento",
}
LICENCIA = "Eurostat: reutilización con cita (CC BY 4.0)"


def leer_tsv_sdmx(ruta: Path, ds: str):
    """Convierte el TSV SDMX de Eurostat (dimensiones separadas por comas, columna final = periodo) a filas largas."""
    with open(ruta, encoding="utf-8") as f:
        cab = f.readline().rstrip("\n").split("\t")
        dims = cab[0].split("\\")[0].split(",")
        periodos = [p.strip() for p in cab[1:]]
        for linea in f:
            partes = linea.rstrip("\n").split("\t")
            if not partes or not partes[0]:
                continue
            clave = dict(zip(dims, partes[0].split(",")))
            geo = clave.pop("geo", "")
            unidad = clave.pop("unit", "")
            indicador = "|".join(f"{k}={v}" for k, v in clave.items())
            for periodo, celda in zip(periodos, partes[1:]):
                tokens = celda.split()
                valor = tokens[0] if tokens and tokens[0] != ":" else ""
                bandera = " ".join(tokens[1:]) if valor else (tokens[0] if tokens else "")
                if valor == "" and not bandera:
                    continue
                yield {"dataset": ds, "geo": geo, "periodo": periodo, "indicador": indicador, "unidad": unidad,
                       "valor": valor, "bandera": bandera}


def _rango(periodos):
    p = sorted(periodos)
    return f"{p[0]}–{p[-1]}" if p else ""


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
        print("OK eurostat_plataformas"); return 0
    tmp = DIR / "original_tsv"
    tmp.mkdir(parents=True, exist_ok=True)
    for ds, desc in DATASETS.items():
        bruto = descargar(BASE.format(ds=ds), tmp / f"{ds}.tsv", timeout=600)
        salida = DIR / f"{ds}.csv.gz"
        filas = 0
        periodos = []
        geos = set()
        with gzip.open(salida, "wt", encoding="utf-8", newline="") as g:
            w = csv.DictWriter(g, fieldnames=["dataset", "geo", "periodo", "indicador", "unidad", "valor", "bandera"])
            w.writeheader()
            for fila in leer_tsv_sdmx(bruto, ds):
                w.writerow(fila); filas += 1
                periodos.append(fila["periodo"]); geos.add(fila["geo"])
        registrar(FUENTE, salida, BASE.format(ds=ds), edicion="SDMX 2.1 TSV (dissemination API)",
                  periodo=_rango(periodos), nivel_territorial=f"geo: {len(geos)} códigos ({desc})",
                  licencia=LICENCIA, redistribuible=True, notas=f"filas={filas}")
        print(ds, filas, _rango(periodos))
    return 0


if __name__ == "__main__":
    sys.exit(main("--verificar" in sys.argv))
