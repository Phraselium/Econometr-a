"""B1 descargas (con red, fuera de make): python3 src/v5/b1_fetch.py
Tablas INE (Tempus) a data/raw/v5/ (filtradas a lo que usa b1_run.py):
  54562 Proyeccion de Hogares (PROH): hogares por CCAA/tamano, 2026-2041 (nult=20)
  36726 Proyecciones de Poblacion (PROP, edicion 2024): poblacion provincial por edad, ambos sexos, proyeccion a corto plazo
  67235 Tablas de mortalidad por provincia (2024): riesgo de muerte por edad, ambos sexos, 65+
  69764 EM/EMCR: saldos migratorios por provincia, todas las edades, total (interior = interprovincial)
"""
import csv
import json
import re
import urllib.request
from pathlib import Path

DEST = Path(__file__).resolve().parents[2] / "data" / "raw" / "v5"
API = "https://servicios.ine.es/wstempus/js/ES/DATOS_TABLA/{t}?nult={n}"


def get(t, n):
    with urllib.request.urlopen(API.format(t=t, n=n), timeout=300) as r:
        return json.load(r)


def vuelca(nombre, t, n, filtro):
    d = get(t, n)
    with open(DEST / nombre, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["tabla", "nombre", "anyo", "fecha", "valor", "url"])
        k = 0
        for s in d:
            if not filtro(s["Nombre"]):
                continue
            for p in s["Data"]:
                if p.get("Valor") is None:
                    continue
                w.writerow([t, s["Nombre"], p.get("Anyo", ""), p.get("Fecha", ""), p["Valor"], API.format(t=t, n=n)])
                k += 1
    print(nombre, len(d), k)


def edad_min(nom, minimo):
    m = re.search(r"(\d+) años?\.?\s*$", nom.strip())
    return bool(m) and int(m.group(1)) >= minimo


def main():
    DEST.mkdir(parents=True, exist_ok=True)
    vuelca("ine_b1_t54562_proy_hogares.csv", 54562, 20, lambda n: True)
    vuelca("ine_b1_t36726_proy_poblacion_prov.csv", 36726, 17,
           lambda n: n.startswith("Total.") and ("Todas las edades" in n or edad_min(n, 65)))
    vuelca("ine_b1_t67235_mortalidad_prov.csv", 67235, 1,
           lambda n: ". Total. " in n and "Riesgo de muerte" in n and edad_min(n.split(". Riesgo")[0], 65))
    vuelca("ine_b1_t69764_saldos_prov.csv", 69764, 10,
           lambda n: "Todas las edades. Total. Total. Saldo" in n)


if __name__ == "__main__":
    main()
