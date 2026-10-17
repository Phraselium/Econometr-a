"""Monte Carlo V16 (fase 5) · Callaway-Sant'Anna con wild cluster bootstrap de Webb por provincia, Q1c.

Proceso generador (declarado en docs/v16/validacion_montecarlo/cs_webb.md ANTES de simular):
  ESTRUCTURA (leída; sin valores del resultado): las 41 provincias de entrenamiento; trimestres 2019T1-2026T2 (30); tratamiento =
  provincia con alguna zona vigente, con la cohorte del primer trimestre completo posterior a la fecha de efecto (intervenciones.csv);
  comparación = nunca tratadas. Cada provincia es su propio cluster.
  RESULTADO SIMULADO (log compraventas trimestral): y_it = mu_i + delta_i t + g_i1 f_1t + g_i2 f_2t + s_it + e_it
    f_1, f_2: factores comunes AR(1) rho 0,8, sd 0,08; g_i1 ~ N(1; 0,4); g_i2 = campo espacial exp(-d/300 km) con sd 0,5
    s_it: campo gaussiano espacial exp(-d/150 km) entre centroides, AR(1) rho 0,6, sd 0,04
    e_it: AR(1) rho 0,5, sd marginal 0,06 * exp(0,3 z_i - 0,045); delta_i ~ N(0; 0,002) tendencia propia. Valores declarados.
  EFECTO: nulo = 0; alternativas 0,05 y 0,10 (log) con heterogeneidad tau_i = tau (1 + 0,5 z_i) y dinámica 1 - exp(-(e+1)/2) tras la entrada;
  la verdad es el ATT agregado muestral (misma ponderación que el estimador).
Estimador: ATT(g,t) con nunca tratadas y periodo base g-1, agregado «simple» (peso por tamaño de cohorte sobre las celdas t >= g).
Inferencia: multiplicador wild cluster bootstrap-t de Webb (6 puntos) sobre la función de influencia, B = 999, por provincia.
"""
from __future__ import annotations

import os

for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS"):
    os.environ.setdefault(_v, "1")

import argparse
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd
from joblib import Parallel, delayed

sys.path.insert(0, str(Path(__file__).resolve().parent))
import _comun_panel as C  # noqa: E402

K = 2
T = 30  # 2019T1..2026T2
B = 999
TAU_ALT = 0.05
TAU_ALT2 = 0.10


def trimestre_idx(fecha: pd.Timestamp) -> int:
    """Índice 0..29 del trimestre que contiene la fecha (2019T1 = 0)."""
    return (fecha.year - 2019) * 4 + (fecha.month - 1) // 3


def construir_estructura() -> dict:
    provs = C.provincias_entrenamiento()
    z = C.zonas_tensionadas()
    primera = z[z.prov.isin(provs)].groupby("prov").efecto.min()
    cohorte = np.full(len(provs), -1)
    for i, p in enumerate(provs):
        if p in primera.index:
            g = trimestre_idx(primera[p]) + 1  # primer trimestre completo posterior
            if g < T:
                cohorte[i] = g
    coords = np.array([C.CENTROIDES[p] for p in provs])
    return {"provs": provs, "cohorte": cohorte, "n": len(provs), "coords": coords,
            "L300": C.cholesky_exp(coords, 300.0), "L150": C.cholesky_exp(coords, 150.0)}


def simular_y(est: dict, rng: np.random.Generator, tau: float, iid: bool = False) -> tuple[np.ndarray, np.ndarray]:
    """Devuelve Y (n, T) y la matriz de efectos verdaderos (n, T). iid=True: control de implementación sin dependencia."""
    n = est["n"]
    if iid:
        y = rng.normal(0, 1, n)[:, None] + rng.normal(0, 0.06, (n, T))
        efecto = np.zeros((n, T))
        for i in range(n):
            g = est["cohorte"][i]
            if g >= 0:
                efecto[i, g:] = tau * (1 - np.exp(-(np.arange(T - g) + 1) / 2))
        return y + efecto, efecto
    f = C.ar1(rng, 2, T, 0.8, 0.08)
    g1 = rng.normal(1.0, 0.4, n)
    g2 = 0.5 * (est["L300"] @ rng.standard_normal(n))
    z = rng.standard_normal(n)
    y = (rng.normal(0, 1, n)[:, None] + rng.normal(0, 0.002, n)[:, None] * np.arange(T)[None, :]
         + g1[:, None] * f[0][None, :] + g2[:, None] * f[1][None, :])
    y += 0.04 * (est["L150"] @ C.ar1(rng, n, T, 0.6, 1.0))
    y += C.ar1(rng, n, T, 0.5, 0.06, escala=np.exp(0.3 * z - 0.045))
    efecto = np.zeros((n, T))
    for i in range(n):
        g = est["cohorte"][i]
        if g >= 0:
            e = np.arange(T - g)
            efecto[i, g:] = tau * (1 + 0.5 * rng.standard_normal()) * (1 - np.exp(-(e + 1) / 2))
    return y + efecto, efecto


