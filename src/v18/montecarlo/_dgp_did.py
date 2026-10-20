"""V18 · Procesos generadores de los diseños de diferencias en diferencias de V18 (solo estructura declarada; todo simulado).

Escenarios (dimensiones tomadas del plan de replicación; ningún dato real):
  cat_trim_S / _M / _L : Cataluña, municipio-trimestre 2019T1-2022T1 (T = 13); una cohorte que entra en 2020T4 (índice 7);
                         tratados 50 / 100 / 150 y controles 100 / 200 / 300; 42 comarcas.
  cat_anual            : Cataluña, municipio-año 2014-2021 (T = 8); cohorte 2020 (índice 6); 100 tratados, 200 controles.
  zt2024_2cohortes     : zonas tensionadas, trimestre 2022T1-2026T1 (T = 17); dos cohortes (2024T2, índice 9, 45 municipios; 2025T2,
                         índice 13, 25 municipios); 150 controles.
  pocos_tratados       : 10 tratados y 150 controles, T = 13, una cohorte en el índice 7.
  itp_8ccaa            : 36 provincias en 8 CCAA (tamaños 8, 1, 9, 5, 4, 3, 2, 4), trimestre 2010T1-2015T4 (T = 24); cohortes por CCAA
                         (3 CCAA / 15 provincias en 2012T1, índice 8; 3 CCAA / 11 provincias en 2013T1, índice 12; 2 CCAA / 10 provincias
                         sin cambio); cluster = CCAA.
Resultado simulado (log):  y_it = a_i + d_i t + Σ_k λ_ik f_kt + η_c(i),t + ε_it + efecto_it
  f_1, f_2 AR(1) (ρ_f, sd_f); λ_i1 ~ N(1; 0,4), λ_i2 ~ N(0; 0,5); η_ct AR(1) por comarca / CCAA (ρ_η, sd_η); ε_it AR(1) (ρ_ε, sd_ε
  · exp(0,3 z_i − 0,045)); d_i ~ N(0; sd_d). Las tendencias paralelas se cumplen en esperanza (la asignación no depende de λ, d ni z).
  Frecuencia trimestral: ρ_f 0,8, sd_f 0,03; ρ_η 0,6, sd_η 0,02; ρ_ε 0,5, sd_ε 0,05; sd_d 0,001.
  Frecuencia anual:      ρ_f 0,6, sd_f 0,04; ρ_η 0,4, sd_η 0,025; ρ_ε 0,4, sd_ε 0,06; sd_d 0,004.
Efecto: nulo = 0; alternativa τ (log) con heterogeneidad τ_i = τ (1 + 0,5 z'_i) y dinámica 1 − exp(−(e + 1)/2) tras la entrada.
Los valores son declarados, no estimados con datos reales.
"""
from __future__ import annotations

import os

for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS"):   # BLAS de un hilo: antes de importar numpy
    os.environ.setdefault(_v, "1")

from dataclasses import dataclass

import numpy as np

ALCANCE_TERRITORIAL = "sin lectura de datos"
SEMILLA = 20261010

TRIM = dict(rho_f=0.8, sd_f=0.03, rho_n=0.6, sd_n=0.02, rho_e=0.5, sd_e=0.05, sd_d=0.001)
ANUAL = dict(rho_f=0.6, sd_f=0.04, rho_n=0.4, sd_n=0.025, rho_e=0.4, sd_e=0.06, sd_d=0.004)


@dataclass
class Diseno:
    nombre: str
    T: int
    cohorte: np.ndarray       # (n,) índice del primer periodo tratado o −1
    cl_fino: np.ndarray       # cluster principal (municipio o provincia→CCAA según diseño)
    cl_grueso: np.ndarray     # comarca o CCAA
    params: dict
    cluster_principal: str    # «municipio» o «CCAA»

    @property
    def n(self) -> int:
        return len(self.cohorte)


def _ar1(rng, n, T, rho, sd):
    z = rng.standard_normal((n, T))
    x = np.empty((n, T))
    x[:, 0] = z[:, 0]
    s = np.sqrt(1 - rho ** 2)
    for t in range(1, T):
        x[:, t] = rho * x[:, t - 1] + s * z[:, t]
    return x * sd


