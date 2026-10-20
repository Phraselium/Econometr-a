"""V18 · Monte Carlo de Driscoll-Kraay en paneles provinciales con T de 14 a 30. Simulación; sin datos reales.

Ejecución: python src/v18/montecarlo/driscoll_kraay.py [--R 2000]   (SEED 20261010)

Proceso generador (declarado antes de simular)
- N = 39 provincias no selladas, T en {14, 20, 30} años. Modelo FE: y_it = a_i + beta x_it + e_it.
- Regresor: x_it = lx_i fx_t + nu_it, con nu_it AR(1) (rho = 0,5) y fx_t AR(1) (rho_f); e_it = sigma_i (le_i fe_t + eps_it), eps AR(1) (rho = 0,5),
  fe_t AR(1) (rho_f), cargas lx_i, le_i ~ N(1; 0,5^2) y factores fx, fe independientes (dependencia transversal fuerte por factores comunes
  con cargas heterogéneas); sigma_i = exp(0,5 N(0,1)) normalizada a media 1 (heterogeneidad). Pocos periodos, N = 39 clusters de unidad.
- Principal: solo efectos fijos de unidad, rho_f = 0,5. Sensibilidad: rho_f = 0,8; efectos de año además de los de unidad; T = 200 como referencia de calibración (DK converge al 5 % solo con T grande).
- Efecto nulo beta = 0; no nulo beta = 0,3. El estimador FE es equivariante a la traslación de beta: potencia = rechazo de H0: beta = -0,3
  con los datos de beta = 0; cobertura = 1 - tamaño.
- Inferencia: Driscoll-Kraay con ancho m = floor(4 (T/100)^(2/9)) (xtscc) y con m = floor(T^(1/3)) + 1, t de Student con T-1 gl; referencias:
  cluster por provincia (CR1, t con N-1 gl) y HC1 (normal).
"""
from __future__ import annotations

import argparse
import importlib.util
import json
import os
import math
import sys
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats

RAIZ = Path(__file__).resolve().parents[3]
SEED = 20261010
ALCANCE_TERRITORIAL = "sin lectura de datos"
HERR = "driscoll_kraay"
ROTULO = "simulación; sin datos reales"
N_PROV = 39
DELTA = 0.3
SALIDA = RAIZ / "output" / "v18" / "montecarlo" / HERR


def _herr():
    """Carga la herramienta por ruta (mismo nombre de fichero que este script: no se puede importar por nombre)."""
    m = sys.modules.get("herr_driscoll_kraay")
    if m is None:
        spec = importlib.util.spec_from_file_location("herr_driscoll_kraay", RAIZ / "src" / "v18" / "herr18" / "driscoll_kraay.py")
        m = importlib.util.module_from_spec(spec)
        sys.modules["herr_driscoll_kraay"] = m
        spec.loader.exec_module(m)
    return m


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


def ar1(rng, n, T, rho):
    e = rng.standard_normal((n, T))
    out = np.empty((n, T))
    out[:, 0] = e[:, 0]
    for t in range(1, T):
        out[:, t] = rho * out[:, t - 1] + math.sqrt(1 - rho ** 2) * e[:, t]
    return out


def dgp(rng, T, rho_f):
    lx = 1 + 0.5 * rng.standard_normal(N_PROV)
    le = 1 + 0.5 * rng.standard_normal(N_PROV)
    sig = np.exp(0.5 * rng.standard_normal(N_PROV))
    sig /= sig.mean()
    fx, fe = ar1(rng, 1, T, rho_f)[0], ar1(rng, 1, T, rho_f)[0]
    x = lx[:, None] * fx[None, :] + ar1(rng, N_PROV, T, 0.5)
    e = sig[:, None] * (le[:, None] * fe[None, :] + ar1(rng, N_PROV, T, 0.5))
    return x, e


def f_rep(rng, n, T, rho_f, tiempo):
    H = _herr()
    m1 = H.ancho_por_defecto(T)
    m2 = int(np.floor(T ** (1 / 3))) + 1
    tT = stats.t.ppf(0.975, T - 1)
    tN = stats.t.ppf(0.975, N_PROV - 1)
    out = np.empty((n, 1 + 4 * 2))
    for i in range(n):
        x, e = dgp(rng, T, rho_f)
        r1 = H.fe_dk(e, x[:, :, None], m1, tiempo)       # y = e (beta = 0)
        r2 = H.fe_dk(e, x[:, :, None], m2, tiempo)
        b = float(r1["beta"][0])
        ses = [math.sqrt(r1["V_dk"][0, 0]), math.sqrt(r2["V_dk"][0, 0]), math.sqrt(r1["V_cluster"][0, 0]), math.sqrt(r1["V_hc1"][0, 0])]
        crit = [tT, tT, tN, 1.959964]
        row = [b]
        for s, c in zip(ses, crit):
            row += [abs(b) / s > c, abs(b + DELTA) / s > c]
        out[i] = row
    return out


def paralelo(k, R, **kw):
    from joblib import Parallel, delayed
    base, extra = divmod(R, 40)
    tr = [base + (1 if i < extra else 0) for i in range(40)]
    res = Parallel(n_jobs=int(os.environ.get("V18_MC_JOBS", "4")))(delayed(f_rep)(np.random.default_rng([SEED, k, i]), n, **kw) for i, n in enumerate(tr) if n > 0)
    return np.vstack(res)


