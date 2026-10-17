"""V15 fase 4.1 · Wild cluster bootstrap de Webb con el número de clusters de H1/H2 (198 municipios; 36 provincias en R-IPVA) y de H4 (38 provincias).

Proceso generador declarado en docs/v15/validacion_montecarlo/wild_webb_v15.md ANTES de simular (el script lo escribe primero).
Uso: python src/v15/montecarlo/wild_webb_v15.py [--R 2000] [--B 9999] [--jobs 4]
"""
from __future__ import annotations

import argparse
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd
from joblib import Parallel, delayed
from scipy import stats

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
sys.path.insert(0, str(Path(__file__).resolve().parent))
from src.v15.montecarlo import _comun_v15 as C  # noqa: E402
from src.v15.montecarlo import _comun_panel_v15 as Pn  # noqa: E402
from src.v15.montecarlo import akm_municipal as AK  # noqa: E402
import sdid_placebo_h1h2 as SD  # noqa: E402

HERR, K = "wild_webb_v15", 8
ESC = ["W1_H1H2_198municipios", "W2_H4_38provincias", "W3_RIPVA_36provincias_pocos_tratados"]
TAU_REF = {"W1_H1H2_198municipios": -0.05, "W2_H4_38provincias": 0.004, "W3_RIPVA_36provincias_pocos_tratados": -0.02}
TAU_MDE = {"W1_H1H2_198municipios": -0.022, "W2_H4_38provincias": 0.003, "W3_RIPVA_36provincias_pocos_tratados": -0.04}

DGP = """# wild_webb_v15 · wild cluster bootstrap de Webb

Herramienta de V15 (preregistro_v15.md H1/H2 «pocos clusters con wild cluster bootstrap de pesos Webb», sección 6; adenda 1 punto 5 y adenda 2 B). Código: `src/v15/montecarlo/wild_webb_v15.py` (usa `_comun_panel_v15`, `sdid_placebo_h1h2.estructura_s4` y `akm_municipal`); semilla `SeedSequence([20261010, 8, escenario*10+etapa]).spawn(R)`.

## Proceso generador (declarado antes de simular)
- **W1 (H1/H2):** 124 tratados de la cohorte 2024T1 y 74 nunca tratados (códigos y centroides reales de Incasòl/geo), 7 trimestres previos y 9 posteriores; clusters = municipio (G = 198). Resultado simulado con el proceso de `sdid_placebo_h1h2` (factores comunes AR(1), campo espacial de 25 km, AR(1) ρ = 0,5, sd_e = 0,05 heterogénea). Efecto en los 9 trimestres posteriores de los tratados: nulo = 0; referencia = −0,05 con tau_i = tau(1 + 0,5 z_i); MDE80 = −0,022. Estimador: MCO con efectos de municipio y trimestre (TWFE) del indicador tratado × posterior (el estimador del pre-registro es SDID/CS; aquí se valida la inferencia de Webb, que es común a los tres).
- **W2 (H4):** estructura de `akm_municipal` (1.451 municipios, 28 orígenes, cuotas 2003 reales, T = 11, provincia × año absorbidos), clusters = provincia (G = 38, muy desiguales: la más grande concentra ≈ 10 % de los municipios). Forma reducida y_it = β_rf z_it + ε_it con el error con dependencia por cuota y factor común de `akm_municipal` (σ_y = 0,05). Nulo β_rf = 0; referencia β_rf = 0,004 (≈ 0,01 × primera etapa 0,39); MDE 0,003.
- **W3 (R-IPVA, adenda 2 B):** 124 municipios tratados y 382 donantes (estructura de S4 de `sdid_placebo_h1h2`: tratados en las pocas provincias con zona, donantes en provincias sin zona), 9 años previos y 1 posterior; clusters = provincia (G ≈ 36, de ellos ≈ 5 tratados: pocos clusters tratados). Mismo proceso de S4 (choque provincia-año AR(1)). Efecto de referencia −0,02, MDE −0,04. TWFE con efectos de municipio y año.
- **Inferencias comparadas:** (a) wild cluster bootstrap-t de Webb (6 puntos) con nulo impuesto (WCR) para el contraste y no impuesto (WCU) para el IC95 percentil-t; (b) error agrupado CR1 con t(G − 1) como referencia. B = 9.999 réplicas bootstrap (como en V15; el cierre algebraico por cluster hace barato usar más de 999) y, como sensibilidad, B = 999 con las primeras 999 columnas.
- **Cierre algebraico:** como el efecto fijo de unidad está anidado en el cluster, el estadístico bootstrap se calcula sobre sumas por cluster (sin rehacer la regresión por réplica); es exactamente la regresión bootstrap con los residuos reponderados (Roodman et al., 2019), con los efectos de tiempo recentrados.
- **Medidas:** tamaño (rechazo de β = 0 con tau = 0), cobertura del IC95 bajo la referencia (verdad = ATT muestral en W1 y W3, β_rf en W2), potencia (referencia y MDE), sesgo y RMSE. R = 2.000.
- **Criterio:** tamaño en [0,04; 0,06] y cobertura en [0,92; 0,97] para Webb. El pre-registro no nombra alternativa; si falla, «NO APTO → inferencia solo descriptiva».
"""


