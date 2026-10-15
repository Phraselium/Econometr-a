"""V9 · validación Monte Carlo del IC de Rambachan y Roth (magnitudes relativas, contraste LF) de src/v9/herramientas.py
antes de usarlo como regla de capa (regla V7; revisión F3, hallazgo 1). Estudio de eventos simulado con 5 coeficientes
previos y 4 posteriores, covarianza intercambiable (ρ = 0,5, EE 0,01), efecto θ = 0,05 y tendencia lineal (que pertenece
a Δ^RM(M̄) para M̄ ≥ 1). Contraste condicional de ARP por pieza. Se mide la cobertura del θ verdadero y la anchura media.
Salida: output/v9/validacion/honest_rr_mc.csv. SEED = 20261010. Tarda unos minutos.
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
import herramientas as H  # noqa: E402

OUT = Path(__file__).resolve().parents[2] / "output" / "v9" / "validacion"
R = 30


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    rng = np.random.default_rng(H.SEED)
    pre, post = list(range(-6, -1)), list(range(0, 4))
    orden = pre + post
    n = len(orden)
    S = 0.01 ** 2 * (0.5 * np.eye(n) + 0.5)
    L = np.linalg.cholesky(S)
    filas = []
    # tamaño del contraste condicional en el θ verdadero (400 réplicas, M̄ = 0): rápido y preciso
    piezas = H._piezas_rm(len(pre), len(post), 0.0)
    A = piezas[0]
    SY = A @ S @ A.T
    sig = np.sqrt(np.clip(np.diag(SY), 1e-14, None))
    l = np.ones(len(post)) / len(post)
    Bm = np.linalg.svd(l[None, :])[2][1:].T
    Ap = A[:, len(pre):]
    rech = []
    for _ in range(400):
        b = np.r_[np.zeros(len(pre)), 0.05 * np.ones(len(post))] + L @ rng.standard_normal(n)
        rech.append(H._arp_condicional(A @ b - Ap @ (0.05 * np.ones(len(post))), Ap @ Bm, sig, SY, 0.05))
    filas.append({"pendiente_previa": 0.0, "Mbar": 0.0, "replicas": 400, "cobertura_theta": 1 - float(np.mean(rech)),
                  "anchura_media": np.nan, "excluye_0": np.nan})
    print(filas[-1])
    for pendiente, M in ((0.0, 0.0), (0.0, 1.0), (0.004, 1.0)):
        cub, ancho, excl0 = [], [], []
        for _ in range(R):
            d = np.array([pendiente * (e + 1) for e in orden])
            tau = np.array([0.0] * len(pre) + [0.05] * len(post))
            b = d + tau + L @ rng.standard_normal(n)
            res = {"es_orden": orden, "es": {e: (b[i], np.sqrt(S[i, i])) for i, e in enumerate(orden)}, "es_vcov": S}
            lo, hi = H.honest_rr(res, M)
            cub.append(lo <= 0.05 <= hi)
            ancho.append(hi - lo)
            excl0.append(not (lo <= 0 <= hi))
        filas.append({"pendiente_previa": pendiente, "Mbar": M, "replicas": R, "cobertura_theta": np.mean(cub),
                      "anchura_media": np.mean(ancho), "excluye_0": np.mean(excl0)})
        print(filas[-1])
    pd.DataFrame(filas).to_csv(OUT / "honest_rr_mc.csv", index=False, float_format="%.4f")
    return 0


if __name__ == "__main__":
    sys.exit(main())
