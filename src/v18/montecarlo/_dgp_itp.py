"""V18 · Proceso generador del diseño ITP (E8): 36 provincias en 8 CCAA, trimestre 2010T1-2015T4 (T = 24), tipo de gravamen por CCAA.

Estructura declarada (ningún dato real):
  tamaños de CCAA (provincias): 8, 1, 9, 5, 4, 3, 2, 4 (régimen común no sellado: Andalucía, Cantabria, Castilla y León, Castilla-La
  Mancha, Cataluña, C. Valenciana, Extremadura, Galicia). Las dos primeras CCAA sin cambio (Cantabria y Castilla y León: 10 provincias)
  garantizan controles en todo periodo; las otras seis cambian el tipo 1 o 2 veces (prob. 0,6 / 0,4); el 85 % de los cambios cae en
  2012T1-2013T4 (índices 8-15) y el resto en cualquier otro trimestre; tamaño del cambio +1 (0,4), +2 (0,3), −1 (0,2), −2 (0,1) puntos.
  El calendario se redibuja en cada réplica (se valida la herramienta para la familia de calendarios con esas propiedades).
Resultado (log): y_it = a_i + d_i t + Σ_k λ_ik f_kt + η_c(i),t + ε_it + β_i D_it
  f_1, f_2 AR(1) ρ 0,8, sd 0,03; η_ct AR(1) ρ 0,6, sd 0,02 · exp(0,3 z_c − 0,045) (heterocedasticidad entre CCAA, solo en «desigual»);
  ε_it AR(1) ρ 0,5, sd 0,05 · exp(0,3 z_i − 0,045); d_i ~ N(0; 0,001); β_i = β (1 + 0,5 z'_i), efecto de NIVEL de la dosis.
  Nulo β = 0; alternativa β = −0,03 por punto (precio, Dolls et al.).
Escenarios: «desigual» (tamaños anteriores y heterocedasticidad) y «equilibrado» (8 CCAA de 4 a 5 provincias, sin heterocedasticidad:
control de diagnóstico).
"""
from __future__ import annotations

import os

for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS"):   # BLAS de un hilo: antes de importar numpy
    os.environ.setdefault(_v, "1")

import numpy as np

ALCANCE_TERRITORIAL = "sin lectura de datos"

T = 24
TAM = {"desigual": [8, 1, 9, 5, 4, 3, 2, 4], "equilibrado": [4, 5, 5, 5, 4, 5, 4, 4]}
SIN_CAMBIO = (1, 2)
BETA_ALT = -0.03


def cl_idx(escenario: str) -> np.ndarray:
    return np.repeat(np.arange(8), TAM[escenario])


def calendario(rng: np.random.Generator, escenario: str = "desigual") -> np.ndarray:
    """Dosis (tipo en puntos) por CCAA y trimestre, (8, T)."""
    Dc = np.full((8, T), 7.0)
    for a in range(8):
        if a in SIN_CAMBIO:
            continue
        k = int(rng.choice([1, 2], p=[0.6, 0.4]))
        tiempos = set()
        while len(tiempos) < k:
            t = int(rng.integers(8, 16)) if rng.random() < 0.85 else int(rng.integers(2, T - 1))
            tiempos.add(t)
        for t in sorted(tiempos):
            Dc[a, t:] += rng.choice([1.0, 2.0, -1.0, -2.0], p=[0.4, 0.3, 0.2, 0.1])
    return Dc


def simular(rng: np.random.Generator, escenario: str, beta: float, het: bool = True) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """Devuelve (Y (n,T), Dc (8,T), beta_i (n,), cl (n,))."""
    cl = cl_idx(escenario)
    n = len(cl)
    Dc = calendario(rng, escenario)
    f = np.empty((2, T))
    for k in range(2):
        z = rng.standard_normal(T)
        f[k, 0] = z[0]
        for t in range(1, T):
            f[k, t] = 0.8 * f[k, t - 1] + 0.6 * z[t]
    f *= 0.03
    eta = np.empty((8, T))
    zz = rng.standard_normal((8, T))
    eta[:, 0] = zz[:, 0]
    for t in range(1, T):
        eta[:, t] = 0.6 * eta[:, t - 1] + 0.8 * zz[:, t]
    eta *= 0.02
    if escenario == "desigual":
        eta *= np.exp(0.3 * rng.standard_normal(8) - 0.045)[:, None]
    ze = rng.standard_normal((n, T))
    eps = np.empty((n, T))
    eps[:, 0] = ze[:, 0]
    for t in range(1, T):
        eps[:, t] = 0.5 * eps[:, t - 1] + np.sqrt(0.75) * ze[:, t]
    eps *= 0.05 * np.exp(0.3 * rng.standard_normal(n) - 0.045)[:, None]
    y = (rng.normal(0, 1, n)[:, None] + rng.normal(0, 0.001, n)[:, None] * np.arange(T)[None, :]
         + rng.normal(1.0, 0.4, n)[:, None] * f[0][None, :] + rng.normal(0, 0.5, n)[:, None] * f[1][None, :] + eta[cl] + eps)
    beta_i = (beta * (1 + 0.5 * rng.standard_normal(n)) if het else np.full(n, beta)) if beta != 0 else np.zeros(n)
    y = y + beta_i[:, None] * Dc[cl]
    return y, Dc, beta_i, cl
