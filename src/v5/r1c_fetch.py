"""R1c descargas (con red, fuera de make): python3 src/v5/r1c_fetch.py
Tablas INE (Tempus) a data/raw/v5/:
  65354 EPA ocupados por sector economico y provincia
  66088 EPA ocupados por sector economico, sexo y CCAA
  6030  ETCL coste laboral por trabajador por sectores (nacional)
  6061  ETCL coste laboral por trabajador, CCAA, sectores
  59531 Censo 2021: viviendas por consumo electrico, incl. vacias y de uso esporadico (BK-034)
"""
import csv
import json
import urllib.request
from pathlib import Path

DEST = Path(__file__).resolve().parents[2] / "data" / "raw" / "v5"
API = "https://servicios.ine.es/wstempus/js/ES/DATOS_TABLA/{t}?nult={n}"
TABLAS = {65354: 400, 66088: 400, 6030: 100, 6061: 100, 59531: 1}


def main():
    DEST.mkdir(parents=True, exist_ok=True)
    for t, n in TABLAS.items():
        if len(__import__('sys').argv) > 1 and str(t) not in __import__('sys').argv[1:]:
            continue
        url = API.format(t=t, n=n)
        with urllib.request.urlopen(url, timeout=180) as r:
            d = json.load(r)
        with open(DEST / f"ine_r1c_t{t}.csv", "w", newline="") as f:
            w = csv.writer(f)
            w.writerow(["tabla", "serie", "nombre", "fecha", "periodo", "valor", "url"])
            for s in d:
                for p in s["Data"]:
                    w.writerow([t, s.get("COD", ""), s["Nombre"], p.get("Fecha", ""), f'{p.get("Anyo", "")}-{p.get("FK_Periodo", "")}', p["Valor"], url])
        print(t, len(d))


if __name__ == "__main__":
    main()
