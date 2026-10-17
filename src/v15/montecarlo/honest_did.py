"""V15 fase 4.1 · Honest DiD (Rambachan y Roth, magnitudes relativas M̄): revalidación de la implementación propia de V9 (src/v9/herramientas.py).

Proceso generador declarado en docs/v15/validacion_montecarlo/honest_did.md ANTES de simular (el script lo escribe primero).
Uso: python src/v15/montecarlo/honest_did.py [--R 2000] [--R_info 500] [--jobs 4]
"""
from __future__ import annotations

import argparse
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd
from joblib import Parallel, delayed

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from src.v15.montecarlo import _comun_v15 as C  # noqa: E402
from src.v15.montecarlo import _comun_panel_v15 as Pn  # noqa: E402
from src.v9 import herramientas as H  # noqa: E402  (implementación V9; por paquete, para no chocar con otros «herramientas»)

HERR, K = "honest_did", 2
SD_E, PEND, TAU_REF, TAU_MDE = 0.05, 0.004, -0.05, -0.022
REF = 6                       # índice del trimestre de referencia e = -1 (2023T4)
PRE_E = list(range(-7, -1))   # e = -7..-2
POST_E = list(range(0, 9))    # e = 0..8
ESC = {  # nombre: (Mbar, pendiente del sesgo, tendencias paralelas exactas en el proceso, rol)
    "A_PT_exacta_M0": (0.0, 0.0, True, "verdad"),
    "B_frontera_lineal_M1": (1.0, PEND, True, "verdad"),
    "C_sin_tendencia_M1": (1.0, 0.0, True, "info"),
    "D_tendencia_con_M0": (0.0, PEND, True, "info"),
    "E_factores_M0": (0.0, 0.0, False, "info"),
    "F_factores_M1": (1.0, 0.0, False, "info"),
}

DGP = """# honest_did · Honest DiD (Rambachan-Roth, magnitudes relativas) en el estudio de eventos de H1

Herramienta de V15 (preregistro_v15.md sección 6: «implementación propia de V9, con tamaño del 7,3 % en 400 réplicas: se revalida o se sustituye»; adenda 1, punto 13). Código: `src/v15/montecarlo/honest_did.py`, que llama a la implementación de V9 (`honest_rr` y sus piezas, `src/v9/herramientas.py`) sin modificarla. Semilla `SeedSequence([20261010, 2, escenario*10+etapa]).spawn(R)`.

## Proceso generador (declarado antes de simular)
- **Panel (estructura de H1, escenario S1 de sdid_placebo_h1h2):** 124 tratados y 74 donantes nunca tratados (códigos reales, centroides reales), 7 trimestres previos (2022T2-2023T4) y 9 posteriores (2024T1-2026T1), mismo proceso generador que `sdid_placebo_h1h2` (factores comunes AR(1), campo espacial, AR(1) ρ = 0,5, sd_e = 0,05 heterogénea). La referencia del estudio de eventos es e = −1 (2023T4).
- **Estudio de eventos estimado dentro de cada réplica:** b_e = (media de tratados − media de donantes) en e, menos la misma diferencia en e = −1; e = −7..−2 (6 previos) y 0..8 (9 posteriores). Covarianza estimada con varianzas robustas por unidad (varianza de las medias de cada grupo): el error de estimación de la covarianza entra en el tamaño.
- **Tendencias paralelas exactas (escenarios A-D):** para aislar el contraste de Honest DiD del sesgo de composición, el proceso de estos escenarios no lleva tendencias propias ni cargas heterogéneas de los factores (solo efectos de tiempo comunes, campo espacial de 25 km y AR(1) idiosincrásico heterocedástico). Los escenarios E y F usan el proceso completo de H1 (factores con cargas heterogéneas y tendencias propias d_i ~ N(0; 0,002²)), en el que las tendencias paralelas solo se cumplen en esperanza (información).
- **Sesgo de tendencias paralelas simulado:** a los tratados se les suma δ_e = s·(e + 1) en todos los trimestres (tendencia diferencial lineal; δ_{−1} = 0). Con s = 0,004 por trimestre las diferencias posteriores igualan a las previas, es decir, el caso frontera de Δ^RM(M̄ = 1).
- **Parámetro:** θ = ATT medio de los 9 trimestres posteriores (media muestral de tau_i, con tau_i = tau(1 + 0,5 z_i)).
- **Escenarios:** A (M̄ = 0, tendencias paralelas exactas), B (M̄ = 1, tendencia lineal frontera; es el umbral de C3 de H1), y de información: C (M̄ = 1, sin tendencia: el contraste es conservador por construcción), D (M̄ = 0 con tendencia: la hipótesis es falsa, mide el sobre-rechazo si se ignora el sesgo), E y F (proceso completo de H1 con M̄ = 0 y M̄ = 1).
- **Medidas:** tamaño = rechazo de θ = 0 con tau = 0; cobertura = 1 − rechazo de θ = θ_verdadero con tau = −0,05 (dualidad: θ ∈ IC si alguna pieza no rechaza θ; es el IC de V9 sin recorrer la rejilla); potencia = rechazo de θ = 0 con tau = −0,05 y con el MDE80 del pre-registro (−0,022). Sesgo y RMSE del estimador puntual (media de los 9 b_e posteriores) frente a θ.
- **Diagnóstico de la covarianza:** además del contraste con la covarianza estimada en cada réplica (la que usará H1), se repite con la covarianza verdadera (covarianza empírica de los coeficientes entre réplicas bajo el nulo, «Σ verdadera»). Si el tamaño solo falla con la estimada, el problema es la covarianza clusterizada por municipio (ignora la correlación espacial y los efectos comunes), no el contraste ARP.
- **Consistencia:** en 60 réplicas se comprueba que `honest_rr` (IC por inversión sobre rejilla, V9) contiene θ0 si y solo si el contraste por piezas no lo rechaza.
- **Criterio:** tamaño en [0,04; 0,06] con R = 2.000 (escenarios A y B, que son los casos frontera) y cobertura en [0,92; 0,97]. El pre-registro no nombra una inferencia alternativa para Honest DiD; la adenda (punto 13) exige además una segunda implementación independiente para sostener C3 (doble implementación: fuera de este encargo).
"""


