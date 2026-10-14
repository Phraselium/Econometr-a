"""V9-DATOS · INE, microdatos anonimizados de la EPA (2018T1-último) y de la ECV transversal (2018-último).

Se descargan los ZIP tal como los publica el INE (con su diseño de registro) a data/raw/v9/ine_microdatos/{epa,ecv}/. No se
convierten ni se abren: se usarán en v9 bajo su propio pre-registro. Condiciones: los ficheros de microdatos anonimizados
del INE son de descarga libre y reutilización con cita (aviso legal del INE). Por tamaño (>50 MB en total) no se
versionan: quedan en .gitignore con su sha256 y este script los descarga (`make datos_v9`).
Uso: python3 src/v9/fetch_ine_microdatos.py [--verificar]
"""
from __future__ import annotations

import csv
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import comun  # noqa: E402

FUENTE = "ine_microdatos"
DIR = comun.RAW9 / FUENTE
BASE = "https://www.ine.es/ftp/microdatos/"
EPA = [f"epa/datos_{t}t{a:02d}.zip" for a in range(18, 27) for t in range(1, 5) if (a, t) <= (26, 2)] + ["epa/dr_EPA_2021.xlsx", "epa/dr_EPA_2026.xlsx"]
ECV = [f"ecv/ecv_b2013/datos_{a}.zip" for a in range(2018, 2026)]
LIC = "INE: microdatos anonimizados, descarga libre y reutilización con cita (aviso legal del INE)"


def verificar() -> int:
    man = DIR / "_manifest.csv"
    if not man.exists():
        return 1
    with open(man, encoding="utf-8") as f:
        filas = list(csv.DictReader(f))
    return 0 if len(filas) == len(EPA) + len(ECV) and all(
        (comun.RAIZ / r["fichero"]).exists() and comun.sha256(comun.RAIZ / r["fichero"]) == r["sha256"] for r in filas) else 1


def main(verificar: bool = False) -> int:
    if verificar:
        return globals()["verificar"]()
    for rel in EPA + ECV:
        op = rel.split("/")[0]
        dest = DIR / op / Path(rel).name
        comun.descargar(BASE + rel, dest)
        periodo = Path(rel).stem.replace("datos_", "")
        comun.registrar(FUENTE, dest, BASE + rel, f"{op.upper()} {periodo}", periodo, "microdatos (individuos y hogares)", LIC, True,
                        "ZIP original del INE; no versionado por tamaño")
    return 0


if __name__ == "__main__":
    sys.exit(main("--verificar" in sys.argv))
