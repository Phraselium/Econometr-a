"""V14 · Series de terceros no redistribuibles (Notariado, Registradores, AEAT, CGPJ) en tablas propias de output/.

- `columnas_terceros(cabecera)`: columnas cuyo nombre contiene, como palabra (separada por «_» o espacios), notariado,
  registradores, cgn, cgpj o aeat. «p_hipotesis_preregistrada» o «especificaciones_registradas» no cuentan.
- `REVISADAS_SIN_SERIES`: tablas revisadas a mano cuyas columnas con ese nombre son resultados propios, no series de la
  fuente. Por ejemplo, la cuota de R² de Shapley de un modelo con el precio de Registradores.
- `redactar(origen, destino)`: copia la tabla sin esas columnas. Así el árbol público y el depósito conservan cada ruta
  publicada (enlaces del verificador, del anexo y de consulta/) sin ninguna serie de esas fuentes (D5 y D4).
- `REQUIEREN_TERCEROS`: ficheros de datos que solo existen tras `make datos_terceros` y la reconstrucción de los paneles.
  tests/conftest.py omite, con su motivo, los tests que los necesitan cuando faltan.
"""
from __future__ import annotations

import csv
import re
from pathlib import Path

PALABRA = re.compile(r"(?:^|[_\s])(notariado|registradores|cgn|cgpj|aeat)(?:[_\s]|$)", re.I)
REVISADAS_SIN_SERIES = {
    "output/v5/B3/tablas/shapley_R2.csv": "cuota de R² (Shapley) de cada familia en modelos con el precio de Registradores: resultado propio",
    "output/v5/B3/_smoke/tablas/shapley_R2.csv": "ídem (ejecución de prueba)",
}
REQUIEREN_TERCEROS = (
    "data/processed/nacional_q.csv", "data/processed/panel_ccaa_a.csv", "data/processed/v2/train/nacional_q_v2.csv",
    "data/processed/v8/nacional_q_v8.csv", "data/processed/v8/cv_prov_q_v8.csv",
    "data/raw/pdf/notariado_cgn_extranjeros_semestral.csv", "data/raw/pdf/registradores_opendata_compraventas.csv",
)


def columnas_terceros(cabecera: list[str]) -> list[str]:
    return [c for c in cabecera if PALABRA.search(c)]


def cabecera(p: Path) -> list[str]:
    if p.suffix != ".csv":
        return []
    with p.open(encoding="utf-8", errors="ignore", newline="") as fh:
        return next(csv.reader(fh), [])


def a_redactar(rel: str, p: Path) -> list[str]:
    """Columnas a quitar de la tabla rel (vacío si no hay que tocarla)."""
    if not rel.startswith("output/") or rel in REVISADAS_SIN_SERIES:
        return []
    return columnas_terceros(cabecera(p))


def redactar(origen: Path, destino: Path, quitar: list[str]) -> None:
    with origen.open(encoding="utf-8", newline="") as fi:
        r = csv.reader(fi)
        cab = next(r)
        idx = [i for i, c in enumerate(cab) if c not in set(quitar)]
        destino.parent.mkdir(parents=True, exist_ok=True)
        with destino.open("w", encoding="utf-8", newline="") as fo:
            w = csv.writer(fo, lineterminator="\n")
            w.writerow([cab[i] for i in idx])
            for fila in r:
                w.writerow([fila[i] if i < len(fila) else "" for i in idx])
