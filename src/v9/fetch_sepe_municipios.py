"""V9-DATOS-COMPLETO (bloque 5): paro registrado y contratos registrados por municipio (SEPE, datos abiertos),
mensual desde 2006 (primer año publicado). Se guarda el total por municipio y mes (código INE de 5 dígitos de la
columna «Codigo Municipio»: cruce por código). Los valores «<5» (secreto estadístico) quedan vacíos.
Licencia: SEPE, datos abiertos (reutilización con cita, Ley 37/2007) → se versiona. Marca posterior_prereg desde 2026-07.
"""
from __future__ import annotations

import csv
import datetime as dt
import io
import sys
from pathlib import Path

import requests

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from src.v9.comun import CABECERAS, INICIO_POSTERIOR, RAIZ, RAW9, abrir_gz_texto, registrar, sha256  # noqa: E402

FUENTE = "sepe_municipios"
DIR = RAW9 / FUENTE
URL = "https://sede.sepe.gob.es/es/portaltrabaja/resources/sede/datos_abiertos/datos/{tipo}_por_municipios_{y}_csv.csv"
TIPOS = {"Paro": "paro_registrado", "Contratos": "contratos"}
LICENCIA = "SEPE, datos abiertos: reutilización con cita (Ley 37/2007)"


def _bajar(url: str) -> str | None:
    for _ in range(3):
        try:
            r = requests.get(url, headers=CABECERAS, timeout=300)
            if r.status_code == 404:
                return None
            r.raise_for_status()
            return r.content.decode("latin-1")
        except Exception:  # noqa: BLE001
            continue
    return None


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
        print("OK sepe_municipios"); return 0
    for tipo, var in TIPOS.items():
        filas, anios, fallos = [], [], []
        for y in range(2006, dt.date.today().year + 1):
            txt = _bajar(URL.format(tipo=tipo, y=y))
            if txt is None:
                fallos.append(y); continue
            lineas = txt.splitlines()
            i = next(k for k, l in enumerate(lineas) if l.lower().startswith("código mes") or l.lower().startswith("codigo mes"))
            lector = csv.reader(io.StringIO("\n".join(lineas[i + 1:])), delimiter=";")
            for f in lector:
                if len(f) < 9 or not f[0].strip().isdigit():
                    continue
                cod = f[6].strip().zfill(5)
                tot = f[8].strip().replace(".", "")
                mes = f[0].strip()
                post = dt.date(int(mes[:4]), int(mes[4:6]), 1) >= INICIO_POSTERIOR
                filas.append([mes, cod, tot if tot.isdigit() else "", post])
            anios.append(y)
        filas.sort()
        ruta = DIR / f"{var}_municipio_mensual.csv.gz"
        with abrir_gz_texto(ruta) as g:
            w = csv.writer(g)
            w.writerow(["mes", "cod_municipio", var, "posterior_prereg"])
            w.writerows(filas)
        registrar(FUENTE, ruta, URL.format(tipo=tipo, y="<año>"), edicion="SEPE datos abiertos (consulta 2026-10-15)",
                  periodo=f"{filas[0][0]}-{filas[-1][0]}", nivel_territorial="municipio (código INE)", licencia=LICENCIA,
                  redistribuible=True, notas=f"años={anios[0]}-{anios[-1]}; sin fichero: {fallos or 'ninguno'}; «<5» vacío")
        print(var, len(filas), anios[0], anios[-1], fallos)
    return 0


if __name__ == "__main__":
    sys.exit(main("--verificar" in sys.argv))
