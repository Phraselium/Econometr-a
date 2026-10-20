"""V18 · Resumen de métricas por variante a partir de p-valores (tamaño, cobertura por inversión del contraste, potencia)."""
from __future__ import annotations

import os

for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS"):   # BLAS de un hilo: antes de importar numpy
    os.environ.setdefault(_v, "1")

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from src.v18.montecarlo._comun import fila_metricas  # noqa: E402

ALCANCE_TERRITORIAL = "sin lectura de datos"


def filas_por_p(escenario: str, variantes: dict, Mn: np.ndarray, Ma: np.ndarray, col_est: int | None = 1, col_ver: int | None = 0,
                extra: dict | None = None) -> list[dict]:
    """variantes: nombre -> (col_p0, col_pverdad). Mn: réplicas bajo el nulo (col_p0 contrasta θ = 0, que es la verdad);
    Ma: réplicas bajo la alternativa (col_p0 = potencia; col_pverdad = cobertura por inversión del contraste en la verdad).
    Un p NaN cuenta como no rechazo."""
    filas = []
    for nom, (c0, cv) in variantes.items():
        pn, pa0, pav = Mn[:, c0], Ma[:, c0], Ma[:, cv]
        tam = float(np.mean(np.nan_to_num(pn, nan=1.0) <= 0.05))
        cob_n = 1 - tam
        cob_a = float(np.mean(np.nan_to_num(pav, nan=1.0) > 0.05))
        pot = float(np.mean(np.nan_to_num(pa0, nan=1.0) <= 0.05))
        sesgo = rmse = None
        if col_est is not None and col_ver is not None:
            e = Mn[:, col_est] - Mn[:, col_ver]
            e = e[np.isfinite(e)]
            sesgo, rmse = float(e.mean()), float(np.sqrt((e ** 2).mean()))
        ex = {"R_alt": int(len(Ma)), "p_nan": float(np.mean(np.isnan(pn)))}
        if extra:
            ex.update(extra)
        filas.append(fila_metricas(escenario, nom, tam, cob_n, cob_a, pot, len(Mn), sesgo, rmse, ex))
    return filas
