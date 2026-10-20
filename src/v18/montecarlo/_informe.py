"""V18 · Redacción común de informe.md de cada herramienta validada por Monte Carlo."""
from __future__ import annotations

import os

for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS"):   # BLAS de un hilo: antes de importar numpy
    os.environ.setdefault(_v, "1")

import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from src.v18.montecarlo._comun import md_tabla  # noqa: E402

ALCANCE_TERRITORIAL = "sin lectura de datos"

CRITERIO = ("Criterio del encargo: APTO si el tamaño al 5 % está en [0,03; 0,08] y la cobertura al 95 % (bajo el nulo y bajo la "
            "alternativa) en [0,92; 0,97], con R >= 2.000 (o >= 1.000 si se declara). Bandas de la adenda 1.12: apta (tamaño [0,04; 0,06], "
            "cobertura [0,93; 0,97], R >= 2.000); con valor crítico corregido (tamaño [0,02; 0,04) o (0,06; 0,15]); no fiable "
            "(tamaño > 0,15 o < 0,02). SEED = 20261010. Resultados simulados: ningún dato real de resultado ni muestra sellada.")


def construir(titulo: str, dgp: str, tabla: pd.DataFrame, veredicto: str, condicion: str, notas: list[str], v16: str,
              columnas: list[str] | None = None) -> str:
    cols = columnas or [c for c in ("escenario", "variante", "R", "tamano_5pct", "cobertura_nulo", "cobertura_alt", "potencia", "sesgo",
                                    "rmse", "veredicto", "banda_112") if c in tabla.columns]
    partes = [f"# V18 · Monte Carlo · {titulo}", "", f"**Veredicto: {veredicto}.**" + (f" Condición en que falla: {condicion}." if condicion else ""),
              "", "## Proceso generador (declarado antes de simular)", "", dgp.strip(), "", "## Qué falló en V16 y qué se hace distinto", "", v16.strip(),
              "", "## Criterio", "", CRITERIO, "", "## Resultados", "", md_tabla(tabla[cols]), ""]
    if notas:
        partes += ["## Notas", ""] + [f"- {n}" for n in notas] + [""]
    return "\n".join(partes)
