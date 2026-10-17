"""Resumen de control de las tablas ADRH descargadas (solo lectura de _grandes/adrh).

Cuenta series, puntos, valores secretos o nulos y periodos por tabla, y escribe un resumen JSON
en data/raw/v16/renta_parque/_grandes/adrh/resumen_control.json (sin datos crudos).
Ejecutar: python3 -I resumen_adrh.py
"""
import gzip
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import adq_utils as au  # noqa: E402

CARPETA = os.path.join(au.FAMILIA_DIR, "_grandes", "adrh")


def main():
    tot = {"tablas": 0, "series": 0, "puntos": 0, "secretos": 0, "nulos": 0}
    anios = {}
    for f in sorted(os.listdir(CARPETA)):
        if not f.endswith(".json.gz") or f == "tablas_adrh.json.gz":
            continue
        with gzip.open(os.path.join(CARPETA, f), "rb") as fh:
            datos = json.loads(fh.read().decode("utf-8"))
        tot["tablas"] += 1
        tot["series"] += len(datos)
        for s in datos:
            for x in s.get("Data", []):
                tot["puntos"] += 1
                tot["secretos"] += 1 if x.get("Secreto") else 0
                tot["nulos"] += 1 if x.get("Valor") is None else 0
                anios[x.get("Anyo")] = anios.get(x.get("Anyo"), 0) + 1
    resumen = {"fecha_control": au.dt_hoy() if hasattr(au, "dt_hoy") else "2026-10-17",
               "totales": tot, "puntos_por_anio": {str(k): v for k, v in sorted(anios.items())}}
    with open(os.path.join(CARPETA, "resumen_control.json"), "w", encoding="utf-8") as f:
        json.dump(resumen, f, ensure_ascii=False, indent=1)
    print(json.dumps(resumen, ensure_ascii=False))


if __name__ == "__main__":
    main()
