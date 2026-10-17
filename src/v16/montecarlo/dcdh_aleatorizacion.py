"""Monte Carlo V16 (fase 5) · de Chaisemartin-D'Haultfoeuille (tratamiento continuo, no absorbente) con inferencia por aleatorización
del calendario entre CCAA, Q6.

Proceso generador (declarado en docs/v16/validacion_montecarlo/dcdh_aleatorizacion.md ANTES de simular):
  ESTRUCTURA (leída; sin valores del resultado): 41 provincias de entrenamiento agrupadas en sus CCAA (9 no selladas + Ceuta y Melilla
  como clusters sin cambio de tipo); tratamiento = tipo general del ITP por CCAA y año 2011-2024, construido con las filas de
  intervenciones.csv (el último valor con fecha de efecto en el año o antes). Panel anual, 14 años.
  RESULTADO SIMULADO (log compraventas usadas anual): y_it = mu_i + delta_i t + g_i1 f_1t + g_i2 f_2t + u_c(i),t + s_it + e_it + beta_i D_it
    f_1, f_2 AR(1) rho 0,7, sd 0,10; g_i1 ~ N(1; 0,4); g_i2 = campo espacial (300 km) sd 0,5
    u_ct: choque CCAA-año AR(1) rho 0,5, sd 0,04 * exp(0,3 z_c - 0,045) (heterocedasticidad entre CCAA)
    s_it: campo espacial exp(-d/150 km), AR(1) rho 0,5, sd 0,04;  e_it: AR(1) rho 0,5, sd 0,06 * exp(0,3 z_i - 0,045); delta_i ~ N(0; 0,003)
  EFECTO (contemporáneo por punto de tipo): nulo = 0; alternativas -0,07 por punto (volumen, Fritzsche-Vandrei) y -0,01 (precio),
  beta_i = beta (1 + 0,5 z_i); la verdad es la media de beta_i ponderada por |dD| en las celdas que cambian.
Estimador DID_M continuo: beta = sum_{(g,t) con cambio} sign(dD)(dY - media de dY de los que no cambian en t) / sum |dD|; el año anterior a
  cada cambio no se usa como control (anticipación).
Inferencia: p-valor y IC por aleatorización: se reasignan los calendarios completos de tipo entre CCAA (B = 499 permutaciones al azar de
  las 11 CCAA/clusters); IC = beta +- cuantil 95 % de |beta permutado| (consistente con el contraste). No hay alternativa nombrada: si falla, NO APTO.
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

K = 3
ANIOS = list(range(2011, 2025))
T = len(ANIOS)
B_PERM = 499
BETA_VOL = -0.07
BETA_PRE = -0.01


def construir_estructura() -> dict:
    provs = C.provincias_entrenamiento()
    ccaa = np.array([C.PROV_CCAA[p] for p in provs])
    d = C.intervenciones()
    i = d[(d.instrumento == "itp") & d.parametro.str.startswith("tipo general ITP")].copy()
    i["f"] = pd.to_datetime(i.fecha_efecto)
    i["v"] = i.valor.astype(float)
    i = i.sort_values("f")
    ucc = sorted(set(ccaa))
    ruta = {}
    for c in ucc:
        x = i[i.cod_ine.str.zfill(2) == c]
        r = []
        for a in ANIOS:
            xx = x[x.f.dt.year <= a]
            r.append(float(xx.v.iloc[-1]) if len(xx) else np.nan)
        r = np.array(r)
        if np.isnan(r).all():
            r = np.full(T, 7.0)  # sin filas: tipo constante (no cambia)
        r = pd.Series(r).ffill().bfill().to_numpy()
        ruta[c] = r
    D = np.array([ruta[c] for c in ccaa])  # (n, T)
    cl = np.array([ucc.index(c) for c in ccaa])
    coords = np.array([C.CENTROIDES[p] for p in provs])
    cambian = [c for c in ucc if np.any(np.diff(ruta[c]) != 0)]
    return {"provs": provs, "ccaa": ccaa, "ucc": ucc, "cl": cl, "G": len(ucc), "D": D, "n": len(provs), "coords": coords,
            "L300": C.cholesky_exp(coords, 300.0), "L150": C.cholesky_exp(coords, 150.0), "cambian": cambian,
            "ruta": {c: ruta[c].tolist() for c in ucc}}


def beta_dcdh(dY: np.ndarray, D: np.ndarray) -> float:
    """DID_M continuo. dY (n, T-1) diferencias de Y para t=1..T-1; D (n, T)."""
    dD = np.diff(D, axis=1)
    cambia = dD != 0
    ant = np.zeros_like(cambia)
    ant[:, :-1] = cambia[:, 1:]  # cambio en t+1: año de anticipación
    est = (~cambia) & (~ant)
    ne = est.sum(axis=0)
    m = np.where(ne > 0, (dY * est).sum(axis=0) / np.maximum(ne, 1), np.nan)
    usa = cambia & (ne > 0)[None, :]
    den = np.abs(dD[usa]).sum()
    if den == 0:
        return np.nan
    return float((np.sign(dD)[usa] * (dY - m[None, :])[usa]).sum() / den)


def simular(est: dict, rng: np.random.Generator, beta: float) -> tuple[np.ndarray, float]:
    n, G = est["n"], est["G"]
    cl = est["cl"]
    f = C.ar1(rng, 2, T, 0.7, 0.10)
    g1 = rng.normal(1.0, 0.4, n)
    g2 = 0.5 * (est["L300"] @ rng.standard_normal(n))
    zc = rng.standard_normal(G)
    z = rng.standard_normal(n)
    if est.get("iid"):  # control de implementación: ruido independiente sin factores, campos ni choques de CCAA
        y = rng.normal(0, 1, n)[:, None] + rng.normal(0, 0.08, (n, T))
        b_i = beta * (1 + 0.5 * rng.standard_normal(n))
        y += b_i[:, None] * est["D"]
        w = np.abs(np.diff(est["D"], axis=1)) * (np.diff(est["D"], axis=1) != 0)
        return y, float((b_i[:, None] * w).sum() / w.sum())
    y = (rng.normal(0, 1, n)[:, None] + rng.normal(0, 0.003, n)[:, None] * np.arange(T)[None, :]
         + g1[:, None] * f[0][None, :] + g2[:, None] * f[1][None, :])
    y += C.ar1(rng, G, T, 0.5, 0.04, escala=np.exp(0.3 * zc - 0.045))[cl]
    y += 0.04 * (est["L150"] @ C.ar1(rng, n, T, 0.5, 1.0))
    y += C.ar1(rng, n, T, 0.5, 0.06, escala=np.exp(0.3 * z - 0.045))
    b_i = beta * (1 + 0.5 * rng.standard_normal(n))
    D = est["D"]
    y += b_i[:, None] * D
    dD = np.diff(D, axis=1)
    cambia = dD != 0
    w = np.abs(dD) * cambia
    ver = float((b_i[:, None] * w).sum() / w.sum())
    return y, ver


def inferir(est: dict, y: np.ndarray, rng: np.random.Generator) -> tuple[float, float, float, float]:
    D = est["D"]
    dY = np.diff(y, axis=1)
    b = beta_dcdh(dY, D)
    G, cl = est["G"], est["cl"]
    pert = np.empty(B_PERM)
    # filas de D por cluster (todas las provincias de una CCAA comparten calendario)
    ruta_cl = np.array([D[np.where(cl == g)[0][0]] for g in range(G)])
    for k in range(B_PERM):
        perm = rng.permutation(G)
        pert[k] = beta_dcdh(dY, ruta_cl[perm][cl])
    ok = np.isfinite(pert)
    a = np.sort(np.abs(pert[ok]))
    if len(a) < 100 or not np.isfinite(b):
        return b, np.nan, np.nan, np.nan
    c = a[int(np.ceil(0.95 * len(a))) - 1]
    p = (1 + np.sum(a >= abs(b))) / (len(a) + 1)
    return b, b - c, b + c, float(p <= 0.05)


def una_rep(est: dict, rng: np.random.Generator, beta: float) -> list[float]:
    y, ver = simular(est, rng, beta)
    b, lo, hi, rej = inferir(est, y, rng)
    return [ver, b, lo, hi, rej]


def _bloque(est, rngs, beta):
    return [una_rep(est, r, beta) for r in rngs]


def correr(est: dict, R: int, beta: float, k_sub: int, n_jobs: int) -> np.ndarray:
    rngs = C.flujos(K * 100 + k_sub, R)
    nb = n_jobs * 4
    sal = Parallel(n_jobs=n_jobs)(delayed(_bloque)(est, rngs[i::nb], beta) for i in range(nb))
    res = [None] * R
    for i, blq in enumerate(sal):
        for j, fila in enumerate(blq):
            res[i + j * nb] = fila
    return np.array(res, float)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--R", type=int, default=2000)
    ap.add_argument("--R_alt", type=int, default=2000)
    ap.add_argument("--R_pre", type=int, default=1000)
    ap.add_argument("--jobs", type=int, default=4)
    ap.add_argument("--salida", default=str(C.RAIZ / "output" / "v16" / "montecarlo" / "dcdh_aleatorizacion"))
    a = ap.parse_args()
    est = construir_estructura()
    info = {"n_provincias": est["n"], "n_clusters_ccaa": est["G"], "ccaa": [str(c) for c in est["ucc"]], "ccaa_con_cambios": [str(c) for c in est["cambian"]],
            "anios": [ANIOS[0], ANIOS[-1]], "n_celdas_con_cambio": int((np.diff(est["D"], axis=1) != 0).sum()),
            "n_permutaciones": B_PERM}
    filas, res = [], {}
    for nom, R, beta, ks in (("nulo", a.R, 0.0, 1), ("alt_vol_-0.07", a.R_alt, BETA_VOL, 2), ("alt_precio_-0.01", a.R_pre, BETA_PRE, 3),
                             ("control_iid_nulo", 1000, 0.0, 4)):
        t0 = time.time()
        est["iid"] = nom == "control_iid_nulo"
        M = correr(est, R, beta, ks, a.jobs)
        d = C.resumen_escenario(M[:, 1], M[:, 2], M[:, 3], M[:, 4], M[:, 0])
        d["segundos"] = time.time() - t0
        res[nom] = d
        filas.append({"escenario": nom, "beta": beta, **d})
    tabla = pd.DataFrame(filas)
    C.guardar(Path(a.salida), {"estructura": info, "resultados": res}, tabla)
    print(info)
    print(tabla.to_string())


if __name__ == "__main__":
    main()
