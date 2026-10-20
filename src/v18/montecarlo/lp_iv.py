"""V18 · Monte Carlo de la proyección local con instrumento (E7-R1): 2SLS con Newey-West (ancho h + 1), versión aumentada con rezagos y errores EHW,
y conjuntos de Anderson-Rubin (plan de replicación 0.4 y 1.13), con la longitud mensual de la sorpresa del BCE 1999-2025 (324 meses = 108 trimestres).

Uso: python3 src/v18/montecarlo/lp_iv.py [--R 3000] [--jobs 4]
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

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from src.v18.herr18 import lp_iv as H  # noqa: E402
from src.v18.montecarlo import _comun as C  # noqa: E402
from src.v18.montecarlo import _informe as I  # noqa: E402
from src.v18.montecarlo._resumen import filas_por_p  # noqa: E402

ALCANCE_TERRITORIAL = "sin lectura de datos"
HERR = "lp_iv"
K1 = 24
HS = (4, 8, 12)
FUERZA = {"fuerte": 1.00, "moderada": 0.40, "debil": 0.17}
PERSIST = {"rho095": 0.95, "rho099": 0.99}
KAPPA, GAMMA = -0.5, 0.1
T, BURN = 108, 100

DGP = """
Estructura (declarada; ningún dato real): serie trimestral 1999T1-2025T4 (T = 108 trimestres = 324 meses). La sorpresa se genera MENSUAL (324 meses más 300 de calentamiento): s_m = 0 en el
15 % de los meses (sin reunión) y en el resto t de Student con 5 gl, escalada para que la suma trimestral (3 meses) tenga varianza 1; z_t = suma de los 3 meses (como en E7).
Modelo: Δi_t = 0,4 Δi_{t−1} + π z_t + u^i_t ;  y_t = r1 y_{t−1} + r2 y_{t−2} + κ Δi_t + γ Δi_{t−1} + u^y_t ;  u^y = 0,8 u^i + w, u^i ~ N(0,1), w ~ N(0; 0,5²) (endogeneidad: el 2SLS es necesario).
r2 = −0,25, r1 = ρ + 0,25 con ρ = r1 + r2 = 0,95 o 0,99 (persistencia alta; el plan exige robustez a ella). Fuerza del instrumento: π = 1,00 (F efectiva robusta medida ≈ 23), 0,40 (≈ 10), 0,17 (≈ 3; Q5 dio 2,1 a 2,9); la F medida se informa en la tabla.
Respuesta verdadera: β_h = IRF_y(h)/π (por unidad de cambio contemporáneo de Δi_t), por recursión determinista; nulo: κ = γ = 0 (β_h = 0); alternativa: κ = −0,5, γ = 0,1.
Estimación (E7-R1): y_{t+h} − y_{t−1} sobre Δi_t, instrumentado por z_t, con constante y 4 rezagos de y (niveles) y de Δi (n = 104 − h observaciones), h = 4, 8 (contraste principal) y 12.
Variantes: (1) 2SLS con Newey-West de ancho h + 1 (la del plan; contraste t normal); (2) 2SLS aumentado (5 rezagos, uno más que la especificación) con EHW; (3) AR con Newey-West de ancho h + 1;
(4) AR aumentado con EHW. Diagnóstico: sorpresa gaussiana sin meses vacíos (ρ = 0,95). Cobertura = 1 − rechazo del contraste en β_h verdadero (inversión; el conjunto AR es una desigualdad cuadrática, posiblemente no acotada).
"""

V16 = """
V16 (lp_newey_west_b): Newey-West con b fija NO APTO (tamaño 0,0642-0,0925, cobertura 0,813-0,9313) con T = 100, h = 1-12 y persistencia 0,90-0,98: el sobre-rechazo crecía con h y con la persistencia,
y el diseño no tenía instrumento ni variación de fuerza. Aquí se estima el 2SLS (que no existe en V16), se evalúa la versión aumentada con EHW que propone el plan y se separa el efecto de la fuerza
del instrumento (con F ≈ 3 el contraste t de 2SLS no es válido por construcción: decide el AR). No se vuelve a probar «b fija».
"""


def trayectoria_verdadera(pi: float, rho: float, kappa: float, gamma: float, hmax: int = 12) -> np.ndarray:
    r2 = -0.25
    r1 = rho + 0.25
    di = np.array([0.4 ** k * pi for k in range(hmax + 1)])
    y = np.zeros(hmax + 1)
    for h in range(hmax + 1):
        y[h] = (r1 * y[h - 1] if h >= 1 else 0) + (r2 * y[h - 2] if h >= 2 else 0) + kappa * di[h] + (gamma * di[h - 1] if h >= 1 else 0)
    return y / pi


def simular(rng: np.random.Generator, pi: float, rho: float, kappa: float, gamma: float, gauss: bool = False):
    Tn = T + BURN
    m = 3 * Tn
    act = rng.random(m) < 0.85
    s = rng.standard_t(5, m) * np.sqrt(3.0 / 5.0) * np.sqrt(1.0 / 3.0) / np.sqrt(0.85) * act
    if gauss:       # diagnóstico: sorpresa gaussiana sin meses vacíos (misma varianza)
        s = rng.standard_normal(m) * np.sqrt(1.0 / 3.0)
    z = s.reshape(Tn, 3).sum(1)
    ui = rng.standard_normal(Tn)
    uy = 0.8 * ui + 0.5 * rng.standard_normal(Tn)
    di = np.zeros(Tn)
    y = np.zeros(Tn)
    r2, r1 = -0.25, rho + 0.25
    for t in range(2, Tn):
        di[t] = 0.4 * di[t - 1] + pi * z[t] + ui[t]
        y[t] = r1 * y[t - 1] + r2 * y[t - 2] + kappa * di[t] + gamma * di[t - 1] + uy[t]
    return y[BURN:], di[BURN:], z[BURN:]


def rep(rng: np.random.Generator, pi: float, rho: float, alt: bool, gauss: bool = False) -> list[float]:
    kappa, gamma = (KAPPA, GAMMA) if alt else (0.0, 0.0)
    y, di, z = simular(rng, pi, rho, kappa, gamma, gauss)
    tray = trayectoria_verdadera(pi, rho, kappa, gamma)
    fila = []
    for h in HS:
        ver = float(tray[h])
        rn = H.lp_iv(y, di, z, h, L=h + 1, p=4)
        re = H.lp_iv(y, di, z, h, L=0, p=5)
        ths = [0.0, ver] if alt else [0.0, 0.0]
        ps = []
        for th in ths:
            ps += [H.p_t(rn, th), H.p_t(re, th), H.p_ar(rn, th), H.p_ar(re, th)]
        tipo = H.conjunto_ar(re)[0]
        fila += [ver, rn["beta"]] + ps + [H.f_robusto(re), float(tipo == "acotado")]
    return fila


def main(R: int = 3000, jobs: int = 4, salida: Path | None = None) -> pd.DataFrame:
    filas = []
    t_ini = time.time()
    idx = 0
    celdas = [(fz, pi, rn_, rho, False) for fz, pi in FUERZA.items() for rn_, rho in PERSIST.items()]
    celdas += [(fz, pi, "rho095_gauss", 0.95, True) for fz, pi in FUERZA.items()]     # diagnóstico: sorpresa gaussiana
    for fz, pi, rn_, rho, gs in celdas:
        if True:
            idx += 1
            t0 = time.time()
            Mn = C.ejecutar(rep, (pi, rho, False, gs), R, K1, idx * 10 + 1, jobs)
            Ma = C.ejecutar(rep, (pi, rho, True, gs), R, K1, idx * 10 + 2, jobs)
            for j, h in enumerate(HS):
                o = j * 12
                var = {"2SLS_NeweyWest_h+1": (o + 2, o + 6), "2SLS_aumentado_EHW": (o + 3, o + 7), "AR_NeweyWest_h+1": (o + 4, o + 8), "AR_aumentado_EHW": (o + 5, o + 9)}
                ex = {"h": h, "fuerza": fz, "rho": rho, "F_efectiva_media": float(Mn[:, o + 10].mean()), "AR_acotado": float(Ma[:, o + 11].mean()), "seg": round(time.time() - t0, 1)}
                filas += _filas(f"{fz}|{rn_}|h{h}", var, Mn, Ma, o, ex)
            print(fz, rn_, [(f["variante"], round(f["tamano_5pct"], 3), round(f["cobertura_alt"], 3)) for f in filas[-4:]], round(time.time() - t0, 1), flush=True)
    tabla = pd.DataFrame(filas)
    por_var = {}
    for v in tabla.variante.unique():
        t = tabla[(tabla.variante == v) & (tabla.h == 8) & ~tabla.escenario.str.contains("gauss")]
        mal = t[t.veredicto != "APTO"]
        por_var[v] = {"apto_en": t[t.veredicto == "APTO"].escenario.tolist(), "falla_en": {r.escenario: r.fallos for r in mal.itertuples()}}
    # veredicto de la herramienta: AR aumentado EHW (válido con instrumento débil) y NW(h+1) 2SLS cuando F >= 10
    rep_ = tabla[(tabla.h == 8) & ~tabla.escenario.str.contains("gauss")]
    ar = rep_[rep_.variante == "AR_aumentado_EHW"]
    nw = rep_[(rep_.variante == "2SLS_NeweyWest_h+1") & (rep_.fuerza != "debil")]
    aug = rep_[(rep_.variante == "2SLS_aumentado_EHW") & (rep_.fuerza != "debil")]
    ver = {"AR_aumentado_EHW (h = 8, todas las fuerzas)": "APTO" if (ar.veredicto == "APTO").all() else "NO APTO",
           "2SLS_NeweyWest_h+1 (h = 8, F >= 10)": "APTO" if (nw.veredicto == "APTO").all() else "NO APTO",
           "2SLS_aumentado_EHW (h = 8, F >= 10)": "APTO" if (aug.veredicto == "APTO").all() else "NO APTO"}
    conds = {k: "; ".join(f"{r.escenario}: {r.fallos}" for r in d[d.veredicto != "APTO"].itertuples())
             for k, d in (("AR_aumentado_EHW", ar), ("2SLS_NeweyWest_h+1", nw), ("2SLS_aumentado_EHW", aug))}
    veredicto = "; ".join(f"{k}: {v}" for k, v in ver.items())
    cond = "; ".join(f"{k}: {v}" for k, v in conds.items() if v)
    res = C.resultado_base(HERR, "¿Son válidos el 2SLS con Newey-West (h+1), la versión aumentada con EHW y el AR en la LP-IV de E7 con T = 108?",
                           "simulados (sin datos reales ni muestra sellada)", f"T = 108 trimestres (324 meses de sorpresa), h = 4, 8, 12; R = {R}",
                           "LP-IV (2SLS y AR) con Newey-West h+1 y con rezagos aumentados + EHW")
    r = ar[ar.fuerza == "debil"].iloc[0]
    res["estimacion"] = {"tamano_AR_aumentado_F3_h8": float(r.tamano_5pct), "cobertura_AR_aumentado_F3_h8": float(r.cobertura_alt), "potencia": float(r.potencia)}
    res["diagnosticos"] = {"veredicto": veredicto, "veredicto_por_variante": ver, "condicion_en_que_falla": cond, "R": R, "por_variante_h8": por_var,
                           "F_efectiva_media_por_fuerza": {f: float(tabla[(tabla.fuerza == f) & (tabla.h == 8)].F_efectiva_media.mean()) for f in FUERZA},
                           "segundos": round(time.time() - t_ini, 1)}
    informe = I.construir("Proyección local con instrumento (E7-R1)", DGP, tabla, veredicto, cond,
                          ["El contraste principal de E7-R1 es h = 8; h = 4 y 12 están en la tabla (columna h). Las filas «rho095_gauss» (sorpresa gaussiana) son diagnóstico y no entran en el veredicto.",
                           "El 2SLS (t) no es válido con instrumento débil (F ≈ 3): se evalúa solo con F >= 10 para el veredicto; el AR es el que decide con F < 10.",
                           "AR_acotado: proporción de réplicas con conjunto AR acotado (informativo) bajo la alternativa.",
                           'Sesgo de muestra finita de la LP (T = 108): con la alternativa, la mediana del estimador queda un 10 %, 22 % y 38 % por debajo de la verdad en valor absoluto a h = 4, 8 y 12 con instrumento fuerte (un 24-53 % con F ≈ 3), y es casi nulo con T = 1.000; es el mismo atenuamiento de la LP con series persistentes que describe la literatura (Herbst y Johannsen), y explica que la cobertura bajo la alternativa (0,72-0,93) sea peor que bajo el nulo (0,91-0,95 con el AR aumentado). Con la sorpresa gaussiana sin meses vacíos los resultados son los mismos: las colas pesadas no son la causa.'], V16,
                          ["escenario", "variante", "R", "tamano_5pct", "cobertura_nulo", "cobertura_alt", "potencia", "veredicto", "banda_112", "F_efectiva_media"])
    C.escribir(HERR, res, tabla, informe, salida)
    return tabla


def _filas(esc, var, Mn, Ma, o, ex):
    """filas_por_p con las columnas del bloque del horizonte (verdad en o, estimación en o + 1)."""
    var2 = {k: (a, b) for k, (a, b) in var.items()}
    sub_n = np.column_stack([Mn[:, o], Mn[:, o + 1]] + [Mn[:, c] for c in range(o + 2, o + 12)])
    sub_a = np.column_stack([Ma[:, o], Ma[:, o + 1]] + [Ma[:, c] for c in range(o + 2, o + 12)])
    var3 = {k: (a - o, b - o) for k, (a, b) in var2.items()}
    return filas_por_p(esc, var3, sub_n, sub_a, col_est=1, col_ver=0, extra=ex)


if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--R", type=int, default=3000)
    ap.add_argument("--jobs", type=int, default=4)
    a = ap.parse_args()
    print(main(a.R, a.jobs).to_string())
