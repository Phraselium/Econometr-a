"""V18 · Monte Carlo de SDID con inferencia de Conley-Taber (placebos) y con pocos tratados (plan de replicación 1.13; E2-A1, A2).

Uso: python3 src/v18/montecarlo/sdid_conley_taber.py [--R 2000] [--jobs 4]
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

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from src.v18.herr18 import sdid as S  # noqa: E402
from src.v18.montecarlo import _comun as C  # noqa: E402
from src.v18.montecarlo import _dgp_did as D  # noqa: E402
from src.v18.montecarlo import _informe as I  # noqa: E402
from src.v18.montecarlo._resumen import filas_por_p  # noqa: E402

ALCANCE_TERRITORIAL = "sin lectura de datos"
HERR = "sdid_conley_taber"
K1 = 23
TAU_ALT = -0.05
BPL = 199
# nombre: (tratados, controles, T, primer periodo posterior)
ESC = {
    "tratados_02": (2, 200, 17, 9),
    "tratados_05": (5, 200, 17, 9),
    "tratados_10": (10, 200, 17, 9),
    "tratados_25": (25, 200, 17, 9),
    "pais_vasco_A2": (8, 150, 40, 37),
    # diagnóstico (no entran en el veredicto): los tratados tienen una variabilidad temporal k veces la de los controles (no intercambiables)
    "tratados_10_variabilidad_x0.5 (diagnóstico)": (10, 200, 17, 9),
    "tratados_10_variabilidad_x2 (diagnóstico)": (10, 200, 17, 9),
}
ESCALA_TRATADOS = {"tratados_10_variabilidad_x0.5 (diagnóstico)": 0.5, "tratados_10_variabilidad_x2 (diagnóstico)": 2.0}

DGP = """
Estructura (declarada; ningún dato real). E2-A1 (zonas tensionadas de 2024 en Cataluña, Incasòl 2022T1-2026T1): T = 17 trimestres, entrada en el índice 9 (2024T2): 9 previos y 8 posteriores;
tratados 2, 5, 10 y 25 municipios y 200 controles (42 comarcas). E2-A2 (País Vasco, EMAL 2016T1-2025T4): T = 40, 3 posteriores (índice 37), 8 tratados y 150 controles.
Resultado: el de _dgp_did.py con la frecuencia trimestral (factores comunes AR(1) ρ 0,8 sd 0,03 con cargas N(1; 0,4) y N(0; 0,5), choque de comarca AR(1) ρ 0,6 sd 0,02, ruido AR(1) ρ 0,5
sd 0,05·exp(0,3 z_i − 0,045), tendencias propias d_i ~ N(0; 0,001)); efecto τ_i = τ(1 + 0,5 z'_i) con rampa 1 − exp(−(e + 1)/2). Los tratados se concentran en las 12 primeras comarcas (los
controles se reparten por todas): la asignación no depende de las cargas, de las tendencias ni de la varianza (intercambiabilidad ex ante necesaria para los placebos).
Estimador: SDID (Arkhangelsky et al. 2021): ω de unidad con intercepto y regularización ζ = (N_tr T_post)^(1/4) σ̂, λ de tiempo con regularización mínima, FISTA (80 y 60 iteraciones).
Inferencia: (1) Conley-Taber: 199 placebos que toman n_tr controles al azar como tratados y reestiman ω con los donantes restantes; p-valor simétrico P(|ĉ| >= |τ̂ − θ0|) (principal);
(2) SE de placebos con normal (Arkhangelsky); (3) Conley-Taber sobre el DiD simple (pesos uniformes; referencia). Diagnóstico de intercambiabilidad: tratados con variabilidad temporal 0,5 y 2 veces la de los controles. Medidas: tamaño = rechazo de θ = 0 con τ = 0; cobertura = 1 − rechazo de
θ = verdad (media de τ_i de los tratados en los periodos posteriores) con τ = −0,05 (inversión del contraste) y bajo el nulo; potencia = rechazo de θ = 0 con τ = −0,05.
Aproximación declarada: los pesos de tiempo λ no se reestiman en los placebos.
"""

V16 = """
V16 (sdid_conley_taber): Conley-Taber APTO solo en el escenario A (2 tratados, 1 provincia): tamaño 0,0575 y cobertura 0,943; la réplica B del mismo diseño dio 0,0650 y 0,9290, y agrupando
4.000 réplicas el tamaño fue 0,0612: «en el límite», no holgado. El Webb de la alternativa degeneraba (tamaño 0,78 con un cluster tratado). Aquí se mide el barrido de n_tr = 2, 5, 10, 25 (el
criterio no se aplica a un solo tamaño) y el diseño de País Vasco (T = 40, 3 posteriores), con R = 2.000 y 199 placebos por réplica. No se usa Webb (con pocos tratados no es una opción).
"""


@functools.lru_cache(maxsize=None)
def _d(nombre: str):
    n1, n0, T, g = ESC[nombre]
    return D._municipal("sdid_" + nombre, {g: n1}, n0, T, D.TRIM)


def rep(rng: np.random.Generator, nombre: str, tau: float) -> list[float]:
    d = _d(nombre)
    n1, n0, T, g = ESC[nombre]
    Y, efecto = D.simular(d, rng, tau)
    tr = d.cohorte >= 0
    k = ESCALA_TRATADOS.get(nombre, 1.0)
    if k != 1.0:       # diagnóstico: se escala la variación temporal propia de los tratados (sin el efecto)
        Y0 = Y[tr] - efecto[tr]
        m0 = Y0.mean(1, keepdims=True)
        Y = Y.copy()
        Y[tr] = m0 + k * (Y0 - m0) + efecto[tr]
    ver = float(efecto[tr][:, g:].mean())
    est = S.sdid(Y[tr][:, :g], Y[tr][:, g:], Y[~tr][:, :g], Y[~tr][:, g:])
    pl = S.placebos(Y[~tr][:, :g], Y[~tr][:, g:], est["lambda"], est["zeta"], n1, rng, BPL)
    tau_h = est["tau"]
    did = float(Y[tr][:, g:].mean() - Y[tr][:, :g].mean() - (Y[~tr][:, g:].mean() - Y[~tr][:, :g].mean()))
    ths = [0.0] if tau == 0 else [0.0, ver]
    fila = [ver, tau_h]
    for th in ths:
        fila += [S.p_placebo(tau_h, pl["sdid"], th), S.p_normal_placebo(tau_h, pl["sdid"], th), S.p_placebo(did, pl["did"], th)]
    if tau == 0:
        fila = fila + fila[2:]
    return fila + [did]


def main(R: int = 2000, jobs: int = 4, escenarios: list[str] | None = None, salida: Path | None = None) -> pd.DataFrame:
    filas = []
    t_ini = time.time()
    for i, nom in enumerate(escenarios or list(ESC)):
        t0 = time.time()
        Mn = C.ejecutar(rep, (nom, 0.0), R, K1, i * 10 + 1, jobs)
        Ma = C.ejecutar(rep, (nom, TAU_ALT), R, K1, i * 10 + 2, jobs)
        var = {"conley_taber_sdid": (2, 5), "sdid_placebo_normal": (3, 6), "conley_taber_did_simple (referencia)": (4, 7)}
        n1, n0, T, g = ESC[nom]
        ex = {"tratados": n1, "controles": n0, "T": T, "posteriores": T - g, "placebos": BPL, "seg": round(time.time() - t0, 1)}
        filas += filas_por_p(nom, var, Mn, Ma, extra=ex)
        print(nom, [(f["variante"], round(f["tamano_5pct"], 4), round(f["cobertura_alt"], 4)) for f in filas[-3:]], ex["seg"], flush=True)
    tabla = pd.DataFrame(filas)
    prin = tabla[(tabla.variante == "conley_taber_sdid") & ~tabla.escenario.str.contains("diagnóstico")]
    mal = prin[prin.veredicto != "APTO"]
    ok = prin[prin.veredicto == "APTO"].escenario.tolist()
    if len(mal) == 0:
        veredicto, cond = "APTO", ""
    else:
        cond = "; ".join(f"{r.escenario} ({r.fallos})" for r in mal.itertuples())
        veredicto = ("APTO CONDICIONADO (solo en: " + ", ".join(ok) + ")") if ok else "NO APTO"
    res = C.resultado_base(HERR, "¿Es válida la inferencia de Conley-Taber con SDID y pocos tratados (2 a 25) en los diseños de zonas tensionadas?",
                           "simulados (sin datos reales ni muestra sellada)", f"2-25 tratados y 150-200 controles; T = 17 y 40; R = {R}",
                           "SDID (Arkhangelsky et al.) + placebos de Conley-Taber (199)")
    r = tabla[(tabla.escenario == "tratados_10") & (tabla.variante == "conley_taber_sdid")]
    r = (r if len(r) else prin).iloc[0]
    res["estimacion"] = {"tamano_10_tratados": float(r.tamano_5pct), "cobertura_nulo": float(r.cobertura_nulo), "cobertura_alt": float(r.cobertura_alt),
                         "potencia": float(r.potencia), "sesgo": float(r.sesgo), "rmse": float(r.rmse)}
    res["diagnosticos"] = {"veredicto": veredicto, "condicion_en_que_falla": cond, "variante_principal": "conley_taber_sdid",
                           "por_escenario": {x.escenario: x.veredicto for x in prin.itertuples()}, "R": R, "placebos": BPL, "segundos": round(time.time() - t_ini, 1)}
    informe = I.construir("SDID y Conley-Taber con pocos tratados", DGP, tabla, veredicto, cond,
                          ["Principal: Conley-Taber sobre SDID. SDID con normal de placebos y Conley-Taber sobre DiD simple son referencia. Las filas «(diagnóstico)» rompen a propósito la intercambiabilidad entre tratados y controles (no deciden el veredicto): muestran la condición en que los placebos dejan de valer.",
                           f"R = {R} réplicas por escenario y por bloque; 199 placebos por réplica (p-valor mínimo 0,005)."], V16)
    C.escribir(HERR, res, tabla, informe, salida)
    return tabla


if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--R", type=int, default=2000)
    ap.add_argument("--jobs", type=int, default=4)
    a = ap.parse_args()
    print(main(a.R, a.jobs).to_string())
