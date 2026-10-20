"""V18 · Monte Carlo del metaanálisis bayesiano de efectos aleatorios con 2 a 10 estudios (plan, sección 3; adenda 1.9): cobertura de μ y de τ
y las tres variantes de prior de μ.

Uso: python3 src/v18/montecarlo/meta_bayes.py [--R 2000] [--jobs 4]
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
from src.v18.herr18 import meta_bayes as H  # noqa: E402
from src.v18.montecarlo import _comun as C  # noqa: E402
from src.v18.montecarlo import _informe as I  # noqa: E402

ALCANCE_TERRITORIAL = "sin lectura de datos"
HERR = "meta_bayes"
K1 = 26
KS = (2, 3, 4, 6, 8, 10)
S = 1.0         # unidad: s_f = 1 (el problema es invariante a la escala)
# nombre: (μ verdadero o None si se sortea del prior, τ verdadero o None, entra en el veredicto)
ESC = {
    "calibracion_prior": (None, None, True),
    "nulo_hom": (0.0, 0.05, False),
    "nulo_het": (0.0, 0.25, True),
    "efecto_hom": (0.4, 0.05, False),
    "efecto_het": (0.4, 0.25, True),
    "efecto_grande": (1.0, 0.25, False),
}
VARIANTES = {"prior_mu_s (principal)": (1.0, "seminormal"), "prior_mu_2s": (2.0, "seminormal"), "prior_mu_s/2": (0.5, "seminormal"),
             "tau_semicauchy (sensibilidad)": (1.0, "semicauchy")}

DGP = """
Estructura (declarada; ningún dato real): K = 2, 3, 4, 6, 8 y 10 estudios en la misma unidad. Todo en unidades de s_f (el modelo es invariante a la escala; s_f = 1).
Errores típicos: se_k = s_f · exp(U(ln 0,05; ln 0,4)) (de 0,05 a 0,4 veces la escala del factor, el rango de las fichas de V18). Modelo: y_k ~ N(θ_k, se_k²), θ_k ~ N(μ, τ²).
Verdades: «calibración» (μ ~ N(0, s_f²) y τ ~ semi-normal(0, (s_f/2)²): los priors del plan; el intervalo central al 95 % debe cubrir 95 % si la cuadratura es exacta); y verdades fijas:
nulo_hom (μ = 0, τ = 0,05), nulo_het (μ = 0, τ = 0,25), efecto_hom (μ = 0,4, τ = 0,05), efecto_het (μ = 0,4, τ = 0,25) y efecto_grande (μ = 1, τ = 0,25).
Estimador: posterior por cuadratura (μ marginalizado, τ en rejilla de 400 puntos hasta 8 s_f). Prior de μ: N(0, s_f²) (principal), N(0, (2 s_f)²) y N(0, (s_f/2)²) (las tres de la adenda 1.9);
prior de τ: semi-normal(0, (s_f/2)²) (semi-Cauchy(0, s_f/2) como sensibilidad). Con K = 2: efecto fijo (media ponderada por la inversa de la varianza, IC95 normal, sin τ), como dice el plan.
Medidas: cobertura del intervalo de credibilidad equicola al 95 % de μ y de τ; «tamaño» = rechazo de μ = μ_verdadero por el intervalo = 1 − cobertura de μ (con μ = 0 es la probabilidad de que el intervalo excluya el cero);
potencia = probabilidad de que el intervalo excluya 0; concordancia de la decisión entre las tres variantes de prior (signo de la mediana y exclusión de 0), que es la regla de publicación de la adenda 1.9.
"""

V16 = """
V16 (bayes_jerarquico): NO APTO con otra especificación (modelo normal-normal sección ⊂ municipio ⊂ provincia con 3 niveles): cobertura de μ 0,972-0,976 con verdades de «no nulo» y «homogéneo» y 0,985 en la sección; el intervalo era
conservador (cubría de más), no insuficiente. Aquí el modelo es el nuevo (un nivel: estudios), con K de 2 a 10 y las tres variantes de prior de la adenda; se mide la cobertura de μ y de τ por separado y se informa de si el fallo es por exceso
(conservador) o por defecto. No se asume que un prior propio centrado en 0 con verdad en 0 cubra el 95 %: la cobertura bajo una verdad fija depende del prior, y por eso se miden también las verdades fijas y no solo la calibración.
"""


def _generar(rng: np.random.Generator, R: int, K: int, mu_v, tau_v):
    se = S * np.exp(rng.uniform(np.log(0.05), np.log(0.4), (R, K)))
    if mu_v is None:
        mu = rng.normal(0, S, R)
        tau = np.abs(rng.normal(0, S / 2, R))
    else:
        mu = np.full(R, mu_v)
        tau = np.full(R, tau_v)
    theta = mu[:, None] + tau[:, None] * rng.standard_normal((R, K))
    y = theta + se * rng.standard_normal((R, K))
    return y, se, mu, tau


def celda(esc: str, K: int, R: int, k2: int) -> list[dict]:
    mu_v, tau_v, _ = ESC[esc]
    rng = np.random.default_rng(np.random.SeedSequence([C.SEMILLA, K1, k2]))
    y, se, mu, tau = _generar(rng, R, K, mu_v, tau_v)
    filas = []
    dec = {}
    if K == 2:
        e = H.efecto_fijo(y, se)
        cov = float(np.mean((e["mu_lo"] <= mu) & (mu <= e["mu_hi"])))
        # el efecto fijo estima la media ponderada de los θ_k; con heterogeneidad no es μ: se mide frente a μ (la afirmación del plan)
        filas.append(_fila(esc, K, "efecto_fijo (K < 3)", R, cov, None, float(np.mean((e["mu_lo"] > 0) | (e["mu_hi"] < 0))),
                           float(np.mean(e["mu_hi"] - e["mu_lo"])), float(np.mean(e["mu_med"] - mu)), float(np.sqrt(np.mean((e["mu_med"] - mu) ** 2)))))
        return filas
    for nom, (mult, tt) in VARIANTES.items():
        P = {k: [] for k in ("mu_lo", "mu_med", "mu_hi", "tau_lo", "tau_med", "tau_hi")}
        for a in range(0, R, 250):
            b = min(R, a + 250)
            r = H.posterior(y[a:b], se[a:b], S, mult, tt)
            for k in P:
                P[k].append(r[k])
        P = {k: np.concatenate(v) for k, v in P.items()}
        cov_mu = float(np.mean((P["mu_lo"] <= mu) & (mu <= P["mu_hi"])))
        cov_tau = float(np.mean((P["tau_lo"] <= tau) & (tau <= P["tau_hi"])))
        excl = (P["mu_lo"] > 0) | (P["mu_hi"] < 0)
        dec[nom] = (np.sign(P["mu_med"]), excl)
        filas.append(_fila(esc, K, nom, R, cov_mu, cov_tau, float(excl.mean()), float(np.mean(P["mu_hi"] - P["mu_lo"])), float(np.mean(P["mu_med"] - mu)),
                           float(np.sqrt(np.mean((P["mu_med"] - mu) ** 2)))))
    ks = ["prior_mu_s (principal)", "prior_mu_2s", "prior_mu_s/2"]
    sig = [dec[k][0] for k in ks]
    ex = [dec[k][1] for k in ks]
    coincide = (sig[0] == sig[1]) & (sig[1] == sig[2]) & (ex[0] == ex[1]) & (ex[1] == ex[2])
    publica = coincide & ex[0]
    for f in filas:
        f["concordancia_3_priors"] = float(coincide.mean())
        f["publica_magnitud (excluye 0 en las 3)"] = float(publica.mean())
    return filas


def _fila(esc, K, var, R, cov_mu, cov_tau, excl, ancho, sesgo, rmse) -> dict:
    tam = 1 - cov_mu
    cobs = [cov_mu] + ([cov_tau] if cov_tau is not None else [])
    b = C.banda_encargo(tam, cobs, R)
    # para esta herramienta el «tamaño» es 1 − cobertura de μ: el criterio de tamaño [0,03; 0,08] equivale a cobertura de μ en [0,92; 0,97]
    return {"escenario": esc, "K": K, "variante": var, "R": R, "cobertura_mu": cov_mu, "cobertura_tau": cov_tau, "tamano_5pct": tam, "se_mc_tamano": C.mc_se(tam, R),
            "excluye_cero": excl, "ancho_mu": ancho, "sesgo": sesgo, "rmse": rmse, "veredicto": "APTO" if b["apto"] else "NO APTO",
            "fallos": " / ".join(b["fallos"]), "banda_112": C.banda_112(tam, cobs, R),
            "direccion": "" if b["apto"] else ("conservador" if cov_mu > 0.97 else ("insuficiente" if cov_mu < 0.92 else "τ fuera de banda"))}


def _tarea(esc, K, R, k2):
    return celda(esc, K, R, k2)


def main(R: int = 2000, jobs: int = 4, salida: Path | None = None) -> pd.DataFrame:
    from joblib import Parallel, delayed
    t0 = time.time()
    tareas = [(esc, K, R, i * 100 + j) for i, esc in enumerate(ESC) for j, K in enumerate(KS)]
    sal = Parallel(n_jobs=jobs)(delayed(_tarea)(*t) for t in tareas)
    tabla = pd.DataFrame([f for s in sal for f in s])
    tabla["entra_en_veredicto"] = tabla.escenario.map(lambda e: ESC[e][2])
    por = {}
    for v in VARIANTES:
        t = tabla[(tabla.variante == v) & tabla.entra_en_veredicto]
        por[v] = {"apto": bool((t.veredicto == "APTO").all()), "falla_en": [f"{r.escenario}|K{r.K}: μ {r.cobertura_mu:.3f}, τ {r.cobertura_tau:.3f} ({r.direccion})"
                                                                         for r in t[t.veredicto != "APTO"].itertuples()]}
    fe = tabla[(tabla.variante == "efecto_fijo (K < 3)") & tabla.entra_en_veredicto]
    por["efecto_fijo (K < 3)"] = {"apto": bool((fe.veredicto == "APTO").all()), "falla_en": [f"{r.escenario}|K2: μ {r.cobertura_mu:.3f} ({r.direccion})" for r in fe[fe.veredicto != "APTO"].itertuples()]}
    princ = por["prior_mu_s (principal)"]
    veredicto = "APTO" if princ["apto"] and por["efecto_fijo (K < 3)"]["apto"] else "NO APTO"
    if veredicto != "APTO":
        partes = [f"{k}: " + "; ".join(v["falla_en"][:6]) + (" ..." if len(v["falla_en"]) > 6 else "") for k, v in por.items() if not v["apto"]]
        cond = " | ".join(partes)
    else:
        cond = ""
    res = C.resultado_base(HERR, "¿Cubren los intervalos de credibilidad de μ y de τ del metaanálisis bayesiano de efectos aleatorios con 2 a 10 estudios?",
                           "simulados (sin datos reales ni muestra sellada)", f"K = 2 a 10 estudios; R = {R} por celda",
                           "metaanálisis bayesiano normal-normal por cuadratura (3 priors de μ; τ semi-normal y semi-Cauchy); efecto fijo con K < 3")
    p = tabla[(tabla.variante == "prior_mu_s (principal)") & (tabla.escenario == "calibracion_prior") & (tabla.K == 6)].iloc[0]
    res["estimacion"] = {"cobertura_mu_calibracion_K6": float(p.cobertura_mu), "cobertura_tau_calibracion_K6": float(p.cobertura_tau)}
    res["diagnosticos"] = {"veredicto": veredicto, "por_variante": por, "condicion_en_que_falla": cond, "R": R, "segundos": round(time.time() - t0, 1),
                           "nota_tamano": "tamaño = 1 − cobertura de μ (rechazo del valor verdadero por el intervalo)"}
    informe = I.construir("Metaanálisis bayesiano de efectos aleatorios (2 a 10 estudios)", DGP, tabla, veredicto, cond,
                          ["Escenarios que entran en el veredicto: calibración, nulo_het y efecto_het (los que representan el uso del plan: factores con efecto cercano a 0 o moderado y heterogeneidad); los demás son diagnóstico.",
                           "Con K = 2 se usa el efecto fijo; su cobertura frente a μ cae con heterogeneidad (el efecto fijo estima la media ponderada de los θ_k).",
                           "τ = 0,05 y 0,25 son verdades fijas: la cobertura de τ de un intervalo equicola cerca del borde 0 es baja por construcción."], V16,
                          ["escenario", "K", "variante", "R", "cobertura_mu", "cobertura_tau", "excluye_cero", "ancho_mu", "veredicto", "banda_112", "direccion"])
    C.escribir(HERR, res, tabla, informe, salida)
    return tabla


if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--R", type=int, default=2000)
    ap.add_argument("--jobs", type=int, default=4)
    a = ap.parse_args()
    print(main(a.R, a.jobs).to_string())