def panel_h1():
    est = Pn.estructura_h1()
    return Pn.armar(est, "74"), est


def evento(P, g, tau, pend, exacta=False):
    Y, att = Pn.simular_h1(P, g, tau, SD_E, pt_exacta=exacta)
    T = Y.shape[1]
    tr, co = P["tr"], P["co"]
    if pend:
        Y = Y.copy()
        Y[tr] += pend * (np.arange(T) - REF)[None, :]
    D = Y - Y[:, [REF]]
    a_tr = D[tr]
    a_co = D[co]
    b = a_tr.mean(0) - a_co.mean(0)
    V = np.cov(a_tr.T) / len(tr) + np.cov(a_co.T) / len(co)
    ev = PRE_E + POST_E
    col = [REF + 1 + e for e in ev]      # e = t − 7 (el trimestre de referencia e = −1 es la columna REF = 6)
    bb = b[col]
    S = V[np.ix_(col, col)]
    res = {"es_orden": ev, "es": {e: (bb[i], float(np.sqrt(S[i, i]))) for i, e in enumerate(ev)}, "es_vcov": S}
    return res, att, float(bb[len(PRE_E):].mean())


def _piezas(res, Mbar):
    pre = sorted(e for e in res["es_orden"] if e < -1)
    post = sorted(e for e in res["es_orden"] if e >= 0)
    orden = pre + post
    idx = [res["es_orden"].index(e) for e in orden]
    b = np.array([res["es"][e][0] for e in orden])
    S = np.atleast_2d(res["es_vcov"])[np.ix_(idx, idx)]
    n_pre, n_post = len(pre), len(post)
    l = np.ones(n_post) / n_post
    Bm = np.linalg.svd(l[None, :])[2][1:].T
    pz = []
    for A in H._piezas_rm(n_pre, n_post, Mbar):
        SY = A @ S @ A.T
        pz.append((A @ b, A[:, n_pre:], A[:, n_pre:] @ Bm, np.sqrt(np.clip(np.diag(SY), 1e-14, None)), SY))
    return pz, n_post


