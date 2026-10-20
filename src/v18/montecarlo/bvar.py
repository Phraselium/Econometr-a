"""V18 · Monte Carlo del BVAR recursivo con prior de Minnesota (cobertura de las bandas al 68 % y al 90 %; E7-R3 y E7-A1).

Todo simulado: ningún dato real de resultado ni muestra sellada. SEED 20261010. Estimador: src/v18/estimacion/e7_bvar_lib.py.
Uso: python3 src/v18/montecarlo/bvar.py [--R 2000] [--jobs 4] [--D 500]

Criterio (declarado antes de simular). Las bandas del BVAR son intervalos de credibilidad al 68 % y al 90 % (San Juan, 2023), no intervalos al 95 %. Se mide su
cobertura frecuentista de la respuesta verdadera (a +100 pb del tipo, en puntos porcentuales) a h = 8 para el precio, las compraventas y los visados. Los
márgenes del criterio del encargo (cobertura al 95 % en [0,92; 0,97], es decir ±2,5 pp, unos 5 errores típicos binomiales con R = 2.000) se trasladan a la
misma distancia en errores típicos binomiales: cobertura del 68 % en [0,63; 0,73] y del 90 % en [0,87; 0,93].
  - Filas decisivas: prior principal, persistencia 0,97 (la de las series en niveles), T = 60 (E7-R3) y T = 74 (E7-A1), con y sin efecto verdadero, tres variables.
  - APTO: todas las filas decisivas dentro de las dos bandas; APTO CONDICIONADO: algunas; NO APTO: ninguna. Con NO APTO la estimación se publica solo como informativa.
  - Las demás filas (persistencia 0,90, T = 48, prior más laxa) son información.
"""
from __future__ import annotations

import os

for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS"):   # BLAS de un hilo: antes de importar numpy
    os.environ.setdefault(_v, "1")

import functools
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd

RAIZ = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(RAIZ))
sys.path.insert(0, str(RAIZ / "src" / "v18" / "estimacion"))
import e7_bvar_lib as B  # noqa: E402
from src.v18.montecarlo import _comun as C  # noqa: E402
from src.v18.montecarlo import _informe as I  # noqa: E402

ALCANCE_TERRITORIAL = "sin lectura de datos"
HERR = "bvar"
K1 = 26
N, P_DGP, P_EST = 7, 2, 2
ORDEN = ["compraventas", "precio", "visados", "PIB", "IPCA", "euribor", "crédito"]
J_SHOCK = 5
VARS = {0: "compraventas", 1: "precio", 2: "visados"}
HS = (4, 8)
GAMMA = np.array([1, 1, 1, 1, 0.8, 0.8, 1.0])
UNIDAD = np.array([100.0, 100.0, 100.0, 100.0, 1.0, 1.0, 100.0])      # divisor de la media inicial en la suma de coeficientes (convención en logaritmos)
NIVEL = np.array([1100.0, 750.0, 1000.0, 470.0, 2.0, 1.5, 950.0])
ESCALA = np.array([3.0, 0.8, 6.0, 0.5, 0.4, 0.15, 5.0])
PRIORS = {"principal": dict(lam=0.2, mu=0.5), "laxa": dict(lam=0.5, mu=0.0), "difusa": dict(lam=50.0, mu=0.0)}
BANDA68, BANDA90 = (0.63, 0.73), (0.87, 0.93)
FALTAN = {33: 2, 37: 2}                       # visados ausentes en 2016T2 y 2017T2 (índices de la muestra que empieza en 2008T1)
ESCENARIOS = [  # (T, persistencia, decisivo)
    (60, 0.97, True), (74, 0.97, True), (60, 0.90, False), (74, 0.90, False), (48, 0.97, False)]

