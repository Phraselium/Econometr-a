"""V9-DATOS-COMPLETO (bloque 4): correspondencia sección censal ↔ código postal desde el Callejero del Censo Electoral
del INE (fichero nacional de tramos, julio de 2025; referencia 2025-06-30).

Cada tramo de vía del fichero TRAM lleva el código de sección (provincia 1-2, municipio 3-5, distrito 6-7, sección
8-10) y el código postal (posiciones 43-47), con los números inicial y final del tramo (49-52 y 54-57). Se agrega a
(sección, código postal) con el número de tramos y una aproximación al número de portales ((final-inicial)/2+1). Es la
tabla con la que D3 reparte variables por sección (VUT del INE, censo, ADRH) entre códigos postales: cruce por código.
Licencia INE: reutilización con cita. El zip (48 MB) no se versiona: se guarda solo la tabla agregada.
"""
from __future__ import annotations

import csv
import io
import sys
import zipfile
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from src.v9.comun import RAIZ, RAW9, abrir_gz_texto, descargar, registrar, sha256  # noqa: E402

FUENTE = "ine_callejero"
DIR = RAW9 / FUENTE
URL = "https://www.ine.es/prodyser/callejero/caj_esp/caj_esp_072025.zip"
SALIDA = DIR / "seccion_cp_2025.csv.gz"


def _num(s: str) -> int | None:
    s = s.strip()
    return int(s) if s.isdigit() else None


def main(verificar: bool = False) -> int:
    DIR.mkdir(parents=True, exist_ok=True)
    if verificar:
        with open(DIR / "_manifest.csv", encoding="utf-8") as f:
            for fila in csv.DictReader(f):
                if sha256(RAIZ / fila["fichero"]) != fila["sha256"]:
                    print("FALLO", fila["fichero"]); return 1
        print("OK ine_callejero"); return 0
    zp = descargar(URL, DIR / "original" / "caj_esp_072025.zip", timeout=900)
    agg: dict[tuple[str, str], list[int]] = defaultdict(lambda: [0, 0])
    with zipfile.ZipFile(zp) as z:
        nombre = next(n for n in z.namelist() if "/TRAM." in n)
        with z.open(nombre) as f:
            for linea in io.TextIOWrapper(f, encoding="latin-1"):
                secc, cp = linea[0:10], linea[42:47]
                if not (secc.isdigit() and cp.isdigit()):
                    continue
                ein, esn = _num(linea[48:52]), _num(linea[53:57])
                portales = (esn - ein) // 2 + 1 if ein is not None and esn is not None and esn >= ein else 1
                a = agg[(secc, cp)]
                a[0] += 1
                a[1] += portales
    with abrir_gz_texto(SALIDA) as g:
        w = csv.writer(g)
        w.writerow(["seccion", "cod_municipio", "cp", "n_tramos", "portales_aprox"])
        for (s, cp), (n, p) in sorted(agg.items()):
            w.writerow([s, s[:5], cp, n, p])
    registrar(FUENTE, SALIDA, URL, edicion="Callejero del Censo Electoral, julio 2025 (ref. 2025-06-30)", periodo="2025-06-30",
              nivel_territorial="sección censal × código postal", licencia="INE: reutilización con cita", redistribuible=True,
              notas=f"pares sección-CP={len(agg)}; secciones={len({k[0] for k in agg})}; CP={len({k[1] for k in agg})}")
    print(len(agg))
    return 0


if __name__ == "__main__":
    sys.exit(main("--verificar" in sys.argv))