def rechaza(res, Mbar, theta0, alfa=0.05):
    """Rechaza θ = θ0 si TODAS las piezas lo rechazan (misma lógica que `acepta` dentro de H.honest_rr)."""
    pz, n_post = _piezas(res, Mbar)
    for AB, Ap, X, sig, SY in pz:
        if not H._arp_condicional(AB - Ap @ (theta0 * np.ones(n_post)), X, sig, SY, alfa):
            return False
    return True


def _res(b, S):
    return {"es_orden": PRE_E + POST_E, "es": {e: (b[i], float(np.sqrt(S[i, i]))) for i, e in enumerate(PRE_E + POST_E)}, "es_vcov": S}


def bloque(P, gens, Mbar, pend, tau, theta_cero, consist, exacta=True):
    sal = []
    for g in gens:
        res, att, est = evento(P, g, tau, pend, exacta)
        th0 = 0.0 if theta_cero else att
        r = rechaza(res, Mbar, th0)
        extra = np.nan
        if consist:
            lo, hi = H.honest_rr(res, Mbar, rejilla=np.linspace(th0 - 0.03, th0 + 0.03, 25))
            dentro = (np.isfinite(lo)) and (lo <= th0 <= hi)
            extra = float(dentro == (not r))
        b = np.array([res["es"][e][0] for e in PRE_E + POST_E])
        sal.append([att, est, float(r), extra] + list(b) + list(res["es_vcov"].ravel()))
    return sal


def bloque_oracle(gens_b, Mbar, S_or, theta_cero):
    out = []
    for fila in gens_b:
        att = fila[0]
        b = np.array(fila[4:19])
        out.append(float(rechaza(_res(b, S_or), Mbar, 0.0 if theta_cero else att)))
    return out


def correr(P, esc_i, etapa, R, Mbar, pend, tau, theta_cero, jobs, consist=False, exacta=True):
    gens = C.flujos(K, R, esc_i * 10 + etapa)
    ch = [gens[i::40] for i in range(40)]
    sal = Parallel(n_jobs=jobs)(delayed(bloque)(P, c, Mbar, pend, tau, theta_cero, consist, exacta) for c in ch)
    res = [None] * R
    for i, b in enumerate(sal):
        for j, f in enumerate(b):
            res[i + j * 40] = f
    return np.array(res, float)


