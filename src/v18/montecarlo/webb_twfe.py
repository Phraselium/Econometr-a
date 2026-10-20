"""V18 · Monte Carlo del wild cluster bootstrap de Webb en TWFE con 8, 30 y 39 clusters. Simulación; sin datos reales.

Ejecución: python src/v18/montecarlo/webb_twfe.py [--R 2000] [--B 9999]   (SEED 20261010)

Proceso generador (declarado antes de simular)
- Panel balanceado de G clusters (provincias; G = 8, 30, 39) x T años (T = 14 en todos; T = 30 como sensibilidad para G = 39).
- Tratamiento escalonado: una fracción p de clusters (principal p = 0,5; sensibilidad con pocos tratados: 1 de 8, 3 de 30, 4 de 39)
  adopta en un año uniforme en [T/3, 2T/3]; D_gt = 1[t >= adopcion_g].
- y_gt = alpha_g + lambda_t + beta D_gt + e_gt. Los efectos fijos se absorben (no se simulan). Perturbación:
  e_gt = sigma_g (u_gt + sqrt(0,5) l_g f_t) con u AR(1) (rho = 0,5, varianza unitaria), f_t AR(1) (rho = 0,5), l_g ~ N(0,1)
  (dependencia transversal: factor común con cargas heterogéneas, que los efectos de tiempo no absorben) y sigma_g = exp(0,5 N(0,1))
  normalizado a media 1 (heterogeneidad de varianza entre clusters).
- Efecto nulo beta = 0; no nulo beta = 0,8. El modelo es equivariante a la traslación: el tamaño es la tasa de rechazo de H0: beta = beta_verdadero,
  la cobertura del IC por inversión es 1 menos esa tasa, y la potencia es la tasa de rechazo de H0: beta = 0 con beta = 0,8.
- Inferencia: CR1 por cluster con normal y con t(G-1); wild cluster bootstrap con H0 impuesta y pesos de Webb (B réplicas bootstrap, p simétrico).
"""
from __future__ import annotations

import argparse
import json
import os
import math
import sys
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats

RAIZ = Path(__file__).resolve().parents[3]


def _herr():
    """Carga la herramienta por ruta (mismo nombre de fichero que este script: no se puede importar por nombre)."""
    import importlib.util
    m = sys.modules.get("herr_webb_twfe")
    if m is None:
        spec = importlib.util.spec_from_file_location("herr_webb_twfe", RAIZ / "src" / "v18" / "herramientas" / "webb_twfe.py")
        m = importlib.util.module_from_spec(spec)
        sys.modules["herr_webb_twfe"] = m
        spec.loader.exec_module(m)
    return m


SEED = 20261010
ALCANCE_TERRITORIAL = "sin lectura de datos"
HERR = "webb_twfe"
ROTULO = "simulación; sin datos reales"
BETA_ALT = 0.8
SALIDA = RAIZ / "output" / "v18" / "montecarlo" / HERR


def veredicto(tam, cob, R):
    fallos = []
    if R < 1000:
        fallos.append(f"R={R} < 1.000")
    if not (0.03 <= tam <= 0.08):
        fallos.append(f"tamaño {tam:.4f} fuera de [0,03; 0,08]")
    if not (0.92 <= cob <= 0.97):
        fallos.append(f"cobertura {cob:.4f} fuera de [0,92; 0,97]")
    return ("APTO" if not fallos else "NO APTO"), fallos


def banda_adenda(tam, cob):
    if tam > 0.15 or tam < 0.02:
        return "no fiable"
    if 0.04 <= tam <= 0.06 and 0.93 <= cob <= 0.97:
        return "apta"
    return "con valor crítico corregido"


def ic_bin(p, n):
    e = 1.96 * math.sqrt(max(p * (1 - p), 1e-12) / n)
    return [round(max(p - e, 0.0), 4), round(min(p + e, 1.0), 4)]


def ar1(rng, G, T, rho):
    e = rng.standard_normal((G, T))
    out = np.empty((G, T))
    out[:, 0] = e[:, 0]
    for t in range(1, T):
        out[:, t] = rho * out[:, t - 1] + math.sqrt(1 - rho ** 2) * e[:, t]
    return out


