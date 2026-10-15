"""V11-DATOS, segunda pasada (punto 18): Universitat de València, Servei d'Anàlisi i Planificació (SAP), «UV en xifres:
Estudiants» (https://www.uv.es/sap/docs/xifres/estudiants.html): tablas HTML del último curso publicado (matrícula por
tipo de estudio y sexo; intercambio ERASMUS por país, etc.). Los cursos anteriores solo están en los «Recull de dades
estadístiques» en PDF (https://www.uv.es/sap/docs/reculls/recullAABB.pdf; no se extraen en esta tarea).
La web no declara una licencia abierta: las tablas NO se versionan (.gitignore) y se regeneran con `make datos_v11`.
UPV: no publica ficheros de matrícula descargables en upv.es; la estadística del Ministerio de Universidades (SIIU)
y datos.upv.es están bloqueados por la red del entorno (docs/v11/fuentes_fallidas.md).
"""
from __future__ import annotations

import io
import sys
from pathlib import Path

import pandas as pd
import requests

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from src.v11.comun import CABECERAS, RAW11, registrar, verificar_manifiesto  # noqa: E402

FUENTE = "uv_matricula"
DIR = RAW11 / FUENTE
URL = "https://www.uv.es/sap/docs/xifres/estudiants.html"
LIC = "Universitat de València: sin licencia abierta declarada (no redistribuible)"


def main(verificar: bool = False) -> int:
    DIR.mkdir(parents=True, exist_ok=True)
    if verificar:
        return verificar_manifiesto(FUENTE)
    h = requests.get(URL, headers=CABECERAS, timeout=120).content.decode("utf-8", "replace")
    tablas = pd.read_html(io.StringIO(h), thousands=".", decimal=",")
    for i, t in enumerate(tablas, 1):
        r = DIR / f"uv_estudiants_t{i}.csv"
        t.to_csv(r, index=False)
        registrar(FUENTE, r, URL, edicion="SAP UV, «UV en xifres: Estudiants» (actualizado 19-01-2026)", periodo="curso 2024/25",
                  nivel_territorial="Universitat de València", licencia=LIC, redistribuible=False,
                  notas=f"tabla {i} de la página; columnas={list(t.columns)[:6]}")
        print(i, t.shape)
    return 0


if __name__ == "__main__":
    sys.exit(main("--verificar" in sys.argv))