def _municipal(nombre: str, cohortes: dict[int, int], N0: int, T: int, params: dict, G: int = 42) -> Diseno:
    rng = np.random.default_rng([SEMILLA, 18, hash_nombre(nombre)])
    coh = np.concatenate([np.full(n, g) for g, n in cohortes.items()] + [np.full(N0, -1)])
    n = len(coh)
    # comarcas: los tratados se concentran en las 12 primeras (peso 3), los controles reparten parejo con tamaños desiguales
    w_c = rng.dirichlet(np.ones(G) * 2.0)
    w_t = w_c.copy()
    w_t[:12] *= 3.0
    w_t /= w_t.sum()
    com = np.empty(n, int)
    tr = coh >= 0
    com[tr] = rng.choice(G, size=int(tr.sum()), p=w_t)
    com[~tr] = rng.choice(G, size=int((~tr).sum()), p=w_c)
    return Diseno(nombre, T, coh, np.arange(n), com, params, "municipio")


def hash_nombre(s: str) -> int:
    return sum((i + 1) * ord(c) for i, c in enumerate(s)) % 100003


def _itp(nombre: str = "itp_8ccaa", coh_ccaa: tuple = (8, -1, -1, 12, 8, 8, 12, 12)) -> Diseno:
    tam = [8, 1, 9, 5, 4, 3, 2, 4]            # And, Cant, CyL, CLM, Cat, Val, Ext, Gal
    ccaa = np.repeat(np.arange(8), tam)
    coh = np.repeat(coh_ccaa, tam)
    return Diseno(nombre, 24, coh, ccaa, ccaa, TRIM, "CCAA")


def diseno(nombre: str) -> Diseno:
    if nombre == "cat_trim_S":
        return _municipal(nombre, {7: 50}, 100, 13, TRIM)
    if nombre == "cat_trim_M":
        return _municipal(nombre, {7: 100}, 200, 13, TRIM)
    if nombre == "cat_trim_L":
        return _municipal(nombre, {7: 150}, 300, 13, TRIM)
    if nombre == "cat_anual":
        return _municipal(nombre, {6: 100}, 200, 8, ANUAL)
    if nombre == "zt2024_2cohortes":
        return _municipal(nombre, {9: 45, 13: 25}, 150, 17, TRIM)
    if nombre == "pocos_tratados":
        return _municipal(nombre, {7: 10}, 150, 13, TRIM)
    if nombre == "itp_8ccaa":
        return _itp()
    if nombre == "itp_8ccaa_4controles (diagnóstico)":
        return _itp(nombre, (8, -1, -1, 12, 8, 12, -1, -1))
    if nombre == "itp_8ccaa_5controles (diagnóstico)":
        return _itp(nombre, (8, -1, -1, 12, -1, -1, -1, 8))
    raise KeyError(nombre)


ESCENARIOS = ["cat_trim_S", "cat_trim_M", "cat_trim_L", "cat_anual", "zt2024_2cohortes", "pocos_tratados", "itp_8ccaa"]
# diagnóstico (no deciden el veredicto): el diseño de 8 CCAA con 4 y 5 CCAA de control (16 y 19 provincias) y 3 y 2 CCAA tratadas
DIAGNOSTICO = ["itp_8ccaa_4controles (diagnóstico)", "itp_8ccaa_5controles (diagnóstico)"]


def simular(d: Diseno, rng: np.random.Generator, tau: float) -> tuple[np.ndarray, np.ndarray]:
    """Y (n, T) y matriz de efectos verdaderos (n, T)."""
    p, n, T = d.params, d.n, d.T
    f = _ar1(rng, 2, T, p["rho_f"], p["sd_f"])
    lam1 = rng.normal(1.0, 0.4, n)
    lam2 = rng.normal(0.0, 0.5, n)
    G = int(d.cl_grueso.max()) + 1
    eta = _ar1(rng, G, T, p["rho_n"], p["sd_n"])
    if d.cluster_principal == "CCAA":     # heterocedasticidad entre CCAA
        eta = eta * np.exp(0.3 * rng.standard_normal(G) - 0.045)[:, None]
    z = rng.standard_normal(n)
    y = (rng.normal(0, 1, n)[:, None] + rng.normal(0, p["sd_d"], n)[:, None] * np.arange(T)[None, :]
         + lam1[:, None] * f[0][None, :] + lam2[:, None] * f[1][None, :] + eta[d.cl_grueso]
         + _ar1(rng, n, T, p["rho_e"], p["sd_e"]) * np.exp(0.3 * z - 0.045)[:, None])
    efecto = np.zeros((n, T))
    if tau != 0.0:
        het = tau * (1 + 0.5 * rng.standard_normal(n))
        for g in set(d.cohorte[d.cohorte >= 0].tolist()):
            m = d.cohorte == g
            ramp = 1 - np.exp(-(np.arange(T - g) + 1) / 2)
            efecto[m, g:] = het[m, None] * ramp[None, :]
    return y + efecto, efecto
