"""V18 · Monte Carlo del SVAR con proxy (instrumento externo) y bandas robustas a la debilidad (E7-R2), con la longitud mensual de la sorpresa 1999-2025.

Uso: python3 src/v18/montecarlo/svar_proxy.py [--R 2000] [--jobs 4]
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
from scipy import stats

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from src.v18.herramientas import lp_iv as L  # noqa: E402
from src.v18.herramientas import svar_proxy as H  # noqa: E402
from src.v18.montecarlo import _comun as C  # noqa: E402
from src.v18.montecarlo import _informe as I  # noqa: E402
from src.v18.montecarlo._resumen import filas_por_p  # noqa: E402

ALCANCE_TERRITORIAL = "sin lectura de datos"
HERR = "svar_proxy"
K1 = 25
N, P_DGP, P_EST, T, BURN = 6, 2, 4, 108, 100
HS = (4, 8)
J_PRECIO, REF = 1, 0
FUERZA_F = {"fuerte": 63.0, "moderada": 12.7, "debil": 3.8}   # objetivos de calibración; la F robusta medida sale ≈ 0,79 de ellos
PERSIST = {"rho090": 0.90, "rho097": 0.97}

DGP = """
Estructura (declarada; ningún dato real): VAR trimestral de 6 variables [tipo hipotecario, ln precio real, ln compraventas, ln PIB, IPCA, euríbor] (E7-R2), T = 108 trimestres (1999T1-2025T4), con
el proxy construido desde una sorpresa MENSUAL de 324 meses (suma de 3 meses por trimestre, t de Student 5 gl, 15 % de meses sin reunión).
Proceso verdadero: VAR(2) con matrices de coeficientes fijadas con SEED 20261010 (diagonal 0,5 y 0,2 más cruces N(0; 0,06²), reescaladas para que la mayor raíz de la companion sea ρ = 0,90 o 0,97);
u_t = B0 ε_t con B0 triangular inferior: primera columna (choque monetario) b = (1; −0,15; −0,3; −0,1; 0,05; 0,6) y resto N(0; 0,5²) con diagonal 1. El proxy es z_t = φ ε_{1t} + ν_t, ν_t la suma trimestral
de la sorpresa mensual con error de medida; φ se calibra para que la F robusta de la primera etapa (u_1 sobre z) medida valga ≈ 50, 10 o 3 con T_eff = 104 (la F de Q5 fue 2,1-2,9); la F medida se informa en la tabla.
Nulo (θ = 0): la ecuación del precio solo depende de su propio pasado y no responde al choque monetario (b_precio = 0), de modo que su IRF al choque es 0 a todo horizonte; alternativa: el precio depende del tipo (−0,15 y −0,05 en los rezagos 1 y 2) y de las compraventas (+0,1), con b_precio = −0,15.
Estimación: VAR(4) por MCO (constante incluida; uno o dos rezagos más que el verdadero), m̂ = E[z û], θ̂_{h,precio} = Ψ_h[precio, :] m̂ / m̂[tipo] a h = 4 y 8 (principal: 8; «a 8 trimestres escalada a +100 pb»).
Variantes: (1) AR por método delta con varianza de largo plazo Newey-West de 4 rezagos sobre las influencias conjuntas de (A, m) (robusta a proxy débil; conjunto por forma cerrada); (2) Wald de método delta (θ̂ ± 1,96 EE);
(3) bootstrap de bloques móviles (longitud 8, 199 réplicas, percentil) sobre las filas (Y, z), en el 20 % de las réplicas (R_bb). Cobertura = 1 − rechazo del contraste en θ verdadero (inversión; AR por forma cerrada).
"""

V16 = """
No hay Monte Carlo previo del SVAR con proxy en V15 ni en V16 (el plan lo marca «Sin validar»). Se reutiliza la lección de V16 sobre series (lp_newey_west_b NO APTO: ancho de banda y persistencia) midiendo con persistencia alta (ρ = 0,97)
y se separa la fuerza del proxy. Con F ≈ 3 el Wald de método delta no es válido por construcción; el AR es el que se evalúa para el veredicto en todas las fuerzas.
"""


@functools.lru_cache(maxsize=None)
def _estructura(rho: float, nulo: bool):
    rng = np.random.default_rng([C.SEMILLA, 25, 1])
    A = np.zeros((P_DGP, N, N))
    A[0] = np.diag([0.5] * N) + rng.normal(0, 0.06, (N, N))
    A[1] = np.diag([0.2] * N) + rng.normal(0, 0.06, (N, N))
    if nulo:
        A[:, J_PRECIO, :] = 0.0
        A[0, J_PRECIO, J_PRECIO] = 0.6
        A[1, J_PRECIO, J_PRECIO] = 0.2
    else:
        A[0, J_PRECIO, 0], A[1, J_PRECIO, 0], A[0, J_PRECIO, 2] = -0.15, -0.05, 0.1
    comp = np.zeros((N * P_DGP, N * P_DGP))
    comp[:N, :N], comp[:N, N:] = A[0], A[1]
    comp[N:, :N] = np.eye(N)
    # reescala solo la parte «libre»: se multiplica todo por el factor que lleva la mayor raíz a rho (el nulo conserva sus ceros)
    r = np.max(np.abs(np.linalg.eigvals(comp)))
    A = A * (rho / r)
    B0 = np.tril(rng.normal(0, 0.5, (N, N)), -1) + np.eye(N)
    B0[:, 0] = [1.0, -0.15, -0.3, -0.1, 0.05, 0.6]
    if nulo:
        B0[J_PRECIO, 0] = 0.0
    return A, B0


@functools.lru_cache(maxsize=None)
def _phi(F_obj: float, nulo: bool, rho: float) -> float:
    """φ que da una F robusta de primera etapa ≈ F_obj: F ≈ T_eff ρ²/(1 − ρ²) con ρ² = φ² b² / ((φ² + 1) Σ_j B0[0, j]²)."""
    A, B0 = _estructura(rho, nulo)
    var_u1 = float((B0[0, :] ** 2).sum())
    b11 = B0[0, 0]
    target = F_obj / (F_obj + (T - P_EST))          # ρ²
    # ρ² = φ² b² / ((φ² + 1) var_u1)  → φ² (b² − target var_u1) = target var_u1 → φ² = target var_u1 /(b² − target var_u1)
    den = b11 ** 2 - target * var_u1
    return float(np.sqrt(max(target * var_u1 / den, 1e-12)))


def simular(rng: np.random.Generator, F_obj: float, rho: float, nulo: bool):
    A, B0 = _estructura(rho, nulo)
    Tn = T + BURN
    eps = rng.standard_normal((Tn, N))
    m = 3 * Tn
    act = rng.random(m) < 0.85
    s = rng.standard_t(5, m) * np.sqrt(3.0 / 5.0) * np.sqrt(1.0 / 3.0) / np.sqrt(0.85) * act
    nu = s.reshape(Tn, 3).sum(1)
    z = _phi(F_obj, nulo, rho) * eps[:, 0] + nu
    U = eps @ B0.T
    Y = np.zeros((Tn, N))
    for t in range(P_DGP, Tn):
        Y[t] = A[0] @ Y[t - 1] + A[1] @ Y[t - 2] + U[t]
    return Y[BURN:], z[BURN:]


def _bb(rng, Y, z, h, B=199, bl=8):
    n = len(Y)
    th = np.empty(B)
    nb = int(np.ceil(n / bl))
    for b in range(B):
        st = rng.integers(0, n - bl + 1, size=nb)
        ix = (st[:, None] + np.arange(bl)[None, :]).ravel()[:n]
        try:
            r = H.proxy_svar(Y[ix], z[ix], P_EST, h, J_PRECIO, REF)
            th[b] = r["beta"]
        except np.linalg.LinAlgError:
            th[b] = np.nan
    return th


def rep(rng: np.random.Generator, F_obj: float, rho: float, nulo: bool, con_bb: bool) -> list[float]:
    Y, z = simular(rng, F_obj, rho, nulo)
    A, B0 = _estructura(rho, nulo)
    fila = []
    hacer_bb = con_bb and rng.random() < 0.2
    for h in HS:
        ver = H.theta_verdadero(A, B0[:, 0], h, J_PRECIO, REF)
        r = H.proxy_svar(Y, z, P_EST, h, J_PRECIO, REF)
        th = r["beta"]
        ths = [0.0, 0.0] if nulo else [0.0, ver]
        ps = []
        for t0 in ths:
            ps += [L.p_ar(r, t0), L.p_t(r, t0)]
        tipo = L.conjunto_ar(r)[0]
        if hacer_bb:
            bb = _bb(rng, Y, z, h)
            lo, hi = np.nanpercentile(bb, [2.5, 97.5])
            rb = [float(not (lo <= t0 <= hi)) for t0 in ths]
            rb = [0.01 if x else 1.0 for x in rb]
        else:
            rb = [np.nan, np.nan]
        # columnas por h: ver, est, p_ar0, p_t0, p_arT, p_tT, bb0, bbT, acotado, F
        F = float(L.f_robusto(r))
        fila += [ver, th, ps[0], ps[1], ps[2], ps[3], rb[0], rb[1], float(tipo == "acotado"), F]
    return fila


def main(R: int = 2000, jobs: int = 4, salida: Path | None = None) -> pd.DataFrame:
    filas = []
    t_ini = time.time()
    idx = 0
    for fz, Fo in FUERZA_F.items():
        for rn_, rho in PERSIST.items():
            idx += 1
            t0 = time.time()
            Mn = C.ejecutar(rep, (Fo, rho, True, True), R, K1, idx * 10 + 1, jobs)
            Ma = C.ejecutar(rep, (Fo, rho, False, True), R, K1, idx * 10 + 2, jobs)
            for j, h in enumerate(HS):
                o = j * 10
                sel = [o, o + 1, o + 2, o + 3, o + 4, o + 5, o + 6, o + 7]
                sn, sa = Mn[:, sel], Ma[:, sel]
                var = {"AR_delta_NeweyWest4": (2, 4), "Wald_delta": (3, 5)}
                ex = {"h": h, "fuerza": fz, "rho": rho, "F_robusta_media": float(Mn[:, o + 9].mean()), "AR_acotado_alt": float(Ma[:, o + 8].mean()),
                      "seg": round(time.time() - t0, 1)}
                filas += filas_por_p(f"{fz}|{rn_}|h{h}", var, sn, sa, col_est=1, col_ver=0, extra=ex)
                ok_n, ok_a = ~np.isnan(sn[:, 6]), ~np.isnan(sa[:, 6])
                if ok_n.sum() >= 100:
                    fb = filas_por_p(f"{fz}|{rn_}|h{h}", {"bootstrap_bloques_percentil (R_bb ≈ 20 %)": (6, 7)}, sn[ok_n], sa[ok_a], col_est=1, col_ver=0, extra=ex)
                    for f in fb:
                        f["banda_112"] = f["banda_112"] + " (R < 2.000: informativo)"
                        f["veredicto"] = "NO EVALUABLE (R < 2.000)" if f["R"] < 1000 else f["veredicto"]
                    filas += fb
            print(fz, rn_, [(f["variante"][:12], round(f["tamano_5pct"], 3), round(f["cobertura_alt"], 3)) for f in filas[-6:]], round(time.time() - t0, 1), flush=True)
    tabla = pd.DataFrame(filas)
    ar = tabla[(tabla.variante == "AR_delta_NeweyWest4") & (tabla.h == 8)]
    wd = tabla[(tabla.variante == "Wald_delta") & (tabla.h == 8) & (tabla.fuerza != "debil")]
    ver = {"AR_delta_NeweyWest4 (h = 8, todas las fuerzas)": "APTO" if (ar.veredicto == "APTO").all() else "NO APTO",
           "Wald_delta (h = 8, F >= 10)": "APTO" if (wd.veredicto == "APTO").all() else "NO APTO"}
    cond = "; ".join(f"AR: {r.escenario}: {r.fallos}" for r in ar[ar.veredicto != "APTO"].itertuples())
    cond2 = "; ".join(f"Wald: {r.escenario}: {r.fallos}" for r in wd[wd.veredicto != "APTO"].itertuples())
    cond = "; ".join(x for x in (cond, cond2) if x)
    veredicto = "; ".join(f"{k}: {v}" for k, v in ver.items())
    res = C.resultado_base(HERR, "¿Son válidas las bandas AR (robustas a proxy débil) del SVAR con proxy de E7-R2 con T = 108 y 6 variables?",
                           "simulados (sin datos reales ni muestra sellada)", f"VAR(2) de 6 variables, T = 108 (324 meses de sorpresa), h = 4 y 8; R = {R}",
                           "proxy-SVAR (Montiel Olea-Stock-Watson): AR por método delta, Wald y bootstrap de bloques")
    r0 = ar[ar.fuerza == "debil"].iloc[0]
    res["estimacion"] = {"tamano_AR_F3_h8": float(r0.tamano_5pct), "cobertura_AR_F3_h8": float(r0.cobertura_alt), "potencia_AR_F3_h8": float(r0.potencia)}
    res["diagnosticos"] = {"veredicto": veredicto, "veredicto_por_variante": ver, "condicion_en_que_falla": cond, "R": R, "segundos": round(time.time() - t_ini, 1)}
    informe = I.construir("SVAR con proxy y bandas robustas a la debilidad (E7-R2)", DGP, tabla, veredicto, cond,
                          ["El veredicto es sobre h = 8. El bootstrap de bloques se mide solo en ≈ 20 % de las réplicas (coste): es información, no decide.",
                           "θ está normalizado a un cambio unitario del tipo en el impacto; la verdad sale de las matrices del VAR verdadero."], V16,
                          ["escenario", "variante", "R", "tamano_5pct", "cobertura_nulo", "cobertura_alt", "potencia", "veredicto", "banda_112", "F_robusta_media"])
    C.escribir(HERR, res, tabla, informe, salida)
    return tabla


if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--R", type=int, default=2000)
    ap.add_argument("--jobs", type=int, default=4)
    a = ap.parse_args()
    print(main(a.R, a.jobs).to_string())
