"""V18 · Monte Carlo de la inferencia por aleatorización (permutaciones) en E2 (asignación entre municipios) y E8 (calendario entre CCAA) (plan, 1.13).

Uso: python3 src/v18/montecarlo/aleatorizacion.py [--R 2000] [--jobs 4]
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
from src.v18.herr18 import aleatorizacion as H  # noqa: E402
from src.v18.herr18 import dcdh as DH  # noqa: E402
from src.v18.montecarlo import _comun as C  # noqa: E402
from src.v18.montecarlo import _dgp_did as D  # noqa: E402
from src.v18.montecarlo import _dgp_itp as P  # noqa: E402
from src.v18.montecarlo import _informe as I  # noqa: E402
from src.v18.montecarlo._resumen import filas_por_p  # noqa: E402

ALCANCE_TERRITORIAL = "sin lectura de datos"
HERR = "aleatorizacion"
K1 = 29
TAU_ALT, BETA_ALT = -0.05, -0.03
BPERM = 499
E2 = ("cat_trim_M", "pocos_tratados")
E8 = ("desigual", "equilibrado")

DGP = """
Dos familias, con la estructura de _dgp_did.py (E2) y _dgp_itp.py (E8); todo simulado.
E2 (topes en Cataluña, R1 / A1): municipio-trimestre, T = 13, entrada en el índice 7; cat_trim_M = 100 tratados y 200 controles; pocos_tratados = 10 y 150; 42 comarcas, tratados concentrados en las 12 primeras.
Resultado: factores comunes AR(1) con cargas heterogéneas, choque de comarca AR(1) (ρ 0,6, sd 0,02), ruido AR(1) heterocedástico, efecto τ_i = τ (1 + 0,5 z_i) con rampa (nulo 0; alternativa τ = −0,05). Estadístico:
ATT = media(Δ_i | tratados) − media(Δ_i | controles), Δ_i = media de los periodos posteriores − media de los previos; verdad = media de los efectos de los tratados en los periodos posteriores.
Contrastes (499 permutaciones + identidad): (1) permutación de la asignación ENTRE TODOS los municipios, estadístico estudentizado (Welch) [la del plan, principal]; (2) la misma con el coeficiente a secas;
(3) permutación DENTRO de cada comarca (conserva los tratados por comarca) estudentizada; (4) dentro de comarca con el coeficiente.
E8 (ITP, R1/R2): 36 provincias en 8 CCAA, T = 24, calendarios de dosis como en dcdh_aleatorizacion («desigual» y «equilibrado»), nulo β = 0 y alternativa β = −0,03 por punto con efecto CONSTANTE (nivel de la dosis).
Estadístico: coeficiente de MCO de dos vías sobre la dosis con EE agrupado por CCAA; permutación de los calendarios completos entre las 8 CCAA (499 + identidad), estudentizado (principal) o no.
Cobertura = 1 − rechazo del contraste en θ = verdad (inversión del contraste, efecto constante impuesto); tamaño = rechazo de θ = 0 con el efecto nulo; potencia = rechazo de θ = 0 con la alternativa.
"""

V16 = """
V16 (dcdh_aleatorizacion, NO APTO): tamaño 0,0775 y cobertura 0,967 con 11 clusters y un estadístico sin estudentizar. La aleatorización de V18 se mide aquí en sus dos usos (asignación entre municipios en E2 y
calendarios entre CCAA en E8) y con dos estadísticos, para aislar qué cambia el tamaño: estudentizar (en estos procesos no lo cambia de forma apreciable) y permutar dentro de la comarca (lo acerca al nominal cuando
los tratados se concentran en pocas comarcas con choques propios, que es lo que el plan no controla cuando permuta entre todos los municipios). El 0,0775 de V16 no se reproduce con estas estructuras.
"""


@functools.lru_cache(maxsize=None)
def _d(nombre):
    return D.diseno(nombre)


def rep_e2(rng: np.random.Generator, nombre: str, tau: float) -> list[float]:
    d = _d(nombre)
    Y, efecto = D.simular(d, rng, tau)
    g = int(d.cohorte[d.cohorte >= 0][0])
    lab = d.cohorte >= 0
    dl = H.delta_unidad(Y, g)
    ver = float(efecto[lab][:, g:].mean())
    a, _ = H.did_welch(dl, lab)
    pi = H.etiquetas_individual(rng, lab, BPERM)
    pe = H.etiquetas_estrato(rng, lab, d.cl_grueso, BPERM)
    ths = [0.0] if tau == 0 else [0.0, ver]
    out = []
    for th in ths:
        out += [H.p_did(dl, lab, th, pi, True), H.p_did(dl, lab, th, pi, False), H.p_did(dl, lab, th, pe, True), H.p_did(dl, lab, th, pe, False)]
    if tau == 0:
        out = out + out
    return [ver, float(a)] + out


def rep_e8(rng: np.random.Generator, esc: str, beta: float) -> list[float]:
    y, Dc, bi, cl = P.simular(rng, esc, beta, het=False)
    ver = float(beta)
    M = (cl[:, None] == np.arange(8)[None, :]).astype(float)
    b, _ = H.twfe_dosis(y, Dc[cl], M)
    perms = DH.permutaciones(rng, 8, BPERM)
    ths = [0.0] if beta == 0 else [0.0, ver]
    out = []
    for th in ths:
        out += [H.p_calendarios(y, Dc, cl, th, perms, True), H.p_calendarios(y, Dc, cl, th, perms, False)]
    if beta == 0:
        out = out + out
    return [ver, float(b)] + out


def main(R: int = 2000, jobs: int = 4, salida: Path | None = None) -> pd.DataFrame:
    filas = []
    t_ini = time.time()
    for i, nom in enumerate(E2):
        t0 = time.time()
        Mn = C.ejecutar(rep_e2, (nom, 0.0), R, K1, i * 10 + 1, jobs)
        Ma = C.ejecutar(rep_e2, (nom, TAU_ALT), R, K1, i * 10 + 2, jobs)
        var = {"permuta_entre_municipios_estudentizada (plan)": (2, 6), "permuta_entre_municipios_coeficiente": (3, 7), "permuta_dentro_de_comarca_estudentizada": (4, 8),
               "permuta_dentro_de_comarca_coeficiente": (5, 9)}
        d = _d(nom)
        ex = {"familia": "E2", "tratados": int((d.cohorte >= 0).sum()), "controles": int((d.cohorte < 0).sum()), "permutaciones": BPERM, "seg": round(time.time() - t0, 1)}
        filas += filas_por_p("E2_" + nom, var, Mn, Ma, extra=ex)
        print(nom, [(f["variante"][:30], round(f["tamano_5pct"], 4), round(f["cobertura_alt"], 4)) for f in filas[-4:]], ex["seg"], flush=True)
    for i, esc in enumerate(E8):
        t0 = time.time()
        Mn = C.ejecutar(rep_e8, (esc, 0.0), R, K1, 100 + i * 10 + 1, jobs)
        Ma = C.ejecutar(rep_e8, (esc, BETA_ALT), R, K1, 100 + i * 10 + 2, jobs)
        var = {"calendarios_entre_CCAA_estudentizada (plan)": (2, 4), "calendarios_entre_CCAA_coeficiente": (3, 5)}
        ex = {"familia": "E8", "tratados": 36, "controles": 0, "clusters": 8, "permutaciones": BPERM, "seg": round(time.time() - t0, 1)}
        filas += filas_por_p("E8_" + esc, var, Mn, Ma, extra=ex)
        print(esc, [(f["variante"][:30], round(f["tamano_5pct"], 4), round(f["cobertura_alt"], 4)) for f in filas[-2:]], ex["seg"], flush=True)
    tabla = pd.DataFrame(filas)
    prin = tabla[tabla.variante.str.contains("(plan)", regex=False)]
    mal = prin[prin.veredicto != "APTO"]
    ok = prin[prin.veredicto == "APTO"].escenario.tolist()
    if len(mal) == 0:
        veredicto, cond = "APTO", ""
    else:
        cond = "; ".join(f"{r.escenario} ({r.fallos})" for r in mal.itertuples())
        veredicto = ("APTO CONDICIONADO (solo en: " + ", ".join(ok) + ")") if ok else "NO APTO"
    alt = tabla[tabla.variante.str.contains("dentro_de_comarca_estudentizada")]
    res = C.resultado_base(HERR, "¿Es válida la inferencia por aleatorización (permutaciones del calendario o de la asignación) en E2 y E8?",
                           "simulados (sin datos reales ni muestra sellada)", f"E2: 100/200 y 10/150 municipios x 13 trimestres; E8: 36 provincias en 8 CCAA x 24 trimestres; R = {R}",
                           "Aleatorización de Fisher estudentizada: asignación entre municipios, dentro de comarca y calendarios entre CCAA")
    p = prin[prin.escenario == "E2_cat_trim_M"].iloc[0]
    res["estimacion"] = {"tamano_E2_cat_trim_M_entre_municipios": float(p.tamano_5pct), "cobertura_alt": float(p.cobertura_alt), "potencia": float(p.potencia)}
    res["diagnosticos"] = {"veredicto": veredicto, "condicion_en_que_falla": cond, "variantes_principales": "estudentizadas del plan (entre municipios en E2; entre CCAA en E8)",
                           "por_escenario": {r.escenario: r.veredicto for r in prin.itertuples()},
                           "alternativa_dentro_de_comarca": {r.escenario: r.veredicto for r in alt.itertuples()}, "R": R, "segundos": round(time.time() - t_ini, 1)}
    informe = I.construir("Inferencia por aleatorización (permutaciones)", DGP, tabla, veredicto, cond,
                          ["Las variantes marcadas (plan) deciden el veredicto; las demás aíslan la causa (estudentización, permutación dentro de comarca).",
                           "E8: el efecto de la alternativa es constante (efecto de nivel de la dosis), porque el contraste de Fisher impone un efecto constante."], V16,
                          ["escenario", "variante", "R", "tamano_5pct", "cobertura_nulo", "cobertura_alt", "potencia", "veredicto", "banda_112"])
    C.escribir(HERR, res, tabla, informe, salida)
    return tabla


if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--R", type=int, default=2000)
    ap.add_argument("--jobs", type=int, default=4)
    a = ap.parse_args()
    print(main(a.R, a.jobs).to_string())
