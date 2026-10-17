"""V15 fase 4.1 · Control sintético por municipio para los 10 tratados mayores de H1: inferencia por permutación (en el espacio).

Proceso generador declarado en docs/v15/validacion_montecarlo/control_sintetico.md ANTES de simular (el script lo escribe primero).
Uso: python src/v15/montecarlo/control_sintetico.py [--R 2000] [--R_alt 2000] [--R_mde 500] [--jobs 4]
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

HERR, K = "control_sintetico", 3
N_TR, N_CO = 10, 74
T_POST = 9
ESC = {"P7_heterogeneo": (7, True), "P7_intercambiable": (7, False), "P20_heterogeneo": (20, True)}
TAU_REF, TAU_MDE = -0.05, -0.022

DGP = """# control_sintetico · control sintético por municipio, 10 tratados mayores de H1, inferencia por permutación

Herramienta de V15 (preregistro_v15.md H1 prueba (vi), sección 6). Código: `src/v15/montecarlo/control_sintetico.py` y `_comun_panel_v15.py`; semilla `SeedSequence([20261010, 3, escenario*10+etapa]).spawn(R)`.

## Proceso generador (declarado antes de simular)
- **Estructura leída:** 10 municipios tratados de la cohorte 2024T1 (los 10 primeros del sorteo de 124 de `sdid_placebo_h1h2`; el tamaño real de población no se lee, se modela abajo) y los 74 donantes nunca tratados de ese mismo sorteo (códigos y centroides reales de Incasòl/geo). Calendario: 7 trimestres previos (2022T2-2023T4, adenda 1) y 9 posteriores (2024T1-2026T1); escenario P20: 20 trimestres previos (2019T1-2023T4, como en el texto de H1).
- **Resultado simulado (log renta):** el mismo del SDID de H1 (mu_i, tendencia propia d_i ~ N(0; 0,002²), dos factores comunes AR(1), campo espacial de 25 km, AR(1) ρ = 0,5), con sd_e = 0,05 × exp(0,5 z_i − 0,125) en los donantes. **Heterogeneidad por tamaño:** los 10 tratados mayores tienen la mitad de ruido idiosincrásico (sd_e × 0,5; ruido ∝ población^(−1/2)); en el escenario «intercambiable» tienen la misma distribución que los donantes (diagnóstico: aísla el efecto de la desigualdad de ruido).
- **Efecto:** nulo = 0; referencia = −0,05 con tau_i = tau(1 + 0,5 z_i) por municipio (la verdad de cobertura es el tau_i del municipio); potencia además con el MDE80 (−0,022).
- **Estimador por municipio:** control sintético con pesos en el símplex sobre los 74 donantes ajustados a la serie previa centrada por unidad (variante con efecto fijo de unidad, Doudchenko-Imbens / Ferman-Pinto, porque los niveles no están en el casco convexo); efecto = (media posterior − media previa) del tratado menos la combinación ponderada de los donantes.
- **Inferencia por permutación (en el espacio):** cada donante hace de tratado con los otros 73 (los 74 placebos se calculan una vez por réplica y se comparten entre los 10 tratados, como en la práctica). (a) p = (1 + #{|tau_j| ≥ |tau|})/75; (b) p con el cociente RMSPE posterior/previo (Abadie et al.). IC95 por inversión del contraste (a): tau ± cuantil 95 % de |tau_j|.
- **Nota de granularidad:** con 75 unidades, p ≤ 0,05 exige rango ≤ 3, es decir, un tamaño exacto máximo de 3/75 = 0,04 incluso con intercambiabilidad perfecta (es el borde inferior del criterio).
- **Medidas:** tamaño (rechazo al 5 % bajo el nulo, promedio de los 10 tratados), cobertura del tau_i del IC95, sesgo/RMSE de tau_i, potencia. R = 2.000 réplicas.
- **Criterio:** tamaño en [0,04; 0,06] y cobertura en [0,92; 0,97]. El pre-registro no nombra una inferencia alternativa para el control sintético; si la permutación no pasa, el control sintético queda descriptivo (la prueba (vi) no puede usarse como criterio de C3).
"""


def sc_pesos(Ypre, y_tr, co):
    """Pesos SC en el símplex; Ypre (n, T0) con filas centradas; devuelve w sobre las filas `co`."""
    A = Ypre[co] - Ypre[co].mean(1, keepdims=True)
    t = y_tr - y_tr.mean()
    return Pn._pesos(A, t, 1e-8 * (A ** 2).sum() / A.shape[0], its=60)


def un_sc(Y, i, co, T0):
    Ypre, Ypost = Y[:, :T0], Y[:, T0:]
    w = sc_pesos(Ypre, Ypre[i], co)
    gap_pre = Ypre[i] - w @ Ypre[co]
    gap_post = Ypost[i] - w @ Ypost[co]
    tau = gap_post.mean() - gap_pre.mean()
    rm_pre = np.sqrt(((gap_pre - gap_pre.mean()) ** 2).mean())
    rm_post = np.sqrt((gap_post ** 2).mean())
    return tau, rm_post / max(rm_pre, 1e-8)


def estructura():
    est = Pn.estructura_h1()
    cods = est["tr"][:N_TR] + est["co"]
    xy = est["coords"].loc[cods, ["lat", "lon"]].to_numpy()
    return {"cods": cods, "xy": xy, "L25": C.cholesky_exp(xy, 25.0), "L60": C.cholesky_exp(xy, 60.0), "n": len(cods)}


def simular(P, g, tau, T0, hetero):
    n, T = P["n"], T0 + T_POST
    f = C.ar1(g, 2, T, 0.6, 0.03)
    g1 = g.normal(1.0, 0.5, n)
    g2 = P["L60"] @ g.standard_normal(n)
    z = g.standard_normal(n)
    esc = np.exp(0.5 * z - 0.125)
    if hetero:
        esc[:N_TR] *= 0.5
    y = (g.normal(0, 1, n)[:, None] + g.normal(0, 0.002, n)[:, None] * np.arange(T)[None, :]
         + g1[:, None] * f[0][None, :] + g2[:, None] * f[1][None, :])
    y += P["L25"] @ C.ar1(g, n, T, 0.5, 0.02)
    y += C.ar1(g, n, T, 0.5, 0.05, escala=esc)
    tau_i = tau * (1 + 0.5 * g.standard_normal(N_TR))
    y[:N_TR, T0:] += tau_i[:, None]
    return y, tau_i


def una(P, g, tau, T0, hetero):
    Y, tau_i = simular(P, g, tau, T0, hetero)
    donantes = np.arange(N_TR, P["n"])
    pl = np.array([un_sc(Y, j, donantes[donantes != j], T0) for j in donantes])
    pl_tau, pl_rat = pl[:, 0], pl[:, 1]
    q = np.quantile(np.abs(pl_tau), 0.95)
    out = []
    for i in range(N_TR):
        t, rat = un_sc(Y, i, donantes, T0)
        p_a = (1 + np.sum(np.abs(pl_tau) >= abs(t))) / (len(donantes) + 1)
        p_b = (1 + np.sum(pl_rat >= rat)) / (len(donantes) + 1)
        out.append([tau_i[i], t, t - q, t + q, float(p_a <= 0.05), float(p_b <= 0.05)])
    return out


def bloque(P, gens, tau, T0, hetero):
    return [una(P, g, tau, T0, hetero) for g in gens]


def correr(P, esc_i, etapa, R, tau, T0, hetero, jobs):
    gens = C.flujos(K, R, esc_i * 10 + etapa)
    ch = [gens[i::40] for i in range(40)]
    sal = Parallel(n_jobs=jobs)(delayed(bloque)(P, c, tau, T0, hetero) for c in ch)
    res = [None] * R
    for i, b in enumerate(sal):
        for j, f in enumerate(b):
            res[i + j * 40] = f
    return np.array(res, float)   # (R, 10, 6)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--R", type=int, default=2000)
    ap.add_argument("--R_alt", type=int, default=2000)
    ap.add_argument("--R_mde", type=int, default=500)
    ap.add_argument("--jobs", type=int, default=4)
    a = ap.parse_args()
    C.declarar(HERR, DGP)
    P = estructura()
    filas = []
    for i, (esc, (T0, het)) in enumerate(ESC.items()):
        t0 = time.time()
        Mn = correr(P, i, 1, a.R, 0.0, T0, het, a.jobs)
        Mr = correr(P, i, 2, a.R_alt, TAU_REF, T0, het, a.jobs)
        Mm = correr(P, i, 3, a.R_mde, TAU_MDE, T0, het, a.jobs)
        f = lambda M, j: M[:, :, j].reshape(-1)
        dres = C.resumen(f(Mr, 1), f(Mr, 2), f(Mr, 3), f(Mr, 4), f(Mr, 0))
        e = f(Mr, 1) - f(Mr, 0)
        filas.append({"escenario": esc, "T_pre": T0, "R_nulo": a.R,
                      "tamano_perm_tau": float(f(Mn, 4).mean()), "tamano_perm_rmspe": float(f(Mn, 5).mean()),
                      "cobertura_ic_perm": dres["cobertura"], "potencia_ref_tau": float(f(Mr, 4).mean()), "potencia_ref_rmspe": float(f(Mr, 5).mean()),
                      "potencia_mde_tau": float(f(Mm, 4).mean()), "sesgo": float(e.mean()), "rmse": float(np.sqrt((e ** 2).mean())),
                      "tam_trat_1_mayor": float(Mn[:, 0, 4].mean()), "tam_trat_10": float(Mn[:, 9, 4].mean()), "segundos": time.time() - t0})
        print(filas[-1], flush=True)
    tab = pd.DataFrame(filas)
    v = {}
    for _, r_ in tab.iterrows():
        v[r_.escenario] = {"perm_tau": C.veredicto(float(r_.tamano_perm_tau), float(r_.cobertura_ic_perm), int(r_.R_nulo)),
                           "perm_rmspe": C.veredicto(float(r_.tamano_perm_rmspe), None, int(r_.R_nulo))}
    pr = v["P7_heterogeneo"]["perm_tau"]
    glob = "APTO (permutación)" if pr["apto"] else "NO APTO → control sintético solo descriptivo"
    p0 = tab.iloc[0]
    r = C.base_resultado("H1 (control sintético, 10 tratados mayores)", {"tratados": N_TR, "donantes": N_CO, "T_pre": 7, "T_post": 9}, "control sintético con efecto fijo + permutación en el espacio")
    r["estimacion"] = {"tamano": float(p0.tamano_perm_tau), "tamano_rmspe": float(p0.tamano_perm_rmspe), "cobertura": float(p0.cobertura_ic_perm),
                       "potencia_ref": float(p0.potencia_ref_tau), "potencia_mde": float(p0.potencia_mde_tau), "sesgo": float(p0.sesgo), "rmse": float(p0.rmse)}
    r["ic95"] = C.ic_binomial(float(p0.tamano_perm_tau), a.R * N_TR)
    r["diagnosticos"] = {"veredicto": glob, "por_escenario": v, "R": a.R, "semilla": C.SEED}
    r["notas"] = ["Veredicto sobre el escenario P7_heterogeneo (preperiodo de la adenda 1).", "Tamaño exacto máximo con 75 unidades: 3/75 = 0,04."]
    md = (f"## Resultados (R = {a.R} nulo, {a.R_alt} cobertura, {a.R_mde} MDE; 10 tratados por réplica; semilla {C.SEED}, k = {K})\n\n" + C.md_tabla(tab.drop(columns=["segundos"]))
          + f"\n**Veredicto: {glob}.**\n\n")
    for e_, x in v.items():
        for nm, y in x.items():
            md += f"- {e_} / {nm}: {y['veredicto']} {('— ' + '; '.join(y['fallos'])) if y['fallos'] else ''}\n"
    C.cerrar(HERR, r, tab, md)
    print(glob)


if __name__ == "__main__":
    main()