def resumir(M, esc, R):
    filas = []
    T = esc["T"]
    nombres = [f"Driscoll-Kraay (m = {int(np.floor(4 * (T / 100.0) ** (2.0 / 9.0)))}, t de T-1 gl)", f"Driscoll-Kraay (m = {int(np.floor(T ** (1 / 3))) + 1}, t de T-1 gl)",
               "cluster por provincia (CR1, t de N-1 gl)", "HC1 (normal, referencia)"]
    for j, nom in enumerate(nombres):
        tam, pot = float(M[:, 1 + 2 * j].mean()), float(M[:, 2 + 2 * j].mean())
        d = {"inferencia": nom, "T": T, "rho_f": esc["rho_f"], "efectos_ano": esc["tiempo"], "R": R, "tamano_5pct": tam, "tamano_ic95": str(ic_bin(tam, R)),
             "cobertura_95": 1 - tam, "potencia": pot, "sesgo": float(M[:, 0].mean()), "rmse": float(np.sqrt(np.mean(M[:, 0] ** 2))),
             "principal": esc["principal"]}
        d["veredicto"] = veredicto(tam, 1 - tam, R)[0]
        d["banda_adenda_1_12"] = banda_adenda(tam, 1 - tam)
        filas.append(d)
    return filas


ESCENARIOS = ([{"T": T, "rho_f": 0.5, "tiempo": False, "principal": True} for T in (14, 20, 30)]
              + [{"T": T, "rho_f": 0.8, "tiempo": False, "principal": False} for T in (14, 30)]
              + [{"T": T, "rho_f": 0.5, "tiempo": True, "principal": False} for T in (14, 30)]
              + [{"T": 200, "rho_f": 0.5, "tiempo": False, "principal": False}])   # referencia de calibración (T grande)


def main(R=2000, salida=SALIDA, esc=None):
    esc = esc or ESCENARIOS
    filas = []
    for k, e in enumerate(esc):
        M = paralelo(k, R, T=e["T"], rho_f=e["rho_f"], tiempo=e["tiempo"])
        filas += resumir(M, e, len(M))
        print(e, flush=True)
    tab = pd.DataFrame(filas)
    escribir(tab, salida)
    return tab


def escribir(tab, salida):
    salida.mkdir(parents=True, exist_ok=True)
    tab.to_csv(salida / "tabla.csv", index=False)
    vg = {}
    pr = tab[tab.principal]
    pr = pr.assign(familia=pr.inferencia.str.replace(r"\(m = \d+, ", "(m = ancho, ", regex=True))
    for inf, g in pr.groupby("familia"):
        ok = g[g.veredicto == "APTO"]
        vg[inf] = {"veredicto": "APTO" if len(ok) == len(g) else ("NO APTO" if len(ok) == 0 else "APTO CONDICIONADO"),
                   "aptos": [f"T={r.T}" for r in ok.itertuples()],
                   "fallan": [f"T={r.T} (tamaño {r.tamano_5pct:.4f}, cobertura {r.cobertura_95:.4f})" for r in g[g.veredicto != "APTO"].itertuples()]}
    res = {"rama": "v18/montecarlo", "pregunta": "validación de Driscoll-Kraay en paneles provinciales (E3, E5, E7-A2, E8, E12, F1-F3)",
           "capa": "validación de herramienta (sin capa de evidencia)", "datos": ROTULO, "N": f"{N_PROV} provincias; T = 14, 20, 30",
           "metodo": "FE con errores de Driscoll-Kraay (Bartlett, t de T-1 gl); referencias CR1 y HC1",
           "estimacion": None, "ic95": None, "p_ajustado": None, "nivel_evidencia": "no aplica (validación Monte Carlo)",
           "diagnosticos": {"veredicto_por_inferencia": vg, "R": int(tab.R.min()), "semilla": SEED,
                            "criterio": "tamaño [0,03; 0,08], cobertura [0,92; 0,97], R >= 2.000",
                            "bandas_adenda_1_12": {f"{r.inferencia} T={r.T} rho_f={r.rho_f} año={r.efectos_ano}": r.banda_adenda_1_12 for r in tab.itertuples()},
                            "alcance_territorial": ALCANCE_TERRITORIAL},
           "fuera_muestra": {"modelo": None, "rmse": None, "dm_vs_ar4": None},
           "notas": [ROTULO, "Cobertura = 1 - tamaño por equivariancia; potencia frente a 0,3."]}
    (salida / "resultado.json").write_text(json.dumps(res, ensure_ascii=False, indent=2), encoding="utf-8")
    cols = ["inferencia", "T", "rho_f", "efectos_ano", "R", "tamano_5pct", "cobertura_95", "potencia", "veredicto", "banda_adenda_1_12", "principal"]
    md = ["# Driscoll-Kraay en paneles provinciales · Monte Carlo V18", "", f"**{ROTULO}.** SEED {SEED}.", "",
          "Proceso generador: ver el docstring de src/v18/montecarlo/driscoll_kraay.py.", "", "## Resultados", "",
          tab[cols].round(4).to_markdown(index=False), "", "## Veredicto (escenarios principales)", ""]
    for k, v in vg.items():
        md.append(f"- **{k}: {v['veredicto']}.** Aptos: {', '.join(v['aptos']) or 'ninguno'}. Fallan: {'; '.join(v['fallan']) or 'ninguno'}.")
    (salida / "informe.md").write_text("\n".join(md) + "\n", encoding="utf-8")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--R", type=int, default=2000)
    main(ap.parse_args().R)
