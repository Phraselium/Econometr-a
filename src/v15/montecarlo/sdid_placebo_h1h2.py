"""V15 fase 4.1 · SDID con error típico por bootstrap de placebo (principal, H1/H2) y wild cluster bootstrap de Webb (alternativa de la adenda).

Proceso generador declarado en docs/v15/validacion_montecarlo/sdid_placebo_h1h2.md ANTES de simular (el script lo escribe primero).
Uso: python src/v15/montecarlo/sdid_placebo_h1h2.py [--R 2000] [--R_alt 2000] [--R_mde 400] [--B 99] [--jobs 4]
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

HERR, K = "sdid_placebo_h1h2", 1
B_WILD = 999
ESCENARIOS = {  # nombre: (resultado, donantes, sd_e, tau_ref, tau_mde)
    "S1_H1_74donantes": ("H1 log renta", "74", 0.05, -0.05, -0.022),
    "S2_H1_14donantes_10km": ("H1 log renta", "14", 0.05, -0.05, -0.022),
    "S3_H2_74donantes": ("H2 log(1+contratos)", "74", 0.15, -0.13, -0.039),
    "S4_IPVA_provincias": ("R-IPVA log IPVA", "382", 0.02, -0.02, -0.04),
}

DGP = """# sdid_placebo_h1h2 · SDID con placebo (H1/H2) y variante IPVA (adenda 2, B)

Herramienta de V15 (preregistro_v15.md sección 6; adenda 1 punto 13). Código: `src/v15/montecarlo/sdid_placebo_h1h2.py` y `_comun_panel_v15.py`; semilla `SeedSequence([20261010, 1, escenario*10+etapa]).spawn(R)` (una réplica = un generador).

## Proceso generador (declarado antes de simular)
**Estructura leída (códigos, calendario, geometría; ningún valor de resultado):** municipios catalanes de entrenamiento con renta de Incasòl (611), cohortes de `regulacion_zonas` (2024T1: 128; 2024T4: 113; nunca tratados: 370) y centroides de `data/base/geo`. Se toman 124 tratados de la cohorte 2024T1 (234 × 128/241, del recuento de la adenda 1) y 74 donantes nunca tratados al azar (el filtro de ≥ 5 contratos no se reproduce porque exigiría leer el número de contratos); la variante de 10 km usa los 14 donantes de esos 74 a ≥ 10 km de cualquier municipio tratado (la adenda cuenta 13).
Calendario (adenda 1, puntos 1 y 6): 7 trimestres previos (2022T2-2023T4; pesos de SDID con los 5 primeros) y 9 posteriores (2024T1-2026T1), ATT = media de los 9.
**Resultado simulado (log):** y_it = mu_i + d_i t + g1_i f1_t + g2_i f2_t + s_it + e_it + efecto.
- mu_i ~ N(0,1); d_i ~ N(0; 0,002²) por trimestre (heterogeneidad de tendencia no relacionada con el tratamiento).
- f1, f2 factores comunes AR(1) con ρ = 0,6 y sd 0,03 (dependencia transversal); g1_i ~ N(1; 0,5²); g2_i = campo espacial exponencial (alcance 60 km) N(0,1).
- s_it: campo espacial exp(-d/25 km), AR(1) ρ = 0,5, sd 0,02 (correlación espacial por distancia entre centroides reales).
- e_it: AR(1) ρ = 0,5 con sd marginal sd_e × exp(0,5 z_i − 0,125) (heterogeneidad entre municipios; sd_e = 0,05 en H1, 0,15 en H2). Valores declarados, no estimados con datos reales.
**Efecto (solo tratados, 9 trimestres posteriores):** nulo = 0. Alternativa de referencia = −0,05 (H1; literatura citada en el pre-registro) y −0,13 (H2), con heterogeneidad tau_i = tau (1 + 0,5 z_i); la verdad de la cobertura es el ATT muestral (media de tau_i). Potencia además frente al MDE80 del pre-registro (−0,022 en H1; −0,039 en H2).
**Escenarios:** S1 (H1, 124 tratados y 74 donantes), S2 (H1, 14 donantes a ≥ 10 km), S3 (H2, 74 donantes, más ruido) y S4 (variante R-IPVA, ver abajo).
**S4 (adenda 2, B):** panel anual 2015-2023 (9 previos) + 2024 (1 posterior), 124 municipios tratados con zona vigente en 2024 (cualquier CCAA, códigos de `regulacion_zonas` presentes en el entrenamiento) y 382 donantes de provincias sin zona (al azar entre los municipios de entrenamiento con SERPAVI); clusters = provincia. Mismo proceso con sd_e = 0,02, más un choque provincia-año AR(1) (ρ = 0,5, sd 0,015), efecto de referencia −0,02 (diluido: el IPVA mide el stock de contratos), MDE −0,04.