DGP = """
Estructura (declarada; ningún dato real): VAR(2) de 7 variables en el orden de San Juan (2023), [compraventas, precio, visados, PIB, IPCA, euríbor, crédito] (variables en 100 log salvo el IPCA y el euríbor, en puntos
porcentuales), con 3 ficticias estacionales no nulas en la estimación (el proceso verdadero no tiene estacionalidad: la estimación se carga de parámetros inútiles, un caso conservador) y los huecos de visados de 2016T2 y 2017T2 de la base.
Proceso verdadero: matrices A_1 = diag(0,5) + N(0; 0,05²) y A_2 = diag(0,2) + N(0; 0,05²) con SEED 20261010; se pone a cero la columna del euríbor en las ecuaciones de las tres variables de interés y se
fijan los efectos hacia delante del euríbor (alternativa: compraventas −1,2, precio −0,5, visados −2,5 por pp en el primer rezago); en el nulo, la respuesta verdadera de las tres variables al choque del euríbor es EXACTAMENTE cero a todo
horizonte (se anula toda la columna del euríbor y la del crédito en las ecuaciones de las variables que anteceden al crédito). Se reescala todo para que la mayor raíz de la companion sea ρ = 0,97 o 0,90.
Perturbaciones u_t = B0 ε_t con B0 = diag(σ) (I + N(0; 0,3²) estrictamente por debajo de la diagonal), σ = (3; 0,8; 6; 0,5; 0,4; 0,15; 5): triangular inferior con diagonal positiva, de modo que el Cholesky de Σ es B0 y la
identificación recursiva es exacta (supuesto de San Juan cumplido por construcción). Choque: el del euríbor (posición 6), normalizado a +1 pp en su impacto (+100 pb).
Estimador: BVAR(2) con prior de Minnesota en observaciones ficticias (λ = 0,2, γ = 1 en niveles y 0,8 en el IPCA y el euríbor, decaimiento por rezago, suma de coeficientes con peso 1/(10 λ) = 0,5 sobre la media inicial en logaritmos (convención de Bańbura et al., 2010); escalas σ_i del AR(1) de cada serie; Σ ~ IW,
B | Σ normal): 500 extracciones del posterior por réplica; bandas por percentiles 16-84 y 5-95 de la respuesta normalizada a h = 4 y 8. La «prior más laxa» (variante v1 de E7-R3) usa λ = 0,5 y sin suma de coeficientes; la «difusa» (λ = 50, sin suma de coeficientes; solo información) comprueba que el código da una cobertura cercana a la nominal cuando el prior apenas informa.
Cobertura = proporción de réplicas con la respuesta verdadera dentro de la banda. T = 60 (2008T1-2022T4, E7-R3), 74 (2008T1-2026T2, E7-A1) y 48 (2008T1-2019T4, E7-R3-v2).
"""

V16 = """
No hay Monte Carlo previo de un BVAR en V15 ni en V16 (el plan lo marca «Sin validar», sección 1.13). Se aplica lo aprendido en las demás herramientas de V18: el proceso generador reproduce la estructura de la muestra (T, huecos, orden de las
variables), el nulo se impone exactamente sobre las respuestas medidas y la cobertura se mide por inversión sobre la verdad del propio proceso; se separan la persistencia (0,90 y 0,97) y el tamaño muestral.
"""


@functools.lru_cache(maxsize=None)
def _estructura(rho: float, alt: bool):
    rng = np.random.default_rng([C.SEMILLA, K1, 1])
    A = np.zeros((P_DGP, N, N))
    A[0] = np.diag([0.5] * N) + rng.normal(0, 0.05, (N, N))
    A[1] = np.diag([0.2] * N) + rng.normal(0, 0.05, (N, N))
    B0 = np.diag(ESCALA) @ (np.eye(N) + np.tril(rng.normal(0, 0.3, (N, N)), -1))
    A[:, :3, J_SHOCK] = 0.0
    if alt:
        A[0, 0, J_SHOCK], A[0, 1, J_SHOCK], A[0, 2, J_SHOCK] = -1.2, -0.5, -2.5
    else:
        A[:, :6, J_SHOCK] = 0.0       # el euríbor no entra en ninguna ecuación previa al crédito
        A[:, :6, 6] = 0.0             # ni el crédito (sumidero)
    comp = np.zeros((N * P_DGP, N * P_DGP))
    comp[:N, :N], comp[:N, N:] = A[0], A[1]
    comp[N:, :N] = np.eye(N)
    A = A * (rho / np.max(np.abs(np.linalg.eigvals(comp))))
    return A, B0


def irf_verdadera(A: np.ndarray, B0: np.ndarray, h: int) -> np.ndarray:
    Psi = [np.eye(N)]
    for s in range(1, h + 1):
        Psi.append(sum(A[l - 1] @ Psi[s - l] for l in range(1, min(s, P_DGP) + 1)))
    return Psi[h] @ B0[:, J_SHOCK] / B0[J_SHOCK, J_SHOCK]