def twfe_estadisticos(dt, yt, cl, G):
    """Cantidades por cluster de la regresión de yt sobre dt (ambos doblemente centrados) con clusters cl."""
    sdd = (dt ** 2).sum()
    beta = (dt * yt).sum() / sdd
    e = yt - beta * dt
    s = np.bincount(cl, weights=(dt * e).sum(1), minlength=G)
    se = np.sqrt((s ** 2).sum() * G / (G - 1)) / sdd
    return beta, e, sdd, se


def agg(cl, G, M):
    out = np.zeros((G,) + M.shape[1:])
    np.add.at(out, cl, M)
    return out


def boot_t(dt, r, cl, G, V, sdd, timefe, n):
    """t* = (b* - b_ref)/se* para y* = M(v_g r) + (b_ref dt): devuelve el vector de t* (B,). r (n,T) es el residuo (restringido o no)."""
    Ag = agg(cl, G, (dt * r).sum(1))          # (G,)
    Dg = agg(cl, G, (dt ** 2).sum(1))
    db = (V * Ag[:, None]).sum(0) / sdd         # b* - b_ref  (B,)
    corr = np.zeros_like(V)
    if timefe:
        Yg = agg(cl, G, r)                      # (G, T)
        dg = agg(cl, G, dt)                     # (G, T)
        W = (Yg.T @ V) / n                      # (T, B): media de columna del residuo reponderado
        corr = dg @ W                           # (G, B)
    sg = V * Ag[:, None] - corr - db[None, :] * Dg[:, None]
    se = np.sqrt((sg ** 2).sum(0) * G / (G - 1)) / sdd
    return db / np.maximum(se, 1e-15)


def inferencia(dt, yt, cl, G, g, B, timefe, truth):
    n = dt.shape[0]
    beta, e, sdd, se = twfe_estadisticos(dt, yt, cl, G)
    tc = stats.t.ppf(0.975, G - 1)
    t_obs = beta / se
    V = C.webb(g, (G, B))
    ts0 = boot_t(dt, yt, cl, G, V, sdd, timefe, n)      # nulo impuesto: residuo restringido = yt (β = 0)
    p = float(np.mean(np.abs(ts0) >= abs(t_obs)))
    p999 = float(np.mean(np.abs(ts0[:999]) >= abs(t_obs)))
    ts1 = boot_t(dt, e, cl, G, V, sdd, timefe, n)       # no impuesto: residuo estimado
    c = float(np.quantile(np.abs(ts1), 0.95))
    c999 = float(np.quantile(np.abs(ts1[:999]), 0.95))
    return [truth, beta, beta - c * se, beta + c * se, float(p <= 0.05), float(p999 <= 0.05), beta - c999 * se, beta + c999 * se,
            beta - tc * se, beta + tc * se, float(abs(t_obs) > tc)]


def dm2(a):
    return a - a.mean(1, keepdims=True) - a.mean(0, keepdims=True) + a.mean()


def rep_w1(P, g, tau, B):
    Y, att = Pn.simular_h1(P, g, tau, 0.05)
    n, T = Y.shape
    D = np.zeros((n, T))
    D[np.ix_(P["tr"], Pn.POST)] = 1.0
    return inferencia(dm2(D), dm2(Y), P["cl"], n, g, B, True, att)


def rep_w3(P, g, tau, B):
    Y, att = SD.sim_s4(P, g, tau, 0.02)
    n, T = Y.shape
    D = np.zeros((n, T))
    D[np.ix_(P["tr"], [T - 1])] = 1.0
    return inferencia(dm2(D), dm2(Y), P["cl"], int(P["cl"].max()) + 1, g, B, True, att)


def rep_w2(D, g, beta, B):
    gk, z, x, eps = AK.lote(g, 1, D, 0.39)
    y = beta * z + SD_Y * eps
    zt, yt = D.dm_prov(z)[0], D.dm_prov(y)[0]
    cl = np.repeat(np.arange(D.G), D.cnt)
    return inferencia(zt, yt, cl, D.G, g, B, False, beta)


SD_Y = 1.0   # eps ya incorpora σ_y = 0,05 en akm_municipal.lote


def bloque(esc, P, gens, tau, B):
    f = {"W1_H1H2_198municipios": rep_w1, "W2_H4_38provincias": rep_w2, "W3_RIPVA_36provincias_pocos_tratados": rep_w3}[esc]
    return [f(P, g, tau, B) for g in gens]