## Inferencias
- **Principal (preregistro H1):** error típico por bootstrap de placebo (Arkhangelsky et al., alg. 4), IC normal ± 1,96 SE. En el Monte Carlo B = 99 réplicas de placebo (el pre-registro usa 1.000: se reduce por coste, 45 min; con B = 99 el SE tiene un error relativo ≈ 7 %). El algoritmo literal reasigna N_tr = 124 donantes como tratados: **no es computable con 74 o 14 donantes**. Se reportan dos variantes de diagnóstico con m = N_co/2 placebo-tratados: sin reescalar y reescalada por sqrt(m/N_tr). No cuentan como la inferencia principal.
- **Alternativa nombrada en la adenda 1 (punto 5):** wild cluster bootstrap-t de Webb por municipio sobre la puntuación SDID (pesos fijos; 999 réplicas; nulo impuesto). En S4 es la inferencia especificada (clusters = provincia; adenda 2, B).
- Para S1-S3 la inferencia principal es la del placebo; si no es computable o no pasa, se prueba solo Webb; si tampoco, «NO APTO → diseño solo descriptivo».
- Criterio: tamaño al 5 % en [0,04; 0,06] con R = 2.000 bajo el nulo y cobertura del IC 95 % en [0,92; 0,97] bajo la alternativa de referencia. Potencia, sesgo y RMSE informados.
"""


def estructura_s4(k: int = 4) -> dict:
    import pandas as pd
    g = C.rng(K, k)
    ce = C.centroides()
    p10 = pd.read_parquet(C.P15 / "p10_espacial.parquet", columns=["territorio_codigo", "nivel", "variable"])
    pool = sorted(set(p10[(p10.nivel == "municipio") & (p10.variable == "serpavi_alquiler_m2_mediana")].territorio_codigo.astype(str).str.zfill(5)) & set(ce.index))
    r = pd.read_parquet(C.RAIZ / "data" / "base" / "regulacion_zonas.parquet", columns=["cod_ine_municipio"])
    zc = set(r.cod_ine_municipio.astype(str).str.zfill(5))
    ptr = sorted(set(pool) & zc) + sorted(set(C.estructura_cataluna()["todos_trat"]))
    ptr = sorted(set(ptr))
    n_tr = min(124, len(ptr))
    tr = sorted(g.choice(ptr, n_tr, replace=False))
    provs_tr = {c[:2] for c in zc}
    pco = [c for c in pool if c[:2] not in provs_tr and c not in zc]
    co = sorted(g.choice(pco, min(382, len(pco)), replace=False))
    cods = tr + co
    xy = ce.loc[cods, ["lat", "lon"]].to_numpy()
    prov = np.array([c[:2] for c in cods])
    return {"cods": cods, "tr": np.arange(len(tr)), "co": np.arange(len(tr), len(cods)), "n": len(cods), "xy": xy,
            "L25": C.cholesky_exp(xy, 25.0), "L60": C.cholesky_exp(xy, 60.0), "cl": np.unique(prov, return_inverse=True)[1],
            "n_prov_tr": len(set(prov[:len(tr)])), "n_prov_co": len(set(prov[len(tr):]))}


def sim_s4(P, g, tau, sd_e):
    n, T = P["n"], 10
    f = C.ar1(g, 2, T, 0.6, 0.03)
    g1 = g.normal(1.0, 0.5, n)
    g2 = P["L60"] @ g.standard_normal(n)
    y = (g.normal(0, 1, n)[:, None] + g.normal(0, 0.002, n)[:, None] * np.arange(T)[None, :]
         + g1[:, None] * f[0][None, :] + g2[:, None] * f[1][None, :])
    y += P["L25"] @ C.ar1(g, n, T, 0.5, 0.02)
    y += C.ar1(g, int(P["cl"].max()) + 1, T, 0.5, 0.015)[P["cl"]]
    z = g.standard_normal(n)
    y += C.ar1(g, n, T, 0.5, sd_e, escala=np.exp(0.5 * z - 0.125))
    tau_i = tau * (1 + 0.5 * g.standard_normal(len(P["tr"])))
    y[np.ix_(P["tr"], [T - 1])] += tau_i[:, None]
    return y, float(tau_i.mean())


def una_rep(P, g, esc, tau, sd_e, B):
    if esc.startswith("S4"):
        Y, att = sim_s4(P, g, tau, sd_e)
        pre, post = list(range(9)), [9]
    else:
        Y, att = Pn.simular_h1(P, g, tau, sd_e)
        pre, post = Pn.PESOS_PRE, Pn.POST
    tr, co = P["tr"], P["co"]
    t, om, lam, s = Pn.sdid(Y, tr, co, pre, post)
    fila = [att, t]
    if esc.startswith("S4"):
        fila += [np.nan] * 9
    else:
        m = len(tr)
        if len(co) - m >= 5:
            se_l, _, _ = Pn.placebo_se(Y, tr, co, g, B, m)
        else:
            se_l = np.nan
        mm = max(len(co) // 2, 2)
        se_m, _, _ = Pn.placebo_se(Y, tr, co, g, B, mm)
        se_e = se_m * np.sqrt(mm / len(tr)) if np.isfinite(se_m) else np.nan
        for se in (se_l, se_m, se_e):
            fila += [t - 1.96 * se, t + 1.96 * se, float(abs(t) > 1.96 * se) if np.isfinite(se) else np.nan]
    p, lo, hi, _ = Pn.wild_webb(None, t, om, s, tr, co, P["cl"], g, B_WILD)
    fila += [lo, hi, float(p <= 0.05)]
    return fila


def bloque(P, gens, esc, tau, sd_e, B):
    return [una_rep(P, g, esc, tau, sd_e, B) for g in gens]


def correr(P, esc, R, tau, sd_e, B, etapa, jobs):
    idx = list(esc_ids).index(esc) * 10 + etapa
    gens = C.flujos(K, R, idx)
    ch = [gens[i::40] for i in range(40)]
    sal = Parallel(n_jobs=jobs)(delayed(bloque)(P, c, esc, tau, sd_e, B) for c in ch)
    res = [None] * R
    for i, b in enumerate(sal):
        for j, f in enumerate(b):
            res[i + j * 40] = f
    return np.array(res, float)


esc_ids = list(ESCENARIOS)
INFS = [("placebo_literal", 2), ("placebo_m_sin_escalar", 5), ("placebo_m_escalado", 8), ("webb_cluster", 11)]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--R", type=int, default=2000)
    ap.add_argument("--R_alt", type=int, default=2000)
    ap.add_argument("--R_mde", type=int, default=400)
    ap.add_argument("--B", type=int, default=99)
    ap.add_argument("--jobs", type=int, default=4)
    ap.add_argument("--escenarios", default=",".join(ESCENARIOS))
    a = ap.parse_args()
    C.declarar(HERR, DGP)
    est = Pn.estructura_h1()
    Ps = {"S1_H1_74donantes": Pn.armar(est, "74"), "S3_H2_74donantes": Pn.armar(est, "74")}
    est3 = dict(est)
    est3["co_lejos"] = [c for c, d in zip(est["co"], est["dmin_km"]) if d >= 10]
    Ps["S2_H1_14donantes_10km"] = Pn.armar(est3, "14")   # armar() usa co_lejos cuando donantes != "74"
    Ps["S4_IPVA_provincias"] = estructura_s4()
    filas, info = [], {}
    for esc in a.escenarios.split(","):
        _, don, sd_e, tref, tmde = ESCENARIOS[esc]
        P = Ps[esc]
        info[esc] = {"n_tratados": int(len(P["tr"])), "n_donantes": int(len(P["co"]))}
        if esc.startswith("S4"):
            info[esc].update({"provincias_tratadas": P["n_prov_tr"], "provincias_donantes": P["n_prov_co"]})
        for nom, R, tau, et in (("nulo", a.R, 0.0, 1), ("ref", a.R_alt, tref, 2), ("mde", a.R_mde, tmde, 3)):
            t0 = time.time()
            M = correr(P, esc, R, tau, sd_e, a.B, et, a.jobs)
            seg = time.time() - t0
            for nm, j in INFS:
                if esc.startswith("S4") and nm != "webb_cluster":
                    continue
                d = C.resumen(M[:, 1], M[:, j], M[:, j + 1], M[:, j + 2], M[:, 0])
                filas.append({"escenario": esc, "inferencia": nm, "efecto": nom, "tau": tau, **info[esc], **d, "segundos": seg})
            print(esc, nom, R, round(seg), flush=True)
    tab = pd.DataFrame(filas)
    ver, glob = {}, []
    for esc in a.escenarios.split(","):
        t = tab[tab.escenario == esc]
        v = {}
        for nm, _ in INFS:
            q = t[t.inferencia == nm]
            if q.empty:
                continue
            nu, rf = q[q.efecto == "nulo"].iloc[0], q[q.efecto == "ref"].iloc[0]
            if nu.R_validas < nu.R * 0.99 or not np.isfinite(nu.rechazo):
                v[nm] = {"veredicto": "NO APTO", "apto": False, "fallos": ["no computable (N donantes <= N tratados + 5)"]}
            else:
                v[nm] = C.veredicto(float(nu.rechazo), float(rf.cobertura), int(nu.R_validas))
        ver[esc] = v
        if esc.startswith("S4"):
            f = "APTO (Webb por provincia)" if v["webb_cluster"]["apto"] else "NO APTO → diseño solo descriptivo"
        elif v["placebo_literal"]["apto"]:
            f = "APTO (placebo)"
        elif v["webb_cluster"]["apto"]:
            f = "alternativa APTA (Webb por municipio)"
        else:
            f = "NO APTO → diseño solo descriptivo"
        glob.append((esc, f))
    r = C.base_resultado("H1/H2 (SDID, preregistro_v15 sección 6)", {"tratados": int(len(Ps['S1_H1_74donantes']['tr'])), "donantes": [74, 14, 382], "T_pre": 7, "T_post": 9}, "SDID con error típico por placebo; alternativa Webb")
    r["estimacion"] = {esc: {nm: {"tamano": float(tab[(tab.escenario == esc) & (tab.inferencia == nm) & (tab.efecto == 'nulo')].rechazo.iloc[0]),
                                  "cobertura": float(tab[(tab.escenario == esc) & (tab.inferencia == nm) & (tab.efecto == 'ref')].cobertura.iloc[0]),
                                  "potencia_ref": float(tab[(tab.escenario == esc) & (tab.inferencia == nm) & (tab.efecto == 'ref')].rechazo.iloc[0]),
                                  "potencia_mde": float(tab[(tab.escenario == esc) & (tab.inferencia == nm) & (tab.efecto == 'mde')].rechazo.iloc[0]),
                                  "sesgo": float(tab[(tab.escenario == esc) & (tab.inferencia == nm) & (tab.efecto == 'ref')].sesgo.iloc[0]),
                                  "rmse": float(tab[(tab.escenario == esc) & (tab.inferencia == nm) & (tab.efecto == 'ref')].rmse.iloc[0])}
                           for nm in ver[esc]} for esc in ver}
    r["diagnosticos"] = {"veredictos_por_inferencia": ver, "veredicto_por_escenario": dict(glob), "R": a.R, "R_alt": a.R_alt, "R_mde": a.R_mde,
                         "B_placebo": a.B, "B_webb": B_WILD, "estructura": info, "semilla": C.SEED,
                         "n_donantes_a_10km_entre_74": int(est["n_donantes_mas_10km_entre_74"])}
    r["notas"] = ["El placebo literal exige N_donantes > N_tratados; con 74 o 14 donantes y 124 tratados no es computable.",
                  "B_placebo = 99 en el Monte Carlo (V15 usa 1.000); Webb con 999 réplicas."]
    md = f"## Resultados (R nulo = {a.R}, R ref = {a.R_alt}, R mde = {a.R_mde}; B placebo = {a.B}; Webb {B_WILD}; semilla {C.SEED}, k = {K})\n\n" + C.md_tabla(tab.drop(columns=["tau", "n_tratados", "n_donantes"]).rename(columns={"rechazo": "rechazo(tamaño|potencia)"}))
    md += "\n**Veredictos**\n\n" + "\n".join(f"- {e}: **{f}**" for e, f in glob) + "\n"
    for e, v in ver.items():
        for nm, x in v.items():
            md += f"- {e} / {nm}: {x['veredicto']} {('— ' + '; '.join(x['fallos'])) if x['fallos'] else ''}\n"
    C.cerrar(HERR, r, tab, md)
    print(tab.to_string())
    print(glob)


if __name__ == "__main__":
    main()
