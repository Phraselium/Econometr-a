"""V18 · Monte Carlo de de Chaisemartin-D'Haultfœuille (dosis continua escalonada) con inferencia por aleatorización del calendario
entre CCAA y con wild bootstrap de Webb (plan de replicación, 1.13; E8-R1 y E8-R2).

Uso: python3 src/v18/montecarlo/dcdh_aleatorizacion.py [--R 2000] [--jobs 4]
Proceso generador: src/v18/montecarlo/_dgp_itp.py (36 provincias en 8 CCAA, T = 24, cambios concentrados en 2012-2013).
"""
from __future__ import annotations

import os

for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS"):   # BLAS de un hilo: antes de importar numpy
    os.environ.setdefault(_v, "1")

import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from src.v18.herramientas import dcdh as H  # noqa: E402
from src.v18.montecarlo import _comun as C  # noqa: E402
from src.v18.montecarlo import _dgp_itp as P  # noqa: E402
from src.v18.montecarlo import _informe as I  # noqa: E402
from src.v18.montecarlo._resumen import filas_por_p  # noqa: E402

ALCANCE_TERRITORIAL = "sin lectura de datos"
HERR = "dcdh_aleatorizacion"
K1 = 21

DGP = """
Estructura (declarada; ningún dato real): panel provincial trimestral 2010T1-2015T4 (T = 24) con 36 provincias en 8 CCAA de régimen común
(tamaños 8, 1, 9, 5, 4, 3, 2, 4); dosis = tipo general del ITP por CCAA; 6 CCAA cambian 1 o 2 veces (85 % de los cambios en 2012T1-2013T4,
índices 8-15; tamaño +1, +2, −1, −2 puntos con prob. 0,4/0,3/0,2/0,1) y 2 CCAA (10 provincias) no cambian. El calendario se redibuja en cada réplica.
Resultado (log): y_it = a_i + d_i t + Σ_k λ_ik f_kt + η_c(i),t + ε_it + β_i D_it. Factores comunes AR(1) ρ 0,8 sd 0,03; choque CCAA-trimestre AR(1)
ρ 0,6 sd 0,02·exp(0,3 z_c − 0,045) (heterocedasticidad entre CCAA, escenario «desigual»); ε_it AR(1) ρ 0,5 sd 0,05·exp(0,3 z_i − 0,045); d_i ~ N(0; 0,001);
β_i = β (1 + 0,5 z'_i), efecto de nivel de la dosis. Nulo β = 0; alternativa β = −0,03 por punto (precio, referencia Dolls et al.).
Pocos clusters: 8 (cluster = CCAA). Escenarios: «desigual» (tamaños y varianzas desiguales) y «equilibrado» (4-5 provincias por CCAA, sin heterocedasticidad; diagnóstico).
Estimador: DID_ℓ de dCDH con ℓ = 4 (efecto a 4 trimestres, E8-R1; principal) y ℓ = 0 (contemporáneo, como V16; información). Cambiantes: ΔD ≠ 0 sin otro
cambio en (t, t+ℓ]; controles: sin cambio en [t, t+ℓ]; β̂ = Σ sign(ΔD)(ΔY − m_t) / Σ |ΔD|. Verdad: media de β_i ponderada por |ΔD| en las celdas cambiantes.
Inferencia: (1) aleatorización del calendario entre las 8 CCAA, estadístico ESTUDENTIZADO |β̂/EE| (nueva; principal), 499 permutaciones aleatorias + identidad;
(2) aleatorización con el coeficiente |β̂| (la de V16); (3) bootstrap-t de Webb por CCAA con nulo impuesto, 999; (4) t de Student (G−1 = 7 gl) con EE de agrupación.
Cobertura = 1 − tasa de rechazo del contraste de θ = verdad (inversión del contraste; efecto constante impuesto en el contraste de aleatorización).
"""

V16 = """
V16 (src/v16/montecarlo/dcdh_aleatorizacion.py): tamaño 0,0775 y cobertura 0,967 con 11 clusters, estadístico sin estudentizar y 499 permutaciones. Hipótesis de V16: heterogeneidad de tamaño y de varianza entre
clusters (los calendarios permutados no serían intercambiables para el coeficiente). Este Monte Carlo NO la confirma con la estructura de V18 (8 CCAA, dosis de nivel, calendarios concentrados en 2012-2013): el
estadístico sin estudentizar da un tamaño de 0,04-0,06 y el estudentizado también, en el escenario desigual y en el equilibrado, de modo que el 0,0775 de V16 no se reproduce y su causa (11 clusters, 41 provincias,
DID_M contemporáneo, correlación espacial entre provincias) no queda identificada aquí. Se mantiene la estudentización como principal (es la razón de intercambiabilidad más robusta a priori) y se mide la
cobertura invirtiendo el contraste. Lo que sí falla, y de forma clara, es el bootstrap de Webb con 8 clusters (tamaño 0,12-0,15), como cabía esperar con menos de 10 clusters. No se repite el diseño de V16
con un criterio más laxo: el criterio es el del encargo y se reporta junto a las bandas de la adenda 1.12.
"""