def correr(esc, P, R, tau, B, etapa, i, jobs):
    gens = C.flujos(K, R, i * 10 + etapa)
    ch = [gens[j::40] for j in range(40)]
    sal = Parallel(n_jobs=jobs)(delayed(bloque)(esc, P, c, tau, B) for c in ch)
    res = [None] * R
    for a, b in enumerate(sal):
        for j, f in enumerate(b):
            res[a + j * 40] = f
    return np.array(res, float)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--R", type=int, default=2000)
    ap.add_argument("--B", type=int, default=9999)
    ap.add_argument("--R_pot", type=int, default=1000)
    ap.add_argument("--jobs", type=int, default=4)
    a = ap.parse_args()
    C.declarar(HERR, DGP)
    est = Pn.estructura_h1()
    S, orig = AK.estructura()
    Ps = {ESC[0]: Pn.armar(est, "74"), ESC[1]: AK.Dis(S, orig, orig), ESC[2]: SD.estructura_s4()}
    filas, ver = [], {}
    for i, esc in enumerate(ESC):
        P = Ps[esc]
        t0 = time.time()
        Mn = correr(esc, P, a.R, 0.0, a.B, 1, i, a.jobs)
        Mr = correr(esc, P, a.R, TAU_REF[esc], a.B, 2, i, a.jobs)
        Mm = correr(esc, P, a.R_pot, TAU_MDE[esc], a.B, 3, i, a.jobs)
        seg = time.time() - t0
        for nm, (jr, jl, jh) in {"Webb WCR/WCU B=9999": (4, 2, 3), "Webb B=999": (5, 6, 7), "CR1 t(G-1)": (10, 8, 9)}.items():
            d = C.resumen(Mr[:, 1], Mr[:, jl], Mr[:, jh], Mr[:, jr], Mr[:, 0])
            filas.append({"escenario": esc, "inferencia": nm, "G": (P.G if esc == ESC[1] else (int(P["cl"].max()) + 1)), "R": a.R,
                          "tamano_5pct": float(Mn[:, jr].mean()), "cobertura_95": d["cobertura"], "potencia_ref": float(Mr[:, jr].mean()),
                          "potencia_mde": float(Mm[:, jr].mean()), "sesgo": d["sesgo"], "rmse": d["rmse"], "ancho_ic": d["ancho_medio_ic"], "segundos": seg})
        print(esc, round(seg), flush=True)
    tab = pd.DataFrame(filas)
    for _, f in tab.iterrows():
        ver.setdefault(f.escenario, {})[f.inferencia] = C.veredicto(float(f.tamano_5pct), float(f.cobertura_95), int(f.R))
    glob = {e: ("APTO (Webb)" if v["Webb WCR/WCU B=9999"]["apto"] else "NO APTO → inferencia solo descriptiva") for e, v in ver.items()}
    p = tab[(tab.escenario == ESC[0]) & (tab.inferencia == "Webb WCR/WCU B=9999")].iloc[0]
    r = C.base_resultado("H1/H2 y H4 (wild cluster bootstrap de Webb)", {"G_H1H2": 198, "G_H4": 38, "G_RIPVA": int(Ps[ESC[2]]["cl"].max()) + 1}, "wild cluster bootstrap-t de Webb, nulo impuesto; IC percentil-t no impuesto")
    r["estimacion"] = {"tamano_W1": float(p.tamano_5pct), "cobertura_W1": float(p.cobertura_95), "potencia_W1": float(p.potencia_ref),
                       "por_escenario": {e: {k: float(v) for k, v in tab[(tab.escenario == e) & (tab.inferencia == 'Webb WCR/WCU B=9999')].iloc[0][["tamano_5pct", "cobertura_95", "potencia_ref", "potencia_mde", "sesgo", "rmse"]].items()} for e in ESC}}
    r["ic95"] = C.ic_binomial(float(p.tamano_5pct), a.R)
    r["diagnosticos"] = {"veredicto_por_escenario": glob, "por_inferencia": ver, "B": a.B, "R": a.R, "semilla": C.SEED,
                         "nota_B": "V15 usa 9.999 réplicas; el cierre algebraico por cluster permite usar el mismo B en el Monte Carlo"}
    r["notas"] = ["La verdad de cobertura en W1 y W3 es el ATT muestral (tau_i heterogéneo); en W2, β_rf."]
    md = (f"## Resultados (R = {a.R} por etapa; B = {a.B}; semilla {C.SEED}, k = {K})\n\n" + C.md_tabla(tab.drop(columns=["segundos"]))
          + "\n**Veredictos (Webb B = 9.999)**\n\n" + "\n".join(f"- {e}: **{g}**" for e, g in glob.items()) + "\n\n")
    for e, v in ver.items():
        for nm, x in v.items():
            md += f"- {e} / {nm}: {x['veredicto']} {('— ' + '; '.join(x['fallos'])) if x['fallos'] else ''}\n"
    C.cerrar(HERR, r, tab, md)
    print(tab.to_string())
    print(glob)


if __name__ == "__main__":
    main()