def dgp(rng, G, T, n_trat):
    sig = np.exp(0.5 * rng.standard_normal(G))
    sig = sig / sig.mean()
    u = ar1(rng, G, T, 0.5)
    f = ar1(rng, 1, T, 0.5)[0]
    lam = rng.standard_normal(G)
    e = sig[:, None] * (u + math.sqrt(0.5) * lam[:, None] * f[None, :])
    D = np.zeros((G, T))
    tratados = rng.permutation(G)[:n_trat]
    for g in tratados:
        D[g, rng.integers(T // 3, 2 * T // 3 + 1):] = 1.0
    return e, D


def f_rep(rng, n, G, T, n_trat, B):
    """Por réplica: [beta_hat, se, rech_normal(H0=beta), rech_t, rech_webb(H0=beta), rech_normal(H0=0), rech_t(0), rech_webb(0)]
    con los datos generados con beta = BETA_ALT."""
    W = _herr()
    tc = stats.t.ppf(0.975, G - 1)
    out = np.empty((n, 8))
    for i in range(n):
        e, D = dgp(rng, G, T, n_trat)
        y = BETA_ALT * D + e
        p_v, t_v, b, se = W.wcr_webb(y, D, BETA_ALT, B, rng)
        p_0, t_0, _, _ = W.wcr_webb(y, D, 0.0, B, rng)
        out[i] = [b, se, abs(t_v) > 1.959964, abs(t_v) > tc, p_v < 0.05, abs(t_0) > 1.959964, abs(t_0) > tc, p_0 < 0.05]
    return out


def paralelo(k, R, **kw):
    from joblib import Parallel, delayed
    base, extra = divmod(R, 40)
    tr = [base + (1 if i < extra else 0) for i in range(40)]
    res = Parallel(n_jobs=int(os.environ.get("V18_MC_JOBS", "4")))(delayed(f_rep)(np.random.default_rng([SEED, k, i]), n, **kw) for i, n in enumerate(tr) if n > 0)
    return np.vstack(res)


def resumir(M, esc, R):
    filas = []
    for j, nom in enumerate(["CR1 (normal)", "CR1 (t de Student, G-1)", "wild cluster bootstrap (Webb)"]):
        tam, pot = float(M[:, 2 + j].mean()), float(M[:, 5 + j].mean())
        cob = 1.0 - tam
        d = {"inferencia": nom, "G": esc["G"], "T": esc["T"], "tratados": esc["n_trat"], "R": R, "B": esc["B"],
             "tamano_5pct": tam, "tamano_ic95": str(ic_bin(tam, R)), "cobertura_95": cob, "potencia": pot,
             "sesgo": float(np.mean(M[:, 0] - BETA_ALT)), "rmse": float(np.sqrt(np.mean((M[:, 0] - BETA_ALT) ** 2))),
             "principal": esc["principal"]}
        d["veredicto"] = veredicto(tam, cob, R)[0]
        d["banda_adenda_1_12"] = banda_adenda(tam, cob)
        filas.append(d)
    return filas


def escenarios(B):
    e = []
    for G, nt in ((8, 4), (30, 15), (39, 20)):
        e.append({"G": G, "T": 14, "n_trat": nt, "B": B, "principal": True})
    for G, nt in ((8, 1), (30, 3), (39, 4)):
        e.append({"G": G, "T": 14, "n_trat": nt, "B": B, "principal": False})
    e.append({"G": 39, "T": 30, "n_trat": 20, "B": B, "principal": False})
    return e


def main(R=2000, B=9999, salida=SALIDA, esc=None):
    esc = esc or escenarios(B)
    filas = []
    for k, e in enumerate(esc):
        M = paralelo(k, R, G=e["G"], T=e["T"], n_trat=e["n_trat"], B=e["B"])
        filas += resumir(M, e, len(M))
        print(e, flush=True)
    tab = pd.DataFrame(filas)
    escribir(tab, salida)
    return tab


def escribir(tab, salida):
    salida.mkdir(parents=True, exist_ok=True)
    tab.to_csv(salida / "tabla.csv", index=False)
    vg = {}
    for inf, g in tab[tab.principal].groupby("inferencia"):
        ok = g[g.veredicto == "APTO"]
        vg[inf] = {"veredicto": "APTO" if len(ok) == len(g) else ("NO APTO" if len(ok) == 0 else "APTO CONDICIONADO"),
                   "aptos": [f"G={r.G}" for r in ok.itertuples()],
                   "fallan": [f"G={r.G} (tamaño {r.tamano_5pct:.4f}, cobertura {r.cobertura_95:.4f})" for r in g[g.veredicto != "APTO"].itertuples()]}
    res = {"rama": "v18/montecarlo", "pregunta": "validación del wild cluster bootstrap de Webb en TWFE (E5, E6-R2, E7-A2, E8, E9, E12)",
           "capa": "validación de herramienta (sin capa de evidencia)", "datos": ROTULO,
           "N": "G = 8, 30, 39 clusters; T = 14 (y 30); tratamiento escalonado", "metodo": "TWFE con CR1 y WCR con pesos de Webb (H0 impuesta)",
           "estimacion": None, "ic95": None, "p_ajustado": None, "nivel_evidencia": "no aplica (validación Monte Carlo)",
           "diagnosticos": {"veredicto_por_inferencia": vg, "R": int(tab.R.min()), "B": int(tab.B.min()), "semilla": SEED,
                            "criterio": "tamaño [0,03; 0,08], cobertura [0,92; 0,97], R >= 2.000",
                            "bandas_adenda_1_12": {f"{r.inferencia} G={r.G} T={r.T} tratados={r.tratados}": r.banda_adenda_1_12 for r in tab.itertuples()},
                            "alcance_territorial": ALCANCE_TERRITORIAL},
           "fuera_muestra": {"modelo": None, "rmse": None, "dm_vs_ar4": None},
           "notas": [ROTULO, "Cobertura del IC por inversión = 1 - tasa de rechazo de H0: beta = beta verdadero (equivariancia)."]}
    (salida / "resultado.json").write_text(json.dumps(res, ensure_ascii=False, indent=2), encoding="utf-8")
    cols = ["inferencia", "G", "T", "tratados", "R", "B", "tamano_5pct", "cobertura_95", "potencia", "veredicto", "banda_adenda_1_12", "principal"]
    md = ["# Wild cluster bootstrap de Webb en TWFE · Monte Carlo V18", "", f"**{ROTULO}.** SEED {SEED}, R = {int(tab.R.min())}, B = {int(tab.B.min())}.", "",
          "Proceso generador: ver el docstring de src/v18/montecarlo/webb_twfe.py.", "", "## Resultados", "",
          tab[cols].round(4).to_markdown(index=False), "", "## Veredicto (escenarios principales: la mitad de los clusters tratados)", ""]
    for k, v in vg.items():
        md.append(f"- **{k}: {v['veredicto']}.** Aptos: {', '.join(v['aptos']) or 'ninguno'}. Fallan: {'; '.join(v['fallan']) or 'ninguno'}.")
    (salida / "informe.md").write_text("\n".join(md) + "\n", encoding="utf-8")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--R", type=int, default=2000)
    ap.add_argument("--B", type=int, default=9999)
    a = ap.parse_args()
    main(a.R, a.B)