def rep(rng: np.random.Generator, esc: str, ell: int, beta: float, B: int) -> list[float]:
    y, Dc, bi, cl = P.simular(rng, esc, beta)
    M = H.onehot(cl)
    Dobs = Dc[cl]
    ver = H.verdad(bi, Dobs, ell)
    r = H.estimar(y, Dobs, ell)
    b = float(r["beta"]) if np.isfinite(r["beta"]) else np.nan
    se = float(H.ee_cluster(r["IF"], M)) if np.isfinite(b) else np.nan
    perms = H.permutaciones(rng, 8, B)
    fila = [ver, b]
    thetas = [0.0] if beta == 0 else [0.0, ver]
    out = {0: [], 1: []}
    for k, th in enumerate(thetas):
        if not np.isfinite(b):
            out[k] = [np.nan] * 4
            continue
        pe = H.p_aleatorizacion(y, Dc, cl, th, ell, perms, True)
        pc = H.p_aleatorizacion(y, Dc, cl, th, ell, perms, False)
        pw = H.p_webb(y, Dobs, th, ell, M, rng, 999)
        pt = float(2 * stats.t.sf(abs(b - th) / max(se, 1e-300), 7))
        out[k] = [pe, pc, pw, pt]
    if beta == 0:
        out[1] = out[0]
    # columnas: 2..5 = p en θ0 = 0 (estud, coef, webb, t); 6..9 = p en θ0 = verdad
    return fila + out[0] + out[1]


def main(R: int = 2000, jobs: int = 4, B: int = 499, salida: Path | None = None) -> pd.DataFrame:
    filas = []
    t_ini = time.time()
    for i, (esc, ell) in enumerate([("desigual", 4), ("equilibrado", 4), ("desigual", 0), ("equilibrado", 0)]):
        t0 = time.time()
        Mn = C.ejecutar(rep, (esc, ell, 0.0, B), R, K1, i * 10 + 1, jobs)
        Ma = C.ejecutar(rep, (esc, ell, P.BETA_ALT, B), R, K1, i * 10 + 2, jobs)
        var = {"aleatorizacion_estudentizada": (2, 6), "aleatorizacion_coeficiente (V16)": (3, 7), "webb_8_clusters": (4, 8), "t_cluster_7gl": (5, 9)}
        ex = {"ell": ell, "clusters": 8, "B_perm": B, "seg": round(time.time() - t0, 1)}
        filas += filas_por_p(f"itp_{esc}_ell{ell}", var, Mn, Ma, extra=ex)
        print(esc, ell, [(f["variante"], round(f["tamano_5pct"], 4), round(f["cobertura_alt"], 4)) for f in filas[-4:]], ex["seg"], flush=True)
    tabla = pd.DataFrame(filas)
    prim = tabla[(tabla.variante == "aleatorizacion_estudentizada") & (tabla.escenario == "itp_desigual_ell4")]
    r = prim.iloc[0]
    veredicto = "APTO" if r.veredicto == "APTO" else "NO APTO"
    cond = "" if veredicto == "APTO" else r.fallos
    res = C.resultado_base(HERR, "¿Es válida la inferencia por aleatorización del calendario (y Webb) para dCDH con dosis continua escalonada, 8 CCAA?",
                           "simulados (sin datos reales ni muestra sellada)", "36 provincias, 8 CCAA, T = 24; R = %d" % R,
                           "DID_ℓ de de Chaisemartin-D'Haultfœuille, aleatorización de calendarios entre CCAA y bootstrap de Webb")
    res["estimacion"] = {"tamano": float(r.tamano_5pct), "cobertura_nulo": float(r.cobertura_nulo), "cobertura_alt": float(r.cobertura_alt),
                         "potencia": float(r.potencia), "sesgo": float(r.sesgo), "rmse": float(r.rmse)}
    res["diagnosticos"] = {"veredicto": veredicto, "condicion_en_que_falla": cond, "variante_principal": "aleatorizacion_estudentizada, itp_desigual_ell4",
                           "por_fila": {f"{a}|{b}": v for a, b, v in zip(tabla.escenario, tabla.variante, tabla.veredicto)},
                           "banda_112_principal": r.banda_112, "R": R, "segundos": round(time.time() - t_ini, 1)}
    res["notas"] = "Valores simulados. Las demás variantes son información; el veredicto lo decide la principal."
    informe = I.construir("de Chaisemartin-D'Haultfœuille con aleatorización del calendario (8 CCAA)", DGP, tabla, veredicto, cond,
                          ["Principal: aleatorización estudentizada, escenario «desigual», ℓ = 4. Las demás filas son diagnóstico.",
                           f"R = {R} réplicas por escenario y por bloque (nulo y alternativa); permutaciones por réplica: {B}."], V16)
    C.escribir(HERR, res, tabla, informe, salida)
    return tabla


if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--R", type=int, default=2000)
    ap.add_argument("--B", type=int, default=499)
    ap.add_argument("--jobs", type=int, default=4)
    a = ap.parse_args()
    print(main(a.R, a.jobs, a.B).to_string())