def simular(rng: np.random.Generator, T: int, rho: float, alt: bool):
    A, B0 = _estructura(rho, alt)
    burn = 100
    U = rng.standard_normal((T + burn, N)) @ B0.T
    Y = np.zeros((T + burn, N))
    for t in range(P_DGP, T + burn):
        Y[t] = A[0] @ Y[t - 1] + A[1] @ Y[t - 2] + U[t]
    Y = Y[burn:] + NIVEL
    for i, c in FALTAN.items():
        if i < T:
            Y[i, c] = np.nan
    return Y


def rep(rng: np.random.Generator, T: int, rho: float, alt: bool, D: int) -> list[float]:
    Y = simular(rng, T, rho, alt)
    A, B0 = _estructura(rho, alt)
    trim = (np.arange(T) % 4) + 1
    fila = []
    for nombre, pr in PRIORS.items():
        post = B.ajustar(Y, trim, P_EST, pr["lam"], pr["mu"], GAMMA, unidad=UNIDAD)
        Bd, Sg = B.sacar(post, D, rng)
        R = B.irf(Bd, Sg, N, P_EST, max(HS), J_SHOCK)
        estable = float(np.mean(B.raiz_maxima(Bd, N, P_EST) < 1.0))
        for h in HS:
            ver = irf_verdadera(A, B0, h)
            for j in VARS:
                x = R[:, h, j]
                q = np.percentile(x, [5, 16, 50, 84, 95])
                v = ver[j]
                fila += [float(q[1] <= v <= q[3]), float(q[0] <= v <= q[4]), float(q[3] - q[1]), float(q[2] - v), float(v)]
        fila.append(estable)
    return fila


def _filas(M: np.ndarray, escenario: str, alt: bool, T: int, rho: float, decisivo: bool, R: int, seg: float) -> list[dict]:
    """M (R, ...) -> filas por prior, h y variable. Por prior: |HS| x |VARS| x 5 columnas + 1 (estable)."""
    filas = []
    por_prior = len(HS) * len(VARS) * 5 + 1
    for ip, nombre in enumerate(PRIORS):
        base = ip * por_prior
        est = float(M[:, base + por_prior - 1].mean())
        c = base
        for h in HS:
            for j, vn in VARS.items():
                cov68, cov90, w68, err, ver = (M[:, c + k] for k in range(5))
                c += 5
                c68, c90 = float(cov68.mean()), float(cov90.mean())
                ok = BANDA68[0] <= c68 <= BANDA68[1] and BANDA90[0] <= c90 <= BANDA90[1]
                fallos = []
                if not BANDA68[0] <= c68 <= BANDA68[1]:
                    fallos.append(f"cobertura 68 % {c68:.3f} fuera de [{BANDA68[0]}; {BANDA68[1]}]" + (" (conservadora)" if c68 > BANDA68[1] else " (insuficiente)"))
                if not BANDA90[0] <= c90 <= BANDA90[1]:
                    fallos.append(f"cobertura 90 % {c90:.3f} fuera de [{BANDA90[0]}; {BANDA90[1]}]" + (" (conservadora)" if c90 > BANDA90[1] else " (insuficiente)"))
                filas.append({"escenario": escenario, "variante": nombre, "variable": vn, "h": h, "T": T, "rho": rho, "efecto_verdadero": "alternativa" if alt else "nulo",
                              "respuesta_verdadera": float(ver.mean()), "R": R, "cobertura_68": c68, "cobertura_90": c90, "se_mc_68": C.mc_se(c68, R), "se_mc_90": C.mc_se(c90, R),
                              "ancho_banda_68": float(w68.mean()), "sesgo_mediana": float(err.mean()), "rmse_mediana": float(np.sqrt((err ** 2).mean())),
                              "raices_estables": est, "decisivo": bool(decisivo and nombre == "principal" and h == 8),
                              "veredicto": "APTO" if ok else "NO APTO", "fallos": " / ".join(fallos), "seg": seg})
    return filas


