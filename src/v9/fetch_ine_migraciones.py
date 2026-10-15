"""V9-DATOS-COMPLETO (bloque 3, punto 14): flujos migratorios por provincia (INE), con la serie más larga disponible.

- Estadística de Migraciones (EM, 2008-2021): 24379 flujo interprovincial origen×destino (anual); 24385 saldo
  interprovincial por provincia y nacionalidad; 24323 inmigración del extranjero por provincia y nacionalidad;
  24326 emigración al extranjero por provincia y nacionalidad.
- Estadística de Migraciones y Cambios de Residencia (EMCR, 2021-): 69764 saldos por provincia y tipo de saldo;
  69693 inmigración del extranjero por provincia y nacionalidad; 69708 emigración al extranjero por provincia y
  nacionalidad; 69733 inmigración interprovincial por provincia de destino y nacionalidad.
- EVR (1988-2007): no está en la API tempus ni en jaxiT3 (docs/v9/fuentes_fallidas.md); para 2003-2007 el
  componente interno se aproxima con el padrón por nacionalidad (cambio de la población española), marcado.

Se guarda cada tabla tal cual (CSV del INE, «Sexo» = total cuando existe), en gzip determinista. Cruces por código: los
códigos de provincia se extraen de las etiquetas («46 Valencia/València») en el uso, nunca por nombre.
Licencia INE: reutilización con cita.
"""
from __future__ import annotations

import csv
import io
import sys
from pathlib import Path

import requests

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from src.v9.comun import CABECERAS, RAIZ, RAW9, abrir_gz_texto, registrar, sha256  # noqa: E402

FUENTE = "ine_migraciones"
DIR = RAW9 / FUENTE
URL = "https://www.ine.es/jaxiT3/files/t/es/csv_bdsc/{t}.csv?nocab=1"
LICENCIA = "INE: reutilización con cita (Ley 37/2007)"
TABLAS = {
    24379: ("EM", "flujo interprovincial origen-destino, anual"),
    24385: ("EM", "saldo interprovincial por provincia y nacionalidad"),
    24323: ("EM", "inmigración del extranjero por provincia y nacionalidad"),
    24326: ("EM", "emigración al extranjero por provincia y nacionalidad"),
    69764: ("EMCR", "saldos por provincia, edad, nacionalidad y tipo de saldo"),
    69693: ("EMCR", "inmigración del extranjero por provincia y nacionalidad"),
    69708: ("EMCR", "emigración al extranjero por provincia y nacionalidad"),
    69733: ("EMCR", "inmigración interprovincial por provincia de destino y nacionalidad"),
}
TOTAL_SEXO = {"Total", "Ambos sexos"}


def main(verificar: bool = False) -> int:
    DIR.mkdir(parents=True, exist_ok=True)
    if verificar:
        with open(DIR / "_manifest.csv", encoding="utf-8") as f:
            for fila in csv.DictReader(f):
                ruta = RAIZ / fila["fichero"]
                if not ruta.exists() or sha256(ruta) != fila["sha256"]:
                    print("FALLO", fila["fichero"]); return 1
        print("OK ine_migraciones"); return 0
    for t, (op, desc) in TABLAS.items():
        r = None
        for _ in range(3):
            try:
                r = requests.get(URL.format(t=t), headers=CABECERAS, timeout=600)
                r.raise_for_status()
                break
            except Exception:  # noqa: BLE001
                r = None
        if r is None:
            print("FALLO", t); continue
        lector = csv.reader(io.StringIO(r.content.decode("utf-8-sig", "replace")), delimiter=";")
        cab = next(lector)
        i_sexo = cab.index("Sexo") if "Sexo" in cab else None
        i_edad = next((i for i, c in enumerate(cab) if c.lower().startswith("edad")), None)
        filas = [f for f in lector if len(f) == len(cab) and (i_sexo is None or f[i_sexo] in TOTAL_SEXO)]
        if i_edad is not None:
            filas = [f for f in filas if f[i_edad].startswith("Todas") or f[i_edad] == "Total"]
        ruta = DIR / f"ine_{op.lower()}_{t}.csv.gz"
        with abrir_gz_texto(ruta) as g:
            w = csv.writer(g)
            w.writerow(cab)
            w.writerows(filas)
        i_per = cab.index("Periodo")
        per = sorted({f[i_per] for f in filas})
        registrar(FUENTE, ruta, URL.format(t=t), edicion=f"INE {op}, tabla {t} (jaxiT3)", periodo=f"{per[0]}–{per[-1]}",
                  nivel_territorial="provincia (código en la etiqueta)", licencia=LICENCIA, redistribuible=True,
                  notas=f"{desc}; sexo=total; edad=total; filas={len(filas)}")
        print(t, len(filas), per[0], per[-1])
    return 0


if __name__ == "__main__":
    sys.exit(main("--verificar" in sys.argv))