def cs_att(Y: np.ndarray, cohorte: np.ndarray) -> tuple[float, np.ndarray, np.ndarray]:
    """ATT simple de CS con nunca tratadas. Devuelve ATT, función de influencia por unidad (n,) y pesos de celda."""
    n = len(cohorte)
    nunca = cohorte < 0
    nC = nunca.sum()
    gs = sorted(set(cohorte[cohorte >= 0]))
    celdas = [(g, t) for g in gs for t in range(g, T)]
    peso_g = {g: (cohorte == g).sum() for g in gs}
    tot = sum(peso_g[g] for g, _ in celdas)
    att = 0.0
    psi = np.zeros(n)
    psi0 = np.zeros(n)  # residuos con el nulo impuesto: tratada menos la media de las nunca tratadas (válido con cohortes de 1 provincia)
    for g, t in celdas:
        w = peso_g[g] / tot
        d = Y[:, t] - Y[:, g - 1]
        G = cohorte == g
        mG, mC = d[G].mean(), d[nunca].mean()
        att += w * (mG - mC)
        psi[G] += w * (d[G] - mG) / G.sum()
        psi[nunca] -= w * (d[nunca] - mC) / nC
        psi0[G] += w * (d[G] - mC) / G.sum()
        psi0[nunca] -= w * (d[nunca] - mC) / nC
    return float(att), psi, psi0


def verdad(efecto: np.ndarray, cohorte: np.ndarray) -> float:
    gs = sorted(set(cohorte[cohorte >= 0]))
    celdas = [(g, t) for g in gs for t in range(g, T)]
    peso_g = {g: (cohorte == g).sum() for g in gs}
    tot = sum(peso_g[g] for g, _ in celdas)
    return float(sum(peso_g[g] / tot * efecto[cohorte == g, t].mean() for g, t in celdas))


def una_rep(est: dict, rng: np.random.Generator, tau: float, iid: bool = False) -> list[float]:
    Y, efecto = simular_y(est, rng, tau, iid)
    coh = est["cohorte"]
    att, psi, psi0 = cs_att(Y, coh)
    ver = verdad(efecto, coh)
    v = C.webb(rng, (est["n"], B))
    out = [ver, att]
    # (a) multiplicador sobre la función de influencia (no restringido); (b) wild cluster bootstrap con el nulo impuesto (WCR)
    for sc in (psi, psi0):
        se = np.sqrt((sc ** 2).sum())
        num = (v * sc[:, None]).sum(axis=0)
        sestar = np.sqrt(((v * sc[:, None]) ** 2).sum(axis=0))
        tstar = num / np.maximum(sestar, 1e-15)
        t_obs = att / max(se, 1e-15)
        c = float(np.quantile(np.abs(tstar), 0.95))
        p = (1 + np.sum(np.abs(tstar) >= abs(t_obs))) / (B + 1)
        out += [att - c * se, att + c * se, float(p <= 0.05)]
    return out


def _bloque(est, rngs, tau, iid):
    return [una_rep(est, r, tau, iid) for r in rngs]


def correr(est: dict, R: int, tau: float, k_sub: int, n_jobs: int, iid: bool = False) -> np.ndarray:
    rngs = C.flujos(K * 100 + k_sub, R)
    nb = n_jobs * 4
    sal = Parallel(n_jobs=n_jobs)(delayed(_bloque)(est, rngs[i::nb], tau, iid) for i in range(nb))
    res = [None] * R
    for i, blq in enumerate(sal):
        for j, fila in enumerate(blq):
            res[i + j * nb] = fila
    return np.array(res, float)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--R", type=int, default=2000)
    ap.add_argument("--R_alt", type=int, default=2000)
    ap.add_argument("--R_alt2", type=int, default=1000)
    ap.add_argument("--jobs", type=int, default=4)
    ap.add_argument("--salida", default=str(C.RAIZ / "output" / "v16" / "montecarlo" / "cs_webb"))
    a = ap.parse_args()
    est = construir_estructura()
    info = {"n_provincias": est["n"], "n_trimestres": T, "n_tratadas": int((est["cohorte"] >= 0).sum()),
            "cohortes": {int(g): int((est["cohorte"] == g).sum()) for g in sorted(set(est["cohorte"][est["cohorte"] >= 0]))},
            "n_nunca_tratadas": int((est["cohorte"] < 0).sum())}
    filas, res = [], {}
    for nom, R, tau, ks, iid in (("nulo", a.R, 0.0, 1, False), ("alt_005", a.R_alt, TAU_ALT, 2, False), ("alt_010", a.R_alt2, TAU_ALT2, 3, False),
                                 ("control_iid_nulo", 1000, 0.0, 4, True)):
        t0 = time.time()
        M = correr(est, R, tau, ks, a.jobs, iid)
        da = C.resumen_escenario(M[:, 1], M[:, 2], M[:, 3], M[:, 4], M[:, 0])
        db = C.resumen_escenario(M[:, 1], M[:, 5], M[:, 6], M[:, 7], M[:, 0])
        res[nom] = {"a_multiplicador_IF": da, "b_WCR_nulo_impuesto": db, "segundos": time.time() - t0}
        filas.append({"escenario": nom, "tau": tau, "variante": "a_multiplicador_IF", **da})
        filas.append({"escenario": nom, "tau": tau, "variante": "b_WCR_nulo_impuesto", **db})
    tabla = pd.DataFrame(filas)
    C.guardar(Path(a.salida), {"estructura": info, "resultados": res}, tabla)
    print(info)
    print(tabla.to_string())


if __name__ == "__main__":
    main()
