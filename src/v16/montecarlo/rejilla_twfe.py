"""Monte Carlo V16 (fase 5) · TWFE de la rejilla fija (output/v16/potencia/rejilla_fija.csv), dos escalas representativas.

Proceso generador (declarado en docs/v16/validacion_montecarlo/rejilla_twfe.md ANTES de simular):
  ESTRUCTURA (leída; sin valores del resultado): MUNICIPIO = unidades de entrenamiento con SERPAVI (2.014; clusters = su provincia);
  PROVINCIA = las 41 provincias de entrenamiento (cada una es su cluster). Ventana 2019-2025 (7 años => 6 diferencias).
  Especificación principal (rejilla): Dlog resultado_it = a_i + l_t + b x_it + u_it, con x_it = z_i * 1[t >= 2023] (exposición continua
  estandarizada, DiD de intensidad), efectos fijos de unidad y de periodo.
  EXPOSICIÓN z_i: campo gaussiano espacial estandarizado (alcance 150 km municipal; 300 km provincial) => correlación espacial.
  RESULTADO SIMULADO (log, en niveles; se toman diferencias): y_it = mu_i + d_i t + g_i1 f_1t + g_i2 f_2t + eta_p(i),t + s_it + e_it
    municipio: f AR(1) rho 0,6 sd 0,03; g_i1 ~ N(1; 0,5); g_i2 campo (150 km) N(0,1); eta provincia-año AR(1) rho 0,5 sd 0,02;
      s_it campo exp(-d/100 km) AR(1) rho 0,5 sd 0,02; e_it AR(1) rho 0,5 sd 0,05 exp(0,4 z_h - 0,08); d_i ~ N(0; 0,005)
    provincia: f AR(1) rho 0,6 sd 0,05; g_i1 ~ N(1; 0,4); g_i2 campo (300 km) N(0; 0,5); s_it campo (150 km) AR(1) 0,5 sd 0,03;
      e_it AR(1) rho 0,5 sd 0,05 exp(0,3 z_h - 0,045); d_i ~ N(0; 0,003)
  EFECTO sobre el crecimiento: nulo b = 0; alternativas b = 0,04 (magnitud de referencia Q2: 0,04 por DT de exposición; cobertura) y
  b = 0,01 (potencia); heterogeneidad b_i = b (1 + 0,5 z_h); verdad = media de b_i ponderada por x_it^2 (la que estima TWFE sin sesgo si
  b_i es independiente de x).
Inferencia: municipio = errores agrupados por provincia (CR1, t con G-1 gl); provincia = wild cluster bootstrap-t de Webb con el nulo
  impuesto (B = 999), cluster = provincia. Informativo (no cambia el veredicto): wild de Webb en la escala municipal no se calcula.
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
from scipy import stats

sys.path.insert(0, str(Path(__file__).resolve().parent))
import _comun_panel as C  # noqa: E402

K = 4
T = 7
TD = T - 1  # diferencias
POST0 = 4   # primer año post (2023) en índice de nivel 0..6 (2019..2025)
B = 999
B_REF = 0.04
B_POT = 0.01


def construir_estructura(escala: str) -> dict:
    rng = C.rng_estructura(K)
    if escala == "municipio":
        s = C.estructura_serpavi_municipal(completo=False)
        cod = s.cod.to_numpy()
        coords = C.coords_municipios(cod, rng)
        cl = pd.factorize(s.prov)[0]
        return {"escala": escala, "n": len(cod), "cl": cl, "G": int(cl.max() + 1), "coords": coords,
                "L_z": C.cholesky_exp(coords, 150.0), "L_g": C.cholesky_exp(coords, 150.0), "L_s": C.cholesky_exp(coords, 100.0)}
    provs = C.provincias_entrenamiento()
    coords = np.array([C.CENTROIDES[p] for p in provs])
    return {"escala": escala, "n": len(provs), "cl": np.arange(len(provs)), "G": len(provs), "coords": coords,
            "L_z": C.cholesky_exp(coords, 300.0), "L_g": C.cholesky_exp(coords, 300.0), "L_s": C.cholesky_exp(coords, 150.0)}


def simular(est: dict, rng: np.random.Generator, b: float) -> tuple[np.ndarray, np.ndarray, float]:
    """Devuelve dY (n, TD), x (n, TD) y la verdad."""
    n = est["n"]
    mun = est["escala"] == "municipio"
    z = est["L_z"] @ rng.standard_normal(n)
    z = (z - z.mean()) / z.std()
    zh = rng.standard_normal(n)
    if est.get("iid"):  # control de implementación: exposición y ruido independientes, sin factores ni campos
        z = rng.standard_normal(n)
        y = rng.normal(0, 1, n)[:, None] + rng.normal(0, 0.05, (n, T))
    elif mun:
        f = C.ar1(rng, 2, T, 0.6, 0.03)
        g1 = rng.normal(1.0, 0.5, n)
        g2 = est["L_g"] @ rng.standard_normal(n)
        y = (rng.normal(0, 1, n)[:, None] + rng.normal(0, 0.005, n)[:, None] * np.arange(T)[None, :]
             + g1[:, None] * f[0][None, :] + g2[:, None] * f[1][None, :])
        y += C.ar1(rng, est["G"], T, 0.5, 0.02)[est["cl"]]
        y += 0.02 * (est["L_s"] @ C.ar1(rng, n, T, 0.5, 1.0))
        y += C.ar1(rng, n, T, 0.5, 0.05, escala=np.exp(0.4 * zh - 0.08))
    else:
        f = C.ar1(rng, 2, T, 0.6, 0.05)
        g1 = rng.normal(1.0, 0.4, n)
        g2 = 0.5 * (est["L_g"] @ rng.standard_normal(n))
        y = (rng.normal(0, 1, n)[:, None] + rng.normal(0, 0.003, n)[:, None] * np.arange(T)[None, :]
             + g1[:, None] * f[0][None, :] + g2[:, None] * f[1][None, :])
        y += 0.03 * (est["L_s"] @ C.ar1(rng, n, T, 0.5, 1.0))
        y += C.ar1(rng, n, T, 0.5, 0.05, escala=np.exp(0.3 * zh - 0.045))
    dY = np.diff(y, axis=1)
    post = (np.arange(1, T) >= POST0).astype(float)  # periodos t=1..6
    x = z[:, None] * post[None, :]
    bi = b * (1 + 0.5 * rng.standard_normal(n))
    dY = dY + bi[:, None] * x
    ver = float((bi[:, None] * x ** 2).sum() / (x ** 2).sum()) if b != 0 else 0.0
    return dY, x, ver


def _tw(a: np.ndarray) -> np.ndarray:
    return a - a.mean(axis=1, keepdims=True) - a.mean(axis=0, keepdims=True) + a.mean()


def twfe(dY: np.ndarray, x: np.ndarray):
    xt, yt = _tw(x), _tw(dY)
    sxx = (xt ** 2).sum()
    beta = (xt * yt).sum() / sxx
    return beta, xt, yt, sxx


def inf_cluster(dY, x, cl, G) -> tuple[float, float, float, float]:
    beta, xt, yt, sxx = twfe(dY, x)
    e = yt - beta * xt
    sc = np.bincount(cl, weights=(xt * e).sum(axis=1), minlength=G)
    N = dY.size
    c = G / (G - 1) * (N - 1) / (N - TD)
    se = np.sqrt(c * (sc ** 2).sum()) / sxx
    tc = stats.t.ppf(0.975, G - 1)
    rej = float(abs(beta / se) > tc)
    return beta, beta - tc * se, beta + tc * se, rej


def inf_wild(dY, x, cl, G, rng) -> tuple[float, float, float, float]:
    """Wild cluster bootstrap-t de Webb con el nulo impuesto (WCR); cluster = provincia."""
    beta, xt, yt, sxx = twfe(dY, x)
    N = dY.size

    def se_de(bb, ys):  # ys: (n, TD, B) ya con efecto fijo proyectado
        e = ys - bb[None, None, :] * xt[:, :, None]
        sc = np.zeros((G, len(bb)))
        np.add.at(sc, cl, (xt[:, :, None] * e).sum(axis=1))
        return np.sqrt((sc ** 2).sum(axis=0)) / sxx

    # observado
    e = yt - beta * xt
    scn = np.bincount(cl, weights=(xt * e).sum(axis=1), minlength=G)
    se = np.sqrt((scn ** 2).sum()) / sxx
    v = C.webb(rng, (G, B))
    ys = yt[:, :, None] * v[cl][:, None, :]
    ys = ys - ys.mean(axis=1, keepdims=True) - ys.mean(axis=0, keepdims=True) + ys.mean(axis=(0, 1), keepdims=True)
    bb = (xt[:, :, None] * ys).sum(axis=(0, 1)) / sxx
    sb = se_de(bb, ys)
    tstar = bb / np.maximum(sb, 1e-15)
    t_obs = beta / se
    p = (1 + np.sum(np.abs(tstar) >= abs(t_obs))) / (B + 1)
    c = float(np.quantile(np.abs(tstar), 0.95))
    return beta, beta - c * se, beta + c * se, float(p <= 0.05)


def una_rep(est: dict, rng: np.random.Generator, b: float) -> list[float]:
    dY, x, ver = simular(est, rng, b)
    if est["escala"] == "municipio":
        r = inf_cluster(dY, x, est["cl"], est["G"])
    else:
        r = inf_wild(dY, x, est["cl"], est["G"], rng)
    return [ver, r[0], r[1], r[2], r[3]]


def _bloque(est, rngs, b):
    return [una_rep(est, r, b) for r in rngs]


def correr(est: dict, R: int, b: float, k_sub: int, n_jobs: int) -> np.ndarray:
    rngs = C.flujos(K * 100 + k_sub + (10 if est["escala"] == "provincia" else 0), R)
    nb = n_jobs * 4
    sal = Parallel(n_jobs=n_jobs)(delayed(_bloque)(est, rngs[i::nb], b) for i in range(nb))
    res = [None] * R
    for i, blq in enumerate(sal):
        for j, fila in enumerate(blq):
            res[i + j * nb] = fila
    return np.array(res, float)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--R", type=int, default=2000)
    ap.add_argument("--R_alt", type=int, default=2000)
    ap.add_argument("--R_pot", type=int, default=1000)
    ap.add_argument("--jobs", type=int, default=4)
    ap.add_argument("--salida", default=str(C.RAIZ / "output" / "v16" / "montecarlo" / "rejilla_twfe"))
    a = ap.parse_args()
    filas, res = [], {}
    for esc in ("municipio", "provincia"):
        est = construir_estructura(esc)
        info = {"n_unidades": est["n"], "n_clusters": est["G"], "periodos": T, "diferencias": TD}
        res[esc] = {"estructura": info, "resultados": {}}
        for nom, R, b, ks in (("nulo", a.R, 0.0, 1), ("alt_ref_0.04", a.R_alt, B_REF, 2), ("alt_pot_0.01", a.R_pot, B_POT, 3),
                              ("control_iid_nulo", 1000, 0.0, 4)):
            t0 = time.time()
            est["iid"] = nom == "control_iid_nulo"
            M = correr(est, R, b, ks, a.jobs)
            d = C.resumen_escenario(M[:, 1], M[:, 2], M[:, 3], M[:, 4], M[:, 0])
            d["segundos"] = time.time() - t0
            res[esc]["resultados"][nom] = d
            filas.append({"escala": esc, "escenario": nom, "b": b, **info, **d})
            print(esc, nom, {k: round(v, 4) for k, v in d.items() if isinstance(v, float)}, flush=True)
    tabla = pd.DataFrame(filas)
    C.guardar(Path(a.salida), res, tabla)


if __name__ == "__main__":
    main()
