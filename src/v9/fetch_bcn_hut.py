"""V9-DATOS-COMPLETO (bloque 1): habitatges d'ús turístic (HUT) con licencia en Barcelona, por barrio.

Fuente: Ajuntament de Barcelona, Open Data BCN, conjunto «habitatges-us-turistic» (CC BY 4.0), recurso vigente
b32fa7f6-… leído por la API CKAN datastore_search. Los cortes trimestrales en zip (2018T2-2026T3) quedan detrás de
una prueba anti-bot (/challenge) y no se pueden descargar por script (docs/v9/fuentes_fallidas.md).
El año de la licencia se toma del número de expediente («01-2009-0354» → 2009); no hay fecha de alta. Barcelona no
concede licencias nuevas de HUT desde 2014 (PEUAT), por lo que el stock vigente aproxima el de 2019 con la cautela de
las bajas (no observadas). Se guarda solo el agregado barrio × año de expediente (n y plazas); cruce por CODI_BARRI
(código municipal de barrio, 73 barrios) y municipio INE 08019.
"""
from __future__ import annotations

import csv
import re
import sys
from collections import defaultdict
from pathlib import Path

import requests

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from src.v9.comun import CABECERAS, RAIZ, RAW9, abrir_gz_texto, registrar, sha256  # noqa: E402

FUENTE = "bcn_hut"
DIR = RAW9 / FUENTE
RECURSO = "b32fa7f6-d464-403b-8a02-0292a64883bf"
API = "https://opendata-ajuntament.barcelona.cat/data/api/action/datastore_search"
SALIDA = DIR / "bcn_hut_barrio_anio_expediente.csv.gz"


def main(verificar: bool = False) -> int:
    DIR.mkdir(parents=True, exist_ok=True)
    if verificar:
        man = DIR / "_manifest.csv"
        if not man.exists():
            return 1
        with open(man, encoding="utf-8") as f:
            for fila in csv.DictReader(f):
                if not (RAIZ / fila["fichero"]).exists() or sha256(RAIZ / fila["fichero"]) != fila["sha256"]:
                    print("FALLO", fila["fichero"]); return 1
        print("OK bcn_hut"); return 0
    regs, off = [], 0
    while True:
        r = requests.get(API, params={"resource_id": RECURSO, "limit": 5000, "offset": off}, headers=CABECERAS, timeout=300)
        r.raise_for_status()
        lote = r.json()["result"]["records"]
        regs += lote
        if len(lote) < 5000:
            break
        off += 5000
    agg = defaultdict(lambda: [0, 0])
    nombres = {}
    for x in regs:
        m = re.match(r"^\d{2}-(\d{4})-", x.get("N_EXPEDIENT") or "")
        anio = m.group(1) if m else ""
        b = (x.get("CODI_BARRI") or "").zfill(2)
        nombres[b] = x.get("NOM_BARRI") or ""
        a = agg[(b, anio)]
        a[0] += 1
        a[1] += int(x["NUMERO_PLACES"]) if (x.get("NUMERO_PLACES") or "").isdigit() else 0
    with abrir_gz_texto(SALIDA) as g:
        w = csv.writer(g)
        w.writerow(["cod_municipio", "codi_barri", "nom_barri", "anio_expediente", "n_hut", "places"])
        for (b, anio), (n, p) in sorted(agg.items()):
            w.writerow(["08019", b, nombres[b], anio, n, p])
    registrar(FUENTE, SALIDA, f"{API}?resource_id={RECURSO}", edicion="Open Data BCN, registro vigente (consulta 2026-10-15)",
              periodo="licencias vigentes; año de expediente", nivel_territorial="barrio de Barcelona (CODI_BARRI)",
              licencia="CC BY 4.0 (Ajuntament de Barcelona)", redistribuible=True,
              notas=f"registros={len(regs)}; barrios={len(nombres)}; sin año de expediente={sum(v[0] for k, v in agg.items() if not k[1])}")
    print(len(regs), len(nombres))
    return 0


if __name__ == "__main__":
    sys.exit(main("--verificar" in sys.argv))