def main(R: int = 2000, jobs: int = 4, D: int = 500, salida: Path | None = None) -> pd.DataFrame:
    filas = []
    t_ini = time.time()
    idx = 0
    for T, rho, dec in ESCENARIOS:
        for alt in (False, True):
            idx += 1
            t0 = time.time()
            M = C.ejecutar(rep, (T, rho, alt, D), R, K1, idx, jobs)
            esc = f"T={T}|rho={rho}"
            filas += _filas(M, esc, alt, T, rho, dec, R, round(time.time() - t0, 1))
            f = [x for x in filas[-12:] if x["variante"] == "principal" and x["h"] == 8]
            print(esc, "alt" if alt else "nulo", [(x["variable"][:4], round(x["cobertura_68"], 3), round(x["cobertura_90"], 3)) for x in f], round(time.time() - t0, 1), flush=True)
    tabla = pd.DataFrame(filas)
    dec = tabla[tabla.decisivo]
    n_ok = int((dec.veredicto == "APTO").sum())
    veredicto = "APTO" if n_ok == len(dec) else ("NO APTO" if n_ok == 0 else "APTO CONDICIONADO")
    cond = "; ".join(f"{r.escenario}|{r.efecto_verdadero}|{r.variable}: {r.fallos}" for r in dec[dec.veredicto != "APTO"].itertuples())
    res = C.resultado_base(HERR, "¿Tienen las bandas bayesianas al 68 % y al 90 % del BVAR recursivo (E7-R3 y E7-A1) una cobertura frecuentista cercana a la nominal con T = 60-74?",
                           "simulados (sin datos reales ni muestra sellada)", f"VAR(2) de 7 variables, T = 48, 60 y 74; R = {R}; {D} extracciones del posterior por réplica",
                           "BVAR de Minnesota (observaciones ficticias, normal-Wishart inversa), identificación recursiva, respuesta a +100 pb del euríbor")
    pr = tabla[tabla.decisivo & (tabla.variable == "precio")]
    res["estimacion"] = {"filas_decisivas": int(len(dec)), "filas_decisivas_aptas": n_ok,
                         "cobertura_68_precio_h8": {f"{r.escenario}|{r.efecto_verdadero}": round(float(r.cobertura_68), 4) for r in pr.itertuples()},
                         "cobertura_90_precio_h8": {f"{r.escenario}|{r.efecto_verdadero}": round(float(r.cobertura_90), 4) for r in pr.itertuples()}}
    res["diagnosticos"] = {"veredicto": veredicto, "condicion_en_que_falla": cond, "R": R, "D": D, "banda_cobertura_68": BANDA68, "banda_cobertura_90": BANDA90,
                           "segundos": round(time.time() - t_ini, 1), "regla": "con NO APTO la estimación de E7-R3 y E7-A1 se publica solo como informativa"}
    informe = I.construir("BVAR recursivo con prior de Minnesota: cobertura de las bandas (E7-R3 y E7-A1)", DGP, tabla, veredicto, cond,
                          ["Filas decisivas: prior principal, persistencia 0,97, T = 60 y 74, h = 8, con y sin efecto verdadero, precio, compraventas y visados (la columna `decisivo`).",
                           "La cobertura es la de un intervalo de credibilidad en repetición frecuentista: un prior de Minnesota encoge hacia el paseo aleatorio y puede sesgar la mediana.",
                           f"El proceso generador cumple por construcción la identificación recursiva: la cobertura mide solo la incertidumbre de estimación, no el error de especificación.",
                           f"R = {R} réplicas (error típico binomial del 68 % ≈ {C.mc_se(0.68, R):.3f}); R >= 1.000, como pide el encargo."],
                          V16, ["escenario", "variante", "variable", "h", "efecto_verdadero", "R", "cobertura_68", "cobertura_90", "ancho_banda_68", "sesgo_mediana", "raices_estables", "decisivo", "veredicto"])
    C.escribir(HERR, res, tabla, informe, salida)
    return tabla


if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--R", type=int, default=2000)
    ap.add_argument("--jobs", type=int, default=4)
    ap.add_argument("--D", type=int, default=500)
    ap.add_argument("--salida", default=None)
    a = ap.parse_args()
    from src.v18.montecarlo import bvar as _m   # las funciones deben vivir en un módulo importable para que joblib las serialice por referencia
    t = _m.main(a.R, a.jobs, a.D, Path(a.salida) if a.salida else None)
    print(t[t.decisivo][["escenario", "efecto_verdadero", "variable", "cobertura_68", "cobertura_90", "veredicto"]].to_string())