def oracle(M, Mbar, S_or, theta_cero, jobs):
    ch = [M[i::40] for i in range(40)]
    sal = Parallel(n_jobs=jobs)(delayed(bloque_oracle)(c, Mbar, S_or, theta_cero) for c in ch)
    out = np.empty(len(M))
    for i, b in enumerate(sal):
        out[i::40] = b
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--R", type=int, default=2000)
    ap.add_argument("--R_info", type=int, default=500)
    ap.add_argument("--R_pot", type=int, default=500)
    ap.add_argument("--jobs", type=int, default=4)
    a = ap.parse_args()
    C.declarar(HERR, DGP)
    P, _ = panel_h1()
    filas = []
    for i, (esc, (Mbar, pend, exacta, rol)) in enumerate(ESC.items()):
        R = a.R if rol == "verdad" else a.R_info
        t0 = time.time()
        Mn = correr(P, i, 1, R, Mbar, pend, 0.0, True, a.jobs, exacta=exacta)
        tam = float(Mn[:, 2].mean())
        Mc = correr(P, i, 2, R, Mbar, pend, TAU_REF, False, a.jobs, exacta=exacta)
        cob = 1 - float(Mc[:, 2].mean())
        Mp = correr(P, i, 3, a.R_pot, Mbar, pend, TAU_REF, True, a.jobs, exacta=exacta)
        Mm = correr(P, i, 4, a.R_pot, Mbar, pend, TAU_MDE, True, a.jobs, exacta=exacta)
        # diagnóstico: Σ verdadera (covarianza empírica de los coeficientes entre réplicas bajo el nulo) en lugar de la estimada
        S_or = np.cov(Mn[:, 4:19].T)
        tam_or = float(oracle(Mn, Mbar, S_or, True, a.jobs).mean())
        cob_or = 1 - float(oracle(Mc, Mbar, S_or, False, a.jobs).mean())
        e = Mc[:, 1] - Mc[:, 0]
        filas.append({"escenario": esc, "Mbar": Mbar, "pendiente": pend, "PT_exacta": exacta, "rol": rol, "R_nulo": R, "tamano_5pct": tam,
                      "cobertura_95": cob, "potencia_tau_-0.05": float(Mp[:, 2].mean()), "potencia_mde_-0.022": float(Mm[:, 2].mean()),
                      "tamano_Sigma_verdadera": tam_or, "cobertura_Sigma_verdadera": cob_or,
                      "sesgo": float(e.mean()), "rmse": float(np.sqrt((e ** 2).mean())), "segundos": time.time() - t0})
        print(filas[-1], flush=True)
    # consistencia honest_rr (grilla V9) frente al contraste por piezas
    Mcons = correr(P, 1, 5, 60, 1.0, PEND, 0.0, True, a.jobs, consist=True)
    cons = float(np.nanmean(Mcons[:, 3]))
    tab = pd.DataFrame(filas)
    v = {}
    for _, f in tab[tab.rol == "verdad"].iterrows():
        v[f.escenario] = C.veredicto(float(f.tamano_5pct), float(f.cobertura_95), int(f.R_nulo))
        v[f.escenario]["con_Sigma_verdadera"] = C.veredicto(float(f.tamano_Sigma_verdadera), float(f.cobertura_Sigma_verdadera), int(f.R_nulo))
    apto = all(x["apto"] for x in v.values())
    glob = "APTO (implementación V9)" if apto else "NO APTO → criterio M̄ solo descriptivo (no sostiene C3)"
    r = C.base_resultado("H1 (Honest DiD, Rambachan-Roth M̄)", {"tratados": 124, "donantes": 74, "pre": 6, "post": 9}, "Honest DiD, implementación propia de V9 (ARP condicional por piezas)")
    A, B = tab.iloc[0], tab.iloc[1]
    r["estimacion"] = {"tamano_A": float(A.tamano_5pct), "cobertura_A": float(A.cobertura_95), "tamano_A_Sigma_verdadera": float(A.tamano_Sigma_verdadera),
                       "tamano_B": float(B.tamano_5pct), "cobertura_B": float(B.cobertura_95), "potencia_B_tau005": float(B["potencia_tau_-0.05"]),
                       "potencia_B_mde": float(B["potencia_mde_-0.022"]), "sesgo_B": float(B.sesgo), "rmse_B": float(B.rmse)}
    r["ic95"] = C.ic_binomial(float(B.tamano_5pct), int(B.R_nulo))
    r["diagnosticos"] = {"veredicto": glob, "por_escenario": v, "consistencia_honest_rr_vs_piezas": cons, "R": a.R, "semilla": C.SEED,
                         "segunda_implementacion_independiente": "no disponible en este entorno (sin red para instalar HonestDiD); la adenda (punto 13) la exige para sostener C3"}
    r["notas"] = ["El pre-registro no nombra inferencia alternativa para Honest DiD.", "Cobertura = 1 − rechazo del verdadero θ (dualidad de la inversión del contraste).",
                  "La columna Sigma_verdadera aísla el contraste ARP del error de estimación de la covarianza (clusterizada por municipio, que ignora la correlación espacial)."]
    md = (f"## Resultados (R = {a.R} en A y B; {a.R_info} en C-F; potencia con {a.R_pot}; semilla {C.SEED}, k = {K})\n\n" + C.md_tabla(tab.drop(columns=["segundos"]))
          + f"\n**Consistencia** (60 réplicas, escenario B): coincidencia de `honest_rr` con el contraste por piezas = {cons:.3f}.\n\n**Veredicto: {glob}.**\n\n")
    for e_, x in v.items():
        md += f"- {e_}: {x['veredicto']} {('— ' + '; '.join(x['fallos'])) if x['fallos'] else ''} (con Σ verdadera: {x['con_Sigma_verdadera']['veredicto']})\n"
    C.cerrar(HERR, r, tab, md)
    print(tab.to_string())
    print(glob)


if __name__ == "__main__":
    main()
